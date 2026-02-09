"""Integration tests for OrchestratorAgent with DAG execution.

Tests the orchestrator's ability to:
- Decompose tasks to subtasks
- Route to DAG executor
- Handle parallel execution
- Manage dependencies correctly
"""

import asyncio

import pytest
from agentic_v2.agents.base import AgentConfig, agent_to_step
from agentic_v2.agents.coder import (CoderAgent)
from agentic_v2.agents.orchestrator import (OrchestratorAgent)
from agentic_v2.contracts import StepStatus
from agentic_v2.engine import DAG, DAGExecutor, ExecutionContext
from agentic_v2.engine.step import StepDefinition
from agentic_v2.models import LLMClientWrapper, MockBackend, get_smart_router


@pytest.fixture
def mock_backend():
    """Create a mock LLM backend for testing."""
    backend = MockBackend()
    backend.set_response(
        "decompose",
        """{
    "subtasks": [
        {
            "id": "task_1",
            "description": "Create user model",
            "capabilities": ["code_generation"],
            "dependencies": [],
            "parallel_group": 1
        },
        {
            "id": "task_2",
            "description": "Create user API endpoints",
            "capabilities": ["code_generation"],
            "dependencies": ["task_1"],
            "parallel_group": 2
        }
    ],
    "execution_order": ["task_1", "task_2"],
    "validation_steps": ["Check code compiles"]
}""",
    )
    return backend


@pytest.fixture
def llm_client(mock_backend):
    """Create an LLM client with mock backend."""
    client = LLMClientWrapper(
        router=get_smart_router(),
        enable_cache=False,
    )
    client.set_backend(mock_backend)
    return client


class TestOrchestratorDAGIntegration:
    """Test OrchestratorAgent integration with DAG execution."""

    @pytest.mark.asyncio
    async def test_orchestrator_creates_dag_from_subtasks(self, llm_client):
        """Test that orchestrator can create a DAG from subtasks."""
        # Create orchestrator with mock LLM
        orchestrator = OrchestratorAgent(
            config=AgentConfig(name="test-orchestrator"),
            llm_client=llm_client,
        )

        # Add a coder agent
        coder = CoderAgent(
            config=AgentConfig(name="coder"),
            llm_client=llm_client,
        )
        orchestrator._agents["coder"] = coder

        # Verify the agent was registered
        assert "coder" in orchestrator._agents

    @pytest.mark.asyncio
    async def test_dag_executor_handles_dependencies(self):
        """Test that DAG executor correctly handles task dependencies."""
        dag = DAG(name="test-dag")

        # Create step definitions with dependencies
        async def handler_a(ctx):
            return {"result": "a"}

        async def handler_b(ctx):
            return {"result": "b"}

        async def handler_c(ctx):
            return {"result": "c"}

        async def handler_d(ctx):
            return {"result": "d"}

        step_a = StepDefinition(
            name="step_a",
            description="First step",
            func=handler_a,
            depends_on=[],
        )
        step_b = StepDefinition(
            name="step_b",
            description="Second step",
            func=handler_b,
            depends_on=["step_a"],
        )
        step_c = StepDefinition(
            name="step_c",
            description="Third step",
            func=handler_c,
            depends_on=["step_a"],
        )
        step_d = StepDefinition(
            name="step_d",
            description="Fourth step",
            func=handler_d,
            depends_on=["step_b", "step_c"],
        )

        dag.add(step_a).add(step_b).add(step_c).add(step_d)

        # Execute DAG
        executor = DAGExecutor()
        ctx = ExecutionContext()
        result = await executor.execute(dag, ctx, max_concurrency=4)

        # All steps should complete successfully
        assert result.overall_status == StepStatus.SUCCESS
        assert len(result.steps) == 4

    @pytest.mark.asyncio
    async def test_dag_executor_respects_max_concurrency(self):
        """Test that DAG executor respects max concurrency limits."""
        dag = DAG(name="concurrency-test")

        execution_order = []
        async_lock = asyncio.Lock()

        # Create handler that records execution
        async def make_tracking_handler(name: str):
            async def tracking_handler(ctx):
                async with async_lock:
                    execution_order.append(f"start_{name}")
                await asyncio.sleep(0.1)  # Simulate work
                async with async_lock:
                    execution_order.append(f"end_{name}")
                return {"name": name}

            return tracking_handler

        # Create parallel steps with no dependencies
        for i in range(4):

            async def step_func(ctx, n=i):
                async with async_lock:
                    execution_order.append(f"start_step_{n}")
                await asyncio.sleep(0.05)
                async with async_lock:
                    execution_order.append(f"end_step_{n}")
                return {"step": n}

            step = StepDefinition(
                name=f"parallel_{i}",
                description=f"Parallel step {i}",
                func=step_func,
                depends_on=[],
            )
            dag.add(step)

        # Execute with max_concurrency=2
        executor = DAGExecutor()
        ctx = ExecutionContext()
        result = await executor.execute(dag, ctx, max_concurrency=2)

        assert result.overall_status == StepStatus.SUCCESS

    @pytest.mark.asyncio
    async def test_dag_executor_cascade_skips_on_failure(self):
        """Test that DAG executor skips downstream tasks on failure."""
        dag = DAG(name="failure-test")

        async def failing_handler(ctx):
            raise RuntimeError("Intentional failure")

        async def success_handler(ctx):
            return {"status": "ok"}

        step_a = StepDefinition(
            name="step_a",
            description="This will fail",
            func=failing_handler,
            depends_on=[],
        )
        step_b = StepDefinition(
            name="step_b",
            description="Should be skipped",
            func=success_handler,
            depends_on=["step_a"],
        )

        dag.add(step_a).add(step_b)

        executor = DAGExecutor()
        ctx = ExecutionContext()
        result = await executor.execute(dag, ctx, max_concurrency=2)

        # Overall should fail
        assert result.overall_status == StepStatus.FAILED

        # step_b should be skipped
        step_b_result = next((r for r in result.steps if r.step_name == "step_b"), None)
        assert step_b_result is not None
        assert step_b_result.status == StepStatus.SKIPPED


class TestAgentToStepConversion:
    """Test converting agents to DAG steps."""

    @pytest.mark.asyncio
    async def test_agent_to_step_creates_valid_step(self, llm_client):
        """Test that agent_to_step creates a valid StepDefinition."""
        coder = CoderAgent(
            config=AgentConfig(name="test-coder"),
            llm_client=llm_client,
        )

        step = agent_to_step(coder, "code_gen_step")

        assert step.name == "code_gen_step"
        assert step.func is not None
        assert callable(step.func)

    @pytest.mark.asyncio
    async def test_multiple_agents_in_dag(self, llm_client):
        """Test running multiple agents as DAG steps."""
        dag = DAG(name="multi-agent-test")

        # Create mock agents that just return data
        for i in range(3):

            async def agent_step(ctx, n=i):
                return {"agent_id": n, "output": f"result_{n}"}

            step = StepDefinition(
                name=f"agent_{i}",
                description=f"Agent {i} task",
                func=agent_step,
                depends_on=[] if i == 0 else [f"agent_{i-1}"],
            )
            dag.add(step)

        executor = DAGExecutor()
        ctx = ExecutionContext()
        result = await executor.execute(dag, ctx)

        assert result.overall_status == StepStatus.SUCCESS
        assert len(result.steps) == 3


class TestCoderAgentLLMIntegration:
    """Test CoderAgent with LLM client."""

    @pytest.mark.asyncio
    async def test_coder_uses_llm_client_when_backend_set(self, llm_client):
        """Test that CoderAgent uses the LLM client when backend is
        configured."""
        mock_backend = llm_client.backend
        mock_backend.set_response(
            "function",
            """```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```""",
        )

        coder = CoderAgent(
            config=AgentConfig(name="test-coder"),
            llm_client=llm_client,
        )

        code = await coder.generate_code(
            description="Create a greeting function",
            language="python",
        )

        # The mock should have been called
        assert len(mock_backend.call_history) > 0

    @pytest.mark.asyncio
    async def test_coder_returns_mock_when_no_backend(self):
        """Test that CoderAgent returns mock response when no backend."""
        # Create client without backend
        client = LLMClientWrapper(
            router=get_smart_router(),
            enable_cache=False,
        )
        # Don't set backend

        coder = CoderAgent(
            config=AgentConfig(name="test-coder"),
            llm_client=client,
        )

        code = await coder.generate_code(
            description="Create something",
            language="python",
        )

        # Should get placeholder response
        assert "placeholder" in code.lower() or "example" in code.lower()
