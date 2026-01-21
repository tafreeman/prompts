"""PromptEval core helpers.

This module serves two purposes:
1) Keep a small legacy surface area (`PromptEval._run_geval`) required by tests.
2) Provide a lightweight `evaluate()` function for `python -m tools.prompteval`.

Historically, the CLI delegated to the deprecated `prompttools` package.
That dependency has been removed from the repo, so `evaluate()` now lives here.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Optional, Union

from .config import EvalConfig
from .parse_utils import BatchResult, EvalResult, _get_grade, extract_body, extract_json, parse_frontmatter


# =============================================================================
# Tier defaults (compatible with the historical prompttools tiers)
# =============================================================================

TIERS: dict[int, dict[str, object]] = {
    0: {"name": "Structural", "model": None, "method": "structural"},
    1: {"name": "Local", "model": "local:phi4mini", "method": "geval"},
    2: {"name": "Cloud Basic", "model": "gh:gpt-4o-mini", "method": "geval"},
    3: {"name": "Cloud Premium", "model": "gh:gpt-4.1", "method": "geval"},
}

PASS_THRESHOLD = 7.0


def evaluate(
    path: Union[str, Path],
    model: Optional[str] = None,
    method: str = "geval",
    tier: Optional[int] = None,
    threshold: float = PASS_THRESHOLD,
    recursive: bool = True,
    verbose: bool = False,
) -> Union[EvalResult, BatchResult]:
    """Evaluate a prompt file or directory.

    This is a pragmatic, dependency-light evaluator intended for repo workflows.
    - Tier 0: purely structural checks (no model calls)
    - Tiers 1-3: judge with an LLM and parse JSON response
    """
    p = Path(path)

    if tier is not None:
        tier_cfg = TIERS.get(int(tier), TIERS[1])
        model = model or (tier_cfg.get("model") if isinstance(tier_cfg, dict) else None)  # type: ignore[assignment]
        method = str(tier_cfg.get("method", method)) if isinstance(tier_cfg, dict) else method
    else:
        tier = 1

    # Default model (only for non-structural)
    if model is None and method != "structural":
        model = "local:phi4mini"

    if p.is_file():
        return _evaluate_single(p, model=model, method=method, tier=int(tier), threshold=threshold, verbose=verbose)
    if p.is_dir():
        return _evaluate_batch(p, model=model, method=method, tier=int(tier), threshold=threshold, recursive=recursive, verbose=verbose)

    return EvalResult(
        file=str(p),
        score=0.0,
        grade="F",
        passed=False,
        error=f"Path not found: {p}",
    )


def _evaluate_single(
    path: Path,
    *,
    model: Optional[str],
    method: str,
    tier: int,
    threshold: float,
    verbose: bool,
) -> EvalResult:
    start = time.time()
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return EvalResult(
            file=str(path),
            score=0.0,
            grade="F",
            passed=False,
            error=f"Cannot read file: {e}",
        )

    if method == "structural":
        return _evaluate_structural(path, content, threshold=threshold, started=start)

    return _evaluate_with_llm(
        path,
        content,
        model=model or "local:phi4mini",
        method=method,
        tier=tier,
        threshold=threshold,
        started=start,
        verbose=verbose,
    )


def _evaluate_structural(path: Path, content: str, *, threshold: float, started: float) -> EvalResult:
    import re

    fm = parse_frontmatter(content)
    body = extract_body(content)

    score = 5.0
    criteria: dict[str, float] = {}
    improvements: list[str] = []

    if fm.get("title"):
        score += 1.0
        criteria["title"] = 10
    else:
        criteria["title"] = 0
        improvements.append("Add title in frontmatter")

    if fm.get("description") or fm.get("intro"):
        score += 1.0
        criteria["description"] = 10
    else:
        criteria["description"] = 0
        improvements.append("Add description/intro in frontmatter")

    sections = [s.lower() for s in re.findall(r"^##\s+(.+)$", content, re.MULTILINE)]
    for section in ["description", "prompt", "variables", "example"]:
        if section in sections:
            score += 0.75
            criteria[section] = 10
        else:
            criteria[section] = 0
            improvements.append(f"Add ## {section.title()} section")

    if len(body) > 500:
        score += 0.5

    score = min(10.0, score)
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
        duration=time.time() - started,
    )


def _evaluate_with_llm(
    path: Path,
    content: str,
    *,
    model: str,
    method: str,
    tier: int,
    threshold: float,
    started: float,
    verbose: bool,
) -> EvalResult:
    # Use the canonical unified scorer for robust parsing and consistency.
    from tools.prompteval.unified_scorer import score_prompt

    if verbose:
        print(f"[prompteval] {path.name}: scoring with {model}")

    try:
        standard = score_prompt(
            prompt_path=path,
            model=model,
            runs=1,
            temperature=0.1,
            verbose=verbose,
        )
    except Exception as e:
        return EvalResult(
            file=str(path),
            score=0.0,
            grade="F",
            passed=False,
            error=f"Evaluation error: {e}",
            model=model,
            method=method,
            tier=tier,
            duration=time.time() - started,
        )

    # unified_scorer returns 0-10 per-dimension scores; keep the same 0-10 scale for criteria.
    criteria: dict[str, float] = {}
    for k, v in (standard.scores or {}).items():
        if isinstance(v, (int, float)):
            criteria[k] = float(v)

    improvements = list(standard.improvements or [])

    # If the scorer couldn't parse any judge responses it returns overall_score=0 and an improvement.
    error = None
    if standard.overall_score <= 0 and improvements:
        error = "Judge output could not be parsed"

    return EvalResult(
        file=str(path),
        score=float(standard.overall_score),
        grade=str(standard.grade),
        passed=float(standard.overall_score) >= threshold,
        criteria=criteria,
        improvements=[str(x) for x in improvements],
        model=model,
        method=method,
        tier=tier,
        duration=time.time() - started,
        error=error,
    )


def _evaluate_batch(
    path: Path,
    *,
    model: Optional[str],
    method: str,
    tier: int,
    threshold: float,
    recursive: bool,
    verbose: bool,
) -> BatchResult:
    started = time.time()
    pattern = "**/*.md" if recursive else "*.md"
    files = list(path.glob(pattern))

    results: list[EvalResult] = []
    for i, f in enumerate(files):
        if verbose and (i % 25 == 0 or i == len(files) - 1):
            print(f"[prompteval] {i+1}/{len(files)}")
        results.append(
            _evaluate_single(
                f,
                model=model,
                method=method,
                tier=tier,
                threshold=threshold,
                verbose=False,
            )
        )

    passed = sum(1 for r in results if r.passed)
    errors = sum(1 for r in results if r.is_error)
    scored = [r.score for r in results if not r.is_error]

    return BatchResult(
        results=results,
        total=len(results),
        passed=passed,
        failed=len(results) - passed - errors,
        errors=errors,
        avg_score=(sum(scored) / len(scored)) if scored else 0.0,
        duration=time.time() - started,
    )


def _build_eval_prompt(content: str, *, method: str) -> str:
    """Deprecated: retained for compatibility.

    Model-based scoring now routes through tools.prompteval.unified_scorer.
    """
    return content


class PromptEval:
    def __init__(self, cfg: EvalConfig):
        self.cfg = cfg
        self.llm_client: Any | None = None

    def _run_geval(self, content: str) -> dict:
        """Run a single G-Eval style judge call and normalize to 0..100.

        Expected judge response format (string):
            {"reasoning": "...", "score": 3.5}

        The legacy tests treat the score as 0..5 and scale it by 20.
        """
        if self.llm_client is None:
            raise RuntimeError("PromptEval.llm_client must be set")

        raw = self.llm_client.generate_text(
            model_name=self.cfg.model,
            prompt=content,
            temperature=self.cfg.temperature,
            max_tokens=self.cfg.max_tokens,
        )

        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = {}

        score = parsed.get("score")
        if score is None:
            score_val = 0.0
        else:
            try:
                score_val = float(score)
            except Exception:
                score_val = 0.0

        # Legacy normalization: 0..5 => 0..100
        score_pct = max(0.0, min(100.0, score_val * 20.0))

        return {
            "clarity": {
                "score": score_pct,
                "reasoning": parsed.get("reasoning", ""),
            }
        }
