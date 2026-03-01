"""Agentic V2 Evaluation Framework.

Provides YAML-rubric scoring, pluggable evaluators (LLM-as-judge,
pattern-based, quality, and standard), batch / streaming runners,
multi-format reporters (JSON, Markdown, HTML), and sandboxed code
execution for end-to-end agent evaluation.

Quick start::

    from agentic_v2_eval import Scorer, PatternEvaluator, StandardEvaluator

    scorer = Scorer("rubrics/default.yaml")
    result = scorer.score({"Accuracy": 0.85, "Completeness": 0.92})
"""

__version__ = "0.3.0"

from agentic_v2_eval.interfaces import LLMClientProtocol, Evaluator
from agentic_v2_eval.scorer import Scorer, ScoringResult
from agentic_v2_eval.evaluators.base import EvaluatorRegistry
from agentic_v2_eval.evaluators.pattern import PatternEvaluator, PatternScore
from agentic_v2_eval.evaluators.quality import (
    QualityEvaluator,
    LLMEvaluatorDefinition,
    COHERENCE,
    FLUENCY,
    RELEVANCE,
    GROUNDEDNESS,
    SIMILARITY,
)
from agentic_v2_eval.evaluators.standard import StandardEvaluator, StandardScore

__all__ = [
    "__version__",
    "LLMClientProtocol",
    "Evaluator",
    "EvaluatorRegistry",
    "Scorer",
    "ScoringResult",
    "PatternEvaluator",
    "PatternScore",
    "QualityEvaluator",
    "LLMEvaluatorDefinition",
    "COHERENCE",
    "FLUENCY",
    "RELEVANCE",
    "GROUNDEDNESS",
    "SIMILARITY",
    "StandardEvaluator",
    "StandardScore",
]
