"""Agentic V2 Evaluation Package."""

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
