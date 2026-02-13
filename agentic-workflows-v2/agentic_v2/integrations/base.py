"""Base adapter contracts for external framework integrations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from ..contracts import WorkflowResult
from ..tools.base import ToolResult


@dataclass(frozen=True)
class AgentResponse:
    """Canonical response envelope for adapter-level agent calls."""

    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    raw: Any = None


@dataclass(frozen=True)
class CanonicalEvent:
    """Unified event payload emitted by adapter implementations."""

    type: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    step_name: str = ""
    data: dict[str, Any] = field(default_factory=dict)

    def to_json_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""
        return {
            "type": self.type,
            "timestamp": self.timestamp.isoformat(),
            "step_name": self.step_name,
            "data": self.data,
        }

    @classmethod
    def from_json_dict(cls, payload: dict[str, Any]) -> "CanonicalEvent":
        """Create an event from a JSON-serialized dictionary."""
        raw_ts = payload.get("timestamp")
        if isinstance(raw_ts, datetime):
            timestamp = raw_ts
        else:
            timestamp = datetime.fromisoformat(str(raw_ts))
        return cls(
            type=str(payload.get("type", "")),
            timestamp=timestamp,
            step_name=str(payload.get("step_name", "")),
            data=dict(payload.get("data") or {}),
        )


class AgentAdapter(ABC):
    """Contract for model/agent adapter entry points.

    Concrete implementations should provide async invocation behavior via
    ``ainvoke``. The ``invoke`` helper is provided for a uniform call shape.
    """

    @abstractmethod
    async def ainvoke(
        self, prompt: Any, context: dict[str, Any] | None = None
    ) -> AgentResponse | Any:
        """Execute an agent/model invocation."""

    async def invoke(
        self, prompt: Any, context: dict[str, Any] | None = None
    ) -> AgentResponse | Any:
        """Alias for ``ainvoke`` with the documented adapter shape."""
        return await self.ainvoke(prompt, context=context)


class ToolAdapter(ABC):
    """Contract for tool adapters."""

    @abstractmethod
    async def execute(self, tool_name: str, args: dict[str, Any]) -> ToolResult:
        """Execute a named tool with a normalized argument payload."""


class WorkflowAdapter(ABC):
    """Contract for workflow execution adapters."""

    @abstractmethod
    async def run(
        self, workflow_def: Any, inputs: dict[str, Any]
    ) -> WorkflowResult | Any:
        """Run a workflow and return its normalized result."""


class TraceAdapter(ABC):
    """Contract for trace/event sinks."""

    @abstractmethod
    def emit(self, event: CanonicalEvent) -> None:
        """Emit a canonical adapter event."""


__all__ = [
    "AgentAdapter",
    "AgentResponse",
    "CanonicalEvent",
    "ToolAdapter",
    "TraceAdapter",
    "WorkflowAdapter",
]
