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
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, AsyncIterator, Iterator

from ..integrations.base import TraceAdapter
from ..integrations.tracing import NullTraceAdapter
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
    run_id: str = ""
    token_counts: dict[str, dict] = field(default_factory=dict)  # {step_name: {"input": N, "output": N}}
    models_used: dict[str, str] = field(default_factory=dict)  # {step_name: model_id}


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
        trace_adapter: TraceAdapter | None = None,
    ):
        """
        Parameters
        ----------
        definitions_dir:
            Directory containing YAML workflow files.
        checkpointer:
            Optional LangGraph checkpointer (e.g. ``MemorySaver()``).
        trace_adapter:
            Optional trace adapter for workflow-level observability.
        """
        self._definitions_dir = definitions_dir
        self._checkpointer = checkpointer
        self._trace_adapter = (
            trace_adapter if trace_adapter is not None else NullTraceAdapter()
        )
        self._graph_cache: dict[tuple[str, int | None], Any] = {}

    # -----------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------

    def invoke(
        self,
        workflow_name: str,
        *,
        use_cache: bool = True,
        thread_id: str | None = None,
        run_config: dict[str, Any] | None = None,
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
        langgraph_config = self._build_langgraph_config(thread_id, run_config)
        run_id = thread_id or str(uuid.uuid4())

        self._trace_adapter.emit_workflow_start(workflow_name, run_id, validated)

        state = initial_state(workflow_inputs=validated)
        # Seed context with inputs so ${inputs.X} resolves
        state["context"]["inputs"] = validated
        # Seed workflow_run_id for step tracing
        state["context"]["workflow_run_id"] = run_id

        start = time.perf_counter()
        try:
            if langgraph_config:
                try:
                    final = graph.invoke(state, config=langgraph_config)
                except TypeError:
                    logger.warning(
                        "Graph.invoke() does not support config argument in "
                        "this LangGraph version; running without thread config."
                    )
                    final = graph.invoke(state)
            else:
                final = graph.invoke(state)
        except Exception as e:
            elapsed = time.perf_counter() - start
            self._trace_adapter.emit_workflow_end(
                workflow_name,
                run_id,
                "failed",
                {"errors": [str(e)]},
            )
            return WorkflowResult(
                workflow_name=workflow_name,
                run_id=run_id,
                status="failed",
                errors=[str(e)],
                elapsed_seconds=elapsed,
            )

        elapsed = time.perf_counter() - start

        # Resolve declared outputs
        outputs = self._resolve_outputs(config, final)

        token_counts, models_used = self._extract_metadata(final)
        result = WorkflowResult(
            workflow_name=workflow_name,
            run_id=run_id,
            status="success" if not final.get("errors") else "partial",
            outputs=outputs,
            steps=final.get("steps", {}),
            errors=final.get("errors", []),
            elapsed_seconds=elapsed,
            final_state=dict(final),
            token_counts=token_counts,
            models_used=models_used,
        )
        self._trace_adapter.emit_workflow_end(
            workflow_name,
            run_id,
            result.status,
            result.outputs,
        )
        return result

    async def run(
        self,
        workflow_name: str,
        *,
        use_cache: bool = True,
        thread_id: str | None = None,
        run_config: dict[str, Any] | None = None,
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
        langgraph_config = self._build_langgraph_config(thread_id, run_config)
        run_id = thread_id or str(uuid.uuid4())

        self._trace_adapter.emit_workflow_start(workflow_name, run_id, validated)

        state = initial_state(workflow_inputs=validated)
        state["context"]["inputs"] = validated

        start = time.perf_counter()
        try:
            if langgraph_config:
                try:
                    final = await graph.ainvoke(state, config=langgraph_config)
                except TypeError:
                    logger.warning(
                        "Graph.ainvoke() does not support config argument in "
                        "this LangGraph version; running without thread config."
                    )
                    final = await graph.ainvoke(state)
            else:
                final = await graph.ainvoke(state)
        except Exception as e:
            elapsed = time.perf_counter() - start
            self._trace_adapter.emit_workflow_end(
                workflow_name,
                run_id,
                "failed",
                {"errors": [str(e)]},
            )
            return WorkflowResult(
                workflow_name=workflow_name,
                run_id=run_id,
                status="failed",
                errors=[str(e)],
                elapsed_seconds=elapsed,
            )

        elapsed = time.perf_counter() - start
        outputs = self._resolve_outputs(config, final)

        token_counts, models_used = self._extract_metadata(final)
        result = WorkflowResult(
            workflow_name=workflow_name,
            run_id=run_id,
            status="success" if not final.get("errors") else "partial",
            outputs=outputs,
            steps=final.get("steps", {}),
            errors=final.get("errors", []),
            elapsed_seconds=elapsed,
            final_state=dict(final),
            token_counts=token_counts,
            models_used=models_used,
        )
        self._trace_adapter.emit_workflow_end(
            workflow_name,
            run_id,
            result.status,
            result.outputs,
        )
        return result

    def stream(
        self,
        workflow_name: str,
        *,
        use_cache: bool = True,
        thread_id: str | None = None,
        run_config: dict[str, Any] | None = None,
        **inputs: Any,
    ) -> Iterator[dict[str, Any]]:
        """Stream workflow execution events synchronously."""
        config = load_workflow_config(workflow_name, self._definitions_dir)
        validated = self._validate_inputs(config, inputs)
        graph = self._get_or_compile(config, use_cache)
        langgraph_config = self._build_langgraph_config(thread_id, run_config)
        run_id = thread_id or str(uuid.uuid4())

        state = initial_state(workflow_inputs=validated)
        state["context"]["inputs"] = validated

        self._trace_adapter.emit_workflow_start(workflow_name, run_id, validated)

        stream_failed = False
        stream_error = ""

        try:
            if langgraph_config:
                try:
                    yield from graph.stream(state, config=langgraph_config)
                    return
                except TypeError:
                    logger.warning(
                        "Graph.stream() does not support config argument in "
                        "this LangGraph version; streaming without thread config."
                    )

            yield from graph.stream(state)
        except Exception as e:
            stream_failed = True
            stream_error = str(e)
            raise
        finally:
            self._trace_adapter.emit_workflow_end(
                workflow_name,
                run_id,
                "failed" if stream_failed else "success",
                {"errors": [stream_error]} if stream_failed else {},
            )

    async def astream(
        self,
        workflow_name: str,
        *,
        use_cache: bool = True,
        thread_id: str | None = None,
        run_config: dict[str, Any] | None = None,
        **inputs: Any,
    ) -> AsyncIterator[dict[str, Any]]:
        """Stream workflow execution events asynchronously."""
        config = load_workflow_config(workflow_name, self._definitions_dir)
        validated = self._validate_inputs(config, inputs)
        graph = self._get_or_compile(config, use_cache)
        langgraph_config = self._build_langgraph_config(thread_id, run_config)
        run_id = thread_id or str(uuid.uuid4())

        state = initial_state(workflow_inputs=validated)
        state["context"]["inputs"] = validated

        self._trace_adapter.emit_workflow_start(workflow_name, run_id, validated)

        stream_failed = False
        stream_error = ""

        try:
            if langgraph_config:
                try:
                    async for event in graph.astream(
                        state,
                        config=langgraph_config,
                    ):
                        yield event
                    return
                except TypeError:
                    logger.warning(
                        "Graph.astream() does not support config argument in "
                        "this LangGraph version; streaming without thread config."
                    )

            async for event in graph.astream(state):
                yield event
        except Exception as e:
            stream_failed = True
            stream_error = str(e)
            raise
        finally:
            self._trace_adapter.emit_workflow_end(
                workflow_name,
                run_id,
                "failed" if stream_failed else "success",
                {"errors": [stream_error]} if stream_failed else {},
            )

    def get_checkpoint_state(
        self,
        workflow_name: str,
        *,
        thread_id: str,
        use_cache: bool = True,
        run_config: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Return latest checkpoint state snapshot for a thread, if available."""
        config = load_workflow_config(workflow_name, self._definitions_dir)
        graph = self._get_or_compile(config, use_cache)
        langgraph_config = self._build_langgraph_config(thread_id, run_config)

        try:
            snapshot = graph.get_state(config=langgraph_config)
        except (AttributeError, TypeError):
            return None

        if snapshot is None:
            return None

        return {
            "values": getattr(snapshot, "values", None),
            "next": list(getattr(snapshot, "next", ()) or ()),
            "metadata": getattr(snapshot, "metadata", None),
            "created_at": getattr(snapshot, "created_at", None),
        }

    def get_checkpoint_history(
        self,
        workflow_name: str,
        *,
        thread_id: str,
        use_cache: bool = True,
        run_config: dict[str, Any] | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Return checkpoint history snapshots for a thread when supported."""
        config = load_workflow_config(workflow_name, self._definitions_dir)
        graph = self._get_or_compile(config, use_cache)
        langgraph_config = self._build_langgraph_config(thread_id, run_config)

        try:
            history_iter = graph.get_state_history(config=langgraph_config)
        except (AttributeError, TypeError):
            return []

        snapshots: list[dict[str, Any]] = []
        for idx, snapshot in enumerate(history_iter):
            if idx >= limit:
                break
            snapshots.append(
                {
                    "values": getattr(snapshot, "values", None),
                    "next": list(getattr(snapshot, "next", ()) or ()),
                    "metadata": getattr(snapshot, "metadata", None),
                    "created_at": getattr(snapshot, "created_at", None),
                }
            )
        return snapshots

    def resume(
        self,
        workflow_name: str,
        *,
        thread_id: str,
        use_cache: bool = True,
        run_config: dict[str, Any] | None = None,
    ) -> WorkflowResult:
        """Resume an interrupted workflow from the latest checkpoint thread state."""
        config = load_workflow_config(workflow_name, self._definitions_dir)
        graph = self._get_or_compile(config, use_cache)
        langgraph_config = self._build_langgraph_config(thread_id, run_config)

        start = time.perf_counter()
        self._trace_adapter.emit_workflow_start(
            workflow_name,
            thread_id,
            {"resume": True},
        )

        try:
            # Preferred LangGraph resume call when checkpointing is active.
            try:
                final = graph.invoke(None, config=langgraph_config)
            except TypeError:
                final = graph.invoke(None)
        except Exception as e:
            elapsed = time.perf_counter() - start
            self._trace_adapter.emit_workflow_end(
                workflow_name,
                thread_id,
                "failed",
                {"errors": [str(e)]},
            )
            return WorkflowResult(
                workflow_name=workflow_name,
                run_id=run_id,
                status="failed",
                errors=[str(e)],
                elapsed_seconds=elapsed,
            )

        elapsed = time.perf_counter() - start
        outputs = self._resolve_outputs(config, final)
        result = WorkflowResult(
            workflow_name=workflow_name,
            status="success" if not final.get("errors") else "partial",
            outputs=outputs,
            steps=final.get("steps", {}),
            errors=final.get("errors", []),
            elapsed_seconds=elapsed,
            final_state=dict(final),
        )
        self._trace_adapter.emit_workflow_end(
            workflow_name,
            thread_id,
            result.status,
            result.outputs,
        )
        return result

    def list_workflows(self) -> list[str]:
        """List available workflow names."""
        return list_workflows(self._definitions_dir)

    @staticmethod
    def _extract_metadata(final_state: dict[str, Any]) -> tuple[dict[str, dict], dict[str, str]]:
        """Extract token counts and models used from final workflow state."""
        token_counts: dict[str, dict] = {}
        models_used: dict[str, str] = {}

        for step_name, step_data in final_state.get("steps", {}).items():
            # Extract token counts if available in metadata
            meta = step_data.get("metadata", {})
            if meta.get("input_tokens") or meta.get("output_tokens"):
                token_counts[step_name] = {
                    "input": meta.get("input_tokens", 0),
                    "output": meta.get("output_tokens", 0),
                }
            # Extract model used if available
            if model := meta.get("model"):
                models_used[step_name] = model

        return token_counts, models_used

    # -----------------------------------------------------------------
    # Internal
    # -----------------------------------------------------------------

    def _get_or_compile(
        self, config: WorkflowConfig, use_cache: bool
    ) -> Any:
        """Compile a WorkflowConfig to a graph, with optional caching."""
        cache_key = (
            config.name,
            id(self._checkpointer) if self._checkpointer is not None else None,
            id(self._trace_adapter),
        )

        if use_cache and cache_key in self._graph_cache:
            return self._graph_cache[cache_key]

        compiled = compile_workflow(
            config,
            checkpointer=self._checkpointer,
            trace_adapter=self._trace_adapter,
        )
        if use_cache:
            self._graph_cache[cache_key] = compiled
        return compiled

    @staticmethod
    def _build_langgraph_config(
        thread_id: str | None,
        run_config: dict[str, Any] | None,
    ) -> dict[str, Any]:
        """Build LangGraph runtime config with optional thread checkpoint key."""
        config: dict[str, Any] = dict(run_config or {})

        if thread_id:
            configurable = dict(config.get("configurable", {}))
            configurable["thread_id"] = thread_id
            config["configurable"] = configurable

        return config

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
