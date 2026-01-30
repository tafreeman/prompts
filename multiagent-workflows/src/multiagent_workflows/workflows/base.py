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
    # NOTE: Artifacts are stored in a flat dictionary. Step outputs are merged,
    # and keys can be overwritten by subsequent steps. This is intentional to
    # allow for refinement loops but requires careful naming of artifact keys.
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
        checkpoint_dir: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute the workflow with support for parallel execution of independent steps.
        """
        import asyncio
        import os
        import json
        self.steps = self.define_steps()
        context = WorkflowContext(
            inputs=inputs,
            total_steps=len(self.steps),
        )

        # Logging: workflow start
        workflow_id = None
        if self.logger:
            workflow_id = self.logger.log_workflow_start(self.name, inputs)

        # Build dependency graph for steps
        step_deps = getattr(self, "step_dependencies", None)
        if step_deps is None:
            # Default: linear execution
            step_deps = {step.name: [] for step in self.steps}
            for i, step in enumerate(self.steps):
                if i > 0:
                    step_deps[step.name] = [self.steps[i-1].name]

        # Track completed steps
        completed = set()
        step_map = {step.name: step for step in self.steps}
        pending = set(step_map.keys())

        async def run_step(step_name):
            step = step_map[step_name]
            context.current_step = self.steps.index(step) + 1
            step_id = None
            if self.logger:
                step_id = self.logger.log_step_start(workflow_id or "", step.name)
            await self._pre_step(step, context)
            result = await self._execute_step(step, context)
            context.step_results[step.name] = result
            context.artifacts.update(result)
            await self._post_step(step, context, result)
            if self.logger:
                self.logger.log_step_complete(step_id or step.name, True, result)
            # Checkpoint after each step
            if checkpoint_dir:
                os.makedirs(checkpoint_dir, exist_ok=True)
                with open(os.path.join(checkpoint_dir, f"checkpoint_{step.name}.json"), "w", encoding="utf-8") as f:
                    json.dump({"artifacts": context.artifacts, "step_results": context.step_results}, f, indent=2)
            completed.add(step_name)

        # Main parallel execution loop
        try:
            while pending:
                # Find all steps whose dependencies are satisfied
                ready = [s for s in pending if all(dep in completed for dep in step_deps.get(s, []))]
                if not ready:
                    raise RuntimeError("Cyclic or unsatisfiable dependencies in workflow steps.")
                # Run all ready steps in parallel
                await asyncio.gather(*(run_step(s) for s in ready))
                for s in ready:
                    pending.remove(s)
            if self.logger:
                self.logger.log_workflow_complete(workflow_id or self.name, True, {"artifacts": context.artifacts})
        except Exception as e:
            if self.logger:
                self.logger.log_workflow_error(workflow_id or self.name, e)
            raise

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
