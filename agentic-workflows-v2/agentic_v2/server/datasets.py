"""Dataset loading, listing, and matching utilities.

Extracted from evaluation.py to reduce file size and improve
single-responsibility adherence.  All public names are re-exported
by ``evaluation.py`` for backward compatibility.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict
from pathlib import Path
from typing import Any

import yaml

from ..workflows.loader import (
    WorkflowDefinition,
    WorkflowInput,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Project root helpers
# ---------------------------------------------------------------------------

def _resolve_project_root() -> Path:
    this_file = Path(__file__).resolve()
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


# ---------------------------------------------------------------------------
# Dataset discovery & listing
# ---------------------------------------------------------------------------

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


def list_eval_sets() -> list[dict[str, Any]]:
    """Return predefined evaluation sets from config."""
    config = _load_eval_config()
    eval_sets_config = (
        config.get("evaluation", {})
        .get("eval_sets", {})
    )

    if not isinstance(eval_sets_config, dict):
        return []

    eval_sets: list[dict[str, Any]] = []
    for set_id, set_config in eval_sets_config.items():
        if not isinstance(set_config, dict):
            continue

        eval_sets.append({
            "id": str(set_id),
            "name": set_config.get("name", str(set_id).replace("_", " ").title()),
            "description": set_config.get("description", ""),
            "datasets": set_config.get("datasets", []),
        })

    return sorted(eval_sets, key=lambda x: x["id"])


# ---------------------------------------------------------------------------
# Dataset loading
# ---------------------------------------------------------------------------

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
    """Resolve a local dataset reference to a JSON file path under an allowed root."""
    for option in list_local_datasets():
        if option["id"] == dataset_ref:
            option_path = (_WORKSPACE_ROOT / option["id"]).resolve()
            if (
                option_path.exists()
                and option_path.is_file()
                and _is_under_allowed_root(option_path)
            ):
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


def load_local_dataset_sample(
    dataset_ref: str, sample_index: int = 0
) -> tuple[dict[str, Any], dict[str, Any]]:
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


def load_repository_dataset_sample(
    dataset_id: str, sample_index: int = 0
) -> tuple[dict[str, Any], dict[str, Any]]:
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


# ---------------------------------------------------------------------------
# Dataset / workflow matching
# ---------------------------------------------------------------------------

def _is_empty_value(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, (list, dict, tuple, set)):
        return len(value) == 0
    return False


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

    if "file" in lowered or "patch" in lowered:
        return _pick_first(
            dataset_sample,
            [
                "code_file", "file_path", "path", "source_path",
                "patch", "code", "body", "prompt",
                "task_description", "instruction", "input",
            ],
        )
    if "bug" in lowered or "report" in lowered or "issue" in lowered:
        value = _pick_first(
            dataset_sample,
            [
                "bug_report", "problem_statement", "issue_text",
                "issue_body", "description", "prompt",
                "task_description", "body", "instruction", "input",
                "question", "query", "request",
            ],
        )
        if value not in (None, ""):
            return value
        return _extract_message_text(dataset_sample)
    if "spec" in lowered or "requirement" in lowered:
        value = _pick_first(
            dataset_sample,
            [
                "feature_spec", "task_description", "prompt",
                "description", "instruction", "input",
                "question", "query", "request", "body",
            ],
        )
        if value not in (None, ""):
            return value
        return _extract_message_text(dataset_sample)
    if "tech_stack" in lowered and input_def.type == "object":
        stack = dataset_sample.get("tech_stack")
        if stack not in (None, ""):
            return stack
        if input_def.default not in (None, ""):
            return input_def.default

    if input_def.enum or input_def.default not in (None, ""):
        return input_def.default

    value = _pick_first(
        dataset_sample,
        [
            "prompt", "task_description", "problem_statement",
            "description", "body", "instruction", "input",
            "question", "query", "request", "issue_text",
            "content", "text", "code",
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
            continue
        required_input_names.append(name)

    for input_name in required_input_names:
        value = _dataset_value_for_input(
            input_name, workflow_def.inputs[input_name], dataset_sample,
        )
        if _is_empty_value(value):
            missing_reasons.append(f"missing: {input_name}")

    caps = workflow_def.capabilities
    capability_inputs = (
        caps.get("inputs", []) if isinstance(caps, dict)
        else getattr(caps, "inputs", [])
    )
    if capability_inputs:
        for capability_input in capability_inputs:
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


def _materialize_file_input(
    value: Any,
    *,
    input_name: str,
    run_id: str,
    artifacts_dir: Path,
) -> Any:
    if not isinstance(value, str):
        return value

    artifacts_dir.mkdir(parents=True, exist_ok=True)
    artifacts_root = artifacts_dir.resolve()

    looks_python = any(marker in value for marker in ("def ", "class ", "import "))

    if looks_python:
        suffix = ".py"
        file_path = artifacts_root / f"{run_id}_{input_name}{suffix}"
        file_path.write_text(value, encoding="utf-8")
        return str(file_path)

    candidate: Path | None = None
    if any(sep in value for sep in ("/", "\\")) or value.endswith((".py", ".txt")):
        try:
            candidate = (artifacts_root / value).resolve()
            try:
                candidate.relative_to(artifacts_root)
                if candidate.is_file():
                    return str(candidate)
            except ValueError:
                candidate = None
        except Exception:
            candidate = None

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
            "prompt", "task_description", "problem_statement",
            "description", "body", "instruction", "input",
            "question", "query", "request", "issue_text",
            "content", "text", "code", "expected_output",
        ],
    )
    if generic_text in (None, ""):
        generic_text = _extract_message_text(sample)
    for name, definition in workflow_inputs.items():
        lowered = name.lower()
        explicit = sample.get(name)
        value = explicit

        if value in (None, ""):
            if "file" in lowered or "patch" in lowered:
                value = _pick_first(
                    sample,
                    [
                        "code_file", "file_path", "path", "source_path",
                        "patch", "code", "body", "prompt", "task_description",
                    ],
                )
            elif "bug" in lowered or "report" in lowered or "issue" in lowered:
                value = _pick_first(
                    sample,
                    [
                        "bug_report", "problem_statement", "issue_text",
                        "issue_body", "description", "prompt",
                        "task_description", "body", "instruction", "input",
                        "question", "query", "request",
                    ],
                )
                if value in (None, ""):
                    value = _extract_message_text(sample)
            elif "spec" in lowered or "requirement" in lowered:
                value = _pick_first(
                    sample,
                    [
                        "feature_spec", "task_description", "prompt",
                        "description", "instruction", "input",
                        "question", "query", "request", "body",
                    ],
                )
                if value in (None, ""):
                    value = _extract_message_text(sample)
            elif "tech_stack" in lowered and definition.type == "object":
                value = sample.get("tech_stack") or {
                    "frontend": "react",
                    "backend": "fastapi",
                    "database": "postgresql",
                }
            else:
                if definition.enum:
                    pass
                elif definition.default not in (None, ""):
                    pass
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
