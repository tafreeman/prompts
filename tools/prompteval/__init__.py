"""
PromptEval - Unified Prompt Evaluation Tool
============================================

A lean, powerful tool for evaluating prompts against quality standards.

Reuses existing infrastructure:
- llm_client.py for multi-provider LLM access
- local_model.py for free local evaluation (G-Eval, direct scoring)
- rubrics/*.yaml for scoring dimensions

Usage:
    # CLI
    python -m prompteval evaluate prompts/advanced/
    python -m prompteval evaluate prompt.md --tier 2 --output report.json
    
    # Python API
    from prompteval import evaluate
    result = evaluate("prompts/example.md")
"""

__version__ = "1.0.0"

from .core import (
    PromptEval,
    evaluate,
    evaluate_directory,
    EvalResult,
    EvalConfig,
)

__all__ = [
    "PromptEval",
    "evaluate",
    "evaluate_directory", 
    "EvalResult",
    "EvalConfig",
    "__version__",
]
