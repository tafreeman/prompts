"""LangChain integration for agentic-workflows-v2.

Provides adapters so V2 components can be used from LangChain surfaces while
also conforming to the framework-neutral integration contracts.
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Optional

from .base import AgentAdapter, CanonicalEvent, ToolAdapter, TraceAdapter
from ..models.client import LLMClientWrapper, get_client
from ..models.router import ModelTier
from ..tools.base import BaseTool as V2BaseTool, ToolResult

logger = logging.getLogger(__name__)

try:
    from langchain_core.callbacks import CallbackManagerForLLMRun
    from langchain_core.language_models.chat_models import BaseChatModel
    from langchain_core.messages import (
        AIMessage,
        BaseMessage,
        HumanMessage,
        SystemMessage,
    )
    from langchain_core.outputs import ChatGeneration, ChatResult
    from langchain_core.tools import BaseTool as LangChainBaseTool

    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    CallbackManagerForLLMRun = Any  # type: ignore[assignment]
    BaseChatModel = object  # type: ignore[assignment]
    BaseMessage = Any  # type: ignore[assignment]
    HumanMessage = Any  # type: ignore[assignment]
    SystemMessage = Any  # type: ignore[assignment]
    AIMessage = Any  # type: ignore[assignment]
    ChatGeneration = Any  # type: ignore[assignment]
    ChatResult = Any  # type: ignore[assignment]
    LangChainBaseTool = object  # type: ignore[assignment]


def _require_langchain() -> None:
    if not LANGCHAIN_AVAILABLE:
        raise ImportError(
            "langchain-core is required for LangChain integration. "
            "Install with: pip install langchain-core"
        )


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


if LANGCHAIN_AVAILABLE:

    class AgenticChatModel(BaseChatModel, AgentAdapter):
        """LangChain ChatModel backed by V2's LLMClientWrapper + SmartModelRouter."""

        tier: int = ModelTier.TIER_2
        _client: Optional[LLMClientWrapper] = None
        _trace_adapter: Optional[TraceAdapter] = None

        class Config:
            arbitrary_types_allowed = True

        @property
        def _llm_type(self) -> str:
            return "agentic-v2"

        def set_trace_adapter(self, trace_adapter: TraceAdapter | None) -> None:
            self._trace_adapter = trace_adapter

        def _get_client(self) -> LLMClientWrapper:
            if self._client is None:
                self._client = get_client()
            return self._client

        def _messages_to_dicts(
            self, messages: list[BaseMessage]
        ) -> list[dict[str, str]]:
            """Convert LangChain messages to OpenAI-style dicts."""
            result: list[dict[str, str]] = []
            for msg in messages:
                if isinstance(msg, SystemMessage):
                    result.append({"role": "system", "content": msg.content})
                elif isinstance(msg, HumanMessage):
                    result.append({"role": "user", "content": msg.content})
                elif isinstance(msg, AIMessage):
                    result.append({"role": "assistant", "content": msg.content})
                else:
                    result.append({"role": "user", "content": str(msg.content)})
            return result

        def _generate(
            self,
            messages: list[BaseMessage],
            stop: Optional[list[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
        ) -> ChatResult:
            """Synchronous generation (runs async under the hood)."""
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(
                    self._agenerate(messages, stop, run_manager, **kwargs)
                )
            finally:
                loop.close()

        async def _agenerate(
            self,
            messages: list[BaseMessage],
            stop: Optional[list[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
        ) -> ChatResult:
            """Async generation via V2 client."""
            _emit(
                self._trace_adapter,
                event_type="chat.generate.start",
                step_name="agentic_chat_model",
                data={"message_count": len(messages), "tier": int(self.tier)},
            )
            client = self._get_client()

            if client.backend is None:
                raise RuntimeError(
                    "No LLM backend configured on LLMClientWrapper. "
                    "Set one with client.set_backend(backend)."
                )

            msg_dicts = self._messages_to_dicts(messages)
            tier = ModelTier(self.tier)
            model = client.router.get_model_for_tier(tier)
            if model is None:
                raise RuntimeError(f"No model available for tier {tier.name}")

            result = await client.backend.complete_chat(
                model=model,
                messages=msg_dicts,
                **kwargs,
            )

            content = result.get("content", "")
            message = AIMessage(content=content)
            generation = ChatGeneration(message=message)
            _emit(
                self._trace_adapter,
                event_type="chat.generate.complete",
                step_name="agentic_chat_model",
                data={"content_length": len(content), "model": model},
            )
            return ChatResult(generations=[generation])

        @property
        def _identifying_params(self) -> dict[str, Any]:
            return {"tier": self.tier, "llm_type": self._llm_type}

else:

    class AgenticChatModel(AgentAdapter):
        """Fallback model placeholder when langchain-core is unavailable."""

        def __init__(self, tier: int = ModelTier.TIER_2, **_: Any) -> None:
            self.tier = int(tier)
            self._trace_adapter: Optional[TraceAdapter] = None

        def set_trace_adapter(self, trace_adapter: TraceAdapter | None) -> None:
            self._trace_adapter = trace_adapter

        async def ainvoke(
            self, prompt: Any, context: dict[str, Any] | None = None
        ) -> Any:
            _require_langchain()

        def invoke(self, *_args: Any, **_kwargs: Any) -> Any:
            _require_langchain()


if LANGCHAIN_AVAILABLE:

    class AgenticTool(LangChainBaseTool, ToolAdapter):
        """Wrap a V2 BaseTool as a LangChain tool and ToolAdapter."""

        name: str = ""
        description: str = ""
        _v2_tool: Optional[V2BaseTool] = None
        _trace_adapter: Optional[TraceAdapter] = None

        class Config:
            arbitrary_types_allowed = True

        @classmethod
        def from_v2_tool(cls, tool: V2BaseTool) -> "AgenticTool":
            instance = cls(name=tool.name, description=tool.description)
            instance._v2_tool = tool
            return instance

        def set_trace_adapter(self, trace_adapter: TraceAdapter | None) -> None:
            self._trace_adapter = trace_adapter

        async def execute(
            self, tool_name: str, args: dict[str, Any] | None = None
        ) -> ToolResult:
            if self._v2_tool is None:
                return ToolResult(success=False, error="No V2 tool bound")
            if tool_name and tool_name != self._v2_tool.name:
                return ToolResult(
                    success=False,
                    error=(
                        f"Tool mismatch: requested '{tool_name}', "
                        f"bound '{self._v2_tool.name}'"
                    ),
                )

            _emit(
                self._trace_adapter,
                event_type="tool.execute.start",
                step_name=self._v2_tool.name,
                data={"arg_keys": sorted((args or {}).keys())},
            )
            result = await self._v2_tool.execute(**(args or {}))
            _emit(
                self._trace_adapter,
                event_type="tool.execute.complete",
                step_name=self._v2_tool.name,
                data={"success": result.success},
            )
            return result

        def _run(self, **kwargs: Any) -> str:
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(self._arun(**kwargs))
            finally:
                loop.close()

        async def _arun(self, **kwargs: Any) -> str:
            result = await self.execute(self.name, kwargs)
            if result.success:
                return json.dumps(result.data, default=str) if result.data else "OK"
            return f"Error: {result.error}"

else:

    class AgenticTool(ToolAdapter):
        """Fallback tool adapter that does not require langchain-core."""

        def __init__(
            self,
            *,
            name: str = "",
            description: str = "",
            v2_tool: V2BaseTool | None = None,
        ) -> None:
            self.name = name
            self.description = description
            self._v2_tool = v2_tool
            self._trace_adapter: Optional[TraceAdapter] = None

        @classmethod
        def from_v2_tool(cls, tool: V2BaseTool) -> "AgenticTool":
            return cls(name=tool.name, description=tool.description, v2_tool=tool)

        def set_trace_adapter(self, trace_adapter: TraceAdapter | None) -> None:
            self._trace_adapter = trace_adapter

        async def execute(
            self, tool_name: str, args: dict[str, Any] | None = None
        ) -> ToolResult:
            if self._v2_tool is None:
                return ToolResult(success=False, error="No V2 tool bound")
            if tool_name and tool_name != self._v2_tool.name:
                return ToolResult(
                    success=False,
                    error=(
                        f"Tool mismatch: requested '{tool_name}', "
                        f"bound '{self._v2_tool.name}'"
                    ),
                )

            _emit(
                self._trace_adapter,
                event_type="tool.execute.start",
                step_name=self._v2_tool.name,
                data={"arg_keys": sorted((args or {}).keys())},
            )
            result = await self._v2_tool.execute(**(args or {}))
            _emit(
                self._trace_adapter,
                event_type="tool.execute.complete",
                step_name=self._v2_tool.name,
                data={"success": result.success},
            )
            return result

        async def _arun(self, **kwargs: Any) -> str:
            result = await self.execute(self.name, kwargs)
            if result.success:
                return json.dumps(result.data, default=str) if result.data else "OK"
            return f"Error: {result.error}"

        def _run(self, **kwargs: Any) -> str:
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(self._arun(**kwargs))
            finally:
                loop.close()


class AgenticAgent(AgentAdapter):
    """Wrap a V2 BaseAgent for adapter-compatible invocation."""

    def __init__(self, agent: Any, trace_adapter: TraceAdapter | None = None):
        self._agent = agent
        self._trace_adapter = trace_adapter

    def set_trace_adapter(self, trace_adapter: TraceAdapter | None) -> None:
        self._trace_adapter = trace_adapter

    def _resolve_input_cls(self) -> Any | None:
        orig_bases = getattr(self._agent.__class__, "__orig_bases__", ())
        for base in orig_bases:
            args = getattr(base, "__args__", ())
            if args:
                return args[0]
        return None

    def _coerce_task(self, input_data: dict[str, Any]) -> Any:
        input_cls = self._resolve_input_cls()
        if input_cls is None:
            return input_data
        try:
            return input_cls(**input_data)
        except Exception:
            return input_data

    async def ainvoke(
        self, prompt: Any, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        payload: dict[str, Any]
        if isinstance(prompt, dict):
            payload = dict(prompt)
        else:
            payload = {"task": str(prompt)}
        if context:
            payload.update(context)

        _emit(
            self._trace_adapter,
            event_type="agent.invoke.start",
            step_name=getattr(self._agent, "name", self._agent.__class__.__name__),
            data={"input_keys": sorted(payload.keys())},
        )

        task = self._coerce_task(payload)
        result = await self._agent.run(task)
        if hasattr(result, "model_dump"):
            output = result.model_dump()
        elif isinstance(result, dict):
            output = result
        else:
            output = {"result": str(result)}

        _emit(
            self._trace_adapter,
            event_type="agent.invoke.complete",
            step_name=getattr(self._agent, "name", self._agent.__class__.__name__),
            data={"output_keys": sorted(output.keys())},
        )
        return output

    def invoke(
        self, input_data: dict[str, Any], config: Optional[Any] = None
    ) -> dict[str, Any]:
        """Synchronous wrapper kept for backwards compatibility."""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.ainvoke(input_data, context=config))
        finally:
            loop.close()


# Backward-compatible aliases used by legacy docs/examples.
AgenticLangChainTool = AgenticTool
AgenticRunnable = AgenticAgent


__all__ = [
    "LANGCHAIN_AVAILABLE",
    "AgenticAgent",
    "AgenticChatModel",
    "AgenticLangChainTool",
    "AgenticRunnable",
    "AgenticTool",
]
