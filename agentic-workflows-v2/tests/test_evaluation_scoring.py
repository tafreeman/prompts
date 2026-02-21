"""Focused unit tests for agentic_v2.server.evaluation_scoring.

Covers the scoring-engine internals that were extracted into this module
during the refactoring described in REFACTORING_PLAN.md.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from agentic_v2.contracts import StepResult, StepStatus, WorkflowResult
from agentic_v2.server.evaluation_scoring import (
    HardGateResult,
    CriterionFloorResult,
    compute_hard_gates,
    validate_evaluation_payload_schema,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_result(
    status: StepStatus = StepStatus.SUCCESS,
    final_output: dict | None = None,
    step_statuses: list[StepStatus] | None = None,
) -> WorkflowResult:
    now = datetime.now(timezone.utc)
    result = WorkflowResult(
        workflow_id="wf-scoring",
        workflow_name="test_workflow",
        overall_status=status,
        start_time=now,
        end_time=now,
        final_output=final_output or {"summary": "ok"},
    )
    for st in step_statuses or [StepStatus.SUCCESS]:
        result.add_step(
            StepResult(
                step_name="step",
                status=st,
                input_data={},
                output_data={},
                start_time=now,
                end_time=now,
            )
        )
    return result


def _valid_payload() -> dict:
    """Return a minimal schema-valid evaluation payload."""
    return {
        "rubric_id": "workflow_default",
        "rubric_version": "1.0",
        "criteria": [
            {
                "criterion": "correctness",
                "raw_score": 80.0,
                "normalized_score": 80.0,
                "weight": 0.5,
                "formula_id": "linear",
                "score": 80.0,
            }
        ],
        "overall_score": 80.0,
        "weighted_score": 40.0,
        "grade": "B",
        "passed": True,
        "pass_threshold": 70.0,
        "step_scores": [],
    }


# ---------------------------------------------------------------------------
# HardGateResult
# ---------------------------------------------------------------------------


class TestHardGateResult:
    def test_all_passed_when_all_true(self) -> None:
        hgr = HardGateResult(
            required_outputs_present=True,
            overall_status_success=True,
            no_critical_step_failures=True,
            schema_contract_valid=True,
            dataset_workflow_compatible=True,
        )
        assert hgr.all_passed is True

    def test_all_passed_false_when_one_fails(self) -> None:
        hgr = HardGateResult(
            required_outputs_present=False,
            overall_status_success=True,
            no_critical_step_failures=True,
            schema_contract_valid=True,
            dataset_workflow_compatible=True,
        )
        assert hgr.all_passed is False

    def test_failures_lists_failed_fields(self) -> None:
        hgr = HardGateResult(
            required_outputs_present=False,
            overall_status_success=False,
            no_critical_step_failures=True,
            schema_contract_valid=True,
            dataset_workflow_compatible=True,
        )
        failures = hgr.failures
        assert "required_outputs_present" in failures
        assert "overall_status_success" in failures
        assert len(failures) == 2

    def test_failures_empty_when_all_pass(self) -> None:
        hgr = HardGateResult(
            required_outputs_present=True,
            overall_status_success=True,
            no_critical_step_failures=True,
            schema_contract_valid=True,
            dataset_workflow_compatible=True,
        )
        assert hgr.failures == []


# ---------------------------------------------------------------------------
# CriterionFloorResult
# ---------------------------------------------------------------------------


class TestCriterionFloorResult:
    def test_stores_fields(self) -> None:
        cfr = CriterionFloorResult(
            criterion="correctness",
            floor=60.0,
            normalized_score=45.0,
        )
        assert cfr.criterion == "correctness"
        assert cfr.floor == 60.0
        assert cfr.normalized_score == 45.0


# ---------------------------------------------------------------------------
# validate_evaluation_payload_schema
# ---------------------------------------------------------------------------


class TestValidateEvaluationPayloadSchema:
    def test_valid_payload_passes(self) -> None:
        ok, errors = validate_evaluation_payload_schema(_valid_payload())
        assert ok is True
        assert errors == []

    def test_non_dict_payload_fails(self) -> None:
        ok, errors = validate_evaluation_payload_schema("not-a-dict")  # type: ignore[arg-type]
        assert ok is False
        assert any("mapping" in e for e in errors)

    def test_missing_required_field(self) -> None:
        payload = _valid_payload()
        del payload["rubric_id"]
        ok, errors = validate_evaluation_payload_schema(payload)
        assert ok is False
        assert any("rubric_id" in e for e in errors)

    def test_wrong_type_for_overall_score(self) -> None:
        payload = _valid_payload()
        payload["overall_score"] = "eighty"  # should be numeric
        ok, errors = validate_evaluation_payload_schema(payload)
        assert ok is False
        assert any("overall_score" in e for e in errors)

    def test_criterion_missing_key(self) -> None:
        payload = _valid_payload()
        del payload["criteria"][0]["weight"]
        ok, errors = validate_evaluation_payload_schema(payload)
        assert ok is False
        assert any("weight" in e for e in errors)

    def test_empty_criteria_list_is_valid(self) -> None:
        payload = _valid_payload()
        payload["criteria"] = []
        ok, errors = validate_evaluation_payload_schema(payload)
        assert ok is True


# ---------------------------------------------------------------------------
# compute_hard_gates
# ---------------------------------------------------------------------------


class TestComputeHardGates:
    def test_success_result_passes_all_gates(self) -> None:
        result = _make_result(
            status=StepStatus.SUCCESS,
            final_output={"summary": "done"},
            step_statuses=[StepStatus.SUCCESS, StepStatus.SUCCESS],
        )
        hgr = compute_hard_gates(result)
        assert hgr.overall_status_success is True
        assert hgr.no_critical_step_failures is True
        assert hgr.schema_contract_valid is True  # no payload provided → default True
        assert hgr.dataset_workflow_compatible is True

    def test_failed_status_fails_gate(self) -> None:
        result = _make_result(status=StepStatus.FAILED)
        hgr = compute_hard_gates(result)
        assert hgr.overall_status_success is False

    def test_failed_step_fails_critical_gate(self) -> None:
        result = _make_result(
            status=StepStatus.SUCCESS,
            step_statuses=[StepStatus.SUCCESS, StepStatus.FAILED],
        )
        hgr = compute_hard_gates(result)
        assert hgr.no_critical_step_failures is False

    def test_schema_contract_validated_when_payload_provided(self) -> None:
        result = _make_result()
        bad_payload = {"rubric_id": "x"}  # missing most required fields
        hgr = compute_hard_gates(result, eval_payload=bad_payload)
        assert hgr.schema_contract_valid is False

    def test_schema_contract_valid_when_good_payload_provided(self) -> None:
        result = _make_result()
        hgr = compute_hard_gates(result, eval_payload=_valid_payload())
        assert hgr.schema_contract_valid is True

    def test_dataset_workflow_compatible_propagated(self) -> None:
        result = _make_result()
        hgr = compute_hard_gates(result, dataset_workflow_compatible=False)
        assert hgr.dataset_workflow_compatible is False
        assert hgr.all_passed is False

    def test_required_outputs_missing_fails_gate(self) -> None:
        from agentic_v2.workflows.loader import WorkflowOutput

        result = _make_result(final_output={"other_key": "value"})
        # Declare "summary" as a required output
        workflow_outputs = {
            "summary": WorkflowOutput(
                name="summary", from_expr="steps.last.summary", optional=False
            )
        }
        hgr = compute_hard_gates(result, workflow_outputs=workflow_outputs)
        # final_output has "other_key" but not "summary" → required output absent
        assert hgr.required_outputs_present is False
