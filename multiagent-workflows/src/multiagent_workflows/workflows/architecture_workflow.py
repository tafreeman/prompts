"""
Architecture Evolution Workflow

Analyzes existing architecture, identifies technical debt, and creates evolution roadmap.

Steps:
1. Architecture Scan - Analyze current architecture
2. Debt Assessment - Identify technical debt
3. Pattern Matching - Compare to best practices
4. Scalability Analysis - Identify bottlenecks
5. Security Audit - Review security architecture
6. Modernization Planning - Create evolution strategy
7. Cost Estimation - Estimate effort and ROI
8. ADR Generation - Create Architecture Decision Records
9. Roadmap Building - Build migration roadmap
10. Stakeholder Report - Create executive summary
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from multiagent_workflows.core.agent_base import AgentBase, AgentConfig, SimpleAgent
from multiagent_workflows.core.logger import VerboseLogger
from multiagent_workflows.core.model_manager import ModelManager
from multiagent_workflows.core.tool_registry import ToolRegistry
from multiagent_workflows.workflows.base import BaseWorkflow, WorkflowStep


class ArchitectureEvolutionWorkflow(BaseWorkflow):
    """
    Architecture evolution workflow.
    
    Takes a codebase and produces architecture assessment,
    evolution roadmap, and ADRs.
    """
    
    name = "architecture_evolution"
    description = "Assess architecture and create evolution roadmap"
    
    def define_steps(self) -> List[WorkflowStep]:
        """Define the workflow steps."""
        return [
            WorkflowStep(
                name="architecture_scan",
                agent="scanner_agent",
                description="Scan current architecture",
                required_inputs=["codebase_path"],
                outputs=["component_inventory", "current_architecture"],
            ),
            WorkflowStep(
                name="debt_assessment",
                agent="debt_assessor_agent",
                description="Identify technical debt",
                required_inputs=["current_architecture"],
                outputs=["debt_items", "debt_prioritization"],
            ),
            WorkflowStep(
                name="pattern_matching",
                agent="pattern_matcher_agent",
                description="Compare to best practices",
                required_inputs=["current_architecture"],
                outputs=["gap_analysis", "pattern_recommendations"],
            ),
            WorkflowStep(
                name="scalability_analysis",
                agent="scalability_agent",
                description="Analyze scalability",
                required_inputs=["component_inventory"],
                outputs=["bottlenecks", "scaling_limits"],
            ),
            WorkflowStep(
                name="security_audit",
                agent="security_auditor_agent",
                description="Security architecture review",
                required_inputs=["current_architecture"],
                outputs=["security_findings", "vulnerability_assessment"],
            ),
            WorkflowStep(
                name="modernization_planning",
                agent="modernization_planner_agent",
                description="Create evolution strategy",
                required_inputs=["debt_prioritization", "pattern_recommendations"],
                outputs=["evolution_strategy", "target_architecture"],
            ),
            WorkflowStep(
                name="cost_estimation",
                agent="cost_estimator_agent",
                description="Estimate migration effort",
                required_inputs=["evolution_strategy"],
                outputs=["effort_estimate", "resource_requirements"],
            ),
            WorkflowStep(
                name="adr_generation",
                agent="adr_agent",
                description="Generate Architecture Decision Records",
                required_inputs=["target_architecture"],
                outputs=["adrs", "decision_rationale"],
            ),
            WorkflowStep(
                name="roadmap_building",
                agent="roadmap_agent",
                description="Build migration roadmap",
                required_inputs=["effort_estimate", "evolution_strategy"],
                outputs=["phased_roadmap", "milestones"],
            ),
            WorkflowStep(
                name="stakeholder_report",
                agent="reporter_agent",
                description="Create executive summary",
                required_inputs=["debt_items", "phased_roadmap"],
                outputs=["executive_summary", "recommendations"],
            ),
        ]
    
    async def _create_agent(self, step: WorkflowStep) -> Optional[AgentBase]:
        """Create the appropriate agent for each step."""
        agent_prompts = {
            "scanner_agent": """You are an architecture analyst.
            
Scan and document the current architecture:
1. High-level component structure
2. Service boundaries and interfaces
3. Data stores and data flow
4. External dependencies
5. Communication patterns (sync/async)
6. Deployment topology

Create architecture diagrams using Mermaid notation.""",
            
            "debt_assessor_agent": """You are a technical debt expert.
            
Identify and quantify technical debt:
1. Code debt (complexity, duplication)
2. Architecture debt (outdated patterns)
3. Infrastructure debt (legacy dependencies)
4. Documentation debt
5. Test debt (low coverage)

For each item: impact (1-10), effort (story points), priority.""",
            
            "scalability_agent": """You are a scalability engineer.
            
Analyze scaling characteristics:
1. Current capacity limits
2. Bottlenecks (CPU, memory, I/O, network)
3. Database scaling constraints
4. Stateful components
5. Horizontal vs vertical scaling options

Provide metrics and recommendations.""",
            
            "security_auditor_agent": """You are a security architect.
            
Review security architecture:
1. Authentication/authorization mechanisms
2. Data protection (at rest, in transit)
3. API security
4. Secrets management
5. Network security
6. Compliance requirements

Rate each area (1-10) and list vulnerabilities.""",
            
            "modernization_planner_agent": """You are a modernization strategist.
            
Create an evolution strategy:
1. Target architecture vision
2. Key transformations needed
3. Risk mitigation strategies
4. Dependencies between changes
5. Quick wins vs long-term improvements

Output a clear evolution plan.""",
            
            "adr_agent": """You are an architecture documentation expert.
            
Generate ADRs following this format:
1. Title - Short descriptive title
2. Status - Proposed/Accepted/Deprecated
3. Context - Why is this decision needed?
4. Decision - What change is proposed?
5. Consequences - Trade-offs and implications
6. Alternatives - What else was considered?

Create ADRs for all key architectural decisions.""",
            
            "reporter_agent": """You are an executive communications expert.
            
Create a stakeholder summary:
1. Executive summary (1 page)
2. Key findings and risks
3. Recommended actions
4. Investment required
5. Expected ROI
6. Timeline overview

Make it clear, concise, and actionable for leadership.""",
        }
        
        prompt = agent_prompts.get(step.agent, f"Perform: {step.description}")
        
        # Select model based on task
        if "security" in step.agent or "auditor" in step.agent:
            model_pref = "code_review"
        elif "reporter" in step.agent or "adr" in step.agent:
            model_pref = "documentation"
        else:
            model_pref = "reasoning"
        
        config = AgentConfig(
            name=step.agent.replace("_", " ").title(),
            role=step.description,
            model_id=self.model_manager.get_optimal_model(model_pref, 6),
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


async def run_architecture_workflow(
    codebase_path: str,
    business_context: Optional[str] = None,
    model_manager: Optional[ModelManager] = None,
    logger: Optional[VerboseLogger] = None,
) -> Dict[str, Any]:
    """
    Convenience function to run the architecture evolution workflow.
    
    Args:
        codebase_path: Path to codebase
        business_context: Business goals and constraints
        model_manager: Optional model manager
        logger: Optional logger
        
    Returns:
        Workflow outputs including roadmap and ADRs
    """
    if model_manager is None:
        model_manager = ModelManager()
    
    workflow = ArchitectureEvolutionWorkflow(
        model_manager=model_manager,
        logger=logger,
    )
    
    inputs = {"codebase_path": codebase_path}
    if business_context:
        inputs["business_context"] = business_context
    
    return await workflow.execute(inputs)
