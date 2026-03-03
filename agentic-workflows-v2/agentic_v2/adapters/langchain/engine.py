"""LangChain execution engine — wraps the existing WorkflowRunner.

:class:`LangChainEngine` satisfies both the :class:`ExecutionEngine` and
:class:`SupportsStreaming` protocols by delegating to the
:class:`~agentic_v2.langchain.runner.WorkflowRunner` methods.

This adapter is a thin wrapper — it does **not** re-implement any
LangGraph compilation or state management logic.  All heavy lifting
is handled by the existing ``agentic_v2.langchain`` package.

LangChain/LangGraph imports are guarded with ``try/except ImportError``
so the module can be safely imported even when those packages are not
installed (registration simply won't occur).
"""

from __future__ import annotations

import logging
from typing import Any, AsyncIterator, Awaitable, Callable, Optional

logger = logging.getLogger(__name__)

try:
    from ...langchain.runner import WorkflowRunner as _WorkflowRunner

    _HAS_LANGCHAIN = True
except ImportError:  # pragma: no cover
    _HAS_LANGCHAIN = False
    _WorkflowRunner = None  # type: ignore[assignment,misc]


class LangChainEngine:
    """Adapter that delegates to the LangChain ``WorkflowRunner``.

    Satisfies :class:`~agentic_v2.core.protocols.ExecutionEngine` and
    :class:`~agentic_v2.core.protocols.SupportsStreaming` via structural
    subtyping — no explicit inheritance required.

    The ``workflow`` argument to :meth:`execute` and :meth:`stream` must
    be a **string** naming a YAML workflow definition (e.g. ``"code_review"``).

    Args:
        runner: An existing :class:`WorkflowRunner` instance.  If ``None``
            (the default), a fresh runner is created on first use.
    """

    def __init__(self, runner: Any = None) -> None:
        self._runner = runner

    @property
    def runner(self) -> Any:
        """Lazily create the underlying ``WorkflowRunner`` if needed."""
        if self._runner is None:
            if not _HAS_LANGCHAIN:
                raise ImportError(
                    "LangChain/LangGraph packages are required for the "
                    "LangChainEngine adapter.  Install them with: "
                    "pip install langchain langgraph"
                )
            self._runner = _WorkflowRunner()
        return self._runner

    async def execute(
        self,
        workflow: Any,
        ctx: Any = None,
        on_update: Optional[Callable[[dict[str, Any]], Awaitable[None]]] = None,
        **kwargs: Any,
    ) -> Any:
        """Execute a workflow by name via the LangChain runner.

        Args:
            workflow: Workflow name string (e.g. ``"code_review"``).
            ctx: Execution context (reserved for future use; not
                forwarded to the LangChain runner at this time).
            on_update: Async progress callback (reserved for future use).
            **kwargs: Forwarded as keyword inputs to
                :meth:`WorkflowRunner.run`.

        Returns:
            :class:`~agentic_v2.contracts.WorkflowResult` produced by
            the runner.

        Raises:
            TypeError: If *workflow* is not a string.
        """
        if not isinstance(workflow, str):
            raise TypeError(
                f"LangChainEngine workflow name must be a string, "
                f"got {type(workflow).__name__}"
            )

        return await self.runner.run(workflow, **kwargs)

    async def stream(
        self,
        workflow: Any,
        ctx: Any = None,
        **kwargs: Any,
    ) -> AsyncIterator[dict[str, Any]]:
        """Stream execution events for a workflow.

        Args:
            workflow: Workflow name string.
            ctx: Execution context (reserved for future use).
            **kwargs: Forwarded as keyword inputs to
                :meth:`WorkflowRunner.astream`.

        Yields:
            Event dictionaries from the LangGraph execution.

        Raises:
            TypeError: If *workflow* is not a string.
        """
        if not isinstance(workflow, str):
            raise TypeError(
                f"LangChainEngine workflow name must be a string, "
                f"got {type(workflow).__name__}"
            )

        async for event in self.runner.astream(workflow, **kwargs):
            yield event
