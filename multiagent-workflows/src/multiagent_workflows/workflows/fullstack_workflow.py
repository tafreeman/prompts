"""
Full-Stack Application Generation Workflow

Converts business requirements and UI mockups into a complete full-stack application.

Steps:
1. Requirements Analysis - Parse business requirements
2. Architecture Design - Design system architecture  
3. Database Design - Create database schema
4. API Design - Design REST/GraphQL APIs
5. Backend Generation - Generate backend code
6. Frontend Generation - Generate frontend code
7. Code Review - Review for security and quality
8. Test Generation - Generate test suites
9. Documentation - Generate documentation
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from multiagent_workflows.core.agent_base import AgentBase, AgentConfig
from multiagent_workflows.core.logger import VerboseLogger
from multiagent_workflows.core.model_manager import ModelManager
from multiagent_workflows.core.tool_registry import ToolRegistry
from multiagent_workflows.workflows.base import BaseWorkflow, WorkflowStep

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
                agent="requirements_agent",
                description="Parse business requirements into structured format",
                required_inputs=["requirements"],
                outputs=["user_stories", "data_entities"],
            ),
            WorkflowStep(
                name="architecture_design",
                agent="architect_agent",
                description="Design system architecture and tech stack",
                required_inputs=["user_stories"],
                outputs=["architecture", "tech_stack"],
            ),
            WorkflowStep(
                name="database_design",
                agent="database_agent",
                description="Design database schema",
                required_inputs=["data_entities", "tech_stack"],
                outputs=["schema", "migrations"],
            ),
            WorkflowStep(
                name="api_design",
                agent="api_agent",
                description="Design API contracts",
                required_inputs=["user_stories", "architecture"],
                outputs=["api_spec", "endpoints"],
            ),
            WorkflowStep(
                name="backend_generation",
                agent="coder_agent",
                description="Generate backend code",
                required_inputs=["api_spec", "schema"],
                outputs=["backend_code", "backend_files"],
            ),
            WorkflowStep(
                name="frontend_generation",
                agent="coder_agent",
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
                name="test_generation",
                agent="test_agent",
                description="Generate comprehensive tests",
                required_inputs=["backend_code", "frontend_code"],
                outputs=["tests", "test_files"],
            ),
            WorkflowStep(
                name="documentation",
                agent="documentation_agent",
                description="Generate documentation",
                required_inputs=["api_spec", "architecture"],
                outputs=["readme", "api_docs"],
                optional=True,
            ),
        ]
    
    async def _create_agent(self, step: WorkflowStep) -> Optional[AgentBase]:
        """Create the appropriate agent for each step."""
        agent_configs = {
            "requirements_agent": AgentConfig(
                name="Requirements Analyst",
                role="Parse business requirements",
                model_id=self.model_manager.get_optimal_model("code_gen", 5),
                system_prompt="""You are a business analyst. Parse the requirements and output:
                
{
    "user_stories": [...],
    "functional_requirements": [...],
    "data_entities": [...],
    "non_functional_requirements": [...]
}""",
            ),
            "architect_agent": AgentConfig(
                name="Technical Architect",
                role="Design system architecture",
                model_id=self.model_manager.get_optimal_model("reasoning", 7),
                system_prompt=ArchitectAgent.__doc__ or "",
            ),
            "database_agent": AgentConfig(
                name="Database Designer",
                role="Design database schema",
                model_id=self.model_manager.get_optimal_model("code_gen", 5),
                system_prompt="""You are a database expert. Design the schema as SQL DDL.""",
            ),
            "api_agent": AgentConfig(
                name="API Designer",
                role="Design API contracts",
                model_id=self.model_manager.get_optimal_model("code_gen", 5),
                system_prompt="""You are an API designer. Create OpenAPI 3.0 specification.""",
            ),
            "coder_agent": AgentConfig(
                name="Code Generator",
                role="Generate production code",
                model_id=self.model_manager.get_optimal_model("code_gen", 7),
                system_prompt=CoderAgent.__doc__ or "",
            ),
            "reviewer_agent": AgentConfig(
                name="Code Reviewer",
                role="Review code quality",
                model_id=self.model_manager.get_optimal_model("code_review", 7),
                system_prompt=ReviewerAgent.__doc__ or "",
            ),
            "test_agent": AgentConfig(
                name="Test Generator",
                role="Generate tests",
                model_id=self.model_manager.get_optimal_model("code_gen", 5),
                system_prompt=TestAgent.__doc__ or "",
            ),
            "documentation_agent": AgentConfig(
                name="Documentation Agent",
                role="Generate documentation",
                model_id=self.model_manager.get_optimal_model("documentation", 3),
                system_prompt="""Generate comprehensive documentation including README and API docs.""",
            ),
        }
        
        config = agent_configs.get(step.agent)
        if not config:
            return None
        
        # Use specific agent classes where available
        agent_classes = {
            "architect_agent": ArchitectAgent,
            "reviewer_agent": ReviewerAgent,
            "test_agent": TestAgent,
        }
        
        agent_class = agent_classes.get(step.agent)
        
        if agent_class:
            return agent_class(
                config=config,
                model_manager=self.model_manager,
                tool_registry=self.tool_registry,
                logger=self.logger,
            )
        
        # Use CoderAgent as default
        return CoderAgent(
            config=config,
            model_manager=self.model_manager,
            tool_registry=self.tool_registry,
            logger=self.logger,
        )


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
