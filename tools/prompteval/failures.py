"""Failure taxonomy for pattern evaluation.

Defines enumerated failure modes and reporting structures for
deterministic classification of pattern execution failures.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class FailureMode(Enum):
    """Fixed taxonomy of pattern execution failures.

    Judges must classify failures using ONLY these modes. Free-text
    explanations are forbidden in scoring.
    """

    # Phase-related failures
    MISSING_PHASE = "missing_phase"
    PHASE_SKIP = "phase_skip"  # Alias for tests
    PHASE_ORDER_VIOLATION = "phase_order_violation"
    ORDER_VIOLATION = "order_violation"  # Alias for tests
    EXTRA_PHASE = "extra_phase"
    INCOMPLETE_PHASE = "incomplete_phase"

    # Reasoning failures
    IMPLICIT_REASONING = "implicit_reasoning"
    LEAKAGE_OUTSIDE_PHASE = "leakage_outside_phase"
    LEAKAGE = "leakage"  # Alias for tests
    PREMATURE_TERMINATION = "premature_termination"

    # Pattern-specific failures
    REFLECTION_WITHOUT_REVISION = "reflection_without_revision"
    RAG_WITHOUT_GROUNDING = "rag_without_grounding"
    TOOL_CALL_WITHOUT_ACTION = "tool_call_without_action"
    VERIFICATION_NOT_INDEPENDENT = "verification_not_independent"

    # Self-reference failures
    SELF_CONSISTENCY_VIOLATION = "self_consistency_violation"
    GENERIC_CRITIQUE = "generic_critique"

    # Robustness failures
    PATTERN_COLLAPSE = "pattern_collapse"
    HALLUCINATED_OBSERVATION = "hallucinated_observation"


@dataclass
class FailureReport:
    """Structured report of a single failure instance.

    Attributes:
        mode: The classified failure type
        phase: Which phase the failure occurred in (if applicable)
        expected: What was expected
        actual: What was observed
        details: Human-readable description (for test compatibility)
        severity: Impact level (critical, major, minor)
    """

    mode: FailureMode
    phase: Optional[str] = None
    expected: Optional[str] = None
    actual: Optional[str] = None
    details: Optional[str] = None
    severity: str = "major"  # critical, major, minor

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "mode": self.mode.value,
            "phase": self.phase,
            "expected": self.expected,
            "actual": self.actual,
            "severity": self.severity,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "FailureReport":
        """Create from dictionary."""
        return cls(
            mode=FailureMode(data["mode"]),
            phase=data.get("phase"),
            expected=data.get("expected"),
            actual=data.get("actual"),
            severity=data.get("severity", "major"),
        )


@dataclass
class PatternFailureSummary:
    """Summary of all failures for a pattern evaluation run.

    Attributes:
        pattern: The pattern being evaluated (e.g., 'react', 'cove')
        failures: List of individual failure reports
        has_critical: Whether any critical failures exist
        hard_gate_failed: Whether hard gates were violated
        failure_count: Total number of failures
    """

    pattern: str = ""
    failures: List[FailureReport] = field(default_factory=list)
    hard_gate_failed: bool = False
    hard_gate_reason: Optional[str] = None

    @property
    def has_critical(self) -> bool:
        """Check if any critical failures exist."""
        return any(f.severity == "critical" for f in self.failures)

    @property
    def failure_count(self) -> int:
        """Total number of failures."""
        return len(self.failures)

    @property
    def failure_modes(self) -> List[str]:
        """List of unique failure mode values."""
        return list(set(f.mode.value for f in self.failures))

    @property
    def total(self) -> int:
        """Alias for failure_count (test compatibility)."""
        return len(self.failures)

    @property
    def by_mode(self) -> dict:
        """Count failures by mode (test compatibility)."""
        counts: dict = {}
        for f in self.failures:
            counts[f.mode] = counts.get(f.mode, 0) + 1
        return counts

    def add_failure(
        self,
        mode_or_report,
        phase: Optional[str] = None,
        expected: Optional[str] = None,
        actual: Optional[str] = None,
        severity: str = "major",
    ) -> None:
        """Add a failure to the summary.

        Accepts FailureMode or FailureReport.
        """
        if isinstance(mode_or_report, FailureReport):
            self.failures.append(mode_or_report)
        else:
            self.failures.append(
                FailureReport(
                    mode=mode_or_report,
                    phase=phase,
                    expected=expected,
                    actual=actual,
                    severity=severity,
                )
            )

    def set_hard_gate_failure(self, reason: str) -> None:
        """Mark that a hard gate was failed."""
        self.hard_gate_failed = True
        self.hard_gate_reason = reason

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "failures": [f.to_dict() for f in self.failures],
            "has_critical": self.has_critical,
            "hard_gate_failed": self.hard_gate_failed,
            "hard_gate_reason": self.hard_gate_reason,
            "failure_count": self.failure_count,
            "failure_modes": self.failure_modes,
        }


# =============================================================================
# FAILURE MODE DESCRIPTIONS (for documentation/judges)
# =============================================================================

FAILURE_DESCRIPTIONS = {
    FailureMode.MISSING_PHASE: "A required phase was not present in the output",
    FailureMode.PHASE_ORDER_VIOLATION: "Phases appeared in incorrect order",
    FailureMode.EXTRA_PHASE: "An unexpected or forbidden phase appeared",
    FailureMode.INCOMPLETE_PHASE: "A phase was present but lacked required content",
    FailureMode.IMPLICIT_REASONING: "Reasoning occurred outside of designated phase markers",
    FailureMode.LEAKAGE_OUTSIDE_PHASE: "Content appeared outside of any phase boundary",
    FailureMode.PREMATURE_TERMINATION: "Pattern ended before completing required phases",
    FailureMode.REFLECTION_WITHOUT_REVISION: "Self-critique occurred but no revision followed",
    FailureMode.RAG_WITHOUT_GROUNDING: "Claims made without citation to retrieved sources",
    FailureMode.TOOL_CALL_WITHOUT_ACTION: "Tool invocation occurred outside Action phase",
    FailureMode.VERIFICATION_NOT_INDEPENDENT: "Verification phase referenced draft instead of checking independently",
    FailureMode.SELF_CONSISTENCY_VIOLATION: "Output contradicts itself across phases",
    FailureMode.GENERIC_CRITIQUE: "Critique was generic rather than specific to the attempt",
    FailureMode.PATTERN_COLLAPSE: "Pattern collapsed into a simpler pattern (e.g., ReAct → CoT)",
    FailureMode.HALLUCINATED_OBSERVATION: "Observation contained fabricated rather than actual results",
}


def get_failure_description(mode: FailureMode) -> str:
    """Get human-readable description of a failure mode."""
    return FAILURE_DESCRIPTIONS.get(mode, f"Unknown failure: {mode.value}")
