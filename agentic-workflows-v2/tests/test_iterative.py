"""Tests for iterative repair execution strategy."""

from __future__ import annotations

import pytest

from agentic_v2.contracts import StepStatus
from agentic_v2.engine import (
    DAG,
    DagOnceStrategy,
    ExecutionContext,
    IterativeRepairStrategy,
    StepDefinition,
    create_execution_strategy,
)
from agentic_v2.workflows.loader import WorkflowDefinition
from agentic_v2.workflows.runner import WorkflowRunner


def _single_step_dag(step_name: str, func) -> DAG:
    dag = DAG(step_name)
    dag.add(StepDefinition(name=step_name, func=func))
    return dag


@pytest.mark.asyncio
async def test_iterative_stops_on_success():
    call_count = 0

    async def always_success(_ctx: ExecutionContext) -> dict[str, bool]:
        nonlocal call_count
        call_count += 1
        return {"ok": True}

    strategy = IterativeRepairStrategy(max_attempts=3)
    result = await strategy.execute(
        _single_step_dag("success_once", always_success),
        ExecutionContext(workflow_id="wf-success-once"),
    )

    assert result.overall_status == StepStatus.SUCCESS
    assert result.metadata["attempts_used"] == 1
    assert len(result.metadata["attempt_history"]) == 1
    assert call_count == 1


@pytest.mark.asyncio
async def test_iterative_retries_on_failure():
    async def fail_then_succeed(ctx: ExecutionContext) -> dict[str, bool]:
        attempt = int(await ctx.get("attempt_number", 1))
        if attempt == 1:
            raise RuntimeError("first attempt fails")
        return {"ok": True}

    strategy = IterativeRepairStrategy(max_attempts=3)
    result = await strategy.execute(
        _single_step_dag("retry_once", fail_then_succeed),
        ExecutionContext(workflow_id="wf-retry-once"),
    )

    assert result.overall_status == StepStatus.SUCCESS
    assert result.metadata["attempts_used"] == 2
    assert len(result.metadata["attempt_history"]) == 2
    assert result.metadata["attempt_history"][0]["status"] == StepStatus.FAILED.value
    assert result.metadata["attempt_history"][1]["status"] == StepStatus.SUCCESS.value


@pytest.mark.asyncio
async def test_iterative_respects_max_attempts():
    async def always_fail(_ctx: ExecutionContext) -> dict[str, bool]:
        raise RuntimeError("always failing")

    strategy = IterativeRepairStrategy(max_attempts=2)
    result = await strategy.execute(
        _single_step_dag("always_fail", always_fail),
        ExecutionContext(workflow_id="wf-max-attempts"),
    )

    assert result.overall_status == StepStatus.FAILED
    assert result.metadata["attempts_used"] == 2
    assert len(result.metadata["attempt_history"]) == 2
    assert all(
        attempt["status"] == StepStatus.FAILED.value
        for attempt in result.metadata["attempt_history"]
    )


@pytest.mark.asyncio
async def test_iterative_emits_attempt_events():
    events: list[dict[str, object]] = []

    async def fail_once(ctx: ExecutionContext) -> dict[str, bool]:
        attempt = int(await ctx.get("attempt_number", 1))
        if attempt < 2:
            raise RuntimeError("fail once")
        return {"ok": True}

    async def capture(event: dict[str, object]) -> None:
        events.append(event)

    strategy = IterativeRepairStrategy(max_attempts=3)
    result = await strategy.execute(
        _single_step_dag("attempt_events", fail_once),
        ExecutionContext(workflow_id="wf-attempt-events"),
        on_update=capture,
    )

    assert result.overall_status == StepStatus.SUCCESS

    start_events = [event for event in events if event.get("type") == "attempt_start"]
    end_events = [event for event in events if event.get("type") == "attempt_end"]

    assert len(start_events) == 2
    assert len(end_events) == 2
    assert all("attempt_number" in event for event in start_events + end_events)


def test_strategy_factory_selects_iterative_for_multiple_attempts(monkeypatch):
    monkeypatch.setenv("AGENTIC_FF_ITERATIVE_STRATEGY", "true")
    from agentic_v2.feature_flags import reset_flags
    reset_flags()
    try:
        strategy = create_execution_strategy({"max_attempts": 3})
        assert isinstance(strategy, IterativeRepairStrategy)
    finally:
        reset_flags()


@pytest.mark.asyncio
async def test_dag_once_backward_compatible():
    async def always_success(_ctx: ExecutionContext) -> dict[str, bool]:
        return {"ok": True}

    dag = _single_step_dag("compat_step", always_success)
    definition = WorkflowDefinition(name="compat_workflow", dag=dag)
    runner = WorkflowRunner()
    events: list[dict[str, object]] = []

    async def capture(event: dict[str, object]) -> None:
        events.append(event)

    result = await runner.run_definition(definition, on_update=capture)
    assert result.overall_status == StepStatus.SUCCESS

    strategy = create_execution_strategy({"max_attempts": 1})
    assert isinstance(strategy, DagOnceStrategy)
    assert all(
        event.get("type") not in {"attempt_start", "attempt_end"}
        for event in events
    )
