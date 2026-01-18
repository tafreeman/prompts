"""
PromptTools: Simple, effective prompt evaluation and validation toolkit.

This package provides a unified interface for:
1. Evaluating prompt quality using G-Eval and structural analysis.
2. Validating prompt file structure and mandatory metadata.
3. Accessing multiple LLM providers (Local, Cloud, Windows AI) via a single API.
4. Caching LLM responses for efficiency and consistency.

Example:
    >>> import prompttools
    >>> result = prompttools.evaluate("prompts/developers/api-design.md")
    >>> print(f"Score: {result.score}/100")
"""

from .evaluate import evaluate, evaluate_batch, EvalResult
from .validate import validate, validate_batch, Issue
from .llm import generate, list_models, probe

__all__ = [
    # Evaluation
    "evaluate",
    "evaluate_batch",
    "EvalResult",
    # Validation
    "validate",
    "validate_batch",
    "Issue",
    # LLM
    "generate",
    "list_models",
    "probe",
]

__version__ = "1.0.0"
