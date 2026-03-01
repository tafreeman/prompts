"""Pluggable evaluator implementations and central registry.

Exposes four evaluator strategies:
    LLMEvaluator: Choice-anchored LLM-as-judge scoring.
    PatternEvaluator: Agentic-pattern phase/constraint scoring.
    QualityEvaluator: Coherence / Fluency / Relevance / Groundedness / Similarity.
    StandardEvaluator: Five-dimension prompt quality scoring.

All evaluators self-register in :class:`EvaluatorRegistry` at import time.
"""

from .base import Evaluator, EvaluatorRegistry
from .llm import LLMClientProtocol, LLMEvaluator, Choice, STANDARD_CHOICES
from .pattern import PatternEvaluator, PatternScore
from .quality import (
    QualityEvaluator,
    LLMEvaluatorDefinition,
    COHERENCE,
    FLUENCY,
    RELEVANCE,
    GROUNDEDNESS,
    SIMILARITY,
)
from .standard import StandardEvaluator, StandardScore

__all__ = [
    # Base
    "Evaluator",
    "EvaluatorRegistry",
    # LLM
    "LLMClientProtocol",
    "LLMEvaluator",
    "Choice",
    "STANDARD_CHOICES",
    # Pattern
    "PatternEvaluator",
    "PatternScore",
    # Quality
    "QualityEvaluator",
    "LLMEvaluatorDefinition",
    "COHERENCE",
    "FLUENCY",
    "RELEVANCE",
    "GROUNDEDNESS",
    "SIMILARITY",
    # Standard
    "StandardEvaluator",
    "StandardScore",
]
