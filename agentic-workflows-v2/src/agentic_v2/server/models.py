"""API request and response models."""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field

from ..contracts import StepStatus


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "ok"
    version: str = "0.1.0"


class WorkflowRunRequest(BaseModel):
    """Request to run a workflow."""

    workflow: str = Field(..., description="Workflow name or path")
    input_data: dict[str, Any] = Field(
        default_factory=dict, description="Input variables"
    )
    run_id: Optional[str] = Field(None, description="Unique run identifier")


class WorkflowRunResponse(BaseModel):
    """Response from starting a workflow."""

    run_id: str
    status: StepStatus


class StepResultModel(BaseModel):
    """Serialized step result."""

    step_name: str
    status: StepStatus
    duration_ms: float
    output: Any = None
    error: Optional[str] = None


class WorkflowResultModel(BaseModel):
    """Detailed workflow result."""

    run_id: str
    workflow_name: str
    status: StepStatus
    steps: list[StepResultModel]
    final_output: dict[str, Any]


class AgentInfo(BaseModel):
    """Information about an available agent."""

    name: str
    description: str
    tier: str


class ListAgentsResponse(BaseModel):
    """Response listing available agents."""

    agents: list[AgentInfo]


class ListWorkflowsResponse(BaseModel):
    """Response listing available workflows."""

    workflows: list[str]


class DAGNodeModel(BaseModel):
    """A node in the DAG visualization."""

    id: str
    agent: Optional[str] = None
    description: str = ""
    depends_on: list[str] = []
    tier: Optional[str] = None


class DAGEdgeModel(BaseModel):
    """An edge in the DAG visualization."""

    source: str
    target: str


class DAGResponse(BaseModel):
    """DAG structure for visualization."""

    name: str
    description: str = ""
    nodes: list[DAGNodeModel]
    edges: list[DAGEdgeModel]


class RunSummaryModel(BaseModel):
    """Summary of a single run in list view."""

    filename: str
    run_id: Optional[str] = None
    workflow_name: Optional[str] = None
    status: Optional[str] = None
    success_rate: Optional[float] = None
    total_duration_ms: Optional[float] = None
    step_count: Optional[int] = None
    failed_step_count: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None


class RunsSummaryResponse(BaseModel):
    """Aggregate stats across runs."""

    total_runs: int = 0
    success: int = 0
    failed: int = 0
    avg_duration_ms: Optional[float] = None
    workflows: list[str] = []
