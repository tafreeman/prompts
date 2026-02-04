"""Agents module - Specialized AI agents for different tasks.

Exports:
- Base: BaseAgent, AgentConfig, AgentState, AgentEvent
- Capabilities: Capability, CapabilitySet, CapabilityType
- Agents: CoderAgent, ReviewerAgent, OrchestratorAgent, ArchitectAgent, TestAgent
- Utilities: agent_to_step, get_agent_capabilities
"""

from .architect import (
    ArchitectAgent,
    ArchitectureInput,
    ArchitectureOutput,
    TechStackChoice,
)
from .base import (
    AgentConfig,
    AgentEvent,
    AgentState,
    BaseAgent,
    ConversationMemory,
    ConversationMessage,
    agent_to_step,
)
from .capabilities import (
    Capability,
    CapabilityMixin,
    CapabilitySet,
    CapabilityType,
    CodeGenerationMixin,
    CodeReviewMixin,
    OrchestrationMixin,
    TestGenerationMixin,
    get_agent_capabilities,
    requires_capabilities,
)
from .coder import CoderAgent
from .orchestrator import (
    OrchestratorAgent,
    OrchestratorInput,
    OrchestratorOutput,
    SubTask,
)
from .reviewer import ReviewerAgent
from .test_agent import (
    TestAgent,
    TestFile,
    TestGenerationInput,
    TestGenerationOutput,
    TestType,
)

__all__ = [
    # Base
    "AgentConfig",
    "AgentEvent",
    "AgentState",
    "BaseAgent",
    "ConversationMemory",
    "ConversationMessage",
    "agent_to_step",
    # Capabilities
    "Capability",
    "CapabilityMixin",
    "CapabilitySet",
    "CapabilityType",
    "CodeGenerationMixin",
    "CodeReviewMixin",
    "OrchestrationMixin",
    "TestGenerationMixin",
    "get_agent_capabilities",
    "requires_capabilities",
    # Agents
    "CoderAgent",
    "ReviewerAgent",
    "OrchestratorAgent",
    "OrchestratorInput",
    "OrchestratorOutput",
    "SubTask",
    # Architect Agent
    "ArchitectAgent",
    "ArchitectureInput",
    "ArchitectureOutput",
    "TechStackChoice",
    # Test Agent
    "TestAgent",
    "TestGenerationInput",
    "TestGenerationOutput",
    "TestFile",
    "TestType",
]
