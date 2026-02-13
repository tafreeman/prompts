"""Dataset selection and scoring helpers for workflow evaluation runs."""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from ..contracts import StepStatus, WorkflowResult
from ..workflows.loader import (
    WorkflowCriterion,
    WorkflowDefinition,
    WorkflowInput,
    WorkflowOutput,
)
from .judge import JudgeCriterionDefinition, JudgeEvaluationResult, LLMJudge
from .normalization import adjust_for_sample_size, normalize_score
from .scoring_profiles import get_profile

logger = logging.getLogger(__name__)


def _resolve_project_root() -> Path:
    this_file = Path(__file__).resolve()
    # Support both layouts:
    # 1) <repo>/agentic_v2/server/evaluation.py
    # 2) <repo>/src/agentic_v2/server/evaluation.py
    candidates = [this_file.parents[2], this_file.parents[3]]
    for root in candidates:
        if (root / "agentic_v2").exists() and (root / "pyproject.toml").exists():
            return root
        if (root / "src" / "agentic_v2").exists() and (root / "pyproject.toml").exists():
            return root
    return this_file.parents[2]


def _resolve_eval_config_path(project_root: Path) -> Path:
    candidates = [
        project_root / "agentic_v2" / "config" / "defaults" / "evaluation.yaml",
        project_root / "src" / "agentic_v2" / "config" / "defaults" / "evaluation.yaml",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


_PROJECT_ROOT = _resolve_project_root()
_WORKSPACE_ROOT = _PROJECT_ROOT.parent
_EVAL_CONFIG_PATH = _resolve_eval_config_path(_PROJECT_ROOT)
_DEFAULT_WEIGHTS: dict[str, float] = {
    "correctness": 0.50,
    "code_quality": 0.25,
    "efficiency": 0.15,
    "documentation": 0.10,
}
_DEFAULT_PASS_THRESHOLD = 70.0
_DEFAULT_RUBRIC = "workflow_default"
_DEFAULT_RUBRIC_VERSION = "1.0"


@dataclass
class HardGateResult:
    """Hard-gate checks required before a run can pass scoring."""

    required_outputs_present: bool
    overall_status_success: bool
    no_critical_step_failures: bool
    schema_contract_valid: bool
    dataset_workflow_compatible: bool

    @property
    def all_passed(self) -> bool:
        return (
            self.required_outputs_present
            and self.overall_status_success
            and self.no_critical_step_failures
            and self.schema_contract_valid
            and self.dataset_workflow_compatible
        )

    @property
    def failures(self) -> list[str]:
        failed: list[str] = []
        if not self.required_outputs_present:
            failed.append("required_outputs_present")
        if not self.overall_status_success:
            failed.append("overall_status_success")
        if not self.no_critical_step_failures:
            failed.append("no_critical_step_failures")
        if not self.schema_contract_valid:
            failed.append("schema_contract_valid")
        if not self.dataset_workflow_compatible:
            failed.append("dataset_workflow_compatible")
        return failed


def compute_hard_gates(
    result: WorkflowResult,
    workflow_outputs: dict[str, WorkflowOutput] | None = None,
    eval_payload: dict[str, Any] | None = None,
    dataset_workflow_compatible: bool = True,
) -> HardGateResult:
    """Compute hard-gate pass/fail flags for a workflow run."""
    required_outputs = [
        output_name
        for output_name, output_def in (workflow_outputs or {}).items()
        if not output_def.optional
    ]

    unresolved_required = result.metadata.get("unresolved_required_outputs", [])
    unresolved_set = set(unresolved_required) if isinstance(unresolved_required, list) else set()
    required_output_values = result.final_output if isinstance(result.final_output, dict) else {}

    required_outputs_present = True
    for output_name in required_outputs:
        if output_name in unresolved_set:
            required_outputs_present = False
            break
        if required_output_values.get(output_name) is None:
            required_outputs_present = False
            break

    overall_status_success = result.overall_status == StepStatus.SUCCESS
    no_critical_step_failures = all(step.status != StepStatus.FAILED for step in result.steps)
    schema_contract_valid = True
    if eval_payload is not None:
        schema_contract_valid, _ = validate_evaluation_payload_schema(eval_payload)

    return HardGateResult(
        required_outputs_present=required_outputs_present,
        overall_status_success=overall_status_success,
        no_critical_step_failures=no_critical_step_failures,
        schema_contract_valid=schema_contract_valid,
        dataset_workflow_compatible=dataset_workflow_compatible,
    )


@dataclass
class CriterionFloorResult:
    """Represents a failed criterion floor requirement."""

    criterion: str
    floor: float
    normalized_score: float


def _clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, value))


def _load_eval_config() -> dict[str, Any]:
    if not _EVAL_CONFIG_PATH.exists():
        return {}
    try:
        with _EVAL_CONFIG_PATH.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data if isinstance(data, dict) else {}
    except Exception as exc:
        logger.warning("Failed to load evaluation config: %s", exc)
        return {}


def _scoring_weights() -> dict[str, float]:
    config = _load_eval_config()
    raw = (
        config.get("evaluation", {})
        .get("scoring", {})
        .get("weights", {})
    )
    if not isinstance(raw, dict):
        return dict(_DEFAULT_WEIGHTS)

    weights: dict[str, float] = {}
    for key, value in raw.items():
        try:
            weights[str(key)] = float(value)
        except Exception:
            continue
    if not weights:
        return dict(_DEFAULT_WEIGHTS)
    return weights


def pass_threshold() -> float:
    config = _load_eval_config()
    raw = (
        config.get("evaluation", {})
        .get("scoring", {})
        .get("pass_threshold", _DEFAULT_PASS_THRESHOLD)
    )
    try:
        return float(raw)
    except Exception:
        return _DEFAULT_PASS_THRESHOLD


def _resolve_rubric(
    workflow_definition: WorkflowDefinition | None,
    rubric_override: str | None,
) -> tuple[str, str, dict[str, float], dict[str, WorkflowCriterion]]:
    """Resolve rubric identity and scoring weights with workflow defaults."""
    base_weights = _scoring_weights()
    weights = dict(base_weights)
    criteria_by_name: dict[str, WorkflowCriterion] = {}

    workflow_rubric_id: str | None = None
    workflow_weights: dict[str, float] | None = None
    workflow_scoring_profile: str | None = None
    if workflow_definition is not None and workflow_definition.evaluation is not None:
        workflow_rubric_id = workflow_definition.evaluation.rubric_id
        workflow_weights = workflow_definition.evaluation.weights
        workflow_scoring_profile = workflow_definition.evaluation.scoring_profile
        criteria_by_name = {
            criterion.name: criterion
            for criterion in workflow_definition.evaluation.criteria
        }

    if workflow_scoring_profile:
        weights = dict(get_profile(workflow_scoring_profile).weights)

    # When workflow declares explicit criteria, scope default/profile weights to
    # that criterion set before applying overrides.
    if criteria_by_name:
        scoped_weights: dict[str, float] = {}
        for criterion_name in criteria_by_name:
            if criterion_name in weights:
                scoped_weights[criterion_name] = weights[criterion_name]
        weights = scoped_weights

    # Criteria-provided weights fill in defaults from profile/global set.
    for criterion_name, criterion in criteria_by_name.items():
        if criterion.weight is not None:
            weights[criterion_name] = criterion.weight

    if workflow_weights:
        _validate_rubric_weights(workflow_weights)
        weights.update(workflow_weights)

    _validate_rubric_weights(
        weights,
        known_criteria=set(criteria_by_name.keys()) if criteria_by_name else None,
    )

    rubric_id = rubric_override or workflow_rubric_id or _DEFAULT_RUBRIC
    version = str(_load_eval_config().get("version") or _DEFAULT_RUBRIC_VERSION)
    return rubric_id, version, weights, criteria_by_name


def _validate_rubric_weights(
    weights: dict[str, float],
    *,
    known_criteria: set[str] | None = None,
) -> None:
    """Validate rubric weights are usable and aligned to known criteria."""
    if not weights:
        raise ValueError("Rubric weights cannot be empty.")

    if known_criteria:
        unknown = sorted(set(weights.keys()) - known_criteria)
    else:
        unknown = []
    if unknown:
        raise ValueError(
            f"Rubric references unknown criteria: {', '.join(unknown)}. "
            f"Known criteria: {', '.join(sorted(known_criteria))}."
        )

    total = sum(weights.values())
    if any(value <= 0 for value in weights.values()):
        raise ValueError("Rubric weights must all be positive.")
    if abs(total - 1.0) > 0.01:
        raise ValueError(
            f"Rubric weights must sum to 1.0 (+/-0.01), got {total:.4f}."
        )


def _step_scores(result: WorkflowResult) -> list[dict[str, Any]]:
    """Produce lightweight per-step scores for event/log payloads."""
    scores: list[dict[str, Any]] = []
    for step in result.steps:
        if step.status == StepStatus.SUCCESS:
            score = 100.0
        elif step.status == StepStatus.SKIPPED:
            score = 0.0
        else:
            score = 0.0
        scores.append(
            {
                "step_name": step.step_name,
                "status": step.status.value,
                "score": score,
            }
        )
    return scores


def validate_evaluation_payload_schema(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    """Validate evaluation payload shape for schema hard-gate checks."""
    errors: list[str] = []
    if not isinstance(payload, dict):
        return False, ["payload must be a mapping"]

    required_fields: dict[str, tuple[type, ...]] = {
        "rubric_id": (str,),
        "rubric_version": (str,),
        "criteria": (list,),
        "overall_score": (int, float),
        "weighted_score": (int, float),
        "grade": (str,),
        "passed": (bool,),
        "pass_threshold": (int, float),
        "step_scores": (list,),
    }
    for field, expected_types in required_fields.items():
        value = payload.get(field)
        if value is None:
            errors.append(f"missing field: {field}")
            continue
        if not isinstance(value, expected_types):
            expected = ", ".join(t.__name__ for t in expected_types)
            errors.append(f"field '{field}' must be {expected}")

    criteria = payload.get("criteria")
    if isinstance(criteria, list):
        for idx, criterion in enumerate(criteria):
            if not isinstance(criterion, dict):
                errors.append(f"criteria[{idx}] must be an object")
                continue
            for key in (
                "criterion",
                "raw_score",
                "normalized_score",
                "weight",
                "formula_id",
                "score",
            ):
                if key not in criterion:
                    errors.append(f"criteria[{idx}] missing key: {key}")

    return len(errors) == 0, errors


def list_repository_datasets() -> list[dict[str, Any]]:
    """Return repository-backed dataset options."""
    options: list[dict[str, Any]] = []
    try:
        from tools.agents.benchmarks.datasets import BENCHMARK_DEFINITIONS

        for dataset_id, definition in BENCHMARK_DEFINITIONS.items():
            source = getattr(getattr(definition, "source", None), "value", "")
            if source not in {"huggingface", "github"}:
                continue
            options.append(
                {
                    "id": dataset_id,
                    "name": definition.name,
                    "source": "repository",
                    "description": definition.description,
                    "sample_count": definition.size,
                }
            )
        return sorted(options, key=lambda x: x["id"])
    except Exception as exc:
        logger.info("Repository benchmark definitions unavailable: %s", exc)

    fallback = (
        _load_eval_config()
        .get("evaluation", {})
        .get("datasets", {})
    )
    for dataset_id, cfg in fallback.items():
        if not isinstance(cfg, dict):
            continue
        if cfg.get("type") and cfg.get("url"):
            options.append(
                {
                    "id": str(dataset_id),
                    "name": str(dataset_id).replace("_", " ").title(),
                    "source": "repository",
                    "description": cfg.get("description", ""),
                    "sample_count": None,
                }
            )
    return sorted(options, key=lambda x: x["id"])


def _local_dataset_roots() -> list[Path]:
    candidates = [
        _PROJECT_ROOT / "tests" / "fixtures" / "datasets",
        _PROJECT_ROOT / "evaluation" / "datasets",
        _WORKSPACE_ROOT / "tools" / "agents" / "benchmarks" / "gold_standards",
    ]
    return [p for p in candidates if p.exists() and p.is_dir()]


def _safe_relative_id(path: Path) -> str:
    try:
        return path.relative_to(_WORKSPACE_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _estimate_sample_count(path: Path) -> int | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return len(data)
        if isinstance(data, dict):
            for key in ("tasks", "samples", "items"):
                value = data.get(key)
                if isinstance(value, list):
                    return len(value)
            return 1
    except Exception:
        return None
    return None


def list_local_datasets() -> list[dict[str, Any]]:
    """Return local JSON dataset options."""
    options: list[dict[str, Any]] = []
    for root in _local_dataset_roots():
        for json_path in sorted(root.rglob("*.json")):
            options.append(
                {
                    "id": _safe_relative_id(json_path),
                    "name": json_path.stem.replace("_", " "),
                    "source": "local",
                    "description": f"Local JSON dataset ({json_path.parent.name})",
                    "sample_count": _estimate_sample_count(json_path),
                }
            )
    dedup: dict[str, dict[str, Any]] = {}
    for option in options:
        dedup[option["id"]] = option
    return sorted(dedup.values(), key=lambda x: x["id"])


def _is_under_allowed_root(path: Path) -> bool:
    resolved = path.resolve()
    for root in _local_dataset_roots():
        try:
            resolved.relative_to(root.resolve())
            return True
        except ValueError:
            continue
    return False


def _resolve_local_dataset(dataset_ref: str) -> Path:
    """
    Resolve a local dataset reference to a JSON file path under an allowed root.

    The reference may be either:
      * an ID previously returned by list_local_datasets(), or
      * a workspace-relative path.

    In all cases the resolved path must point to a file under one of the
    directories returned by _local_dataset_roots(), otherwise a ValueError
    is raised.
    """
    ref_path = Path(dataset_ref)

    # First, treat the reference as a workspace-relative path and validate it.
    if not ref_path.is_absolute():
        candidate = (_WORKSPACE_ROOT / ref_path).resolve()
        if candidate.exists() and candidate.is_file() and _is_under_allowed_root(candidate):
            return candidate

    # Next, try to match against known local dataset IDs.
    for option in list_local_datasets():
        if option["id"] == dataset_ref:
            # option["id"] is produced by _safe_relative_id from a path under
            # one of the allowed roots, relative to _WORKSPACE_ROOT when possible.
            option_path = (_WORKSPACE_ROOT / option["id"]).resolve()
            if option_path.exists() and option_path.is_file() and _is_under_allowed_root(option_path):
                return option_path

    raise ValueError(f"Local dataset not found or not allowed: {dataset_ref}")


def _extract_sample(data: Any, sample_index: int) -> tuple[dict[str, Any], str | None]:
    if isinstance(data, list):
        if not data:
            raise ValueError("Dataset has no samples")
        idx = min(max(sample_index, 0), len(data) - 1)
        sample = data[idx]
        if isinstance(sample, dict):
            return sample, str(sample.get("task_id") or sample.get("id") or idx)
        return {"value": sample}, str(idx)

    if isinstance(data, dict):
        for key in ("tasks", "samples", "items"):
            entries = data.get(key)
            if isinstance(entries, list) and entries:
                idx = min(max(sample_index, 0), len(entries) - 1)
                sample = entries[idx]
                if isinstance(sample, dict):
                    return sample, str(sample.get("task_id") or sample.get("id") or idx)
                return {"value": sample}, str(idx)
        return data, str(data.get("task_id") or data.get("id") or "0")

    raise ValueError("Unsupported dataset format; expected JSON object or array")


def load_local_dataset_sample(dataset_ref: str, sample_index: int = 0) -> tuple[dict[str, Any], dict[str, Any]]:
    path = _resolve_local_dataset(dataset_ref)
    payload = json.loads(path.read_text(encoding="utf-8"))
    sample, task_id = _extract_sample(payload, sample_index)
    meta = {
        "source": "local",
        "dataset_id": dataset_ref,
        "dataset_path": _safe_relative_id(path),
        "sample_index": sample_index,
        "task_id": task_id,
    }
    return sample, meta


def load_repository_dataset_sample(dataset_id: str, sample_index: int = 0) -> tuple[dict[str, Any], dict[str, Any]]:
    try:
        from tools.agents.benchmarks.loader import load_benchmark

        tasks = load_benchmark(dataset_id=dataset_id, limit=max(sample_index + 1, 1))
        if not tasks:
            raise ValueError(f"No samples returned for repository dataset '{dataset_id}'")
        index = min(max(sample_index, 0), len(tasks) - 1)
        task = tasks[index]
        sample = task.to_dict() if hasattr(task, "to_dict") else asdict(task)
        meta = {
            "source": "repository",
            "dataset_id": dataset_id,
            "sample_index": index,
            "task_id": sample.get("task_id"),
            "benchmark_id": sample.get("benchmark_id", dataset_id),
        }
        return sample, meta
    except Exception as exc:
        raise ValueError(
            f"Unable to load repository dataset '{dataset_id}'. "
            "Choose a local JSON dataset or ensure benchmark dependencies are available."
        ) from exc


def _is_empty_value(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, (list, dict, tuple, set)):
        return len(value) == 0
    return False


def validate_required_inputs_present(
    workflow_inputs: dict[str, WorkflowInput],
    provided_inputs: dict[str, Any],
) -> list[str]:
    """Return required workflow input names that are missing/empty."""
    missing: list[str] = []
    for input_name, input_def in workflow_inputs.items():
        if not input_def.required:
            continue
        value = provided_inputs.get(input_name)
        if _is_empty_value(value):
            missing.append(input_name)
    return missing


def _extract_message_text(
    sample: dict[str, Any],
    preferred_roles: tuple[str, ...] = ("user", "system", "assistant"),
) -> str | None:
    """Extract the best available text snippet from chat-style dataset samples."""
    messages = sample.get("messages")
    if not isinstance(messages, list):
        return None

    candidates: list[tuple[str, str]] = []
    for message in messages:
        if not isinstance(message, dict):
            continue
        content = message.get("content")
        if not isinstance(content, str):
            continue
        text = content.strip()
        if not text:
            continue
        role = str(message.get("role", "")).lower()
        candidates.append((role, text))

    if not candidates:
        return None

    for role in preferred_roles:
        for candidate_role, text in candidates:
            if candidate_role == role:
                return text
    return candidates[0][1]


def _dataset_value_for_input(
    input_name: str,
    input_def: WorkflowInput,
    dataset_sample: dict[str, Any],
) -> Any:
    lowered = input_name.lower()
    explicit = dataset_sample.get(input_name)
    if explicit not in (None, ""):
        return explicit
    nested_inputs = dataset_sample.get("inputs")
    if isinstance(nested_inputs, dict):
        nested_value = nested_inputs.get(input_name)
        if nested_value not in (None, ""):
            return nested_value

    if "file" in lowered:
        return _pick_first(
            dataset_sample,
            [
                "code_file",
                "file_path",
                "path",
                "source_path",
                "code",
                "body",
                "prompt",
                "task_description",
                "instruction",
                "input",
            ],
        )
    if "spec" in lowered or "requirement" in lowered:
        value = _pick_first(
            dataset_sample,
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
        if value not in (None, ""):
            return value
        return _extract_message_text(dataset_sample, preferred_roles=("user", "system", "assistant"))
    if "tech_stack" in lowered and input_def.type == "object":
        stack = dataset_sample.get("tech_stack")
        if stack not in (None, ""):
            return stack
        if input_def.default not in (None, ""):
            return input_def.default

    value = _pick_first(
        dataset_sample,
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
        ],
    )
    if value not in (None, ""):
        return value
    return _extract_message_text(dataset_sample)


def match_workflow_dataset(
    workflow_def: WorkflowDefinition,
    dataset_sample: dict[str, Any],
) -> tuple[bool, list[str]]:
    """Check whether dataset sample can satisfy required workflow inputs."""
    if not isinstance(dataset_sample, dict):
        return False, ["invalid_dataset_sample"]

    missing_reasons: list[str] = []
    required_input_names = []
    for name, input_def in workflow_def.inputs.items():
        if not input_def.required:
            continue
        if input_def.default not in (None, ""):
            # Workflow defaults satisfy required inputs even when dataset omits them.
            continue
        required_input_names.append(name)

    for input_name in required_input_names:
        value = _dataset_value_for_input(
            input_name,
            workflow_def.inputs[input_name],
            dataset_sample,
        )
        if _is_empty_value(value):
            missing_reasons.append(f"missing: {input_name}")

    if workflow_def.capabilities.inputs:
        for capability_input in workflow_def.capabilities.inputs:
            input_def = workflow_def.inputs.get(capability_input)
            if input_def is not None and input_def.default not in (None, ""):
                continue

            if input_def is not None:
                value = _dataset_value_for_input(capability_input, input_def, dataset_sample)
            else:
                value = dataset_sample.get(capability_input)

            if _is_empty_value(value):
                missing_reasons.append(f"missing: {capability_input}")

    return len(missing_reasons) == 0, sorted(set(missing_reasons))


def _tokenize(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[A-Za-z0-9_]+", text.lower())
        if len(token) > 2
    }


def _extract_expected_text(sample: dict[str, Any]) -> str:
    if not isinstance(sample, dict):
        return ""
    if isinstance(sample.get("expected_output"), str):
        return sample["expected_output"]
    if isinstance(sample.get("golden_patch"), str):
        return sample["golden_patch"]
    answer = sample.get("answer")
    if isinstance(answer, dict) and isinstance(answer.get("body"), str):
        return answer["body"]
    if isinstance(sample.get("solution"), str):
        return sample["solution"]
    return ""


def _output_text(result: WorkflowResult) -> str:
    try:
        return json.dumps(result.final_output, default=str)
    except Exception:
        return str(result.final_output)


def _text_overlap_score(expected: str, generated: str) -> float:
    expected_tokens = _tokenize(expected)
    generated_tokens = _tokenize(generated)
    if not expected_tokens:
        return 0.0
    overlap = expected_tokens & generated_tokens
    return (len(overlap) / len(expected_tokens)) * 100.0


def _compute_criterion_score(
    criterion: str,
    result: WorkflowResult,
    expected_text: str,
) -> float:
    success_rate = float(result.success_rate)
    total_steps = max(len(result.steps), 1)
    failed_steps = len(result.failed_steps)
    retries = result.total_retries
    duration_ms = result.total_duration_ms or 0.0
    output_text = _output_text(result)

    if criterion == "correctness":
        overlap = _text_overlap_score(expected_text, output_text) if expected_text else success_rate
        blended = (success_rate * 0.7) + (overlap * 0.3)
        if result.overall_status == StepStatus.FAILED:
            blended *= 0.75
        return _clamp(blended)

    if criterion == "code_quality":
        failure_penalty = (failed_steps / total_steps) * 45.0
        retry_penalty = min(retries * 4.0, 20.0)
        status_bonus = 8.0 if result.overall_status == StepStatus.SUCCESS else -12.0
        score = 78.0 - failure_penalty - retry_penalty + status_bonus
        return _clamp(score)

    if criterion == "efficiency":
        seconds = duration_ms / 1000.0
        duration_penalty = min(seconds * 1.5, 55.0)
        retry_penalty = min(retries * 5.0, 20.0)
        score = 100.0 - duration_penalty - retry_penalty
        return _clamp(score)

    if criterion == "documentation":
        if not output_text:
            return 20.0
        chars = len(output_text)
        key_count = len(result.final_output.keys()) if isinstance(result.final_output, dict) else 1
        richness = min(chars / 120.0, 45.0) + min(key_count * 6.0, 30.0)
        base = 30.0 + richness
        if result.overall_status == StepStatus.FAILED:
            base -= 15.0
        return _clamp(base)

    # Generic fallback for unknown criteria from config
    return _clamp(success_rate)


def _grade(score: float) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def _default_judge_scale() -> dict[str, str]:
    return {
        "1": "Major requirement failures",
        "2": "Multiple significant errors",
        "3": "Minimum acceptable quality",
        "4": "Strong quality with minor gaps",
        "5": "Excellent quality and completeness",
    }


def _build_judge_criteria(
    *,
    weights: dict[str, float],
    criteria_by_name: dict[str, WorkflowCriterion],
) -> list[JudgeCriterionDefinition]:
    criteria: list[JudgeCriterionDefinition] = []
    if criteria_by_name:
        for criterion_name in weights:
            criterion = criteria_by_name.get(criterion_name)
            if criterion is None:
                continue
            criteria.append(
                JudgeCriterionDefinition(
                    name=criterion.name,
                    definition=criterion.definition,
                    scale=criterion.scale or _default_judge_scale(),
                )
            )
        if criteria:
            return criteria

    for criterion_name in weights:
        criteria.append(
            JudgeCriterionDefinition(
                name=criterion_name,
                definition=f"Evaluate {criterion_name}",
                scale=_default_judge_scale(),
            )
        )
    return criteria


def _advisory_similarity_score(
    *,
    expected_text: str,
    generated_text: str,
    objective_score_0_1: float,
) -> float:
    if expected_text:
        overlap = _text_overlap_score(expected_text, generated_text)
        return normalize_score(overlap / 100.0, "zero_one")
    # When no reference text is available, avoid penalizing by falling back
    # to objective execution signal.
    return normalize_score(objective_score_0_1, "zero_one")


def _advisory_efficiency_score(
    *,
    result: WorkflowResult,
    normalized_scores: dict[str, float],
) -> float:
    if "efficiency" in normalized_scores:
        return normalize_score(normalized_scores["efficiency"], "zero_one")

    duration_seconds = (result.total_duration_ms or 0.0) / 1000.0
    duration_norm = normalize_score(
        duration_seconds,
        "lower_is_better",
        slo_good=2.0,
        slo_bad=60.0,
    )
    retry_norm = normalize_score(
        result.total_retries,
        "lower_is_better",
        slo_good=0.0,
        slo_bad=8.0,
    )
    return (duration_norm * 0.7) + (retry_norm * 0.3)


def _compose_hybrid_score(
    *,
    objective_score_0_1: float,
    advisory_score_0_1: float,
    judge_score_0_1: float | None,
    component_weights: dict[str, float] | None = None,
) -> tuple[float, dict[str, float]]:
    default_weights = {
        "objective": 0.60,
        "judge": 0.25,
        "advisory": 0.15,
    }
    weights = dict(default_weights)
    if component_weights:
        weights.update(component_weights)

    active_components: dict[str, float] = {
        "objective": objective_score_0_1,
        "advisory": advisory_score_0_1,
    }
    if judge_score_0_1 is not None:
        active_components["judge"] = judge_score_0_1

    weight_sum = 0.0
    weighted = 0.0
    active_weights: dict[str, float] = {}
    for name, value in active_components.items():
        weight = max(float(weights.get(name, 0.0)), 0.0)
        if weight <= 0:
            continue
        active_weights[name] = weight
        weighted += value * weight
        weight_sum += weight

    if weight_sum <= 0:
        return objective_score_0_1, {"objective": 1.0}
    return weighted / weight_sum, active_weights


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
    rubric_id, rubric_version, weights, criteria_by_name = _resolve_rubric(
        workflow_definition,
        rubric,
    )
    total_weight = sum(weights.values()) or 1.0
    expected_text = _extract_expected_text(dataset_sample or {})

    criteria: list[dict[str, Any]] = []
    normalized_scores: dict[str, float] = {}
    weighted_sum = 0.0
    raw_sum = 0.0
    for criterion, weight in weights.items():
        raw_score = _compute_criterion_score(criterion, result, expected_text)
        config = criteria_by_name.get(criterion)
        formula_id = config.formula_id if config else "zero_one"
        # Legacy scorer emits 0..100. Canonical normalization uses 0..1.
        normalized_score = normalize_score(raw_score / 100.0, formula_id)
        adjusted_score = adjust_for_sample_size(normalized_score, n=max(len(result.steps), 1))
        critical_floor = config.critical_floor if config else None
        floor_passed = True if critical_floor is None else normalized_score >= critical_floor

        criteria.append(
            {
                "criterion": criterion,
                "raw_score": round(raw_score, 4),
                "normalized_score": round(normalized_score, 4),
                "adjusted_normalized_score": round(adjusted_score, 4),
                "score": round(normalized_score * 100.0, 2),
                "weight": float(weight),
                "formula_id": formula_id,
                "critical_floor": critical_floor,
                "floor_passed": floor_passed,
                "max_score": 100.0,
            }
        )
        normalized_scores[criterion] = normalized_score
        weighted_sum += normalized_score * float(weight)
        raw_sum += raw_score

    objective_score_0_1 = weighted_sum / total_weight
    objective_weighted_score = objective_score_0_1 * 100.0
    generated_text = _output_text(result)
    advisory_similarity_0_1 = _advisory_similarity_score(
        expected_text=expected_text,
        generated_text=generated_text,
        objective_score_0_1=objective_score_0_1,
    )
    advisory_efficiency_0_1 = _advisory_efficiency_score(
        result=result,
        normalized_scores=normalized_scores,
    )
    advisory_score_0_1 = (advisory_similarity_0_1 * 0.67) + (advisory_efficiency_0_1 * 0.33)

    judge_result: JudgeEvaluationResult | None = None
    judge_score_0_1: float | None = None
    if judge is not None:
        try:
            judge_criteria = _build_judge_criteria(
                weights=weights,
                criteria_by_name=criteria_by_name,
            )
            judge_result = judge.evaluate(
                candidate_output=generated_text,
                expected_output=expected_text,
                criteria=judge_criteria,
            )
            judge_score_0_1 = judge_result.normalized_score

            judge_by_name = {item.name: item for item in judge_result.criteria}
            for criterion_payload in criteria:
                judge_item = judge_by_name.get(str(criterion_payload["criterion"]))
                if judge_item is None:
                    continue
                criterion_payload["judge_raw_score"] = round(judge_item.raw_score, 4)
                criterion_payload["judge_normalized_score"] = round(judge_item.normalized_score, 4)
                criterion_payload["judge_evidence"] = judge_item.evidence
        except Exception as exc:
            logger.warning("Judge evaluation skipped due to error: %s", exc)

    hybrid_score_0_1, active_hybrid_weights = _compose_hybrid_score(
        objective_score_0_1=objective_score_0_1,
        advisory_score_0_1=advisory_score_0_1,
        judge_score_0_1=judge_score_0_1,
        component_weights=hybrid_component_weights,
    )
    weighted_score = hybrid_score_0_1 * 100.0
    overall_score = raw_sum / len(criteria) if criteria else 0.0
    threshold = pass_threshold()
    grade = _grade(weighted_score)

    floor_violations: list[CriterionFloorResult] = []

    def _record_floor_failure(name: str, floor: float, value: float) -> None:
        existing = {violation.criterion for violation in floor_violations}
        if name in existing:
            return
        if value < floor:
            floor_violations.append(
                CriterionFloorResult(
                    criterion=name,
                    floor=floor,
                    normalized_score=value,
                )
            )

    for criterion_payload in criteria:
        critical_floor = criterion_payload.get("critical_floor")
        if critical_floor is not None:
            _record_floor_failure(
                str(criterion_payload["criterion"]),
                float(critical_floor),
                float(criterion_payload["normalized_score"]),
            )

    for correctness_key in ("correctness", "correctness_rubric"):
        if correctness_key in normalized_scores:
            _record_floor_failure(correctness_key, 0.70, normalized_scores[correctness_key])
            break

    for validation_key in ("safety_validation", "validation", "safety", "code_quality"):
        if validation_key in normalized_scores:
            _record_floor_failure(validation_key, 0.80, normalized_scores[validation_key])
            break

    step_scores = _step_scores(result)
    payload: dict[str, Any] = {
        "enabled": True,
        "rubric": rubric_id,
        "rubric_id": rubric_id,
        "rubric_version": rubric_version,
        "criteria": criteria,
        "overall_score": round(overall_score, 2),
        "weighted_score": round(weighted_score, 2),
        "objective_weighted_score": round(objective_weighted_score, 2),
        "grade": grade,
        "passed": False,
        "pass_threshold": threshold,
        "step_scores": step_scores,
        "dataset": dataset_meta,
        "score_layers": {
            "layer1_objective": round(objective_score_0_1 * 100.0, 2),
            "layer2_judge": None if judge_score_0_1 is None else round(judge_score_0_1 * 100.0, 2),
            "layer3_similarity": round(advisory_similarity_0_1 * 100.0, 2),
            "layer3_efficiency": round(advisory_efficiency_0_1 * 100.0, 2),
            "layer3_advisory": round(advisory_score_0_1 * 100.0, 2),
        },
        "hybrid_weights": active_hybrid_weights,
        "judge": judge_result.to_payload() if judge_result is not None else None,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    dataset_compatible = True
    if isinstance(dataset_meta, dict) and "dataset_workflow_compatible" in dataset_meta:
        dataset_compatible = bool(dataset_meta["dataset_workflow_compatible"])
    elif workflow_definition is not None and isinstance(dataset_sample, dict):
        dataset_compatible, _ = match_workflow_dataset(workflow_definition, dataset_sample)

    hard_gates = compute_hard_gates(
        result,
        workflow_outputs=workflow_definition.outputs if workflow_definition else None,
        eval_payload=payload,
        dataset_workflow_compatible=dataset_compatible,
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
