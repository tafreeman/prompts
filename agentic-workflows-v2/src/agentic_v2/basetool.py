from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field, validator
from pydantic.validator import validator
import httpx
import jinja2
import jmespath
import toml

class BaseTool(BaseModel):
    """
    Abstract base class for all tools in the agentic-workflows-v2 system.
    """
    name: str
    description: str

    async def run(self, **kwargs: Any) -> Any:
        """
        Executes the tool's functionality.

        Args:
            **kwargs: Keyword arguments passed to the tool.

        Returns:
            The result of the tool's execution.
        """
        raise NotImplementedError("Subclasses must implement the run method.")


class ToolResult(BaseModel):
    """
    Represents the result of a tool's execution.
    """
    result: Any
    success: bool = True  # Defaults to success

    @classmethod
    def from_dict(cls, data: dict) -> "ToolResult":
        """
        Creates a ToolResult object from a dictionary.
        """
        result = cls(**data)
        if not result.success:
            result.result = data.get("error", "An error occurred")
        return result


class FileCopyTool(BaseTool):
    """
    A tool for copying files.
    """
    name: str = "file_copy"
    description: str = "Copies a file from one location to another."

    source: str = Field(..., description="Path to the source file.")
    destination: str = Field(..., description="Path to the destination file.")

    async def run(self, **kwargs: Any) -> ToolResult:
        """
        Copies the file from source to destination.
        """
        try:
            Path(self.destination).resolve().copy(Path(self.source).resolve())
            return ToolResult(result=self.destination.parent / self.destination.name)
        except Exception as e:
            return ToolResult(result=str(e), success=False)


class DirectoryCreateTool(BaseTool):
    """
    A tool for creating directories.
    """
    name: str = "directory_create"
    description: str = "Creates a directory."

    path: str = Field(..., description="Path to the directory to create.")

    async def run(self, **kwargs: Any) -> ToolResult:
        """
        Creates the directory.
        """
        try:
            Path(self.path).mkdir(parents=True, exist_ok=True)
            return ToolResult(result=self.path)
        except Exception as e:
            return ToolResult(result=str(e), success=False)


class JsonTransformTool(BaseTool):
    """
    A tool for transforming JSON data using JMESPath.
    """
    name: str = "json_transform"
    description: str = "Transforms JSON data using JMESPath."

    json_data: str = Field(..., description="The JSON data to transform.")
    jmespath_expression: str = Field(..., description="The JMESPath expression to use.")

    async def run(self, **kwargs: Any) -> ToolResult:
        """
        Transforms the JSON data using the JMESPath expression.
        """
        try:
            result = jmespath.search(self.jmespath_expression, self.json_data)
            return ToolResult(result=result)
        except Exception as e:
            return ToolResult(result=str(e), success=False)


class TemplateRenderTool(BaseTool):
    """
    A tool for rendering Jinja2 templates.
    """
    name: str = "template_render"
    description: str = "Renders a Jinja2 template with provided data."

    template_path: str = Field(..., description="Path to the Jinja2 template file.")
    data: dict = Field(..., description="Data to pass to the template.")

    async def run(self, **kwargs: Any) -> ToolResult:
        """
        Renders the template with the provided data.
        """
        try:
            template = jinja2.Template(open(self.template_path).read())
            result = template.render(self.data)
            return ToolResult(result=result)
        except Exception as e:
            return ToolResult(result=str(e), success=False)


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

    # Create package directory
    package_dir = project_dir / config.package_name
    package_dir.mkdir(parents=True, exist_ok=True)

    # Copy tools to package directory
    FileCopyTool.model_config = {
        "populate_by_name": True
    }
    DirectoryCreateTool.model_config = {
        "populate_by_name": True
    }
    JsonTransformTool.model_config = {
        "populate_by_name": True
    }
    TemplateRenderTool.model_config = {
        "populate_by_name": True
    }

    # Create a dummy config.toml file
    config_toml = toml.dumps(config.dict())
    config_path = package_dir / "config.toml"
    config_path.write_text(config_toml)

    # Create a dummy README.md file
    readme_content = f"""# {config.package_name}

{config.description}
"""
    readme_path = package_dir / "README.md"
    readme_path.write_text(readme_content)

    print(f"agentic-workflows-v2 package created successfully at: {project_dir}")
