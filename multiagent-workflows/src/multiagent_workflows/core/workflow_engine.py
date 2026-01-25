"""
Workflow Engine

Orchestrates multi-agent workflows with:
- Step-by-step execution with context passing
- Parallel step execution where applicable
- Automatic evaluation integration
- Error handling with graceful degradation
"""

from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Type

import yaml

from multiagent_workflows.core.agent_base import AgentBase, AgentConfig, AgentResult
from multiagent_workflows.core.evaluator import WorkflowEvaluator
from multiagent_workflows.core.logger import VerboseLogger
from multiagent_workflows.core.model_manager import ModelManager
from multiagent_workflows.core.tool_registry import ToolRegistry, get_default_registry


@dataclass
class WorkflowStep:
    """Definition of a workflow step."""
    id: str
    name: str
    agent: str
    model_preference: str
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    condition: Optional[str] = None
    config: Dict[str, Any] = field(default_factory=dict)
    iterative: bool = False
    max_iterations: int = 1


@dataclass
class WorkflowDefinition:
    """Complete workflow definition."""
    name: str
    description: str
    inputs: List[Dict[str, Any]]
    outputs: List[Dict[str, Any]]
    steps: List[WorkflowStep]


@dataclass
class WorkflowResult:
    """Result from workflow execution."""
    workflow_id: str
    workflow_name: str
    success: bool
    outputs: Dict[str, Any]
    duration_ms: float
    step_results: Dict[str, AgentResult]
    evaluation: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class WorkflowEngine:
    """
    Orchestrates multi-agent workflows with evaluation integration.
    
    Responsibilities:
    - Load workflow definitions from YAML
    - Execute workflows step by step
    - Pass context between steps
    - Handle parallel execution
    - Integrate with evaluation framework
    
    Example:
        engine = WorkflowEngine(model_manager, tool_registry)
        result = await engine.execute_workflow(
            "fullstack_generation",
            {"requirements": "Build a todo app..."}
        )
    """
    
    def __init__(
        self,
        model_manager: ModelManager,
        tool_registry: Optional[ToolRegistry] = None,
        evaluator: Optional[WorkflowEvaluator] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize workflow engine.
        
        Args:
            model_manager: Model manager for LLM calls
            tool_registry: Registry for tools
            evaluator: Optional evaluator for scoring
            config: Optional configuration override
        """
        self.model_manager = model_manager
        self.tool_registry = tool_registry or get_default_registry()
        self.evaluator = evaluator
        self.config = config or self._load_default_config()
        
        # Agent registry
        self._agent_classes: Dict[str, Type[AgentBase]] = {}
        self._agent_configs: Dict[str, AgentConfig] = {}
        
        # Workflow definitions
        self._workflows: Dict[str, WorkflowDefinition] = {}
        
        # Load agent and workflow configs
        self._load_agent_configs()
        self._load_workflow_definitions()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration."""
        config_path = Path(__file__).parent.parent.parent / "config" / "workflows.yaml"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {}
    
    def _load_agent_configs(self) -> None:
        """Load agent configurations from YAML."""
        config_path = Path(__file__).parent.parent.parent / "config" / "agents.yaml"
        if not config_path.exists():
            return
        
        with open(config_path, "r", encoding="utf-8") as f:
            agents_config = yaml.safe_load(f)
        
        for agent_id, agent_def in agents_config.get("agents", {}).items():
            self._agent_configs[agent_id] = AgentConfig(
                name=agent_def.get("name", agent_id),
                role=agent_def.get("role", ""),
                model_id=agent_def.get("default_model", "local:phi4mini"),
                system_prompt=agent_def.get("system_prompt", ""),
                tools=agent_def.get("tools", []),
                fallback_models=agent_def.get("fallback_models", []),
            )
    
    def _load_workflow_definitions(self) -> None:
        """Load workflow definitions from YAML."""
        workflows_config = self.config.get("workflows", {})
        
        for wf_id, wf_def in workflows_config.items():
            steps = []
            for step_def in wf_def.get("steps", []):
                steps.append(WorkflowStep(
                    id=step_def.get("id", ""),
                    name=step_def.get("name", ""),
                    agent=step_def.get("agent", ""),
                    model_preference=step_def.get("model_preference", ""),
                    inputs=step_def.get("inputs", []),
                    outputs=step_def.get("outputs", []),
                    condition=step_def.get("condition"),
                    config=step_def.get("config", {}),
                    iterative=step_def.get("iterative", False),
                    max_iterations=step_def.get("max_iterations", 1),
                ))
            
            self._workflows[wf_id] = WorkflowDefinition(
                name=wf_def.get("name", wf_id),
                description=wf_def.get("description", ""),
                inputs=wf_def.get("inputs", []),
                outputs=wf_def.get("outputs", []),
                steps=steps,
            )
    
    def register_agent(
        self,
        agent_id: str,
        agent_class: Type[AgentBase],
    ) -> None:
        """
        Register an agent class for use in workflows.
        
        Args:
            agent_id: Agent identifier matching config
            agent_class: Agent class
        """
        self._agent_classes[agent_id] = agent_class
    
    async def execute_workflow(
        self,
        workflow_name: str,
        inputs: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None,
    ) -> WorkflowResult:
        """
        Execute a predefined workflow with full logging and evaluation.
        
        Args:
            workflow_name: Name of workflow to execute
            inputs: Workflow inputs
            config: Optional config overrides
            
        Returns:
            WorkflowResult with outputs and metrics
        """
        import time
        start_time = time.perf_counter()
        
        # Generate workflow ID
        workflow_id = f"wf-{uuid.uuid4().hex[:8]}"
        
        # Create logger
        logger = VerboseLogger(
            workflow_id=workflow_id,
            config={"level": config.get("logging_level", "DEBUG") if config else "DEBUG"},
        )
        
        # Get workflow definition
        if workflow_name not in self._workflows:
            raise ValueError(f"Unknown workflow: {workflow_name}")
        
        workflow = self._workflows[workflow_name]
        
        # Log workflow start
        wf_log_id = logger.log_workflow_start(
            workflow_name=workflow.name,
            inputs=inputs,
            metadata={"description": workflow.description},
        )
        
        try:
            # Initialize context
            context = {
                "inputs": inputs,
                "config": config or {},
                "artifacts": {},
                "workflow_id": workflow_id,
            }
            
            step_results: Dict[str, AgentResult] = {}
            
            # Execute steps
            for step in workflow.steps:
                # Check condition
                if step.condition and not self._evaluate_condition(step.condition, context):
                    continue
                
                # Log step start
                step_log_id = logger.log_step_start(
                    workflow_id=wf_log_id,
                    step_name=step.name,
                    step_id=step.id,
                    context={"inputs": step.inputs, "outputs": step.outputs},
                )
                
                try:
                    # Execute step
                    step_context = context.copy()
                    step_context["step_id"] = step_log_id
                    
                    result = await self._execute_step(step, step_context, logger)
                    step_results[step.id] = result
                    
                    # Store outputs in context
                    if result.success:
                        context["artifacts"][step.id] = result.output
                    
                    logger.log_step_complete(
                        step_id=step_log_id,
                        success=result.success,
                        outputs=result.output,
                    )
                    
                except Exception as e:
                    logger.log_step_error(step_log_id, e)
                    step_results[step.id] = AgentResult(
                        success=False,
                        output={},
                        error=str(e),
                    )
            
            # Compile final output
            final_output = self._compile_output(context, workflow)
            
            # Evaluate if evaluator available
            evaluation = None
            if self.evaluator and self.evaluator.has_golden(workflow_name, inputs):
                evaluation = await self.evaluator.score_output(
                    final_output,
                    workflow_name,
                    inputs,
                )
                final_output["evaluation"] = evaluation
            
            duration_ms = (time.perf_counter() - start_time) * 1000
            
            # Log completion
            logger.log_workflow_complete(
                workflow_id=wf_log_id,
                success=True,
                summary={
                    "steps_executed": len(step_results),
                    "steps_succeeded": sum(1 for r in step_results.values() if r.success),
                    "duration_ms": duration_ms,
                },
            )
            
            # Export logs
            logs_dir = Path("evaluation/results/logs")
            logs_dir.mkdir(parents=True, exist_ok=True)
            logger.export_to_json(logs_dir / f"{workflow_id}.json")
            logger.export_to_markdown(logs_dir / f"{workflow_id}.md")
            
            return WorkflowResult(
                workflow_id=workflow_id,
                workflow_name=workflow_name,
                success=True,
                outputs=final_output,
                duration_ms=duration_ms,
                step_results=step_results,
                evaluation=evaluation,
            )
            
        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.log_workflow_error(wf_log_id, e)
            
            return WorkflowResult(
                workflow_id=workflow_id,
                workflow_name=workflow_name,
                success=False,
                outputs={},
                duration_ms=duration_ms,
                step_results={},
                error=str(e),
            )
    
    async def _execute_step(
        self,
        step: WorkflowStep,
        context: Dict[str, Any],
        logger: VerboseLogger,
    ) -> AgentResult:
        """Execute a single workflow step."""
        # Get or create agent
        agent = self._create_agent(step, context, logger)
        
        # Gather inputs from context
        task = self._gather_inputs(step.inputs, context)
        task.update(step.config)
        
        # Handle iterative steps
        if step.iterative:
            return await self._execute_iterative(agent, task, context, step.max_iterations)
        
        return await agent.execute(task, context)
    
    async def _execute_iterative(
        self,
        agent: AgentBase,
        task: Dict[str, Any],
        context: Dict[str, Any],
        max_iterations: int,
    ) -> AgentResult:
        """Execute an iterative step until done or max iterations."""
        combined_output: Dict[str, Any] = {}
        total_tokens = 0
        total_duration = 0.0
        
        for i in range(max_iterations):
            iter_task = task.copy()
            iter_task["iteration"] = i + 1
            iter_task["previous_output"] = combined_output
            
            result = await agent.execute(iter_task, context)
            
            if not result.success:
                return result
            
            combined_output.update(result.output)
            total_tokens += result.tokens_used
            total_duration += result.duration_ms
            
            # Check if done (agent can signal completion)
            if result.output.get("done", False):
                break
        
        return AgentResult(
            success=True,
            output=combined_output,
            tokens_used=total_tokens,
            duration_ms=total_duration,
        )
    
    def _create_agent(
        self,
        step: WorkflowStep,
        context: Dict[str, Any],
        logger: VerboseLogger,
    ) -> AgentBase:
        """Create an agent instance for a step."""
        agent_id = step.agent
        
        # Get or use default config
        if agent_id in self._agent_configs:
            config = self._agent_configs[agent_id]
        else:
            config = AgentConfig(
                name=agent_id,
                role=step.name,
                model_id=self._resolve_model(step.model_preference),
                system_prompt=f"You are an agent performing: {step.name}",
            )
        
        # Override model based on preference
        if step.model_preference:
            config.model_id = self._resolve_model(step.model_preference)
        
        # Get agent class or use default
        if agent_id in self._agent_classes:
            agent_class = self._agent_classes[agent_id]
            return agent_class(
                config=config,
                model_manager=self.model_manager,
                tool_registry=self.tool_registry,
                logger=logger,
            )
        
        # Use SimpleAgent as fallback
        from multiagent_workflows.core.agent_base import SimpleAgent
        return SimpleAgent(
            config=config,
            model_manager=self.model_manager,
            tool_registry=self.tool_registry,
            logger=logger,
            prompt_template="Task: {task}\n\nContext:\n{context}\n\nProvide your output:",
            output_key=step.outputs[0] if step.outputs else "output",
        )
    
    def _resolve_model(self, model_preference: str) -> str:
        """Resolve a model preference to a specific model ID."""
        return self.model_manager.get_optimal_model(
            task_type=model_preference,
            complexity=5,
            prefer_local=True,
        )
    
    def _gather_inputs(
        self,
        input_refs: List[str],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Gather inputs from context based on references."""
        result: Dict[str, Any] = {}
        
        for ref in input_refs:
            # Parse ref like "inputs.requirements" or "step1.output"
            parts = ref.split(".")
            value = context
            
            for part in parts:
                if isinstance(value, dict):
                    value = value.get(part, value.get("artifacts", {}).get(part, {}))
                else:
                    value = {}
                    break
            
            result[parts[-1]] = value
        
        return result
    
    def _evaluate_condition(
        self,
        condition: str,
        context: Dict[str, Any],
    ) -> bool:
        """Evaluate a condition string against context."""
        # Simple condition evaluation
        # Format: "inputs.field is not None" or "step.success == True"
        try:
            # Create safe evaluation context
            eval_context = {
                "inputs": context.get("inputs", {}),
                "artifacts": context.get("artifacts", {}),
                "config": context.get("config", {}),
                "None": None,
                "True": True,
                "False": False,
            }
            
            # Replace "is not None" with Python syntax
            condition = condition.replace(" is not None", " != None")
            condition = condition.replace(" is None", " == None")
            
            return eval(condition, {"__builtins__": {}}, eval_context)
        except Exception:
            return True  # Default to executing if condition fails
    
    def _compile_output(
        self,
        context: Dict[str, Any],
        workflow: WorkflowDefinition,
    ) -> Dict[str, Any]:
        """Compile final output from context artifacts."""
        output: Dict[str, Any] = {}
        
        for output_def in workflow.outputs:
            name = output_def.get("name", "")
            # Find matching artifact
            for step_id, artifacts in context.get("artifacts", {}).items():
                if isinstance(artifacts, dict) and name in artifacts:
                    output[name] = artifacts[name]
                elif step_id == name:
                    output[name] = artifacts
        
        # Include all artifacts if no specific outputs defined
        if not output:
            output = context.get("artifacts", {})
        
        return output
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """List available workflows."""
        return [
            {
                "name": wf.name,
                "description": wf.description,
                "steps": len(wf.steps),
            }
            for wf in self._workflows.values()
        ]
