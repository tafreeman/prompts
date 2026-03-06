"""Core protocols — engine-agnostic interfaces for the workflow system.

Defines the structural subtyping contracts (PEP 544) that all execution
engines, agents, tools, and memory stores must satisfy.  Uses
``typing.Protocol`` so existing classes conform implicitly by shape
without inheriting from these types.

Why Protocol over ABC:
- **Structural subtyping** — conformance checked by shape, not lineage.
- **No runtime cost** — erased at runtime; no ``super().__init__()`` needed.
- **Gradual adoption** — opt-in ``runtime_checkable`` verification.
"""

from __future__ import annotations

from typing import Any, Awaitable, Callable, Optional, Protocol, runtime_checkable


@runtime_checkable
class ExecutionEngine(Protocol):
    """Common interface for workflow execution engines.

    Any class with a matching ``execute`` signature satisfies this protocol
    via structural subtyping — no explicit inheritance required.

    Implementations:
    - ``DAGExecutor`` — Kahn's algorithm scheduler, maximum parallelism
    - ``PipelineExecutor`` — sequential pipeline execution
    - ``WorkflowExecutor`` — polymorphic executor
    - ``LangChainEngine`` — LangGraph state-machine compiler (via adapter)

    All engines MUST:
    - Accept an execution context for shared state
    - Return a ``WorkflowResult`` with step results, status, and timing
    - Call ``on_update`` (if provided) for real-time progress reporting
    - Propagate exceptions from individual steps
    - Never mutate the workflow definition in-place
    """

    async def execute(
        self,
        workflow: Any,
        ctx: Any = None,
        on_update: Optional[Callable[[dict[str, Any]], Awaitable[None]]] = None,
        **kwargs: Any,
    ) -> Any:
        """Execute a workflow and return results.

        Args:
            workflow: Engine-specific workflow definition (``DAG``, ``Pipeline``,
                workflow name string, etc.).
            ctx: Execution context with shared variables and services.
            on_update: Async callback fired on step start/end/error events.
            **kwargs: Engine-specific options (e.g., ``max_concurrency``).

        Returns:
            ``WorkflowResult`` with ordered step results, aggregate status,
            final outputs, and timing metadata.
        """
        ...


@runtime_checkable
class SupportsStreaming(Protocol):
    """Optional capability: streaming execution events."""

    async def stream(
        self,
        workflow: Any,
        ctx: Any = None,
        **kwargs: Any,
    ) -> Any:
        """Stream execution events as an async iterator."""
        ...


@runtime_checkable
class SupportsCheckpointing(Protocol):
    """Optional capability: execution checkpointing."""

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
        ctx: Any = None,
        **kwargs: Any,
    ) -> Any:
        """Resume execution from the last checkpoint."""
        ...


@runtime_checkable
class AgentProtocol(Protocol):
    """Common interface for workflow agents.

    Agents process task inputs and produce task outputs, optionally
    maintaining state across invocations.
    """

    @property
    def name(self) -> str:
        """Agent's unique name."""
        ...

    async def run(self, input_data: Any, ctx: Any = None) -> Any:
        """Execute the agent on the given input.

        Args:
            input_data: Task input (varies by agent type).
            ctx: Optional execution context.

        Returns:
            Task output.
        """
        ...


@runtime_checkable
class ToolProtocol(Protocol):
    """Common interface for tools available to agents."""

    @property
    def name(self) -> str:
        """Tool's unique name."""
        ...

    @property
    def description(self) -> str:
        """Human-readable description of what the tool does."""
        ...

    async def execute(self, **kwargs: Any) -> Any:
        """Execute the tool with the given arguments.

        Returns:
            Tool output (varies by tool type).
        """
        ...


# MemoryStore is deprecated — use MemoryStoreProtocol from core.memory instead.
# Kept as an alias for backward compatibility with existing agent code.
from .memory import MemoryStoreProtocol as MemoryStore  # noqa: E402
