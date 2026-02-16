"""Top-level workflow runner.

Provides the high-level ``WorkflowRunner`` class that:
1. Loads a YAML workflow config
2. Validates inputs
3. Compiles it into a LangGraph
4. Executes (invoke / stream)
5. Resolves outputs
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, AsyncIterator

from .config import WorkflowConfig, load_workflow_config, list_workflows
from .expressions import resolve_expression
from .graph import compile_workflow
from .state import initial_state

logger = logging.getLogger(__name__)


@dataclass
class WorkflowResult:
    """Result of a workflow execution."""

    workflow_name: str
    status: str = "success"
    outputs: dict[str, Any] = field(default_factory=dict)
    steps: dict[str, dict] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    elapsed_seconds: float = 0.0
    final_state: dict[str, Any] = field(default_factory=dict)


class WorkflowRunner:
    """Load, validate, compile, and execute YAML workflows.

    Usage::

        runner = WorkflowRunner()
        result = await runner.run("code_review", code_file="main.py")

    Or synchronously::

        result = runner.invoke("code_review", code_file="main.py")
    """

    def __init__(
        self,
        definitions_dir: Path | None = None,
        checkpointer: Any = None,
    ):
        """
        Parameters
        ----------
        definitions_dir:
            Directory containing YAML workflow files.
        checkpointer:
            Optional LangGraph checkpointer (e.g. ``MemorySaver()``).
        """
        self._definitions_dir = definitions_dir
        self._checkpointer = checkpointer
        self._graph_cache: dict[str, Any] = {}

    # -----------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------

    def invoke(
        self,
        workflow_name: str,
        *,
        use_cache: bool = True,
        **inputs: Any,
    ) -> WorkflowResult:
        """Run a workflow synchronously.

        Parameters
        ----------
        workflow_name:
            Name of the YAML workflow (without extension).
        inputs:
            Keyword arguments matching the workflow's declared inputs.
        """
        config = load_workflow_config(workflow_name, self._definitions_dir)
        validated = self._validate_inputs(config, inputs)
        graph = self._get_or_compile(config, use_cache)

        state = initial_state(workflow_inputs=validated)
        # Seed context with inputs so ${inputs.X} resolves
        state["context"]["inputs"] = validated

        start = time.perf_counter()
        try:
            final = graph.invoke(state)
        except Exception as e:
            elapsed = time.perf_counter() - start
            return WorkflowResult(
                workflow_name=workflow_name,
                status="failed",
                errors=[str(e)],
                elapsed_seconds=elapsed,
            )

        elapsed = time.perf_counter() - start

        # Resolve declared outputs
        outputs = self._resolve_outputs(config, final)

        return WorkflowResult(
            workflow_name=workflow_name,
            status="success" if not final.get("errors") else "partial",
            outputs=outputs,
            steps=final.get("steps", {}),
            errors=final.get("errors", []),
            elapsed_seconds=elapsed,
            final_state=dict(final),
        )

    async def run(
        self,
        workflow_name: str,
        *,
        use_cache: bool = True,
        **inputs: Any,
    ) -> WorkflowResult:
        """Run a workflow asynchronously.

        Parameters
        ----------
        workflow_name:
            Name of the YAML workflow.
        inputs:
            Keyword arguments matching the workflow's declared inputs.
        """
        config = load_workflow_config(workflow_name, self._definitions_dir)
        validated = self._validate_inputs(config, inputs)
        graph = self._get_or_compile(config, use_cache)

        state = initial_state(workflow_inputs=validated)
        state["context"]["inputs"] = validated

        start = time.perf_counter()
        try:
            final = await graph.ainvoke(state)
        except Exception as e:
            elapsed = time.perf_counter() - start
            return WorkflowResult(
                workflow_name=workflow_name,
                status="failed",
                errors=[str(e)],
                elapsed_seconds=elapsed,
            )

        elapsed = time.perf_counter() - start
        outputs = self._resolve_outputs(config, final)

        return WorkflowResult(
            workflow_name=workflow_name,
            status="success" if not final.get("errors") else "partial",
            outputs=outputs,
            steps=final.get("steps", {}),
            errors=final.get("errors", []),
            elapsed_seconds=elapsed,
            final_state=dict(final),
        )

    def list_workflows(self) -> list[str]:
        """List available workflow names."""
        return list_workflows(self._definitions_dir)

    # -----------------------------------------------------------------
    # Internal
    # -----------------------------------------------------------------

    def _get_or_compile(
        self, config: WorkflowConfig, use_cache: bool
    ) -> Any:
        """Compile a WorkflowConfig to a graph, with optional caching."""
        if use_cache and config.name in self._graph_cache:
            return self._graph_cache[config.name]

        compiled = compile_workflow(config)
        if use_cache:
            self._graph_cache[config.name] = compiled
        return compiled

    def _validate_inputs(
        self,
        config: WorkflowConfig,
        supplied: dict[str, Any],
    ) -> dict[str, Any]:
        """Validate and apply defaults for workflow inputs."""
        result: dict[str, Any] = {}
        errors: list[str] = []

        for name, input_cfg in config.inputs.items():
            if name in supplied:
                value = supplied[name]
                # Enum validation
                if input_cfg.enum and value not in input_cfg.enum:
                    errors.append(
                        f"Input '{name}' must be one of {input_cfg.enum}, "
                        f"got '{value}'"
                    )
                result[name] = value
            elif input_cfg.default is not None:
                result[name] = input_cfg.default
            elif input_cfg.required:
                errors.append(f"Missing required input: '{name}'")

        if errors:
            raise ValueError(
                f"Input validation failed for '{config.name}': "
                + "; ".join(errors)
            )

        return result

    @staticmethod
    def _resolve_outputs(
        config: WorkflowConfig,
        final_state: dict[str, Any],
    ) -> dict[str, Any]:
        """Resolve declared outputs from final state."""
        outputs: dict[str, Any] = {}

        for name, output_cfg in config.outputs.items():
            value = resolve_expression(output_cfg.from_expr, final_state)
            if value is not None:
                outputs[name] = value
            elif not output_cfg.optional:
                logger.warning("Output '%s' could not be resolved", name)

        return outputs
