"""Tests for execution strategy abstraction."""

from __future__ import annotations

import pytest

from agentic_v2.contracts import StepStatus
from agentic_v2.engine import (
    DAG,
    DAGExecutor,
    DagOnceStrategy,
    ExecutionContext,
    ExecutionStrategy,
    StepDefinition,
    create_execution_strategy,
)


def _build_simple_dag() -> DAG:
    async def produce(_ctx: ExecutionContext) -> dict[str, bool]:
        return {"ok": True}

    dag = DAG("strategy_simple")
    dag.add(StepDefinition(name="only", func=produce))
    return dag


@pytest.mark.asyncio
async def test_dag_once_strategy_matches_current_behavior():
    dag = _build_simple_dag()

    direct_ctx = ExecutionContext(workflow_id="wf-direct")
    strategy_ctx = ExecutionContext(workflow_id="wf-strategy")

    direct = await DAGExecutor().execute(dag, direct_ctx)
    via_strategy = await DagOnceStrategy().execute(dag, strategy_ctx)

    assert direct.overall_status == StepStatus.SUCCESS
    assert via_strategy.overall_status == StepStatus.SUCCESS
    assert [step.step_name for step in via_strategy.steps] == [
        step.step_name for step in direct.steps
    ]
    assert [step.status for step in via_strategy.steps] == [
        step.status for step in direct.steps
    ]


def test_strategy_factory_default_dag_once():
    strategy = create_execution_strategy()
    assert isinstance(strategy, DagOnceStrategy)


def test_strategy_is_abstract():
    with pytest.raises(TypeError):
        ExecutionStrategy()  # type: ignore[abstract]
