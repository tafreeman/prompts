"""Tests for the LangChain workflow engine.

Tests config loading, expression evaluation, and graph compilation
without requiring any API keys (tier-0 only).
"""

import json
import os
import pytest
from pathlib import Path

from agentic_v2.langchain.config import (
    WorkflowConfig,
    StepConfig,
    load_workflow_config,
    list_workflows,
)
from agentic_v2.langchain.expressions import (
    evaluate_condition,
    resolve_expression,
)
from agentic_v2.langchain.state import WorkflowState, initial_state
from agentic_v2.langchain.graph import compile_workflow


# ---------------------------------------------------------------------------
# Config loader tests
# ---------------------------------------------------------------------------


class TestConfigLoader:
    """Test YAML config loading."""

    def test_list_workflows(self):
        names = list_workflows()
        assert isinstance(names, list)
        assert len(names) > 0
        assert "code_review" in names

    def test_load_code_review(self):
        config = load_workflow_config("code_review")
        assert config.name == "code_review"
        assert config.version == "1.0"
        assert len(config.steps) >= 3
        assert "code_file" in config.inputs
        assert config.evaluation is not None
        assert len(config.evaluation.criteria) > 0

    def test_load_nonexistent_raises(self):
        with pytest.raises(FileNotFoundError):
            load_workflow_config("nonexistent_workflow_xyz")

    def test_step_config_fields(self):
        config = load_workflow_config("code_review")
        parse_step = next(s for s in config.steps if s.name == "parse_code")
        assert parse_step.agent == "tier0_parser"
        assert "file_path" in parse_step.inputs

    def test_step_dependencies(self):
        config = load_workflow_config("code_review")
        review_step = next(s for s in config.steps if s.name == "review_code")
        assert "style_check" in review_step.depends_on
        assert "complexity_analysis" in review_step.depends_on

    def test_conditional_step(self):
        config = load_workflow_config("code_review")
        summary_step = next(
            s for s in config.steps if s.name == "generate_summary"
        )
        assert summary_step.when is not None
        assert "review_depth" in summary_step.when

    def test_capabilities_parsed(self):
        config = load_workflow_config("code_review")
        assert "inputs" in config.capabilities
        assert "code_file" in config.capabilities["inputs"]

    def test_evaluation_criteria(self):
        config = load_workflow_config("code_review")
        assert config.evaluation is not None
        criteria_names = [c.name for c in config.evaluation.criteria]
        assert "correctness_rubric" in criteria_names
        assert "code_quality" in criteria_names


# ---------------------------------------------------------------------------
# Expression evaluator tests
# ---------------------------------------------------------------------------


class TestExpressions:
    """Test expression evaluation."""

    def test_simple_variable(self):
        state = {"inputs": {"code_file": "main.py"}}
        result = resolve_expression("${inputs.code_file}", state)
        assert result == "main.py"

    def test_nested_path(self):
        state = {
            "steps": {
                "parse_code": {
                    "outputs": {"ast": {"functions": ["foo", "bar"]}}
                }
            }
        }
        result = resolve_expression(
            "${steps.parse_code.outputs.ast}", state
        )
        assert result == {"functions": ["foo", "bar"]}

    def test_condition_true(self):
        state = {"inputs": {"review_depth": "standard"}}
        assert evaluate_condition(
            "${inputs.review_depth} != 'quick'", state
        )

    def test_condition_false(self):
        state = {"inputs": {"review_depth": "quick"}}
        assert not evaluate_condition(
            "${inputs.review_depth} != 'quick'", state
        )

    def test_in_operator(self):
        state = {
            "steps": {
                "review": {"outputs": {"status": "APPROVED"}}
            }
        }
        assert evaluate_condition(
            "${steps.review.outputs.status} in ['APPROVED', 'PASSED']",
            state,
        )

    def test_missing_path_returns_none(self):
        state = {"inputs": {}}
        result = resolve_expression("${inputs.nonexistent}", state)
        assert result is None

    def test_empty_expression_is_true(self):
        assert evaluate_condition("", {})
        assert evaluate_condition(None, {})


# ---------------------------------------------------------------------------
# State tests
# ---------------------------------------------------------------------------


class TestState:
    """Test state creation."""

    def test_initial_state(self):
        state = initial_state(workflow_inputs={"code_file": "test.py"})
        assert state["inputs"]["code_file"] == "test.py"
        assert state["messages"] == []
        assert state["errors"] == []
        assert state["steps"] == {}

    def test_initial_state_defaults(self):
        state = initial_state()
        assert state["inputs"] == {}
        assert state["context"] == {}


# ---------------------------------------------------------------------------
# Graph compilation tests (tier-0 only, no API keys)
# ---------------------------------------------------------------------------


class TestGraphCompilation:
    """Test graph compilation from config."""

    @pytest.mark.skipif(
        not os.environ.get("OPENAI_API_KEY"),
        reason="Requires OPENAI_API_KEY to instantiate LLM agents",
    )
    def test_compile_code_review(self):
        """Verify the code_review workflow compiles without errors."""
        config = load_workflow_config("code_review")
        graph = compile_workflow(config)
        assert graph is not None

    def test_empty_workflow_raises(self):
        config = WorkflowConfig(name="empty", steps=[])
        with pytest.raises(ValueError, match="no steps"):
            compile_workflow(config)

    def test_missing_dependency_raises(self):
        config = WorkflowConfig(
            name="bad_deps",
            steps=[
                StepConfig(
                    name="step1",
                    agent="tier0_parser",
                    depends_on=["nonexistent"],
                ),
            ],
        )
        with pytest.raises(ValueError, match="unknown step"):
            compile_workflow(config)

    def test_tier0_only_workflow_runs(self):
        """A workflow with only tier-0 steps should execute end-to-end."""
        config = WorkflowConfig(
            name="test_tier0",
            steps=[
                StepConfig(
                    name="parse",
                    agent="tier0_parser",
                    inputs={"file_path": "${inputs.code_file}"},
                    outputs={"parsed_ast": "ast_result"},
                ),
            ],
            inputs={},
        )
        graph = compile_workflow(config)
        state = initial_state(workflow_inputs={"code_file": "nonexistent.py"})
        state["context"]["inputs"] = state["inputs"]
        result = graph.invoke(state)
        assert "parse" in result["steps"]
        assert result["steps"]["parse"]["status"] == "success"
