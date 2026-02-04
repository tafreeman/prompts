"""LangGraph State Management.

Defines state schemas for different workflow types. Provides typed state
classes for LangGraph StateGraph usage.
"""

from __future__ import annotations

import operator
from typing import Any, Dict, List, Optional, TypedDict

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


# =============================================================================
# Base State Types
# =============================================================================


class BaseWorkflowState(TypedDict, total=False):
    """Base state shared across all workflows."""

    # Workflow metadata
    workflow_id: str
    workflow_name: str
    current_step: str

    # Execution tracking
    messages: Annotated[List[Dict[str, Any]], operator.add]
    errors: Annotated[List[str], operator.add]

    # Artifacts storage
    artifacts: Dict[str, Any]

    # Evaluation data
    scores: Dict[str, float]
    evaluation_notes: Annotated[List[str], operator.add]


# =============================================================================
# Full-Stack Generation State
# =============================================================================


class FullStackState(BaseWorkflowState):
    """State for full-stack application generation workflow."""

    # Inputs
    requirements: str
    mockup_path: Optional[str]
    tech_preferences: Optional[Dict[str, Any]]

    # Step outputs
    user_stories: Annotated[List[str], operator.add]
    data_entities: List[Dict[str, Any]]
    architecture: Dict[str, Any]
    tech_stack: Dict[str, Any]
    schema: str
    migrations: List[str]
    api_spec: Dict[str, Any]
    endpoints: List[Dict[str, Any]]
    backend_code: str
    frontend_code: str
    review_results: Dict[str, Any]
    tests: str
    readme: str
    api_docs: str


# =============================================================================
# Legacy Refactoring State
# =============================================================================


class RefactoringState(BaseWorkflowState):
    """State for legacy code refactoring workflow."""

    # Inputs
    codebase_path: str
    target_framework: Optional[str]

    # Step outputs
    structure_analysis: Dict[str, Any]
    component_inventory: List[Dict[str, Any]]
    dependency_graph: Dict[str, Any]
    coupling_report: Dict[str, Any]
    anti_patterns: List[Dict[str, Any]]
    code_smells: List[Dict[str, Any]]
    prioritized_issues: List[Dict[str, Any]]
    coverage_report: Dict[str, Any]
    coverage_gaps: List[str]
    characterization_tests: str
    refactoring_roadmap: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    transformed_code: str
    change_log: List[str]
    migrated_code: str
    dependency_updates: List[str]
    validation_report: Dict[str, Any]
    test_results: Dict[str, Any]


# =============================================================================
# Bug Fixing State
# =============================================================================


class BugFixingState(BaseWorkflowState):
    """State for bug triage and fixing workflow."""

    # Inputs
    bug_report: str
    codebase_path: str

    # Step outputs
    structured_bug: Dict[str, Any]
    affected_areas: List[str]
    severity: str
    repro_test: str
    failure_trace: str
    execution_trace: str
    failure_point: Dict[str, Any]
    root_cause: str
    causal_chain: List[str]
    candidate_fixes: List[Dict[str, Any]]
    regression_tests: str
    validated_fix: Dict[str, Any]
    test_results: Dict[str, Any]
    impact_analysis: Dict[str, Any]
    affected_modules: List[str]
    fix_documentation: str
    pr_title: str
    pr_body: str
    pr_labels: List[str]


# =============================================================================
# Architecture Evolution State
# =============================================================================


class ArchitectureEvolutionState(BaseWorkflowState):
    """State for architecture evolution workflow."""

    # Inputs
    codebase_path: str
    business_context: Optional[str]

    # Step outputs
    component_inventory: List[Dict[str, Any]]
    current_architecture: Dict[str, Any]
    debt_items: List[Dict[str, Any]]
    debt_prioritization: List[Dict[str, Any]]
    gap_analysis: Dict[str, Any]
    pattern_recommendations: List[Dict[str, Any]]
    bottlenecks: List[str]
    scaling_limits: Dict[str, Any]
    security_findings: List[Dict[str, Any]]
    vulnerability_assessment: Dict[str, Any]
    evolution_strategy: Dict[str, Any]
    target_architecture: Dict[str, Any]
    effort_estimate: Dict[str, Any]
    resource_requirements: Dict[str, Any]
    adrs: List[Dict[str, Any]]
    decision_rationale: str
    phased_roadmap: Dict[str, Any]
    milestones: List[Dict[str, Any]]
    executive_summary: str
    recommendations: List[str]


# =============================================================================
# Code Grading State
# =============================================================================


class CodeGradingState(BaseWorkflowState):
    """State for code quality grading workflow."""

    # Inputs
    code_submission: str
    language: Optional[str]
    context: Optional[str]

    # Step outputs
    lint_results: Dict[str, Any]
    complexity_metrics: Dict[str, Any]
    duplication_report: Dict[str, Any]
    coverage_metrics: Dict[str, Any]
    test_quality_assessment: Dict[str, Any]
    docstring_coverage: float
    comment_quality: Dict[str, Any]
    readme_assessment: Dict[str, Any]
    owasp_findings: List[Dict[str, Any]]
    vulnerability_list: List[Dict[str, Any]]
    severity_assessment: Dict[str, Any]
    cve_report: List[Dict[str, Any]]
    license_compliance: Dict[str, Any]
    outdated_deps: List[str]
    complexity_analysis: Dict[str, Any]
    optimization_suggestions: List[str]
    resource_usage: Dict[str, Any]
    pattern_adherence: Dict[str, Any]
    separation_score: float
    architecture_issues: List[str]
    maintainability_index: float
    tech_debt_estimate: Dict[str, Any]
    refactoring_suggestions: List[str]
    framework_compliance: Dict[str, Any]
    idiom_violations: List[str]
    style_recommendations: List[str]
    overall_grade: str
    category_scores: Dict[str, float]
    final_report: str
    improvement_priorities: List[str]


# =============================================================================
# State Factory
# =============================================================================

WORKFLOW_STATE_MAP: Dict[str, type] = {
    "fullstack_generation": FullStackState,
    "legacy_refactoring": RefactoringState,
    "bug_fixing": BugFixingState,
    "architecture_evolution": ArchitectureEvolutionState,
    "code_grading": CodeGradingState,
}


def get_state_class(workflow_name: str) -> type:
    """Get the appropriate state class for a workflow."""
    return WORKFLOW_STATE_MAP.get(workflow_name, BaseWorkflowState)


def create_initial_state(
    workflow_name: str,
    inputs: Dict[str, Any],
    workflow_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Create initial state for a workflow.

    Args:
        workflow_name: Name of the workflow
        inputs: Initial inputs
        workflow_id: Optional workflow ID

    Returns:
        Initial state dict
    """
    import uuid

    state = {
        "workflow_id": workflow_id or str(uuid.uuid4()),
        "workflow_name": workflow_name,
        "current_step": "",
        "messages": [],
        "errors": [],
        "artifacts": {},
        "scores": {},
        "evaluation_notes": [],
    }

    # Merge inputs
    state.update(inputs)

    return state
