"""Iterative execution strategy with retry/repair attempts."""

from __future__ import annotations

import logging
from copy import deepcopy
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Callable

from ..contracts import StepStatus, WorkflowResult
from .context import ExecutionContext
from .dag import DAG
from .dag_executor import DAGExecutor
from .step import StepExecutor
from .strategy import ExecutionStrategy, UpdateCallback

if TYPE_CHECKING:
    from ..workflows.run_logger import RunLogger

FeedbackBuilder = Callable[[WorkflowResult, int], dict[str, Any]]

_logger = logging.getLogger(__name__)


class IterativeRepairStrategy(ExecutionStrategy):
    """Execute a DAG repeatedly until success or max attempts is reached."""

    def __init__(
        self,
        max_attempts: int = 2,
        *,
        step_executor: StepExecutor | None = None,
        feedback_builder: FeedbackBuilder | None = None,
        run_logger: RunLogger | None = None,
    ) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")

        self.max_attempts = max_attempts
        self._dag_executor = DAGExecutor(step_executor=step_executor)
        self._feedback_builder = feedback_builder or self._default_feedback_builder
        self._run_logger = run_logger

    async def execute(
        self,
        dag: DAG,
        ctx: ExecutionContext,
        *,
        max_concurrency: int = 10,
        on_update: UpdateCallback = None,
    ) -> WorkflowResult:
        baseline_variables = _safe_deepcopy(ctx.all_variables())
        feedback: dict[str, Any] = {}
        attempt_history: list[dict[str, Any]] = []
        final_result: WorkflowResult | None = None

        for attempt_number in range(1, self.max_attempts + 1):
            self._reset_context(ctx, baseline_variables)
            ctx.set_sync("attempt_number", attempt_number)
            ctx.set_sync("max_attempts", self.max_attempts)
            if feedback:
                ctx.set_sync("iterative_feedback", feedback)

            await _emit_event(
                on_update,
                {
                    "type": "attempt_start",
                    "attempt_number": attempt_number,
                    "max_attempts": self.max_attempts,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            )

            attempt_start = datetime.now(timezone.utc)
            result = await self._dag_executor.execute(
                dag,
                ctx,
                max_concurrency=max_concurrency,
                on_update=on_update,
            )
            final_result = result

            attempt_duration_ms = (
                datetime.now(timezone.utc) - attempt_start
            ).total_seconds() * 1000
            failed_steps = [step.step_name for step in result.steps if step.is_failed]
            attempt_history.append(
                {
                    "attempt_number": attempt_number,
                    "status": result.overall_status.value,
                    "duration_ms": attempt_duration_ms,
                    "failed_steps": failed_steps,
                }
            )

            # Persist attempt artifacts if a run logger is available
            if self._run_logger is not None:
                run_id = ctx.workflow_id or "unknown"
                try:
                    self._run_logger.log_attempt(
                        run_id,
                        attempt_number,
                        result,
                        feedback=feedback or None,
                    )
                except Exception:
                    _logger.warning(
                        "Failed to log attempt %d for run %s",
                        attempt_number,
                        run_id,
                        exc_info=True,
                    )

            await _emit_event(
                on_update,
                {
                    "type": "attempt_end",
                    "attempt_number": attempt_number,
                    "max_attempts": self.max_attempts,
                    "status": result.overall_status.value,
                    "duration_ms": attempt_duration_ms,
                    "failed_steps": failed_steps,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            )

            if result.overall_status == StepStatus.SUCCESS:
                result.metadata["strategy"] = "iterative_repair"
                result.metadata["attempts_used"] = attempt_number
                result.metadata["max_attempts"] = self.max_attempts
                result.metadata["attempt_history"] = attempt_history
                return result

            feedback = self._feedback_builder(result, attempt_number)

        assert final_result is not None
        final_result.metadata["strategy"] = "iterative_repair"
        final_result.metadata["attempts_used"] = self.max_attempts
        final_result.metadata["max_attempts"] = self.max_attempts
        final_result.metadata["attempt_history"] = attempt_history
        return final_result

    @staticmethod
    def _reset_context(
        ctx: ExecutionContext,
        baseline_variables: dict[str, Any],
    ) -> None:
        # We intentionally restore the local variable store between attempts
        # so each run starts from the same baseline input state.
        ctx._variables = _safe_deepcopy(baseline_variables)  # noqa: SLF001
        ctx.completed_steps.clear()
        ctx.failed_steps.clear()
        ctx.current_step = None

    @staticmethod
    def _default_feedback_builder(
        result: WorkflowResult,
        attempt_number: int,
    ) -> dict[str, Any]:
        failed_steps = [step for step in result.steps if step.is_failed]
        return {
            "attempt_number": attempt_number,
            "failed_steps": [step.step_name for step in failed_steps],
            "errors": {
                step.step_name: step.error
                for step in failed_steps
                if step.error is not None
            },
        }


async def _emit_event(on_update: UpdateCallback, event: dict[str, Any]) -> None:
    if on_update is None:
        return
    await on_update(event)


def _safe_deepcopy(value: Any) -> Any:
    try:
        return deepcopy(value)
    except Exception:
        return value


__all__ = ["IterativeRepairStrategy"]
