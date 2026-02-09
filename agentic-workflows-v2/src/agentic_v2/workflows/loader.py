"""Workflow loader for YAML workflow definitions.

Loads YAML workflow files and converts them to executable DAG objects.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from ..engine.dag import DAG
from ..engine.step import StepDefinition


@dataclass
class WorkflowInput:
    """Input parameter definition for a workflow."""

    name: str
    type: str = "string"
    description: str = ""
    default: Any = None
    required: bool = True
    enum: list[str] | None = None


@dataclass
class WorkflowOutput:
    """Output definition for a workflow."""

    name: str
    from_expr: str
    optional: bool = False


@dataclass
class WorkflowDefinition:
    """Parsed workflow definition from YAML."""

    name: str
    description: str = ""
    version: str = "1.0"
    inputs: dict[str, WorkflowInput] = field(default_factory=dict)
    outputs: dict[str, WorkflowOutput] = field(default_factory=dict)
    dag: DAG = field(default_factory=lambda: DAG(name="unnamed"))


class WorkflowLoadError(Exception):
    """Raised when workflow loading fails."""

    pass


class WorkflowLoader:
    """Load workflow definitions from YAML files.

    Usage:
        loader = WorkflowLoader()
        workflow = loader.load("code_review")
        dag = workflow.dag
    """

    def __init__(self, definitions_dir: Path | None = None):
        """Initialize the loader.

        Args:
            definitions_dir: Directory containing workflow YAML files.
                           Defaults to workflows/definitions/ in package.
        """
        if definitions_dir is None:
            # Default to package definitions directory
            definitions_dir = Path(__file__).parent / "definitions"
        self.definitions_dir = Path(definitions_dir)
        self._cache: dict[str, WorkflowDefinition] = {}

    def load(self, name: str, use_cache: bool = True) -> WorkflowDefinition:
        """Load a workflow by name.

        Args:
            name: Workflow name (without .yaml extension)
            use_cache: Whether to use cached definition

        Returns:
            Parsed WorkflowDefinition

        Raises:
            WorkflowLoadError: If workflow cannot be loaded
        """
        if use_cache and name in self._cache:
            return self._cache[name]

        # Find the YAML file
        yaml_path = self.definitions_dir / f"{name}.yaml"
        if not yaml_path.exists():
            yaml_path = self.definitions_dir / f"{name}.yml"

        if not yaml_path.exists():
            available = self.list_workflows()
            raise WorkflowLoadError(
                f"Workflow '{name}' not found in {self.definitions_dir}. "
                f"Available: {available}"
            )

        workflow = self._parse_file(yaml_path)

        if use_cache:
            self._cache[name] = workflow

        return workflow

    def load_file(self, path: Path) -> WorkflowDefinition:
        """Load a workflow from a specific file path."""
        if not path.exists():
            raise WorkflowLoadError(f"Workflow file not found: {path}")
        return self._parse_file(path)

    def list_workflows(self) -> list[str]:
        """List all available workflow names."""
        if not self.definitions_dir.exists():
            return []

        workflows = []
        for path in self.definitions_dir.iterdir():
            if path.suffix in (".yaml", ".yml"):
                workflows.append(path.stem)
        return sorted(workflows)

    def clear_cache(self) -> None:
        """Clear the workflow cache."""
        self._cache.clear()

    def _parse_file(self, path: Path) -> WorkflowDefinition:
        """Parse a YAML workflow file."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise WorkflowLoadError(f"Invalid YAML in {path}: {e}")

        if not isinstance(data, dict):
            raise WorkflowLoadError(f"Workflow must be a YAML mapping: {path}")

        return self._parse_definition(data, path.stem)

    def _parse_definition(
        self, data: dict[str, Any], default_name: str
    ) -> WorkflowDefinition:
        """Parse workflow definition from dict."""
        name = data.get("name", default_name)
        description = data.get("description", "")
        version = data.get("version", "1.0")

        # Parse inputs
        inputs = {}
        for input_name, input_def in data.get("inputs", {}).items():
            if isinstance(input_def, dict):
                inputs[input_name] = WorkflowInput(
                    name=input_name,
                    type=input_def.get("type", "string"),
                    description=input_def.get("description", ""),
                    default=input_def.get("default"),
                    required=input_def.get("required", True),
                    enum=input_def.get("enum"),
                )
            else:
                # Simple value is the default
                inputs[input_name] = WorkflowInput(
                    name=input_name,
                    default=input_def,
                    required=False,
                )

        # Parse outputs
        outputs = {}
        for output_name, output_def in data.get("outputs", {}).items():
            if isinstance(output_def, dict):
                outputs[output_name] = WorkflowOutput(
                    name=output_name,
                    from_expr=str(output_def.get("from", "")),
                    optional=output_def.get("optional", False),
                )
            else:
                outputs[output_name] = WorkflowOutput(
                    name=output_name,
                    from_expr=str(output_def),
                )

        # Parse steps into DAG
        dag = DAG(name=name, description=description)

        for step_data in data.get("steps", []):
            step = self._parse_step(step_data)
            dag.add(step)

        return WorkflowDefinition(
            name=name,
            description=description,
            version=version,
            inputs=inputs,
            outputs=outputs,
            dag=dag,
        )

    def _parse_step(self, data: dict[str, Any]) -> StepDefinition:
        """Parse a step definition from dict."""
        name = data.get("name")
        if not name:
            raise WorkflowLoadError("Step must have a 'name' field")

        # Build input/output mappings
        input_mapping = {}
        for key, value in data.get("inputs", {}).items():
            if isinstance(value, str):
                input_mapping[key] = value

        output_mapping = {}
        for key, value in data.get("outputs", {}).items():
            if isinstance(value, str):
                output_mapping[key] = value

        # Parse 'when' condition as string (will be evaluated at runtime)
        when_expr = data.get("when")
        when_func = None
        if when_expr:
            # Store expression for later evaluation
            pass  # Will be handled by step executor

        return StepDefinition(
            name=name,
            description=data.get("description", ""),
            depends_on=data.get("depends_on", []),
            input_mapping=input_mapping,
            output_mapping=output_mapping,
            metadata={
                "agent": data.get("agent"),
                "when_expr": when_expr,
            },
        )


def load_workflow(name: str, definitions_dir: Path | None = None) -> WorkflowDefinition:
    """Convenience function to load a workflow.

    Args:
        name: Workflow name
        definitions_dir: Optional custom definitions directory

    Returns:
        Parsed WorkflowDefinition
    """
    loader = WorkflowLoader(definitions_dir=definitions_dir)
    return loader.load(name)


def get_dag(name: str, definitions_dir: Path | None = None) -> DAG:
    """Convenience function to get just the DAG from a workflow.

    Args:
        name: Workflow name
        definitions_dir: Optional custom definitions directory

    Returns:
        The workflow's DAG
    """
    return load_workflow(name, definitions_dir).dag
