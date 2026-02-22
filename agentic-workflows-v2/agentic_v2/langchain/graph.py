"""Graph compiler — turns YAML WorkflowConfig into a LangGraph StateGraph.

This is the heart of the system.  It reads the parsed config from
``config.py`` and programmatically builds a ``StateGraph`` with:

- One node per YAML step
- Edges derived from ``depends_on``
- Conditional edges from ``when`` expressions
- Loop edges from ``loop_until`` expressions
"""

from __future__ import annotations

import ast as python_ast
import json
import logging
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, StateGraph

from .agents import create_agent, parse_agent_tier
from .config import StepConfig, WorkflowConfig
from .expressions import evaluate_condition, resolve_expression
from .models import get_model_candidates_for_tier, is_retryable_model_error
from .state import WorkflowState
from ..integrations.base import TraceAdapter
from ..integrations.tracing import NullTraceAdapter

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Tier-0 deterministic step implementations
# ---------------------------------------------------------------------------


def _tier0_parse_code(state: WorkflowState) -> dict[str, Any]:
    """Deterministic code parsing (no LLM)."""
    ctx = dict(state.get("context", {}))
    file_path = ctx.get("file_path") or state.get("inputs", {}).get("code_file", "")

    result: dict[str, Any] = {
        "parsed_ast": "{}",
        "code_metrics": "{}",
    }

    if not file_path:
        return {
            "context": {**ctx, **result},
            "steps": {
                **state.get("steps", {}),
                "__current__": {"status": "success", "outputs": result},
            },
        }

    p = Path(file_path)
    if p.exists() and p.suffix == ".py":
        try:
            code = p.read_text(encoding="utf-8")
            tree = python_ast.parse(code)
            functions = [
                n.name
                for n in python_ast.walk(tree)
                if isinstance(n, python_ast.FunctionDef | python_ast.AsyncFunctionDef)
            ]
            classes = [
                n.name
                for n in python_ast.walk(tree)
                if isinstance(n, python_ast.ClassDef)
            ]
            result["parsed_ast"] = json.dumps(
                {"functions": functions, "classes": classes}
            )
            result["code_metrics"] = json.dumps(
                {"lines": len(code.splitlines()), "functions": len(functions)}
            )
        except Exception as e:
            result["parsed_ast"] = json.dumps({"error": str(e)})

    return {
        "context": {**ctx, **result},
        "steps": {
            **state.get("steps", {}),
            "__current__": {"status": "success", "outputs": result},
        },
    }


_TIER0_REGISTRY: dict[str, Any] = {
    "tier0_parser": _tier0_parse_code,
}


def _resolve_inputs_into_context(
    step: StepConfig,
    state: WorkflowState,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Resolve step input expressions into context and return both."""
    ctx = dict(state.get("context", {}))
    resolved_inputs: dict[str, Any] = {}
    for key, expr in step.inputs.items():
        value = resolve_expression(expr, state)
        resolved_inputs[key] = value
        ctx[key] = value
    return ctx, resolved_inputs


def _next_iteration(state: WorkflowState, step_name: str) -> int:
    """Compute next loop iteration number for a step."""
    existing = state.get("steps", {}).get(step_name, {})
    return existing.get("loop_iteration", 0) + 1


def _record_step_result(
    state: WorkflowState,
    step_name: str,
    status: str,
    outputs: dict[str, Any],
    *,
    error: str | None = None,
    metadata: dict[str, Any] | None = None,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
) -> dict[str, dict]:
    """Return updated steps dict for a completed/failed step."""
    steps = dict(state.get("steps", {}))
    payload: dict[str, Any] = {
        "status": status,
        "outputs": outputs,
        "loop_iteration": _next_iteration(state, step_name),
    }
    if error:
        payload["error"] = error
    if metadata:
        payload["metadata"] = metadata
    if start_time:
        payload["start_time"] = start_time.isoformat()
    if end_time:
        payload["end_time"] = end_time.isoformat()
        if start_time:
            payload["duration_ms"] = (end_time - start_time).total_seconds() * 1000
    steps[step_name] = payload
    return steps


def _map_step_outputs_to_context(
    step: StepConfig,
    step_outputs: dict[str, Any],
    ctx: dict[str, Any],
) -> dict[str, Any]:
    """Map declared step outputs into context keys."""
    final_ctx = dict(ctx)
    for out_key, ctx_key in step.outputs.items():
        if out_key in step_outputs:
            final_ctx[ctx_key] = step_outputs[out_key]
    return final_ctx


def _build_task_description(step: StepConfig, resolved_inputs: dict[str, Any]) -> str:
    """Create an LLM task prompt payload for a workflow step."""
    task_description = (
        f"Step: {step.name}\n"
        f"Description: {step.description}\n"
        f"Inputs:\n{json.dumps(resolved_inputs, indent=2, default=str)}\n\n"
        f"Please complete this task and return your result."
    )
    if step.outputs:
        output_keys = list(step.outputs.keys())
        task_description += (
            f"\n\nReturn your result as JSON with these keys: {output_keys}"
        )
    return task_description


def _extract_agent_response_text(agent_result: dict[str, Any]) -> str:
    """Extract the final AIMessage text from an agent response payload."""
    ai_messages = [
        m for m in agent_result.get("messages", [])
        if isinstance(m, AIMessage)
    ]
    if not ai_messages:
        return ""
    return _coerce_message_content_to_text(ai_messages[-1].content)


def _coerce_message_content_to_text(content: Any) -> str:
    """Normalize provider-specific message content into plain text."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, (int, float, bool)):
        return str(content)
    if isinstance(content, list):
        parts = [_coerce_message_content_to_text(item) for item in content]
        return "\n".join(part for part in parts if part and part.strip())
    if isinstance(content, dict):
        # Common LangChain/OpenAI/Gemini message block shapes.
        for key in ("text", "output_text", "content", "message"):
            if key in content:
                text = _coerce_message_content_to_text(content.get(key))
                if text:
                    return text
        try:
            return json.dumps(content, ensure_ascii=False, default=str)
        except TypeError:
            return str(content)
    return str(content)


def _parse_json_dict_from_text(text: str) -> dict[str, Any] | None:
    """Best-effort JSON object extraction from model text output."""
    raw = text.strip()
    if not raw:
        return None

    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass

    fenced = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", raw, flags=re.DOTALL | re.IGNORECASE)
    for candidate in fenced:
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            continue

    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            parsed = json.loads(raw[start : end + 1])
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

    return None


def _parse_step_outputs(response_text: Any) -> dict[str, Any]:
    """Parse structured output from model response text when possible."""
    normalized = _coerce_message_content_to_text(response_text)
    step_outputs: dict[str, Any] = {"raw_response": normalized}
    parsed = _parse_json_dict_from_text(normalized)
    if isinstance(parsed, dict):
        step_outputs.update(parsed)
    return step_outputs


def _extract_agent_metadata(agent_result: dict[str, Any]) -> dict[str, Any]:
    """Extract token usage and model info from agent response."""
    metadata: dict[str, Any] = {}

    # Try to find the last AIMessage
    messages = agent_result.get("messages", [])
    if not messages:
        return metadata

    last_msg = messages[-1]
    if not isinstance(last_msg, AIMessage):
        # Look backwards for the last AIMessage
        for msg in reversed(messages):
            if isinstance(msg, AIMessage):
                last_msg = msg
                break
        else:
            return metadata

    # 1. Token usage from usage_metadata (standard LangChain)
    if hasattr(last_msg, "usage_metadata") and last_msg.usage_metadata:
        usage = last_msg.usage_metadata
        metadata["input_tokens"] = usage.get("input_tokens")
        metadata["output_tokens"] = usage.get("output_tokens")
        metadata["total_tokens"] = usage.get("total_tokens")

    # 2. Token usage from response_metadata (provider specific)
    elif hasattr(last_msg, "response_metadata"):
        rm = last_msg.response_metadata
        # OpenAI/Azure often put it in 'token_usage'
        if "token_usage" in rm:
            usage = rm["token_usage"]
            metadata["input_tokens"] = usage.get("prompt_tokens")
            metadata["output_tokens"] = usage.get("completion_tokens")
            metadata["total_tokens"] = usage.get("total_tokens")
        # Anthropic often puts it in 'usage'
        elif "usage" in rm:
            usage = rm["usage"]
            metadata["input_tokens"] = usage.get("input_tokens")
            metadata["output_tokens"] = usage.get("output_tokens")

        # Model name
        if "model_name" in rm:
            metadata["model"] = rm["model_name"]
        elif "model" in rm:
            metadata["model"] = rm["model"]

    return metadata


# ---------------------------------------------------------------------------
# Node factory
# ---------------------------------------------------------------------------


def _make_step_node(
    step: StepConfig,
    workflow: WorkflowConfig,
    trace_adapter: Optional[TraceAdapter] = None,
    *,
    validate_only: bool = False,
):
    """Create a graph node function for a workflow step.

    Returns a callable ``(state) -> state_update`` suitable for
    ``graph.add_node()``.
    """
    tier = parse_agent_tier(step.agent)
    _trace = trace_adapter or NullTraceAdapter()

    # Tier 0: deterministic
    if tier == 0:
        deterministic_fn = _TIER0_REGISTRY.get(step.agent)

        def _tier0_node(state: WorkflowState) -> dict[str, Any]:
            run_id = state.get("context", {}).get("workflow_run_id", "")
            start_time = datetime.now(timezone.utc)
            _trace.emit_step_start(step.name, run_id, {})

            ctx, _ = _resolve_inputs_into_context(step, state)

            updated = {**state, "context": ctx}
            if deterministic_fn:
                result = deterministic_fn(updated)
            else:
                # Unknown tier0 agent — noop
                result = {"context": ctx}

            # Move step outputs from __current__ into named step
            step_outputs = (
                result.get("steps", {}).get("__current__", {}).get("outputs", {})
            )
            end_time = datetime.now(timezone.utc)
            steps = _record_step_result(
                state,
                step.name,
                "success",
                step_outputs,
                start_time=start_time,
                end_time=end_time,
            )

            # Map outputs to context
            final_ctx = _map_step_outputs_to_context(
                step,
                step_outputs,
                dict(result.get("context", ctx)),
            )

            _trace.emit_step_complete(step.name, run_id, "success", step_outputs)

            return {
                "context": final_ctx,
                "steps": steps,
                "current_step": step.name,
            }

        return _tier0_node

    # Validation mode: compile graph shape without requiring provider/model setup.
    if validate_only:
        def _validation_noop(state: WorkflowState) -> dict[str, Any]:
            return {
                "context": dict(state.get("context", {})),
                "steps": {
                    **state.get("steps", {}),
                    step.name: {
                        "status": "validation",
                        "outputs": {},
                        "loop_iteration": _next_iteration(state, step.name),
                    },
                },
                "current_step": step.name,
            }

        return _validation_noop

    # Tier 1+: LLM-backed agent with runtime failover chain
    model_candidates = get_model_candidates_for_tier(
        tier,
        step.model_override,
        include_unavailable=False,
        include_gh_backup=True,
    )
    agent_cache: dict[str, Any] = {}

    def _get_agent_for_model(model_id: str) -> Any:
        cached = agent_cache.get(model_id)
        if cached is not None:
            return cached
        agent = create_agent(
            step.agent,
            tool_names=step.tools,
            prompt_file=step.prompt_file,
            model_override=model_id,
        )
        agent_cache[model_id] = agent
        return agent

    def _llm_node(state: WorkflowState) -> dict[str, Any]:
        run_id = state.get("context", {}).get("workflow_run_id", "")
        start_time = datetime.now(timezone.utc)
        ctx, resolved_inputs = _resolve_inputs_into_context(step, state)
        _trace.emit_step_start(step.name, run_id, resolved_inputs)

        task_description = _build_task_description(step, resolved_inputs)

        attempt_errors: list[dict[str, Any]] = []
        attempted_models: list[str] = []
        agent_result: dict[str, Any] | None = None
        response_text = ""
        metadata: dict[str, Any] = {}

        # Invoke the react agent with failover across candidate models.
        for model_id in model_candidates:
            attempted_models.append(model_id)
            try:
                agent = _get_agent_for_model(model_id)
                agent_result = agent.invoke(
                    {"messages": [HumanMessage(content=task_description)]}
                )
                response_text = _extract_agent_response_text(agent_result)
                metadata = _extract_agent_metadata(agent_result)
                metadata.setdefault("model", model_id)
                break
            except Exception as e:
                retryable = is_retryable_model_error(e)
                attempt_errors.append(
                    {
                        "model": model_id,
                        "error": str(e),
                        "retryable": retryable,
                    }
                )
                logger.warning(
                    "Step %s model attempt failed (%s, retryable=%s): %s",
                    step.name,
                    model_id,
                    retryable,
                    e,
                )

        if agent_result is None:
            err_text = "All model attempts failed"
            if attempt_errors:
                last = attempt_errors[-1]
                err_text = (
                    f"{err_text} (last model={last.get('model')}: {last.get('error')})"
                )
            end_time = datetime.now(timezone.utc)
            steps = _record_step_result(
                state,
                step.name,
                "failed",
                {},
                error=err_text,
                start_time=start_time,
                end_time=end_time,
            )
            _trace.emit_step_complete(
                step.name,
                run_id,
                "failed",
                {
                    "error": err_text,
                    "attempted_models": attempted_models,
                    "attempt_errors": attempt_errors,
                },
            )
            return {
                "context": ctx,
                "steps": steps,
                "current_step": step.name,
                "errors": [f"Step {step.name} failed: {err_text}"],
            }

        if attempt_errors:
            metadata["attempted_models"] = attempted_models
            metadata["attempt_errors"] = attempt_errors

        step_outputs = _parse_step_outputs(response_text)

        # Map outputs to context
        ctx = _map_step_outputs_to_context(step, step_outputs, ctx)

        end_time = datetime.now(timezone.utc)
        steps = _record_step_result(
            state,
            step.name,
            "success",
            step_outputs,
            metadata=metadata,
            start_time=start_time,
            end_time=end_time,
        )

        _trace.emit_step_complete(step.name, run_id, "success", step_outputs)

        return {
            "context": ctx,
            "steps": steps,
            "current_step": step.name,
            "messages": [AIMessage(content=response_text)],
            "metadata": metadata,
        }

    return _llm_node


# ---------------------------------------------------------------------------
# Graph compiler
# ---------------------------------------------------------------------------


def _add_step_nodes(
    graph: StateGraph,
    config: WorkflowConfig,
    trace_adapter: Optional[TraceAdapter] = None,
    *,
    validate_only: bool = False,
) -> None:
    """Add one graph node per configured workflow step."""
    for step in config.steps:
        graph.add_node(
            step.name,
            _make_step_node(
                step,
                config,
                trace_adapter,
                validate_only=validate_only,
            ),
        )


def _add_start_edges(graph: StateGraph, root_steps: list[str]) -> None:
    """Wire START to all root steps."""
    if len(root_steps) == 1:
        graph.add_edge(START, root_steps[0])
        return
    for root in root_steps:
        graph.add_edge(START, root)


def _validate_dependencies(config: WorkflowConfig, step_names: set[str]) -> None:
    """Validate all depends_on references exist in workflow steps."""
    for step in config.steps:
        for dep in step.depends_on:
            if dep not in step_names:
                raise ValueError(
                    f"Step '{step.name}' depends on unknown step '{dep}'"
                )


def _build_outgoing_map(config: WorkflowConfig) -> dict[str, list[StepConfig]]:
    """Build mapping of source-step to dependents."""
    outgoing: dict[str, list[StepConfig]] = defaultdict(list)
    for step in config.steps:
        for dep in step.depends_on:
            outgoing[dep].append(step)
    return outgoing


def _wire_dependency_edges(
    graph: StateGraph,
    outgoing: dict[str, list[StepConfig]],
) -> None:
    """Wire dependency edges from the outgoing map."""
    for source, dependents in outgoing.items():
        unconditional = [s for s in dependents if not s.when]
        conditional = [s for s in dependents if s.when]
        if not conditional:
            for step in unconditional:
                graph.add_edge(source, step.name)
            continue
        _add_fan_out_edges(graph, source, unconditional, conditional)


def _add_terminal_edges(graph: StateGraph, config: WorkflowConfig) -> None:
    """Add END edges for terminal (non-loop) steps."""
    has_dependents = set()
    for step in config.steps:
        has_dependents.update(step.depends_on)

    step_by_name = {step.name: step for step in config.steps}
    terminal_steps = [
        step.name for step in config.steps if step.name not in has_dependents
    ]
    for step_name in terminal_steps:
        step_cfg = step_by_name[step_name]
        if not step_cfg.loop_until:
            graph.add_edge(step_name, END)


def _add_loop_edges(graph: StateGraph, config: WorkflowConfig) -> None:
    """Add self-loop wiring for loop-enabled steps."""
    for step in config.steps:
        if step.loop_until:
            _add_loop_edge(graph, step)


def _compile_graph(graph: StateGraph, checkpointer: Any = None) -> Any:
    """Compile graph with optional checkpointer, with compatibility fallback."""
    if checkpointer is None:
        return graph.compile()
    try:
        return graph.compile(checkpointer=checkpointer)
    except TypeError:
        logger.warning(
            "Graph.compile() does not accept checkpointer in this LangGraph "
            "version; proceeding without checkpointing."
        )
        return graph.compile()


def compile_workflow(
    config: WorkflowConfig,
    checkpointer: Any = None,
    trace_adapter: Optional[TraceAdapter] = None,
    *,
    validate_only: bool = False,
) -> Any:
    """Compile a ``WorkflowConfig`` into a runnable LangGraph.

    Parameters
    ----------
    config:
        Parsed workflow config from YAML.
    checkpointer:
        Optional LangGraph checkpointer for persistence.
    trace_adapter:
        Optional trace adapter for step-level observability.
    validate_only:
        When True, compile graph topology without constructing live agents.

    Returns
    -------
    A compiled ``CompiledGraph`` ready to ``.invoke()`` or ``.stream()``.
    """
    if not config.steps:
        raise ValueError(f"Workflow '{config.name}' has no steps.")

    graph = StateGraph(WorkflowState)
    step_names = {s.name for s in config.steps}
    root_steps = [s.name for s in config.steps if not s.depends_on]

    _add_step_nodes(graph, config, trace_adapter, validate_only=validate_only)
    _add_start_edges(graph, root_steps)
    _validate_dependencies(config, step_names)
    _wire_dependency_edges(graph, _build_outgoing_map(config))
    _add_terminal_edges(graph, config)
    _add_loop_edges(graph, config)

    return _compile_graph(graph, checkpointer)


def _add_fan_out_edges(
    graph: StateGraph,
    source: str,
    unconditional: list[StepConfig],
    conditional: list[StepConfig],
) -> None:
    """Wire fan-out edges from one source to multiple dependents.

    Unconditional targets always run; conditional targets gate on their ``when``
    expression.  Returns a list so LangGraph fans out in parallel.
    """
    # Snapshot expressions for closures
    cond_pairs = [(s.name, s.when) for s in conditional]
    uncond_names = [s.name for s in unconditional]

    path_map: dict[str, str] = {n: n for n in uncond_names}
    for name, _ in cond_pairs:
        path_map[name] = name
    path_map[END] = END

    def _route(state: WorkflowState) -> list[str]:
        targets = list(uncond_names)
        for name, when_expr in cond_pairs:
            if evaluate_condition(when_expr, state):
                targets.append(name)
        return targets if targets else [END]

    graph.add_conditional_edges(source, _route, path_map)


def _add_loop_edge(graph: StateGraph, step: StepConfig) -> None:
    """Add a self-loop: step re-runs until loop_until is True or loop_max."""
    loop_expr = step.loop_until
    max_iters = step.loop_max

    def _loop_route(state: WorkflowState) -> str:
        # Check iteration count
        step_data = state.get("steps", {}).get(step.name, {})
        iteration = step_data.get("loop_iteration", 0)

        if iteration >= max_iters:
            return END

        if evaluate_condition(loop_expr, state):
            return END  # Condition met, stop looping

        # Update iteration count
        return step.name  # Loop back

    graph.add_conditional_edges(
        step.name,
        _loop_route,
        {step.name: step.name, END: END},
    )
