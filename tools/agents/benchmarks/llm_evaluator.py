#!/usr/bin/env python3
"""
LLM-Based Benchmark Evaluator
==============================

Uses an LLM judge to evaluate generated outputs against gold standards
with structured scoring rubrics (0.0-10.0 scale).

This is a generic evaluator that works for any benchmark type,
not just API design tasks.
"""

import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# =============================================================================
# SCORING RUBRIC (0.0 - 10.0 Scale)
# =============================================================================

SCORE_RUBRIC = {
    10.0: "Perfect - Flawless execution, all requirements met, exceeds expectations",
    9.0: "Excellent - Near-perfect, trivial gaps only, production-ready",
    8.0: "Very Good - Strong output, 1-2 minor issues, high quality",
    7.0: "Good - Solid work, meets most requirements, some improvements possible",
    6.0: "Adequate - Acceptable output, notable gaps but fundamentally correct",
    5.0: "Fair - Partially correct, significant gaps, needs improvement",
    4.0: "Below Average - Multiple issues, incomplete, misses key requirements",
    3.0: "Poor - Major deficiencies, barely usable",
    2.0: "Very Poor - Fundamental problems, largely incorrect",
    1.0: "Extremely Poor - Minimal effort, almost unusable",
    0.0: "Failed - Did not produce relevant output or completely wrong",
}

# Evaluation dimensions (generic, applicable to all task types)
EVALUATION_DIMENSIONS = {
    "completeness": {
        "description": "Does the output address all requirements from the task?",
        "weight": 0.25,
    },
    "correctness": {
        "description": "Is the output technically correct and follows best practices?",
        "weight": 0.25,
    },
    "quality": {
        "description": "Is the output well-structured, clear, and maintainable?",
        "weight": 0.20,
    },
    "specificity": {
        "description": "Does the output provide specific, actionable details rather than generic advice?",
        "weight": 0.15,
    },
    "alignment": {
        "description": "Does the output align with the gold standard expectations?",
        "weight": 0.15,
    },
}


# =============================================================================
# DATA CLASSES
# =============================================================================


@dataclass
class DimensionScore:
    """Score for a single evaluation dimension."""

    dimension: str
    score: float  # 0.0 - 10.0
    reasoning: str
    evidence: List[str] = field(default_factory=list)  # Specific quotes/examples
    weight: float = 0.2

    @property
    def weighted_score(self) -> float:
        return self.score * self.weight


@dataclass
class EvaluationResult:
    """Complete evaluation result for a single task."""

    task_id: str
    model: str
    benchmark_id: str
    timestamp: str

    # Scores
    dimension_scores: Dict[str, DimensionScore] = field(default_factory=dict)
    overall_score: float = 0.0
    grade: str = "F"

    # Content
    task_prompt: str = ""
    generated_output: str = ""
    gold_standard_summary: str = ""

    # Metadata
    duration_seconds: float = 0.0
    evaluator_model: str = ""

    # Analysis
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    improvement_suggestions: List[str] = field(default_factory=list)
    key_findings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        # Convert DimensionScore to dict
        result["dimension_scores"] = {
            k: asdict(v) for k, v in self.dimension_scores.items()
        }
        return result

    @staticmethod
    def grade_from_score(score: float) -> str:
        """Convert 0-10 score to letter grade."""
        if score >= 9.0:
            return "A"
        elif score >= 8.0:
            return "B"
        elif score >= 7.0:
            return "C"
        elif score >= 6.0:
            return "D"
        else:
            return "F"


# =============================================================================
# LLM EVALUATOR
# =============================================================================


def build_evaluation_prompt(
    task_prompt: str,
    generated_output: str,
    gold_standard: Dict[str, Any],
    dimensions: Dict[str, Dict[str, Any]] = None,
) -> str:
    """Build the evaluation prompt for the LLM judge."""

    if dimensions is None:
        dimensions = EVALUATION_DIMENSIONS

    # Build gold standard summary (generic)
    gold_summary_parts = []

    # Handle common gold standard fields
    if "required_components" in gold_standard:
        gold_summary_parts.append(
            f"Required Components: {gold_standard['required_components']}"
        )

    if "required_patterns" in gold_standard:
        gold_summary_parts.append(
            f"Required Patterns: {gold_standard['required_patterns']}"
        )

    if "key_decisions" in gold_standard:
        gold_summary_parts.append(
            f"Key Decisions/Concepts: {gold_standard['key_decisions']}"
        )

    if "expected_output" in gold_standard:
        gold_summary_parts.append(
            f"Expected Output: {gold_standard['expected_output']}"
        )

    if "api_endpoints" in gold_standard:
        endpoints = [
            f"{e.get('method', 'ANY')} {e.get('path', 'N/A')}"
            for e in gold_standard["api_endpoints"]
        ]
        gold_summary_parts.append(f"Expected Endpoints: {endpoints}")

    if "database_tables" in gold_standard:
        gold_summary_parts.append(
            f"Expected Tables/Schemas: {gold_standard['database_tables']}"
        )

    if "test_cases" in gold_standard:
        gold_summary_parts.append(
            f"Test Cases: {len(gold_standard['test_cases'])} defined"
        )

    # Add any other keys generically
    skip_keys = {
        "required_components",
        "required_patterns",
        "key_decisions",
        "expected_output",
        "api_endpoints",
        "database_tables",
        "test_cases",
        "task_id",
        "name",
        "version",
        "last_updated",
        "source_references",
        "prompt",
        "instruction",
    }
    for key, value in gold_standard.items():
        if key not in skip_keys and value:
            gold_summary_parts.append(f"{key.replace('_', ' ').title()}: {value}")

    gold_summary = (
        "\n".join(gold_summary_parts)
        if gold_summary_parts
        else "No specific gold standard defined."
    )

    # Build dimensions section
    dimensions_text = "\n".join(
        [
            f"- **{name}** (weight: {info['weight']}): {info['description']}"
            for name, info in dimensions.items()
        ]
    )

    # Build score rubric text
    rubric_text = "\n".join(
        [
            f"  {score}: {desc}"
            for score, desc in sorted(SCORE_RUBRIC.items(), reverse=True)
        ]
    )

    prompt = f"""You are an expert code/design evaluator. Evaluate the following generated output against the task requirements and gold standard.

## TASK PROMPT
{task_prompt}

## GOLD STANDARD EXPECTATIONS
{gold_summary}

## GENERATED OUTPUT
{generated_output}

## EVALUATION DIMENSIONS
Evaluate each dimension on a 0.0-10.0 scale:
{dimensions_text}

## SCORING RUBRIC
{rubric_text}

## INSTRUCTIONS
1. Analyze the generated output against the task requirements
2. Compare with gold standard expectations
3. Score each dimension with detailed reasoning
4. Provide specific evidence (quotes, examples) for each score
5. List strengths, weaknesses, and improvement suggestions

## REQUIRED OUTPUT FORMAT
Respond with a valid JSON object (no markdown code blocks):
{{
  "dimension_scores": {{
    "completeness": {{
      "score": <0.0-10.0>,
      "reasoning": "<detailed explanation>",
      "evidence": ["<specific quote or example>", ...]
    }},
    "correctness": {{
      "score": <0.0-10.0>,
      "reasoning": "<detailed explanation>",
      "evidence": ["<specific quote or example>", ...]
    }},
    "quality": {{
      "score": <0.0-10.0>,
      "reasoning": "<detailed explanation>",
      "evidence": ["<specific quote or example>", ...]
    }},
    "specificity": {{
      "score": <0.0-10.0>,
      "reasoning": "<detailed explanation>",
      "evidence": ["<specific quote or example>", ...]
    }},
    "alignment": {{
      "score": <0.0-10.0>,
      "reasoning": "<detailed explanation>",
      "evidence": ["<specific quote or example>", ...]
    }}
  }},
  "strengths": ["<strength 1>", "<strength 2>", ...],
  "weaknesses": ["<weakness 1>", "<weakness 2>", ...],
  "improvement_suggestions": ["<suggestion 1>", "<suggestion 2>", ...],
  "key_findings": ["<finding 1>", "<finding 2>", ...]
}}"""

    return prompt


def parse_evaluation_response(response: str) -> Dict[str, Any]:
    """Parse the LLM evaluation response."""
    # Try to extract JSON from the response
    response = response.strip()

    # Remove markdown code blocks if present
    if response.startswith("```"):
        # Find the end of the opening code fence
        first_newline = response.find("\n")
        if first_newline != -1:
            response = response[first_newline + 1 :]
        # Remove closing fence
        if response.endswith("```"):
            response = response[:-3].strip()

    # Try direct JSON parse
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        pass

    # Try to find JSON object in response
    json_match = re.search(r"\{[\s\S]*\}", response)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

    # Return empty structure on parse failure
    return {
        "dimension_scores": {},
        "strengths": [],
        "weaknesses": ["Failed to parse evaluation response"],
        "improvement_suggestions": [],
        "key_findings": ["Evaluation parsing error"],
        "parse_error": True,
        "raw_response": response[:500],
    }


def evaluate_with_llm(
    task_id: str,
    task_prompt: str,
    generated_output: str,
    gold_standard: Dict[str, Any],
    model: str,
    benchmark_id: str,
    evaluator_model: str = None,
    verbose: bool = False,
) -> EvaluationResult:
    """Evaluate generated output using an LLM judge.

    Args:
        task_id: Unique task identifier
        task_prompt: Original task prompt
        generated_output: The generated output to evaluate
        gold_standard: Gold standard data for comparison
        model: Model that generated the output
        benchmark_id: Benchmark identifier
        evaluator_model: Model to use for evaluation (defaults to same as generation)
        verbose: Print detailed output

    Returns:
        EvaluationResult with scores and analysis
    """
    from tools.llm.llm_client import LLMClient

    if evaluator_model is None:
        evaluator_model = model

    # Build evaluation prompt
    eval_prompt = build_evaluation_prompt(
        task_prompt=task_prompt,
        generated_output=generated_output,
        gold_standard=gold_standard,
    )

    if verbose:
        print(f"  [Evaluator] Using {evaluator_model} for evaluation...")

    # Call LLM (generate_text is a static method with model_name as first arg)
    start_time = datetime.now()

    try:
        response = LLMClient.generate_text(
            evaluator_model,  # model_name is first positional arg
            eval_prompt,  # prompt is second positional arg
            max_tokens=2000,
        )

        duration = (datetime.now() - start_time).total_seconds()

        if verbose:
            print(f"  [Evaluator] Completed in {duration:.1f}s")

    except Exception as e:
        if verbose:
            print(f"  [Evaluator] Error: {e}")

        # Return error result
        return EvaluationResult(
            task_id=task_id,
            model=model,
            benchmark_id=benchmark_id,
            timestamp=datetime.now().isoformat(),
            overall_score=0.0,
            grade="F",
            task_prompt=task_prompt[:500],
            generated_output=generated_output[:500],
            evaluator_model=evaluator_model,
            weaknesses=[f"Evaluation failed: {str(e)}"],
        )

    # Parse response
    parsed = parse_evaluation_response(response)

    # Build dimension scores
    dimension_scores = {}
    total_weighted = 0.0

    for dim_name, dim_info in EVALUATION_DIMENSIONS.items():
        dim_data = parsed.get("dimension_scores", {}).get(dim_name, {})
        score = float(dim_data.get("score", 0.0))

        # Clamp score to valid range
        score = max(0.0, min(10.0, score))

        dim_score = DimensionScore(
            dimension=dim_name,
            score=score,
            reasoning=dim_data.get("reasoning", "No reasoning provided"),
            evidence=dim_data.get("evidence", []),
            weight=dim_info["weight"],
        )
        dimension_scores[dim_name] = dim_score
        total_weighted += dim_score.weighted_score

    # Calculate overall score
    overall_score = total_weighted
    grade = EvaluationResult.grade_from_score(overall_score)

    # Build gold standard summary for storage
    gold_summary = json.dumps(
        {k: v for k, v in gold_standard.items() if k not in ["prompt", "instruction"]},
        indent=2,
    )[:1000]

    return EvaluationResult(
        task_id=task_id,
        model=model,
        benchmark_id=benchmark_id,
        timestamp=datetime.now().isoformat(),
        dimension_scores=dimension_scores,
        overall_score=overall_score,
        grade=grade,
        task_prompt=task_prompt,
        generated_output=generated_output,
        gold_standard_summary=gold_summary,
        duration_seconds=duration,
        evaluator_model=evaluator_model,
        strengths=parsed.get("strengths", []),
        weaknesses=parsed.get("weaknesses", []),
        improvement_suggestions=parsed.get("improvement_suggestions", []),
        key_findings=parsed.get("key_findings", []),
    )


# =============================================================================
# OUTPUT FORMATTING
# =============================================================================


def print_evaluation_report(result: EvaluationResult, verbose: bool = True) -> None:
    """Print formatted evaluation report to console."""
    print("\n" + "=" * 70)
    print("LLM EVALUATION REPORT")
    print("=" * 70)

    print(f"\nTask: {result.task_id}")
    print(f"Model: {result.model}")
    print(f"Evaluator: {result.evaluator_model}")
    print(f"Benchmark: {result.benchmark_id}")

    print(f"\n{'─' * 50}")
    print(f"OVERALL SCORE: {result.overall_score:.1f}/10.0 (Grade: {result.grade})")
    print(f"{'─' * 50}")

    # Dimension scores
    print("\nDIMENSION SCORES:")
    for name, dim in sorted(result.dimension_scores.items()):
        bar = "█" * int(dim.score) + "░" * (10 - int(dim.score))
        print(f"  {name:15} {bar} {dim.score:.1f}/10 (w={dim.weight})")
        if verbose and dim.reasoning:
            # Wrap reasoning text
            reason_lines = [
                dim.reasoning[i : i + 55] for i in range(0, len(dim.reasoning), 55)
            ]
            for line in reason_lines[:2]:  # Limit to 2 lines
                print(f"                  {line}")

    # Strengths
    if result.strengths:
        print("\n[+] STRENGTHS:")
        for s in result.strengths[:5]:
            print(f"    - {s}")

    # Weaknesses
    if result.weaknesses:
        print("\n[-] WEAKNESSES:")
        for w in result.weaknesses[:5]:
            print(f"    - {w}")

    # Suggestions
    if result.improvement_suggestions and verbose:
        print("\n[>] SUGGESTIONS:")
        for s in result.improvement_suggestions[:3]:
            print(f"    - {s}")

    # Key findings
    if result.key_findings and verbose:
        print("\n[!] KEY FINDINGS:")
        for f in result.key_findings[:3]:
            print(f"    - {f}")


def save_evaluation_report(result: EvaluationResult, output_dir: Path) -> Path:
    """Save detailed evaluation report to files."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save JSON report
    json_file = output_dir / f"task_{result.task_id}_eval.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, indent=2)

    # Save Markdown report
    md_file = output_dir / f"task_{result.task_id}_eval.md"

    md_content = [
        f"# Evaluation Report: Task {result.task_id}",
        "",
        f"**Model:** {result.model}",
        f"**Evaluator:** {result.evaluator_model}",
        f"**Benchmark:** {result.benchmark_id}",
        f"**Timestamp:** {result.timestamp}",
        f"**Duration:** {result.duration_seconds:.1f}s",
        "",
        f"## Overall Score: {result.overall_score:.1f}/10.0 (Grade: {result.grade})",
        "",
        "## Dimension Scores",
        "",
        "| Dimension | Score | Weight | Weighted |",
        "|-----------|-------|--------|----------|",
    ]

    for name, dim in sorted(result.dimension_scores.items()):
        md_content.append(
            f"| {name.title()} | {dim.score:.1f} | {dim.weight} | {dim.weighted_score:.2f} |"
        )

    md_content.extend(
        [
            "",
            "### Detailed Reasoning",
            "",
        ]
    )

    for name, dim in sorted(result.dimension_scores.items()):
        md_content.extend(
            [
                f"#### {name.title()} ({dim.score:.1f}/10)",
                "",
                dim.reasoning,
                "",
            ]
        )
        if dim.evidence:
            md_content.append("**Evidence:**")
            for e in dim.evidence:
                md_content.append(f"- {e}")
            md_content.append("")

    # Strengths and weaknesses
    md_content.extend(
        [
            "## Strengths",
            "",
        ]
    )
    for s in result.strengths:
        md_content.append(f"- {s}")

    md_content.extend(
        [
            "",
            "## Weaknesses",
            "",
        ]
    )
    for w in result.weaknesses:
        md_content.append(f"- {w}")

    md_content.extend(
        [
            "",
            "## Improvement Suggestions",
            "",
        ]
    )
    for s in result.improvement_suggestions:
        md_content.append(f"- {s}")

    md_content.extend(
        [
            "",
            "## Key Findings",
            "",
        ]
    )
    for f in result.key_findings:
        md_content.append(f"- {f}")

    # Gold standard reference
    md_content.extend(
        [
            "",
            "## Gold Standard Reference",
            "",
            "```json",
            result.gold_standard_summary,
            "```",
            "",
            "## Generated Output Preview",
            "",
            "```",
            result.generated_output[:3000],
            "```" if len(result.generated_output) <= 3000 else "... (truncated)",
        ]
    )

    md_file.write_text("\n".join(md_content), encoding="utf-8")

    return md_file


# =============================================================================
# BATCH EVALUATION
# =============================================================================


@dataclass
class BatchEvaluationSummary:
    """Summary of batch evaluation results."""

    benchmark_id: str
    model: str
    evaluator_model: str
    timestamp: str
    output_directory: str

    total_tasks: int = 0
    evaluated_tasks: int = 0
    average_score: float = 0.0
    grade_distribution: Dict[str, int] = field(default_factory=dict)
    dimension_averages: Dict[str, float] = field(default_factory=dict)

    top_strengths: List[str] = field(default_factory=list)
    common_weaknesses: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def summarize_batch_results(results: List[EvaluationResult]) -> BatchEvaluationSummary:
    """Summarize batch evaluation results."""
    if not results:
        return BatchEvaluationSummary(
            benchmark_id="",
            model="",
            evaluator_model="",
            timestamp=datetime.now().isoformat(),
            output_directory="",
        )

    first = results[0]

    # Calculate averages
    scores = [r.overall_score for r in results]
    avg_score = sum(scores) / len(scores)

    # Grade distribution
    grades = [r.grade for r in results]
    grade_dist = {g: grades.count(g) for g in set(grades)}

    # Dimension averages
    dim_totals: Dict[str, List[float]] = {}
    for r in results:
        for dim_name, dim_score in r.dimension_scores.items():
            if dim_name not in dim_totals:
                dim_totals[dim_name] = []
            dim_totals[dim_name].append(dim_score.score)

    dim_avgs = {name: sum(vals) / len(vals) for name, vals in dim_totals.items()}

    # Collect all strengths/weaknesses
    all_strengths = []
    all_weaknesses = []
    for r in results:
        all_strengths.extend(r.strengths)
        all_weaknesses.extend(r.weaknesses)

    # Get most common (simple frequency)
    from collections import Counter

    top_strengths = [s for s, _ in Counter(all_strengths).most_common(5)]
    common_weaknesses = [w for w, _ in Counter(all_weaknesses).most_common(5)]

    return BatchEvaluationSummary(
        benchmark_id=first.benchmark_id,
        model=first.model,
        evaluator_model=first.evaluator_model,
        timestamp=datetime.now().isoformat(),
        output_directory="",
        total_tasks=len(results),
        evaluated_tasks=len(results),
        average_score=avg_score,
        grade_distribution=grade_dist,
        dimension_averages=dim_avgs,
        top_strengths=top_strengths,
        common_weaknesses=common_weaknesses,
    )
