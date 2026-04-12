"""Pydantic request and response models for the Agentic server REST API.

All models use Pydantic V2 ``BaseModel`` with ``Field`` annotations.
These schemas define the JSON contract between the FastAPI backend and
the React frontend (or any HTTP client).

Request models:
    :class:`WorkflowRunRequest` -- POST ``/api/run`` payload.
    :class:`WorkflowEvaluationRequest` -- nested evaluation settings.
    :class:`WorkflowExecutionProfileRequest` -- runtime execution controls.

Response models:
    :class:`HealthResponse` -- GET ``/api/health``.
    :class:`WorkflowRunResponse` -- accepted run confirmation.
    :class:`WorkflowResultModel` -- detailed run result.
    :class:`ListWorkflowsResponse`, :class:`ListAgentsResponse` -- discovery.
    :class:`DAGResponse` -- workflow DAG structure for visualization.
    :class:`RunsSummaryResponse` -- aggregate run statistics.
    :class:`ListEvaluationDatasetsResponse` -- available datasets for eval UI.
"""

from __future__ import annotations

import re
from typing import Any, Literal

import yaml
from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from ..contracts import StepStatus


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "ok"
    version: str = "0.1.0"


class WorkflowExecutionProfileRequest(BaseModel):
    """Optional execution profile controlling runtime behavior for workflow
    runs.

    Attributes:
        runtime: Execution runtime (``"subprocess"`` or ``"docker"``).
        max_attempts: Maximum retry attempts per step (None = unlimited).
        max_duration_minutes: Hard timeout for the entire workflow run.
        container_image: Docker image to use when ``runtime="docker"``.
    """

    runtime: Literal["subprocess", "docker"] = "subprocess"
    max_attempts: int | None = Field(default=None, ge=1)
    max_duration_minutes: int | None = Field(default=None, ge=1)
    container_image: str | None = None


class WorkflowRunRequest(BaseModel):
    """POST ``/api/run`` request body to execute a workflow.

    Attributes:
        workflow: Workflow name or YAML path to execute.
        input_data: Key-value input variables for the workflow.
        run_id: Optional user-supplied run identifier (auto-generated if None).
        adapter: Execution adapter name (default ``"langchain"``).
        evaluation: Optional evaluation settings for scored runs.
        execution_profile: Optional runtime execution controls.
    """

    workflow: str = Field(..., description="Workflow name or path")
    input_data: dict[str, Any] = Field(
        default_factory=dict, description="Input variables"
    )
    run_id: str | None = Field(None, description="Unique run identifier")

    @field_validator("run_id")
    @classmethod
    def _validate_run_id(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if not re.match(r"^[a-zA-Z0-9_-]{1,128}$", v):
            raise ValueError(
                "run_id must be 1-128 characters using only letters, digits, hyphens, and underscores"
            )
        return v


    adapter: str = Field(
        "langchain",
        description="Execution adapter: 'langchain' (default) or 'native'",
    )
    evaluation: WorkflowEvaluationRequest | None = Field(
        None, description="Optional evaluation settings for scored runs"
    )
    execution_profile: WorkflowExecutionProfileRequest | None = Field(
        None, description="Optional runtime execution settings"
    )


class WorkflowRunResponse(BaseModel):
    """Immediate response confirming a workflow run was accepted.

    Attributes:
        run_id: Unique identifier for the background execution.
        status: Initial status (always ``PENDING`` on acceptance).
    """

    run_id: str
    status: StepStatus


class StepResultModel(BaseModel):
    """Serialized result of a single workflow step execution.

    Attributes:
        step_name: Identifier of the step within the workflow DAG.
        status: Terminal status of the step.
        duration_ms: Wall-clock execution time in milliseconds.
        output: Step output data (type varies by agent).
        error: Error message if the step failed, else None.
    """

    step_name: str
    status: StepStatus
    duration_ms: float
    output: Any = None
    error: str | None = None


class WorkflowResultModel(BaseModel):
    """Complete workflow execution result with per-step detail.

    Attributes:
        run_id: Unique run identifier.
        workflow_name: Name of the executed workflow.
        status: Overall terminal status of the workflow.
        steps: Ordered list of per-step results.
        final_output: Resolved workflow output variables.
    """

    run_id: str
    workflow_name: str
    status: StepStatus
    steps: list[StepResultModel]
    final_output: dict[str, Any]


class AgentInfo(BaseModel):
    """Metadata for a single agent discovered from configuration.

    Attributes:
        name: Display name of the agent.
        description: Human-readable summary of the agent's role.
        tier: Model tier assignment (e.g., ``"1"``, ``"2"``, ``"3"``).
    """

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
    """A single node (step) in the workflow DAG visualization.

    Attributes:
        id: Step name used as the unique node identifier.
        agent: Agent name assigned to execute this step, or None.
        description: Human-readable step description.
        depends_on: List of predecessor step names.
        tier: Model tier hint (often embedded in the agent name).
    """

    id: str
    agent: str | None = None
    description: str = ""
    depends_on: list[str] = []
    tier: str | None = None


class DAGEdgeModel(BaseModel):
    """A directed dependency edge in the workflow DAG visualization.

    Attributes:
        source: Name of the predecessor step.
        target: Name of the dependent step.
    """

    source: str
    target: str


class DAGResponse(BaseModel):
    """Complete DAG structure returned by ``GET /api/workflows/{name}/dag``.

    Attributes:
        name: Workflow name.
        description: Workflow description from the YAML definition.
        nodes: List of DAG nodes (steps).
        edges: List of directed dependency edges.
    """

    name: str
    description: str = ""
    nodes: list[DAGNodeModel]
    edges: list[DAGEdgeModel]


class WorkflowEditorRequest(BaseModel):
    """Request body for workflow editor validate/save operations."""

    model_config = ConfigDict(populate_by_name=True)

    document: dict[str, Any] | None = Field(
        default=None,
        description="Raw YAML workflow document expressed as JSON.",
    )
    yaml_text: str | None = Field(
        default=None,
        validation_alias=AliasChoices("yaml_text", "source"),
        description="Raw YAML workflow document as text.",
    )

    @model_validator(mode="after")
    def _normalize_document(self) -> "WorkflowEditorRequest":
        if self.document is not None:
            return self

        if not self.yaml_text or not self.yaml_text.strip():
            raise ValueError("Workflow editor request must include document or yaml_text.")

        parsed = yaml.safe_load(self.yaml_text)
        if not isinstance(parsed, dict):
            raise ValueError("Workflow YAML must deserialize to a mapping.")
        self.document = parsed
        return self


class WorkflowEditorResponse(BaseModel):
    """Workflow editor payload with raw YAML and parsed metadata."""

    name: str
    path: str
    yaml_text: str
    document: dict[str, Any] = Field(default_factory=dict)
    step_count: int = 0


class WorkflowValidationResponse(BaseModel):
    """Validation result for a workflow document."""

    valid: bool = True
    name: str
    step_count: int = 0
    yaml_text: str


class RunSummaryModel(BaseModel):
    """Lightweight summary of a single workflow run for list views.

    Attributes:
        filename: JSON log filename on disk.
        run_id: Unique run identifier.
        workflow_name: Name of the executed workflow.
        status: Terminal status string.
        success_rate: Fraction of steps that succeeded (0.0--1.0).
        total_duration_ms: Total wall-clock time in milliseconds.
        step_count: Number of steps executed.
        failed_step_count: Number of steps that failed.
        start_time: ISO-8601 start timestamp.
        end_time: ISO-8601 end timestamp.
        evaluation_score: Weighted evaluation score, if scored.
        evaluation_grade: Letter grade (A--F), if scored.
    """

    filename: str
    run_id: str | None = None
    workflow_name: str | None = None
    status: str | None = None
    success_rate: float | None = None
    total_duration_ms: float | None = None
    step_count: int | None = None
    failed_step_count: int | None = None
    start_time: str | None = None
    end_time: str | None = None
    evaluation_score: float | None = None
    evaluation_grade: str | None = None


class RunsSummaryResponse(BaseModel):
    """Aggregate statistics across all (or filtered) workflow runs.

    Attributes:
        total_runs: Total number of runs found.
        success: Count of runs with ``SUCCESS`` status.
        failed: Count of runs with ``FAILED`` status.
        avg_duration_ms: Mean duration in milliseconds, or None.
        workflows: Distinct workflow names seen.
    """

    total_runs: int = 0
    success: int = 0
    failed: int = 0
    avg_duration_ms: float | None = None
    workflows: list[str] = []


class WorkflowEvaluationRequest(BaseModel):
    """Evaluation settings nested within :class:`WorkflowRunRequest`.

    Controls whether and how the workflow result is scored after execution.

    Attributes:
        enabled: If True, trigger post-execution evaluation scoring.
        enforce_hard_gates: If True, hard-gate failures force grade ``F``.
        dataset_source: Where to load the evaluation dataset from.
        dataset_id: Repository dataset ID or local dataset reference.
        local_dataset_path: Explicit filesystem path for local datasets.
        sample_index: Zero-based index of the sample within the dataset.
        rubric: Rubric name override (deprecated, use ``rubric_id``).
        rubric_id: Rubric identifier override for scoring.
    """

    enabled: bool = False
    enforce_hard_gates: bool = True
    dataset_source: Literal["none", "repository", "local"] = "none"
    dataset_id: str | None = None
    local_dataset_path: str | None = None
    sample_index: int = Field(default=0, ge=0)
    rubric: str | None = None
    rubric_id: str | None = None


class EvaluationDatasetOption(BaseModel):
    """A single dataset option surfaced in the evaluation dataset picker UI.

    Attributes:
        id: Unique dataset identifier (path or registry ID).
        name: Human-readable display name.
        source: Origin of the dataset (``"repository"`` or ``"local"``).
        description: Brief description of the dataset contents.
        sample_count: Number of samples, or None if unknown.
    """

    id: str
    name: str
    source: Literal["repository", "local"]
    description: str = ""
    sample_count: int | None = None


class EvaluationSetOption(BaseModel):
    """A predefined evaluation set grouping multiple datasets together.

    Attributes:
        id: Unique evaluation set identifier.
        name: Human-readable display name.
        description: Summary of the set's purpose or scope.
        datasets: List of dataset IDs included in this set.
    """

    id: str
    name: str
    description: str = ""
    datasets: list[str] = []


class ListEvaluationDatasetsResponse(BaseModel):
    """Response for ``GET /api/eval/datasets`` listing all dataset options.

    Attributes:
        repository: Datasets available from benchmark registries.
        local: Datasets available as local JSON files.
        eval_sets: Predefined evaluation sets from configuration.
    """

    repository: list[EvaluationDatasetOption] = []
    local: list[EvaluationDatasetOption] = []
    eval_sets: list[EvaluationSetOption] = []
