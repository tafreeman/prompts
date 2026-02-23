"""Workflow-family scoring profile defaults."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class ScoringProfile:
    """Named weight profile with optional extra hard-gate hints."""

    profile_id: str
    description: str
    weights: Mapping[str, float]
    extra_gates: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "weights", MappingProxyType(dict(self.weights)))
        object.__setattr__(self, "extra_gates", tuple(self.extra_gates))


SCORING_PROFILES: dict[str, ScoringProfile] = {
    "A": ScoringProfile(
        profile_id="A",
        description="Code repair / SWE-style iterative workflows",
        weights={
            "objective_tests": 0.60,
            "code_quality": 0.20,
            "efficiency": 0.10,
            "documentation": 0.10,
        },
        extra_gates=("fail_to_pass",),
    ),
    "B": ScoringProfile(
        profile_id="B",
        description="DAG generation/review workflows",
        weights={
            "correctness_rubric": 0.35,
            "code_quality": 0.30,
            "efficiency": 0.20,
            "documentation": 0.15,
        },
        extra_gates=("required_outputs_parseable",),
    ),
    "C": ScoringProfile(
        profile_id="C",
        description="RAG workflows",
        weights={
            "faithfulness": 0.35,
            "relevance": 0.30,
            "citation_quality": 0.20,
            "coherence": 0.15,
        },
        extra_gates=("answer_grounded",),
    ),
    "D": ScoringProfile(
        profile_id="D",
        description="Agentic tool-use/routing workflows",
        weights={
            "tool_selection_accuracy": 0.25,
            "task_completion": 0.30,
            "efficiency": 0.25,
            "coherence": 0.20,
        },
        extra_gates=("tool_call_schema_valid",),
    ),
    "E": ScoringProfile(
        profile_id="E",
        description=(
            "Deep research iterative pipeline"
            " (ADR-007 multidimensional tiebreaker weights)"
        ),
        weights={
            "coverage": 0.25,
            "source_quality": 0.20,
            "agreement": 0.20,
            "verification": 0.20,
            "recency": 0.15,
        },
        extra_gates=(
            "all_dimensions_high",
            "no_critical_contradictions",
            "sources_floor",
        ),
    ),
}

DEFAULT_PROFILE_ID = "B"


def get_profile(profile_id: str | None) -> ScoringProfile:
    """Return a scoring profile, falling back to default."""
    if not profile_id:
        return SCORING_PROFILES[DEFAULT_PROFILE_ID]
    return SCORING_PROFILES.get(profile_id, SCORING_PROFILES[DEFAULT_PROFILE_ID])

