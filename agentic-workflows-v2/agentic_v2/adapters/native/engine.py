"""Native execution engine — wraps DAGExecutor and PipelineExecutor.

:class:`NativeEngine` satisfies the :class:`ExecutionEngine` protocol
by delegating to the existing ``engine/`` executors based on the
workflow type.  This is the default adapter when no external engine
(e.g. LangChain) is needed.
"""

from __future__ import annotations

import logging
from typing import Any, Awaitable, Callable, Optional

from ...contracts import WorkflowResult
from ...engine.context import ExecutionContext
from ...engine.dag import DAG
from ...engine.dag_executor import DAGExecutor
from ...engine.pipeline import Pipeline, PipelineExecutor

logger = logging.getLogger(__name__)


class NativeEngine:
    """Adapter that delegates to the native DAG/Pipeline executors.

    Satisfies :class:`~agentic_v2.core.protocols.ExecutionEngine` via
    structural subtyping — no explicit inheritance required.

    Supported workflow types:

    - :class:`DAG` → :class:`DAGExecutor`
    - :class:`Pipeline` → :class:`PipelineExecutor`
    """

    def __init__(self) -> None:
        self._dag_executor = DAGExecutor()
        self._pipeline_executor = PipelineExecutor()

    async def execute(
        self,
        workflow: Any,
        ctx: Optional[ExecutionContext] = None,
        on_update: Optional[Callable[[dict[str, Any]], Awaitable[None]]] = None,
        **kwargs: Any,
    ) -> WorkflowResult:
        """Execute a workflow using the appropriate native executor.

        Args:
            workflow: A :class:`DAG` or :class:`Pipeline` instance.
            ctx: Execution context for shared variables and services.
            on_update: Async callback for progress events.
            **kwargs: Forwarded to the underlying executor (e.g.
                ``max_concurrency`` for DAG execution).

        Returns:
            :class:`WorkflowResult` with step results and status.

        Raises:
            TypeError: If *workflow* is not a supported type.
        """
        if ctx is None:
            ctx = ExecutionContext()

        if isinstance(workflow, DAG):
            return await self._dag_executor.execute(
                workflow, ctx, on_update=on_update, **kwargs
            )
        elif isinstance(workflow, Pipeline):
            return await self._pipeline_executor.execute(
                workflow, ctx, on_update=on_update, **kwargs
            )
        else:
            raise TypeError(
                f"Unsupported workflow type: {type(workflow).__name__}. "
                f"NativeEngine supports DAG and Pipeline."
            )
