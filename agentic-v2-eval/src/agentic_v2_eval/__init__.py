"""Agentic V2 Evaluation Framework.

A comprehensive evaluation framework for AI agent workflows.

Modules:
    metrics: Accuracy, quality, and performance metrics
    runners: Batch and streaming evaluation runners
    reporters: JSON, Markdown, and HTML report generators
    rubrics: Evaluation rubric definitions
    scorer: Rubric-based scoring

Example:
    >>> from agentic_v2_eval import Scorer
    >>> from agentic_v2_eval.metrics import calculate_accuracy
    >>> from agentic_v2_eval.reporters import generate_json_report
"""

from __future__ import annotations

__version__ = "0.2.0"

from .scorer import Criterion, Scorer, ScoringResult

__all__ = [
    "__version__",
    "Scorer",
    "ScoringResult",
    "Criterion",
]
