"""Integration test for tracing in WorkflowRunner."""

import pytest
from agentic_v2.workflows.runner import WorkflowRunner
from agentic_v2.integrations.base import TraceAdapter, CanonicalEvent


class CaptureTraceAdapter(TraceAdapter):
    """Test adapter that captures events in a list."""
    def __init__(self):
        self.events = []

    def emit(self, event: CanonicalEvent):
        self.events.append(event)


@pytest.mark.asyncio
async def test_workflow_runner_uses_null_adapter_by_default():
    """WorkflowRunner uses NullTraceAdapter when none provided."""
    runner = WorkflowRunner()
    from agentic_v2.integrations.tracing import NullTraceAdapter

    assert isinstance(runner._trace_adapter, NullTraceAdapter)


@pytest.mark.asyncio
async def test_workflow_runner_accepts_trace_adapter():
    """WorkflowRunner accepts and stores a custom trace adapter."""
    capture = CaptureTraceAdapter()
    runner = WorkflowRunner(trace_adapter=capture)

    assert runner._trace_adapter is capture
    assert isinstance(runner._trace_adapter, TraceAdapter)
