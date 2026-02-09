"""Output parser for pattern evaluation.

Parses raw model outputs into structured execution traces (IR) for
deterministic pattern conformance scoring.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

# =============================================================================
# DATA STRUCTURES
# =============================================================================


@dataclass
class Phase:
    """A detected phase in the model output."""

    type: str
    content: str
    line_start: int
    line_end: int
    valid: bool = True
    issues: List[str] = field(default_factory=list)

    @property
    def content_preview(self) -> str:
        """First 50 chars of content."""
        return (
            self.content[:50].replace("\n", " ").strip() + "..."
            if len(self.content) > 50
            else self.content.replace("\n", " ").strip()
        )

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "content_preview": self.content_preview,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "valid": self.valid,
            "issues": self.issues,
        }


@dataclass
class ParseResult:
    """Intermediate representation (IR) of parsed output.

    This is the structured execution trace used for scoring.
    """

    phases: List[Phase] = field(default_factory=list)
    ordering_valid: bool = True
    missing_phases: List[str] = field(default_factory=list)
    extra_phases: List[str] = field(default_factory=list)
    leakage_detected: bool = False
    leakage_content: List[str] = field(default_factory=list)
    parse_errors: List[str] = field(default_factory=list)
    raw_output: str = ""

    @property
    def phase_types(self) -> List[str]:
        """List of phase types in order of appearance."""
        return [p.type for p in self.phases]

    @property
    def is_valid(self) -> bool:
        """Check if parse produced a valid result."""
        return len(self.phases) > 0 and len(self.parse_errors) == 0

    def to_dict(self) -> dict:
        return {
            "phases": [p.to_dict() for p in self.phases],
            "phase_types": self.phase_types,
            "ordering_valid": self.ordering_valid,
            "missing_phases": self.missing_phases,
            "extra_phases": self.extra_phases,
            "leakage_detected": self.leakage_detected,
            "leakage_content": self.leakage_content,
            "parse_errors": self.parse_errors,
            "is_valid": self.is_valid,
        }


# =============================================================================
# PATTERN DEFINITION LOADER
# =============================================================================


def load_pattern_definition(pattern_name: str) -> Dict[str, Any]:
    """Load a pattern definition from YAML.

    Args:
        pattern_name: Name of pattern (react, cove, reflexion, rag)

    Returns:
        Pattern definition dictionary
    """
    patterns_dir = Path(__file__).parent.parent / "rubrics" / "patterns"
    pattern_file = patterns_dir / f"{pattern_name.lower()}.yaml"

    if not pattern_file.exists():
        raise ValueError(f"Pattern definition not found: {pattern_file}")

    with open(pattern_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_available_patterns() -> List[str]:
    """Get list of available pattern names."""
    patterns_dir = Path(__file__).parent.parent / "rubrics" / "patterns"
    if not patterns_dir.exists():
        return []
    return [f.stem for f in patterns_dir.glob("*.yaml")]


# =============================================================================
# PHASE DETECTION
# =============================================================================


def compile_phase_markers(pattern_def: Dict[str, Any]) -> Dict[str, List[re.Pattern]]:
    """Compile regex patterns for phase detection.

    Args:
        pattern_def: Pattern definition with phase_markers

    Returns:
        Dict mapping phase names to compiled regex patterns
    """
    markers = pattern_def.get("phase_markers", {})
    compiled = {}

    for phase_name, patterns in markers.items():
        compiled[phase_name] = [
            re.compile(p, re.IGNORECASE | re.MULTILINE) for p in patterns
        ]

    return compiled


def detect_phases(
    output: str,
    phase_markers: Dict[str, List[re.Pattern]],
) -> Tuple[List[Phase], List[str]]:
    """Detect phases in model output using regex markers.

    Args:
        output: Raw model output
        phase_markers: Compiled regex patterns per phase

    Returns:
        Tuple of (detected phases, content outside phases)
    """
    lines = output.split("\n")
    phases = []
    current_phase = None
    current_content = []
    current_start = 0
    leakage = []
    pre_phase_content = []

    for i, line in enumerate(lines):
        phase_found = None

        # Check each phase marker
        for phase_name, patterns in phase_markers.items():
            for pattern in patterns:
                if pattern.search(line):
                    phase_found = phase_name
                    break
            if phase_found:
                break

        if phase_found:
            # Save previous phase if exists
            if current_phase:
                phases.append(
                    Phase(
                        type=current_phase.lower(),  # Normalize to lowercase
                        content="\n".join(current_content),
                        line_start=current_start,
                        line_end=i - 1,
                    )
                )
            elif current_content:
                # Content before first phase = potential leakage
                pre_phase_content = current_content.copy()

            # Start new phase (will be lowercased when saved)
            current_phase = phase_found
            current_content = [line]
            current_start = i
        else:
            current_content.append(line)

    # Don't forget the last phase
    if current_phase:
        phases.append(
            Phase(
                type=current_phase.lower(),  # Normalize to lowercase
                content="\n".join(current_content),
                line_start=current_start,
                line_end=len(lines) - 1,
            )
        )

    # Check for leakage (non-whitespace content before first phase)
    if pre_phase_content:
        content = "\n".join(pre_phase_content).strip()
        if content and not content.startswith("#"):  # Allow markdown headers
            leakage.append(content)

    return phases, leakage


# =============================================================================
# ORDERING VALIDATION
# =============================================================================


def validate_ordering(
    phases: List[Phase],
    pattern_def: Dict[str, Any],
) -> Tuple[bool, List[str]]:
    """Validate phase ordering against pattern constraints.

    Args:
        phases: Detected phases
        pattern_def: Pattern definition with ordering_constraints

    Returns:
        Tuple of (is_valid, list of violations)
    """
    constraints = pattern_def.get("ordering_constraints", {})
    sequence = constraints.get("sequence", [])
    is_loop = constraints.get("loop", False)
    rules = constraints.get("rules", [])

    if not sequence:
        return True, []

    violations = []
    phase_types = [p.type for p in phases]
    # Normalize sequence to lowercase for comparison
    sequence_lower = [s.lower() for s in sequence]

    if is_loop:
        # For loops, check that sequence repeats correctly
        seq_len = len(sequence_lower)
        for i, phase in enumerate(phase_types):
            expected_idx = i % seq_len
            if phase != sequence_lower[expected_idx]:
                # Check if it's a valid terminator
                terminator = constraints.get("terminator")
                if terminator and phase == terminator.lower():
                    break  # Valid termination
                violations.append(
                    f"Expected {sequence[expected_idx]} at position {i}, got {phase}"
                )
    else:
        # Strict sequence check
        seq_idx = 0
        for phase in phase_types:
            if seq_idx < len(sequence_lower) and phase == sequence_lower[seq_idx]:
                seq_idx += 1
            elif phase in sequence_lower:
                violations.append(f"Phase {phase} appeared out of order")

    return len(violations) == 0, violations


# =============================================================================
# COMPLETENESS CHECK
# =============================================================================


def check_completeness(
    phases: List[Phase],
    pattern_def: Dict[str, Any],
) -> Tuple[List[str], List[str]]:
    """Check for missing and extra phases.

    Args:
        phases: Detected phases
        pattern_def: Pattern definition with required_phases

    Returns:
        Tuple of (missing_phases, extra_phases)
    """
    required = pattern_def.get("required_phases", [])
    required_names = [p["name"].lower() for p in required if p.get("required", True)]

    found_types = set(p.type for p in phases)  # Already lowercase

    missing = [name for name in required_names if name not in found_types]

    # Extra phases are those not defined in the pattern
    defined_names = set(p["name"].lower() for p in required)
    extra = [p.type for p in phases if p.type not in defined_names]

    return missing, extra


# =============================================================================
# MAIN PARSER
# =============================================================================


def parse_output(
    output: str,
    pattern_name: str,
    pattern_def: Optional[Dict[str, Any]] = None,
) -> ParseResult:
    """Parse model output into structured execution trace.

    Args:
        output: Raw model output
        pattern_name: Name of expected pattern
        pattern_def: Optional pre-loaded pattern definition

    Returns:
        ParseResult with structured IR
    """
    result = ParseResult(raw_output=output)

    # Load pattern definition if not provided
    if pattern_def is None:
        try:
            pattern_def = load_pattern_definition(pattern_name)
        except Exception as e:
            result.parse_errors.append(f"Failed to load pattern: {e}")
            return result

    # Compile phase markers
    try:
        markers = compile_phase_markers(pattern_def)
    except Exception as e:
        result.parse_errors.append(f"Failed to compile markers: {e}")
        return result

    # Detect phases
    phases, leakage = detect_phases(output, markers)
    result.phases = phases

    if leakage:
        result.leakage_detected = True
        result.leakage_content = leakage

    # Validate ordering
    ordering_valid, violations = validate_ordering(phases, pattern_def)
    result.ordering_valid = ordering_valid
    if violations:
        result.parse_errors.extend(violations)

    # Check completeness
    missing, extra = check_completeness(phases, pattern_def)
    result.missing_phases = missing
    result.extra_phases = extra

    return result


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================


def detect_pattern(output: str) -> Optional[str]:
    """Auto-detect which pattern an output follows.

    Args:
        output: Raw model output

    Returns:
        Pattern name or None if not detected
    """
    patterns = get_available_patterns()
    best_match = None
    best_score = 0

    for pattern_name in patterns:
        try:
            pattern_def = load_pattern_definition(pattern_name)
            markers = compile_phase_markers(pattern_def)
            phases, _ = detect_phases(output, markers)

            # Score based on number of phases found
            score = len(phases)
            if score > best_score:
                best_score = score
                best_match = pattern_name
        except Exception:
            continue

    return best_match if best_score > 0 else None


def extract_phase_content(
    result: ParseResult,
    phase_type: str,
) -> List[str]:
    """Extract all content from phases of a specific type.

    Args:
        result: ParseResult from parsing
        phase_type: Type of phase to extract

    Returns:
        List of content strings from matching phases
    """
    return [p.content for p in result.phases if p.type == phase_type]
