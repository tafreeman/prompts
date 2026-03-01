"""Concrete agent implementations backed by external LLM SDKs.

This subpackage provides two production-ready agent implementations:

:class:`ClaudeAgent`:
    A :class:`~agentic_v2.agents.base.BaseAgent` subclass that calls the
    Anthropic Messages API, translating between the project's internal
    OpenAI-style message format and the Anthropic SDK.

:class:`ClaudeSDKAgent`:
    A standalone wrapper around the ``claude-agent-sdk`` package that
    provides built-in file, web, and terminal tools without requiring
    :class:`~agentic_v2.agents.base.BaseAgent` infrastructure.

:func:`load_agents`:
    Loader that reads ``.md`` agent definition files (YAML frontmatter +
    system prompt body) and returns a dict of
    :class:`~claude_agent_sdk.AgentDefinition` instances.
"""

from __future__ import annotations

from .claude_agent import ClaudeAgent, SimpleTask, SimpleOutput
from .claude_sdk_agent import ClaudeSDKAgent, BUILTIN_TOOLS
from .agent_loader import load_agents, agents as AGENTS

__all__ = [
    "ClaudeAgent",
    "ClaudeSDKAgent",
    "SimpleTask",
    "SimpleOutput",
    "BUILTIN_TOOLS",
    "load_agents",
    "AGENTS",
]
