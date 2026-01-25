from __future__ import annotations

from dataclasses import dataclass
import importlib
from typing import Any, Dict, List, Optional

from .benchmarks import FALLBACK_BENCHMARKS, try_get_repo_benchmarks


@dataclass(frozen=True)
class LoadedTasks:
    benchmark_id: str
    tasks: List[Dict[str, Any]]


def _normalize_task_for_ui(task: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize a task into a stable, UI-friendly structure.

    The UI in `ui/index.html` historically expected keys like:
      - task_id / instance_id
      - prompt / problem_statement
      - test / test_list / test_patch
      - canonical_solution / code / patch

    This function returns a dict that includes those conventional keys plus
    the normalized BenchmarkTask-like fields.
    """

    # Preserve original keys, but add common aliases used by the UI.
    out = dict(task)

    task_id = out.get("task_id") or out.get("id") or out.get("instance_id")
    if task_id is not None:
        out["task_id"] = str(task_id)

    # Best-effort synonyms (keep UI simple).
    if "problem_statement" not in out and out.get("prompt"):
        out["problem_statement"] = out.get("prompt")

    # Expose expected output under more dataset-native names.
    if out.get("expected_output") and "canonical_solution" not in out and "code" not in out:
        # For function-level problems, treat it as canonical solution.
        out["canonical_solution"] = out.get("expected_output")
        out["code"] = out.get("expected_output")

    if out.get("golden_patch") and "patch" not in out:
        out["patch"] = out.get("golden_patch")

    # Common test fields.
    if out.get("test_cases") and "test" not in out and "test_list" not in out and "test_patch" not in out:
        tc0 = out["test_cases"][0] if isinstance(out.get("test_cases"), list) and out["test_cases"] else {}
        if isinstance(tc0, dict):
            if tc0.get("test"):
                out["test"] = tc0.get("test")
            if tc0.get("test_list"):
                out["test_list"] = tc0.get("test_list")
            if tc0.get("test_patch"):
                out["test_patch"] = tc0.get("test_patch")
            if tc0.get("entry_point"):
                out["entry_point"] = tc0.get("entry_point")

    return out


def load_tasks(
    benchmark_id: str,
    limit: Optional[int] = None,
    offset: int = 0,
    use_cache: bool = True,
) -> LoadedTasks:
    """Load tasks for a benchmark.

    Preference order:
      1) Use repo's benchmark tool (tools.agents.benchmarks.loader.load_benchmark) if importable.
      2) Fall back to a minimal HuggingFace loader using `datasets`.

    Returns:
      LoadedTasks with tasks as plain JSON-serializable dicts.
    """

    # 1) Use the repo benchmark tool if present (this matches "like the tool does").
    try:
        from tools.agents.benchmarks.loader import load_benchmark  # type: ignore

        tasks = load_benchmark(benchmark_id, limit=limit, offset=offset, use_cache=use_cache)
        # BenchmarkTask has to_dict(); keep it robust if it returns dicts already.
        as_dicts: List[Dict[str, Any]] = []
        for t in tasks:
            if hasattr(t, "to_dict"):
                as_dicts.append(t.to_dict())
            elif isinstance(t, dict):
                as_dicts.append(t)
            else:
                as_dicts.append({"task_id": str(getattr(t, "task_id", "unknown")), "raw": str(t)})

        normalized = [_normalize_task_for_ui(d) for d in as_dicts]
        return LoadedTasks(benchmark_id=benchmark_id, tasks=normalized)
    except Exception:
        pass

    # 2) Fallback: direct HuggingFace load.
    b = FALLBACK_BENCHMARKS.get(benchmark_id)
    if not b:
        raise KeyError(f"Unknown benchmark_id: {benchmark_id}")

    if b.source != "huggingface":
        raise ValueError(f"Fallback loader only supports HuggingFace benchmarks. Got: {b.source}")

    try:
        datasets_mod = importlib.import_module("datasets")
        load_dataset = getattr(datasets_mod, "load_dataset")
    except Exception as exc:
        raise ImportError(
            "HuggingFace datasets support requires the 'datasets' package. "
            "Install it (e.g., pip install datasets)."
        ) from exc

    split = b.source_config.get("split", "test")
    ds = load_dataset(b.source_url, split=split)

    # Apply offset + limit.
    if offset:
        ds = ds.select(range(offset, len(ds)))
    if limit:
        ds = ds.select(range(min(limit, len(ds))))

    # Transform rows into a dict shape similar to the repo benchmark tool.
    out: List[Dict[str, Any]] = []
    for idx, row in enumerate(ds):
        # HumanEval
        if benchmark_id.startswith("humaneval"):
            task = {
                "task_id": row.get("task_id", f"HumanEval/{idx}"),
                "benchmark_id": benchmark_id,
                "prompt": row.get("prompt", ""),
                "instruction": "Complete the function implementation.",
                "expected_output": row.get("canonical_solution", ""),
                "test_cases": [{
                    "test": row.get("test", ""),
                    "entry_point": row.get("entry_point", ""),
                }],
                "language": "python",
            }
        # MBPP
        elif benchmark_id.startswith("mbpp"):
            task = {
                "task_id": str(row.get("task_id", idx)),
                "benchmark_id": benchmark_id,
                "prompt": row.get("text", row.get("prompt", "")),
                "instruction": "Write a Python function to solve the problem.",
                "expected_output": row.get("code", ""),
                "test_cases": [{
                    "test_list": row.get("test_list", []),
                    "test_setup_code": row.get("test_setup_code", ""),
                }],
                "language": "python",
            }
        # SWE-bench
        elif benchmark_id.startswith("swe-bench"):
            task = {
                "task_id": row.get("instance_id", f"task_{idx}"),
                "benchmark_id": benchmark_id,
                "prompt": row.get("problem_statement", ""),
                "instruction": "Fix the issue described above by modifying the repository.",
                "repo": row.get("repo", ""),
                "base_commit": row.get("base_commit", ""),
                "issue_text": row.get("problem_statement", ""),
                "hints": row.get("hints_text", ""),
                "golden_patch": row.get("patch", ""),
                "test_cases": [{"test_patch": row.get("test_patch", "")}],
                "language": "python",
            }
        else:
            task = {
                "task_id": row.get("id", f"task_{idx}"),
                "benchmark_id": benchmark_id,
                "prompt": row.get("prompt", row.get("text", row.get("instruction", ""))),
                "expected_output": row.get("solution", row.get("output", "")),
                "language": "python",
            }

        out.append(_normalize_task_for_ui(task))

    return LoadedTasks(benchmark_id=benchmark_id, tasks=out)


def list_benchmarks() -> List[Dict[str, Any]]:
    """Return benchmarks in a JSON-serializable list."""

    repo_defs = try_get_repo_benchmarks()
    if repo_defs:
        result = []
        for bid, b in repo_defs.items():
            # tools.agents.benchmarks.datasets.BenchmarkDefinition is a dataclass
            result.append(
                {
                    "id": getattr(b, "id", bid),
                    "name": getattr(b, "name", bid),
                    "description": getattr(b, "description", ""),
                    "size": getattr(b, "size", 0),
                    "source": getattr(getattr(b, "source", None), "value", str(getattr(b, "source", ""))),
                    "source_url": getattr(b, "source_url", ""),
                    "source_config": getattr(b, "source_config", {}) or {},
                    "benchmark_type": getattr(getattr(b, "benchmark_type", None), "value", ""),
                    "metrics": getattr(b, "metrics", []) or [],
                    "evaluation_method": getattr(b, "evaluation_method", ""),
                    "license": getattr(b, "license", "unknown"),
                    "languages": getattr(b, "languages", []) or [],
                    "tags": getattr(b, "tags", []) or [],
                }
            )
        return sorted(result, key=lambda x: x["id"])

    # Fallback
    return [
        {
            "id": b.id,
            "name": b.name,
            "description": b.description,
            "size": b.size,
            "source": b.source,
            "source_url": b.source_url,
            "source_config": b.source_config,
            "benchmark_type": b.benchmark_type,
            "metrics": b.metrics,
            "evaluation_method": b.evaluation_method,
            "license": b.license,
            "languages": b.languages,
            "tags": b.tags,
        }
        for b in FALLBACK_BENCHMARKS.values()
    ]
