"""
PromptEval - Unified Prompt Evaluation System

This package provides comprehensive prompt evaluation with:
- Standard scoring (clarity, effectiveness, structure, specificity, completeness)
- Pattern scoring (CoVe, ReAct, Reflexion, RAG)
- Built-in evaluators ported from Microsoft PromptFlow/gh-models
- Example-anchored rubrics for consistent scoring
- Multi-run aggregation with outlier trimming
"""

# Built-in evaluators (ported from gh-models/Microsoft PromptFlow)
from .builtin_evaluators import (
    BUILTIN_EVALUATORS,
    Choice,
    EvaluatorRunner,
    LLMEvaluator,
    StringEvaluator,
    get_evaluator,
    list_evaluators,
)

# Parser
from .parser import detect_pattern, load_pattern_definition, parse_output

# Pattern evaluator
from .pattern_evaluator import PatternEvaluator

# Prompt file format (.prompt.yml compatibility)
from .prompt_file import (
    EvaluationResult,
    EvaluationSummary,
    Evaluator,
    Message,
    PromptEvaluator,
    PromptFile,
    TestResult,
)

# Core scoring
from .unified_scorer import (
    PatternScore,
    StandardScore,
    get_grade,
    load_unified_rubric,
    score_pattern,
    score_prompt,
)

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
