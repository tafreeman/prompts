"""Scoring utilities with rubric support."""

from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Any, Dict


@dataclass
class ScoreResult:
    scores: Dict[str, float]
    weighted_score: float
    details: Dict[str, Any]


class Scorer:
    """Score outputs against goldens using rubric weights."""

    def __init__(self, rubrics: Dict[str, Any]):
        self.rubrics = rubrics

    def score(self, output: str, golden: str, rubric_name: str) -> ScoreResult:
        rubric = self.rubrics.get("rubrics", {}).get(rubric_name, {})
        categories = rubric.get("categories", {})
        scores: Dict[str, float] = {}
        details: Dict[str, Any] = {}

        for category_name in categories:
            method = getattr(self, f"score_{category_name}", None)
            if not method:
                continue
            scores[category_name] = method(output, golden, categories[category_name])

        weighted_total = 0.0
        weight_sum = 0.0
        for category_name, category in categories.items():
            weight = float(category.get("weight", 0))
            score = scores.get(category_name, 0.0)
            weighted_total += score * weight
            weight_sum += weight

        weighted_score = (weighted_total / weight_sum) if weight_sum else 0.0
        details["weights"] = {
            name: cat.get("weight") for name, cat in categories.items()
        }

        return ScoreResult(
            scores=scores, weighted_score=round(weighted_score, 2), details=details
        )

    def score_functional_correctness(
        self, output: str, golden: str, _: Dict[str, Any]
    ) -> float:
        if not output or not golden:
            return 0.0
        ratio = SequenceMatcher(None, output.strip(), golden.strip()).ratio()
        return round(ratio * 100, 2)

    def score_code_quality(
        self, output: str, _: str, category: Dict[str, Any]
    ) -> float:
        if not output:
            return 0.0
        penalties = 0.0
        if "TODO" in output or "FIXME" in output:
            penalties += 10
        if len(output.splitlines()) > category.get("max_lines", 400):
            penalties += 15
        base = 85.0
        return max(0.0, base - penalties)

    def score_completeness(
        self, output: str, golden: str, category: Dict[str, Any]
    ) -> float:
        required_keys = category.get("required_keys", [])
        missing = [k for k in required_keys if k.lower() not in output.lower()]
        if not required_keys:
            return self.score_functional_correctness(output, golden, category)
        return round(100 * (1 - (len(missing) / len(required_keys))), 2)

    def score_documentation(self, output: str, _: str, __: Dict[str, Any]) -> float:
        if not output:
            return 0.0
        markers = ["##", "###", "README", "Usage", "API"]
        hits = sum(1 for m in markers if m.lower() in output.lower())
        return min(100.0, hits / len(markers) * 100)

    def score_efficiency(self, output: str, _: str, __: Dict[str, Any]) -> float:
        if not output:
            return 0.0
        length = len(output)
        if length < 1500:
            return 90.0
        if length < 4000:
            return 75.0
        return 60.0

    def score_architecture(self, output: str, _: str, __: Dict[str, Any]) -> float:
        keywords = ["diagram", "component", "trade-off", "risk", "scalability"]
        hits = sum(1 for k in keywords if k in output.lower())
        return min(100.0, hits / len(keywords) * 100)

    def score_security(self, output: str, _: str, __: Dict[str, Any]) -> float:
        keywords = ["threat", "mitigation", "auth", "authorization", "encryption"]
        hits = sum(1 for k in keywords if k in output.lower())
        return min(100.0, hits / len(keywords) * 100)
