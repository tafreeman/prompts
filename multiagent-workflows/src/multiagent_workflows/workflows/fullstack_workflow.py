
from __future__ import annotations

from typing import Any, Dict, List, Optional, Type, TypedDict
import operator
try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

from multiagent_workflows.core.agent_base import AgentBase, AgentConfig
from multiagent_workflows.core.logger import VerboseLogger
from multiagent_workflows.core.model_manager import ModelManager
from tools.llm.langchain_adapter import LangChainAdapter
from multiagent_workflows.core.tool_registry import ToolRegistry
from multiagent_workflows.workflows.base import BaseWorkflow, WorkflowStep

from multiagent_workflows.core.agent_base import SimpleAgent
from multiagent_workflows.agents.architect_agent import ArchitectAgent
from multiagent_workflows.agents.coder_agent import CoderAgent
from multiagent_workflows.agents.reviewer_agent import ReviewerAgent
from multiagent_workflows.agents.test_agent import TestAgent


class FullStackWorkflow(BaseWorkflow):
    """
    Full-stack application generation workflow.
    
    Takes business requirements and produces a complete deployable application
    with backend, frontend, tests, and documentation.
    """

    name = "fullstack_generation"
    description = "Generate complete full-stack application from requirements"

    def define_steps(self) -> List[WorkflowStep]:
        """Define the workflow steps."""
        return [
            WorkflowStep(
                name="requirements_analysis",
                agent="requirements_analyzer",
                description="Parse business requirements into structured format",
                required_inputs=["requirements"],
                outputs=["user_stories", "data_entities"],
            ),
            WorkflowStep(
                name="architecture_design",
                agent="system_architect",
                description="Design system architecture and tech stack",
                required_inputs=["user_stories"],
                outputs=["architecture", "tech_stack"],
            ),
            WorkflowStep(
                name="database_design",
                agent="database_architect",
                description="Design database schema",
                required_inputs=["data_entities", "tech_stack"],
                outputs=["schema", "migrations"],
            ),
            WorkflowStep(
                name="api_design",
                agent="api_designer",
                description="Design API contracts",
                required_inputs=["user_stories", "architecture"],
                outputs=["api_spec", "endpoints"],
            ),
            WorkflowStep(
                name="backend_generation",
                agent="backend_generator",
                description="Generate backend code",
                required_inputs=["api_spec", "schema"],
                outputs=["backend_code", "backend_files"],
            ),
            WorkflowStep(
                name="frontend_generation",
                agent="frontend_generator",
                description="Generate frontend code",
                required_inputs=["api_spec", "architecture"],
                outputs=["frontend_code", "frontend_files"],
            ),
            WorkflowStep(
                name="code_review",
                agent="reviewer_agent",
                description="Review code for security and quality",
                required_inputs=["backend_code", "frontend_code"],
                outputs=["review_results", "issues"],
            ),
            WorkflowStep(
                name="code_refinement",
                agent="code_refiner",
                description="Refine code based on review feedback",
                required_inputs=["backend_code", "frontend_code", "review_results"],
                outputs=["backend_code", "frontend_code"], # Overwrites previous code artifacts
            ),
            WorkflowStep(
                name="test_generation",
                agent="test_generator",
                description="Generate comprehensive tests",
                required_inputs=["backend_code", "frontend_code"],
                outputs=["tests", "test_files"],
            ),
            WorkflowStep(
                name="documentation",
                agent="documentation_writer",
                description="Generate documentation",
                required_inputs=["api_spec", "architecture"],
                outputs=["readme", "api_docs"],
                optional=True,
            ),
        ]

    @property
    def step_dependencies(self):
        """
        Returns a dictionary mapping step names to their dependencies for parallel execution.
        """
        return {
            "requirements_analysis": [],
            "architecture_design": ["requirements_analysis"],
            "database_design": ["requirements_analysis", "architecture_design"],
            "api_design": ["requirements_analysis", "architecture_design"],
            "backend_generation": ["api_design", "database_design"],
            "frontend_generation": ["api_design", "architecture_design"],
            "code_review": ["backend_generation", "frontend_generation"],
            "code_refinement": ["code_review"],
            "test_generation": ["code_refinement"],
            "documentation": ["api_design", "architecture_design"],
        }

    async def _create_agent(self, step: WorkflowStep):
        """Create the appropriate agent for each step."""
        agent_details: Dict[str, Dict[str, Any]] = {
            "requirements_analyzer": {
                "class": SimpleAgent, "pref": "reasoning", "prompt": "You are a senior business analyst. Analyze the provided requirements thoroughly. Output a JSON object with keys: user_stories, data_entities."
            },
            "system_architect": {
                "class": ArchitectAgent, "pref": "reasoning", "prompt": "You are a senior system architect. Create a complete system architecture including: ARCHITECTURE DIAGRAM (in MermaidJS), SERVICE DECOMPOSITION, and TECH STACK. Output a JSON object with keys: architecture, tech_stack."
            },
            "database_architect": {
                "class": SimpleAgent, "pref": "reasoning", "prompt": "You are a database architect. Design the database schema and migrations. Output a JSON object with keys: schema, migrations."
            },
            "api_designer": {
                "class": SimpleAgent, "pref": "reasoning", "prompt": "You are an API design expert. Design the API contracts and provide a complete OpenAPI 3.0 specification. Output a JSON object with keys: api_spec, endpoints."
            },
            "backend_generator": {
                "class": CoderAgent, "pref": "code_gen", "prompt": "You are a senior backend developer. Generate backend code following clean architecture and secure coding practices. Output a JSON object with keys: backend_code, backend_files."
            },
            "frontend_generator": {
                "class": CoderAgent, "pref": "code_gen", "prompt": "You are a senior frontend developer. Generate frontend code following best practices for component structure and state management. Output a JSON object with keys: frontend_code, frontend_files."
            },
            "reviewer_agent": {
                "class": ReviewerAgent, "pref": "code_review", "prompt": "You are a senior security engineer and code reviewer. Review for SECURITY, PERFORMANCE, and MAINTAINABILITY. Output a JSON object with keys: review_results, issues."
            },
            "code_refiner": {
                "class": CoderAgent, "pref": "code_gen", "prompt": "You are a senior developer. Refine the provided code based on the review feedback to fix all identified issues. If there are no issues, return the original code. Output a JSON object with keys: backend_code, frontend_code."
            },
            "test_generator": {
                "class": TestAgent, "pref": "code_gen", "prompt": "You are a QA engineer. Generate comprehensive tests including Unit, Integration, and E2E tests. Output a JSON object with keys: tests, test_files."
            },
            "documentation_writer": {
                "class": SimpleAgent, "pref": "documentation", "prompt": "You are a technical writer. Generate a README and API documentation. Output a JSON object with keys: readme, api_docs."
            },
        }

        details = agent_details.get(step.agent)
        if not details:
            return None

        agent_class: Type[AgentBase] = details["class"]
        model_pref: str = details["pref"]
        system_prompt: str = details["prompt"]

        # Dynamically select model based on preference
        model_id = self.model_manager.get_optimal_model(model_pref, complexity=6)

        config = AgentConfig(
            name=step.agent.replace("_", " ").title(),
            role=step.description,
            model_id=model_id,
            system_prompt=system_prompt,
        )

        # Inject LangChainAdapter into agent config (as runtime attribute, not dataclass field)
        setattr(config, 'langchain_adapter', LangChainAdapter(config.model_id))

        # For SimpleAgent, we can create a generic instance.
        # For specialized agents, they might have different constructors, but here we assume a common pattern.
        if agent_class == SimpleAgent:
            # SimpleAgent is configured to wrap its output in a dict where the key is the first declared output.
            # For multiple outputs, the system prompt must instruct the model to return a JSON with all keys.
            output_keys_str = ", ".join(step.outputs)
            return SimpleAgent(
                config=config,
                model_manager=self.model_manager,
                tool_registry=self.tool_registry,
                logger=self.logger,
                prompt_template=f"Task: {{task}}\n\nContext:\n{{context}}\n\nProvide your output as a single JSON object with the keys {output_keys_str}.",
                # SimpleAgent doesn't natively support multiple output keys, so the prompt must handle it.
                # The agent will return a dict, which the workflow will unpack.
            )
        else:
            # Specialized agents like CoderAgent, ReviewerAgent are expected to handle their specific
            # inputs and outputs correctly as per their implementation.
            return agent_class(
                config=config,
                model_manager=self.model_manager,
                tool_registry=self.tool_registry,
                logger=self.logger,
            )

    def to_langgraph(self, output_path: Optional[str] = None) -> Any:
        """
        Exports this workflow as a LangChain LangGraph StateGraph.
        
        Args:
            output_path: Optional path to save the Mermaid visualization of the graph.
            
        Returns:
            A compiled StateGraph ready for execution.
        """
        try:
            from langgraph.graph import StateGraph, END
        except ImportError:
            if self.logger:
                self.logger.warning("LangGraph not installed or dependencies missing. Cannot export.")
            return None

        # Define the state schema dynamically based on workflow steps
        class WorkflowState(TypedDict):
            # Base inputs
            requirements: str
            # Dynamic outputs from steps
            user_stories: Annotated[List[str], operator.add]
            architecture: Dict
            tech_stack: Dict
            schema: str
            api_spec: Dict
            backend_code: str
            frontend_code: str
            review_results: Dict
            tests: str
            readme: str
            artifacts: Dict[str, Any]

        workflow = StateGraph(WorkflowState)
        steps = self.define_steps()
        step_deps = self.step_dependencies
        
        # Add nodes for each step
        for step in steps:
            # In a real implementation, this would wrap the actual AgentBase.execute
            # For now, we register the node name
            workflow.add_node(step.name, lambda state: {step.outputs[0]: f"Generated by {step.agent}"})

        # Add edges based on dependencies
        dependencies_found = False
        for step in steps:
            deps = step_deps.get(step.name, [])
            if not deps:
                # No dependencies -> Entry point
                workflow.set_entry_point(step.name)
            else:
                dependencies_found = True
                for dep in deps:
                    workflow.add_edge(dep, step.name)
        
        # If no explicit dependencies were found in the config, fall back to sequential
        if not dependencies_found and len(steps) > 1:
             for i in range(1, len(steps)):
                 workflow.add_edge(steps[i-1].name, steps[i].name)
             workflow.set_entry_point(steps[0].name)

        # Add edge from last step(s) to END
        # A step is a leaf if it is not a dependency for any other step
        all_deps = set()
        for deps in step_deps.values():
            all_deps.update(deps)
            
        for step in steps:
            if step.name not in all_deps and step.name != "code_refinement": # logic exception for cycle
                # Check if it isn't part of a cycle or explicitly final
                 workflow.add_edge(step.name, END)
                 
        # Special handling for cycle in code_refinement if needed, or just let it be linear for now
        # Ideally, we should detect leaf nodes more robustly.
        # For this specific workflow, 'documentation' is a leaf. 'test_generation' is a leaf? 
        # Let's just connect the last defined step to END for simplicity if no better logic,
        # OR better: connect all nodes that have no outgoing edges to END.
        
        # Simplified END connection: Connect explicitly known final steps
        # or the last step in the list if it's a linear process.
        # Given the "bad output" complaint, let's trust the step defs are topologically sorted-ish
        # but the safest generic way is to connect sinks to END.
        
        # Re-evaluating: The original code connected steps[-1] to END. 
        # Let's keep that default but be smarter if possible. 
        # For now, let's just restore the basic logic but using the graph edges.
        workflow.add_edge(steps[-1].name, END)
        compiled_graph = workflow.compile()

        if output_path:
            try:
                mermaid_graph = compiled_graph.get_graph().draw_mermaid()
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(mermaid_graph)
                if self.logger:
                    import logging
                    # Fallback to standard logging if custom logger doesn't support info/error directly
                    logging.getLogger(__name__).info(f"LangGraph exported to {output_path}")
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Failed to save LangGraph export: {e}")

        return compiled_graph


async def run_fullstack_workflow(
    requirements: str,
    model_manager: Optional[ModelManager] = None,
    logger: Optional[VerboseLogger] = None,
) -> Dict[str, Any]:
    """
    Convenience function to run the full-stack workflow.
    
    Args:
        requirements: Business requirements text
        model_manager: Optional model manager (creates default if not provided)
        logger: Optional logger
        
    Returns:
        Workflow outputs
    """
    if model_manager is None:
        model_manager = ModelManager()
    
    workflow = FullStackWorkflow(
        model_manager=model_manager,
        logger=logger,
    )
    
    return await workflow.execute({"requirements": requirements})
