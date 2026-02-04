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
async def run(config: AgenticWorkflowsV2Config):
    """
    Main function to run the agentic-workflows-v2 setup.

    Args:
        config: The AgenticWorkflowsV2Config object.
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
