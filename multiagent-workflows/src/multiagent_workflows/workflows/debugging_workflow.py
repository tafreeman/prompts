"""Bug Triage & Automated Fixing Workflow.

Analyzes bug reports, reproduces issues, identifies root causes, and generates fixes.

Steps:
1. Bug Analysis - Parse bug report
2. Reproduction - Create reproduction case
3. Code Tracing - Trace execution to failure
4. Root Cause Analysis - Identify root cause
5. Fix Generation - Generate candidate fixes
6. Test Generation - Create regression tests
7. Fix Validation - Validate fixes
8. Side Effect Check - Analyze side effects
9. Documentation - Document the fix
10. PR Creation - Create pull request
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from multiagent_workflows.core.agent_base import AgentBase, AgentConfig, SimpleAgent
from multiagent_workflows.core.logger import VerboseLogger
from multiagent_workflows.core.model_manager import ModelManager
from multiagent_workflows.workflows.base import BaseWorkflow, WorkflowStep


class BugFixingWorkflow(BaseWorkflow):
    """Bug triage and fixing workflow.

    Takes bug reports and produces fixes with regression tests and pull
    request content.
    """

    name = "bug_fixing"
    description = "Analyze bugs and generate fixes with tests"

    def define_steps(self) -> List[WorkflowStep]:
        """Define the workflow steps."""
        return [
            WorkflowStep(
                name="bug_analysis",
                agent="bug_analyst_agent",
                description="Parse bug report into structured format",
                required_inputs=["bug_report"],
                outputs=["structured_bug", "affected_areas", "severity"],
            ),
            WorkflowStep(
                name="reproduction",
                agent="reproduction_agent",
                description="Create reproduction case",
                required_inputs=["structured_bug", "codebase_path"],
                outputs=["repro_test", "failure_trace"],
            ),
            WorkflowStep(
                name="code_tracing",
                agent="tracer_agent",
                description="Trace execution to find failure",
                required_inputs=["failure_trace", "codebase_path"],
                outputs=["execution_trace", "failure_point"],
            ),
            WorkflowStep(
                name="root_cause_analysis",
                agent="root_cause_agent",
                description="Identify root cause",
                required_inputs=["execution_trace", "failure_point"],
                outputs=["root_cause", "causal_chain"],
            ),
            WorkflowStep(
                name="fix_generation",
                agent="fix_generator_agent",
                description="Generate candidate fixes",
                required_inputs=["root_cause", "codebase_path"],
                outputs=["candidate_fixes"],
            ),
            WorkflowStep(
                name="test_generation",
                agent="test_generator_agent",
                description="Create regression tests",
                required_inputs=["repro_test", "candidate_fixes"],
                outputs=["regression_tests"],
            ),
            WorkflowStep(
                name="fix_validation",
                agent="validator_agent",
                description="Validate fixes",
                required_inputs=["candidate_fixes", "regression_tests"],
                outputs=["validated_fix", "test_results"],
            ),
            WorkflowStep(
                name="side_effect_check",
                agent="side_effect_agent",
                description="Analyze side effects",
                required_inputs=["validated_fix", "codebase_path"],
                outputs=["impact_analysis", "affected_modules"],
            ),
            WorkflowStep(
                name="documentation",
                agent="documentation_agent",
                description="Document the fix",
                required_inputs=["root_cause", "validated_fix"],
                outputs=["fix_documentation", "code_comments"],
            ),
            WorkflowStep(
                name="pr_creation",
                agent="pr_agent",
                description="Create pull request",
                required_inputs=["validated_fix", "fix_documentation"],
                outputs=["pr_title", "pr_body", "pr_labels"],
            ),
        ]

    async def _create_agent(self, step: WorkflowStep) -> Optional[AgentBase]:
        """Create the appropriate agent for each step."""
        agent_prompts = {
            "bug_analyst_agent": """You are a bug report analyst.
            
Parse the bug report and extract:
1. Summary of the issue
2. Steps to reproduce
3. Expected vs actual behavior
4. Environment details
5. Severity assessment (1-10)
6. Affected code areas

Output structured JSON.""",
            "reproduction_agent": """You are a reproduction specialist.
            
Create a minimal reproduction case:
1. Smallest code that triggers the bug
2. Required setup/fixtures
3. Expected failure output
4. Step-by-step instructions

Output a failing test case.""",
            "root_cause_agent": """You are a debugging expert.
            
Given the execution trace, identify:
1. The fundamental root cause (not symptoms)
2. The causal chain from root to symptom
3. Why this bug was introduced
4. Similar patterns that might exist elsewhere

Think step by step and explain your reasoning.""",
            "fix_generator_agent": """You are a bug fix specialist.
            
Generate multiple candidate fixes:
1. Minimal fix - smallest change to fix the issue
2. Robust fix - handles edge cases
3. Comprehensive fix - includes related improvements

For each, show the exact code change and explain the approach.""",
            "side_effect_agent": """You are a change impact analyst.
            
Analyze the fix for side effects:
1. Other code that calls the modified code
2. Potential behavioral changes
3. Performance implications
4. Security implications
5. Compatibility concerns

List all affected areas with risk levels.""",
            "pr_agent": """You are a pull request specialist.
            
Create a clear, professional PR:
1. Concise, descriptive title
2. Detailed description with:
   - Bug summary
   - Root cause explanation
   - Solution approach
   - Testing performed
3. Appropriate labels
4. Reviewer suggestions

Output the complete PR content.""",
        }

        prompt = agent_prompts.get(step.agent, f"Perform: {step.description}")

        # Select model based on task
        model_pref = (
            "reasoning"
            if "root_cause" in step.agent or "tracer" in step.agent
            else "code_gen"
        )

        config = AgentConfig(
            name=step.agent.replace("_", " ").title(),
            role=step.description,
            model_id=self.model_manager.get_optimal_model(model_pref, 5),
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


async def run_bug_fixing_workflow(
    bug_report: str,
    codebase_path: str,
    model_manager: Optional[ModelManager] = None,
    logger: Optional[VerboseLogger] = None,
) -> Dict[str, Any]:
    """Convenience function to run the bug fixing workflow.

    Args:
        bug_report: Bug report text
        codebase_path: Path to codebase
        model_manager: Optional model manager
        logger: Optional logger

    Returns:
        Workflow outputs including fix and tests
    """
    if model_manager is None:
        model_manager = ModelManager()

    workflow = BugFixingWorkflow(
        model_manager=model_manager,
        logger=logger,
    )

    return await workflow.execute(
        {
            "bug_report": bug_report,
            "codebase_path": codebase_path,
        }
    )
