"""Workflow state definition for LangGraph.

Single TypedDict that flows through every node in the compiled graph.
Uses LangGraph annotation reducers for append-only fields.
"""

from __future__ import annotations

import operator
from typing import Annotated, Any, Sequence

from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict


class WorkflowState(TypedDict):
    """Central state for all LangGraph workflow executions.

    messages : list[BaseMessage]
        Append-only chat history.  Each node returns new messages
        that get appended via ``operator.add``.

    context : dict[str, Any]
        Mutable key/value store shared across steps.
        Last-writer-wins (overwrite merge).

    inputs : dict[str, Any]
        Immutable workflow inputs (set once at start).

    outputs : dict[str, Any]
        Collected workflow outputs (resolved at end).

    steps : dict[str, dict]
        Per-step status + output metadata for expression eval.

    current_step : str
        Currently executing step name.

    errors : list[str]
        Append-only error log.
    """

    messages: Annotated[Sequence[BaseMessage], operator.add]
    context: dict[str, Any]
    inputs: dict[str, Any]
    outputs: dict[str, Any]
    steps: dict[str, dict]
    current_step: str
    errors: Annotated[list[str], operator.add]


def initial_state(
    workflow_inputs: dict[str, Any] | None = None,
) -> WorkflowState:
    """Create a fresh state dict with safe defaults."""
    return WorkflowState(
        messages=[],
        context={},
        inputs=workflow_inputs or {},
        outputs={},
        steps={},
        current_step="",
        errors=[],
    )
