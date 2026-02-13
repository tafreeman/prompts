"""Execution strategy abstractions for DAG workflows."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Mapping, Optional

from ..contracts import WorkflowResult
from .context import ExecutionContext
from .dag import DAG
from .dag_executor import DAGExecutor
from .step import StepExecutor

_logger = logging.getLogger(__name__)

UpdateCallback = Optional[Callable[[dict[str, Any]], Awaitable[None]]]


class ExecutionStrategy(ABC):
    """Strategy contract for DAG execution."""

    @abstractmethod
    async def execute(
        self,
        dag: DAG,
        ctx: ExecutionContext,
        *,
        max_concurrency: int = 10,
        on_update: UpdateCallback = None,
    ) -> WorkflowResult:
        """Execute a DAG and return a workflow result."""


class DagOnceStrategy(ExecutionStrategy):
    """Default strategy: execute the DAG exactly once."""

    def __init__(self, step_executor: StepExecutor | None = None) -> None:
        self._dag_executor = DAGExecutor(step_executor=step_executor)

    async def execute(
        self,
        dag: DAG,
        ctx: ExecutionContext,
        *,
        max_concurrency: int = 10,
        on_update: UpdateCallback = None,
    ) -> WorkflowResult:
        return await self._dag_executor.execute(
            dag,
            ctx,
            max_concurrency=max_concurrency,
            on_update=on_update,
        )


def create_execution_strategy(
    execution_profile: Mapping[str, Any] | None = None,
    *,
    step_executor: StepExecutor | None = None,
) -> ExecutionStrategy:
    """Create an execution strategy from profile settings.

    Defaults to :class:`DagOnceStrategy` for backward compatibility.
    When ``max_attempts > 1`` and no explicit strategy is specified, this
    automatically chooses iterative repair.
    """

    profile = dict(execution_profile or {})
    strategy_name = str(profile.get("strategy", "")).strip().lower()
    raw_max_attempts = profile.get("max_attempts", 1)

    try:
        max_attempts = int(raw_max_attempts)
    except (TypeError, ValueError):
        max_attempts = 1
    if max_attempts < 1:
        max_attempts = 1

    if not strategy_name:
        strategy_name = "iterative_repair" if max_attempts > 1 else "dag_once"

    if strategy_name in {"dag_once", "once", "default"}:
        return DagOnceStrategy(step_executor=step_executor)

    if strategy_name in {"iterative", "iterative_repair", "repair"}:
        from ..feature_flags import get_flags

        if not get_flags().iterative_strategy:
            _logger.warning(
                "Iterative strategy requested but feature flag "
                "'iterative_strategy' is disabled — falling back to dag_once."
            )
            return DagOnceStrategy(step_executor=step_executor)

        from .iterative import IterativeRepairStrategy

        return IterativeRepairStrategy(
            max_attempts=max_attempts,
            step_executor=step_executor,
        )

    raise ValueError(
        "Unsupported execution strategy "
        f"'{strategy_name}'. Expected 'dag_once' or 'iterative_repair'."
    )


__all__ = [
    "ExecutionStrategy",
    "DagOnceStrategy",
    "create_execution_strategy",
]
