from __future__ import annotations

from multiagent_workflows.server.run_manager import RunStore


def test_list_runs_returns_sorted_summaries() -> None:
    store = RunStore()
    store._runs = {
        "run_a": {
            "run_id": "run_a",
            "benchmark_id": "humaneval",
            "workflow": "fullstack",
            "status": "running",
            "created_at_ms": 1000,
            "updated_at_ms": 2000,
        },
        "run_b": {
            "run_id": "run_b",
            "benchmark_id": "mbpp",
            "workflow": "bugfix",
            "status": "completed",
            "created_at_ms": 3000,
            "updated_at_ms": 4000,
        },
    }

    runs = store.list_runs()

    assert [r["run_id"] for r in runs] == ["run_b", "run_a"]
    assert runs[0]["workflow_name"] == "Bug Triage & Fix"
    assert runs[1]["workflow_name"] == "Full-Stack Generation"
    assert runs[0]["started_at"] is not None
    assert runs[1]["started_at"] is not None
