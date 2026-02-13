"""Tests for framework-neutral integration adapter contracts."""

from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest

from agentic_v2.contracts import StepStatus, WorkflowResult
from agentic_v2.integrations.base import (
    AgentAdapter,
    CanonicalEvent,
    ToolAdapter,
    TraceAdapter,
    WorkflowAdapter,
)
from agentic_v2.tools.base import ToolResult


def test_agent_adapter_is_abstract() -> None:
    with pytest.raises(TypeError):
        AgentAdapter()  # type: ignore[abstract]


def test_canonical_event_serializable() -> None:
    event = CanonicalEvent(
        type="step.completed",
        timestamp=datetime(2026, 2, 9, tzinfo=timezone.utc),
        step_name="analyze",
        data={"score": 0.88, "passed": True},
    )
    encoded = json.dumps(event.to_json_dict())
    decoded = json.loads(encoded)
    roundtrip = CanonicalEvent.from_json_dict(decoded)

    assert roundtrip.type == event.type
    assert roundtrip.timestamp == event.timestamp
    assert roundtrip.step_name == event.step_name
    assert roundtrip.data == event.data


def test_adapter_subclass_contract() -> None:
    class StubAgentAdapter(AgentAdapter):
        async def ainvoke(self, prompt, context=None):
            return {"prompt": prompt, "context": context or {}}

    class StubToolAdapter(ToolAdapter):
        async def execute(self, tool_name: str, args: dict):
            return ToolResult(success=True, data={"tool": tool_name, "args": args})

    class StubWorkflowAdapter(WorkflowAdapter):
        async def run(self, workflow_def, inputs):
            return WorkflowResult(
                workflow_id="wf-stub",
                workflow_name="stub",
                overall_status=StepStatus.SUCCESS,
                final_output={"inputs": inputs, "workflow": workflow_def},
            )

    class StubTraceAdapter(TraceAdapter):
        def __init__(self) -> None:
            self.events: list[CanonicalEvent] = []

        def emit(self, event: CanonicalEvent) -> None:
            self.events.append(event)

    assert isinstance(StubAgentAdapter(), AgentAdapter)
    assert isinstance(StubToolAdapter(), ToolAdapter)
    assert isinstance(StubWorkflowAdapter(), WorkflowAdapter)
    assert isinstance(StubTraceAdapter(), TraceAdapter)
