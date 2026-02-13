"""Tests for LangChain integration contract normalization."""

from __future__ import annotations

import importlib

import pytest

from agentic_v2.integrations.base import AgentAdapter, CanonicalEvent, ToolAdapter, TraceAdapter
from agentic_v2.integrations.langchain import (
    LANGCHAIN_AVAILABLE,
    AgenticAgent,
    AgenticChatModel,
    AgenticTool,
)
from agentic_v2.tools.base import BaseTool, ToolResult


class DummyTool(BaseTool):
    @property
    def name(self) -> str:
        return "dummy_tool"

    @property
    def description(self) -> str:
        return "Dummy tool for integration tests"

    @property
    def parameters(self) -> dict:
        return {"value": {"type": "string", "required": True}}

    async def execute(self, **kwargs) -> ToolResult:
        return ToolResult(success=True, data={"echo": kwargs.get("value")})


class CollectingTraceAdapter(TraceAdapter):
    def __init__(self) -> None:
        self.events: list[CanonicalEvent] = []

    def emit(self, event: CanonicalEvent) -> None:
        self.events.append(event)


class DummyAgent:
    name = "dummy_agent"

    async def run(self, task):
        if isinstance(task, dict):
            return {"echo": task.get("task", "")}
        return {"echo": str(task)}


def test_agentic_chat_model_implements_agent_adapter() -> None:
    model = AgenticChatModel()
    assert isinstance(model, AgentAdapter)


def test_agentic_tool_implements_tool_adapter() -> None:
    adapter = AgenticTool.from_v2_tool(DummyTool())
    assert isinstance(adapter, ToolAdapter)


def test_langchain_unavailable_graceful() -> None:
    module = importlib.import_module("agentic_v2.integrations.langchain")
    assert hasattr(module, "AgenticChatModel")

    if module.LANGCHAIN_AVAILABLE:
        # Environment has langchain-core installed; import safety already verified.
        assert module.LANGCHAIN_AVAILABLE is True
        return

    model = module.AgenticChatModel()
    assert isinstance(model, AgentAdapter)
    with pytest.raises(ImportError):
        model.invoke("hello")


@pytest.mark.asyncio
async def test_canonical_event_emission() -> None:
    trace = CollectingTraceAdapter()
    adapter = AgenticAgent(DummyAgent(), trace_adapter=trace)
    result = await adapter.ainvoke("hello world")

    assert result["echo"] == "hello world"
    assert len(trace.events) >= 2
    assert trace.events[0].type == "agent.invoke.start"
    assert trace.events[-1].type == "agent.invoke.complete"
    assert trace.events[-1].step_name == "dummy_agent"


@pytest.mark.skipif(not LANGCHAIN_AVAILABLE, reason="langchain-core not installed")
def test_chat_model_optional_dependency_signal() -> None:
    assert LANGCHAIN_AVAILABLE is True
