"""
Base Workflow

Provides foundation for workflow implementations with:
- Step management
- Context handling
- Progress tracking
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from multiagent_workflows.core.logger import VerboseLogger
from multiagent_workflows.core.model_manager import ModelManager
from multiagent_workflows.core.tool_registry import ToolRegistry


@dataclass
class WorkflowStep:
    """A single step in a workflow."""
    name: str
    agent: str
    description: str
    required_inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    optional: bool = False


@dataclass
class WorkflowContext:
    """Context maintained throughout workflow execution."""
    inputs: Dict[str, Any]
    artifacts: Dict[str, Any] = field(default_factory=dict)
    step_results: Dict[str, Any] = field(default_factory=dict)
    current_step: int = 0
    total_steps: int = 0


class BaseWorkflow(ABC):
    """
    Base class for workflow implementations.
    
    Subclasses should:
    1. Define steps in __init__
    2. Implement _create_agent for each step
    3. Optionally override _pre_step and _post_step hooks
    """
    
    name: str = "base_workflow"
    description: str = "Base workflow"
    
    def __init__(
        self,
        model_manager: ModelManager,
        tool_registry: Optional[ToolRegistry] = None,
        logger: Optional[VerboseLogger] = None,
    ):
        """Initialize workflow."""
        self.model_manager = model_manager
        self.tool_registry = tool_registry
        self.logger = logger
        self.steps: List[WorkflowStep] = []
    
    @abstractmethod
    def define_steps(self) -> List[WorkflowStep]:
        """Define the workflow steps. Must be implemented by subclasses."""
        pass
    
    async def execute(
        self,
        inputs: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Execute the workflow.
        
        Args:
            inputs: Workflow inputs
            config: Optional configuration overrides
            
        Returns:
            Workflow outputs
        """
        # Initialize steps
        self.steps = self.define_steps()
        
        # Create context
        context = WorkflowContext(
            inputs=inputs,
            total_steps=len(self.steps),
        )
        
        # Execute each step
        for i, step in enumerate(self.steps):
            context.current_step = i + 1
            
            # Pre-step hook
            await self._pre_step(step, context)
            
            # Execute step
            result = await self._execute_step(step, context)
            context.step_results[step.name] = result
            context.artifacts.update(result)
            
            # Post-step hook
            await self._post_step(step, context, result)
        
        return self._compile_outputs(context)
    
    async def _execute_step(
        self,
        step: WorkflowStep,
        context: WorkflowContext,
    ) -> Dict[str, Any]:
        """Execute a single step."""
        # Gather inputs
        step_inputs = {}
        for input_name in step.required_inputs:
            if input_name in context.inputs:
                step_inputs[input_name] = context.inputs[input_name]
            elif input_name in context.artifacts:
                step_inputs[input_name] = context.artifacts[input_name]
        
        # Create and execute agent
        agent = await self._create_agent(step)
        if agent is None:
            return {}
        
        result = await agent.execute(step_inputs, {"artifacts": context.artifacts})
        
        if result.success:
            return result.output
        else:
            if not step.optional:
                raise RuntimeError(f"Step {step.name} failed: {result.error}")
            return {}
    
    @abstractmethod
    async def _create_agent(self, step: WorkflowStep):
        """Create agent for a step. Must be implemented by subclasses."""
        pass
    
    async def _pre_step(
        self,
        step: WorkflowStep,
        context: WorkflowContext,
    ) -> None:
        """Hook called before each step. Override for custom behavior."""
        if self.logger:
            self.logger.log_step_start(
                workflow_id="",
                step_name=step.name,
                context={"step": context.current_step, "total": context.total_steps},
            )
    
    async def _post_step(
        self,
        step: WorkflowStep,
        context: WorkflowContext,
        result: Dict[str, Any],
    ) -> None:
        """Hook called after each step. Override for custom behavior."""
        pass
    
    def _compile_outputs(self, context: WorkflowContext) -> Dict[str, Any]:
        """Compile final outputs from context."""
        return {
            "artifacts": context.artifacts,
            "step_results": context.step_results,
        }
