"""Main workflow executor with full orchestration.

Aggressive design improvements:
- Unified execution interface
- Async-native with cancellation tokens
- Memory tracking for context growth
- Execution history/audit trail
- Sub-workflow composition
- Resource cleanup guarantees
"""

from __future__ import annotations

import asyncio
import traceback
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Optional, Union

from ..contracts import StepResult, StepStatus, WorkflowResult
from ..models import SmartModelRouter, get_smart_router
from ..tools import ToolRegistry, get_registry
from .context import ExecutionContext
from .pipeline import Pipeline, PipelineExecutor
from .step import StepDefinition, StepExecutor


class ExecutorEvent(str, Enum):
    """Events emitted by executor."""

    WORKFLOW_START = "workflow_start"
    WORKFLOW_END = "workflow_end"
    STEP_START = "step_start"
    STEP_END = "step_end"
    ERROR = "error"
    CANCELLED = "cancelled"
    CHECKPOINT = "checkpoint"


EventListener = Callable[[ExecutorEvent, dict[str, Any]], None]


@dataclass
class ExecutionConfig:
    """Configuration for workflow execution."""

    # Timeouts
    global_timeout_seconds: Optional[float] = None
    step_default_timeout_seconds: float = 300.0

    # Retries
    max_global_retries: int = 0

    # Checkpointing
    enable_checkpoints: bool = False
    checkpoint_interval: int = 5

    # Resource limits
    max_memory_mb: Optional[int] = None
    max_context_variables: int = 1000

    # Cleanup
    cleanup_on_complete: bool = True

    # Debugging
    debug_mode: bool = False
    trace_steps: bool = False


@dataclass
class ExecutionHistory:
    """Audit trail for workflow execution."""

    entries: list[dict[str, Any]] = field(default_factory=list)

    def record(
        self,
        event_type: str,
        step_name: Optional[str] = None,
        data: Optional[dict[str, Any]] = None,
    ) -> None:
        """Record an event."""
        self.entries.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "event": event_type,
                "step": step_name,
                "data": data or {},
            }
        )

    def get_step_history(self, step_name: str) -> list[dict[str, Any]]:
        """Get history for a specific step."""
        return [e for e in self.entries if e.get("step") == step_name]

    def get_errors(self) -> list[dict[str, Any]]:
        """Get all error entries."""
        return [e for e in self.entries if e.get("event") == "error"]


class WorkflowExecutor:
    """Main executor for workflows and pipelines.

    Aggressive improvements:
    - Unified interface for steps, pipelines, and sub-workflows
    - Global timeout with graceful cancellation
    - Memory/resource monitoring
    - Full execution history
    - Event listeners for observability
    - Automatic service injection
    """

    def __init__(
        self,
        config: Optional[ExecutionConfig] = None,
        router: Optional[SmartModelRouter] = None,
        tools: Optional[ToolRegistry] = None,
    ):
        self.config = config or ExecutionConfig()
        self.router = router or get_smart_router()
        self.tools = tools or get_registry()

        self._step_executor = StepExecutor()
        self._pipeline_executor = PipelineExecutor()

        self._listeners: list[EventListener] = []
        self._history = ExecutionHistory()
        self._cancelled = False
        self._current_ctx: Optional[ExecutionContext] = None

    def add_listener(self, listener: EventListener) -> None:
        """Add an event listener."""
        self._listeners.append(listener)

    def remove_listener(self, listener: EventListener) -> None:
        """Remove an event listener."""
        if listener in self._listeners:
            self._listeners.remove(listener)

    async def _emit(self, event: ExecutorEvent, data: dict[str, Any]) -> None:
        """Emit event to all listeners."""
        for listener in self._listeners:
            try:
                result = listener(event, data)
                if asyncio.iscoroutine(result):
                    await result
            except Exception:
                pass  # Don't let listener errors break execution

    async def execute(
        self,
        workflow: Union[StepDefinition, Pipeline, list[StepDefinition]],
        ctx: Optional[ExecutionContext] = None,
        **initial_vars: Any,
    ) -> WorkflowResult:
        """Execute a workflow.

        Accepts:
        - Single StepDefinition
        - Pipeline
        - List of StepDefinitions (sequential execution)

        Args:
            workflow: What to execute
            ctx: Optional execution context
            **initial_vars: Initial context variables

        Returns:
            WorkflowResult with execution details
        """
        # Create context if needed
        if ctx is None:
            ctx = ExecutionContext()

        self._current_ctx = ctx
        self._cancelled = False

        # Set initial variables
        for key, value in initial_vars.items():
            ctx.set_sync(key, value)

        # Inject services
        ctx.services.register_singleton(SmartModelRouter, self.router)
        ctx.services.register_singleton(ToolRegistry, self.tools)

        # Create result
        workflow_name = self._get_workflow_name(workflow)
        result = WorkflowResult(
            workflow_id=ctx.workflow_id,
            workflow_name=workflow_name,
            overall_status=StepStatus.RUNNING,
        )

        self._history.record("workflow_start", data={"name": workflow_name})
        await self._emit(ExecutorEvent.WORKFLOW_START, {"workflow": workflow_name})

        try:
            # Execute with global timeout
            if self.config.global_timeout_seconds:
                result = await asyncio.wait_for(
                    self._execute_workflow(workflow, ctx, result),
                    timeout=self.config.global_timeout_seconds,
                )
            else:
                result = await self._execute_workflow(workflow, ctx, result)

        except (asyncio.TimeoutError, TimeoutError):
            result.overall_status = StepStatus.FAILED
            result.metadata["error"] = (
                f"Global timeout after {self.config.global_timeout_seconds}s"
            )
            result.metadata["error_type"] = "timeout"
            self._history.record("error", data={"type": "timeout"})

        except asyncio.CancelledError:
            result.overall_status = StepStatus.FAILED
            result.metadata["cancelled"] = True
            self._history.record("cancelled")
            await self._emit(ExecutorEvent.CANCELLED, {})

        except Exception as e:
            result.overall_status = StepStatus.FAILED
            result.metadata["error"] = str(e)
            result.metadata["traceback"] = traceback.format_exc()
            self._history.record(
                "error", data={"type": type(e).__name__, "message": str(e)}
            )
            await self._emit(ExecutorEvent.ERROR, {"error": str(e)})

        result.mark_complete(result.overall_status == StepStatus.SUCCESS)
        result.metadata["history_entries"] = len(self._history.entries)

        self._history.record(
            "workflow_end", data={"status": result.overall_status.value}
        )
        await self._emit(
            ExecutorEvent.WORKFLOW_END,
            {
                "status": result.overall_status.value,
                "duration_ms": result.total_duration_ms,
            },
        )

        # Cleanup
        if self.config.cleanup_on_complete:
            self._current_ctx = None

        return result

    async def _execute_workflow(
        self,
        workflow: Union[StepDefinition, Pipeline, list[StepDefinition]],
        ctx: ExecutionContext,
        result: WorkflowResult,
    ) -> WorkflowResult:
        """Internal workflow execution."""

        if isinstance(workflow, StepDefinition):
            # Single step
            step_result = await self._execute_step(workflow, ctx)
            result.add_step(step_result)
            result.overall_status = (
                StepStatus.SUCCESS if step_result.is_success else StepStatus.FAILED
            )

        elif isinstance(workflow, Pipeline):
            # Pipeline
            pipeline_result = await self._pipeline_executor.execute(workflow, ctx)
            result.steps = pipeline_result.steps
            result.overall_status = pipeline_result.overall_status
            result.final_output = pipeline_result.final_output

        elif isinstance(workflow, list):
            # Sequential steps
            for step_def in workflow:
                if self._cancelled:
                    break

                step_result = await self._execute_step(step_def, ctx)
                result.add_step(step_result)

                if step_result.is_failed:
                    result.overall_status = StepStatus.FAILED
                    break
            else:
                result.overall_status = StepStatus.SUCCESS

        # Set final output from context
        result.final_output = ctx.all_variables()

        return result

    async def _execute_step(
        self, step_def: StepDefinition, ctx: ExecutionContext
    ) -> StepResult:
        """Execute a single step with monitoring."""

        self._history.record("step_start", step_def.name)
        await self._emit(ExecutorEvent.STEP_START, {"step": step_def.name})

        # Apply default timeout if not set
        if step_def.timeout_seconds is None:
            step_def.timeout_seconds = self.config.step_default_timeout_seconds

        result = await self._step_executor.execute(step_def, ctx)

        self._history.record(
            "step_end",
            step_def.name,
            {"status": result.status.value, "duration_ms": result.duration_ms},
        )
        await self._emit(
            ExecutorEvent.STEP_END,
            {"step": step_def.name, "status": result.status.value},
        )

        # Check context size limits
        if self.config.max_context_variables:
            var_count = len(ctx.all_variables())
            if var_count > self.config.max_context_variables:
                result.metadata["warning"] = (
                    f"Context has {var_count} variables (limit: {self.config.max_context_variables})"
                )

        return result

    async def cancel(self) -> None:
        """Cancel current execution."""
        self._cancelled = True
        await self._step_executor.cancel_all()
        await self._pipeline_executor.cancel()

    def _get_workflow_name(
        self, workflow: Union[StepDefinition, Pipeline, list[StepDefinition]]
    ) -> str:
        """Get workflow name for logging."""
        if isinstance(workflow, StepDefinition):
            return f"step:{workflow.name}"
        elif isinstance(workflow, Pipeline):
            return workflow.name
        elif isinstance(workflow, list):
            return f"sequence:{len(workflow)}_steps"
        return "unknown"

    @property
    def history(self) -> ExecutionHistory:
        """Get execution history."""
        return self._history

    @property
    def current_context(self) -> Optional[ExecutionContext]:
        """Get current execution context."""
        return self._current_ctx


# Global executor instance
_executor: Optional[WorkflowExecutor] = None


def get_executor() -> WorkflowExecutor:
    """Get or create global executor."""
    global _executor
    if _executor is None:
        _executor = WorkflowExecutor()
    return _executor


def reset_executor() -> None:
    """Reset global executor (for testing)."""
    global _executor
    _executor = None


# Convenience functions
async def execute(
    workflow: Union[StepDefinition, Pipeline, list[StepDefinition]], **initial_vars: Any
) -> WorkflowResult:
    """Execute a workflow with the global executor."""
    return await get_executor().execute(workflow, **initial_vars)


async def run(step_def: StepDefinition, **initial_vars: Any) -> StepResult:
    """Run a single step and return its result."""
    result = await execute(step_def, **initial_vars)
    if result.steps:
        return result.steps[0]
    return StepResult(
        step_name=step_def.name, status=StepStatus.FAILED, error="No step result"
    )
