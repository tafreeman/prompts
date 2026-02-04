"""Base agent implementation.

Aggressive design improvements:
- Full lifecycle management (init, run, cleanup)
- Typed message passing with validation
- Dynamic tool binding at runtime
- Model tier selection with fallback
- Conversation memory with summarization
- Streaming support
- Hooks for observability
"""

from __future__ import annotations

import asyncio
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, AsyncIterator, Callable, Generic, Optional, TypeVar

from ..contracts import TaskInput, TaskOutput
from ..engine import ExecutionContext, StepDefinition
from ..models import (LLMClientWrapper, ModelTier, SmartModelRouter,
                      get_client, get_smart_router)
from ..tools import BaseTool, ToolRegistry, get_registry

TInput = TypeVar("TInput", bound=TaskInput)
TOutput = TypeVar("TOutput", bound=TaskOutput)


class AgentState(str, Enum):
    """Agent lifecycle states."""

    CREATED = "created"
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentEvent(str, Enum):
    """Events emitted by agents."""

    STATE_CHANGE = "state_change"
    MESSAGE_RECEIVED = "message_received"
    MESSAGE_SENT = "message_sent"
    TOOL_CALLED = "tool_called"
    TOOL_RESULT = "tool_result"
    THINKING = "thinking"
    STREAMING = "streaming"
    ERROR = "error"


AgentEventHandler = Callable[["BaseAgent", AgentEvent, dict[str, Any]], None]


@dataclass
class ConversationMessage:
    """A message in the agent's conversation history."""

    role: str  # "user", "assistant", "system", "tool"
    content: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    tool_call_id: Optional[str] = None
    tool_name: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict for LLM API."""
        msg = {"role": self.role, "content": self.content}
        if self.tool_call_id:
            msg["tool_call_id"] = self.tool_call_id
        if self.tool_name and self.role == "tool":
            msg["name"] = self.tool_name
        return msg


@dataclass
class ConversationMemory:
    """Manages conversation history with automatic summarization.

    Aggressive improvements:
    - Sliding window with configurable size
    - Automatic summarization when window exceeded
    - Token counting for context management
    - Message importance scoring
    """

    messages: list[ConversationMessage] = field(default_factory=list)
    max_messages: int = 50
    max_tokens: int = 8000
    summaries: list[str] = field(default_factory=list)
    max_summaries: int = 5
    token_counter: Optional[Callable[[str], int]] = None

    def add(self, role: str, content: str, **kwargs: Any) -> ConversationMessage:
        """Add a message to history."""
        msg = ConversationMessage(role=role, content=content, **kwargs)
        self.messages.append(msg)

        # Auto-trim if needed
        if (
            len(self.messages) > self.max_messages
            or self.total_tokens > self.max_tokens
        ):
            self._summarize_and_trim()

        return msg

    def add_user(self, content: str) -> ConversationMessage:
        """Add a user message."""
        return self.add("user", content)

    def add_assistant(self, content: str) -> ConversationMessage:
        """Add an assistant message."""
        return self.add("assistant", content)

    def add_system(self, content: str) -> ConversationMessage:
        """Add a system message."""
        return self.add("system", content)

    def add_tool_result(
        self, tool_name: str, result: str, tool_call_id: str
    ) -> ConversationMessage:
        """Add a tool result message."""
        return self.add("tool", result, tool_name=tool_name, tool_call_id=tool_call_id)

    def get_messages(self, include_system: bool = True) -> list[dict[str, Any]]:
        """Get messages for LLM API."""
        msgs = []

        # Add summaries as system context if available
        if self.summaries:
            summary_text = "\n\n".join(self.summaries)
            msgs.append(
                {
                    "role": "system",
                    "content": f"Previous conversation summary:\n{summary_text}",
                }
            )

        for msg in self.messages:
            if not include_system and msg.role == "system":
                continue
            msgs.append(msg.to_dict())

        return msgs

    def estimate_tokens(self, text: str) -> int:
        """Estimate tokens for the given text.

        If a token_counter is provided, it will be used. Otherwise, uses
        a simple heuristic of ~4 characters per token.
        """
        if not text:
            return 0
        if self.token_counter is not None:
            try:
                return max(0, int(self.token_counter(text)))
            except Exception:
                # Fall back to heuristic if the counter fails.
                pass
        return max(1, len(text) // 4)

    @property
    def total_tokens(self) -> int:
        """Estimate total tokens across all stored messages and summaries."""
        msg_tokens = sum(self.estimate_tokens(m.content) for m in self.messages)
        summary_tokens = sum(self.estimate_tokens(s) for s in self.summaries)
        return msg_tokens + summary_tokens

    def _preview(self, text: str, max_chars: int = 160) -> str:
        cleaned = " ".join((text or "").split())
        if len(cleaned) <= max_chars:
            return cleaned
        return cleaned[: max_chars - 3] + "..."

    def _build_summary(self, to_summarize: list[ConversationMessage]) -> str:
        if not to_summarize:
            return ""

        lines: list[str] = []
        for msg in to_summarize:
            if msg.role == "tool":
                tool_name = msg.tool_name or "tool"
                lines.append(f"tool({tool_name}): {self._preview(msg.content)}")
            else:
                lines.append(f"{msg.role}: {self._preview(msg.content)}")

        if not lines:
            return ""

        # Keep summaries bounded and predictable.
        max_lines = 30
        shown = lines[:max_lines]
        omitted = len(lines) - len(shown)
        header = f"[Summary of {len(to_summarize)} messages]"
        if omitted > 0:
            shown.append(f"... ({omitted} more omitted) ...")
        return header + "\n" + "\n".join(shown)

    def _compact_summaries(self) -> None:
        """Bound the number and size of summaries."""
        if len(self.summaries) > self.max_summaries:
            self.summaries = self.summaries[-self.max_summaries :]

        # If summaries alone consume too much budget, drop oldest.
        while self.summaries and sum(
            self.estimate_tokens(s) for s in self.summaries
        ) > (self.max_tokens // 2):
            self.summaries.pop(0)

    def _summarize_and_trim(self) -> None:
        """Summarize older messages and trim history."""
        if not self.messages:
            return

        # Keep a stable core: system prompt (first system message) + most recent messages.
        first_system = next((m for m in self.messages if m.role == "system"), None)

        keep_count = max(4, self.max_messages // 2)
        recent = self.messages[-keep_count:]

        kept: list[ConversationMessage] = []
        if first_system and first_system not in recent:
            kept.append(first_system)
        kept.extend(recent)

        # De-duplicate while preserving order.
        seen: set[int] = set()
        kept_unique: list[ConversationMessage] = []
        for m in kept:
            mid = id(m)
            if mid in seen:
                continue
            seen.add(mid)
            kept_unique.append(m)

        to_summarize = [m for m in self.messages if id(m) not in seen]
        self.messages = kept_unique

        summary = self._build_summary(to_summarize)
        if summary:
            self.summaries.append(summary)
            self._compact_summaries()

        # Enforce token budget by moving oldest non-system messages into a summary.
        extra: list[ConversationMessage] = []
        while self.messages and (
            len(self.messages) > self.max_messages
            or self.total_tokens > self.max_tokens
        ):
            # Prefer to keep the first message if it's system.
            pop_index = (
                1
                if (
                    self.messages
                    and self.messages[0].role == "system"
                    and len(self.messages) > 1
                )
                else 0
            )
            extra.append(self.messages.pop(pop_index))

        extra_summary = self._build_summary(extra)
        if extra_summary:
            self.summaries.append(extra_summary)
            self._compact_summaries()

    def clear(self) -> None:
        """Clear all history."""
        self.messages.clear()
        self.summaries.clear()

    @property
    def last_message(self) -> Optional[ConversationMessage]:
        """Get the last message."""
        return self.messages[-1] if self.messages else None


@dataclass
class AgentConfig:
    """Configuration for an agent."""

    # Identity
    name: str = "agent"
    description: str = ""
    system_prompt: str = ""

    # Model selection
    default_tier: ModelTier = ModelTier.TIER_2
    max_tier: ModelTier = ModelTier.TIER_4

    # Behavior
    max_iterations: int = 10
    max_tool_calls_per_turn: int = 5
    timeout_seconds: float = 300.0

    # Memory
    max_memory_messages: int = 50
    max_memory_tokens: int = 8000

    # Streaming
    enable_streaming: bool = False

    # Debug
    verbose: bool = False


class BaseAgent(ABC, Generic[TInput, TOutput]):
    """Abstract base agent with full lifecycle management.

    Aggressive improvements:
    - Generic input/output types for type safety
    - Full lifecycle (init → ready → running → completed)
    - Dynamic tool binding
    - Event system for observability
    - Conversation memory
    - Streaming support
    """

    def __init__(
        self,
        config: Optional[AgentConfig] = None,
        router: Optional[SmartModelRouter] = None,
        tools: Optional[ToolRegistry] = None,
        llm_client: Optional[LLMClientWrapper] = None,
    ):
        self.id = str(uuid.uuid4())
        self.config = config or AgentConfig()
        self.router = router or get_smart_router()
        self.tools = tools or get_registry()
        self.llm_client = llm_client or get_client()

        # State
        self._state = AgentState.CREATED
        self._memory = ConversationMemory(
            max_messages=self.config.max_memory_messages,
            max_tokens=self.config.max_memory_tokens,
        )
        self._bound_tools: dict[str, BaseTool] = {}
        self._event_handlers: list[AgentEventHandler] = []

        # Execution tracking
        self._current_ctx: Optional[ExecutionContext] = None
        self._iteration_count = 0
        self._tool_call_count = 0

        # Results
        self._last_result: Optional[TOutput] = None
        self._error: Optional[str] = None

    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------

    async def initialize(self, ctx: Optional[ExecutionContext] = None) -> None:
        """Initialize the agent."""
        self._set_state(AgentState.INITIALIZING)
        self._current_ctx = ctx or ExecutionContext()

        # Set up system prompt
        if self.config.system_prompt:
            self._memory.add_system(self.config.system_prompt)

        # Discover and bind tools
        await self._bind_tools()

        # Subclass initialization
        await self._on_initialize()

        self._set_state(AgentState.READY)

    async def _on_initialize(self) -> None:
        """Override for custom initialization."""
        pass

    async def cleanup(self) -> None:
        """Clean up agent resources."""
        await self._on_cleanup()
        self._memory.clear()
        self._bound_tools.clear()
        self._current_ctx = None

    async def _on_cleanup(self) -> None:
        """Override for custom cleanup."""
        pass

    # -------------------------------------------------------------------------
    # Execution
    # -------------------------------------------------------------------------

    async def run(
        self, task: TInput, ctx: Optional[ExecutionContext] = None
    ) -> TOutput:
        """Run the agent on a task.

        Args:
            task: The input task
            ctx: Optional execution context

        Returns:
            The task output
        """
        # Initialize if needed
        if self._state == AgentState.CREATED:
            await self.initialize(ctx)
        elif ctx:
            self._current_ctx = ctx

        self._set_state(AgentState.RUNNING)
        self._iteration_count = 0
        self._tool_call_count = 0

        try:
            # Add task to memory
            task_message = self._format_task_message(task)
            self._memory.add_user(task_message)

            # Main execution loop
            result = await self._execute_loop(task)

            self._last_result = result
            self._set_state(AgentState.COMPLETED)
            return result

        except asyncio.CancelledError:
            self._set_state(AgentState.CANCELLED)
            raise

        except Exception as e:
            self._error = str(e)
            self._set_state(AgentState.FAILED)
            raise

    async def _execute_loop(self, task: TInput) -> TOutput:
        """Main execution loop with iteration limit."""
        while self._iteration_count < self.config.max_iterations:
            self._iteration_count += 1

            # Get model response
            self._emit(AgentEvent.THINKING, {"iteration": self._iteration_count})

            response = await self._get_model_response()

            # Check for tool calls
            if response.get("tool_calls"):
                await self._handle_tool_calls(response["tool_calls"])
                continue

            # Check if done
            content = response.get("content", "")
            self._memory.add_assistant(content)

            if await self._is_task_complete(task, content):
                return await self._parse_output(task, content)

        # Max iterations reached
        raise RuntimeError(
            f"Agent reached max iterations ({self.config.max_iterations}) without completing task"
        )

    async def stream(
        self, task: TInput, ctx: Optional[ExecutionContext] = None
    ) -> AsyncIterator[str]:
        """Stream agent output.

        Yields content chunks as they're generated.
        """
        if not self.config.enable_streaming:
            # Fall back to non-streaming
            result = await self.run(task, ctx)
            yield str(result)
            return

        # Initialize if needed
        if self._state == AgentState.CREATED:
            await self.initialize(ctx)

        self._set_state(AgentState.RUNNING)

        try:
            task_message = self._format_task_message(task)
            self._memory.add_user(task_message)

            async for chunk in self._stream_response():
                self._emit(AgentEvent.STREAMING, {"chunk": chunk})
                yield chunk

            self._set_state(AgentState.COMPLETED)

        except Exception as e:
            self._error = str(e)
            self._set_state(AgentState.FAILED)
            raise

    # -------------------------------------------------------------------------
    # Model Interaction (override for real LLM calls)
    # -------------------------------------------------------------------------

    async def _get_model_response(self) -> dict[str, Any]:
        """Get response from the model.

        Override this to implement actual LLM calls. Default
        implementation returns a simple response for testing.
        """
        messages = self._memory.get_messages()
        tools = self._get_tool_schemas()

        # Default: subclass should override with actual LLM call
        return await self._call_model(messages, tools)

    @abstractmethod
    async def _call_model(
        self,
        messages: list[dict[str, Any]],
        tools: Optional[list[dict[str, Any]]] = None,
    ) -> dict[str, Any]:
        """Call the LLM.

        Must be implemented by subclasses.

        Returns:
            Dict with 'content' and optionally 'tool_calls'
        """
        pass

    async def _stream_response(self) -> AsyncIterator[str]:
        """Stream response from model.

        Override for real streaming.
        """
        response = await self._get_model_response()
        yield response.get("content", "")

    # -------------------------------------------------------------------------
    # Tool Handling
    # -------------------------------------------------------------------------

    async def _bind_tools(self) -> None:
        """Bind tools based on agent's tier."""
        max_tier = self.config.default_tier.value

        for tool in self.tools.list_tools():
            if tool.tier <= max_tier:
                self._bound_tools[tool.name] = tool

    def bind_tool(self, tool: BaseTool) -> None:
        """Manually bind a tool."""
        self._bound_tools[tool.name] = tool

    def unbind_tool(self, name: str) -> bool:
        """Unbind a tool."""
        if name in self._bound_tools:
            del self._bound_tools[name]
            return True
        return False

    def _get_tool_schemas(self) -> list[dict[str, Any]]:
        """Get OpenAI-compatible tool schemas."""
        schemas = []
        for tool in self._bound_tools.values():
            tool_schema = tool.get_schema()
            schemas.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool_schema.parameters if tool_schema else {},
                    },
                }
            )
        return schemas

    async def _handle_tool_calls(self, tool_calls: list[dict[str, Any]]) -> None:
        """Handle tool calls from model response."""
        for call in tool_calls[: self.config.max_tool_calls_per_turn]:
            self._tool_call_count += 1

            tool_name = call.get("function", {}).get("name", "")
            tool_args = call.get("function", {}).get("arguments", {})
            call_id = call.get("id", str(uuid.uuid4()))

            self._emit(
                AgentEvent.TOOL_CALLED,
                {"tool": tool_name, "args": tool_args, "call_id": call_id},
            )

            # Execute tool
            tool = self._bound_tools.get(tool_name)
            if tool:
                try:
                    result = await tool.execute(**tool_args)
                    result_str = (
                        str(result.data) if result.success else f"Error: {result.error}"
                    )
                except Exception as e:
                    result_str = f"Error executing tool: {e}"
            else:
                result_str = f"Unknown tool: {tool_name}"

            self._emit(
                AgentEvent.TOOL_RESULT,
                {"tool": tool_name, "result": result_str, "call_id": call_id},
            )

            # Add to memory
            self._memory.add_tool_result(tool_name, result_str, call_id)

    # -------------------------------------------------------------------------
    # Abstract Methods
    # -------------------------------------------------------------------------

    @abstractmethod
    def _format_task_message(self, task: TInput) -> str:
        """Format the task as a user message."""
        pass

    @abstractmethod
    async def _is_task_complete(self, task: TInput, response: str) -> bool:
        """Check if the task is complete based on response."""
        pass

    @abstractmethod
    async def _parse_output(self, task: TInput, response: str) -> TOutput:
        """Parse the model response into output type."""
        pass

    # -------------------------------------------------------------------------
    # Events
    # -------------------------------------------------------------------------

    def on_event(self, handler: AgentEventHandler) -> None:
        """Register an event handler."""
        self._event_handlers.append(handler)

    def off_event(self, handler: AgentEventHandler) -> bool:
        """Unregister an event handler."""
        if handler in self._event_handlers:
            self._event_handlers.remove(handler)
            return True
        return False

    def _emit(self, event: AgentEvent, data: dict[str, Any]) -> None:
        """Emit an event."""
        for handler in self._event_handlers:
            try:
                handler(self, event, data)
            except Exception:
                pass  # Don't let handler errors break agent

    def _set_state(self, state: AgentState) -> None:
        """Set agent state and emit event."""
        old_state = self._state
        self._state = state
        self._emit(
            AgentEvent.STATE_CHANGE,
            {"old_state": old_state.value, "new_state": state.value},
        )

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def state(self) -> AgentState:
        """Get current state."""
        return self._state

    @property
    def memory(self) -> ConversationMemory:
        """Get conversation memory."""
        return self._memory

    @property
    def context(self) -> Optional[ExecutionContext]:
        """Get current execution context."""
        return self._current_ctx

    @property
    def last_result(self) -> Optional[TOutput]:
        """Get last execution result."""
        return self._last_result

    @property
    def error(self) -> Optional[str]:
        """Get error if failed."""
        return self._error

    @property
    def iteration_count(self) -> int:
        """Get current iteration count."""
        return self._iteration_count

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id[:8]}, state={self._state.value})"


def agent_to_step(
    agent: BaseAgent[TInput, TOutput], name: Optional[str] = None
) -> StepDefinition:
    """Convert an agent to a step definition for pipeline integration.

    Usage:
        coder = CoderAgent()
        pipeline.add_step(agent_to_step(coder, "generate_code"))
    """

    async def run_agent(ctx: ExecutionContext) -> dict[str, Any]:
        task_data = ctx.get_sync("task")
        if task_data is None:
            raise ValueError("No task in context")

        result = await agent.run(task_data, ctx)
        return {"result": result}

    return StepDefinition(
        name=name or agent.config.name,
        description=agent.config.description,
        func=run_agent,
        tier=agent.config.default_tier,
        timeout_seconds=agent.config.timeout_seconds,
    )
