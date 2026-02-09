"""Message contracts for agent communication.

Enhanced with Pydantic v2 features:
- Computed properties for common checks
- Field validators for data quality
- Discriminated unions for polymorphic types
- Rich __repr__ for debugging
- Efficient serialization (exclude_none)
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import (BaseModel, ConfigDict, Field, computed_field,
                      field_validator)


class MessageType(str, Enum):
    """Type of message in the agent workflow."""

    TASK = "task"
    RESPONSE = "response"
    ERROR = "error"
    STATUS = "status"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"


class StepStatus(str, Enum):
    """Status of a workflow step execution."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    RETRYING = "retrying"


class AgentMessage(BaseModel):
    """Message exchanged between agents and orchestrator.

    Design improvements:
    - Discriminated union via message_type for polymorphic serialization
    - Auto-timestamps with timezone awareness
    - Computed properties for common checks
    - Content truncation helper for logging
    """

    model_config = ConfigDict(
        use_enum_values=False,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        extra="forbid",
    )

    message_type: MessageType = Field(
        description="Type of message for discriminated union"
    )
    role: str = Field(
        description="Agent role (e.g., 'coder', 'reviewer', 'orchestrator')",
        min_length=1,
        max_length=100,
    )
    content: str = Field(
        description="Message content (prompt, response, error details)", min_length=1
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context (model, tier, tokens, etc.)",
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp of message creation",
    )
    correlation_id: Optional[str] = Field(
        default=None, description="ID to correlate related messages across workflow"
    )

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Ensure role is lowercase and alphanumeric."""
        cleaned = v.lower().strip()
        if not cleaned.replace("_", "").replace("-", "").isalnum():
            raise ValueError(f"Role must be alphanumeric (with _ or -), got: {v}")
        return cleaned

    @computed_field
    @property
    def is_error(self) -> bool:
        """Check if this message represents an error."""
        return self.message_type == MessageType.ERROR

    @computed_field
    @property
    def is_tool_call(self) -> bool:
        """Check if this message is a tool invocation."""
        return self.message_type == MessageType.TOOL_CALL

    @computed_field
    @property
    def is_tool_result(self) -> bool:
        """Check if this message is a tool result."""
        return self.message_type == MessageType.TOOL_RESULT

    def truncated_content(self, max_length: int = 200) -> str:
        """Get truncated content for logging.

        Args:
            max_length: Maximum characters to return

        Returns:
            Truncated content with ellipsis if needed
        """
        if len(self.content) <= max_length:
            return self.content
        return self.content[: max_length - 3] + "..."

    def __repr__(self) -> str:
        """Rich representation for debugging."""
        content_preview = self.truncated_content(50)
        return (
            f"AgentMessage(type={self.message_type.value}, "
            f"role={self.role}, "
            f"content='{content_preview}', "
            f"timestamp={self.timestamp.isoformat()})"
        )


class StepResult(BaseModel):
    """Result of a single workflow step execution.

    Design improvements:
    - Computed duration property
    - Success rate tracking
    - Detailed error context
    - Retry tracking
    """

    model_config = ConfigDict(
        use_enum_values=False,
        validate_assignment=True,
        extra="allow",  # Allow extra fields for extensibility
    )

    step_name: str = Field(
        description="Unique identifier for this workflow step", min_length=1
    )
    status: StepStatus = Field(description="Execution status of the step")
    agent_role: Optional[str] = Field(
        default=None, description="Role of agent that executed this step"
    )
    tier: Optional[int] = Field(
        default=None,
        description="Model tier used (0=no LLM, 1=1-3B, 2=7-14B, 3=32B+)",
        ge=0,
        le=5,
    )
    model_used: Optional[str] = Field(
        default=None,
        description="Specific model identifier (e.g., 'ollama:phi4', 'gh:gpt-4o')",
    )
    input_data: dict[str, Any] = Field(
        default_factory=dict, description="Input parameters for this step"
    )
    output_data: dict[str, Any] = Field(
        default_factory=dict, description="Output/results from this step"
    )
    error: Optional[str] = Field(
        default=None, description="Error message if step failed"
    )
    error_type: Optional[str] = Field(
        default=None, description="Error class name for structured handling"
    )
    start_time: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp when step started",
    )
    end_time: Optional[datetime] = Field(
        default=None, description="UTC timestamp when step completed"
    )
    retry_count: int = Field(default=0, description="Number of retries attempted", ge=0)
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metrics (tokens, latency, cache hits, etc.)",
    )

    @computed_field
    @property
    def is_success(self) -> bool:
        """Check if step succeeded."""
        return self.status == StepStatus.SUCCESS

    @computed_field
    @property
    def is_failed(self) -> bool:
        """Check if step failed."""
        return self.status == StepStatus.FAILED

    @computed_field
    @property
    def is_complete(self) -> bool:
        """Check if step finished (success or failure)."""
        return self.status in (
            StepStatus.SUCCESS,
            StepStatus.FAILED,
            StepStatus.SKIPPED,
        )

    @computed_field
    @property
    def duration_ms(self) -> Optional[float]:
        """Calculate execution duration in milliseconds."""
        if self.end_time is None:
            return None
        delta = self.end_time - self.start_time
        return delta.total_seconds() * 1000

    def mark_complete(self, success: bool = True, error: Optional[str] = None) -> None:
        """Mark step as complete.

        Args:
            success: Whether step succeeded
            error: Optional error message if failed
        """
        self.end_time = datetime.now(timezone.utc)
        self.status = StepStatus.SUCCESS if success else StepStatus.FAILED
        if error:
            self.error = error

    def __repr__(self) -> str:
        """Rich representation for debugging."""
        duration_str = f"{self.duration_ms:.1f}ms" if self.duration_ms else "running"
        return (
            f"StepResult(name={self.step_name}, "
            f"status={self.status.value}, "
            f"duration={duration_str}, "
            f"retries={self.retry_count})"
        )


class WorkflowResult(BaseModel):
    """Complete result of a workflow execution.

    Design improvements:
    - Aggregate success rate
    - Total execution time
    - Step dependency tracking
    - Failure analysis
    """

    model_config = ConfigDict(
        use_enum_values=False, validate_assignment=True, extra="allow"
    )

    workflow_id: str = Field(
        description="Unique identifier for this workflow run", min_length=1
    )
    workflow_name: str = Field(description="Human-readable workflow name", min_length=1)
    steps: list[StepResult] = Field(
        default_factory=list, description="Ordered list of step results"
    )
    overall_status: StepStatus = Field(
        description="Aggregate status of entire workflow"
    )
    start_time: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp when workflow started",
    )
    end_time: Optional[datetime] = Field(
        default=None, description="UTC timestamp when workflow completed"
    )
    final_output: dict[str, Any] = Field(
        default_factory=dict, description="Final workflow output/artifacts"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Workflow-level metadata (costs, resource usage, etc.)",
    )

    @computed_field
    @property
    def total_duration_ms(self) -> Optional[float]:
        """Calculate total workflow duration in milliseconds."""
        if self.end_time is None:
            return None
        delta = self.end_time - self.start_time
        return delta.total_seconds() * 1000

    @computed_field
    @property
    def success_rate(self) -> float:
        """Calculate percentage of successful steps."""
        if not self.steps:
            return 0.0
        successful = sum(1 for step in self.steps if step.is_success)
        return (successful / len(self.steps)) * 100

    @computed_field
    @property
    def failed_steps(self) -> list[StepResult]:
        """Get list of failed steps."""
        return [step for step in self.steps if step.is_failed]

    @computed_field
    @property
    def total_retries(self) -> int:
        """Count total retry attempts across all steps."""
        return sum(step.retry_count for step in self.steps)

    def add_step(self, step: StepResult) -> None:
        """Add a step result to the workflow.

        Args:
            step: Step result to add
        """
        self.steps.append(step)
        # Update overall status based on step status
        if step.is_failed and self.overall_status != StepStatus.FAILED:
            self.overall_status = StepStatus.FAILED

    def mark_complete(self, success: bool = True) -> None:
        """Mark workflow as complete.

        Args:
            success: Whether workflow succeeded overall
        """
        self.end_time = datetime.now(timezone.utc)
        self.overall_status = StepStatus.SUCCESS if success else StepStatus.FAILED

    def __repr__(self) -> str:
        """Rich representation for debugging."""
        duration_str = (
            f"{self.total_duration_ms:.1f}ms" if self.total_duration_ms else "running"
        )
        return (
            f"WorkflowResult(name={self.workflow_name}, "
            f"status={self.overall_status.value}, "
            f"steps={len(self.steps)}, "
            f"success_rate={self.success_rate:.1f}%, "
            f"duration={duration_str})"
        )
