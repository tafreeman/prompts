"""Pattern evaluator for advanced prompt scoring.

Implements multi-run LLM-as-judge evaluation with hard gates,
statistical aggregation, and deterministic failure classification.
"""

import json
import re
import statistics
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

from .failures import FailureMode, PatternFailureSummary
from .parser import ParseResult, parse_output


# =============================================================================
# CONFIGURATION
# =============================================================================

DEFAULT_NUM_RUNS = 20
DEFAULT_TEMPERATURE = 0.1
HARD_GATES = {
    "PC": 4,  # Phase Completeness ≥ 4
    "POI": 4,  # Pattern Ordering Integrity ≥ 4
    "CA": 4,  # Constraint Adherence ≥ 4
    "PR": 0.75,  # Pass Rate ≥ 75%
}


# =============================================================================
# DATA STRUCTURES
# =============================================================================


@dataclass
class DimensionScore:
    """Score for a single evaluation dimension."""

    name: str
    abbreviation: str
    score: float
    max_score: float = 5.0
    weight: float = 1.0
    rationale: str = ""

    @property
    def normalized(self) -> float:
        """Normalized score (0-1)."""

        return self.score / self.max_score

    @property
    def weighted(self) -> float:
        """Weighted score."""

        return self.score * self.weight

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "abbreviation": self.abbreviation,
            "score": self.score,
            "max_score": self.max_score,
            "weight": self.weight,
            "normalized": round(self.normalized, 3),
            "rationale": self.rationale,
        }


@dataclass
class SingleRunResult:
    """Result from a single evaluation run."""
    run_id: int
    dimensions: Dict[str, DimensionScore] = field(default_factory=dict)
    failure_modes: List[FailureMode] = field(default_factory=list)
    raw_judge_output: str = ""
    parse_success: bool = True
    error: Optional[str] = None

    @property
    def composite_score(self) -> float:
        """Weighted average of all dimension scores."""
        if not self.dimensions:
            return 0.0
        total_weight = sum(d.weight for d in self.dimensions.values())
        if total_weight == 0:
            return 0.0
        return sum(d.weighted for d in self.dimensions.values()) / total_weight

    @property
    def passed_hard_gates(self) -> bool:
        """Check if this run passes all hard gates."""
        for gate, threshold in HARD_GATES.items():
            if gate in self.dimensions:
                if self.dimensions[gate].score < threshold:
                    return False
        return True

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "dimensions": {k: v.to_dict() for k, v in self.dimensions.items()},
            "failure_modes": [fm.value for fm in self.failure_modes],
            "composite_score": round(self.composite_score, 3),
            "passed_hard_gates": self.passed_hard_gates,
            "parse_success": self.parse_success,
            "error": self.error,
        }


@dataclass
class PatternScore:
    """
    Aggregated pattern evaluation score.

    Combines multiple runs using median aggregation for robustness.
    """
    pattern_name: str
    runs: List[SingleRunResult] = field(default_factory=list)

    # Aggregated scores (computed after all runs)
    dimension_medians: Dict[str, float] = field(default_factory=dict)
    dimension_stdevs: Dict[str, float] = field(default_factory=dict)

    # Statistical metrics
    pass_rate: float = 0.0
    perfect_pass_rate: float = 0.0  # Passes all hard gates
    mean_phase_fidelity: float = 0.0
    critical_failure_rate: float = 0.0

    # Failure summary
    failure_summary: Optional[PatternFailureSummary] = None

    # Final verdict
    overall_score: float = 0.0
    passes_hard_gates: bool = False

    def compute_aggregates(self):
        """Compute aggregate statistics from runs."""
        if not self.runs:
            return

        # Collect all dimension names
        all_dims = set()
        for run in self.runs:
            all_dims.update(run.dimensions.keys())

        # Compute medians and stdevs per dimension
        for dim in all_dims:
            scores = [
                run.dimensions[dim].score
                for run in self.runs
                if dim in run.dimensions
            ]
            if scores:
                self.dimension_medians[dim] = statistics.median(scores)
                self.dimension_stdevs[dim] = statistics.stdev(scores) if len(scores) > 1 else 0.0

        # Pass rate (runs that completed successfully)
        successful_runs = [r for r in self.runs if r.parse_success]
        self.pass_rate = len(successful_runs) / len(self.runs) if self.runs else 0.0

        # Perfect pass rate (runs that pass hard gates)
        perfect_runs = [r for r in successful_runs if r.passed_hard_gates]
        self.perfect_pass_rate = len(perfect_runs) / len(self.runs) if self.runs else 0.0

        # Mean Phase Fidelity (if PIF dimension exists)
        if "PIF" in self.dimension_medians:
            self.mean_phase_fidelity = self.dimension_medians["PIF"] / 5.0

        # Critical failure rate
        all_failures = []
        for run in self.runs:
            all_failures.extend(run.failure_modes)
        critical = [
            f for f in all_failures
            if f in [
                FailureMode.MISSING_PHASE,
                FailureMode.PHASE_ORDER_VIOLATION,
                FailureMode.PREMATURE_TERMINATION,
            ]
        ]
        self.critical_failure_rate = len(critical) / len(all_failures) if all_failures else 0.0

        # Build failure summary
        self.failure_summary = PatternFailureSummary()
        for run in self.runs:
            for fm in run.failure_modes:
                # PatternFailureSummary.add_failure expects the mode/report as the
                # first positional arg (keyword name is mode_or_report).
                self.failure_summary.add_failure(fm)

        # Overall score = median of composite scores
        composites = [r.composite_score for r in successful_runs]
        self.overall_score = statistics.median(composites) if composites else 0.0

        # Hard gates check on aggregated values
        self.passes_hard_gates = self._check_aggregated_hard_gates()

    def _check_aggregated_hard_gates(self) -> bool:
        """Check hard gates on aggregated median values."""
        for gate, threshold in HARD_GATES.items():
            if gate == "PR":
                if self.pass_rate < threshold:
                    return False
            elif gate in self.dimension_medians:
                if self.dimension_medians[gate] < threshold:
                    return False
        return True

    def to_dict(self) -> dict:
        self.compute_aggregates()
        return {
            "pattern_name": self.pattern_name,
            "num_runs": len(self.runs),
            "dimension_medians": {k: round(v, 3) for k, v in self.dimension_medians.items()},
            "dimension_stdevs": {k: round(v, 3) for k, v in self.dimension_stdevs.items()},
            "pass_rate": round(self.pass_rate, 3),
            "perfect_pass_rate": round(self.perfect_pass_rate, 3),
            "mean_phase_fidelity": round(self.mean_phase_fidelity, 3),
            "critical_failure_rate": round(self.critical_failure_rate, 3),
            "overall_score": round(self.overall_score, 3),
            "passes_hard_gates": self.passes_hard_gates,
            "failure_summary": self.failure_summary.to_dict() if self.failure_summary else None,
            "runs": [r.to_dict() for r in self.runs],
        }


# =============================================================================
# SCORING SCHEMA LOADER
# =============================================================================

def load_scoring_schema() -> Dict[str, Any]:
    """Load the pattern scoring schema."""
    schema_path = Path(__file__).parent.parent / "rubrics" / "pattern-scoring.yaml"
    if not schema_path.exists():
        raise FileNotFoundError(f"Scoring schema not found: {schema_path}")

    with open(schema_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_dimension_config(
    pattern_name: str,
    schema: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Get scoring dimensions for a pattern.

    Combines universal dimensions with pattern-specific ones.
    Returns list of dicts with 'name', 'abbreviation', 'description', 'weight'.
    """
    if schema is None:
        schema = load_scoring_schema()

    dimensions = []

    # Universal dimensions (dict format in schema)
    universal = schema.get("universal_dimensions", {})
    if isinstance(universal, dict):
        for name, config in universal.items():
            dimensions.append({
                "name": name,
                "abbreviation": config.get("id", name[:3].upper()),
                "description": config.get("description", ""),
                "weight": config.get("weight", 1.0),
            })
    elif isinstance(universal, list):
        dimensions.extend(universal)

    # Pattern-specific dimensions
    pattern_dims = schema.get("pattern_specific", {}).get(pattern_name, {})
    if isinstance(pattern_dims, dict):
        for name, config in pattern_dims.items():
            dimensions.append({
                "name": name,
                "abbreviation": config.get("id", name[:3].upper()),
                "description": config.get("description", ""),
                "weight": config.get("weight", 1.0),
            })
    elif isinstance(pattern_dims, list):
        dimensions.extend(pattern_dims)

    return dimensions


# =============================================================================
# JUDGE PROMPT BUILDER
# =============================================================================

def load_judge_template(pattern_name: str) -> str:
    """Load the judge prompt template for a pattern."""
    judges_dir = Path(__file__).parent.parent / "rubrics" / "judges"

    # Try pattern-specific first
    pattern_judge = judges_dir / "pattern_judge.yaml"
    if pattern_judge.exists():
        with open(pattern_judge, "r", encoding="utf-8") as f:
            templates = yaml.safe_load(f)

        # Get pattern-specific template
        pattern_instructions = templates.get("pattern_templates", {}).get(pattern_name, "")
        base_template = templates.get("user_template", "")

        return base_template.replace("{pattern_instructions}", pattern_instructions)

    # Fallback to base judge
    base_judge = judges_dir / "base_judge.yaml"
    if base_judge.exists():
        with open(base_judge, "r", encoding="utf-8") as f:
            return yaml.safe_load(f).get("system_prompt", "")

    return ""


def build_judge_prompt(
    prompt_content: str,
    model_output: str,
    pattern_name: str,
    dimensions: List[Dict[str, Any]],
    parse_result: ParseResult,
) -> str:
    """
    Build the complete judge prompt.

    Args:
        prompt_content: The original prompt being evaluated
        model_output: The model's response
        pattern_name: Expected pattern
        dimensions: Scoring dimensions to evaluate
        parse_result: Pre-parsed output IR

    Returns:
        Complete judge prompt string
    """
    template = load_judge_template(pattern_name)

    # Build dimensions section
    dim_text = "\n".join([
        f"- **{d['abbreviation']}** ({d['name']}): {d['description']} [Weight: {d.get('weight', 1.0)}]"
        for d in dimensions
    ])

    # Build phase summary from parse result
    phase_summary = "Detected phases:\n"
    for p in parse_result.phases:
        phase_summary += f"  - {p.type} (lines {p.line_start}-{p.line_end})\n"
    if parse_result.missing_phases:
        phase_summary += f"Missing phases: {', '.join(parse_result.missing_phases)}\n"
    if not parse_result.ordering_valid:
        phase_summary += "Ordering violations detected.\n"

    # Build expected output schema
    output_schema = {
        "scores": {d["abbreviation"]: {"score": 0, "rationale": ""} for d in dimensions},
        "failure_modes": [],
        "summary": "",
    }

    prompt = f"""## Evaluation Task

Evaluate the following prompt and its model output for conformance to the **{pattern_name.upper()}** pattern.

### Original Prompt
```
{prompt_content}
```

### Model Output
```
{model_output}
```

### Pre-parsed Analysis
{phase_summary}

### Scoring Dimensions
{dim_text}

### Instructions
1. Score each dimension from 1-5 (1=poor, 5=excellent)
2. Identify any failure modes from the taxonomy
3. Output ONLY valid JSON matching this schema:

```json
{json.dumps(output_schema, indent=2)}
```

{template}
"""
    return prompt


# =============================================================================
# JUDGE OUTPUT PARSER
# =============================================================================

def parse_judge_output(
    output: str,
    dimensions: List[Dict[str, Any]],
) -> Tuple[Dict[str, DimensionScore], List[FailureMode], Optional[str]]:
    """
    Parse the judge's JSON output into structured scores.

    Args:
        output: Raw judge output
        dimensions: Expected dimensions

    Returns:
        Tuple of (dimension_scores, failure_modes, error)
    """
    # Extract JSON from output (handle markdown code blocks)
    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', output)
    if json_match:
        json_str = json_match.group(1)
    else:
        # Try to find raw JSON
        json_match = re.search(r'\{[\s\S]*\}', output)
        if json_match:
            json_str = json_match.group(0)
        else:
            return {}, [], "No JSON found in judge output"

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        return {}, [], f"JSON parse error: {e}"

    # Extract dimension scores
    scores = {}
    raw_scores = data.get("scores", {})

    for dim in dimensions:
        abbrev = dim["abbreviation"]
        if abbrev in raw_scores:
            score_data = raw_scores[abbrev]
            if isinstance(score_data, dict):
                score_val = score_data.get("score", 0)
                rationale = score_data.get("rationale", "")
            else:
                score_val = score_data
                rationale = ""

            scores[abbrev] = DimensionScore(
                name=dim["name"],
                abbreviation=abbrev,
                score=float(score_val),
                weight=dim.get("weight", 1.0),
                rationale=rationale,
            )

    # Extract failure modes
    failures = []
    raw_failures = data.get("failure_modes", [])
    for fm in raw_failures:
        try:
            failures.append(FailureMode(fm))
        except ValueError:
            # Unknown failure mode, skip
            pass

    return scores, failures, None


# =============================================================================
# MAIN EVALUATOR
# =============================================================================

class PatternEvaluator:
    """
    Multi-run pattern evaluator with LLM-as-judge.

    Implements the evaluation framework with:
    - Multi-iteration execution (20 runs default)
    - Deterministic output parsing
    - Hard gate enforcement
    - Median aggregation
    - Failure taxonomy classification
    """

    def __init__(
        self,
        llm_client: Any,
        num_runs: int = DEFAULT_NUM_RUNS,
        temperature: float = DEFAULT_TEMPERATURE,
    ):
        """
        Initialize the evaluator.

        Args:
            llm_client: LLM client instance (e.g., from tools.llm_client)
            num_runs: Number of evaluation runs
            temperature: Sampling temperature for judge
        """
        self.llm_client = llm_client
        self.num_runs = num_runs
        self.temperature = temperature
        self.schema = load_scoring_schema()

    def evaluate_single(
        self,
        prompt_content: str,
        model_output: str,
        pattern_name: str,
        run_id: int = 0,
    ) -> SingleRunResult:
        """
        Perform a single evaluation run.

        Args:
            prompt_content: Original prompt
            model_output: Model's response
            pattern_name: Expected pattern
            run_id: Run identifier

        Returns:
            SingleRunResult with scores and failures
        """
        result = SingleRunResult(run_id=run_id)

        # Parse the output first
        try:
            parse_result = parse_output(model_output, pattern_name)
        except Exception as e:
            result.parse_success = False
            result.error = f"Parse error: {e}"
            return result

        # Get dimensions for this pattern
        dimensions = get_dimension_config(pattern_name, self.schema)

        # Build judge prompt
        judge_prompt = build_judge_prompt(
            prompt_content,
            model_output,
            pattern_name,
            dimensions,
            parse_result,
        )

        # Call LLM judge
        try:
            judge_response = self.llm_client.complete(
                prompt=judge_prompt,
                temperature=self.temperature,
            )
            result.raw_judge_output = judge_response
        except Exception as e:
            result.parse_success = False
            result.error = f"LLM error: {e}"
            return result

        # Parse judge output
        scores, failures, error = parse_judge_output(judge_response, dimensions)

        if error:
            result.parse_success = False
            result.error = error
            return result

        result.dimensions = scores
        result.failure_modes = failures

        # Add parse-detected failures
        if parse_result.missing_phases:
            if FailureMode.PHASE_SKIP not in result.failure_modes:
                result.failure_modes.append(FailureMode.PHASE_SKIP)
        if not parse_result.ordering_valid:
            if FailureMode.ORDER_VIOLATION not in result.failure_modes:
                result.failure_modes.append(FailureMode.ORDER_VIOLATION)
        if parse_result.leakage_detected:
            if FailureMode.LEAKAGE not in result.failure_modes:
                result.failure_modes.append(FailureMode.LEAKAGE)

        return result

    def evaluate(
        self,
        prompt_content: str,
        model_output: str,
        pattern_name: str,
    ) -> PatternScore:
        """
        Perform full multi-run evaluation.

        Args:
            prompt_content: Original prompt
            model_output: Model's response
            pattern_name: Expected pattern

        Returns:
            PatternScore with aggregated results
        """
        score = PatternScore(pattern_name=pattern_name)

        for i in range(self.num_runs):
            run_result = self.evaluate_single(
                prompt_content,
                model_output,
                pattern_name,
                run_id=i,
            )
            score.runs.append(run_result)

        score.compute_aggregates()
        return score

    def quick_evaluate(
        self,
        prompt_content: str,
        model_output: str,
        pattern_name: str,
    ) -> PatternScore:
        """
        Quick evaluation with single run (for testing/development).

        Args:
            prompt_content: Original prompt
            model_output: Model's response
            pattern_name: Expected pattern

        Returns:
            PatternScore with single run result
        """
        score = PatternScore(pattern_name=pattern_name)

        run_result = self.evaluate_single(
            prompt_content,
            model_output,
            pattern_name,
            run_id=0,
        )
        score.runs.append(run_result)
        score.compute_aggregates()

        return score


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def evaluate_pattern(
    prompt_content: str,
    model_output: str,
    pattern_name: str,
    llm_client: Any,
    num_runs: int = DEFAULT_NUM_RUNS,
) -> PatternScore:
    """
    Convenience function for pattern evaluation.

    Args:
        prompt_content: Original prompt
        model_output: Model's response
        pattern_name: Expected pattern
        llm_client: LLM client instance
        num_runs: Number of evaluation runs

    Returns:
        PatternScore with evaluation results
    """
    evaluator = PatternEvaluator(llm_client, num_runs=num_runs)
    return evaluator.evaluate(prompt_content, model_output, pattern_name)
