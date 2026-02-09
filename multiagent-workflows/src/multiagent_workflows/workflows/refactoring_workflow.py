"""Legacy Code Refactoring Workflow.

Analyzes legacy codebases and systematically refactors to modern patterns.

Steps:
1. Code Archaeology - Deep analysis of legacy structure
2. Dependency Mapping - Map dependencies and coupling
3. Pattern Detection - Identify anti-patterns and code smells
4. Test Coverage Analysis - Analyze existing test coverage
5. Safety Net Generation - Create characterization tests
6. Refactoring Planning - Create phased refactoring plan
7. Code Transformation - Apply incremental transformations
8. Migration - Migrate to modern framework
9. Validation - Verify behavioral equivalence
10. Documentation Update - Update documentation
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from multiagent_workflows.core.agent_base import AgentBase, AgentConfig, SimpleAgent
from multiagent_workflows.core.logger import VerboseLogger
from multiagent_workflows.core.model_manager import ModelManager
from multiagent_workflows.workflows.base import BaseWorkflow, WorkflowStep


class LegacyRefactoringWorkflow(BaseWorkflow):
    """Legacy code refactoring workflow.

    Takes a legacy codebase and produces modernized code with
    characterization tests and migration documentation.
    """

    name = "legacy_refactoring"
    description = "Refactor legacy code to modern patterns safely"

    def define_steps(self) -> List[WorkflowStep]:
        """Define the workflow steps."""
        return [
            WorkflowStep(
                name="code_archaeology",
                agent="archaeologist_agent",
                description="Deep analysis of legacy code structure",
                required_inputs=["codebase_path"],
                outputs=["structure_analysis", "component_inventory"],
            ),
            WorkflowStep(
                name="dependency_mapping",
                agent="dependency_agent",
                description="Map dependencies and coupling",
                required_inputs=["structure_analysis"],
                outputs=["dependency_graph", "coupling_report"],
            ),
            WorkflowStep(
                name="pattern_detection",
                agent="pattern_agent",
                description="Detect anti-patterns and code smells",
                required_inputs=["structure_analysis"],
                outputs=["anti_patterns", "code_smells", "prioritized_issues"],
            ),
            WorkflowStep(
                name="test_coverage_analysis",
                agent="test_analyst_agent",
                description="Analyze existing test coverage",
                required_inputs=["codebase_path"],
                outputs=["coverage_report", "coverage_gaps"],
            ),
            WorkflowStep(
                name="safety_net_generation",
                agent="safety_net_agent",
                description="Generate characterization tests",
                required_inputs=["coverage_gaps"],
                outputs=["characterization_tests"],
            ),
            WorkflowStep(
                name="refactoring_planning",
                agent="planner_agent",
                description="Create refactoring roadmap",
                required_inputs=["prioritized_issues", "coupling_report"],
                outputs=["refactoring_roadmap", "risk_assessment"],
            ),
            WorkflowStep(
                name="code_transformation",
                agent="transformer_agent",
                description="Apply code transformations",
                required_inputs=["refactoring_roadmap"],
                outputs=["transformed_code", "change_log"],
            ),
            WorkflowStep(
                name="migration",
                agent="migration_agent",
                description="Migrate to modern framework",
                required_inputs=["transformed_code", "target_framework"],
                outputs=["migrated_code", "dependency_updates"],
            ),
            WorkflowStep(
                name="validation",
                agent="validator_agent",
                description="Validate behavioral equivalence",
                required_inputs=["characterization_tests", "migrated_code"],
                outputs=["validation_report", "test_results"],
            ),
            WorkflowStep(
                name="documentation_update",
                agent="documentation_agent",
                description="Update documentation",
                required_inputs=["migrated_code", "refactoring_roadmap"],
                outputs=["updated_docs", "migration_guide"],
                optional=True,
            ),
        ]

    async def _create_agent(self, step: WorkflowStep) -> Optional[AgentBase]:
        """Create the appropriate agent for each step."""
        agent_prompts = {
            "archaeologist_agent": """You are a code archaeologist analyzing legacy codebases.
            
Analyze the code structure and document:
1. Overall architecture (layers, modules, components)
2. Key classes and their responsibilities
3. Data flow between components
4. External dependencies
5. Implicit conventions and patterns
6. Areas of high complexity

Output structured JSON with your analysis.""",
            "dependency_agent": """You are a dependency analyzer.
            
Map all dependencies and identify:
1. Module dependencies (internal)
2. External package dependencies
3. Coupling levels between components
4. Circular dependencies
5. Dependency injection patterns (or lack thereof)

Output a dependency graph and coupling metrics.""",
            "pattern_agent": """You are a code quality expert detecting anti-patterns.
            
Identify and categorize:
1. Design anti-patterns (God class, Spaghetti, etc.)
2. Performance anti-patterns
3. Security anti-patterns
4. Maintainability issues
5. Testing anti-patterns

For each issue, provide severity (1-10), location, and recommended fix.""",
            "planner_agent": """You are a refactoring strategist.
            
Create a phased refactoring plan that:
1. Prioritizes by risk and impact
2. Groups related changes
3. Minimizes regression risk
4. Includes verification steps
5. Provides rollback strategies

Output a detailed roadmap with phases, dependencies, and estimates.""",
            "transformer_agent": """You are a safe code transformer.
            
Apply refactoring transformations that:
1. Preserve external behavior
2. Are small and reversible
3. Follow established patterns
4. Include before/after documentation

Show each transformation with explanation.""",
            "validator_agent": """You are a behavioral equivalence validator.
            
Verify that refactored code:
1. Passes all existing tests
2. Passes characterization tests
3. Maintains API contracts
4. Preserves performance characteristics

Report any behavioral differences found.""",
        }

        prompt = agent_prompts.get(step.agent, f"Perform: {step.description}")

        config = AgentConfig(
            name=step.agent.replace("_", " ").title(),
            role=step.description,
            model_id=self.model_manager.get_optimal_model("code_gen", 5),
            system_prompt=prompt,
        )

        return SimpleAgent(
            config=config,
            model_manager=self.model_manager,
            tool_registry=self.tool_registry,
            logger=self.logger,
            prompt_template="Task: {task}\n\nContext:\n{context}\n\nProvide your analysis:",
            output_key=step.outputs[0] if step.outputs else "output",
        )


async def run_refactoring_workflow(
    codebase_path: str,
    target_framework: Optional[str] = None,
    model_manager: Optional[ModelManager] = None,
    logger: Optional[VerboseLogger] = None,
) -> Dict[str, Any]:
    """Convenience function to run the legacy refactoring workflow.

    Args:
        codebase_path: Path to legacy codebase
        target_framework: Target modern framework
        model_manager: Optional model manager
        logger: Optional logger

    Returns:
        Workflow outputs
    """
    if model_manager is None:
        model_manager = ModelManager()

    workflow = LegacyRefactoringWorkflow(
        model_manager=model_manager,
        logger=logger,
    )

    inputs = {"codebase_path": codebase_path}
    if target_framework:
        inputs["target_framework"] = target_framework

    return await workflow.execute(inputs)
