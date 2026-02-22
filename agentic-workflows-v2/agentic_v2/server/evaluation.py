"""Dataset selection and scoring helpers for workflow evaluation runs.

This module is the backward-compatible orchestration surface. Heavy scoring
logic lives in ``evaluation_scoring.py`` and dataset loading/matching helpers
live in ``datasets.py``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..contracts import WorkflowResult
from ..workflows.loader import (
    WorkflowDefinition,
    WorkflowInput,
)
from .datasets import (
    _dataset_value_for_input,
    _extract_message_text,
    _is_empty_value,
    _load_eval_config,
    _materialize_file_input,
    _pick_first,
    adapt_sample_to_workflow_inputs,
    list_eval_sets,
    list_local_datasets,
    list_repository_datasets,
    load_local_dataset_sample,
    load_repository_dataset_sample,
    match_workflow_dataset,
    validate_required_inputs_present,
)
from .evaluation_scoring import (
    CriterionFloorResult,
    HardGateResult,
    _build_judge_criteria,
    _clamp,
    _compose_hybrid_score,
    _compute_criterion_score as _compute_criterion_score_impl,
    _extract_expected_text,
    _grade,
    _output_text,
    _resolve_rubric,
    _step_scores,
    _text_overlap_score,
    _tokenize,
    _validate_rubric_weights,
    compute_hard_gates,
    pass_threshold,
    score_workflow_result_impl,
    validate_evaluation_payload_schema,
)
from .judge import LLMJudge


def _compute_criterion_score(
    criterion: str,
    result: WorkflowResult,
    expected_text: str,
) -> float:
    """Compatibility wrapper retained for monkeypatch-based tests."""
    return _compute_criterion_score_impl(criterion, result, expected_text)


def score_workflow_result(
    result: WorkflowResult,
    *,
    dataset_meta: dict[str, Any] | None,
    dataset_sample: dict[str, Any] | None,
    rubric: str | None = None,
    workflow_definition: WorkflowDefinition | None = None,
    enforce_hard_gates: bool = True,
    judge: LLMJudge | None = None,
    hybrid_component_weights: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Produce criterion-level and aggregate scores for a workflow result."""
    return score_workflow_result_impl(
        result,
        dataset_meta=dataset_meta,
        dataset_sample=dataset_sample,
        rubric=rubric,
        workflow_definition=workflow_definition,
        enforce_hard_gates=enforce_hard_gates,
        judge=judge,
        hybrid_component_weights=hybrid_component_weights,
        compute_criterion_score_fn=_compute_criterion_score,
        match_workflow_dataset_fn=match_workflow_dataset,
    )

    no_floor_violations = len(floor_violations) == 0
    grade_capped = False
    if no_floor_violations is False and grade in {"A", "B", "C"}:
        grade = "D"
        grade_capped = True

    if hard_gates.all_passed is False and enforce_hard_gates:
        grade = "F"
        grade_capped = False

    passed = (weighted_score >= threshold) and no_floor_violations
    if enforce_hard_gates:
        passed = passed and hard_gates.all_passed

    payload["hard_gates"] = {
        "required_outputs_present": hard_gates.required_outputs_present,
        "overall_status_success": hard_gates.overall_status_success,
        "no_critical_step_failures": hard_gates.no_critical_step_failures,
        "schema_contract_valid": hard_gates.schema_contract_valid,
        "dataset_workflow_compatible": hard_gates.dataset_workflow_compatible,
    }
    payload["hard_gate_failures"] = hard_gates.failures
    payload["floor_violations"] = [
        {
            "criterion": violation.criterion,
            "floor": round(violation.floor, 4),
            "normalized_score": round(violation.normalized_score, 4),
        }
        for violation in floor_violations
    ]
    payload["grade_capped"] = grade_capped
    payload["grade"] = grade
    payload["passed"] = passed

    return payload


def _pick_first(sample: dict[str, Any], keys: list[str]) -> Any:
    nested_inputs = sample.get("inputs")
    nested_input = sample.get("input")
    for key in keys:
        if key in sample and sample[key] not in (None, ""):
            return sample[key]
        if isinstance(nested_inputs, dict) and key in nested_inputs and nested_inputs[key] not in (None, ""):
            return nested_inputs[key]
        if isinstance(nested_input, dict) and key in nested_input and nested_input[key] not in (None, ""):
            return nested_input[key]
        if key == "input" and isinstance(nested_input, str) and nested_input.strip():
            return nested_input
    return None


def _materialize_file_input(
    value: Any,
    *,
    input_name: str,
    run_id: str,
    artifacts_dir: Path,
) -> Any:
    if not isinstance(value, str):
        return value

    # Always materialize files under the controlled artifacts_dir.
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    artifacts_root = artifacts_dir.resolve()

    looks_python = any(marker in value for marker in ("def ", "class ", "import "))

    # If the value is clearly code, treat it as content, not as a path.
    if looks_python:
        suffix = ".py"
        file_path = artifacts_root / f"{run_id}_{input_name}{suffix}"
        file_path.write_text(value, encoding="utf-8")
        return str(file_path)

    # Otherwise, if the value looks like a path, attempt to interpret it as a
    # path relative to artifacts_dir, but prevent directory traversal.
    candidate: Path | None = None
    if any(sep in value for sep in ("/", "\\")) or value.endswith((".py", ".txt")):
        try:
            candidate = (artifacts_root / value).resolve()
            # Ensure the resolved candidate is within artifacts_root
            try:
                candidate.relative_to(artifacts_root)
                if candidate.is_file():
                    return str(candidate)
            except ValueError:
                # candidate is outside artifacts_root; ignore and treat as content
                candidate = None
        except Exception:
            candidate = None

    # Fallback: treat value as content and write it to a new file.
    suffix = ".py" if looks_python else ".txt"
    file_path = artifacts_root / f"{run_id}_{input_name}{suffix}"
    file_path.write_text(value, encoding="utf-8")
    return str(file_path)


def adapt_sample_to_workflow_inputs(
    workflow_inputs: dict[str, WorkflowInput],
    sample: dict[str, Any],
    *,
    run_id: str,
    artifacts_dir: Path,
) -> dict[str, Any]:
    """Map dataset sample fields onto workflow input schema."""
    if not isinstance(sample, dict):
        return {}

    adapted: dict[str, Any] = {}
    generic_text = _pick_first(
        sample,
        [
            "prompt",
            "task_description",
            "description",
            "body",
            "instruction",
            "input",
            "question",
            "query",
            "request",
            "issue_text",
            "content",
            "text",
            "code",
            "expected_output",
        ],
    )
    if generic_text in (None, ""):
        generic_text = _extract_message_text(sample)
    for name, definition in workflow_inputs.items():
        lowered = name.lower()
        explicit = sample.get(name)
        value = explicit

        if value in (None, ""):
            if "file" in lowered:
                value = _pick_first(
                    sample,
                    [
                        "code_file",
                        "file_path",
                        "path",
                        "source_path",
                        "code",
                        "body",
                        "prompt",
                        "task_description",
                    ],
                )
            elif "spec" in lowered or "requirement" in lowered:
                value = _pick_first(
                    sample,
                    [
                        "feature_spec",
                        "task_description",
                        "prompt",
                        "description",
                        "instruction",
                        "input",
                        "question",
                        "query",
                        "request",
                        "body",
                    ],
                )
                if value in (None, ""):
                    value = _extract_message_text(sample, preferred_roles=("user", "system", "assistant"))
            elif "tech_stack" in lowered and definition.type == "object":
                value = sample.get("tech_stack") or {
                    "frontend": "react",
                    "backend": "fastapi",
                    "database": "postgresql",
                }
            else:
                value = generic_text

        if value in (None, ""):
            continue

        if definition.type == "string":
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            if "file" in lowered:
                value = _materialize_file_input(
                    value,
                    input_name=name,
                    run_id=run_id,
                    artifacts_dir=artifacts_dir,
                )
        elif definition.type in {"object", "array"} and isinstance(value, str):
            try:
                value = json.loads(value)
            except Exception:
                value = {"value": value}

        adapted[name] = value

    return adapted

__all__ = [
    "CriterionFloorResult",
    "HardGateResult",
    "_build_judge_criteria",
    "_clamp",
    "_compose_hybrid_score",
    "_compute_criterion_score",
    "_dataset_value_for_input",
    "_extract_expected_text",
    "_extract_message_text",
    "_grade",
    "_is_empty_value",
    "_load_eval_config",
    "_materialize_file_input",
    "_output_text",
    "_pick_first",
    "_resolve_rubric",
    "_step_scores",
    "_text_overlap_score",
    "_tokenize",
    "_validate_rubric_weights",
    "adapt_sample_to_workflow_inputs",
    "compute_hard_gates",
    "list_eval_sets",
    "list_local_datasets",
    "list_repository_datasets",
    "load_local_dataset_sample",
    "load_repository_dataset_sample",
    "match_workflow_dataset",
    "pass_threshold",
    "score_workflow_result",
    "validate_evaluation_payload_schema",
    "validate_required_inputs_present",
    "WorkflowDefinition",
    "WorkflowInput",
    "Path",
]
