"""Microsoft Agent Framework integration adapters.

This module is dependency-optional: it can be imported without Microsoft
framework packages installed and still provide adapter contracts.
"""

from __future__ import annotations

import importlib.util
import inspect
from typing import Any

from .base import AgentAdapter, AgentResponse, CanonicalEvent, TraceAdapter

try:
    MICROSOFT_AGENT_FRAMEWORK_AVAILABLE = (
        importlib.util.find_spec("microsoft.agent_framework") is not None
    )
except ModuleNotFoundError:
    MICROSOFT_AGENT_FRAMEWORK_AVAILABLE = False


def _emit(
    trace_adapter: TraceAdapter | None,
    *,
    event_type: str,
    step_name: str,
    data: dict[str, Any] | None = None,
) -> None:
    if trace_adapter is None:
        return
    trace_adapter.emit(
        CanonicalEvent(
            type=event_type,
            step_name=step_name,
            data=data or {},
        )
    )


class AgenticMicrosoftAgent(AgentAdapter):
    """Normalize invocation and events for Microsoft-style agent objects."""

    def __init__(
        self,
        agent: Any,
        *,
        name: str | None = None,
        trace_adapter: TraceAdapter | None = None,
    ) -> None:
        self._agent = agent
        self._name = name or getattr(agent, "name", "microsoft_agent")
        self._trace_adapter = trace_adapter

    @staticmethod
    def canonicalize_event(payload: dict[str, Any] | None) -> CanonicalEvent:
        """Convert a framework event payload into a canonical event."""
        payload = payload or {}
        event_type = payload.get("type") or payload.get("event_type") or "unknown"
        step_name = payload.get("step_name") or payload.get("step") or ""
        data = payload.get("data")

        if isinstance(data, dict):
            normalized_data = data
        else:
            normalized_data = {
                key: value
                for key, value in payload.items()
                if key not in {"type", "event_type", "step_name", "step", "timestamp"}
            }

        return CanonicalEvent(
            type=str(event_type),
            step_name=str(step_name),
            data=normalized_data,
        )

    async def ainvoke(
        self, prompt: Any, context: dict[str, Any] | None = None
    ) -> AgentResponse:
        _emit(
            self._trace_adapter,
            event_type="agent.invoke.start",
            step_name=self._name,
            data={"has_context": bool(context)},
        )
        result = await self._invoke_underlying(prompt, context=context)

        if isinstance(result, AgentResponse):
            response = result
        elif isinstance(result, dict):
            content = str(
                result.get("content")
                or result.get("output")
                or result.get("response")
                or ""
            )
            metadata = {
                key: value
                for key, value in result.items()
                if key not in {"content", "output", "response"}
            }
            response = AgentResponse(content=content, metadata=metadata, raw=result)
        else:
            response = AgentResponse(content=str(result), metadata={}, raw=result)

        _emit(
            self._trace_adapter,
            event_type="agent.invoke.complete",
            step_name=self._name,
            data={"content_length": len(response.content)},
        )
        return response

    async def _invoke_underlying(
        self, prompt: Any, context: dict[str, Any] | None = None
    ) -> Any:
        if hasattr(self._agent, "run"):
            call_result = self._agent.run(prompt, context=context)
        elif hasattr(self._agent, "invoke"):
            call_result = self._agent.invoke(prompt, context=context)
        elif callable(self._agent):
            call_result = self._agent(prompt, context=context)
        else:
            raise TypeError(
                "Unsupported Microsoft agent object; expected run(), invoke(), or callable()."
            )

        if inspect.isawaitable(call_result):
            return await call_result
        return call_result


__all__ = [
    "MICROSOFT_AGENT_FRAMEWORK_AVAILABLE",
    "AgenticMicrosoftAgent",
]
