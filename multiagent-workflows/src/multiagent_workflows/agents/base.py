"""
DEPRECATED: This module is part of the legacy multiagent-workflows package.
It has been superseded by the `agentic-workflows-v2` package.
Please migrate to `agentic_v2.agents.base` (implied).
"""

"""
Base Agent - Re-export from core for convenience.
"""

from multiagent_workflows.core.agent_base import (
    AgentBase,
    AgentConfig,
    AgentResult,
    SimpleAgent,
)

# Alias for backward compatibility
BaseAgent = AgentBase

__all__ = ["AgentBase", "BaseAgent", "AgentConfig", "AgentResult", "SimpleAgent"]
