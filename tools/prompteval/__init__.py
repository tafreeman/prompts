"""
PromptEval - Unified Prompt Evaluation System

This package provides comprehensive prompt evaluation with:
- Standard scoring (clarity, effectiveness, structure, specificity, completeness)
- Pattern scoring (CoVe, ReAct, Reflexion, RAG)
- Built-in evaluators ported from Microsoft PromptFlow/gh-models
- Example-anchored rubrics for consistent scoring
- Multi-run aggregation with outlier trimming
"""

# Core scoring
from .unified_scorer import (
    StandardScore,
    PatternScore,
    score_prompt,
    score_pattern,
    get_grade,
    load_unified_rubric,
)

# Built-in evaluators (ported from gh-models/Microsoft PromptFlow)
from .builtin_evaluators import (
    Choice,
    LLMEvaluator,
    StringEvaluator,
    EvaluatorRunner,
    BUILTIN_EVALUATORS,
    get_evaluator,
    list_evaluators,
)

# Prompt file format (.prompt.yml compatibility)
from .prompt_file import (
    PromptFile,
    Message,
    Evaluator,
    EvaluationResult,
    TestResult,
    EvaluationSummary,
    PromptEvaluator,
)

# Parser
from .parser import parse_output, detect_pattern, load_pattern_definition

# Pattern evaluator
from .pattern_evaluator import PatternEvaluator

__all__ = [
    # Standard scoring
    "StandardScore",
    "PatternScore",
    "score_prompt",
    "score_pattern",
    "get_grade",
    "load_unified_rubric",
    # Built-in evaluators
    "Choice",
    "LLMEvaluator",
    "StringEvaluator",
    "EvaluatorRunner",
    "BUILTIN_EVALUATORS",
    "get_evaluator",
    "list_evaluators",
    # Prompt file
    "PromptFile",
    "Message",
    "Evaluator",
    "EvaluationResult",
    "TestResult",
    "EvaluationSummary",
    "PromptEvaluator",
    # Parser
    "parse_output",
    "detect_pattern",
    "load_pattern_definition",
    # Pattern evaluator
    "PatternEvaluator",
]
