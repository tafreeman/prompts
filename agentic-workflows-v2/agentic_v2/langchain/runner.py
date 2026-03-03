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
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, AsyncIterator, Iterator

from ..contracts import StepResult, StepStatus, WorkflowResult
from ..integrations.base import TraceAdapter
from ..integrations.tracing import NullTraceAdapter
from .config import WorkflowConfig, list_workflows, load_workflow_config
from .expressions import resolve_expression
from .graph import compile_workflow
from .state import initial_state

logger = logging.getLogger(__name__)


def _steps_dict_to_list(
    steps_dict: dict[str, dict],
    token_counts: dict[str, dict] | None = None,
    models_used: dict[str, str] | None = None,
) -> list[StepResult]:
    """Convert LangGraph step dict to a list of contract StepResult objects.

    Args:
        steps_dict: Mapping of step name → step data from LangGraph state.
        token_counts: Per-step token counts extracted from metadata.
        models_used: Per-step model identifiers.

    Returns:
        Ordered list of ``StepResult`` Pydantic models.
    """
    token_counts = token_counts or {}
    models_used = models_used or {}
    results: list[StepResult] = []

    for step_name, step_data in steps_dict.items():
        if not isinstance(step_data, dict):
            continue

        raw_status = step_data.get("status", "success")
        if raw_status == "success":
            status = StepStatus.SUCCESS
        elif raw_status in ("failed", "error"):
            status = StepStatus.FAILED
        elif raw_status == "skipped":
            status = StepStatus.SKIPPED
        else:
            logger.warning(
                "Unknown step status %r for step %r, defaulting to FAILED",
                raw_status,
                step_name,
            )
            status = StepStatus.FAILED

        step_tokens = token_counts.get(step_name, {})
        meta: dict[str, Any] = {}
        if step_tokens:
            meta["input_tokens"] = step_tokens.get("input", 0)
            meta["output_tokens"] = step_tokens.get("output", 0)

        results.append(
            StepResult(
                step_name=step_name,
                status=status,
                agent_role=step_data.get("agent"),
                model_used=models_used.get(step_name),
                input_data=step_data.get("inputs", {}),
                output_data=step_data.get("outputs", {}),
                error=step_data.get("error"),
                metadata=meta,
            )
        )

    return results


def _build_workflow_result(
    *,
    workflow_name: str,
    run_id: str,
    started_at: datetime,
    elapsed_seconds: float,
    final_state: dict[str, Any] | None = None,
    outputs: dict[str, Any] | None = None,
    steps: list[StepResult] | None = None,
    errors: list[str] | None = None,
    token_counts: dict[str, dict] | None = None,
    models_used: dict[str, str] | None = None,
    failed: bool = False,
) -> WorkflowResult:
    """Construct a canonical WorkflowResult from LangGraph execution state.

    Bridges between the LangGraph runner's internal data and the
    contract type used throughout the rest of the system.
    """
    errors = errors or []
    if failed or errors:
        overall_status = StepStatus.FAILED
    else:
        overall_status = StepStatus.SUCCESS

    ended_at = started_at + timedelta(seconds=elapsed_seconds)

    metadata: dict[str, Any] = {
        "elapsed_seconds": elapsed_seconds,
    }
    if token_counts:
        metadata["token_counts"] = token_counts
    if models_used:
        metadata["models_used"] = models_used
    if final_state is not None:
        metadata["final_state"] = final_state
    if errors:
        metadata["errors"] = errors

    return WorkflowResult(
        workflow_id=run_id,
        workflow_name=workflow_name,
        steps=steps or [],
        overall_status=overall_status,
        start_time=started_at,
        end_time=ended_at,
        final_output=outputs or {},
        metadata=metadata,
    )


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

        started_at = datetime.now(timezone.utc)
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
            return _build_workflow_result(
                workflow_name=workflow_name,
                run_id=run_id,
                started_at=started_at,
                elapsed_seconds=elapsed,
                errors=[str(e)],
                failed=True,
            )

        elapsed = time.perf_counter() - start

        # Resolve declared outputs
        outputs = self.resolve_outputs(config, final)

        token_counts, models_used = self.extract_metadata(final)
        errors = [str(e) for e in final.get("errors", []) if e]
        step_results = _steps_dict_to_list(
            final.get("steps", {}), token_counts, models_used
        )
        result = _build_workflow_result(
            workflow_name=workflow_name,
            run_id=run_id,
            started_at=started_at,
            elapsed_seconds=elapsed,
            final_state=dict(final),
            outputs=outputs,
            steps=step_results,
            errors=errors,
            token_counts=token_counts,
            models_used=models_used,
        )
        self._trace_adapter.emit_workflow_end(
            workflow_name,
            run_id,
            result.overall_status.value,
            result.final_output,
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
        # Ensure step-level trace events can be correlated to this run.
        state["context"]["workflow_run_id"] = run_id

        started_at = datetime.now(timezone.utc)
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
            return _build_workflow_result(
                workflow_name=workflow_name,
                run_id=run_id,
                started_at=started_at,
                elapsed_seconds=elapsed,
                errors=[str(e)],
                failed=True,
            )

        elapsed = time.perf_counter() - start
        outputs = self.resolve_outputs(config, final)

        token_counts, models_used = self.extract_metadata(final)
        errors = [str(e) for e in final.get("errors", []) if e]
        step_results = _steps_dict_to_list(
            final.get("steps", {}), token_counts, models_used
        )
        result = _build_workflow_result(
            workflow_name=workflow_name,
            run_id=run_id,
            started_at=started_at,
            elapsed_seconds=elapsed,
            final_state=dict(final),
            outputs=outputs,
            steps=step_results,
            errors=errors,
            token_counts=token_counts,
            models_used=models_used,
        )
        self._trace_adapter.emit_workflow_end(
            workflow_name,
            run_id,
            result.overall_status.value,
            result.final_output,
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
        # Ensure step-level trace events can be correlated to this run.
        state["context"]["workflow_run_id"] = run_id

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
        # Ensure step-level trace events can be correlated to this run.
        state["context"]["workflow_run_id"] = run_id

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
        """Return latest checkpoint state snapshot for a thread, if
        available."""
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
        """Resume an interrupted workflow from the latest checkpoint thread
        state."""
        config = load_workflow_config(workflow_name, self._definitions_dir)
        graph = self._get_or_compile(config, use_cache)
        langgraph_config = self._build_langgraph_config(thread_id, run_config)

        started_at = datetime.now(timezone.utc)
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
            return _build_workflow_result(
                workflow_name=workflow_name,
                run_id=thread_id,
                started_at=started_at,
                elapsed_seconds=elapsed,
                errors=[str(e)],
                failed=True,
            )

        elapsed = time.perf_counter() - start
        outputs = self.resolve_outputs(config, final)
        token_counts, models_used = self.extract_metadata(final)
        errors = [str(e) for e in final.get("errors", []) if e]
        step_results = _steps_dict_to_list(
            final.get("steps", {}), token_counts, models_used
        )
        result = _build_workflow_result(
            workflow_name=workflow_name,
            run_id=thread_id,
            started_at=started_at,
            elapsed_seconds=elapsed,
            final_state=dict(final),
            outputs=outputs,
            steps=step_results,
            errors=errors,
            token_counts=token_counts,
            models_used=models_used,
        )
        self._trace_adapter.emit_workflow_end(
            workflow_name,
            thread_id,
            result.overall_status.value,
            result.final_output,
        )
        return result

    def list_workflows(self) -> list[str]:
        """List available workflow names."""
        return list_workflows(self._definitions_dir)

    @staticmethod
    def extract_metadata(
        final_state: dict[str, Any],
    ) -> tuple[dict[str, dict], dict[str, str]]:
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

    def _get_or_compile(self, config: WorkflowConfig, use_cache: bool) -> Any:
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
        """Build LangGraph runtime config with optional thread checkpoint
        key."""
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
                f"Input validation failed for '{config.name}': " + "; ".join(errors)
            )

        return result

    @staticmethod
    def resolve_outputs(
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
