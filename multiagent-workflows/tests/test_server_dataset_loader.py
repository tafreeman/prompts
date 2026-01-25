from __future__ import annotations

import importlib


_normalize_task_for_ui = importlib.import_module(
    "multiagent_workflows.server.dataset_loader"
)._normalize_task_for_ui


def test_normalize_humaneval_task_exposes_common_keys() -> None:
    raw = {
        "task_id": "HumanEval/0",
        "benchmark_id": "humaneval",
        "prompt": "Write a function add(a, b)",
        "expected_output": "def add(a,b): return a+b",
        "test_cases": [{"test": "assert add(1,2)==3", "entry_point": "add"}],
        "language": "python",
    }

    norm = _normalize_task_for_ui(raw)
    assert norm["task_id"] == "HumanEval/0"
    assert norm["problem_statement"] == raw["prompt"]
    assert "canonical_solution" in norm
    assert norm["canonical_solution"]
    assert norm["test"] == "assert add(1,2)==3"
    assert norm["entry_point"] == "add"


def test_normalize_swebench_task_exposes_patch_and_test_patch() -> None:
    raw = {
        "task_id": "django__django-12345",
        "benchmark_id": "swe-bench-lite",
        "prompt": "Fix bug...",
        "repo": "django/django",
        "golden_patch": "diff --git a/x b/x\n+fix",
        "test_cases": [{"test_patch": "diff --git a/t b/t\n+test"}],
        "language": "python",
    }

    norm = _normalize_task_for_ui(raw)
    assert norm["task_id"] == "django__django-12345"
    assert norm["patch"].startswith("diff --git")
    assert norm["test_patch"].startswith("diff --git")


def test_normalize_mbpp_task_exposes_test_list() -> None:
    raw = {
        "task_id": "1",
        "benchmark_id": "mbpp",
        "prompt": "Write a function...",
        "expected_output": "def f(): ...",
        "test_cases": [{"test_list": ["assert f()==1"], "test_setup_code": ""}],
        "language": "python",
    }

    norm = _normalize_task_for_ui(raw)
    assert norm["task_id"] == "1"
    assert norm["test_list"] == ["assert f()==1"]
