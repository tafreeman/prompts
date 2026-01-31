from __future__ import annotations

import asyncio
import time
import uuid
import asyncio
import time
import uuid
import re
import json
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional

from multiagent_workflows.evaluation.scorer import ExecutionScorer
from tools.agents.workflow_runner import WorkflowExecutor

from .benchmarks import FALLBACK_BENCHMARKS, try_get_repo_benchmarks
from .dataset_loader import load_tasks

# Map UI workflow IDs to their configuration names
UI_WORKFLOW_MAP = {
    "fullstack": "end_to_end",
    "bugfix": "defect_resolution",
    "architecture": "system_design",
    "refactoring": "end_to_end",  # Placeholder
}


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
    breakdown: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "exact_match": self.exact_match,
            "similarity": round(self.similarity, 4),
            "normalized_similarity": round(self.normalized_similarity, 4),
            "total_score": round(self.total_score, 2),
            "grade": self.grade,
            "passed": self.passed,
            "feedback": self.feedback,
            "breakdown": self.breakdown,
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
    steps: Optional[List[Dict[str, Any]]] = None  # Agent execution steps


def _now_ms() -> int:
    return int(time.time() * 1000)


def _task_before(task: Dict[str, Any]) -> str:
    return (
        task.get("prompt")
        or task.get("problem_statement")
        or task.get("issue_text")
        or ""
    )


def _extract_code_block(text: str) -> str:
    """Extract the last code block from text, or return text if none found."""
    # Try to find python blocks first
    matches = re.findall(r"```python\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if matches:
        return matches[-1].strip()
    
    # Fallback to any code block
    matches = re.findall(r"```\s*(.*?)```", text, re.DOTALL)
    if matches:
        return matches[-1].strip()
        
    return text.strip()



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


_RUBRICS_CACHE = None

def _load_rubrics() -> Dict[str, Any]:
    global _RUBRICS_CACHE
    if _RUBRICS_CACHE is not None:
        return _RUBRICS_CACHE
    
    try:
        # parent of server -> multiagent_workflows -> src -> root
        rubrics_path = Path(__file__).resolve().parents[3] / "config" / "rubrics.yaml"
        if rubrics_path.exists():
            with open(rubrics_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                _RUBRICS_CACHE = data.get("rubrics", {})
        else:
            print(f"[RunStore] Warning: Rubrics file not found at {rubrics_path}")
            _RUBRICS_CACHE = {}
    except Exception as e:
        print(f"[RunStore] Failed to load rubrics: {e}")
        _RUBRICS_CACHE = {}
    
    return _RUBRICS_CACHE

def _get_rubric_text(workflow_id: str) -> str:
    rubrics = _load_rubrics()
    
    # Map workflow ID to rubric key
    key_map = {
        "fullstack": "fullstack_generation",
        "bugfix": "bug_fixing",
        "architecture": "architecture_evolution",
        "refactoring": "legacy_refactoring"
    }
    
    rubric_key = key_map.get(workflow_id, "fullstack_generation") # Default
    rubric_data = rubrics.get(rubric_key)
    
    if rubric_data:
        return yaml.dump(rubric_data, sort_keys=False)
    return ""


def _judge_with_llm(model: str, task_desc: str, gold: str, actual: str, workflow_id: str = "fullstack") -> ItemScore:
    """Use an LLM to judge the correctness of the generated code."""
    from tools.llm.llm_client import LLMClient
    
    rubric_text = _get_rubric_text(workflow_id)
    
    prompt = f"""You are an expert Senior Technical Lead and Grader.

Task Description:
{task_desc}

Reference Solution (For FUNCTIONAL comparison only):
{gold}

Candidate Solution (Generated):
{actual}

RUBRIC CONFIGURATION:
{rubric_text}

INSTRUCTIONS:
1. Ignore implementation differences between Candidate and Reference. Focus on FUNCTIONAL CORRECTNESS and QUALITY.
2. Evaluate the Candidate Solution strictly against the provided RUBRIC categories.
3. For each category in the rubric (e.g., 'Correctness', 'Code Quality', etc.), assign a score from 1-10.
4. Calculate a weighted total score (0-100) based on the rubric weights.

Respond with a JSON object ONLY in this format:
{{
    "breakdown": {{
        "category_name_1": score_int,
        "category_name_2": score_int
        ...
    }},
    "total_score": float (0-100),
    "passed": boolean (Total >= Pass Threshold defined in rubric),
    "feedback": "Detailed justification for scores..."
}}
"""

    try:
        # Determine strictness/model. Default to a strong model for judging if possible.
        judge_model = model or "gh:openai/gpt-4o"
        
        # Call LLM
        response = LLMClient.generate_text(model_name=judge_model, prompt=prompt)
        
        # Parse JSON
        code = _extract_code_block(response) # In case it's wrapped in markdown
        if not code.startswith("{"):
             # Try to find { ... }
             m = re.search(r"\{.*\}", response, re.DOTALL)
             if m:
                 code = m.group(0)
             else:
                 code = response

        data = json.loads(code)
        
        breakdown = data.get("breakdown", {})
        score_val = float(data.get("total_score", 0))
        passed = bool(data.get("passed", False))
        reasoning = data.get("feedback") or data.get("reasoning", "No reasoning provided.")
        
        # Calculate grade based on 0-100 rubric scale
        if score_val >= 90: grade = "A"
        elif score_val >= 80: grade = "B"
        elif score_val >= 70: grade = "C"
        elif score_val >= 60: grade = "D"
        else: grade = "F"
        
        return ItemScore(
            exact_match=False,
            similarity=score_val / 100.0, 
            normalized_similarity=score_val,
            total_score=score_val,
            grade=grade,
            passed=passed,
            feedback=reasoning,
            breakdown=breakdown
        )
        
    except Exception as e:
        print(f"[RunStore] LLM Judge failed: {e}")
        # Fallback to string matching
        return _score_item(actual, gold)
        
    except Exception as e:
        print(f"[RunStore] LLM Judge failed: {e}")
        # Fallback to string matching
        return _score_item(actual, gold)


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
        self._load_existing_runs()

    def _load_existing_runs(self) -> None:
        """Load persisted runs from the results directory."""
        try:
            for run_file in self._results_dir.glob("run_*.json"):
                try:
                    with open(run_file, "r", encoding="utf-8") as f:
                        run_data = json.load(f)
                        if "run_id" in run_data:
                            self._runs[run_data["run_id"]] = run_data
                except Exception as e:
                    print(f"[RunStore] Failed to load run {run_file}: {e}")
            print(f"[RunStore] Loaded {len(self._runs)} existing runs.")
        except Exception as e:
            print(f"[RunStore] Failed to scan results dir: {e}")

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
                    prompt = _default_prompt_for_model(benchmark_id, t)
                    
                    if workflow and workflow != "baseline":
                        # Use multi-agent workflow
                        wf_name = UI_WORKFLOW_MAP.get(workflow, workflow)
                        executor = WorkflowExecutor(model_override=model, verbose=True)
                        
                        print(f"[RunStore] [{run_id}] Running workflow '{wf_name}' for task {tid}")
                        
                        # WorkflowExecutor.run is synchronous, run in thread
                        wf_result = await asyncio.to_thread(executor.run, wf_name, prompt)
                        after = wf_result.final_output
                        
                        # Extract agent results as steps
                        steps = []
                        if wf_result.agent_results:
                            for agent_id, res in wf_result.agent_results.items():
                                steps.append({
                                    "step_id": agent_id,
                                    "name": res.agent_name,
                                    "role": getattr(res, "role", "Agent"), # Check if agent result has role, else separate
                                    "status": res.status.value,
                                    "model": res.model_used,
                                    "input": res.input_context,
                                    "output": res.output,
                                    "duration": res.duration_seconds,
                                    "timestamp": res.timestamp
                                })
                        
                        # Extract code for scoring
                        code_to_score = _extract_code_block(after)
                        status = f"workflow:{wf_name}"
                    elif model:
                        after = _try_generate_with_llm(model, prompt)
                        code_to_score = after
                        status = "generated"
                    else:
                        after = gold
                        code_to_score = gold
                        status = "baseline_gold"

                    if evaluation_method == "execution" and execution_scorer:
                        exec_result = execution_scorer.score_task(t, code_to_score)
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
                        # Use LLM Judge for more semantic evaluation
                        judge_input_model = model or "gh:openai/gpt-4o" # Default to strong model
                        item_score = await asyncio.to_thread(_judge_with_llm, judge_input_model, before, gold, code_to_score, workflow)
                        item_score = item_score.to_dict()

                    item = RunItemResult(
                        task_id=tid,
                        status=status,
                        before=before,
                        gold=gold,
                        after=after,
                        score=item_score,
                        steps=steps if status.startswith("workflow") else None,
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
