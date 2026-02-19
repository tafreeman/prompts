"""Claude API agent — BaseAgent subclass backed by Anthropic SDK.

Bridges the project's existing BaseAgent/BaseTool infrastructure to the
Anthropic messages API.  All your registered BaseTool instances are
automatically converted to Anthropic tool schemas and the responses are
translated back into the OpenAI-style format that BaseAgent expects.

Usage::

    from agentic_v2.agents.implementations import ClaudeAgent

    agent = ClaudeAgent(system_prompt="You are a helpful coding assistant.")
    result = await agent.run(task)
"""

from __future__ import annotations

import json
from typing import Any, Optional

try:
    import anthropic
except ImportError as e:
    raise ImportError(
        "anthropic package is required: pip install 'agentic-workflows-v2[claude]'"
    ) from e

from ..base import AgentConfig, BaseAgent
from ...contracts import TaskInput, TaskOutput


# ---------------------------------------------------------------------------
# Default task/output types (override for typed agents)
# ---------------------------------------------------------------------------

class SimpleTask(TaskInput):
    prompt: str


class SimpleOutput(TaskOutput):
    response: str


# ---------------------------------------------------------------------------
# ClaudeAgent
# ---------------------------------------------------------------------------

class ClaudeAgent(BaseAgent[SimpleTask, SimpleOutput]):
    """Concrete agent that calls Claude via the Anthropic SDK.

    Translates between the project's internal OpenAI-style message format and
    the Anthropic messages API, so all BaseAgent lifecycle / tool / memory
    features work unchanged.
    """

    def __init__(
        self,
        model: str = "claude-opus-4-6",
        system_prompt: str = "You are a helpful AI assistant.",
        config: Optional[AgentConfig] = None,
        api_key: Optional[str] = None,
        **kwargs: Any,
    ):
        cfg = config or AgentConfig(
            name="claude_agent",
            system_prompt=system_prompt,
        )
        super().__init__(config=cfg, **kwargs)
        self._model = model
        self._client = anthropic.AsyncAnthropic(api_key=api_key)  # uses ANTHROPIC_API_KEY if None

    # ------------------------------------------------------------------
    # _call_model — translate formats and call Anthropic
    # ------------------------------------------------------------------

    async def _call_model(
        self,
        messages: list[dict[str, Any]],
        tools: Optional[list[dict[str, Any]]] = None,
    ) -> dict[str, Any]:
        system, anthropic_messages = self._convert_messages(messages)
        anthropic_tools = self._convert_tools(tools or [])

        kwargs: dict[str, Any] = dict(
            model=self._model,
            max_tokens=4096,
            messages=anthropic_messages,
            thinking={"type": "adaptive"},
        )
        if system:
            kwargs["system"] = system
        if anthropic_tools:
            kwargs["tools"] = anthropic_tools

        response = await self._client.messages.create(**kwargs)
        return self._convert_response(response)

    # ------------------------------------------------------------------
    # Format conversions
    # ------------------------------------------------------------------

    @staticmethod
    def _convert_messages(
        messages: list[dict[str, Any]],
    ) -> tuple[Optional[str], list[dict[str, Any]]]:
        """Split system prompt out; convert tool-result messages."""
        system: Optional[str] = None
        out: list[dict[str, Any]] = []

        for msg in messages:
            role = msg["role"]

            if role == "system":
                # Anthropic wants system as a top-level param
                system = msg["content"]
                continue

            if role == "tool":
                # OpenAI tool result → Anthropic tool_result content block
                out.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": msg.get("tool_call_id", ""),
                        "content": msg["content"],
                    }],
                })
                continue

            out.append({"role": role, "content": msg["content"]})

        return system, out

    @staticmethod
    def _convert_tools(
        tools: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """OpenAI function-tool schema → Anthropic tool schema."""
        result = []
        for t in tools:
            fn = t.get("function", {})
            result.append({
                "name": fn["name"],
                "description": fn.get("description", ""),
                "input_schema": fn.get("parameters", {"type": "object", "properties": {}}),
            })
        return result

    @staticmethod
    def _convert_response(response: Any) -> dict[str, Any]:
        """Anthropic response → internal {content, tool_calls} dict."""
        text = ""
        tool_calls: list[dict[str, Any]] = []

        for block in response.content:
            if block.type == "text":
                text = block.text
            elif block.type == "tool_use":
                tool_calls.append({
                    "id": block.id,
                    "function": {
                        "name": block.name,
                        "arguments": block.input,  # already a dict
                    },
                })

        return {"content": text, "tool_calls": tool_calls or None}

    # ------------------------------------------------------------------
    # BaseAgent abstract methods
    # ------------------------------------------------------------------

    def _format_task_message(self, task: SimpleTask) -> str:
        return task.prompt

    async def _is_task_complete(self, task: SimpleTask, response: str) -> bool:
        return True  # single-turn by default; override for multi-turn

    async def _parse_output(self, task: SimpleTask, response: str) -> SimpleOutput:
        return SimpleOutput(response=response)
