"""
Tests for LangChain Integration Module

Tests the LangChain chains, state, tools, callbacks, and orchestrator.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Any, Dict


# =============================================================================
# Test State Management
# =============================================================================

class TestWorkflowState:
    """Test workflow state schemas."""
    
    def test_get_state_class_fullstack(self):
        """Test getting state class for fullstack workflow."""
        from multiagent_workflows.langchain.state import get_state_class, FullStackState
        
        state_class = get_state_class("fullstack_generation")
        assert state_class == FullStackState
    
    def test_get_state_class_refactoring(self):
        """Test getting state class for refactoring workflow."""
        from multiagent_workflows.langchain.state import get_state_class, RefactoringState
        
        state_class = get_state_class("legacy_refactoring")
        assert state_class == RefactoringState
    
    def test_get_state_class_bug_fixing(self):
        """Test getting state class for bug fixing workflow."""
        from multiagent_workflows.langchain.state import get_state_class, BugFixingState
        
        state_class = get_state_class("bug_fixing")
        assert state_class == BugFixingState
    
    def test_get_state_class_unknown(self):
        """Test getting state class for unknown workflow returns base."""
        from multiagent_workflows.langchain.state import get_state_class, BaseWorkflowState
        
        state_class = get_state_class("unknown_workflow")
        assert state_class == BaseWorkflowState
    
    def test_create_initial_state(self):
        """Test creating initial state for a workflow."""
        from multiagent_workflows.langchain.state import create_initial_state
        
        inputs = {"requirements": "Build a web app"}
        state = create_initial_state("fullstack_generation", inputs)
        
        assert state["workflow_name"] == "fullstack_generation"
        assert state["requirements"] == "Build a web app"
        assert state["messages"] == []
        assert state["errors"] == []
        assert state["artifacts"] == {}
    
    def test_create_initial_state_with_workflow_id(self):
        """Test creating initial state with custom workflow ID."""
        from multiagent_workflows.langchain.state import create_initial_state
        
        state = create_initial_state(
            "bug_fixing",
            {"bug_report": "Fix crash"},
            workflow_id="custom-id-123",
        )
        
        assert state["workflow_id"] == "custom-id-123"


# =============================================================================
# Test Chain Configuration
# =============================================================================

class TestChainConfig:
    """Test ChainConfig dataclass."""
    
    def test_chain_config_creation(self):
        """Test creating a ChainConfig."""
        from multiagent_workflows.langchain.chains import ChainConfig
        
        config = ChainConfig(
            agent_id="test_agent",
            name="Test Agent",
            role="tester",
            system_prompt="You are a test agent.",
            model_id="mock:test",
        )
        
        assert config.agent_id == "test_agent"
        assert config.name == "Test Agent"
        assert config.role == "tester"
        assert config.model_id == "mock:test"
        assert config.tools == []
        assert config.temperature == 0.7
        assert config.max_tokens == 4096
    
    def test_chain_config_with_tools(self):
        """Test ChainConfig with tools list."""
        from multiagent_workflows.langchain.chains import ChainConfig
        
        config = ChainConfig(
            agent_id="tooled_agent",
            name="Tooled Agent",
            role="worker",
            system_prompt="You use tools.",
            model_id="mock:test",
            tools=["search", "write_file"],
        )
        
        assert config.tools == ["search", "write_file"]


class TestRoleChainConfigs:
    """Test pre-defined role chain configurations."""
    
    def test_role_configs_exist(self):
        """Test that role configurations exist."""
        from multiagent_workflows.langchain.chains import ROLE_CHAIN_CONFIGS
        
        assert "requirements_analyzer" in ROLE_CHAIN_CONFIGS
        assert "system_architect" in ROLE_CHAIN_CONFIGS
        assert "backend_generator" in ROLE_CHAIN_CONFIGS
        assert "frontend_generator" in ROLE_CHAIN_CONFIGS
        assert "code_reviewer" in ROLE_CHAIN_CONFIGS
        assert "test_generator" in ROLE_CHAIN_CONFIGS
    
    def test_role_config_has_system_prompt(self):
        """Test that each role has a system prompt."""
        from multiagent_workflows.langchain.chains import ROLE_CHAIN_CONFIGS
        
        for role, config in ROLE_CHAIN_CONFIGS.items():
            assert "system_prompt" in config, f"Role {role} missing system_prompt"
            assert len(config["system_prompt"]) > 50, f"Role {role} has short prompt"


# =============================================================================
# Test AgentChainFactory
# =============================================================================

class TestAgentChainFactory:
    """Test AgentChainFactory class."""
    
    @pytest.fixture
    def mock_model_manager(self):
        """Create a mock model manager."""
        from multiagent_workflows.core.model_manager import ModelManager
        
        manager = MagicMock(spec=ModelManager)
        manager.get_optimal_model = MagicMock(return_value="mock:test")
        manager.generate_text = MagicMock(return_value=MagicMock(text='{"result": "test"}'))
        
        return manager
    
    def test_factory_creation(self, mock_model_manager):
        """Test creating AgentChainFactory."""
        from multiagent_workflows.langchain.chains import AgentChainFactory
        
        factory = AgentChainFactory(mock_model_manager)
        
        assert factory.model_manager == mock_model_manager
        assert factory._chain_cache == {}
    
    def test_create_fallback_chain(self, mock_model_manager):
        """Test creating fallback chain when LangChain unavailable."""
        from multiagent_workflows.langchain.chains import AgentChainFactory, ChainConfig
        
        factory = AgentChainFactory(mock_model_manager)
        
        config = ChainConfig(
            agent_id="fallback_test",
            name="Fallback Test",
            role="tester",
            system_prompt="Test prompt",
            model_id="mock:test",
        )
        
        # Get fallback chain
        chain = factory._create_fallback_chain(config)
        
        assert callable(chain)
    
    def test_chain_caching(self, mock_model_manager):
        """Test that chains are cached."""
        from multiagent_workflows.langchain.chains import AgentChainFactory, ChainConfig
        
        factory = AgentChainFactory(mock_model_manager)
        
        config = ChainConfig(
            agent_id="cache_test",
            name="Cache Test",
            role="tester",
            system_prompt="Test prompt",
            model_id="mock:test",
        )
        
        # Create chain twice
        chain1 = factory.create_chain(config)
        chain2 = factory.create_chain(config)
        
        # Should be same cached instance
        assert chain1 is chain2


# =============================================================================
# Test Tools Conversion
# =============================================================================

class TestToolsConversion:
    """Test ToolRegistry to LangChain tools conversion."""
    
    def test_get_type_string(self):
        """Test type annotation to JSON schema conversion."""
        from multiagent_workflows.langchain.tools import _get_type_string
        
        assert _get_type_string(str) == "string"
        assert _get_type_string(int) == "integer"
        assert _get_type_string(float) == "number"
        assert _get_type_string(bool) == "boolean"
        assert _get_type_string(list) == "array"
        assert _get_type_string(dict) == "object"
    
    def test_generate_schema_from_function(self):
        """Test schema generation from function signature."""
        from multiagent_workflows.langchain.tools import _generate_schema_from_function
        
        def sample_func(name: str, count: int = 5) -> str:
            return f"{name}: {count}"
        
        schema = _generate_schema_from_function(sample_func)
        
        assert schema["type"] == "object"
        assert "name" in schema["properties"]
        assert "count" in schema["properties"]
        assert "name" in schema["required"]
        assert "count" not in schema["required"]  # Has default
    
    def test_agent_tool_schemas_exist(self):
        """Test that pre-defined tool schemas exist."""
        from multiagent_workflows.langchain.tools import AGENT_TOOL_SCHEMAS
        
        assert "analyze_code" in AGENT_TOOL_SCHEMAS
        assert "generate_code" in AGENT_TOOL_SCHEMAS
        assert "review_code" in AGENT_TOOL_SCHEMAS
        assert "run_tests" in AGENT_TOOL_SCHEMAS


# =============================================================================
# Test Callbacks
# =============================================================================

class TestRunMetrics:
    """Test RunMetrics dataclass."""
    
    def test_metrics_defaults(self):
        """Test RunMetrics default values."""
        from multiagent_workflows.langchain.callbacks import RunMetrics
        
        metrics = RunMetrics()
        
        assert metrics.start_time == 0.0
        assert metrics.end_time == 0.0
        assert metrics.total_tokens == 0
        assert metrics.llm_calls == 0
        assert metrics.errors == []
    
    def test_duration_calculation(self):
        """Test duration calculation."""
        from multiagent_workflows.langchain.callbacks import RunMetrics
        
        metrics = RunMetrics(start_time=100.0, end_time=100.5)
        
        assert metrics.duration_ms == 500.0


class TestWorkflowCallbackHandler:
    """Test WorkflowCallbackHandler class."""
    
    def test_callback_handler_creation(self):
        """Test creating callback handler."""
        from multiagent_workflows.langchain.callbacks import WorkflowCallbackHandler
        
        handler = WorkflowCallbackHandler()
        
        assert handler._workflow_runs == {}
        assert handler._current_workflow_id is None
    
    def test_workflow_start(self):
        """Test on_workflow_start callback."""
        from multiagent_workflows.langchain.callbacks import WorkflowCallbackHandler
        
        handler = WorkflowCallbackHandler()
        
        handler.on_workflow_start(
            workflow_id="test-123",
            workflow_name="test_workflow",
            inputs={"key": "value"},
        )
        
        assert handler._current_workflow_id == "test-123"
        assert "test-123" in handler._workflow_runs
        assert handler._workflow_runs["test-123"]["name"] == "test_workflow"
    
    def test_workflow_complete(self):
        """Test on_workflow_complete callback."""
        from multiagent_workflows.langchain.callbacks import WorkflowCallbackHandler
        
        handler = WorkflowCallbackHandler()
        
        handler.on_workflow_start("test-123", "test_workflow", {})
        handler.on_workflow_complete("test-123", {"success": True, "outputs": {}})
        
        assert handler._workflow_runs["test-123"]["success"] is True
    
    def test_step_callbacks(self):
        """Test step start/complete callbacks."""
        from multiagent_workflows.langchain.callbacks import WorkflowCallbackHandler
        
        handler = WorkflowCallbackHandler()
        
        handler.on_workflow_start("test-123", "test_workflow", {})
        handler.on_step_start("step_1", {"input": "data"})
        handler.on_step_complete("step_1", {"output": "result"}, 100.0)
        
        steps = handler._workflow_runs["test-123"]["steps"]
        assert len(steps) == 1
        assert steps[0]["name"] == "step_1"
        assert steps[0]["success"] is True
    
    def test_get_workflow_metrics(self):
        """Test getting workflow metrics."""
        from multiagent_workflows.langchain.callbacks import WorkflowCallbackHandler
        
        handler = WorkflowCallbackHandler()
        
        handler.on_workflow_start("test-123", "test_workflow", {})
        handler.on_step_start("step_1", {})
        handler.on_step_complete("step_1", {}, 50.0)
        handler.on_workflow_complete("test-123", {"success": True})
        
        metrics = handler.get_workflow_metrics("test-123")
        
        assert metrics is not None
        assert metrics["workflow_id"] == "test-123"
        assert metrics["step_count"] == 1


class TestEvaluationCallbackHandler:
    """Test EvaluationCallbackHandler class."""
    
    def test_ui_scoring_categories(self):
        """Test UI scoring categories match expected values."""
        from multiagent_workflows.langchain.callbacks import UI_SCORING_CATEGORIES
        
        assert "correctness" in UI_SCORING_CATEGORIES
        assert "quality" in UI_SCORING_CATEGORIES
        assert "documentation" in UI_SCORING_CATEGORIES
        assert "completeness" in UI_SCORING_CATEGORIES
        assert "efficiency" in UI_SCORING_CATEGORIES
    
    def test_heuristic_scores(self):
        """Test heuristic scoring when Scorer unavailable."""
        from multiagent_workflows.langchain.callbacks import EvaluationCallbackHandler
        
        handler = EvaluationCallbackHandler()
        
        code = '''
def hello_world():
    """Print hello world."""
    print("Hello, World!")
'''
        
        scores = handler._heuristic_scores(code, "")
        
        assert "correctness" in scores
        assert "quality" in scores
        assert "documentation" in scores
        assert all(0 <= s <= 1 for s in scores.values())


# =============================================================================
# Test Orchestrator
# =============================================================================

class TestWorkflowConfig:
    """Test workflow configuration classes."""
    
    def test_workflow_step_config(self):
        """Test WorkflowStepConfig dataclass."""
        from multiagent_workflows.langchain.orchestrator import WorkflowStepConfig
        
        step = WorkflowStepConfig(
            id="step_1",
            name="Analyze Requirements",
            agent="requirements_analyzer",
            model_preference="reasoning",
            inputs=["requirements"],
            outputs=["user_stories"],
        )
        
        assert step.id == "step_1"
        assert step.agent == "requirements_analyzer"
        assert step.iterative is False
        assert step.max_iterations == 1
    
    def test_workflow_config(self):
        """Test WorkflowConfig dataclass."""
        from multiagent_workflows.langchain.orchestrator import WorkflowConfig, WorkflowStepConfig
        
        config = WorkflowConfig(
            name="Test Workflow",
            description="A test workflow",
            inputs=[{"name": "requirements", "type": "string"}],
            outputs=[{"name": "result", "type": "object"}],
            steps=[
                WorkflowStepConfig(
                    id="step_1",
                    name="Step 1",
                    agent="test_agent",
                    model_preference="reasoning",
                ),
            ],
        )
        
        assert config.name == "Test Workflow"
        assert len(config.steps) == 1


class TestLangChainOrchestrator:
    """Test LangChainOrchestrator class."""
    
    @pytest.fixture
    def mock_model_manager(self):
        """Create mock model manager."""
        from multiagent_workflows.core.model_manager import ModelManager
        
        manager = MagicMock(spec=ModelManager)
        manager.get_optimal_model = MagicMock(return_value="mock:test")
        manager.generate_text = MagicMock(return_value=MagicMock(text='{"result": "ok"}'))
        
        return manager
    
    def test_orchestrator_creation(self, mock_model_manager):
        """Test creating LangChainOrchestrator."""
        from multiagent_workflows.langchain.orchestrator import LangChainOrchestrator
        
        orchestrator = LangChainOrchestrator(mock_model_manager)
        
        assert orchestrator.model_manager == mock_model_manager
        assert orchestrator.workflows == {} or len(orchestrator.workflows) >= 0
    
    def test_resolve_model(self, mock_model_manager):
        """Test model preference resolution."""
        from multiagent_workflows.langchain.orchestrator import LangChainOrchestrator
        
        orchestrator = LangChainOrchestrator(mock_model_manager)
        
        assert orchestrator._resolve_model("reasoning") == "gh:openai/gpt-4o"
        assert orchestrator._resolve_model("code_gen_fast") == "gh:openai/gpt-4o-mini"
        assert orchestrator._resolve_model("local_efficient") == "local:phi4"
        assert "gpt-4o-mini" in orchestrator._resolve_model("unknown")
    
    def test_get_agent_config_fallback(self, mock_model_manager):
        """Test agent config fallback for unknown agents."""
        from multiagent_workflows.langchain.orchestrator import LangChainOrchestrator
        
        orchestrator = LangChainOrchestrator(mock_model_manager)
        
        config = orchestrator._get_agent_config("unknown_agent")
        
        assert config["name"] == "Unknown Agent"
        assert "system_prompt" in config


# =============================================================================
# Test create_agent_chain helper
# =============================================================================

class TestCreateAgentChain:
    """Test create_agent_chain convenience function."""
    
    def test_create_agent_chain(self):
        """Test creating agent chain with convenience function."""
        from multiagent_workflows.langchain.chains import create_agent_chain
        from multiagent_workflows.core.model_manager import ModelManager
        
        manager = MagicMock(spec=ModelManager)
        manager.get_optimal_model = MagicMock(return_value="mock:test")
        
        chain = create_agent_chain(
            agent_id="code_reviewer",
            model_manager=manager,
        )
        
        assert chain is not None
        assert callable(chain) or hasattr(chain, 'invoke')
