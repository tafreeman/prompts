"""Tests for Agents.

Tests agent functionality including execution and logging.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest


class TestAgentBase:
    """Test base agent functionality."""

    def test_agent_config(self):
        """Test AgentConfig creation."""
        from multiagent_workflows.core.agent_base import AgentConfig

        config = AgentConfig(
            name="TestAgent",
            role="Test role",
            model_id="mock:test",
            system_prompt="You are a test agent.",
        )

        assert config.name == "TestAgent"
        assert config.role == "Test role"
        assert config.model_id == "mock:test"

    def test_simple_agent_creation(self, mock_model_manager, logger):
        """Test SimpleAgent creation."""
        from multiagent_workflows.core.agent_base import AgentConfig, SimpleAgent

        config = AgentConfig(
            name="TestAgent",
            role="Test role",
            model_id="mock:test",
            system_prompt="Test prompt",
        )

        agent = SimpleAgent(
            config=config,
            model_manager=mock_model_manager,
            prompt_template="Task: {task}\nContext: {context}",
            logger=logger,
        )

        assert agent.name == "TestAgent"
        assert agent.role == "Test role"


class TestAgentExecution:
    """Test agent execution."""

    @pytest.mark.asyncio
    async def test_simple_agent_execute(self, mock_model_manager, logger):
        """Test SimpleAgent execution."""
        from multiagent_workflows.core.agent_base import AgentConfig, SimpleAgent

        config = AgentConfig(
            name="TestAgent",
            role="Test role",
            model_id="mock:test",
            system_prompt="Test prompt",
        )

        agent = SimpleAgent(
            config=config,
            model_manager=mock_model_manager,
            prompt_template="Task: {task}\nContext: {context}",
            output_key="result",
            logger=logger,
        )

        result = await agent.execute(
            task={"description": "Test task"},
            context={"step_id": "test-step"},
        )

        assert result.success is True
        assert "result" in result.output

    @pytest.mark.asyncio
    async def test_agent_with_tools(self, mock_model_manager, tool_registry, logger):
        """Test agent with tool invocation."""
        from multiagent_workflows.core.agent_base import AgentConfig, SimpleAgent

        config = AgentConfig(
            name="ToolAgent",
            role="Test with tools",
            model_id="mock:test",
            system_prompt="Test",
            tools=["test_tool"],
        )

        agent = SimpleAgent(
            config=config,
            model_manager=mock_model_manager,
            tool_registry=tool_registry,
            prompt_template="{task}",
            logger=logger,
        )

        # Test tool usage
        result = await agent.use_tool("test_tool", {"input": "hello"})
        assert result == "processed: hello"


class TestArchitectAgent:
    """Test ArchitectAgent."""

    @pytest.mark.asyncio
    async def test_architect_agent(self, mock_model_manager, logger):
        """Test ArchitectAgent execution."""
        from multiagent_workflows.agents.architect_agent import ArchitectAgent
        from multiagent_workflows.core.agent_base import AgentConfig

        # Mock response with architecture
        mock_model_manager.generate = AsyncMock(
            return_value=MagicMock(
                text='{"tech_stack": {"frontend": {"framework": "React"}}, "api_strategy": {"type": "REST"}}',
                tokens_used=50,
            )
        )

        config = AgentConfig(
            name="Architect",
            role="Design architecture",
            model_id="mock:test",
            system_prompt="",
        )

        agent = ArchitectAgent(
            config=config,
            model_manager=mock_model_manager,
            logger=logger,
        )

        result = await agent.execute(
            task={"requirements": "Build a web app"},
            context={"step_id": "arch-step"},
        )

        assert result.success is True
        assert "architecture" in result.output
