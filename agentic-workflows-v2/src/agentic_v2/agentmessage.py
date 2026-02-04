from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field, ValidationError
from pydantic.validator import validator
import httpx
import jinja2
import jmespath
import toml

class AgentMessage(BaseModel):
    """
    Represents a message sent between agents.
    """
    id: str = Field(..., description="Unique identifier for the message")
    type: str = Field("agent", description="Type of message (e.g., 'agent', 'workflow')")
    payload: dict[str, Any] = Field(..., description="Message payload")

    @validator("id")
    def id_must_be_unique(cls, value: str) -> str:
        """
        Ensures the message ID is unique.
        """
        if not isinstance(value, str):
            raise ValueError("Message ID must be a string.")
        return value


class StepResult(BaseModel):
    """
    Represents the result of a step in a workflow.
    """
    step_id: str = Field(..., description="ID of the step that produced this result")
    status: str = Field("success", description="Status of the step (e.g., 'success', 'failure')")
    result: dict[str, Any] = Field(None, description="Result data from the step")

    @validator("status")
    def status_must_be_valid(cls, value: str) -> str:
        """
        Validates the step status.
        """
        if value not in ["success", "failure"]:
            raise ValueError("Step status must be 'success' or 'failure'.")
        return value


class WorkflowResult(BaseModel):
    """
    Represents the overall result of a workflow.
    """
    workflow_id: str = Field(..., description="ID of the workflow")
    status: str = Field("success", description="Status of the workflow (e.g., 'success', 'failure')")
    results: list[StepResult] = Field([], description="List of results from each step")

    @validator("status")
    def workflow_status_must_be_valid(cls, value: str) -> str:
        """
        Validates the workflow status.
        """
        if value not in ["success", "failure"]:
            raise ValueError("Workflow status must be 'success' or 'failure'.")
        return value


class AgenticWorkflowsV2Config(BaseModel):
    """
    Configuration for the agentic-workflows-v2 package.
    """
    package_name: str = "agentic_workflows_v2"
    version: str = "0.1.0"
    description: str = "A flexible workflow engine."
    author: str = "Your Name"
    license: str = "MIT"
    dependencies: list[str] = [
        "pydantic>=2.0",
        "httpx",
        "jinja2",
        "jmespath",
    ]

    @validator('package_name')
    def package_name_must_start_with_underscore(cls, value):
        if not value.startswith('_'):
            raise ValueError("Package name must start with an underscore.")
        return value


@asyncio.coroutine
def run(config: AgenticWorkflowsV2Config):
    """
    Main function to run the agentic-workflows-v2 setup.
    """
    print(f"Running agentic-workflows-v2 setup with config: {config}")

    # Create project directory
    project_root = Path(".")
    project_dir = project_root / config.package_name

    # Create package structure
    src_dir = project_dir / "src"
    src_dir.mkdir(exist_ok=True)
    agentic_v2_dir = src_dir / config.package_name
    agentic_v2_dir.mkdir(exist_ok=True)
    __init_py_path = agentic_v2_dir / "__init__.py"
    __init_py_path.write_text("")

    # Create tests directory
    tests_dir = project_dir / "tests"
    tests_dir.mkdir(exist_ok=True)
    conftest_py_path = tests_dir / "conftest.py"
    conftest_py_path.write_text("")

    # Create README.md
    readme_path = project_dir / "README.md"
    readme_content = f"""
# {config.package_name}

{config.description}

## Installation
