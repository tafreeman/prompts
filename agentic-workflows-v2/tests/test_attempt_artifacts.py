"""Tests for W3-ART-001: attempt artifact persistence."""

from __future__ import annotations

import pytest

from agentic_v2.contracts import StepStatus
from agentic_v2.engine import (
    DAG,
    ExecutionContext,
    IterativeRepairStrategy,
    StepDefinition,
)
from agentic_v2.workflows.run_logger import RunLogger


def _single_step_dag(step_name: str, func) -> DAG:
    dag = DAG(step_name)
    dag.add(StepDefinition(name=step_name, func=func))
    return dag


@pytest.mark.asyncio
async def test_attempt_artifacts_saved(tmp_path):
    """After an iterative run, each attempt is persisted as JSON."""
    run_logger = RunLogger(runs_dir=tmp_path)

    async def fail_then_succeed(ctx: ExecutionContext) -> dict[str, bool]:
        attempt = int(await ctx.get("attempt_number", 1))
        if attempt == 1:
            raise RuntimeError("first attempt fails")
        return {"ok": True}

    strategy = IterativeRepairStrategy(
        max_attempts=2,
        run_logger=run_logger,
    )
    result = await strategy.execute(
        _single_step_dag("art_step", fail_then_succeed),
        ExecutionContext(workflow_id="wf-artifact-test"),
    )

    assert result.overall_status == StepStatus.SUCCESS
    assert result.metadata["attempts_used"] == 2

    # Both attempt dirs should exist
    attempt_1 = tmp_path / "wf-artifact-test" / "attempts" / "1" / "attempt.json"
    attempt_2 = tmp_path / "wf-artifact-test" / "attempts" / "2" / "attempt.json"
    assert attempt_1.exists(), "Attempt 1 artifact not saved"
    assert attempt_2.exists(), "Attempt 2 artifact not saved"


@pytest.mark.asyncio
async def test_attempt_artifacts_retrievable(tmp_path):
    """Attempt data can be listed and loaded via RunLogger helpers."""
    run_logger = RunLogger(runs_dir=tmp_path)

    async def fail_then_succeed(ctx: ExecutionContext) -> dict[str, bool]:
        attempt = int(await ctx.get("attempt_number", 1))
        if attempt == 1:
            raise RuntimeError("first attempt fails")
        return {"ok": True}

    strategy = IterativeRepairStrategy(
        max_attempts=2,
        run_logger=run_logger,
    )
    await strategy.execute(
        _single_step_dag("retrieve_step", fail_then_succeed),
        ExecutionContext(workflow_id="wf-retrieve-test"),
    )

    # list_attempts returns sorted dirs
    attempt_dirs = run_logger.list_attempts("wf-retrieve-test")
    assert len(attempt_dirs) == 2

    # load_attempt returns correct data
    a1 = run_logger.load_attempt("wf-retrieve-test", 1)
    assert a1["attempt_number"] == 1
    assert a1["status"] == "failed"

    a2 = run_logger.load_attempt("wf-retrieve-test", 2)
    assert a2["attempt_number"] == 2
    assert a2["status"] == "success"
