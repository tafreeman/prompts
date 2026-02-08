"""Workflow runner — unified entry point for YAML workflows.

Usage:
    runner = WorkflowRunner()
    result = await runner.run("code_review", code_file="main.py")

Combines:
- WorkflowLoader: YAML → WorkflowDefinition (DAG + inputs/outputs)
- DAGExecutor: dynamic parallel execution
- ExpressionEvaluator: runtime ${...} variable resolution
- Output resolution: map final context to declared outputs
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Awaitable, Callable, Optional

from ..contracts import StepStatus, WorkflowResult
from ..engine.context import ExecutionContext, get_context
from ..engine.dag_executor import DAGExecutor
from ..engine.expressions import ExpressionEvaluator
from ..engine.step import StepExecutor
from .loader import WorkflowDefinition, WorkflowLoader, WorkflowLoadError
from .run_logger import RunLogger

logger = logging.getLogger(__name__)


class WorkflowValidationError(ValueError):
    """Raised when workflow inputs fail validation."""

    def __init__(self, workflow: str, errors: list[str]):
        msg = f"Validation failed for workflow '{workflow}': " + "; ".join(errors)
        super().__init__(msg)
        self.workflow = workflow
        self.errors = errors


class WorkflowRunner:
    """Load, validate, execute, and resolve YAML workflows.

    This is the primary high-level API.  It orchestrates:
    1. Loading the YAML workflow (cached by default)
    2. Validating supplied inputs against the schema
    3. Seeding the ExecutionContext with validated inputs
    4. Running the DAG via DAGExecutor (max parallelism)
    5. Resolving declared workflow outputs from the final context
    """

    def __init__(
        self,
        definitions_dir: Path | None = None,
        step_executor: StepExecutor | None = None,
        max_concurrency: int = 10,
        run_logger: RunLogger | bool | None = None,
    ):
        self._loader = WorkflowLoader(definitions_dir=definitions_dir)
        self._step_executor = step_executor
        self._max_concurrency = max_concurrency
        # run_logger=True → auto-create with default dir; False/None → disabled
        if run_logger is True:
            self._run_logger: RunLogger | None = RunLogger()
        elif isinstance(run_logger, RunLogger):
            self._run_logger = run_logger
        else:
            self._run_logger = None

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #

    async def run(
        self,
        workflow_name: str,
        ctx: ExecutionContext | None = None,
        on_update: Optional[Callable[[dict[str, Any]], Awaitable[None]]] = None,
        dataset_meta: dict[str, Any] | None = None,
        **inputs: Any,
    ) -> WorkflowResult:
        """Run a named workflow end-to-end.

        Args:
            workflow_name: Name of the YAML workflow (without extension).
            ctx: Optional pre-built context; one is created if omitted.
            on_update: Optional async callback for step/workflow events.
            dataset_meta: Optional dataset provenance for run logging.
            **inputs: Keyword arguments matching declared workflow inputs.

        Returns:
            WorkflowResult with step results, final outputs, and status.

        Raises:
            WorkflowLoadError: If the YAML file cannot be found/parsed.
            WorkflowValidationError: If required inputs are missing.
        """
        # 1. Load
        definition = self._loader.load(workflow_name)

        # 2. Validate inputs
        validated = self._validate_inputs(definition, inputs)

        # 3. Build context
        if ctx is None:
            ctx = ExecutionContext(workflow_id=f"wf-{workflow_name}")

        # Seed inputs into context under an "inputs" namespace
        for key, value in validated.items():
            ctx.set_sync(f"inputs.{key}", value)
        # Also store the flat dict for expression resolution
        ctx.set_sync("inputs", validated)

        # 4. Execute DAG
        executor = DAGExecutor(step_executor=self._step_executor)
        result = await executor.execute(
            definition.dag,
            ctx,
            max_concurrency=self._max_concurrency,
            on_update=on_update,
        )

        # 5. Resolve outputs
        result.final_output = self._resolve_outputs(definition, ctx, result)
        result.workflow_name = definition.name

        # 6. Log run
        self._log_run(result, dataset_meta=dataset_meta, workflow_inputs=validated)

        return result

    async def run_definition(
        self,
        definition: WorkflowDefinition,
        ctx: ExecutionContext | None = None,
        on_update: Optional[Callable[[dict[str, Any]], Awaitable[None]]] = None,
        dataset_meta: dict[str, Any] | None = None,
        **inputs: Any,
    ) -> WorkflowResult:
        """Run a pre-loaded WorkflowDefinition (useful for testing)."""
        validated = self._validate_inputs(definition, inputs)

        if ctx is None:
            ctx = ExecutionContext(workflow_id=f"wf-{definition.name}")

        for key, value in validated.items():
            ctx.set_sync(f"inputs.{key}", value)
        ctx.set_sync("inputs", validated)

        executor = DAGExecutor(step_executor=self._step_executor)
        result = await executor.execute(
            definition.dag,
            ctx,
            max_concurrency=self._max_concurrency,
            on_update=on_update,
        )

        result.final_output = self._resolve_outputs(definition, ctx, result)
        result.workflow_name = definition.name

        self._log_run(result, dataset_meta=dataset_meta, workflow_inputs=validated)
        return result

    def list_workflows(self, include_experimental: bool = False) -> list[str]:
        """List available workflow names."""
        return self._loader.list_workflows(include_experimental=include_experimental)

    def _log_run(
        self,
        result: WorkflowResult,
        *,
        dataset_meta: dict[str, Any] | None = None,
        workflow_inputs: dict[str, Any] | None = None,
    ) -> None:
        """Log a run result if a RunLogger is configured."""
        if self._run_logger is None:
            return
        try:
            path = self._run_logger.log(
                result,
                dataset_meta=dataset_meta,
                workflow_inputs=workflow_inputs,
            )
            logger.info("Run logged to %s", path)
        except Exception:
            logger.exception("Failed to log run")

    # --------------------------------------------------------------------- #
    # Internal helpers
    # --------------------------------------------------------------------- #

    def _validate_inputs(
        self, definition: WorkflowDefinition, supplied: dict[str, Any]
    ) -> dict[str, Any]:
        """Validate and apply defaults for workflow inputs."""
        validated: dict[str, Any] = {}
        errors: list[str] = []

        for name, input_def in definition.inputs.items():
            if name in supplied:
                value = supplied[name]
                # Enum check
                if input_def.enum and value not in input_def.enum:
                    errors.append(
                        f"Input '{name}' must be one of {input_def.enum}, got '{value}'"
                    )
                validated[name] = value
            elif input_def.default is not None:
                validated[name] = input_def.default
            elif input_def.required:
                errors.append(f"Missing required input '{name}'")

        if errors:
            raise WorkflowValidationError(definition.name, errors)

        return validated

    @staticmethod
    def _resolve_outputs(
        definition: WorkflowDefinition,
        ctx: ExecutionContext,
        result: WorkflowResult,
    ) -> dict[str, Any]:
        """Resolve declared outputs from the execution context."""
        outputs: dict[str, Any] = {}
        unresolved_required_outputs: list[str] = []

        # Build step_results dict from the WorkflowResult so the evaluator
        # can resolve ${steps.X.outputs.Y} references.
        step_results = {s.step_name: s for s in result.steps}
        evaluator = ExpressionEvaluator(ctx, step_results)

        for name, output_def in definition.outputs.items():
            from_expr = output_def.from_expr
            if from_expr in ("", None):
                continue

            try:
                value = WorkflowRunner._resolve_output_expr(evaluator, from_expr)
                outputs[name] = value
                if value is None and not output_def.optional:
                    unresolved_required_outputs.append(name)
                    logger.warning(
                        "Required output '%s' resolved to None from '%s'",
                        name,
                        from_expr,
                    )
            except Exception:
                if not output_def.optional:
                    unresolved_required_outputs.append(name)
                    logger.warning(
                        "Failed to resolve required output '%s' from '%s'",
                        name,
                        from_expr,
                    )
                outputs[name] = None

        if unresolved_required_outputs:
            result.metadata["unresolved_required_outputs"] = sorted(
                set(unresolved_required_outputs)
            )
        else:
            result.metadata.pop("unresolved_required_outputs", None)

        return outputs

    @staticmethod
    def _resolve_output_expr(
        evaluator: ExpressionEvaluator,
        from_expr: Any,
    ) -> Any:
        """Resolve workflow output expressions from string/dict/list mappings."""
        if isinstance(from_expr, str):
            expr = from_expr.strip()
            if expr.startswith("${") and expr.endswith("}"):
                expr = expr[2:-1].strip()
            return evaluator.resolve_variable(expr)

        if isinstance(from_expr, dict):
            resolved: dict[str, Any] = {}
            for key, value in from_expr.items():
                resolved[key] = WorkflowRunner._resolve_output_expr(evaluator, value)
            return resolved

        if isinstance(from_expr, list):
            return [WorkflowRunner._resolve_output_expr(evaluator, item) for item in from_expr]

        return from_expr


# -------------------------------------------------------------------------
# Convenience function
# -------------------------------------------------------------------------

async def run_workflow(
    name: str,
    definitions_dir: Path | None = None,
    max_concurrency: int = 10,
    **inputs: Any,
) -> WorkflowResult:
    """One-liner to run a named workflow.

    Example:
        result = await run_workflow("code_review", code_file="main.py")
    """
    runner = WorkflowRunner(
        definitions_dir=definitions_dir, max_concurrency=max_concurrency
    )
    return await runner.run(name, **inputs)
