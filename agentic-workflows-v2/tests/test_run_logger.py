"""Tests for workflow run logger record shaping."""

import json
import pytest

from agentic_v2.contracts import StepStatus, WorkflowResult
from agentic_v2.workflows.run_logger import RunLogger, build_run_record


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


def test_summary_ignores_non_run_json_artifacts(tmp_path):
    logger = RunLogger(runs_dir=tmp_path)

    valid = build_run_record(_result())
    (tmp_path / "20260222T120000Z_test_workflow_success.json").write_text(
        json.dumps(valid),
        encoding="utf-8",
    )

    # Utility artifact (not a run record) should not crash summary().
    (tmp_path / "provider_limits.json").write_text(
        json.dumps({"checked": {"openai": {"ok": True}}}),
        encoding="utf-8",
    )

    summary = logger.summary()

    assert summary["total_runs"] == 1
    assert summary["success"] == 1
    assert summary["failed"] == 0
    assert summary["workflows"] == ["test_workflow"]
