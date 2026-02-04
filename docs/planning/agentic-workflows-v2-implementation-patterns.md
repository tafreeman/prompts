# Agentic Workflows v2 - Implementation Patterns

**Purpose:** Reference implementations for key architectural patterns  
**Date:** February 2, 2026

---

## 1. Contract-Based Agent Communication

### 1.1 Pydantic Message Models

```python
# agentic-workflows/contracts/messages.py
"""
Standardized messages for inter-agent communication.
All agents receive and emit these structured messages.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


class MessageType(str, Enum):
    """Types of messages in the system."""
    TASK = "task"           # Task assignment
    RESULT = "result"       # Task completion
    ERROR = "error"         # Error notification
    HANDOFF = "handoff"     # Agent-to-agent transfer
    FEEDBACK = "feedback"   # Iteration feedback


class AgentMessage(BaseModel):
    """
    Base message exchanged between agents.
    
    Example:
        msg = AgentMessage(
            type=MessageType.TASK,
            source_agent="orchestrator",
            target_agent="architect",
            content={"requirements": "Build a todo app"},
        )
    """
    type: MessageType
    source_agent: str
    target_agent: Optional[str] = None
    content: Dict[str, Any]
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    correlation_id: Optional[str] = None  # For tracing
    
    class Config:
        extra = "forbid"  # Strict validation - no unknown fields

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        if not v:
            raise ValueError("Content cannot be empty")
        return v


class StepResult(BaseModel):
    """
    Result from executing a workflow step.
    
    This is what the executor returns after running an agent.
    """
    step_id: str
    agent_id: str
    success: bool
    outputs: Dict[str, Any] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    duration_ms: float
    model_used: str
    tokens_used: int = 0
    iteration: int = 1  # For iterative patterns
    
    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0


class WorkflowResult(BaseModel):
    """
    Final result from a complete workflow execution.
    """
    workflow_id: str
    workflow_name: str
    success: bool
    outputs: Dict[str, Any]
    step_results: Dict[str, StepResult]
    total_duration_ms: float
    total_tokens: int = 0
    evaluation_score: Optional[float] = None
    checkpointed: bool = False
```

### 1.2 Agent-Specific Contracts

```python
# agentic-workflows/contracts/agent_contracts.py
"""
Input/Output contracts for each agent type.
These are used for validation at step boundaries.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ============================================================================
# Architect Agent Contract
# ============================================================================

class ArchitectInput(BaseModel):
    """Input schema for Architect agent."""
    requirements: str = Field(..., min_length=10)
    user_stories: Optional[List[Dict[str, Any]]] = None
    constraints: Optional[Dict[str, Any]] = None
    tech_preferences: Optional[Dict[str, str]] = None


class TechStackOutput(BaseModel):
    """Tech stack recommendation."""
    frontend: Dict[str, str] = Field(..., description="Frontend framework and language")
    backend: Dict[str, str] = Field(..., description="Backend framework and language")
    database: Dict[str, str] = Field(..., description="Database type and ORM")
    infrastructure: Dict[str, str] = Field(..., description="Deployment platform")


class ArchitectOutput(BaseModel):
    """Output schema for Architect agent."""
    tech_stack: TechStackOutput
    component_diagram: str = Field(..., description="Mermaid diagram")
    api_strategy: Dict[str, Any]
    deployment_strategy: Optional[Dict[str, Any]] = None
    rationale: str = Field(..., description="Design decisions explanation")


# ============================================================================
# Coder Agent Contract
# ============================================================================

class CoderInput(BaseModel):
    """Input schema for Coder agent."""
    spec: Dict[str, Any] = Field(..., description="Code specification")
    tech_stack: Optional[TechStackOutput] = None
    language: str = "python"
    framework: Optional[str] = None
    context_code: Optional[str] = None  # Existing code for context


class GeneratedFile(BaseModel):
    """A single generated file."""
    path: str
    content: str
    language: str


class CoderOutput(BaseModel):
    """Output schema for Coder agent."""
    files: List[GeneratedFile]
    dependencies: List[str] = Field(default_factory=list)
    setup_instructions: Optional[str] = None


# ============================================================================
# Reviewer Agent Contract
# ============================================================================

class ReviewerInput(BaseModel):
    """Input schema for Reviewer agent."""
    code: str = Field(..., min_length=10)
    context: Optional[Dict[str, Any]] = None
    focus_areas: List[str] = Field(
        default=["security", "performance", "maintainability"]
    )


class ReviewIssue(BaseModel):
    """A single review issue."""
    severity: str = Field(..., pattern="^(critical|high|medium|low|info)$")
    category: str
    location: str
    description: str
    suggestion: str


class ReviewerOutput(BaseModel):
    """Output schema for Reviewer agent."""
    issues: List[ReviewIssue]
    score: float = Field(..., ge=0, le=100)
    approved: bool
    summary: str
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)


# ============================================================================
# Contract Registry
# ============================================================================

AGENT_CONTRACTS = {
    "architect": {
        "input": ArchitectInput,
        "output": ArchitectOutput,
    },
    "coder": {
        "input": CoderInput,
        "output": CoderOutput,
    },
    "reviewer": {
        "input": ReviewerInput,
        "output": ReviewerOutput,
    },
    # Add more agents...
}


def validate_agent_input(agent_id: str, data: Dict[str, Any]) -> BaseModel:
    """Validate input data against agent contract."""
    contract = AGENT_CONTRACTS.get(agent_id)
    if not contract:
        raise ValueError(f"No contract defined for agent: {agent_id}")
    return contract["input"].model_validate(data)


def validate_agent_output(agent_id: str, data: Dict[str, Any]) -> BaseModel:
    """Validate output data against agent contract."""
    contract = AGENT_CONTRACTS.get(agent_id)
    if not contract:
        raise ValueError(f"No contract defined for agent: {agent_id}")
    return contract["output"].model_validate(data)
```

---

## 2. Tool System with Auto-Discovery

### 2.1 Base Tool Class

```python
# agentic-workflows/tools/base.py
"""
Base classes for the tool system.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
import time


class ToolSchema(BaseModel):
    """Schema describing a tool for agent consumption."""
    name: str
    description: str
    parameters: Dict[str, Any]  # JSON Schema format
    required: List[str]
    returns: str


class ToolResult(BaseModel):
    """Standardized result from tool execution."""
    success: bool
    output: Any = None
    error: Optional[str] = None
    execution_time_ms: float = 0.0


class BaseTool(ABC):
    """
    Abstract base class for all tools.
    
    Tools must implement:
    - schema property: Returns ToolSchema
    - execute method: Performs the tool action
    
    Example:
        class FileReadTool(BaseTool):
            @property
            def schema(self) -> ToolSchema:
                return ToolSchema(
                    name="file_read",
                    description="Read contents of a file",
                    parameters={
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "File path"},
                            "encoding": {"type": "string", "default": "utf-8"}
                        }
                    },
                    required=["path"],
                    returns="string"
                )
            
            async def execute(self, path: str, encoding: str = "utf-8") -> ToolResult:
                # Implementation...
    """
    
    @property
    @abstractmethod
    def schema(self) -> ToolSchema:
        """Return the tool schema for agent consumption."""
        pass
    
    @abstractmethod
    async def execute(self, **params) -> ToolResult:
        """Execute the tool with given parameters."""
        pass
    
    async def __call__(self, **params) -> ToolResult:
        """Convenience method for execution with timing."""
        start = time.perf_counter()
        try:
            result = await self.execute(**params)
            result.execution_time_ms = (time.perf_counter() - start) * 1000
            return result
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e),
                execution_time_ms=(time.perf_counter() - start) * 1000
            )
```

### 2.2 Tool Registry with Auto-Discovery

```python
# agentic-workflows/tools/registry.py
"""
Tool registry with automatic discovery and registration.
"""
from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path
from typing import Dict, List, Optional, Type

from .base import BaseTool, ToolSchema


class ToolRegistry:
    """
    Registry for tools that agents can invoke.
    
    Supports:
    - Manual registration
    - Automatic discovery from packages
    - Tool lookup by name
    """
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
    
    def register(self, tool: BaseTool) -> None:
        """Register a tool instance."""
        name = tool.schema.name
        if name in self._tools:
            raise ValueError(f"Tool '{name}' already registered")
        self._tools[name] = tool
    
    def register_class(self, tool_class: Type[BaseTool]) -> None:
        """Register a tool class (instantiates it)."""
        tool = tool_class()
        self.register(tool)
    
    def discover(self, package_path: str) -> int:
        """
        Auto-discover and register tools from a package.
        
        Args:
            package_path: Dotted path like 'agentic_workflows.tools.builtin'
            
        Returns:
            Number of tools discovered
        """
        count = 0
        package = importlib.import_module(package_path)
        
        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            module = importlib.import_module(f"{package_path}.{module_name}")
            
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    isinstance(attr, type) and
                    issubclass(attr, BaseTool) and
                    attr is not BaseTool
                ):
                    try:
                        self.register_class(attr)
                        count += 1
                    except ValueError:
                        pass  # Already registered
        
        return count
    
    def get(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name."""
        return self._tools.get(name)
    
    def list_tools(self) -> List[ToolSchema]:
        """List all registered tool schemas."""
        return [tool.schema for tool in self._tools.values()]
    
    def has(self, name: str) -> bool:
        """Check if a tool is registered."""
        return name in self._tools
    
    async def invoke(self, name: str, **params) -> Any:
        """Invoke a tool by name."""
        tool = self.get(name)
        if not tool:
            raise KeyError(f"Tool '{name}' not registered")
        return await tool(**params)


# Global registry instance
_global_registry: Optional[ToolRegistry] = None


def get_registry() -> ToolRegistry:
    """Get or create the global tool registry."""
    global _global_registry
    if _global_registry is None:
        _global_registry = ToolRegistry()
        # Auto-discover built-in tools
        _global_registry.discover("agentic_workflows.tools.builtin")
    return _global_registry
```

### 2.3 Built-in Tool Example

```python
# agentic-workflows/tools/builtin/file_operations.py
"""
File operation tools.
"""
from pathlib import Path
from typing import List, Optional
import aiofiles

from ..base import BaseTool, ToolResult, ToolSchema


class FileReadTool(BaseTool):
    """Tool for reading file contents."""
    
    @property
    def schema(self) -> ToolSchema:
        return ToolSchema(
            name="file_read",
            description="Read the contents of a file",
            parameters={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file to read"
                    },
                    "encoding": {
                        "type": "string",
                        "default": "utf-8",
                        "description": "File encoding"
                    }
                }
            },
            required=["path"],
            returns="string"
        )
    
    async def execute(
        self,
        path: str,
        encoding: str = "utf-8"
    ) -> ToolResult:
        try:
            async with aiofiles.open(path, mode="r", encoding=encoding) as f:
                content = await f.read()
            return ToolResult(success=True, output=content)
        except FileNotFoundError:
            return ToolResult(success=False, error=f"File not found: {path}")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class FileWriteTool(BaseTool):
    """Tool for writing file contents."""
    
    @property
    def schema(self) -> ToolSchema:
        return ToolSchema(
            name="file_write",
            description="Write content to a file",
            parameters={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file to write"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write"
                    },
                    "encoding": {
                        "type": "string",
                        "default": "utf-8",
                        "description": "File encoding"
                    },
                    "create_dirs": {
                        "type": "boolean",
                        "default": True,
                        "description": "Create parent directories if needed"
                    }
                }
            },
            required=["path", "content"],
            returns="boolean"
        )
    
    async def execute(
        self,
        path: str,
        content: str,
        encoding: str = "utf-8",
        create_dirs: bool = True
    ) -> ToolResult:
        try:
            p = Path(path)
            if create_dirs:
                p.parent.mkdir(parents=True, exist_ok=True)
            
            async with aiofiles.open(path, mode="w", encoding=encoding) as f:
                await f.write(content)
            
            return ToolResult(success=True, output=True)
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class FileListTool(BaseTool):
    """Tool for listing files in a directory."""
    
    @property
    def schema(self) -> ToolSchema:
        return ToolSchema(
            name="file_list",
            description="List files in a directory",
            parameters={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory path"
                    },
                    "pattern": {
                        "type": "string",
                        "default": "*",
                        "description": "Glob pattern for filtering"
                    },
                    "recursive": {
                        "type": "boolean",
                        "default": False,
                        "description": "Search recursively"
                    }
                }
            },
            required=["directory"],
            returns="array"
        )
    
    async def execute(
        self,
        directory: str,
        pattern: str = "*",
        recursive: bool = False
    ) -> ToolResult:
        try:
            p = Path(directory)
            if not p.exists():
                return ToolResult(success=False, error=f"Directory not found: {directory}")
            
            if recursive:
                files = list(p.rglob(pattern))
            else:
                files = list(p.glob(pattern))
            
            return ToolResult(
                success=True,
                output=[str(f) for f in files if f.is_file()]
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))
```

---

## 3. Execution Patterns

### 3.1 Iterative Pattern (Retry-with-Feedback)

```python
# agentic-workflows/engine/patterns/iterative.py
"""
Iterative execution pattern with feedback loops.
"""
from __future__ import annotations

from typing import Any, Callable, Dict, Optional
from dataclasses import dataclass, field

from ..context import StepContext
from ...contracts.messages import StepResult


@dataclass
class IterationFeedback:
    """Feedback from an iteration."""
    iteration: int
    score: float
    issues: list[str]
    suggestions: list[str]


@dataclass
class IterativeConfig:
    """Configuration for iterative execution."""
    max_iterations: int = 3
    success_threshold: float = 0.8
    score_function: Optional[Callable[[StepResult], float]] = None
    feedback_template: str = """
Previous attempt scored {score:.1%}. Issues found:
{issues}

Please address these issues in your next attempt.
"""


class IterativePattern:
    """
    Executes a step iteratively until success threshold is met.
    
    Each iteration:
    1. Execute the step
    2. Score the result
    3. If score >= threshold, return success
    4. Otherwise, add feedback to context and retry
    
    Example:
        pattern = IterativePattern(executor)
        result = await pattern.execute(
            step=review_step,
            context=ctx,
            config=IterativeConfig(max_iterations=3, success_threshold=0.8)
        )
    """
    
    def __init__(self, executor):
        self.executor = executor
    
    async def execute(
        self,
        step: Any,  # WorkflowStep
        context: StepContext,
        config: IterativeConfig,
    ) -> StepResult:
        """Execute step iteratively with feedback."""
        
        best_result: Optional[StepResult] = None
        best_score: float = 0.0
        feedback_history: list[IterationFeedback] = []
        
        for iteration in range(1, config.max_iterations + 1):
            # Add feedback from previous iteration to context
            if feedback_history:
                context.add_iteration_feedback(feedback_history[-1])
            
            # Execute the step
            result = await self.executor.execute_step(step, context)
            result.iteration = iteration
            
            # Score the result
            score = await self._score_result(result, config)
            
            # Track best result
            if score > best_score:
                best_score = score
                best_result = result
            
            # Check if we've met the threshold
            if score >= config.success_threshold:
                return result
            
            # Generate feedback for next iteration
            feedback = IterationFeedback(
                iteration=iteration,
                score=score,
                issues=result.errors,
                suggestions=self._generate_suggestions(result),
            )
            feedback_history.append(feedback)
        
        # Return best result after all iterations
        if best_result:
            best_result.warnings.append(
                f"Did not meet threshold ({best_score:.1%} < {config.success_threshold:.1%}) "
                f"after {config.max_iterations} iterations"
            )
            return best_result
        
        # Should not happen, but handle edge case
        return StepResult(
            step_id=step.id,
            agent_id=step.agent,
            success=False,
            errors=["No results after all iterations"],
            duration_ms=0,
            model_used="unknown",
        )
    
    async def _score_result(
        self,
        result: StepResult,
        config: IterativeConfig,
    ) -> float:
        """Score the result (0.0 to 1.0)."""
        if config.score_function:
            return config.score_function(result)
        
        # Default scoring: penalize for errors
        if not result.success:
            return 0.0
        
        base_score = 1.0
        error_penalty = len(result.errors) * 0.2
        warning_penalty = len(result.warnings) * 0.05
        
        return max(0.0, base_score - error_penalty - warning_penalty)
    
    def _generate_suggestions(self, result: StepResult) -> list[str]:
        """Generate suggestions based on errors."""
        suggestions = []
        for error in result.errors:
            if "validation" in error.lower():
                suggestions.append("Ensure output matches expected schema")
            if "timeout" in error.lower():
                suggestions.append("Simplify the request or break into smaller parts")
        return suggestions
```

### 3.2 Parallel Pattern

```python
# agentic-workflows/engine/patterns/parallel.py
"""
Parallel execution pattern for independent steps.
"""
from __future__ import annotations

import asyncio
from typing import Any, Dict, List

from ..context import StepContext
from ...contracts.messages import StepResult


class ParallelPattern:
    """
    Executes multiple steps concurrently.
    
    Use when steps are independent and can run simultaneously.
    
    Example:
        pattern = ParallelPattern(executor)
        results = await pattern.execute(
            steps=[backend_step, frontend_step],
            context=ctx,
        )
    """
    
    def __init__(self, executor, max_concurrency: int = 5):
        self.executor = executor
        self.max_concurrency = max_concurrency
        self._semaphore = asyncio.Semaphore(max_concurrency)
    
    async def execute(
        self,
        steps: List[Any],  # List[WorkflowStep]
        context: StepContext,
    ) -> Dict[str, StepResult]:
        """
        Execute steps in parallel.
        
        Returns:
            Dict mapping step_id to StepResult
        """
        async def run_step(step):
            async with self._semaphore:
                # Create isolated context for each step
                step_context = context.fork(step.id)
                result = await self.executor.execute_step(step, step_context)
                return step.id, result
        
        # Create tasks for all steps
        tasks = [run_step(step) for step in steps]
        
        # Execute all tasks concurrently
        completed = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Collect results
        results: Dict[str, StepResult] = {}
        for item in completed:
            if isinstance(item, Exception):
                # Handle task-level exceptions
                results["_error"] = StepResult(
                    step_id="_error",
                    agent_id="unknown",
                    success=False,
                    errors=[str(item)],
                    duration_ms=0,
                    model_used="unknown",
                )
            else:
                step_id, result = item
                results[step_id] = result
        
        return results
    
    async def execute_with_dependencies(
        self,
        steps: List[Any],  # List[WorkflowStep]
        dependencies: Dict[str, List[str]],  # step_id -> [dependency_ids]
        context: StepContext,
    ) -> Dict[str, StepResult]:
        """
        Execute steps respecting dependencies.
        
        Steps with no dependencies run first, then steps whose
        dependencies are complete, and so on.
        """
        results: Dict[str, StepResult] = {}
        pending = {step.id: step for step in steps}
        
        while pending:
            # Find steps with satisfied dependencies
            ready = []
            for step_id, step in pending.items():
                deps = dependencies.get(step_id, [])
                if all(dep in results for dep in deps):
                    ready.append(step)
            
            if not ready:
                # Circular dependency or missing step
                raise ValueError(
                    f"Cannot resolve dependencies for: {list(pending.keys())}"
                )
            
            # Execute ready steps in parallel
            batch_results = await self.execute(ready, context)
            results.update(batch_results)
            
            # Remove completed steps from pending
            for step in ready:
                del pending[step.id]
        
        return results
```

### 3.3 Self-Refinement Pattern (LATS-inspired)

```python
# agentic-workflows/engine/patterns/self_refine.py
"""
Self-refinement pattern inspired by LATS (Language Agent Tree Search).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..context import StepContext
from ...contracts.messages import StepResult


@dataclass
class RefinementCandidate:
    """A candidate output for evaluation."""
    result: StepResult
    score: float
    feedback: str


class SelfRefinePattern:
    """
    Self-refinement loop: Generate → Evaluate → Refine.
    
    Process:
    1. Generate initial output
    2. Use evaluator agent to score and critique
    3. If score is good enough, return
    4. Otherwise, use refiner agent to improve based on critique
    5. Repeat until threshold or max iterations
    
    Example:
        pattern = SelfRefinePattern(executor, evaluator)
        result = await pattern.execute(
            generator_step=code_gen_step,
            evaluator_step=review_step,
            refiner_step=fix_step,
            context=ctx,
        )
    """
    
    def __init__(
        self,
        executor,
        max_iterations: int = 3,
        success_threshold: float = 0.85,
        keep_best: bool = True,
    ):
        self.executor = executor
        self.max_iterations = max_iterations
        self.success_threshold = success_threshold
        self.keep_best = keep_best
    
    async def execute(
        self,
        generator_step: Any,  # WorkflowStep for initial generation
        evaluator_step: Any,  # WorkflowStep for evaluation/critique
        refiner_step: Any,    # WorkflowStep for refinement
        context: StepContext,
    ) -> StepResult:
        """Execute self-refinement loop."""
        
        candidates: List[RefinementCandidate] = []
        current_output: Optional[StepResult] = None
        
        for iteration in range(self.max_iterations):
            # Step 1: Generate (or refine previous)
            if iteration == 0:
                gen_result = await self.executor.execute_step(
                    generator_step, context
                )
            else:
                # Add previous critique to context
                context.set("previous_output", current_output.outputs)
                context.set("critique", candidates[-1].feedback)
                
                gen_result = await self.executor.execute_step(
                    refiner_step, context
                )
            
            if not gen_result.success:
                # Generation failed, try again or return best
                if self.keep_best and candidates:
                    return candidates[-1].result
                return gen_result
            
            current_output = gen_result
            
            # Step 2: Evaluate
            context.set("code_to_evaluate", current_output.outputs)
            eval_result = await self.executor.execute_step(
                evaluator_step, context
            )
            
            if not eval_result.success:
                # Evaluation failed, return current output
                return current_output
            
            # Extract score and feedback
            score = eval_result.outputs.get("score", 0) / 100  # Normalize to 0-1
            feedback = eval_result.outputs.get("summary", "")
            
            candidates.append(RefinementCandidate(
                result=current_output,
                score=score,
                feedback=feedback,
            ))
            
            # Step 3: Check if good enough
            if score >= self.success_threshold:
                return current_output
        
        # Return best candidate
        if self.keep_best and candidates:
            best = max(candidates, key=lambda c: c.score)
            best.result.warnings.append(
                f"Best score {best.score:.1%} after {len(candidates)} attempts"
            )
            return best.result
        
        return current_output or StepResult(
            step_id=generator_step.id,
            agent_id=generator_step.agent,
            success=False,
            errors=["Self-refinement failed"],
            duration_ms=0,
            model_used="unknown",
        )
```

---

## 4. State Management & Checkpointing

```python
# agentic-workflows/engine/state.py
"""
State management with checkpointing support.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class WorkflowCheckpoint(BaseModel):
    """Checkpoint for persisting workflow state."""
    workflow_id: str
    workflow_name: str
    current_step: str
    completed_steps: List[str]
    step_results: Dict[str, Any]
    context: Dict[str, Any]
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    version: str = "1.0"


class StateManager:
    """
    Manages workflow state and checkpointing.
    
    Features:
    - Save checkpoints after each step
    - Resume from checkpoint
    - List available checkpoints
    - Clean up old checkpoints
    """
    
    def __init__(
        self,
        checkpoint_dir: Path | str = ".checkpoints",
        auto_checkpoint: bool = True,
    ):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.auto_checkpoint = auto_checkpoint
    
    def _checkpoint_path(self, workflow_id: str) -> Path:
        return self.checkpoint_dir / f"{workflow_id}.json"
    
    def save(self, checkpoint: WorkflowCheckpoint) -> None:
        """Save a checkpoint."""
        path = self._checkpoint_path(checkpoint.workflow_id)
        path.write_text(checkpoint.model_dump_json(indent=2))
    
    def load(self, workflow_id: str) -> Optional[WorkflowCheckpoint]:
        """Load a checkpoint if it exists."""
        path = self._checkpoint_path(workflow_id)
        if path.exists():
            return WorkflowCheckpoint.model_validate_json(path.read_text())
        return None
    
    def delete(self, workflow_id: str) -> bool:
        """Delete a checkpoint."""
        path = self._checkpoint_path(workflow_id)
        if path.exists():
            path.unlink()
            return True
        return False
    
    def list_checkpoints(self) -> List[Dict[str, Any]]:
        """List all available checkpoints."""
        checkpoints = []
        for path in self.checkpoint_dir.glob("*.json"):
            try:
                cp = WorkflowCheckpoint.model_validate_json(path.read_text())
                checkpoints.append({
                    "workflow_id": cp.workflow_id,
                    "workflow_name": cp.workflow_name,
                    "current_step": cp.current_step,
                    "timestamp": cp.timestamp,
                })
            except Exception:
                continue
        return sorted(checkpoints, key=lambda x: x["timestamp"], reverse=True)
    
    def create_checkpoint(
        self,
        workflow_id: str,
        workflow_name: str,
        current_step: str,
        completed_steps: List[str],
        step_results: Dict[str, Any],
        context: Dict[str, Any],
    ) -> WorkflowCheckpoint:
        """Create and save a checkpoint."""
        checkpoint = WorkflowCheckpoint(
            workflow_id=workflow_id,
            workflow_name=workflow_name,
            current_step=current_step,
            completed_steps=completed_steps,
            step_results=step_results,
            context=context,
        )
        if self.auto_checkpoint:
            self.save(checkpoint)
        return checkpoint
```

---

## 5. CLI Example

```python
# agentic-workflows/cli/main.py
"""
Command-line interface for agentic workflows.
"""
import typer
from rich.console import Console
from rich.table import Table
from typing import Optional

app = typer.Typer(
    name="agentic",
    help="Agentic Workflows CLI - Run multi-agent workflows"
)
console = Console()


@app.command()
def run(
    workflow: str = typer.Argument(..., help="Workflow name to execute"),
    requirements: Optional[str] = typer.Option(None, "--requirements", "-r"),
    input_file: Optional[str] = typer.Option(None, "--input", "-i"),
    model: Optional[str] = typer.Option(None, "--model", "-m"),
    prefer_local: bool = typer.Option(False, "--local"),
    resume: Optional[str] = typer.Option(None, "--resume"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    """Run a workflow."""
    console.print(f"[bold blue]Running workflow:[/] {workflow}")
    
    # Implementation would go here
    # from agentic_workflows import Orchestrator
    # ...


@app.command()
def list(
    what: str = typer.Argument("workflows", help="What to list: workflows, agents, tools")
):
    """List available resources."""
    table = Table(title=f"Available {what.title()}")
    
    if what == "workflows":
        table.add_column("Name")
        table.add_column("Description")
        # Add rows...
    elif what == "agents":
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Role")
        # Add rows...
    elif what == "tools":
        table.add_column("Name")
        table.add_column("Description")
        # Add rows...
    
    console.print(table)


@app.command()
def validate(
    config_file: str = typer.Argument(..., help="Config file to validate")
):
    """Validate a configuration file."""
    # Implementation would go here
    pass


@app.command()
def checkpoints():
    """List and manage checkpoints."""
    # Implementation would go here
    pass


if __name__ == "__main__":
    app()
```

---

## Summary

This document provides reference implementations for the key architectural patterns in the v2 system:

1. **Contract-Based Communication** - Pydantic models for all inter-agent messages
2. **Tool System** - Auto-discovery registry with standardized schemas
3. **Execution Patterns** - Iterative, parallel, and self-refinement loops
4. **State Management** - Checkpointing for long-running workflows
5. **CLI** - Typer-based command-line interface

These patterns align with best practices from AutoGen and LangGraph while being tailored to this specific use case. The UI is a thin client that only consumes server endpoints, keeping integration minimal. All new components are duplicated into the new package; existing implementations remain untouched until migration completion and new repo creation.
