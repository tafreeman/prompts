"""
Base Agent Class

Provides a foundation for all agents with:
- Built-in logging hooks
- Tool invocation support
- Structured output handling
- Error handling with retries
"""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Type

from multiagent_workflows.core.logger import VerboseLogger
from multiagent_workflows.core.model_manager import ModelManager
from multiagent_workflows.core.tool_registry import ToolRegistry


@dataclass
class AgentConfig:
    """Configuration for an agent."""
    name: str
    role: str
    model_id: str
    system_prompt: str
    tools: List[str] = field(default_factory=list)
    fallback_models: List[str] = field(default_factory=list)
    max_retries: int = 3
    timeout_seconds: int = 300


@dataclass
class AgentResult:
    """Result from agent execution."""
    success: bool
    output: Dict[str, Any]
    error: Optional[str] = None
    tokens_used: int = 0
    duration_ms: float = 0.0


class AgentBase(ABC):
    """
    Base class for all agents with built-in logging and tool support.
    
    All agents should inherit from this class and implement:
    - _process(): Core logic for processing tasks
    
    Example:
        class ArchitectAgent(AgentBase):
            async def _process(self, task: dict, context: dict) -> dict:
                # Generate architecture design
                result = await self.call_model(
                    "Design the system architecture for: " + task["requirements"]
                )
                return {"architecture": result.text}
    """
    
    def __init__(
        self,
        config: AgentConfig,
        model_manager: ModelManager,
        tool_registry: Optional[ToolRegistry] = None,
        logger: Optional[VerboseLogger] = None,
    ):
        """
        Initialize agent.
        
        Args:
            config: Agent configuration
            model_manager: Model manager for LLM calls
            tool_registry: Registry for tool invocations
            logger: Verbose logger for tracking
        """
        self.config = config
        self.model_manager = model_manager
        self.tool_registry = tool_registry or ToolRegistry()
        self.logger = logger
        
        # Runtime state
        self._agent_id: Optional[str] = None
        self._current_model: str = config.model_id
    
    @property
    def name(self) -> str:
        """Agent name."""
        return self.config.name
    
    @property
    def role(self) -> str:
        """Agent role description."""
        return self.config.role
    
    @property
    def system_prompt(self) -> str:
        """Agent system prompt."""
        return self.config.system_prompt
    
    async def execute(
        self,
        task: Dict[str, Any],
        context: Dict[str, Any],
    ) -> AgentResult:
        """
        Execute agent task with context and full logging.
        
        Args:
            task: Task specification
            context: Execution context (inputs from previous steps)
            
        Returns:
            AgentResult with output and metrics
        """
        import time
        start_time = time.perf_counter()
        
        # Log agent start
        if self.logger:
            self._agent_id = self.logger.log_agent_start(
                step_id=context.get("step_id", "unknown"),
                agent_name=self.name,
                model_id=self._current_model,
                system_prompt=self.system_prompt,
            )
        
        try:
            # Process with retries
            result = await self._execute_with_retries(task, context)
            
            duration_ms = (time.perf_counter() - start_time) * 1000
            
            # Log success
            if self.logger and self._agent_id:
                self.logger.log_agent_output(
                    agent_id=self._agent_id,
                    output=result,
                    metrics={"duration_ms": duration_ms},
                )
            
            return AgentResult(
                success=True,
                output=result,
                duration_ms=duration_ms,
            )
            
        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            
            # Log error
            if self.logger and self._agent_id:
                self.logger.log_agent_error(self._agent_id, e)
            
            return AgentResult(
                success=False,
                output={},
                error=str(e),
                duration_ms=duration_ms,
            )
    
    async def _execute_with_retries(
        self,
        task: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute with retry logic and model fallback."""
        last_error: Optional[Exception] = None
        models_to_try = [self._current_model] + self.config.fallback_models
        
        for model_id in models_to_try:
            self._current_model = model_id
            
            for attempt in range(self.config.max_retries):
                try:
                    return await asyncio.wait_for(
                        self._process(task, context),
                        timeout=self.config.timeout_seconds,
                    )
                except asyncio.TimeoutError:
                    last_error = TimeoutError(
                        f"Agent {self.name} timed out after {self.config.timeout_seconds}s"
                    )
                except Exception as e:
                    last_error = e
                    # Wait before retry
                    await asyncio.sleep(1.0 * (attempt + 1))
        
        raise last_error or RuntimeError(f"Agent {self.name} failed after all retries")
    
    async def _process(
        self,
        task: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Fallback core processing logic for agents without a custom implementation.
        Calls the model and tries to parse JSON from the response, returning structured output or a raw_response field.
        """
        prompt = task.get("prompt") or task.get("requirements") or task.get("input") or str(task)
        result = await self.call_model(prompt=prompt)
        response = result.text if hasattr(result, "text") else str(result)
        import json
        # Try to extract JSON from response
        try:
            if "```json" in response:
                start = response.index("```json") + 7
                end = response.index("```", start)
                json_str = response[start:end].strip()
            elif "```" in response:
                start = response.index("```") + 3
                end = response.index("```", start)
                json_str = response[start:end].strip()
            elif "{" in response:
                start = response.index("{")
                end = response.rindex("}") + 1
                json_str = response[start:end]
            else:
                json_str = response
            return json.loads(json_str)
        except Exception:
            return {"raw_response": response}
    
    async def call_model(
        self,
        prompt: str,
        context: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ):
        """
        Call the model with the agent's system prompt.
        
        Args:
            prompt: User prompt
            context: Optional additional context
            temperature: Override temperature
            max_tokens: Override max tokens
            
        Returns:
            GenerationResult from model
        """
        return await self.model_manager.generate(
            model_id=self._current_model,
            prompt=prompt,
            context=context,
            system_prompt=self.system_prompt,
            temperature=temperature or 0.7,
            max_tokens=max_tokens or 4096,
        )
    
    async def use_tool(
        self,
        tool_name: str,
        params: Dict[str, Any],
    ) -> Any:
        """
        Invoke a registered tool with logging.
        
        Args:
            tool_name: Name of the tool to invoke
            params: Tool parameters
            
        Returns:
            Tool result
        """
        # Log tool invocation
        tool_call_id = None
        if self.logger and self._agent_id:
            tool_call_id = self.logger.log_tool_invocation(
                agent_id=self._agent_id,
                tool_name=tool_name,
                params=params,
            )
        
        try:
            result = await self.tool_registry.invoke(tool_name, params)
            
            # Log result
            if self.logger and tool_call_id:
                self.logger.log_tool_result(tool_call_id, result, success=True)
            
            return result
            
        except Exception as e:
            if self.logger and tool_call_id:
                self.logger.log_tool_result(tool_call_id, str(e), success=False)
            raise
    
    def format_context(self, context: Dict[str, Any]) -> str:
        """Format context dict as string for prompt inclusion."""
        if not context:
            return ""
        
        lines = ["## Context from previous steps:", ""]
        for key, value in context.items():
            if key.startswith("_"):
                continue  # Skip internal keys
            if isinstance(value, dict):
                lines.append(f"### {key}")
                for k, v in value.items():
                    lines.append(f"- {k}: {v}")
            else:
                lines.append(f"### {key}")
                lines.append(str(value))
            lines.append("")
        
        return "\n".join(lines)


class SimpleAgent(AgentBase):
    """
    Simple agent that just calls the model with a prompt template.
    
    For simple use cases where no special processing is needed.
    """
    
    def __init__(
        self,
        config: AgentConfig,
        model_manager: ModelManager,
        prompt_template: str,
        output_key: str = "output",
        **kwargs,
    ):
        """
        Initialize simple agent.
        
        Args:
            config: Agent configuration
            model_manager: Model manager
            prompt_template: Template with {task} and {context} placeholders
            output_key: Key for the output in result dict
        """
        super().__init__(config, model_manager, **kwargs)
        self.prompt_template = prompt_template
        self.output_key = output_key
    
    async def _process(
        self,
        task: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Process by filling template and calling model."""
        prompt = self.prompt_template.format(
            task=task,
            context=self.format_context(context),
        )
        
        result = await self.call_model(prompt)
        
        return {self.output_key: result.text}
