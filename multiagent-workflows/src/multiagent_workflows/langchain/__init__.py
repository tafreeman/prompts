"""LangChain Integration Module for Multi-Agent Workflows.

This module provides the integration layer between the multiagent-workflows
system and LangChain/LangGraph for real LLM-backed agent execution.

Submodules:
- tools: LangChain tool bindings from ToolRegistry
- chains: Chain/Runnable implementations for agents
- orchestrator: LangGraph workflow orchestration
- state: State schemas for workflow graphs
- callbacks: Logging and evaluation callbacks

Usage:
    from multiagent_workflows.langchain import (
        LangChainOrchestrator,
        create_langchain_tools,
        create_agent_chain,
        get_state_class,
        WorkflowCallbackHandler,
    )

    # Execute a workflow with LangChain
    orchestrator = LangChainOrchestrator(model_manager)
    result = await orchestrator.execute_workflow("full_stack_generation", inputs)
"""

# Callbacks - Logging and evaluation
from multiagent_workflows.langchain.callbacks import (
    EvaluationCallbackHandler,
    RunMetrics,
    WorkflowCallbackHandler,
    create_callbacks,
)

# Chains - Agent chain implementations
from multiagent_workflows.langchain.chains import (
    ROLE_CHAIN_CONFIGS,
    AgentChainFactory,
    ChainConfig,
    create_agent_chain,
)

# Orchestrator - Workflow execution
from multiagent_workflows.langchain.orchestrator import (
    LangChainOrchestrator,
    WorkflowConfig,
    WorkflowStepConfig,
    execute_workflow,
)

# State - Workflow state schemas
from multiagent_workflows.langchain.state import (
    ArchitectureEvolutionState,
    BaseWorkflowState,
    BugFixingState,
    CodeGradingState,
    FullStackState,
    RefactoringState,
    create_initial_state,
    get_state_class,
)

# Tools - Convert ToolRegistry to LangChain tools
from multiagent_workflows.langchain.tools import (
    create_langchain_tools,
    tool_definition_to_langchain,
    tool_registry_to_langchain,
)

__all__ = [
    # Tools
    "create_langchain_tools",
    "tool_definition_to_langchain",
    "tool_registry_to_langchain",
    # State
    "BaseWorkflowState",
    "FullStackState",
    "RefactoringState",
    "BugFixingState",
    "ArchitectureEvolutionState",
    "CodeGradingState",
    "get_state_class",
    "create_initial_state",
    # Chains
    "AgentChainFactory",
    "ChainConfig",
    "create_agent_chain",
    "ROLE_CHAIN_CONFIGS",
    # Orchestrator
    "LangChainOrchestrator",
    "WorkflowConfig",
    "WorkflowStepConfig",
    "execute_workflow",
    # Callbacks
    "WorkflowCallbackHandler",
    "EvaluationCallbackHandler",
    "RunMetrics",
    "create_callbacks",
]
