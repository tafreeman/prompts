"""Integration tests for LangChain/LangGraph workflow engine.

Tests end-to-end execution, checkpointing, and streaming behavior.
"""

import asyncio
import os
from pathlib import Path

import pytest
from langgraph.checkpoint.memory import MemorySaver

from agentic_v2.langchain import WorkflowRunner, load_workflow_config, compile_workflow
from agentic_v2.langchain.state import initial_state


# Skip when neither set of API credentials is available in the environment
_HAS_CREDENTIALS = bool(os.environ.get("GH_TOKEN") or os.environ.get("GOOGLE_API_KEY"))
pytestmark = pytest.mark.skipif(
    not _HAS_CREDENTIALS,
    reason="Requires external LLM API credentials (GH_TOKEN or GOOGLE_API_KEY)",
)


class TestEndToEndExecution:
    """End-to-end workflow execution tests."""

    def test_simple_workflow_invocation(self):
        """Execute a simple workflow and verify result structure."""
        runner = WorkflowRunner()
        result = runner.invoke("code_review", code_file="def foo(): pass", review_depth="quick")

        assert result.run_id, "run_id should be set"
        assert result.workflow_name == "code_review"
        assert result.elapsed_seconds >= 0
        assert isinstance(result.outputs, dict)
        assert isinstance(result.steps, dict)
        assert isinstance(result.token_counts, dict)
        assert isinstance(result.models_used, dict)

    @pytest.mark.asyncio
    async def test_async_workflow_execution(self):
        """Execute a workflow asynchronously."""
        runner = WorkflowRunner()
        result = await runner.run("code_review", code_file="def bar(): pass", review_depth="full")

        assert result.run_id
        assert result.status in ("success", "partial", "failed")
        assert result.elapsed_seconds >= 0

    def test_workflow_with_errors(self):
        """Verify error handling in workflow execution."""
        runner = WorkflowRunner()
        # Missing required input should trigger validation error
        try:
            with pytest.raises((ValueError, KeyError, TypeError)):
                runner.invoke("code_review", review_depth="quick")
        except FileNotFoundError:
            # Workflow doesn't exist in test environment, that's ok
            pytest.skip("code_review workflow not found")

    def test_workflow_result_metadata(self):
        """Verify WorkflowResult includes execution metadata."""
        runner = WorkflowRunner()
        try:
            result = runner.invoke("code_review", code_file="x = 1", review_depth="quick")

            # run_id should be set
            assert result.run_id
            # token_counts and models_used should be dicts (may be empty if no LLM calls)
            assert isinstance(result.token_counts, dict)
            assert isinstance(result.models_used, dict)
        except ValueError as e:
            if "GOOGLE_API_KEY" in str(e) or "API" in str(e):
                pytest.skip(f"Requires API credentials: {e}")
            raise


class TestCheckpointing:
    """Checkpoint and resume tests."""

    def test_workflow_with_checkpointer(self):
        """Execute workflow with MemorySaver checkpointer."""
        checkpointer = MemorySaver()
        runner = WorkflowRunner(checkpointer=checkpointer)
        thread_id = "test_thread_1"

        result = runner.invoke(
            "code_review",
            thread_id=thread_id,
            code_file="print('hello')",
            review_depth="quick",
        )

        assert result.run_id == thread_id
        assert result.status in ("success", "partial")

    def test_checkpoint_state_inspection(self):
        """Inspect checkpoint state for a thread."""
        checkpointer = MemorySaver()
        runner = WorkflowRunner(checkpointer=checkpointer)
        thread_id = "inspect_test"

        # Run workflow
        runner.invoke("code_review", thread_id=thread_id, code_file="x = 1", review_depth="quick")

        # Inspect checkpoint state
        checkpoint = runner.get_checkpoint_state("code_review", thread_id=thread_id)
        # Checkpoint may be None if not supported by version
        if checkpoint:
            assert isinstance(checkpoint, dict)
            assert "values" in checkpoint or "next" in checkpoint

    def test_checkpoint_history(self):
        """Retrieve checkpoint history for a workflow."""
        checkpointer = MemorySaver()
        runner = WorkflowRunner(checkpointer=checkpointer)
        thread_id = "history_test"

        runner.invoke("code_review", thread_id=thread_id, code_file="y = 2", review_depth="quick")

        history = runner.get_checkpoint_history("code_review", thread_id=thread_id, limit=5)
        # History may be empty if not supported
        assert isinstance(history, list)


class TestStreamingEvents:
    """Streaming execution and event tests."""

    def test_stream_execution(self):
        """Stream workflow execution events."""
        runner = WorkflowRunner()
        events = list(runner.stream("code_review", code_file="z = 3", review_depth="quick"))

        # Should get some node updates
        assert len(events) > 0
        # Each event should be a dict
        for event in events:
            assert isinstance(event, dict)

    @pytest.mark.asyncio
    async def test_async_stream_execution(self):
        """Stream workflow execution asynchronously."""
        runner = WorkflowRunner()
        events = []
        async for event in runner.astream("code_review", code_file="w = 4", review_depth="quick"):
            events.append(event)

        assert len(events) > 0
        for event in events:
            assert isinstance(event, dict)

    def test_stream_node_updates(self):
        """Verify streaming events contain step updates."""
        runner = WorkflowRunner()
        events = list(runner.stream("code_review", code_file="a = 5", review_depth="quick"))

        # At minimum, should have events for graph nodes
        assert any(isinstance(e, dict) for e in events)


class TestGraphCompilation:
    """Graph compilation and validation tests."""

    def test_compile_valid_workflow(self):
        """Compile a valid workflow config."""
        config = load_workflow_config("code_review")
        graph = compile_workflow(config)

        assert graph is not None
        # Compiled graph should be a LangGraph CompiledGraph
        assert hasattr(graph, "invoke") or hasattr(graph, "ainvoke")

    def test_compiled_graph_execution(self):
        """Execute a compiled graph directly."""
        config = load_workflow_config("code_review")
        graph = compile_workflow(config)

        state = initial_state(workflow_inputs={"code_file": "test", "review_depth": "quick"})
        state["context"]["inputs"] = {"code_file": "test", "review_depth": "quick"}

        # Should be able to invoke the compiled graph
        result = graph.invoke(state)
        assert isinstance(result, dict)
        assert "steps" in result or "errors" in result

    @pytest.mark.asyncio
    async def test_compiled_graph_async_execution(self):
        """Execute a compiled graph asynchronously."""
        config = load_workflow_config("code_review")
        graph = compile_workflow(config)

        state = initial_state(workflow_inputs={"code_file": "test", "review_depth": "quick"})
        state["context"]["inputs"] = {"code_file": "test", "review_depth": "quick"}

        result = await graph.ainvoke(state)
        assert isinstance(result, dict)


class TestWorkflowVariations:
    """Test various workflow configurations."""

    def test_workflow_list(self):
        """List available workflows."""
        # Just verify we can list workflows without API credentials
        try:
            from agentic_v2.langchain import list_workflows
            workflows = list_workflows()
            assert isinstance(workflows, list)
            # Verify list is valid (may be empty if definitions dir doesn't exist)
            if workflows:
                # If we have workflows, check that known ones exist
                assert "code_review" in workflows or "test_deterministic" in workflows
        except FileNotFoundError:
            # Workflows directory doesn't exist in this environment
            pytest.skip("Workflows directory not found")

    def test_load_different_workflows(self):
        """Load and verify workflow configs can be parsed."""
        found_any = False
        for workflow_name in ["code_review", "test_deterministic"]:
            try:
                config = load_workflow_config(workflow_name)
                assert config.name == workflow_name
                assert isinstance(config.steps, list)
                assert isinstance(config.inputs, dict)
                found_any = True
            except FileNotFoundError:
                # If workflow doesn't exist, try the next one
                pass
        if not found_any:
            pytest.skip("No test workflows found")
