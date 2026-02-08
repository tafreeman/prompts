"""Workflow-family scoring profile defaults."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ScoringProfile:
    """Named weight profile with optional extra hard-gate hints."""

    profile_id: str
    description: str
    weights: dict[str, float]
    extra_gates: list[str] = field(default_factory=list)


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
        extra_gates=["fail_to_pass"],
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
        extra_gates=["required_outputs_parseable"],
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
        extra_gates=["answer_grounded"],
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
        extra_gates=["tool_call_schema_valid"],
    ),
}

DEFAULT_PROFILE_ID = "B"


def get_profile(profile_id: str | None) -> ScoringProfile:
    """Return a scoring profile, falling back to default."""
    if not profile_id:
        return SCORING_PROFILES[DEFAULT_PROFILE_ID]
    return SCORING_PROFILES.get(profile_id, SCORING_PROFILES[DEFAULT_PROFILE_ID])

