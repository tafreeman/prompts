"""
Base Agent - Re-export from core for convenience.
"""

from multiagent_workflows.core.agent_base import AgentBase, AgentConfig, AgentResult, SimpleAgent

# Alias for backward compatibility
BaseAgent = AgentBase

__all__ = ["AgentBase", "BaseAgent", "AgentConfig", "AgentResult", "SimpleAgent"]
