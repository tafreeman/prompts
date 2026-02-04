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
