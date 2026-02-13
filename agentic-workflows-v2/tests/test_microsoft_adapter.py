"""Tests for Microsoft adapter optional integration behavior."""

from __future__ import annotations

import pytest

from agentic_v2.integrations.base import CanonicalEvent, TraceAdapter
from agentic_v2.integrations.microsoft_agent_framework import (
    MICROSOFT_AGENT_FRAMEWORK_AVAILABLE,
    AgenticMicrosoftAgent,
)


class CollectingTraceAdapter(TraceAdapter):
    def __init__(self) -> None:
        self.events: list[CanonicalEvent] = []

    def emit(self, event: CanonicalEvent) -> None:
        self.events.append(event)


class DummyAsyncAgent:
    name = "dummy_ms_agent"

    async def run(self, prompt, context=None):
        return {
            "content": f"ok:{prompt}",
            "context_size": len((context or {}).keys()),
        }


def test_module_exposes_optional_dependency_flag() -> None:
    assert isinstance(MICROSOFT_AGENT_FRAMEWORK_AVAILABLE, bool)


def test_canonicalize_event_handles_missing_fields() -> None:
    event = AgenticMicrosoftAgent.canonicalize_event({"event_type": "step.completed"})
    assert event.type == "step.completed"
    assert event.step_name == ""
    assert event.data == {}


@pytest.mark.asyncio
async def test_adapter_invocation_and_trace_emission() -> None:
    trace = CollectingTraceAdapter()
    adapter = AgenticMicrosoftAgent(DummyAsyncAgent(), trace_adapter=trace)
    response = await adapter.ainvoke("hello", context={"x": 1})

    assert response.content == "ok:hello"
    assert response.metadata["context_size"] == 1
    assert len(trace.events) >= 2
    assert trace.events[0].type == "agent.invoke.start"
    assert trace.events[-1].type == "agent.invoke.complete"
