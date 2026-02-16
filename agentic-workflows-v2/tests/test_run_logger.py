"""Tests for workflow run logger record shaping."""

import pytest

from agentic_v2.contracts import StepStatus, WorkflowResult
from agentic_v2.workflows.run_logger import build_run_record


def _result() -> WorkflowResult:
    return WorkflowResult(
        workflow_id="wf-test-1",
        workflow_name="test_workflow",
        overall_status=StepStatus.SUCCESS,
        steps=[],
        final_output={},
    )


def test_build_run_record_score_falls_back_to_success_rate():
    result = _result()

    record = build_run_record(result)

    assert "score" in record
    assert record["score"] == result.success_rate


def test_build_run_record_score_uses_evaluation_weighted_score():
    result = _result()

    record = build_run_record(
        result,
        extra={"evaluation": {"weighted_score": 87.5, "overall_score": 71.0}},
    )

    assert record["score"] == pytest.approx(87.5)
