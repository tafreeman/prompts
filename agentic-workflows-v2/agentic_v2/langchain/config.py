"""YAML workflow configuration loader.

Reads workflow YAML files and produces lightweight config dataclasses.
This is intentionally *not* an executor — it just parses config.
The graph compiler (``graph.py``) turns configs into runnable graphs.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# Config dataclasses
# ---------------------------------------------------------------------------


@dataclass
class StepConfig:
    """A single step parsed from YAML."""

    name: str
    agent: str = ""
    description: str = ""
    depends_on: list[str] = field(default_factory=list)
    inputs: dict[str, str] = field(default_factory=dict)
    outputs: dict[str, str] = field(default_factory=dict)
    when: str | None = None
    loop_until: str | None = None
    loop_max: int = 3
    tools: list[str] | None = None
    prompt_file: str | None = None
    model_override: str | None = None


@dataclass
class InputConfig:
    """Workflow input parameter."""

    name: str
    type: str = "string"
    description: str = ""
    default: Any = None
    required: bool = True
    enum: list[str] | None = None


@dataclass
class OutputConfig:
    """Workflow output."""

    name: str
    from_expr: Any = ""
    optional: bool = False


@dataclass
class CriterionConfig:
    """Evaluation criterion."""

    name: str
    definition: str = ""
    weight: float | None = None
    critical_floor: float | None = None
    scale: dict[str, str] = field(default_factory=dict)
    evidence_required: list[str] = field(default_factory=list)
    formula_id: str = "zero_one"


@dataclass
class EvaluationConfig:
    """Workflow evaluation settings."""

    rubric_id: str | None = None
    scoring_profile: str | None = None
    weights: dict[str, float] | None = None
    criteria: list[CriterionConfig] = field(default_factory=list)


@dataclass
class WorkflowConfig:
    """Complete parsed workflow configuration.

    This is a pure-data object — no execution logic.
    """

    name: str
    description: str = ""
    version: str = "1.0"
    experimental: bool = False
    inputs: dict[str, InputConfig] = field(default_factory=dict)
    outputs: dict[str, OutputConfig] = field(default_factory=dict)
    steps: list[StepConfig] = field(default_factory=list)
    evaluation: EvaluationConfig | None = None
    capabilities: dict[str, list[str]] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------

_DEFAULT_DEFINITIONS_DIR = Path(__file__).parent.parent / "workflows" / "definitions"


def _is_within_base(path: Path, base: Path) -> bool:
    """Return True if ``path`` is inside ``base`` after resolution."""
    resolved_base = base.resolve()
    resolved_path = path.resolve()
    try:
        # Python 3.9+
        return resolved_path.is_relative_to(resolved_base)
    except AttributeError:
        base_str = os.fspath(resolved_base)
        path_str = os.fspath(resolved_path)
        if path_str == base_str:
            return True
        # Ensure we only match proper sub-paths, not common prefixes
        return path_str.startswith(base_str + os.sep)


def _safe_workflow_path(base: Path, name: str) -> Path:
    """
    Construct a safe workflow path under ``base`` from a workflow ``name``.

    The workflow ``name`` is treated as a simple identifier (file stem) without
    directory components or an extension. The resulting path is always
    constructed under ``base`` and verified with ``_is_within_base``.
    """
    if not name or not isinstance(name, str):
        raise ValueError("Workflow name must be a non-empty string")

    # Interpret name as a Path and ensure it is just a bare stem, not a path.
    raw_path = Path(name)

    # Reject absolute paths and any name that has directory components.
    if raw_path.is_absolute() or raw_path.parent != Path("."):
        raise ValueError(f"Invalid workflow name: {name}")

    # We expect a bare name without an extension; derive the stem explicitly.
    stem = raw_path.stem
    if not stem or stem in (".", ".."):
        raise ValueError(f"Invalid workflow name: {name}")

    candidate = base / f"{stem}.yaml"
    if _is_within_base(candidate, base) and candidate.exists():
        return candidate

    candidate_yml = base / f"{stem}.yml"
    if _is_within_base(candidate_yml, base) and candidate_yml.exists():
        return candidate_yml

    available = list_workflows(base)
    raise FileNotFoundError(
        f"Workflow '{name}' not found in {base}. Available: {available}"
    )


def load_workflow_config(
    name: str,
    definitions_dir: Path | None = None,
) -> WorkflowConfig:
    """Load a workflow YAML file by name and return a ``WorkflowConfig``.

    Parameters
    ----------
    name:
        Workflow name (without ``.yaml`` extension).
    definitions_dir:
        Directory containing YAML files.  Defaults to the package's
        built-in ``workflows/definitions/`` folder.
    """
    base = (definitions_dir or _DEFAULT_DEFINITIONS_DIR).resolve()
    path = _safe_workflow_path(base, name)
    return _parse_file(path)


def list_workflows(definitions_dir: Path | None = None) -> list[str]:
    """List available workflow names."""
    base = definitions_dir or _DEFAULT_DEFINITIONS_DIR
    if not base.exists():
        return []
    return sorted(
        p.stem
        for p in base.iterdir()
        if p.suffix in (".yaml", ".yml")
    )


# ---------------------------------------------------------------------------
# Internal parsing
# ---------------------------------------------------------------------------


def _parse_file(path: Path) -> WorkflowConfig:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Workflow YAML must be a mapping: {path}")
    return _parse(data, path.stem)


def _parse(data: dict[str, Any], default_name: str) -> WorkflowConfig:
    # --- Steps ---
    steps: list[StepConfig] = []
    for raw in data.get("steps", []):
        if not isinstance(raw, dict) or "name" not in raw:
            continue
        steps.append(
            StepConfig(
                name=raw["name"],
                agent=raw.get("agent", ""),
                description=raw.get("description", ""),
                depends_on=raw.get("depends_on", []),
                inputs=dict(raw.get("inputs", {})),
                outputs=dict(raw.get("outputs", {})),
                when=raw.get("when"),
                loop_until=raw.get("loop_until"),
                loop_max=max(1, int(raw.get("loop_max", 3))),
                tools=(
                    raw.get("tools")
                    if isinstance(raw.get("tools"), list)
                    else None
                ),
                prompt_file=raw.get("prompt_file"),
                model_override=(
                    raw.get("model_override")
                    if isinstance(raw.get("model_override"), str)
                    else raw.get("model")
                ),
            )
        )

    # --- Inputs ---
    inputs: dict[str, InputConfig] = {}
    for k, v in data.get("inputs", {}).items():
        if isinstance(v, dict):
            inputs[k] = InputConfig(
                name=k,
                type=v.get("type", "string"),
                description=v.get("description", ""),
                default=v.get("default"),
                required=v.get("required", True),
                enum=v.get("enum"),
            )
        else:
            inputs[k] = InputConfig(name=k, default=v, required=False)

    # --- Outputs ---
    outputs: dict[str, OutputConfig] = {}
    for k, v in data.get("outputs", {}).items():
        if isinstance(v, dict):
            outputs[k] = OutputConfig(
                name=k,
                from_expr=v.get("from", ""),
                optional=v.get("optional", False),
            )
        else:
            outputs[k] = OutputConfig(name=k, from_expr=v)

    # --- Evaluation ---
    evaluation = None
    raw_eval = data.get("evaluation")
    if isinstance(raw_eval, dict):
        criteria = []
        for c in raw_eval.get("criteria", []):
            if isinstance(c, dict) and c.get("name"):
                criteria.append(
                    CriterionConfig(
                        name=c["name"],
                        definition=c.get("definition", ""),
                        weight=float(c["weight"]) if c.get("weight") else None,
                        critical_floor=(
                            float(c["critical_floor"])
                            if c.get("critical_floor") is not None
                            else None
                        ),
                        scale={
                            str(sk): str(sv)
                            for sk, sv in (c.get("scale") or {}).items()
                        },
                        evidence_required=c.get("evidence_required", []),
                        formula_id=c.get("formula_id", "zero_one"),
                    )
                )
        evaluation = EvaluationConfig(
            rubric_id=raw_eval.get("rubric_id"),
            scoring_profile=raw_eval.get("scoring_profile"),
            weights=raw_eval.get("weights"),
            criteria=criteria,
        )

    # --- Capabilities ---
    capabilities: dict[str, list[str]] = {}
    raw_cap = data.get("capabilities")
    if isinstance(raw_cap, dict):
        for ck, cv in raw_cap.items():
            if isinstance(cv, list):
                capabilities[ck] = [str(i) for i in cv]

    return WorkflowConfig(
        name=data.get("name", default_name),
        description=data.get("description", ""),
        version=str(data.get("version", "1.0")),
        experimental=bool(data.get("experimental", False)),
        inputs=inputs,
        outputs=outputs,
        steps=steps,
        evaluation=evaluation,
        capabilities=capabilities,
    )
