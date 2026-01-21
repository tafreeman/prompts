"""
Integration module for pattern evaluation.

Provides CLI and API integration with existing prompteval and prompttools.
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any, List, Union

# Import existing evaluation infrastructure
from prompttools.evaluate import EvalResult, BatchResult, _get_grade
from prompttools.parse import parse_frontmatter

# Import pattern evaluation components
from tools.prompteval.parser import parse_output, detect_pattern, get_available_patterns
from tools.prompteval.pattern_evaluator import (
    PatternEvaluator,
    PatternScore,
    evaluate_pattern,
    DEFAULT_NUM_RUNS,
)
from tools.prompteval.failures import FailureMode


# =============================================================================
# PATTERN DETECTION FROM FRONTMATTER
# =============================================================================

PATTERN_KEYWORDS = {
    "react": ["react", "thought-action-observation", "reasoning-acting"],
    "cove": ["cove", "chain-of-verification", "verification"],
    "reflexion": ["reflexion", "self-critique", "self-improvement"],
    "rag": ["rag", "retrieval", "retrieval-augmented"],
}


def detect_pattern_from_frontmatter(frontmatter: Dict[str, Any]) -> Optional[str]:
    """
    Detect pattern from frontmatter tags or pattern field.

    Args:
        frontmatter: Parsed frontmatter dict

    Returns:
        Pattern name or None
    """
    # Check explicit pattern field
    pattern = frontmatter.get("pattern")
    if pattern:
        return pattern.lower()

    # Check tags
    tags = frontmatter.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]

    for pattern_name, keywords in PATTERN_KEYWORDS.items():
        for keyword in keywords:
            if keyword in [t.lower() for t in tags]:
                return pattern_name

    # Check category
    category = frontmatter.get("category", "")
    if category:
        for pattern_name, keywords in PATTERN_KEYWORDS.items():
            if pattern_name in category.lower():
                return pattern_name

    return None


# =============================================================================
# EXTENDED EVAL RESULT
# =============================================================================

@dataclass
class PatternEvalResult(EvalResult):
    """Extended EvalResult with pattern scoring."""
    pattern_name: str = ""
    pattern_score: Optional[PatternScore] = None
    dimension_scores: Dict[str, float] = field(default_factory=dict)
    failure_modes: List[str] = field(default_factory=list)
    passes_hard_gates: bool = False

    def to_dict(self) -> dict:
        base = {
            "file": self.file,
            "score": self.score,
            "grade": self.grade,
            "passed": self.passed,
            "criteria": self.criteria,
            "improvements": self.improvements,
            "model": self.model,
            "method": self.method,
            "tier": self.tier,
            "duration": self.duration,
            "error": self.error,
            "pattern_name": self.pattern_name,
            "dimension_scores": self.dimension_scores,
            "failure_modes": self.failure_modes,
            "passes_hard_gates": self.passes_hard_gates,
        }
        if self.pattern_score:
            base["pattern_details"] = self.pattern_score.to_dict()
        return base


# =============================================================================
# PATTERN EVALUATION FUNCTIONS
# =============================================================================

def evaluate_with_pattern(
    prompt_path: Union[str, Path],
    model_output: str,
    llm_client: Any,
    pattern_name: Optional[str] = None,
    num_runs: int = DEFAULT_NUM_RUNS,
    quick: bool = False,
) -> PatternEvalResult:
    """
    Evaluate a prompt with pattern scoring.

    Args:
        prompt_path: Path to prompt file
        model_output: Model's response to evaluate
        llm_client: LLM client for judge calls
        pattern_name: Override pattern detection
        num_runs: Number of evaluation runs
        quick: Use single-run evaluation

    Returns:
        PatternEvalResult with full scoring
    """
    path = Path(prompt_path)

    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return PatternEvalResult(
            file=str(path),
            score=0,
            grade="F",
            passed=False,
            error=f"Cannot read file: {e}",
        )

    # Parse frontmatter
    fm = parse_frontmatter(content)

    # Detect pattern
    if pattern_name is None:
        pattern_name = detect_pattern_from_frontmatter(fm)

    if pattern_name is None:
        # Try auto-detection from output
        pattern_name = detect_pattern(model_output)

    if pattern_name is None:
        return PatternEvalResult(
            file=str(path),
            score=0,
            grade="F",
            passed=False,
            error="Could not detect pattern. Specify --pattern explicitly.",
        )

    # Run pattern evaluation
    evaluator = PatternEvaluator(llm_client, num_runs=num_runs if not quick else 1)

    if quick:
        pattern_score = evaluator.quick_evaluate(content, model_output, pattern_name)
    else:
        pattern_score = evaluator.evaluate(content, model_output, pattern_name)

    # Convert to score 0-100
    overall = pattern_score.overall_score * 20  # 5-point to 100-point

    return PatternEvalResult(
        file=str(path),
        score=overall,
        grade=_get_grade(overall),
        passed=pattern_score.passes_hard_gates,
        criteria={
            k: v * 20 for k, v in pattern_score.dimension_medians.items()
        },
        improvements=_extract_improvements(pattern_score),
        model=str(llm_client),
        method="pattern",
        pattern_name=pattern_name,
        pattern_score=pattern_score,
        dimension_scores=pattern_score.dimension_medians,
        failure_modes=[
            fm.value for fm in (pattern_score.failure_summary.by_mode.keys() if pattern_score.failure_summary else [])
        ],
        passes_hard_gates=pattern_score.passes_hard_gates,
    )


def _extract_improvements(score: PatternScore) -> List[str]:
    """Extract improvement suggestions from pattern score."""
    improvements = []

    # Based on dimension scores
    for dim, val in score.dimension_medians.items():
        if val < 3:
            if dim == "PIF":
                improvements.append("Improve phase identification clarity")
            elif dim == "POI":
                improvements.append("Ensure correct phase ordering")
            elif dim == "PC":
                improvements.append("Include all required phases")
            elif dim == "CA":
                improvements.append("Better adhere to pattern constraints")
            elif dim == "SRC":
                improvements.append("Strengthen self-referential consistency")
            elif dim == "IR":
                improvements.append("Better integrate intermediate reasoning")

    # Based on failure modes
    if score.failure_summary:
        for mode in score.failure_summary.by_mode:
            if mode == FailureMode.PHASE_SKIP:
                improvements.append("Don't skip required phases")
            elif mode == FailureMode.ORDER_VIOLATION:
                improvements.append("Maintain correct phase order")
            elif mode == FailureMode.LEAKAGE:
                improvements.append("Avoid content leakage outside phases")

    return list(set(improvements))[:5]  # Dedupe and limit


# =============================================================================
# CLI INTEGRATION
# =============================================================================

def add_pattern_args(parser: argparse.ArgumentParser):
    """Add pattern-specific arguments to CLI parser."""
    pattern_group = parser.add_argument_group("Pattern Evaluation")

    pattern_group.add_argument(
        "--pattern",
        choices=get_available_patterns(),
        help="Pattern to evaluate (auto-detected if not specified)",
    )

    pattern_group.add_argument(
        "--pattern-output",
        type=str,
        help="Model output to evaluate (or path to file containing output)",
    )

    pattern_group.add_argument(
        "--pattern-runs",
        type=int,
        default=DEFAULT_NUM_RUNS,
        help=f"Number of evaluation runs (default: {DEFAULT_NUM_RUNS})",
    )

    pattern_group.add_argument(
        "--quick-pattern",
        action="store_true",
        help="Single-run pattern evaluation (faster but less robust)",
    )


def run_pattern_evaluation(args) -> int:
    """
    Run pattern evaluation from CLI args.

    Args:
        args: Parsed argument namespace

    Returns:
        Exit code (0=success, 1=failure)
    """
    from tools.llm.llm_client import LLMClient

    # Load model output
    output_arg = args.pattern_output
    if output_arg:
        output_path = Path(output_arg)
        if output_path.exists():
            model_output = output_path.read_text(encoding="utf-8")
        else:
            model_output = output_arg
    else:
        print("Error: --pattern-output required for pattern evaluation", file=sys.stderr)
        return 1

    # Initialize LLM client
    model = getattr(args, 'model', None) or "local:phi4mini"
    client = LLMClient(model=model)

    # Run evaluation
    result = evaluate_with_pattern(
        prompt_path=args.path,
        model_output=model_output,
        llm_client=client,
        pattern_name=args.pattern,
        num_runs=args.pattern_runs,
        quick=args.quick_pattern,
    )

    # Output results
    if getattr(args, 'json', False):
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"Pattern Evaluation: {result.file}")
        print(f"{'='*60}")
        print(f"Pattern: {result.pattern_name}")
        print(f"Score: {result.score:.1f} ({result.grade})")
        print(f"Hard Gates: {'PASS' if result.passes_hard_gates else 'FAIL'}")
        print(f"\nDimension Scores:")
        for dim, score in result.dimension_scores.items():
            print(f"  {dim}: {score:.2f}/5.0")
        if result.failure_modes:
            print(f"\nFailure Modes: {', '.join(result.failure_modes)}")
        if result.improvements:
            print(f"\nImprovements:")
            for imp in result.improvements:
                print(f"  - {imp}")
        print(f"{'='*60}\n")

    return 0 if result.passes_hard_gates else 1


# =============================================================================
# QUICK TEST
# =============================================================================

if __name__ == "__main__":
    print("Pattern evaluation integration module")
    print(f"Available patterns: {get_available_patterns()}")
