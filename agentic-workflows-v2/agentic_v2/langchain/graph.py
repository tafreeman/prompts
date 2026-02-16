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
from pathlib import Path
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, StateGraph

from .agents import create_agent, parse_agent_tier
from .config import StepConfig, WorkflowConfig
from .expressions import evaluate_condition, resolve_expression
from .state import WorkflowState

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


# ---------------------------------------------------------------------------
# Node factory
# ---------------------------------------------------------------------------


def _make_step_node(
    step: StepConfig,
    workflow: WorkflowConfig,
):
    """Create a graph node function for a workflow step.

    Returns a callable ``(state) -> state_update`` suitable for
    ``graph.add_node()``.
    """
    tier = parse_agent_tier(step.agent)

    # Tier 0: deterministic
    if tier == 0:
        deterministic_fn = _TIER0_REGISTRY.get(step.agent)

        def _tier0_node(state: WorkflowState) -> dict[str, Any]:
            # Resolve inputs into context
            ctx = dict(state.get("context", {}))
            for key, expr in step.inputs.items():
                ctx[key] = resolve_expression(expr, state)

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
            steps = dict(state.get("steps", {}))
            steps[step.name] = {"status": "success", "outputs": step_outputs}

            # Map outputs to context
            final_ctx = dict(result.get("context", ctx))
            for out_key, ctx_key in step.outputs.items():
                if out_key in step_outputs:
                    final_ctx[ctx_key] = step_outputs[out_key]

            return {
                "context": final_ctx,
                "steps": steps,
                "current_step": step.name,
            }

        return _tier0_node

    # Tier 1+: LLM-backed agent
    agent = create_agent(
        step.agent,
        tool_names=step.tools,
        prompt_file=step.prompt_file,
    )

    def _llm_node(state: WorkflowState) -> dict[str, Any]:
        # Build the user message from resolved inputs
        ctx = dict(state.get("context", {}))
        resolved_inputs: dict[str, Any] = {}
        for key, expr in step.inputs.items():
            resolved_inputs[key] = resolve_expression(expr, state)
            ctx[key] = resolved_inputs[key]

        task_description = (
            f"Step: {step.name}\n"
            f"Description: {step.description}\n"
            f"Inputs:\n{json.dumps(resolved_inputs, indent=2, default=str)}\n\n"
            f"Please complete this task and return your result."
        )

        # Expected output keys for structured output
        if step.outputs:
            output_keys = list(step.outputs.keys())
            task_description += (
                f"\n\nReturn your result as JSON with these keys: {output_keys}"
            )

        # Invoke the react agent
        try:
            agent_result = agent.invoke(
                {"messages": [HumanMessage(content=task_description)]}
            )
            # Extract the last AI message
            ai_messages = [
                m for m in agent_result.get("messages", [])
                if isinstance(m, AIMessage)
            ]
            response_text = ai_messages[-1].content if ai_messages else ""
        except Exception as e:
            logger.error("Agent %s failed: %s", step.agent, e)
            steps = dict(state.get("steps", {}))
            steps[step.name] = {"status": "failed", "error": str(e), "outputs": {}}
            return {
                "context": ctx,
                "steps": steps,
                "current_step": step.name,
                "errors": [f"Step {step.name} failed: {e}"],
            }

        # Try to parse structured output
        step_outputs: dict[str, Any] = {"raw_response": response_text}
        try:
            # Try JSON extraction
            parsed = json.loads(response_text)
            if isinstance(parsed, dict):
                step_outputs.update(parsed)
        except (json.JSONDecodeError, TypeError):
            pass

        # Map outputs to context
        for out_key, ctx_key in step.outputs.items():
            if out_key in step_outputs:
                ctx[ctx_key] = step_outputs[out_key]

        steps = dict(state.get("steps", {}))
        steps[step.name] = {"status": "success", "outputs": step_outputs}

        return {
            "context": ctx,
            "steps": steps,
            "current_step": step.name,
            "messages": [AIMessage(content=response_text)],
        }

    return _llm_node


# ---------------------------------------------------------------------------
# Graph compiler
# ---------------------------------------------------------------------------


def compile_workflow(config: WorkflowConfig) -> Any:
    """Compile a ``WorkflowConfig`` into a runnable LangGraph.

    Parameters
    ----------
    config:
        Parsed workflow config from YAML.

    Returns
    -------
    A compiled ``CompiledGraph`` ready to ``.invoke()`` or ``.stream()``.
    """
    if not config.steps:
        raise ValueError(f"Workflow '{config.name}' has no steps.")

    graph = StateGraph(WorkflowState)

    # Track which steps have dependents (for edge wiring)
    step_names = {s.name for s in config.steps}
    steps_with_deps: dict[str, list[str]] = {
        s.name: s.depends_on for s in config.steps
    }

    # Add nodes
    for step in config.steps:
        node_fn = _make_step_node(step, config)
        graph.add_node(step.name, node_fn)

    # Build a lookup for conditional steps
    conditional_steps = {s.name: s for s in config.steps if s.when}

    # Wire edges
    root_steps = [s.name for s in config.steps if not s.depends_on]

    # START → root steps
    if len(root_steps) == 1:
        graph.add_edge(START, root_steps[0])
    elif len(root_steps) > 1:
        # Fan out to all root steps
        for root in root_steps:
            graph.add_edge(START, root)

    # Dependency edges
    for step in config.steps:
        if not step.depends_on:
            continue

        for dep in step.depends_on:
            if dep not in step_names:
                raise ValueError(
                    f"Step '{step.name}' depends on unknown step '{dep}'"
                )

            # If this step has a 'when' condition, use conditional edge
            if step.when:
                _add_conditional_edge(graph, dep, step, config)
            else:
                graph.add_edge(dep, step.name)

    # Terminal steps (no one depends on them) → END
    has_dependents = set()
    for s in config.steps:
        has_dependents.update(s.depends_on)

    terminal_steps = [s.name for s in config.steps if s.name not in has_dependents]
    for term in terminal_steps:
        step_cfg = next(s for s in config.steps if s.name == term)
        if not step_cfg.loop_until:
            graph.add_edge(term, END)

    # Loop edges (loop_until)
    for step in config.steps:
        if step.loop_until:
            _add_loop_edge(graph, step)

    return graph.compile()


def _add_conditional_edge(
    graph: StateGraph,
    source: str,
    target_step: StepConfig,
    config: WorkflowConfig,
) -> None:
    """Add a conditional edge: source → target_step only if 'when' is True."""
    # Find other steps that also depend on the same source
    # to build a proper routing function
    when_expr = target_step.when

    def _route(state: WorkflowState) -> str:
        if evaluate_condition(when_expr, state):
            return target_step.name
        return END

    graph.add_conditional_edges(
        source,
        _route,
        {target_step.name: target_step.name, END: END},
    )


def _add_loop_edge(graph: StateGraph, step: StepConfig) -> None:
    """Add a self-loop: step re-runs until loop_until is True or loop_max."""
    loop_expr = step.loop_until
    max_iters = step.loop_max

    def _loop_route(state: WorkflowState) -> str:
        # Check iteration count
        step_data = state.get("steps", {}).get(step.name, {})
        iteration = step_data.get("loop_iteration", 1)

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
