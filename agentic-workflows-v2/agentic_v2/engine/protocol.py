"""Execution engine protocol — common interface for all workflow engines (ADR-001).

Defines the structural subtyping contract that all execution engines must
satisfy.  Uses ``typing.Protocol`` (PEP 544) instead of ABC inheritance
so existing engine classes conform implicitly without code changes.

Why Protocol over ABC:
- **Structural subtyping** — conformance is checked by shape, not lineage.
  Existing ``DAGExecutor`` and ``LangGraphEngine`` satisfy the protocol
  without inheriting from it, enabling the Strangler Fig migration pattern.
- **No runtime cost** — Protocol is erased at runtime; no ``super().__init__()``
  or metaclass machinery.
- **Gradual adoption** — engines opt-in to ``runtime_checkable`` verification
  without refactoring inheritance trees.

Usage:
    from agentic_v2.engine.protocol import ExecutionEngine

    def run_workflow(engine: ExecutionEngine, ...) -> WorkflowResult:
        return await engine.execute(workflow, ctx)

    # Both pass static type checks:
    run_workflow(DAGExecutor(), ...)
    run_workflow(LangGraphEngine(), ...)
"""

from __future__ import annotations

from typing import Any, Awaitable, Callable, Optional, Protocol, runtime_checkable

from agentic_v2.contracts.messages import WorkflowResult

from .context import ExecutionContext


@runtime_checkable
class ExecutionEngine(Protocol):
    """Common interface for workflow execution engines.

    Any class with a matching ``execute`` signature satisfies this protocol
    via structural subtyping — no explicit inheritance required.

    Implementations:
    - ``DAGExecutor`` — Kahn's algorithm scheduler, maximum parallelism
    - ``LangGraphEngine`` — LangGraph state-machine compiler, streaming/checkpointing
    - ``PipelineExecutor`` — sequential pipeline execution

    All engines MUST:
    - Accept an ``ExecutionContext`` for shared state
    - Return a ``WorkflowResult`` with step results, status, and timing
    - Call ``on_update`` (if provided) for real-time progress reporting
    - Propagate exceptions from individual steps as ``StepResult.error``
    - Never mutate the workflow definition in-place
    """

    async def execute(
        self,
        workflow: Any,
        ctx: Optional[ExecutionContext] = None,
        on_update: Optional[Callable[[dict[str, Any]], Awaitable[None]]] = None,
        **kwargs: Any,
    ) -> WorkflowResult:
        """Execute a workflow and return results.

        Args:
            workflow: Engine-specific workflow definition (``DAG``, ``Pipeline``,
                workflow name string, etc.).  The engine is responsible for
                validating the type.
            ctx: Execution context with shared variables and services.
                If ``None``, engines should create a default context.
            on_update: Async callback fired on step start/end/error events.
                Payload is a dict with at minimum ``{"event": str, "step": str}``.
            **kwargs: Engine-specific options.  Common examples:
                - ``max_concurrency: int`` (DAGExecutor)
                - ``thread_id: str`` (LangGraphEngine)
                - ``use_cache: bool`` (LangGraphEngine)

        Returns:
            ``WorkflowResult`` with ordered step results, aggregate status,
            final outputs, and timing metadata.

        Raises:
            ValueError: If ``workflow`` is not a type this engine supports.
            RuntimeError: If execution fails in an unrecoverable way.
        """
        ...


@runtime_checkable
class SupportsStreaming(Protocol):
    """Optional capability: streaming execution events.

    Engines that support real-time event streaming (e.g., LangGraph)
    implement this in addition to ``ExecutionEngine``.
    """

    async def stream(
        self,
        workflow: Any,
        ctx: Optional[ExecutionContext] = None,
        **kwargs: Any,
    ) -> Any:
        """Stream execution events as an async iterator.

        Yields engine-specific event dicts. Callers should handle
        ``StopAsyncIteration`` gracefully.
        """
        ...


@runtime_checkable
class SupportsCheckpointing(Protocol):
    """Optional capability: execution checkpointing.

    Engines that support pause/resume (e.g., LangGraph with thread-based
    checkpointing) implement this in addition to ``ExecutionEngine``.
    """

    def get_checkpoint_state(
        self,
        workflow: Any,
        *,
        thread_id: str,
        **kwargs: Any,
    ) -> Optional[dict[str, Any]]:
        """Retrieve the latest checkpoint state for a workflow thread."""
        ...

    async def resume(
        self,
        workflow: Any,
        *,
        thread_id: str,
        ctx: Optional[ExecutionContext] = None,
        **kwargs: Any,
    ) -> WorkflowResult:
        """Resume execution from the last checkpoint."""
        ...
