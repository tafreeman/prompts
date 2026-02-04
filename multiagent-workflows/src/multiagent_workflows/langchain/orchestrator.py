"""
LangChain Workflow Orchestrator

Replaces stub functions with real LangChain execution.
Maps workflow definitions to LangGraph StateGraphs with proper agent invocations.
"""

from __future__ import annotations

import asyncio
import json
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Type, Union

import yaml

from multiagent_workflows.core.model_manager import ModelManager
from multiagent_workflows.core.tool_registry import ToolRegistry, get_default_registry
from multiagent_workflows.core.logger import VerboseLogger
from multiagent_workflows.core.contracts import get_contract
from multiagent_workflows.langchain.chains import AgentChainFactory, ChainConfig, ROLE_CHAIN_CONFIGS
from multiagent_workflows.langchain.state import (
    get_state_class,
    create_initial_state,
    BaseWorkflowState,
)
from multiagent_workflows.langchain.callbacks import WorkflowCallbackHandler


@dataclass
class WorkflowStepConfig:
    """Configuration for a workflow step."""
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
class WorkflowConfig:
    """Configuration for a complete workflow."""
    name: str
    description: str
    inputs: List[Dict[str, Any]]
    outputs: List[Dict[str, Any]]
    steps: List[WorkflowStepConfig]


class LangChainOrchestrator:
    """
    Orchestrates multi-agent workflows using LangChain/LangGraph.
    
    Replaces the stub-based orchestrator with real LLM-backed execution.
    """
    
    def __init__(
        self,
        model_manager: ModelManager,
        tool_registry: Optional[ToolRegistry] = None,
        logger: Optional[VerboseLogger] = None,
        config_path: Optional[str] = None,
        agent_config_path: Optional[str] = None,
    ):
        self.model_manager = model_manager
        self.tool_registry = tool_registry or get_default_registry()
        self.logger = logger
        
        self.chain_factory = AgentChainFactory(model_manager, self.tool_registry)
        self.workflows: Dict[str, WorkflowConfig] = {}
        self.agent_configs: Dict[str, Dict[str, Any]] = {}
        
        # Load configurations
        if config_path:
            self._load_workflow_config(config_path)
        else:
            self._load_default_workflows()
        
        if agent_config_path:
            self._load_agent_config(agent_config_path)
        else:
            self._load_default_agents()
        
        # Callback handler for logging
        self.callback_handler = WorkflowCallbackHandler(logger)
    
    def _load_workflow_config(self, path: str) -> None:
        """Load workflow definitions from YAML."""
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        for name, wf_data in data.get('workflows', {}).items():
            steps = [
                WorkflowStepConfig(
                    id=s.get('id', s.get('name', '')),
                    name=s.get('name', ''),
                    agent=s.get('agent', ''),
                    model_preference=s.get('model_preference', 'reasoning'),
                    inputs=s.get('inputs', []),
                    outputs=s.get('outputs', []),
                    condition=s.get('condition'),
                    config=s.get('config', {}),
                    iterative=s.get('iterative', False),
                    max_iterations=s.get('max_iterations', 1),
                )
                for s in wf_data.get('steps', [])
            ]
            
            self.workflows[name] = WorkflowConfig(
                name=wf_data.get('name', name),
                description=wf_data.get('description', ''),
                inputs=wf_data.get('inputs', []),
                outputs=wf_data.get('outputs', []),
                steps=steps,
            )
    
    def _load_default_workflows(self) -> None:
        """Load default workflow configurations."""
        # Try to load from default location
        default_paths = [
            Path(__file__).parent.parent.parent.parent / "config" / "workflows.yaml",
            Path(__file__).parent.parent.parent.parent.parent / "config" / "workflows.yaml",
        ]
        
        for path in default_paths:
            if path.exists():
                self._load_workflow_config(str(path))
                return
    
    def _load_agent_config(self, path: str) -> None:
        """Load agent configurations from YAML."""
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        self.agent_configs = data.get('agents', {})
    
    def _load_default_agents(self) -> None:
        """Load default agent configurations."""
        default_paths = [
            Path(__file__).parent.parent.parent.parent / "config" / "agents.yaml",
            Path(__file__).parent.parent.parent.parent.parent / "config" / "agents.yaml",
        ]
        
        for path in default_paths:
            if path.exists():
                self._load_agent_config(str(path))
                return
    
    def _get_agent_config(self, agent_id: str) -> Dict[str, Any]:
        """Get configuration for an agent."""
        # Check loaded configs
        if agent_id in self.agent_configs:
            return self.agent_configs[agent_id]
        
        # Check role chain configs as fallback
        if agent_id in ROLE_CHAIN_CONFIGS:
            return ROLE_CHAIN_CONFIGS[agent_id]
        
        # Return minimal default
        return {
            "name": agent_id.replace("_", " ").title(),
            "role": agent_id,
            "system_prompt": f"You are a {agent_id.replace('_', ' ')}. Complete the assigned task professionally.",
            "default_model": "gh:gpt-4o-mini",
        }
    
    def _resolve_model(self, preference: str) -> str:
        """Resolve model preference to actual model ID."""
        # Use cloud models for faster execution
        preference_map = {
            "vision": "gh:openai/gpt-4o",  # Cloud vision for speed
            "reasoning": "gh:openai/gpt-4o",
            "reasoning_complex": "gh:openai/o3-mini",
            "code_gen": "gh:openai/gpt-4o",
            "code_gen_fast": "gh:openai/gpt-4o-mini",
            "code_gen_premium": "gh:openai/gpt-4o",
            "code_review": "gh:openai/o4-mini",
            "documentation": "gh:openai/gpt-4o-mini",
            "coordination": "gh:openai/gpt-4o-mini",
            "local_efficient": "local:phi4",
        }
        
        return preference_map.get(preference, "gh:openai/gpt-4o-mini")
    
    def _create_step_node(
        self,
        step: WorkflowStepConfig,
    ) -> Callable:
        """Create a graph node function for a workflow step."""
        agent_config = self._get_agent_config(step.agent)
        model_id = self._resolve_model(step.model_preference)
        
        # Get or create chain for this agent
        chain_config = ChainConfig(
            agent_id=step.agent,
            name=agent_config.get("name", step.name),
            role=agent_config.get("role", step.agent),
            system_prompt=agent_config.get("system_prompt", ""),
            model_id=model_id,
            tools=agent_config.get("tools", []),
        )
        
        chain = self.chain_factory.create_chain(
            chain_config,
            use_tools=bool(chain_config.tools),
        )
        
        def node_function(state: Dict[str, Any]) -> Dict[str, Any]:
            """Execute the agent chain and update state."""
            start_time = time.time()
            
            # Log step start
            if self.callback_handler:
                self.callback_handler.on_step_start(step.name, state)
            
            try:
                # Gather inputs from state
                input_data = self._gather_step_inputs(step, state)
                
                # Validate inputs against contract (if available)
                contract = get_contract(step.agent)
                if contract:
                    input_errors = contract.validate_inputs(input_data)
                    if input_errors and self.logger:
                        self.logger.warning(f"Input validation warnings for {step.agent}: {input_errors}")
                
                # Build prompt from inputs
                input_text = self._format_step_input(step, input_data)
                
                # Execute chain
                if callable(chain):
                    # Direct callable (fallback mode)
                    result = chain({"input": input_text, "artifacts": state.get("artifacts", {})})
                elif hasattr(chain, 'invoke'):
                    # LangChain Runnable
                    result = chain.invoke({
                        "input": input_text,
                        "artifacts": state.get("artifacts", {}),
                        "history": state.get("messages", []),
                    })
                else:
                    result = {"error": "Chain not callable"}
                
                # Update state with outputs
                state_update = {"current_step": step.name}
                
                if isinstance(result, dict):
                    # Validate outputs against contract (if available)
                    if contract:
                        output_errors = contract.validate_outputs(result)
                        if output_errors and self.logger:
                            self.logger.warning(f"Output validation warnings for {step.agent}: {output_errors}")
                    
                    # Map result keys to state
                    for output_key in step.outputs:
                        if output_key in result:
                            state_update[output_key] = result[output_key]
                    
                    # Update artifacts
                    artifacts = state.get("artifacts", {}).copy()
                    artifacts.update(result)
                    state_update["artifacts"] = artifacts
                else:
                    # Single output
                    if step.outputs:
                        state_update[step.outputs[0]] = result
                
                duration_ms = (time.time() - start_time) * 1000
                
                if self.callback_handler:
                    self.callback_handler.on_step_complete(step.name, state_update, duration_ms)
                
                return state_update
                
            except Exception as e:
                error_msg = f"Step {step.name} failed: {str(e)}"
                
                if self.callback_handler:
                    self.callback_handler.on_step_error(step.name, e)
                
                return {
                    "current_step": step.name,
                    "errors": [error_msg],
                }
        
        return node_function
    
    def _gather_step_inputs(
        self,
        step: WorkflowStepConfig,
        state: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Gather inputs from state based on input references."""
        inputs = {}
        
        for ref in step.inputs:
            if ref.startswith("inputs."):
                # Direct input reference
                key = ref.replace("inputs.", "")
                if key in state:
                    inputs[key] = state[key]
            elif "." in ref:
                # Step output reference (step_name.output_key)
                parts = ref.split(".")
                step_ref = parts[0]
                output_key = parts[1]
                
                # Check artifacts first
                if output_key in state.get("artifacts", {}):
                    inputs[output_key] = state["artifacts"][output_key]
                elif output_key in state:
                    inputs[output_key] = state[output_key]
            else:
                # Direct key reference
                if ref in state.get("artifacts", {}):
                    inputs[ref] = state["artifacts"][ref]
                elif ref in state:
                    inputs[ref] = state[ref]
        
        return inputs
    
    def _format_step_input(
        self,
        step: WorkflowStepConfig,
        inputs: Dict[str, Any],
    ) -> str:
        """Format step inputs into a prompt string."""
        parts = [f"Task: {step.name}"]
        parts.append(f"Description: {step.config.get('description', '')}")
        parts.append("")
        parts.append("Inputs:")
        
        for key, value in inputs.items():
            if isinstance(value, str):
                parts.append(f"\n## {key}\n{value}")
            else:
                parts.append(f"\n## {key}\n```json\n{json.dumps(value, indent=2, default=str)}\n```")
        
        parts.append("")
        parts.append(f"Required outputs: {', '.join(step.outputs)}")
        parts.append("Provide output as a JSON object with the required keys.")
        
        return "\n".join(parts)
    
    def to_langgraph(
        self,
        workflow_name: str,
        output_path: Optional[str] = None,
    ) -> Any:
        """
        Export a workflow as a LangGraph StateGraph.
        
        Args:
            workflow_name: Name of workflow to export
            output_path: Optional path to save Mermaid diagram
            
        Returns:
            Compiled LangGraph StateGraph
        """
        try:
            from langgraph.graph import StateGraph, END
        except ImportError:
            raise ImportError("LangGraph not installed. Run: pip install langgraph")
        
        workflow = self.workflows.get(workflow_name)
        if not workflow:
            raise ValueError(f"Workflow '{workflow_name}' not found")
        
        # Get state class for this workflow
        state_class = get_state_class(workflow_name)
        
        # Create graph
        graph = StateGraph(state_class)
        
        # Build dependency map
        step_deps = self._build_dependency_map(workflow.steps)
        
        # Add nodes
        for step in workflow.steps:
            node_fn = self._create_step_node(step)
            graph.add_node(step.id, node_fn)
        
        # Add edges based on dependencies
        entry_points = []
        for step in workflow.steps:
            deps = step_deps.get(step.id, [])
            if not deps:
                entry_points.append(step.id)
            else:
                for dep in deps:
                    graph.add_edge(dep, step.id)
        
        # Set entry point(s)
        if len(entry_points) == 1:
            graph.set_entry_point(entry_points[0])
        elif entry_points:
            # Multiple entry points - start with first
            graph.set_entry_point(entry_points[0])
        
        # Find leaf nodes (no outgoing edges) and connect to END
        all_deps = set()
        for deps in step_deps.values():
            all_deps.update(deps)
        
        for step in workflow.steps:
            if step.id not in all_deps:
                graph.add_edge(step.id, END)
        
        # Compile
        compiled = graph.compile()
        
        # Export diagram if requested
        if output_path:
            try:
                mermaid = compiled.get_graph().draw_mermaid()
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(mermaid)
            except Exception as e:
                if self.logger:
                    self.logger.warning(f"Could not export diagram: {e}")
        
        return compiled
    
    def _build_dependency_map(
        self,
        steps: List[WorkflowStepConfig],
    ) -> Dict[str, List[str]]:
        """Build a map of step dependencies from input references."""
        deps = {step.id: [] for step in steps}
        step_outputs = {}
        
        # Map outputs to steps
        for step in steps:
            for output in step.outputs:
                step_outputs[output] = step.id
        
        # Resolve dependencies
        for step in steps:
            for ref in step.inputs:
                if "." in ref and not ref.startswith("inputs."):
                    step_ref = ref.split(".")[0]
                    # Find the step that produces this
                    for s in steps:
                        if s.id == step_ref or s.name == step_ref:
                            if s.id not in deps[step.id]:
                                deps[step.id].append(s.id)
                            break
                else:
                    # Check if any step produces this output
                    key = ref.replace("inputs.", "")
                    if key in step_outputs:
                        dep_step = step_outputs[key]
                        if dep_step not in deps[step.id] and dep_step != step.id:
                            deps[step.id].append(dep_step)
        
        return deps
    
    async def execute_workflow(
        self,
        workflow_name: str,
        inputs: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Execute a workflow with real LangChain chains.
        
        Args:
            workflow_name: Name of workflow to execute
            inputs: Workflow inputs
            config: Optional configuration overrides
            
        Returns:
            Workflow results including outputs and metrics
        """
        workflow_id = str(uuid.uuid4())
        start_time = time.time()
        
        if self.callback_handler:
            self.callback_handler.on_workflow_start(workflow_id, workflow_name, inputs)
        
        try:
            # Get compiled graph
            graph = self.to_langgraph(workflow_name)
            
            # Create initial state
            initial_state = create_initial_state(workflow_name, inputs, workflow_id)
            
            # Execute graph
            final_state = await asyncio.to_thread(graph.invoke, initial_state)
            
            duration_ms = (time.time() - start_time) * 1000
            
            result = {
                "workflow_id": workflow_id,
                "workflow_name": workflow_name,
                "success": not final_state.get("errors"),
                "outputs": final_state.get("artifacts", {}),
                "duration_ms": duration_ms,
                "state": final_state,
            }
            
            if self.callback_handler:
                self.callback_handler.on_workflow_complete(workflow_id, result)
            
            return result
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            result = {
                "workflow_id": workflow_id,
                "workflow_name": workflow_name,
                "success": False,
                "error": str(e),
                "duration_ms": duration_ms,
            }
            
            if self.callback_handler:
                self.callback_handler.on_workflow_error(workflow_id, e)
            
            return result


async def execute_workflow(
    workflow_name: str,
    inputs: Dict[str, Any],
    model_manager: Optional[ModelManager] = None,
    tool_registry: Optional[ToolRegistry] = None,
    logger: Optional[VerboseLogger] = None,
) -> Dict[str, Any]:
    """
    Convenience function to execute a workflow.
    
    Args:
        workflow_name: Name of workflow to execute
        inputs: Workflow inputs
        model_manager: Optional model manager
        tool_registry: Optional tool registry
        logger: Optional logger
        
    Returns:
        Workflow results
    """
    if model_manager is None:
        model_manager = ModelManager()
    
    orchestrator = LangChainOrchestrator(
        model_manager=model_manager,
        tool_registry=tool_registry,
        logger=logger,
    )
    
    return await orchestrator.execute_workflow(workflow_name, inputs)
