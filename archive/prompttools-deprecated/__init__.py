"""
PromptTools: Simple, effective prompt evaluation and validation toolkit.

.. deprecated:: 2.0.0
    This package is deprecated. Use `tools.prompteval` instead:

    - `from tools.prompteval import score_prompt` (evaluation)
    - `from tools.llm import LLMClient` (LLM access)
    - `from tools.validators import validate_frontmatter` (validation)

    This module will be removed in a future release.

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

import warnings as _warnings

_warnings.warn(
    "prompttools is deprecated. Use 'tools.prompteval' and 'tools.llm' instead. "
    "See tools/README.md for migration guide.",
    DeprecationWarning,
    stacklevel=2,
)

from .evaluate import EvalResult, evaluate, evaluate_batch
from .llm import generate, list_models, probe
from .validate import Issue, validate, validate_batch

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
