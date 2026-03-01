"""Step definition and execution.

Provides the two core abstractions for individual step lifecycle:

- :class:`StepDefinition` — declarative specification of *what* a step does
  (function, tier, conditions, I/O mappings, hooks, retry, loop_until).
- :class:`StepExecutor` — executes a :class:`StepDefinition` with full
  lifecycle management (input mapping, timeout, retry, hooks, output
  capture, loop-until re-execution, and review-report normalization).

Design highlights:
- **Fluent builder API** for programmatic step construction.
- **@step decorator** for defining steps from async functions.
- **Configurable retry** with FIXED / LINEAR / EXPONENTIAL backoff + jitter.
- **Conditional execution** via ``when`` / ``unless`` callables.
- **Loop-until** for bounded re-review: re-execute until a ``${...}``
  expression evaluates ``True`` or ``loop_max`` iterations reached.
"""

from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Awaitable, Callable, Optional, TypeVar

from ..contracts import ReviewStatus, StepResult, StepStatus
from ..models import ModelTier
from .context import ExecutionContext

T = TypeVar("T")


class RetryStrategy(str, Enum):
    """Retry backoff strategies."""

    NONE = "none"
    FIXED = "fixed"
    EXPONENTIAL = "exponential"
    LINEAR = "linear"


@dataclass
class RetryConfig:
    """Configuration for step retry behaviour.

    Attributes:
        max_retries: Maximum number of retry attempts (0 = no retries).
        strategy: Backoff algorithm — NONE, FIXED, LINEAR, or EXPONENTIAL.
        base_delay_seconds: Starting delay between attempts.
        max_delay_seconds: Ceiling for computed delay (prevents runaway waits).
        jitter: Fractional jitter applied to the delay (±jitter × delay) to
            prevent thundering-herd effects on parallel retries.
        retry_on: Exception types that trigger a retry.
        no_retry_on: Exception types that must *never* be retried, even if
            they match ``retry_on`` (takes precedence).
    """

    max_retries: int = 3
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL
    base_delay_seconds: float = 1.0
    max_delay_seconds: float = 60.0
    jitter: float = 0.1

    retry_on: tuple[type[Exception], ...] = (Exception,)
    no_retry_on: tuple[type[Exception], ...] = ()

    def get_delay(self, attempt: int) -> float:
        """Calculate the backoff delay for *attempt* (1-indexed).

        Args:
            attempt: Current attempt number (1 = first retry).

        Returns:
            Non-negative delay in seconds, capped at ``max_delay_seconds``
            and perturbed by ±``jitter``.
        """
        import random

        if self.strategy == RetryStrategy.NONE:
            return 0
        elif self.strategy == RetryStrategy.FIXED:
            base = self.base_delay_seconds
        elif self.strategy == RetryStrategy.LINEAR:
            base = self.base_delay_seconds * attempt
        else:  # EXPONENTIAL
            base = self.base_delay_seconds * (2 ** (attempt - 1))

        # Apply cap
        delay = min(base, self.max_delay_seconds)

        # Apply jitter
        jitter_range = delay * self.jitter
        delay += random.uniform(-jitter_range, jitter_range)

        return max(0, delay)

    def should_retry(self, error: Exception) -> bool:
        """Check whether *error* should trigger a retry.

        ``no_retry_on`` takes precedence: if the error matches that tuple
        the answer is always ``False``, regardless of ``retry_on``.
        """
        if isinstance(error, self.no_retry_on):
            return False
        return isinstance(error, self.retry_on)


# Type for step functions
StepFunction = Callable[[ExecutionContext], Awaitable[dict[str, Any]]]
HookFunction = Callable[[ExecutionContext, "StepDefinition"], Awaitable[None]]
ConditionFunction = Callable[[ExecutionContext], bool]


@dataclass
class StepDefinition:
    """Declarative step definition for workflow DAGs.

    Each instance describes a single node in the workflow graph: what
    function to run, which LLM tier to use, how to map inputs/outputs,
    when to skip, and how to handle failures.

    Supports a **fluent builder API** (``with_retry``, ``with_timeout``,
    ``with_dependency``, ``with_input``, ``with_output``, ``with_pre_hook``,
    ``with_post_hook``) for programmatic construction, and is also
    hydrated from YAML by the workflow loader.

    Attributes:
        name: Unique step identifier within a DAG.
        description: Human-readable purpose of this step.
        func: Async callable ``(ctx) → dict`` that performs the work.
        tier: LLM model tier (TIER_0 = deterministic, higher = stronger).
        timeout_seconds: Per-step wall-clock timeout (``None`` = unlimited).
        retry: Retry policy (backoff strategy, max attempts, jitter).
        when: Optional predicate — step runs only if this returns ``True``.
        unless: Optional predicate — step is skipped if this returns ``True``.
        loop_until: Expression string re-evaluated after each execution;
            the step re-runs until it evaluates ``True`` or ``loop_max``
            iterations are exhausted.
        loop_max: Upper bound on loop-until iterations (default 3).
        depends_on: List of upstream step names that must complete first.
        input_mapping: Maps step-local input names to context variable paths.
        output_mapping: Maps step output keys to context variable paths.
        pre_hooks: Async callables invoked before step execution.
        post_hooks: Async callables invoked after successful execution.
        error_hooks: Async callables invoked on step failure.
        tags: Freeform labels for filtering/grouping.
        metadata: Arbitrary key-value pairs attached to the step.
    """

    name: str
    description: str = ""

    # Execution
    func: Optional[StepFunction] = None
    tier: ModelTier = ModelTier.TIER_0
    timeout_seconds: Optional[float] = None

    # Retry configuration
    retry: RetryConfig = field(default_factory=RetryConfig)

    # Conditions
    when: Optional[ConditionFunction] = None  # Run only if True
    unless: Optional[ConditionFunction] = None  # Skip if True

    # Loop control (R5)
    # When set, the step re-executes until this expression evaluates to True,
    # or until loop_max iterations have been reached.
    # Example YAML:  loop_until: "${review_report.overall_status} in ['APPROVED']"
    loop_until: Optional[str] = None
    loop_max: int = 3

    # Dependencies
    depends_on: list[str] = field(default_factory=list)

    # I/O mapping
    input_mapping: dict[str, str] = field(
        default_factory=dict
    )  # step_input -> context_var
    output_mapping: dict[str, str] = field(
        default_factory=dict
    )  # step_output -> context_var

    # Hooks
    pre_hooks: list[HookFunction] = field(default_factory=list)
    post_hooks: list[HookFunction] = field(default_factory=list)
    error_hooks: list[HookFunction] = field(default_factory=list)

    # Metadata
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def should_run(self, ctx: ExecutionContext) -> bool:
        """Determine whether this step is eligible to execute.

        Checks, in order: (1) all ``depends_on`` steps are complete and
        none have failed, (2) ``when`` predicate passes (if set),
        (3) ``unless`` predicate does not trigger (if set).

        Args:
            ctx: Current execution context with step completion state.

        Returns:
            ``True`` if all conditions are satisfied.
        """
        # Check dependencies
        for dep in self.depends_on:
            if not ctx.is_step_complete(dep):
                return False
            if ctx.is_step_failed(dep):
                return False

        # Check when condition
        if self.when is not None and not self.when(ctx):
            return False

        # Check unless condition
        if self.unless is not None and self.unless(ctx):
            return False

        return True

    def with_retry(
        self,
        max_retries: int = 3,
        strategy: RetryStrategy = RetryStrategy.EXPONENTIAL,
        base_delay: float = 1.0,
    ) -> "StepDefinition":
        """Fluent builder: Configure retry."""
        self.retry = RetryConfig(
            max_retries=max_retries, strategy=strategy, base_delay_seconds=base_delay
        )
        return self

    def with_timeout(self, seconds: float) -> "StepDefinition":
        """Fluent builder: Set timeout."""
        self.timeout_seconds = seconds
        return self

    def with_dependency(self, *step_names: str) -> "StepDefinition":
        """Fluent builder: Add dependencies."""
        self.depends_on.extend(step_names)
        return self

    def with_input(self, **mapping: str) -> "StepDefinition":
        """Fluent builder: Map context variables to step inputs."""
        self.input_mapping.update(mapping)
        return self

    def with_output(self, **mapping: str) -> "StepDefinition":
        """Fluent builder: Map step outputs to context variables."""
        self.output_mapping.update(mapping)
        return self

    def with_pre_hook(self, hook: HookFunction) -> "StepDefinition":
        """Fluent builder: Add pre-execution hook."""
        self.pre_hooks.append(hook)
        return self

    def with_post_hook(self, hook: HookFunction) -> "StepDefinition":
        """Fluent builder: Add post-execution hook."""
        self.post_hooks.append(hook)
        return self


def step(
    name: str,
    description: str = "",
    tier: ModelTier = ModelTier.TIER_0,
    timeout: Optional[float] = None,
    depends_on: Optional[list[str]] = None,
    retry: Optional[RetryConfig] = None,
) -> Callable[[StepFunction], StepDefinition]:
    """Decorator to define a step from an async function.

    Usage:
        @step("generate_code", tier=ModelTier.TIER_2, timeout=30)
        async def generate_code(ctx: ExecutionContext) -> dict:
            ...
    """

    def decorator(func: StepFunction) -> StepDefinition:
        return StepDefinition(
            name=name,
            description=description or func.__doc__ or "",
            func=func,
            tier=tier,
            timeout_seconds=timeout,
            depends_on=depends_on or [],
            retry=retry or RetryConfig(),
        )

    return decorator


class StepExecutor:
    """Executes :class:`StepDefinition` instances with full lifecycle management.

    Handles the complete step execution pipeline in order:

    1. **Condition check** — ``should_run()`` gates on dependencies + when/unless.
    2. **Pre-hooks** — async callables for logging, validation, etc.
    3. **Input mapping** — resolve ``${...}`` expressions into a child context.
    4. **Execution with retry** — run ``func(ctx)`` with timeout, retry on
       eligible exceptions using :class:`RetryConfig` backoff.
    5. **Output capture** — extract ``_meta`` for model tracking, normalize
       ``review_report`` outputs for gating conditions.
    6. **Loop-until** — optionally re-execute until a ``${...}`` condition
       is satisfied or ``loop_max`` iterations exhausted.
    7. **Post-hooks / Error-hooks** — invoked on success / failure.
    8. **Context update** — write outputs to parent context via ``output_mapping``.

    Attributes:
        _running_tasks: Active ``asyncio.Task`` instances keyed by step name,
            supporting cancellation via :meth:`cancel`.
    """

    def __init__(self):
        self._running_tasks: dict[str, asyncio.Task] = {}

    async def execute(
        self, step_def: StepDefinition, ctx: ExecutionContext
    ) -> StepResult:
        """Execute a single step through the full lifecycle pipeline.

        Args:
            step_def: The step specification to execute.
            ctx: Parent execution context (a child context is created for
                isolated input mapping).

        Returns:
            :class:`StepResult` with status, output data, model info,
            retry count, and timing metadata.
        """
        result = StepResult(
            step_name=step_def.name,
            status=StepStatus.PENDING,
            tier=(
                step_def.tier.value
                if isinstance(step_def.tier, ModelTier)
                else step_def.tier
            ),
        )

        # Check conditions
        if not step_def.should_run(ctx):
            result.status = StepStatus.SKIPPED
            result.metadata["skip_reason"] = "conditions not met"
            return result

        # Validate function exists
        if step_def.func is None:
            result.status = StepStatus.FAILED
            result.error = "No function defined for step"
            return result

        # Mark step as running
        result.status = StepStatus.RUNNING
        await ctx.mark_step_start(step_def.name)

        # Run pre-hooks
        try:
            for hook in step_def.pre_hooks:
                await hook(ctx, step_def)
        except Exception as e:
            result.status = StepStatus.FAILED
            result.error = f"Pre-hook failed: {e}"
            await ctx.mark_step_failed(step_def.name, result.error)
            return result

        # Prepare inputs
        child_ctx = ctx.child(step_def.name)
        mapped_inputs: dict[str, Any] = {}
        for step_input, ctx_var in step_def.input_mapping.items():
            value = self._resolve_input_mapping_value(ctx, ctx_var)
            mapped_inputs[step_input] = value
            await child_ctx.set(step_input, value)
        result.input_data = mapped_inputs

        # Execute with retry
        attempt = 0
        last_error: Optional[Exception] = None

        while attempt <= step_def.retry.max_retries:
            attempt += 1
            result.retry_count = attempt - 1

            try:
                output = await self._execute_with_timeout(
                    step_def.func, child_ctx, step_def.timeout_seconds, step_def.name
                )

                # Success - map outputs
                result.status = StepStatus.SUCCESS
                result.output_data = output or {}

                # Extract _meta injected by LLM step for model tracking
                meta = result.output_data.pop("_meta", None)
                if isinstance(meta, dict):
                    result.model_used = meta.get("model_used")
                    if meta.get("tokens_used"):
                        result.metadata["tokens_used"] = meta["tokens_used"]

                # Safety-net: reviewer outputs sometimes arrive as raw_response
                # (e.g. fenced/truncated JSON). Ensure gating conditions can still
                # evaluate ${steps.<review>.outputs.review_report.overall_status}.
                if (
                    (
                        "review_report" in step_def.output_mapping
                        or step_def.name.startswith("review")
                    )
                    and "review_report" not in result.output_data
                ):
                    raw_text = str(result.output_data.get("raw_response", ""))
                    status_match = re.search(
                        r'"?overall_status"?\s*[:=]\s*"?([A-Za-z_ -]+)"?',
                        raw_text,
                        flags=re.IGNORECASE,
                    )
                    approved_match = re.search(
                        r'"?approved"?\s*[:=]\s*(true|false)',
                        raw_text,
                        flags=re.IGNORECASE,
                    )

                    if status_match:
                        raw_status = status_match.group(1).strip()
                    elif approved_match:
                        raw_status = (
                            "APPROVED"
                            if approved_match.group(1).lower() == "true"
                            else None
                        )
                    else:
                        raw_status = None  # normalize() defaults to NEEDS_FIXES

                    result.output_data["review_report"] = {
                        "overall_status": ReviewStatus.normalize(raw_status).value
                    }

                # Also normalize review_report.overall_status when it IS present
                if isinstance(result.output_data.get("review_report"), dict):
                    rr = result.output_data["review_report"]
                    if "overall_status" in rr:
                        rr["overall_status"] = ReviewStatus.normalize(
                            rr["overall_status"]
                        ).value

                for step_output, ctx_var in step_def.output_mapping.items():
                    if step_output in result.output_data:
                        await ctx.set(ctx_var, result.output_data[step_output])

                # Store step result in context for expression resolution
                # This enables ${steps.<name>.outputs.<key>} in when conditions
                step_view = {
                    "status": result.status.value,
                    "outputs": result.output_data,
                }
                # Store under a shared nested "steps" namespace so expressions
                # like ${steps.review_code.outputs.foo} resolve correctly.
                steps_state = ctx.get_sync("steps")
                if not isinstance(steps_state, dict):
                    steps_state = {}
                steps_state[step_def.name] = step_view
                ctx.set_sync("steps", steps_state)

                # Run post-hooks
                for hook in step_def.post_hooks:
                    await hook(ctx, step_def)

                # Loop-until logic (R5): re-execute until condition is satisfied
                if step_def.loop_until:
                    loop_iteration = result.metadata.get("loop_iteration", 1)
                    if loop_iteration < step_def.loop_max:
                        from .expressions import ExpressionEvaluator
                        satisfied = ExpressionEvaluator(ctx, {}).evaluate(
                            step_def.loop_until
                        )
                        if not satisfied:
                            result.metadata["loop_iteration"] = loop_iteration + 1
                            result.status = StepStatus.RUNNING
                            result.retry_count = 0
                            continue  # re-run the step body

                    result.metadata.setdefault("loop_iteration", loop_iteration)

                await ctx.mark_step_complete(step_def.name)
                break

            except asyncio.CancelledError:
                result.status = StepStatus.FAILED
                result.error = "Step was cancelled"
                result.error_type = "CancelledError"
                await ctx.mark_step_failed(step_def.name, result.error)
                break

            except asyncio.TimeoutError:
                result.status = StepStatus.FAILED
                result.error = f"Step timed out after {step_def.timeout_seconds}s"
                result.error_type = "TimeoutError"
                last_error = asyncio.TimeoutError(result.error)

                # Timeout typically shouldn't retry
                await ctx.mark_step_failed(step_def.name, result.error)
                break

            except Exception as e:
                last_error = e
                result.error = str(e)
                result.error_type = type(e).__name__

                # Check if should retry
                if (
                    attempt <= step_def.retry.max_retries
                    and step_def.retry.should_retry(e)
                ):
                    result.status = StepStatus.RETRYING
                    delay = step_def.retry.get_delay(attempt)
                    result.metadata[f"retry_{attempt}_delay"] = delay
                    await asyncio.sleep(delay)
                    continue

                # Run error hooks
                for hook in step_def.error_hooks:
                    try:
                        await hook(ctx, step_def)
                    except Exception:
                        pass  # Don't fail on error hook failure

                result.status = StepStatus.FAILED
                await ctx.mark_step_failed(step_def.name, result.error)
                break

        result.mark_complete(result.status == StepStatus.SUCCESS, result.error)
        return result

    async def _execute_with_timeout(
        self,
        func: StepFunction,
        ctx: ExecutionContext,
        timeout: Optional[float],
        step_name: str,
    ) -> dict[str, Any]:
        """Execute *func* as an asyncio task with optional wall-clock timeout.

        The task is tracked in ``_running_tasks`` so it can be cancelled
        externally via :meth:`cancel`.

        Args:
            func: The async step callable ``(ctx) → dict``.
            ctx: Child execution context with mapped inputs.
            timeout: Maximum seconds to wait (``None`` = no limit).
            step_name: Used as the key in ``_running_tasks``.

        Returns:
            The dict returned by *func*.

        Raises:
            asyncio.TimeoutError: If *timeout* is exceeded.
            asyncio.CancelledError: If the task is cancelled externally.
        """
        task = asyncio.create_task(func(ctx))
        self._running_tasks[step_name] = task

        try:
            if timeout:
                return await asyncio.wait_for(task, timeout=timeout)
            else:
                return await task
        finally:
            self._running_tasks.pop(step_name, None)

    async def cancel(self, step_name: str) -> bool:
        """Cancel a running step by name.

        Args:
            step_name: Name of the step to cancel.

        Returns:
            ``True`` if the task was found and cancelled, ``False`` otherwise.
        """
        task = self._running_tasks.get(step_name)
        if task and not task.done():
            task.cancel()
            return True
        return False

    async def cancel_all(self) -> int:
        """Cancel every currently running step.

        Returns:
            Number of tasks successfully cancelled.
        """
        count = 0
        for name in list(self._running_tasks.keys()):
            if await self.cancel(name):
                count += 1
        return count

    @staticmethod
    def _resolve_input_mapping_value(ctx: ExecutionContext, mapping_value: Any) -> Any:
        """Resolve an input mapping value from context.

        If *mapping_value* is a ``${...}`` expression string, delegates to
        :class:`ExpressionEvaluator`.  Otherwise performs a direct
        synchronous context lookup.

        Args:
            ctx: Execution context to resolve against.
            mapping_value: Either a ``${...}`` expression string or a
                plain context key name.

        Returns:
            The resolved value.
        """
        if not isinstance(mapping_value, str):
            return mapping_value

        expr = mapping_value.strip()
        if expr.startswith("${") and expr.endswith("}"):
            from .expressions import ExpressionEvaluator

            return ExpressionEvaluator(ctx).resolve_variable(expr[2:-1].strip())

        return ctx.get_sync(mapping_value)


# Convenience function for simple step execution
async def run_step(
    step_def: StepDefinition, ctx: Optional[ExecutionContext] = None
) -> StepResult:
    """Run a single step with optional context."""
    from .context import get_context

    if ctx is None:
        ctx = get_context()

    executor = StepExecutor()
    return await executor.execute(step_def, ctx)
