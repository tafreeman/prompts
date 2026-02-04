"""Scoring framework for Agentic V2 Evaluation.

Provides rubric-based scoring with validation and error handling.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class Criterion:
    """A single scoring criterion."""

    name: str
    weight: float = 1.0
    description: str = ""
    min_value: float = 0.0
    max_value: float = 1.0


@dataclass
class ScoringResult:
    """Result of scoring operation."""

    total_score: float
    weighted_score: float
    criterion_scores: dict[str, float] = field(default_factory=dict)
    missing_criteria: list[str] = field(default_factory=list)


class Scorer:
    """Score evaluation results based on rubric criteria.

    Example:
        >>> scorer = Scorer("rubrics/default.yaml")
        >>> result = scorer.score({"Accuracy": 0.8, "Completeness": 0.9})
        >>> print(f"Score: {result.weighted_score:.2f}")
    """

    def __init__(self, rubric_path: str | Path):
        """Initialize scorer with rubric file.

        Args:
            rubric_path: Path to YAML rubric file.

        Raises:
            FileNotFoundError: If rubric file doesn't exist.
            ValueError: If rubric format is invalid.
        """
        rubric_path = Path(rubric_path)

        if not rubric_path.exists():
            raise FileNotFoundError(f"Rubric file not found: {rubric_path}")

        with rubric_path.open("r", encoding="utf-8") as f:
            self.rubric = yaml.safe_load(f)

        if not isinstance(self.rubric, dict):
            raise ValueError("Rubric must be a YAML dictionary")

        self.criteria = self._parse_criteria(self.rubric.get("criteria", []))
        self.name = self.rubric.get("name", "Unnamed Rubric")
        self.version = self.rubric.get("version", "1.0")

    def _parse_criteria(self, raw_criteria: list[dict[str, Any]]) -> list[Criterion]:
        """Parse raw criteria from rubric."""
        criteria = []

        for item in raw_criteria:
            if not isinstance(item, dict) or "name" not in item:
                continue

            criteria.append(
                Criterion(
                    name=item["name"],
                    weight=float(item.get("weight", 1.0)),
                    description=item.get("description", ""),
                    min_value=float(item.get("min_value", 0.0)),
                    max_value=float(item.get("max_value", 1.0)),
                )
            )

        return criteria

    def score(self, results: dict[str, float]) -> ScoringResult:
        """Score results based on rubric criteria.

        Args:
            results: Dictionary of metric results, e.g., {'Accuracy': 0.8, 'Completeness': 0.9}

        Returns:
            ScoringResult with weighted and raw scores.
        """
        if not self.criteria:
            return ScoringResult(
                total_score=0.0,
                weighted_score=0.0,
            )

        total_weight = sum(c.weight for c in self.criteria)
        weighted_sum = 0.0
        raw_sum = 0.0
        criterion_scores: dict[str, float] = {}
        missing: list[str] = []

        for criterion in self.criteria:
            name = criterion.name

            if name not in results:
                missing.append(name)
                continue

            value = float(results[name])

            # Clamp to valid range
            value = max(criterion.min_value, min(criterion.max_value, value))

            # Normalize to 0-1 range
            range_size = criterion.max_value - criterion.min_value
            if range_size > 0:
                normalized = (value - criterion.min_value) / range_size
            else:
                normalized = value

            criterion_scores[name] = value
            weighted_sum += criterion.weight * normalized
            raw_sum += normalized

        weighted_score = weighted_sum / total_weight if total_weight > 0 else 0.0
        total_score = raw_sum / len(self.criteria) if self.criteria else 0.0

        return ScoringResult(
            total_score=total_score,
            weighted_score=weighted_score,
            criterion_scores=criterion_scores,
            missing_criteria=missing,
        )

    def validate_results(self, results: dict[str, float]) -> list[str]:
        """Validate that results contain all required criteria.

        Args:
            results: Dictionary of metric results.

        Returns:
            List of missing criterion names.
        """
        return [c.name for c in self.criteria if c.name not in results]
