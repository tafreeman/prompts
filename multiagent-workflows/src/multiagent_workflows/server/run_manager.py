from __future__ import annotations

import asyncio
import time
import uuid
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional

from multiagent_workflows.evaluation.scorer import ExecutionScorer

from .benchmarks import FALLBACK_BENCHMARKS, try_get_repo_benchmarks
from .dataset_loader import load_tasks


@dataclass
class ItemScore:
    """Scoring metrics for a single item."""
    exact_match: bool = False
    similarity: float = 0.0
    normalized_similarity: float = 0.0
    total_score: float = 0.0
    grade: str = "F"
    passed: bool = False
    feedback: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "exact_match": self.exact_match,
            "similarity": round(self.similarity, 4),
            "normalized_similarity": round(self.normalized_similarity, 4),
            "total_score": round(self.total_score, 2),
            "grade": self.grade,
            "passed": self.passed,
            "feedback": self.feedback,
        }


@dataclass
class RunItemResult:
    task_id: str
    status: str
    before: str
    gold: str
    after: str
    error: Optional[str] = None
    score: Optional[Dict[str, Any]] = None


def _now_ms() -> int:
    return int(time.time() * 1000)


def _task_before(task: Dict[str, Any]) -> str:
    return (
        task.get("prompt")
        or task.get("problem_statement")
        or task.get("issue_text")
        or ""
    )


def _task_gold(task: Dict[str, Any]) -> str:
    # HumanEval: canonical_solution
    # MBPP: code
    # SWE-bench: patch
    return (
        task.get("canonical_solution")
        or task.get("code")
        or task.get("patch")
        or task.get("golden_patch")
        or task.get("expected_output")
        or ""
    )


def _default_prompt_for_model(benchmark_id: str, task: Dict[str, Any]) -> str:
    if benchmark_id.startswith("swe-bench"):
        return (
            "You are fixing a real-world GitHub issue. "
            "Return ONLY a unified diff patch.\n\n"
            f"Repository: {task.get('repo', '')}\n\n"
            f"Issue:\n{_task_before(task)}\n"
        )

    # HumanEval / MBPP style
    test = task.get("test") or ""
    entry = task.get("entry_point") or ""
    test_list = task.get("test_list")
    if isinstance(test_list, list) and test_list:
        test = "\n".join(test_list)

    return (
        "Write Python code to solve the task. "
        "Return ONLY code (no markdown fences).\n\n"
        f"Task:\n{_task_before(task)}\n\n"
        + (f"Entry point: {entry}\n\n" if entry else "")
        + (f"Tests:\n{test}\n" if test else "")
    )


def _try_generate_with_llm(model: str, prompt: str) -> str:
    # Optional integration with the repo's LLM client.
    # If not configured, callers should catch exceptions and record them.
    from tools.llm.llm_client import LLMClient  # type: ignore

    return LLMClient.generate_text(model_name=model, prompt=prompt)


def _score_item(after: str, gold: str, pass_threshold: float = 70.0) -> ItemScore:
    """
    Score a generated output against the gold standard.

    Metrics:
    - exact_match: True if output == gold (after normalization)
    - similarity: SequenceMatcher ratio (0.0 - 1.0)
    - normalized_similarity: similarity * 100 (0.0 - 100.0)
    - total_score: weighted score (currently = normalized_similarity)
    - grade: letter grade (A/B/C/D/F)
    - passed: True if total_score >= pass_threshold
    """
    # Normalize whitespace for comparison
    after_norm = " ".join(after.split())
    gold_norm = " ".join(gold.split())

    exact_match = after_norm == gold_norm

    # Similarity using SequenceMatcher (same as WorkflowEvaluator)
    similarity = SequenceMatcher(None, after_norm, gold_norm).ratio()
    normalized_similarity = similarity * 100.0

    # Total score (can be extended with more metrics)
    total_score = normalized_similarity

    # Grade
    if total_score >= 90:
        grade = "A"
    elif total_score >= 80:
        grade = "B"
    elif total_score >= 70:
        grade = "C"
    elif total_score >= 60:
        grade = "D"
    else:
        grade = "F"

    passed = total_score >= pass_threshold

    # Feedback
    if exact_match:
        feedback = "Exact match with gold standard."
    elif passed:
        feedback = f"Passed with {total_score:.1f}% similarity."
    else:
        feedback = f"Did not pass. Similarity: {total_score:.1f}% (threshold: {pass_threshold}%)."

    return ItemScore(
        exact_match=exact_match,
        similarity=similarity,
        normalized_similarity=normalized_similarity,
        total_score=total_score,
        grade=grade,
        passed=passed,
        feedback=feedback,
    )


def _truncate_text(text: str, max_len: int = 4000) -> str:
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."


def _get_evaluation_method(benchmark_id: str) -> str:
    repo_defs = try_get_repo_benchmarks()
    if repo_defs and benchmark_id in repo_defs:
        return getattr(repo_defs[benchmark_id], "evaluation_method", "pass@1")
    if benchmark_id in FALLBACK_BENCHMARKS:
        return FALLBACK_BENCHMARKS[benchmark_id].evaluation_method
    return "pass@1"


class RunStore:
    """In-memory run store + background execution."""

    def __init__(self) -> None:
        self._runs: Dict[str, Dict[str, Any]] = {}
        self._tasks: Dict[str, asyncio.Task] = {}

        # Directory for autosaving results
        from pathlib import Path
        self._results_dir = Path(__file__).resolve().parents[3] / "evaluations" / "results"
        self._results_dir.mkdir(parents=True, exist_ok=True)

    def create_run(
        self,
        *,
        benchmark_id: str,
        task_ids: List[str],
        workflow: str,
        model: Optional[str],
        use_cache: bool,
    ) -> str:
        run_id = uuid.uuid4().hex
        evaluation_method = _get_evaluation_method(benchmark_id)
        self._runs[run_id] = {
            "run_id": run_id,
            "benchmark_id": benchmark_id,
            "workflow": workflow,
            "model": model,
            "evaluation_method": evaluation_method,
            "status": "queued",
            "created_at_ms": _now_ms(),
            "updated_at_ms": _now_ms(),
            "total": len(task_ids),
            "completed": 0,
            "items": [],
            "errors": [],
            # Aggregate scoring
            "scoring": self._init_scoring_state(evaluation_method, len(task_ids)),
        }

        task = asyncio.create_task(
            self._execute_run(
                run_id=run_id,
                benchmark_id=benchmark_id,
                task_ids=task_ids,
                workflow=workflow,
                model=model,
                use_cache=use_cache,
            )
        )
        self._tasks[run_id] = task
        return run_id

    def _init_scoring_state(self, evaluation_method: str, total_items: int) -> Dict[str, Any]:
        if evaluation_method == "execution":
            return {
                "evaluation_method": evaluation_method,
                "total_items": total_items,
                "scored_items": 0,
                "resolved_items": 0,
                "resolved_rate": 0.0,
                "avg_duration_ms": 0.0,
                "execution_errors": 0,
            }

        return {
            "evaluation_method": evaluation_method,
            "pass_threshold": 70.0,
            "total_items": total_items,
            "scored_items": 0,
            "passed_items": 0,
            "exact_matches": 0,
            "avg_similarity": 0.0,
            "avg_score": 0.0,
            "pass_rate": 0.0,
        }

    def get_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        return self._runs.get(run_id)

    async def shutdown(self) -> None:
        for t in list(self._tasks.values()):
            t.cancel()
        await asyncio.gather(*self._tasks.values(), return_exceptions=True)

    async def _execute_run(
        self,
        *,
        run_id: str,
        benchmark_id: str,
        task_ids: List[str],
        workflow: str,
        model: Optional[str],
        use_cache: bool,
    ) -> None:
        run = self._runs[run_id]
        run["status"] = "running"
        run["updated_at_ms"] = _now_ms()

        evaluation_method = run.get("evaluation_method", _get_evaluation_method(benchmark_id))
        execution_scorer = ExecutionScorer() if evaluation_method == "execution" else None

        print(f"[RunStore] Starting run {run_id} (benchmark={benchmark_id}, model={model}, workflow={workflow})")

        try:
            loaded = load_tasks(benchmark_id=benchmark_id, limit=None, offset=0, use_cache=use_cache)
            by_id = {str(t.get("task_id")): t for t in loaded.tasks}

            ordered_tasks: List[Dict[str, Any]] = []
            for tid in task_ids:
                t = by_id.get(str(tid))
                if t:
                    ordered_tasks.append(t)

            # Execute sequentially for now.
            for t in ordered_tasks:
                tid = str(t.get("task_id"))
                before = _task_before(t)
                gold = _task_gold(t)

                try:
                    if model:
                        prompt = _default_prompt_for_model(benchmark_id, t)
                        after = _try_generate_with_llm(model, prompt)
                        status = "generated"
                    else:
                        after = gold
                        status = "baseline_gold"

                    if evaluation_method == "execution" and execution_scorer:
                        exec_result = execution_scorer.score_task(t, after)
                        item_score = {
                            "resolved": exec_result.resolved,
                            "return_code": exec_result.return_code,
                            "duration_ms": round(exec_result.duration_ms, 2),
                            "stdout": _truncate_text(exec_result.stdout),
                            "stderr": _truncate_text(exec_result.stderr),
                            "error": exec_result.error,
                            "test_command": exec_result.test_command,
                        }

                        if exec_result.error:
                            run["errors"].append({"task_id": tid, "error": exec_result.error})
                    else:
                        # Score the output against gold
                        item_score = _score_item(after, gold, pass_threshold=run["scoring"]["pass_threshold"]).to_dict()

                    item = RunItemResult(
                        task_id=tid,
                        status=status,
                        before=before,
                        gold=gold,
                        after=after,
                        score=item_score,
                    )
                    run["items"].append(item.__dict__)
                    if evaluation_method == "execution":
                        print(f"[RunStore] [{run_id}] Task {tid}: status={status}, resolved={item_score.get('resolved')}, return_code={item_score.get('return_code')}")
                    else:
                        print(f"[RunStore] [{run_id}] Task {tid}: status={status}, score={item_score.get('total_score', 0):.1f}%, grade={item_score.get('grade')}, passed={item_score.get('passed')}")
                except Exception as e:
                    item = RunItemResult(
                        task_id=tid,
                        status="error",
                        before=before,
                        gold=gold,
                        after="",
                        error=str(e),
                    )
                    run["items"].append(item.__dict__)
                    run["errors"].append({"task_id": tid, "error": str(e)})
                    print(f"[RunStore] [{run_id}] Task {tid}: ERROR {e}")

                run["completed"] = len(run["items"])
                run["updated_at_ms"] = _now_ms()

                # Yield control so polling clients see progress.
                await asyncio.sleep(0)

            run["status"] = "completed" if not run["errors"] else "completed_with_errors"
            run["updated_at_ms"] = _now_ms()

            # Compute aggregate scoring
            scored_items = [it for it in run["items"] if it.get("score")]
            if scored_items:
                run["scoring"]["scored_items"] = len(scored_items)
                if evaluation_method == "execution":
                    resolved_items = sum(1 for it in scored_items if it["score"].get("resolved"))
                    run["scoring"]["resolved_items"] = resolved_items
                    run["scoring"]["resolved_rate"] = round(resolved_items / len(scored_items) * 100, 2)
                    run["scoring"]["avg_duration_ms"] = round(
                        sum(it["score"].get("duration_ms", 0) for it in scored_items) / len(scored_items), 2
                    )
                    run["scoring"]["execution_errors"] = sum(1 for it in scored_items if it["score"].get("error"))
                else:
                    run["scoring"]["passed_items"] = sum(1 for it in scored_items if it["score"].get("passed"))
                    run["scoring"]["exact_matches"] = sum(1 for it in scored_items if it["score"].get("exact_match"))
                    run["scoring"]["avg_similarity"] = round(
                        sum(it["score"].get("similarity", 0) for it in scored_items) / len(scored_items), 4
                    )
                    run["scoring"]["avg_score"] = round(
                        sum(it["score"].get("total_score", 0) for it in scored_items) / len(scored_items), 2
                    )
                    run["scoring"]["pass_rate"] = round(
                        run["scoring"]["passed_items"] / len(scored_items) * 100, 2
                    )

            if evaluation_method == "execution":
                print(f"[RunStore] [{run_id}] Scoring summary: "
                      f"resolved_rate={run['scoring'].get('resolved_rate', 0)}%, "
                      f"resolved_items={run['scoring'].get('resolved_items', 0)}/{run['scoring'].get('scored_items', 0)}, "
                      f"execution_errors={run['scoring'].get('execution_errors', 0)}")
            else:
                print(f"[RunStore] [{run_id}] Scoring summary: "
                      f"pass_rate={run['scoring']['pass_rate']}%, "
                      f"avg_score={run['scoring']['avg_score']}%, "
                      f"exact_matches={run['scoring']['exact_matches']}/{run['scoring']['scored_items']}")

            # Autosave result to disk
            import json
            out_path = self._results_dir / f"run_{run_id}.json"
            with out_path.open("w", encoding="utf-8") as f:
                json.dump(run, f, ensure_ascii=False, indent=2)
            print(f"[RunStore] Saved run {run_id} to {out_path}")

        except asyncio.CancelledError:
            run["status"] = "cancelled"
            run["updated_at_ms"] = _now_ms()
            raise
        except Exception as e:
            run["status"] = "failed"
            run["updated_at_ms"] = _now_ms()
            run["errors"].append({"error": str(e)})
            print(f"[RunStore] [{run_id}] FAILED: {e}")
