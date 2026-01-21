"""
Unified Prompt Scorer - Simple & Complex scoring aligned with rr.txt spec.

Two modes:
1. Standard scoring: 5 dimensions × 10 points = 100 (all prompts)
2. Pattern scoring: 7 universal + pattern-specific dimensions (advanced prompts)

Usage:
    from tools.prompteval.unified_scorer import score_prompt, score_pattern

    # Simple scoring for any prompt
    result = score_prompt("prompts/my-prompt.md", model="local:phi4mini")

    # Pattern scoring for advanced prompts
    result = score_pattern("prompts/advanced/CoVe.md", output="...", model="local:phi4mini")
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Dict, Union
import yaml
import statistics
import json


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class StandardScore:
    """Result from standard (simple) prompt scoring."""
    prompt_file: str
    scores: Dict[str, float]  # clarity, effectiveness, structure, specificity, completeness
    overall_score: float      # 0-100
    grade: str               # A, B, C, D, F
    passed: bool
    improvements: List[str] = field(default_factory=list)
    confidence: float = 1.0
    model: str = ""
    # Metadata
    eval_type: str = "standard"
    runs: int = 1
    temperature: float = 0.1
    successful_runs: int = 0

    def to_dict(self) -> dict:
        return {
            "eval_type": self.eval_type,
            "prompt_file": self.prompt_file,
            "model": self.model,
            "runs": self.runs,
            "successful_runs": self.successful_runs,
            "temperature": self.temperature,
            "scores": self.scores,
            "overall_score": self.overall_score,
            "grade": self.grade,
            "passed": self.passed,
            "improvements": self.improvements,
            "confidence": self.confidence,
        }


@dataclass
class PatternScore:
    """Result from pattern (complex) prompt scoring."""
    prompt_file: str
    pattern: str

    # Universal dimension scores (7 dimensions)
    universal_scores: Dict[str, float]  # PIF, POI, PC, CA, SRC, PR, IR

    # Pattern-specific scores
    pattern_scores: Dict[str, float]  # R1-R3, C1-C3, F1-F3, G1-G3

    # Aggregated
    overall_universal: float    # 0-35
    overall_pattern: float      # varies by pattern
    combined_score: float

    # Pass/fail
    hard_gates_passed: bool
    hard_gate_failures: List[str] = field(default_factory=list)
    failures: List[str] = field(default_factory=list)

    # Stats
    pass_rate: float = 1.0
    confidence: float = 1.0
    model: str = ""
    # Metadata
    eval_type: str = "pattern"
    runs: int = 20
    temperature: float = 0.1
    successful_runs: int = 0

    def to_dict(self) -> dict:
        return {
            "eval_type": self.eval_type,
            "prompt_file": self.prompt_file,
            "pattern": self.pattern,
            "model": self.model,
            "runs": self.runs,
            "successful_runs": self.successful_runs,
            "temperature": self.temperature,
            "universal_scores": self.universal_scores,
            "pattern_scores": self.pattern_scores,
            "overall_universal": self.overall_universal,
            "overall_pattern": self.overall_pattern,
            "combined_score": self.combined_score,
            "hard_gates_passed": self.hard_gates_passed,
            "hard_gate_failures": self.hard_gate_failures,
            "failures": self.failures,
            "pass_rate": self.pass_rate,
            "confidence": self.confidence,
        }


# =============================================================================
# RUBRIC LOADING
# =============================================================================

_RUBRIC_CACHE: Dict[str, dict] = {}


def load_unified_rubric() -> dict:
    """Load the unified scoring rubric."""
    if "unified" in _RUBRIC_CACHE:
        return _RUBRIC_CACHE["unified"]

    rubric_path = Path(__file__).parent.parent / "rubrics" / "unified-scoring.yaml"
    if not rubric_path.exists():
        raise FileNotFoundError(f"Unified rubric not found: {rubric_path}")

    with open(rubric_path, "r", encoding="utf-8") as f:
        rubric = yaml.safe_load(f)

    _RUBRIC_CACHE["unified"] = rubric
    return rubric


# =============================================================================
# JUDGE PROMPTS
# =============================================================================

STANDARD_JUDGE_PROMPT = """You are an expert prompt quality evaluator using example-anchored assessment.

# Instructions
Evaluate the following prompt on 5 dimensions (0-10 scale each).
For each dimension, compare against the example anchors to ensure consistent scoring.

**CRITICAL**: Before providing scores, you MUST:
1. Write a ThoughtChain analyzing the prompt systematically
2. Reference specific examples from the anchors
3. Then provide your scores

# Dimension 1: CLARITY (0-10)
**Definition**: Is the prompt unambiguous and easy to understand?

## Clarity Score Anchors with Examples:
**[Clarity: 10]** Absolute perfection - zero ambiguity, flawless instruction flow
    *Example*: "You are a JSON formatter. Given raw text input, output valid JSON with keys:
    'summary' (string, max 50 words), 'sentiment' (enum: positive/negative/neutral),
    'confidence' (float 0-1).
    Return only the JSON object, no explanation."

**[Clarity: 8]** Very good - clear purpose, 1-2 minor ambiguities
  *Example*: "Summarize the following text in a professional tone. Keep it brief and highlight the main points."

**[Clarity: 5]** Fair - main idea clear but multiple unclear parts
  *Example*: "Help me with my document. Make it better and more professional."

**[Clarity: 2]** Very poor - major rewrites needed to understand
  *Example*: "Do the thing with the stuff like we discussed. You know what I mean."

**[Clarity: 0]** Incomprehensible

1. **Clarity** (0-10): Is the prompt unambiguous and easy to understand?
   - 10: Absolute perfection - zero ambiguity, flawless instruction flow, self-explanatory
   - 9: Excellent - crystal clear purpose, negligible ambiguity (e.g., one minor term)
   - 8: Very good - clear purpose, 1-2 minor ambiguities that don't affect execution
   - 7: Good - clear intent, some terms could be clearer
   - 6: Adequate - understandable but requires some interpretation
   - 5: Fair - main idea clear but multiple unclear parts
# Dimension 2: EFFECTIVENESS (0-10)
**Definition**: Will it consistently produce quality output?

## Effectiveness Score Anchors with Examples:
**[Effectiveness: 10]** Produces excellent results 99%+ of the time, handles all edge cases
    *Example*: System prompt with explicit error handling, fallback behaviors, input validation rules,
    and comprehensive examples for each scenario.

**[Effectiveness: 8]** Good results 90%+ of the time, decent edge case handling
    *Example*: "Translate the following text to French.
    If text contains technical terms, keep them in English with French explanation in parentheses.
    If input is empty, respond 'No text provided.'"

**[Effectiveness: 5]** Acceptable results 65%+ of time, some inconsistency
  *Example*: "Translate this to French and make it sound natural."

**[Effectiveness: 2]** Frequently fails, rarely produces usable output
  *Example*: "Make this French."

**[Effectiveness: 0]** Never produces usable output

# Dimension 3: STRUCTURE (0-10)
**Definition**: How well organized and formatted?

## Structure Score Anchors with Examples:
**[Structure: 10]** Perfect professional formatting, optimal hierarchy, publication-ready
    *Example*: Prompt with clear # headings, numbered steps, bullet lists for constraints,
    ```code blocks``` for examples, logical flow from context → task → output format.

**[Structure: 8]** Very good formatting, well-organized, 1-2 small issues
  *Example*: Prompt with clear sections but could benefit from numbered constraints instead of prose.

**[Structure: 5]** Fair structure, inconsistent formatting
  *Example*: Mix of bullets and prose, sections exist but unclear boundaries.

**[Structure: 2]** Very poor, wall of text with minimal breaks
  *Example*: Single dense paragraph with all instructions run together.

**[Structure: 0]** Completely unformatted/unreadable

# Dimension 4: SPECIFICITY (0-10)
**Definition**: How specific and actionable?

## Specificity Score Anchors with Examples:
**[Specificity: 10]** Perfectly specific, unambiguous constraints, measurable success criteria
    *Example*: "Output: 3-5 bullet points, each 10-20 words, using active voice, present tense, no jargon. Include
    at least one statistic per bullet."

**[Specificity: 8]** Very specific, good constraints, minor improvements possible
  *Example*: "Summarize in 3-5 bullet points, keeping each point brief and professional."

**[Specificity: 5]** Somewhat vague, several unclear expectations
  *Example*: "Summarize briefly in bullet points."

**[Specificity: 2]** Extremely vague, almost no constraints
  *Example*: "Summarize this."

**[Specificity: 0]** Completely vague/unusable

# Dimension 5: COMPLETENESS (0-10)
**Definition**: Has all necessary components?

## Completeness Score Anchors with Examples:
**[Completeness: 10]** Has everything: context, instructions, examples, output format, error handling, edge cases
    *Example*: Prompt includes role, task description, 2+ input/output examples, explicit format spec,
    error handling instructions, and edge case guidance.

**[Completeness: 8]** Has most components, small gaps
  *Example*: Has role, task, format, examples but no error handling specified.

**[Completeness: 5]** Fair, missing several components (e.g., no examples)
  *Example*: Has clear task and format but no examples or edge case handling.

**[Completeness: 2]** Very incomplete, bare minimum
  *Example*: Just the core task with no supporting elements.

**[Completeness: 0]** Empty or no useful content

---
# Required Response Format

**IMPORTANT**: You MUST follow this exact format:

## ThoughtChain (Required)
First, analyze the prompt by explicitly comparing to the example anchors above:
- What clarity level does it most closely match?
- What effectiveness level?
- Structure level?
- Specificity level?
- Completeness level?

## Final Scores
After your ThoughtChain analysis, output ONLY this JSON:
```json
{{
  "thoughtchain": "<your 2-3 sentence analysis referencing specific anchor examples>",
  "scores": {{
    "clarity": <0-10>,
    "effectiveness": <0-10>,
    "structure": <0-10>,
    "specificity": <0-10>,
    "completeness": <0-10>
  }},
  "justifications": {{
    "clarity": "<why this score, referencing anchors>",
    "effectiveness": "<why this score>",
    "structure": "<why this score>",
    "specificity": "<why this score>",
    "completeness": "<why this score>"
  }},
  "improvements": ["<specific improvement 1>", "<specific improvement 2>"],
  "confidence": <0.0-1.0>
}}
```

PROMPT TO EVALUATE:
---
{prompt_content}
---
"""


PATTERN_JUDGE_PROMPT = """You are a deterministic pattern execution evaluator.

You evaluate whether a prompt RELIABLY INDUCES a specific reasoning pattern.
You do NOT judge answer quality. You judge STRUCTURAL conformance.

Pattern: {pattern_name}
Expected phases: {phases}
State machine: {state_machine}

Evaluate these UNIVERSAL dimensions (0-5 scale):

A. **PIF** - Pattern Invocation Fidelity: Did model attempt the pattern?
   0=Not invoked, 3=Explicit but flawed, 5=Explicit & clean

B. **POI** - Phase Ordering Integrity: Correct order? (HARD GATE ≥4)
   0=Random, 3=Mostly correct, 5=Strictly ordered

C. **PC** - Phase Completeness: All phases present? (HARD GATE ≥4)
   0=No phases, 3=Most present, 5=All with proper content

D. **CA** - Constraint Adherence: Constraints followed? (HARD GATE ≥4)
   0=None followed, 3=Most followed, 5=Perfect adherence

E. **SRC** - Self-Reference Correctness: Is self-reference accurate?
   0=None when required, 3=With errors, 5=Precise

F. **PR** - Pattern Robustness: % of runs pattern executes (HARD GATE ≥0.75)
   Estimate based on prompt structure

G. **IR** - Interference Resistance: Prevents collapse to simpler pattern?
   0=Always collapses, 3=Usually maintains, 5=Never collapses

{pattern_specific_instructions}

Output ONLY valid JSON:
```json
{{
  "universal_scores": {{
    "PIF": <0-5>,
    "POI": <0-5>,
    "PC": <0-5>,
    "CA": <0-5>,
    "SRC": <0-5>,
    "PR": <0.0-1.0>,
    "IR": <0-5>
  }},
  "pattern_scores": {{
    {pattern_score_fields}
  }},
  "failures": ["<failure mode if any>"],
  "confidence": <0.0-1.0>
}}
```

PROMPT:
---
{prompt_content}
---

MODEL OUTPUT TO EVALUATE:
---
{model_output}
---
"""


PATTERN_SPECIFIC_INSTRUCTIONS = {
    "react": """
Also evaluate ReAct-specific dimensions:
- **R1** (Thought/Action Separation): Are actions tool-like? No analysis inside action?
- **R2** (Observation Binding): Are observations used in next thought?
- **R3** (Termination Discipline): Does it stop looping appropriately?
""",
    "cove": """
Also evaluate CoVe-specific dimensions:
- **C1** (Verification Question Quality): Independent and non-leading?
- **C2** (Evidence Independence): Verification isn't just rephrasing?
- **C3** (Revision Delta): Final answer changes when verification fails?
""",
    "reflexion": """
Also evaluate Reflexion-specific dimensions:
- **F1** (Critique Specificity): References concrete failures?
- **F2** (Memory Utilization): Reflection actually used?
- **F3** (Improvement Signal): Measurable change between attempts?
""",
    "rag": """
Also evaluate RAG-specific dimensions:
- **G1** (Retrieval Trigger Accuracy): Calls retrieval only when needed?
- **G2** (Evidence Grounding): Claims trace to sources?
- **G3** (Citation Discipline): No uncited claims?
""",
}


PATTERN_SCORE_FIELDS = {
    "react": '"R1": <0-5>, "R2": <0-5>, "R3": <0-5>',
    "cove": '"C1": <0-5>, "C2": <0-5>, "C3": <0-5>',
    "reflexion": '"F1": <0-5>, "F2": <0-5>, "F3": <0-5>',
    "rag": '"G1": <0-5>, "G2": <0-5>, "G3": <0-5>',
}


PATTERN_PHASES = {
    "react": ["Thought", "Action", "Observation", "Final Answer"],
    "cove": ["Draft Answer", "Verification Questions", "Independent Checks", "Revised Answer"],
    "reflexion": ["Attempt", "Self-Critique", "Reflection Memory", "Improved Attempt"],
    "rag": ["Query Decomposition", "Retrieval Call", "Evidence Integration", "Answer with Citations"],
}


PATTERN_STATE_MACHINES = {
    "react": "Thought → Action → Observation → (repeat) → Answer",
    "cove": "Draft → Verification → Independent → Revised",
    "reflexion": "Attempt → Critique → Memory → Improved",
    "rag": "Query → Retrieve → Integrate → Cite",
}


# =============================================================================
# GRADE CALCULATION
# =============================================================================

def get_grade(score: float, max_score: float = 100) -> str:
    """Convert score to letter grade."""
    percent = (score / max_score) * 100
    if percent >= 90:
        return "A"
    if percent >= 80:
        return "B"
    if percent >= 70:
        return "C"
    if percent >= 60:
        return "D"
    return "F"


# =============================================================================
# STANDARD SCORING
# =============================================================================

def score_prompt(
    prompt_path: Union[str, Path],
    model: str = "local:phi4mini",
    runs: int = 1,
    temperature: float = 0.1,
    llm_client=None,
    verbose: bool = False,
) -> StandardScore:
    """
    Score a prompt using standard (simple) 5-dimension rubric.

    Args:
        prompt_path: Path to prompt file
        model: Model to use for judging
        runs: Number of runs for stability (use 1 for quick, 20 for robust)
        temperature: Judge temperature
        llm_client: Optional pre-configured LLM client
        verbose: If True, print detailed progress and raw responses

    Returns:
        StandardScore with 0-100 overall score
    """
    prompt_path = Path(prompt_path)

    # Load prompt content
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_content = f.read()

    # Load rubric for weights
    rubric = load_unified_rubric()
    weights = {
        name: dim["weight"]
        for name, dim in rubric["standard"]["dimensions"].items()
    }

    # Build judge prompt
    judge_prompt = STANDARD_JUDGE_PROMPT.format(prompt_content=prompt_content)

    # Run judge
    if llm_client is None:
        from ..llm.llm_client import LLMClient
        llm_client = LLMClient

    all_scores = []
    for i in range(runs):
        if verbose:
            print(f"\n{'='*60}")
            print(f"Run {i+1}/{runs}")
            print(f"{'='*60}")
        try:
            response = llm_client.generate_text(
                model_name=model,
                prompt=judge_prompt,
                temperature=temperature,
            )

            if verbose:
                preview = response[:500]
                suffix = "..." if len(response) > 500 else ""
                print(f"\n📝 Raw Response:\n{preview}{suffix}")

            # Parse JSON from response
            scores = _parse_standard_response(response)
            if scores:
                all_scores.append(scores)
                if verbose:
                    print(f"\n✅ Parsed scores: {scores.get('scores', {})}")
            else:
                if verbose:
                    print("\n⚠️ Failed to parse response")
        except Exception as e:
            print(f"Run {i+1} failed: {e}")
            if verbose:
                import traceback
                traceback.print_exc()

    if not all_scores:
        return StandardScore(
            prompt_file=str(prompt_path),
            scores={},
            overall_score=0,
            grade="F",
            passed=False,
            improvements=["Evaluation failed"],
            model=model,
        )

    # Aggregate scores (median for robustness)
    final_scores = {}
    for dim in ["clarity", "effectiveness", "structure", "specificity", "completeness"]:
        values = [s["scores"].get(dim, 0) for s in all_scores if "scores" in s]
        final_scores[dim] = statistics.median(values) if values else 0

    # Calculate weighted overall score
    overall = sum(final_scores[dim] * weights[dim] * 10 for dim in final_scores)

    # Aggregate improvements
    all_improvements = []
    for s in all_scores:
        all_improvements.extend(s.get("improvements", []))
    # Deduplicate
    improvements = list(dict.fromkeys(all_improvements))[:5]

    # Confidence
    confidences = [s.get("confidence", 1.0) for s in all_scores]
    confidence = statistics.median(confidences) if confidences else 1.0

    return StandardScore(
        prompt_file=str(prompt_path),
        scores=final_scores,
        overall_score=round(overall, 1),
        grade=get_grade(overall),
        passed=overall >= 70,
        improvements=improvements,
        confidence=confidence,
        model=model,
        eval_type="standard",
        runs=runs,
        temperature=temperature,
        successful_runs=len(all_scores),
    )


def _parse_standard_response(response: str) -> Optional[dict]:
    """Parse JSON from judge response with ThoughtChain support.

    Handles both new format (with thoughtchain/justifications) and legacy format.
    Also supports choice-based score extraction as fallback (gh-models pattern).
    """
    import re

    # Try to find JSON block
    json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
    if json_match:
        try:
            parsed = json.loads(json_match.group(1))
            return _normalize_standard_result(parsed)
        except json.JSONDecodeError:
            pass

    # Try direct JSON parse
    try:
        parsed = json.loads(response)
        return _normalize_standard_result(parsed)
    except json.JSONDecodeError:
        pass

    # Try to find JSON object
    json_match = re.search(r'\{.*\}', response, re.DOTALL)
    if json_match:
        try:
            parsed = json.loads(json_match.group())
            return _normalize_standard_result(parsed)
        except json.JSONDecodeError:
            pass

    # Fallback: Choice-based extraction (gh-models pattern)
    # Look for patterns like "[Clarity: 8]" or "**Clarity**: 8"
    scores = _extract_choice_scores(response)
    if scores:
        return {
            "scores": scores,
            "improvements": [],
            "confidence": 0.7,  # Lower confidence for choice-extracted scores
        }

    return None


def _extract_choice_scores(response: str) -> Optional[dict]:
    """Extract scores using choice-based pattern matching (gh-models style).

    Looks for patterns like:
    - [Clarity: 8]
    - **Clarity**: 8
    - Clarity: 8/10
    - clarity = 8
    """
    import re

    dimensions = ["clarity", "effectiveness", "structure", "specificity", "completeness"]
    scores = {}

    for dim in dimensions:
        # Pattern 1: [Dimension: N]
        match = re.search(rf'\[{dim}:\s*(\d+)\]', response, re.IGNORECASE)
        if match:
            scores[dim] = min(10, int(match.group(1)))
            continue

        # Pattern 2: **Dimension**: N or **Dimension** N
        match = re.search(rf'\*\*{dim}\*\*:?\s*(\d+)', response, re.IGNORECASE)
        if match:
            scores[dim] = min(10, int(match.group(1)))
            continue

        # Pattern 3: Dimension: N/10
        match = re.search(rf'{dim}:\s*(\d+)/10', response, re.IGNORECASE)
        if match:
            scores[dim] = min(10, int(match.group(1)))
            continue

        # Pattern 4: dimension = N
        match = re.search(rf'{dim}\s*[=:]\s*(\d+)', response, re.IGNORECASE)
        if match:
            scores[dim] = min(10, int(match.group(1)))
            continue

    # Only return if we found at least 3 dimensions
    return scores if len(scores) >= 3 else None


def _normalize_standard_result(parsed: dict) -> dict:
    """Normalize parsed response to standard format, preserving thoughtchain."""
    result = {
        "scores": parsed.get("scores", {}),
        "improvements": parsed.get("improvements", []),
        "confidence": parsed.get("confidence", 1.0),
    }

    # Preserve thoughtchain and justifications if present (new format)
    if "thoughtchain" in parsed:
        result["thoughtchain"] = parsed["thoughtchain"]
    if "justifications" in parsed:
        result["justifications"] = parsed["justifications"]

    return result


# =============================================================================
# PATTERN SCORING
# =============================================================================

def score_pattern(
    prompt_path: Union[str, Path],
    model_output: str,
    pattern: Optional[str] = None,
    model: str = "local:phi4mini",
    runs: int = 20,
    temperature: float = 0.1,
    llm_client=None,
) -> PatternScore:
    """
    Score a prompt using pattern (complex) evaluation.

    Args:
        prompt_path: Path to prompt file
        model_output: The model's output to evaluate
        pattern: Pattern type (react, cove, reflexion, rag). Auto-detected if None.
        model: Model to use for judging
        runs: Number of runs (20 minimum for robust results)
        temperature: Judge temperature
        llm_client: Optional pre-configured LLM client

    Returns:
        PatternScore with universal and pattern-specific scores
    """
    prompt_path = Path(prompt_path)

    # Load prompt content
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_content = f.read()

    # Auto-detect pattern if not specified
    if pattern is None:
        pattern = _detect_pattern(prompt_content)
    pattern = pattern.lower()

    if pattern not in PATTERN_PHASES:
        allowed = list(PATTERN_PHASES.keys())
        raise ValueError(f"Unknown pattern: {pattern}. Must be one of: {allowed}")

    # Build judge prompt
    judge_prompt = PATTERN_JUDGE_PROMPT.format(
        pattern_name=pattern.upper(),
        phases=", ".join(PATTERN_PHASES[pattern]),
        state_machine=PATTERN_STATE_MACHINES[pattern],
        pattern_specific_instructions=PATTERN_SPECIFIC_INSTRUCTIONS.get(pattern, ""),
        pattern_score_fields=PATTERN_SCORE_FIELDS.get(pattern, ""),
        prompt_content=prompt_content,
        model_output=model_output,
    )

    # Run judge
    if llm_client is None:
        from ..llm.llm_client import LLMClient
        llm_client = LLMClient

    all_results = []
    for i in range(runs):
        try:
            response = llm_client.generate_text(
                model_name=model,
                prompt=judge_prompt,
                temperature=temperature,
            )

            result = _parse_pattern_response(response)
            if result:
                all_results.append(result)
        except Exception as e:
            print(f"Run {i+1} failed: {e}")

    if not all_results:
        return PatternScore(
            prompt_file=str(prompt_path),
            pattern=pattern,
            universal_scores={},
            pattern_scores={},
            overall_universal=0,
            overall_pattern=0,
            combined_score=0,
            hard_gates_passed=False,
            hard_gate_failures=["Evaluation failed"],
            failures=["evaluation_failure"],
            model=model,
        )

    # Aggregate universal scores (median, trim outliers)
    universal_scores = _aggregate_universal_scores(all_results)

    # Aggregate pattern-specific scores
    pattern_scores = _aggregate_pattern_scores(all_results, pattern)

    # Check hard gates
    hard_gate_failures = []
    if universal_scores.get("POI", 0) < 4:
        hard_gate_failures.append("POI < 4: Phase ordering violated")
    if universal_scores.get("PC", 0) < 4:
        hard_gate_failures.append("PC < 4: Missing required phases")
    if universal_scores.get("CA", 0) < 4:
        hard_gate_failures.append("CA < 4: Constraint violations")
    if universal_scores.get("PR", 0) < 0.75:
        hard_gate_failures.append("PR < 0.75: Pattern not robust")

    # Calculate overall scores
    overall_universal = sum(
        v for k, v in universal_scores.items()
        if k != "PR"
    ) + (universal_scores.get("PR", 0) * 5)  # PR is 0-1, scale to 0-5

    overall_pattern = sum(pattern_scores.values()) if pattern_scores else 0

    # Combined score (weighted: 60% pattern, 40% universal)
    max_universal = 35  # 7 dimensions × 5
    max_pattern = 15    # 3 dimensions × 5
    combined = (
        (overall_universal / max_universal) * 0.4 +
        (overall_pattern / max_pattern) * 0.6
    ) * 100 if max_pattern > 0 else overall_universal / max_universal * 100

    # Aggregate failures
    all_failures = []
    for r in all_results:
        all_failures.extend(r.get("failures", []))
    failures = list(dict.fromkeys(all_failures))

    # Calculate pass rate
    passed_runs = sum(
        1 for r in all_results
        if r.get("universal_scores", {}).get("POI", 0) >= 4
        and r.get("universal_scores", {}).get("PC", 0) >= 4
    )
    pass_rate = passed_runs / len(all_results) if all_results else 0

    if len(all_results) > 1:
        run_confidences = [r.get("confidence", 1) for r in all_results]
        confidence = 1.0 - statistics.pstdev(run_confidences)
    else:
        confidence = 1.0

    return PatternScore(
        prompt_file=str(prompt_path),
        pattern=pattern,
        universal_scores=universal_scores,
        pattern_scores=pattern_scores,
        overall_universal=round(overall_universal, 2),
        overall_pattern=round(overall_pattern, 2),
        combined_score=round(combined, 1),
        hard_gates_passed=len(hard_gate_failures) == 0,
        hard_gate_failures=hard_gate_failures,
        failures=failures,
        pass_rate=pass_rate,
        confidence=confidence,
        model=model,
        eval_type="pattern",
        runs=runs,
        temperature=temperature,
        successful_runs=len(all_results),
    )


def _detect_pattern(prompt_content: str) -> str:
    """Auto-detect pattern from prompt content.

    Priority:
    1. Explicit `pattern:` field in YAML frontmatter
    2. Keyword detection in prompt body
    3. Default to 'react'
    """
    import re

    # Try to extract from YAML frontmatter first (most reliable)
    fm_match = re.match(r'^---\s*\n(.*?)\n---', prompt_content, re.DOTALL)
    if fm_match:
        fm_text = fm_match.group(1)
        # Look for pattern: field in frontmatter
        pattern_match = re.search(r'^pattern:\s*["\']?(\w+)["\']?\s*$', fm_text, re.MULTILINE | re.IGNORECASE)
        if pattern_match:
            detected = pattern_match.group(1).lower()
            if detected in PATTERN_PHASES:
                return detected

    # Fallback: Check for pattern keywords in content
    content_lower = prompt_content.lower()

    cove_keywords = [
        "verification question",
        "chain-of-verification",
        "draft answer",
        "revised answer",
    ]

    if any(kw in content_lower for kw in ["thought:", "action:", "observation:"]):
        return "react"
    if any(kw in content_lower for kw in cove_keywords):
        return "cove"
    if any(kw in content_lower for kw in ["reflexion", "self-critique", "reflection memory", "improved attempt"]):
        return "reflexion"
    if any(kw in content_lower for kw in ["retrieval", "citation", "grounded answer", "evidence integration"]):
        return "rag"

    return "react"  # Default


def _parse_pattern_response(response: str) -> Optional[dict]:
    """Parse JSON from pattern judge response."""
    return _parse_standard_response(response)  # Same logic


def _aggregate_universal_scores(results: List[dict]) -> Dict[str, float]:
    """Aggregate universal scores across runs using median."""
    dimensions = ["PIF", "POI", "PC", "CA", "SRC", "PR", "IR"]
    scores = {}

    for dim in dimensions:
        values = [
            r.get("universal_scores", {}).get(dim, 0)
            for r in results
            if "universal_scores" in r
        ]
        if values:
            # Trim outliers (top/bottom 10%)
            if len(values) >= 10:
                values = sorted(values)
                trim = len(values) // 10
                values = values[trim:-trim] if trim > 0 else values
            scores[dim] = round(statistics.median(values), 2)
        else:
            scores[dim] = 0

    return scores


def _aggregate_pattern_scores(results: List[dict], pattern: str) -> Dict[str, float]:
    """Aggregate pattern-specific scores across runs."""
    # Get expected dimensions for pattern
    dim_map = {
        "react": ["R1", "R2", "R3"],
        "cove": ["C1", "C2", "C3"],
        "reflexion": ["F1", "F2", "F3"],
        "rag": ["G1", "G2", "G3"],
    }
    dimensions = dim_map.get(pattern, [])

    scores = {}
    for dim in dimensions:
        values = [
            r.get("pattern_scores", {}).get(dim, 0)
            for r in results
            if "pattern_scores" in r
        ]
        if values:
            if len(values) >= 10:
                values = sorted(values)
                trim = len(values) // 10
                values = values[trim:-trim] if trim > 0 else values
            scores[dim] = round(statistics.median(values), 2)
        else:
            scores[dim] = 0

    return scores


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Unified Prompt Scorer")
    parser.add_argument("prompt", help="Path to prompt file")
    parser.add_argument("--output", "-o", help="Model output file (for pattern scoring)")
    parser.add_argument("--pattern", "-p", help="Pattern type (react, cove, reflexion, rag)")
    parser.add_argument("--model", "-m", default="local:phi4mini", help="Judge model")
    parser.add_argument("--runs", "-r", type=int, default=1, help="Number of runs")
    parser.add_argument("--json", action="store_true", help="Output JSON")

    args = parser.parse_args()

    if args.output:
        # Pattern scoring
        with open(args.output, "r", encoding="utf-8") as f:
            model_output = f.read()

        result = score_pattern(
            args.prompt,
            model_output,
            pattern=args.pattern,
            model=args.model,
            runs=args.runs,
        )

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print(f"\n{'='*60}")
            print(f" PATTERN EVALUATION: {result.pattern.upper()}")
            print(f"{'='*60}")
            print(f"\nPrompt: {result.prompt_file}")
            print(f"Combined Score: {result.combined_score}/100")
            print(f"Hard Gates: {'PASS ✓' if result.hard_gates_passed else 'FAIL ✗'}")
            print("\nUniversal Scores:")
            for k, v in result.universal_scores.items():
                gate = " (HARD GATE)" if k in ["POI", "PC", "CA", "PR"] else ""
                print(f"  {k}: {v}{gate}")
            print(f"\nPattern Scores ({result.pattern}):")
            for k, v in result.pattern_scores.items():
                print(f"  {k}: {v}")
            if result.hard_gate_failures:
                print("\n⚠️ Hard Gate Failures:")
                for f in result.hard_gate_failures:
                    print(f"  - {f}")
    else:
        # Standard scoring
        result = score_prompt(
            args.prompt,
            model=args.model,
            runs=args.runs,
        )

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print(f"\n{'='*60}")
            print(" STANDARD EVALUATION")
            print(f"{'='*60}")
            print(f"\nPrompt: {result.prompt_file}")
            print(f"Overall Score: {result.overall_score}/100 ({result.grade})")
            print(f"Passed: {'✓' if result.passed else '✗'}")
            print("\nDimension Scores:")
            for k, v in result.scores.items():
                print(f"  {k.capitalize()}: {v}/10")
            if result.improvements:
                print("\nSuggested Improvements:")
                for imp in result.improvements:
                    print(f"  - {imp}")
