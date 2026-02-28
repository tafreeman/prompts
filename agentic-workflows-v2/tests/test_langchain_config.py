"""Tests for workflow config loader."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from agentic_v2.langchain.config import (
    WorkflowConfig,
    list_workflows,
    load_workflow_config,
)


def _write_workflow(tmp_path: Path, name: str, data: dict) -> None:
    """Helper to write a workflow YAML file."""
    (tmp_path / f"{name}.yaml").write_text(yaml.dump(data))


class TestLoadWorkflowConfig:
    """Tests for load_workflow_config."""

    def test_load_existing_workflow(self, tmp_path: Path) -> None:
        """Loading a valid YAML returns WorkflowConfig."""
        data = {
            "name": "test-workflow",
            "description": "A test workflow",
            "steps": [
                {
                    "name": "step1",
                    "agent": "coder",
                    "description": "Write code",
                    "depends_on": [],
                    "inputs": {"code": "hello"},
                    "outputs": {"result": "output"},
                }
            ],
        }
        _write_workflow(tmp_path, "test-workflow", data)

        config = load_workflow_config("test-workflow", definitions_dir=tmp_path)
        assert isinstance(config, WorkflowConfig)
        assert config.name == "test-workflow"
        assert config.description == "A test workflow"
        assert len(config.steps) == 1
        assert config.steps[0].name == "step1"
        assert config.steps[0].agent == "coder"

    def test_load_nonexistent_raises_file_not_found(self, tmp_path: Path) -> None:
        """Missing workflow raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="not found"):
            load_workflow_config("nonexistent", definitions_dir=tmp_path)

    def test_invalid_name_raises_value_error(self) -> None:
        """Name with path separators raises ValueError."""
        with pytest.raises(ValueError, match="Invalid workflow name"):
            load_workflow_config("../../etc/passwd")

    def test_path_traversal_in_name_rejected(self) -> None:
        """Path traversal characters are rejected."""
        with pytest.raises(ValueError, match="Invalid workflow name"):
            load_workflow_config("../secret")

    def test_yml_extension_fallback(self, tmp_path: Path) -> None:
        """Tries .yaml then .yml extension."""
        data = {"name": "my-workflow", "steps": []}
        (tmp_path / "my-workflow.yml").write_text(yaml.dump(data))

        config = load_workflow_config("my-workflow", definitions_dir=tmp_path)
        assert config.name == "my-workflow"

    def test_full_step_parsing(self, tmp_path: Path) -> None:
        """Step with all fields is correctly parsed."""
        data = {
            "steps": [
                {
                    "name": "complex-step",
                    "agent": "architect",
                    "description": "Design system",
                    "depends_on": ["step0"],
                    "inputs": {"x": "1"},
                    "outputs": {"y": "2"},
                    "when": "${inputs.enabled}",
                    "loop_until": "${steps.complex-step.outputs.done}",
                    "loop_max": 5,
                    "tools": ["file_read", "code_analyze"],
                    "model_override": "gh:openai/gpt-4o",
                }
            ],
        }
        _write_workflow(tmp_path, "full-step", data)
        config = load_workflow_config("full-step", definitions_dir=tmp_path)

        step = config.steps[0]
        assert step.name == "complex-step"
        assert step.when == "${inputs.enabled}"
        assert step.loop_until == "${steps.complex-step.outputs.done}"
        assert step.loop_max == 5
        assert step.tools == ["file_read", "code_analyze"]
        assert step.model_override == "gh:openai/gpt-4o"

    def test_step_without_name_skipped(self, tmp_path: Path) -> None:
        """Steps missing 'name' are silently skipped."""
        data = {
            "steps": [
                {"agent": "coder"},  # no name
                {"name": "valid", "agent": "coder"},
            ],
        }
        _write_workflow(tmp_path, "partial", data)
        config = load_workflow_config("partial", definitions_dir=tmp_path)
        assert len(config.steps) == 1
        assert config.steps[0].name == "valid"


class TestParseEvaluation:
    """Tests for evaluation section parsing."""

    def test_evaluation_section_parsed(self, tmp_path: Path) -> None:
        """Evaluation criteria are correctly parsed."""
        data = {
            "steps": [],
            "evaluation": {
                "rubric_id": "test-rubric",
                "criteria": [
                    {
                        "name": "quality",
                        "definition": "Code quality",
                        "weight": 0.8,
                        "critical_floor": 0.5,
                    },
                ],
            },
        }
        _write_workflow(tmp_path, "with-eval", data)
        config = load_workflow_config("with-eval", definitions_dir=tmp_path)

        assert config.evaluation is not None
        assert config.evaluation.rubric_id == "test-rubric"
        assert len(config.evaluation.criteria) == 1
        assert config.evaluation.criteria[0].name == "quality"
        assert config.evaluation.criteria[0].weight == 0.8

    def test_no_evaluation_section(self, tmp_path: Path) -> None:
        """Missing evaluation section results in None."""
        data = {"steps": []}
        _write_workflow(tmp_path, "no-eval", data)
        config = load_workflow_config("no-eval", definitions_dir=tmp_path)
        assert config.evaluation is None


class TestListWorkflows:
    """Tests for list_workflows."""

    def test_lists_yaml_files(self, tmp_path: Path) -> None:
        """Lists .yaml and .yml stems."""
        (tmp_path / "alpha.yaml").write_text("name: alpha")
        (tmp_path / "beta.yml").write_text("name: beta")
        (tmp_path / "readme.md").write_text("# Readme")

        result = list_workflows(definitions_dir=tmp_path)
        assert "alpha" in result
        assert "beta" in result
        assert "readme" not in result

    def test_empty_directory_returns_empty(self, tmp_path: Path) -> None:
        """Empty dir returns []."""
        result = list_workflows(definitions_dir=tmp_path)
        assert result == []

    def test_nonexistent_directory_returns_empty(self, tmp_path: Path) -> None:
        """Non-existent dir returns []."""
        result = list_workflows(definitions_dir=tmp_path / "nonexistent")
        assert result == []

    def test_sorted_order(self, tmp_path: Path) -> None:
        """Results are sorted alphabetically."""
        (tmp_path / "zeta.yaml").write_text("name: zeta")
        (tmp_path / "alpha.yaml").write_text("name: alpha")
        (tmp_path / "mid.yaml").write_text("name: mid")

        result = list_workflows(definitions_dir=tmp_path)
        assert result == ["alpha", "mid", "zeta"]
