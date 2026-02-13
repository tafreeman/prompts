"""Cross-framework adapter conformance tests."""

from __future__ import annotations

import pytest

from agentic_v2.integrations.base import CanonicalEvent, TraceAdapter
from agentic_v2.integrations.langchain import AgenticAgent
from agentic_v2.integrations.microsoft_agent_framework import AgenticMicrosoftAgent


class CollectingTraceAdapter(TraceAdapter):
    """Collect emitted canonical events for assertions."""

    def __init__(self) -> None:
        self.events: list[CanonicalEvent] = []

    def emit(self, event: CanonicalEvent) -> None:
        self.events.append(event)


class DummyConformanceAgent:
    """Fixture agent used to validate adapter behavior parity."""

    name = "conformance_agent"

    async def run(self, prompt, context=None):
        return {"content": f"echo:{prompt}"}


async def _invoke_both(prompt: str = "hello"):
    lang_trace = CollectingTraceAdapter()
    ms_trace = CollectingTraceAdapter()

    base_agent = DummyConformanceAgent()
    lang_adapter = AgenticAgent(base_agent, trace_adapter=lang_trace)
    ms_adapter = AgenticMicrosoftAgent(base_agent, trace_adapter=ms_trace)

    lang_result = await lang_adapter.ainvoke(prompt, context={"source": "conformance"})
    ms_result = await ms_adapter.ainvoke(prompt, context={"source": "conformance"})

    return lang_result, ms_result, lang_trace, ms_trace


@pytest.mark.asyncio
async def test_status_parity() -> None:
    lang_result, ms_result, lang_trace, ms_trace = await _invoke_both()

    assert lang_result is not None
    assert ms_result is not None
    assert lang_trace.events
    assert ms_trace.events
    assert "complete" in lang_trace.events[-1].type
    assert "complete" in ms_trace.events[-1].type
    assert lang_trace.events[-1].type == ms_trace.events[-1].type


@pytest.mark.asyncio
async def test_output_parity() -> None:
    lang_result, ms_result, _lang_trace, _ms_trace = await _invoke_both()

    assert isinstance(lang_result, dict)
    assert lang_result
    assert any(value not in (None, "") for value in lang_result.values())

    assert ms_result is not None
    assert getattr(ms_result, "content", "")


@pytest.mark.asyncio
async def test_required_output_presence_parity() -> None:
    lang_result, ms_result, _lang_trace, _ms_trace = await _invoke_both()

    assert isinstance(lang_result, dict)
    assert "content" in lang_result
    assert str(lang_result["content"]).strip() != ""

    assert getattr(ms_result, "content", "").strip() != ""


@pytest.mark.asyncio
async def test_event_sequence_parity() -> None:
    _lang_result, _ms_result, lang_trace, ms_trace = await _invoke_both()

    assert lang_trace.events
    assert ms_trace.events

    lang_event_types = [event.type for event in lang_trace.events]
    ms_event_types = [event.type for event in ms_trace.events]
    assert lang_event_types == ms_event_types


@pytest.mark.asyncio
async def test_event_completeness() -> None:
    _lang_result, _ms_result, lang_trace, ms_trace = await _invoke_both()

    assert len(lang_trace.events) == 2
    assert len(ms_trace.events) == 2
    assert [event.type for event in lang_trace.events] == [
        "agent.invoke.start",
        "agent.invoke.complete",
    ]
    assert [event.type for event in ms_trace.events] == [
        "agent.invoke.start",
        "agent.invoke.complete",
    ]
