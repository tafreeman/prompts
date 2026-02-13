"""Integrations with external frameworks."""

from __future__ import annotations

from .base import (
    AgentAdapter,
    AgentResponse,
    CanonicalEvent,
    ToolAdapter,
    TraceAdapter,
    WorkflowAdapter,
)
from .langchain import (
    LANGCHAIN_AVAILABLE,
    AgenticAgent,
    AgenticChatModel,
    AgenticLangChainTool,
    AgenticRunnable,
    AgenticTool,
)
from .microsoft_agent_framework import (
    MICROSOFT_AGENT_FRAMEWORK_AVAILABLE,
    AgenticMicrosoftAgent,
)

__all__ = [
    "AgentAdapter",
    "AgentResponse",
    "CanonicalEvent",
    "ToolAdapter",
    "TraceAdapter",
    "WorkflowAdapter",
    "LANGCHAIN_AVAILABLE",
    "AgenticAgent",
    "AgenticChatModel",
    "AgenticLangChainTool",
    "AgenticRunnable",
    "AgenticTool",
    "MICROSOFT_AGENT_FRAMEWORK_AVAILABLE",
    "AgenticMicrosoftAgent",
]
