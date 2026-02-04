"""Integration tests for workflow execution."""

from pathlib import Path

import pytest
import yaml

from multiagent_workflows.core.workflow_engine import WorkflowEngine


@pytest.mark.asyncio
async def test_fullstack_workflow_integration(
    mock_model_manager, sample_requirements, monkeypatch, tmp_path
):
    """Execute fullstack workflow end-to-end with mocked model calls."""
    # Avoid writing logs into the repo during test runs.
    monkeypatch.chdir(tmp_path)

    config_path = Path(__file__).resolve().parents[1] / "config" / "workflows.yaml"
    with config_path.open("r", encoding="utf-8") as f:
        workflows_config = yaml.safe_load(f)

    engine = WorkflowEngine(
        model_manager=mock_model_manager,
        evaluator=None,
        config=workflows_config,
    )

    result = await engine.execute_workflow(
        workflow_name="fullstack_generation",
        inputs={"requirements": sample_requirements},
    )

    assert result.success is True
    assert result.outputs
    assert "documentation" in result.outputs
    assert "readme" in result.outputs["documentation"]

    # Ensure key step artifacts are present in step results.
    assert "requirements_parsing" in result.step_results
    assert "architecture_design" in result.step_results
    assert "backend_generation" in result.step_results
    assert "frontend_generation" in result.step_results
    assert "test_generation" in result.step_results

    # Verify logs were exported.
    logs_dir = tmp_path / "evaluation" / "results" / "logs"
    assert logs_dir.exists()
    assert any(logs_dir.glob("*.json"))
    assert any(logs_dir.glob("*.md"))
