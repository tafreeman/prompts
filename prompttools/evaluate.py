"""
Prompt evaluation - direct, G-Eval, and tiered methods.

Simple usage:
    from prompttools import evaluate
    result = evaluate("prompts/my-prompt.md")  # Uses sensible defaults
    
Batch usage:
    results = evaluate("prompts/")  # Evaluates entire directory
    results = evaluate("prompts/", tier=2)  # Cloud model tier
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
import time

from .parse import parse_frontmatter, extract_body, extract_json, extract_score, extract_criteria_scores
from .cache import get_cached, set_cached
from .config import PASS_THRESHOLD


# =============================================================================
# RESULT CLASSES
# =============================================================================

@dataclass
class EvalResult:
    """Result from evaluating a single prompt."""
    file: str
    score: float
    grade: str
    passed: bool
    criteria: Dict[str, float] = field(default_factory=dict)
    improvements: List[str] = field(default_factory=list)
    model: str = ""
    method: str = ""
    tier: int = 1
    duration: float = 0.0
    error: Optional[str] = None
    
    @property
    def is_error(self) -> bool:
        return self.error is not None


@dataclass
class BatchResult:
    """Result from evaluating multiple prompts."""
    results: List[EvalResult] = field(default_factory=list)
    total: int = 0
    passed: int = 0
    failed: int = 0
    errors: int = 0
    avg_score: float = 0.0
    duration: float = 0.0
    
    def summary(self) -> str:
        return f"{self.passed}/{self.total} passed ({self.avg_score:.1f} avg)"


# =============================================================================
# TIER DEFINITIONS
# =============================================================================

TIERS = {
    0: {"name": "Structural", "model": None, "method": "structural"},
    1: {"name": "Local", "model": "local:phi4mini", "method": "geval"},
    2: {"name": "Cloud Basic", "model": "gh:gpt-4o-mini", "method": "geval"},
    3: {"name": "Cloud Premium", "model": "gh:gpt-4.1", "method": "geval"},
}


# =============================================================================
# GRADE CONVERSION
# =============================================================================

def _get_grade(score: float) -> str:
    """Convert score to letter grade."""
    if score >= 90: return "A"
    if score >= 80: return "B"
    if score >= 70: return "C"
    if score >= 60: return "D"
    return "F"


# =============================================================================
# MAIN EVALUATE FUNCTION
# =============================================================================

def evaluate(
    path: Union[str, Path],
    model: Optional[str] = None,
    method: str = "geval",
    tier: Optional[int] = None,
    threshold: float = PASS_THRESHOLD,
    recursive: bool = True,
    verbose: bool = False,
) -> Union[EvalResult, BatchResult]:
    """
    Evaluate a prompt file or directory.
    
    This is the main entry point - handles both single files and directories.
    
    Args:
        path: Path to prompt file or directory
        model: Model to use (default: auto-select based on tier)
        method: "geval", "direct", or "structural"
        tier: Evaluation tier (0=structural, 1=local, 2=cloud, 3=premium)
              If set, overrides model and method
        threshold: Score threshold for passing (default: 70)
        recursive: For directories, whether to recurse
        verbose: Print progress
        
    Returns:
        EvalResult for single file, BatchResult for directory
        
    Examples:
        # Single file with defaults
        result = evaluate("prompts/my-prompt.md")
        
        # Directory with tier
        results = evaluate("prompts/", tier=2)
        
        # Custom model
        result = evaluate("prompts/my-prompt.md", model="ollama:llama3.3")
    """
    path = Path(path)
    
    # Apply tier settings if specified
    if tier is not None:
        tier_config = TIERS.get(tier, TIERS[1])
        model = model or tier_config["model"]
        method = tier_config["method"]
    else:
        tier = 1  # Default tier
    
    # Default model if not specified
    if model is None and method != "structural":
        model = "local:phi4mini"
    
    # Single file or directory?
    if path.is_file():
        return _evaluate_single(path, model, method, tier, threshold, verbose)
    elif path.is_dir():
        return _evaluate_batch(path, model, method, tier, threshold, recursive, verbose)
    else:
        return EvalResult(
            file=str(path),
            score=0,
            grade="F",
            passed=False,
            error=f"Path not found: {path}"
        )


def evaluate_batch(
    paths: List[Union[str, Path]],
    model: Optional[str] = None,
    method: str = "geval",
    tier: Optional[int] = None,
    threshold: float = PASS_THRESHOLD,
    verbose: bool = False,
) -> BatchResult:
    """
    Evaluate a list of prompt files.
    
    Args:
        paths: List of file paths
        model, method, tier, threshold: Same as evaluate()
        verbose: Print progress
        
    Returns:
        BatchResult with all evaluations
    """
    start_time = time.time()
    
    # Apply tier settings
    if tier is not None:
        tier_config = TIERS.get(tier, TIERS[1])
        model = model or tier_config["model"]
        method = tier_config["method"]
    else:
        tier = 1
        model = model or "local:phi4mini"
    
    results = []
    for i, p in enumerate(paths):
        if verbose:
            print(f"[{i+1}/{len(paths)}] Evaluating {p}...")
        result = _evaluate_single(Path(p), model, method, tier, threshold, verbose=False)
        results.append(result)
    
    return _build_batch_result(results, time.time() - start_time)


# =============================================================================
# INTERNAL FUNCTIONS
# =============================================================================

def _evaluate_single(
    path: Path,
    model: Optional[str],
    method: str,
    tier: int,
    threshold: float,
    verbose: bool,
) -> EvalResult:
    """Evaluate a single prompt file."""
    start_time = time.time()
    
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return EvalResult(
            file=str(path),
            score=0,
            grade="F",
            passed=False,
            error=f"Cannot read file: {e}"
        )
    
    # Structural analysis (no LLM)
    if method == "structural":
        return _evaluate_structural(path, content, threshold, start_time)
    
    # LLM-based evaluation
    return _evaluate_with_llm(path, content, model, method, tier, threshold, start_time, verbose)


def _evaluate_structural(path: Path, content: str, threshold: float, start_time: float) -> EvalResult:
    """Structural analysis without LLM."""
    fm = parse_frontmatter(content)
    body = extract_body(content)
    
    # Score based on structure
    score = 50.0  # Base score
    criteria = {}
    improvements = []
    
    # Check frontmatter fields
    if fm.get("title"):
        score += 10
        criteria["title"] = 100
    else:
        criteria["title"] = 0
        improvements.append("Add title in frontmatter")
    
    if fm.get("description") or fm.get("intro"):
        score += 10
        criteria["description"] = 100
    else:
        criteria["description"] = 0
        improvements.append("Add description in frontmatter")
    
    # Check sections
    import re
    sections = [s.lower() for s in re.findall(r'^##\s+(.+)$', content, re.MULTILINE)]
    
    for section in ["description", "prompt", "variables", "example"]:
        if section in sections:
            score += 7.5
            criteria[section] = 100
        else:
            criteria[section] = 0
            improvements.append(f"Add ## {section.title()} section")
    
    # Content length bonus
    if len(body) > 500:
        score += 5
    
    score = min(100, score)
    
    return EvalResult(
        file=str(path),
        score=score,
        grade=_get_grade(score),
        passed=score >= threshold,
        criteria=criteria,
        improvements=improvements,
        model="structural",
        method="structural",
        tier=0,
        duration=time.time() - start_time,
    )


def _evaluate_with_llm(
    path: Path,
    content: str,
    model: str,
    method: str,
    tier: int,
    threshold: float,
    start_time: float,
    verbose: bool,
) -> EvalResult:
    """Evaluate using an LLM."""
    from .llm import generate
    
    # Check cache
    cached_response = get_cached(content, model)
    if cached_response:
        if verbose:
            print(f"  [Cache hit]")
        return _parse_llm_response(cached_response, path, model, method, tier, threshold, start_time)
    
    # Build evaluation prompt
    eval_prompt = _build_eval_prompt(content, method)
    
    # Call LLM
    try:
        response = generate(model, eval_prompt)
        set_cached(content, model, response)
    except Exception as e:
        return EvalResult(
            file=str(path),
            score=0,
            grade="F",
            passed=False,
            error=f"LLM error: {e}",
            model=model,
            method=method,
            tier=tier,
            duration=time.time() - start_time,
        )
    
    return _parse_llm_response(response, path, model, method, tier, threshold, start_time)


def _build_eval_prompt(content: str, method: str) -> str:
    """Build the evaluation prompt."""
    if method == "geval":
        return f"""Evaluate this prompt template on a scale of 0-100.

First, think step-by-step about these criteria:
1. Clarity - Is the purpose clear? Are instructions unambiguous?
2. Effectiveness - Will this produce good results with an LLM?
3. Reusability - Can this be used for multiple similar tasks?
4. Structure - Is it well-organized with proper sections?
5. Examples - Are there helpful examples?

Then provide your evaluation as JSON:
{{
  "score": <0-100>,
  "criteria": {{
    "clarity": <0-100>,
    "effectiveness": <0-100>,
    "reusability": <0-100>,
    "structure": <0-100>,
    "examples": <0-100>
  }},
  "improvements": ["suggestion 1", "suggestion 2"]
}}

PROMPT TO EVALUATE:
---
{content}
---

Respond with your step-by-step reasoning, then the JSON."""
    
    else:  # direct
        return f"""Rate this prompt template from 0-100 and explain why.
Respond as JSON: {{"score": <0-100>, "reasoning": "<explanation>"}}

PROMPT:
{content}"""


def _parse_llm_response(
    response: str,
    path: Path,
    model: str,
    method: str,
    tier: int,
    threshold: float,
    start_time: float,
) -> EvalResult:
    """Parse the LLM response into an EvalResult."""
    score = extract_score(response)
    if score is None:
        score = 50.0  # Default if parsing fails
    
    criteria = extract_criteria_scores(response)
    
    # Extract improvements from JSON
    improvements = []
    data = extract_json(response)
    if data and isinstance(data, dict):
        impr = data.get("improvements", [])
        if isinstance(impr, list):
            improvements = [str(i) for i in impr]
    
    return EvalResult(
        file=str(path),
        score=score,
        grade=_get_grade(score),
        passed=score >= threshold,
        criteria=criteria,
        improvements=improvements,
        model=model,
        method=method,
        tier=tier,
        duration=time.time() - start_time,
    )


def _evaluate_batch(
    directory: Path,
    model: Optional[str],
    method: str,
    tier: int,
    threshold: float,
    recursive: bool,
    verbose: bool,
) -> BatchResult:
    """Evaluate all prompts in a directory."""
    from .validate import SKIP_PATTERNS
    import fnmatch
    
    start_time = time.time()
    
    # Find prompt files
    pattern = "**/*.md" if recursive else "*.md"
    files = list(directory.glob(pattern))
    
    # Filter skipped files
    filtered = []
    for f in files:
        skip = False
        for pat in SKIP_PATTERNS:
            if fnmatch.fnmatch(str(f), pat) or fnmatch.fnmatch(f.name, pat):
                skip = True
                break
        if not skip:
            filtered.append(f)
    
    if verbose:
        tier_name = TIERS.get(tier, {}).get("name", f"Tier {tier}")
        print(f"\nEvaluating {len(filtered)} prompts with {tier_name}...")
        print(f"Model: {model or 'structural'}\n")
    
    results = []
    for i, f in enumerate(filtered):
        if verbose:
            print(f"[{i+1}/{len(filtered)}] {f.name}...", end=" ", flush=True)
        
        result = _evaluate_single(f, model, method, tier, threshold, verbose=False)
        results.append(result)
        
        if verbose:
            status = "✓" if result.passed else "✗"
            print(f"{status} {result.score:.0f}")
    
    return _build_batch_result(results, time.time() - start_time)


def _build_batch_result(results: List[EvalResult], duration: float) -> BatchResult:
    """Build a BatchResult from a list of EvalResults."""
    passed = sum(1 for r in results if r.passed)
    errors = sum(1 for r in results if r.is_error)
    valid_scores = [r.score for r in results if not r.is_error]
    avg_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0
    
    return BatchResult(
        results=results,
        total=len(results),
        passed=passed,
        failed=len(results) - passed - errors,
        errors=errors,
        avg_score=avg_score,
        duration=duration,
    )


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def evaluate_tiered(
    path: Union[str, Path],
    tier: int = 1,
    threshold: float = PASS_THRESHOLD,
    verbose: bool = True,
) -> Union[EvalResult, BatchResult]:
    """
    Shortcut for tiered evaluation with defaults.
    
    Tiers:
        0: Structural only (no LLM, instant)
        1: Local model (free, ~10s per prompt)
        2: Cloud basic (gh:gpt-4o-mini)
        3: Cloud premium (gh:gpt-4.1)
    
    Example:
        results = evaluate_tiered("prompts/", tier=2)
    """
    return evaluate(path, tier=tier, threshold=threshold, verbose=verbose)


def quick_eval(path: Union[str, Path]) -> Union[EvalResult, BatchResult]:
    """
    Quick evaluation with local model and minimal output.
    
    Example:
        result = quick_eval("prompts/my-prompt.md")
        print(result.score)
    """
    return evaluate(path, tier=1, verbose=False)
