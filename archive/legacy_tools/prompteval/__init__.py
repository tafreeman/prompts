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
    
    # Tier configuration
    from prompteval.tiers import TIERS, get_tier_info
"""

__version__ = "1.0.0"

from .core import (
    PromptEval,
    evaluate,
    evaluate_directory,
    EvalResult,
    EvalConfig,
)

from .tiers import (
    TIERS,
    TIER_CONFIGS,
    get_tier_info,
    get_tier_models,
    get_tier_name,
    list_tiers,
)

# Import find_prompts from __main__ for convenience
# This allows: from prompteval import find_prompts
def find_prompts(path, exclude=None):
    """Find all prompt files in a path.
    
    Re-exported from prompteval.__main__ for convenience.
    """
    from .__main__ import find_prompts as _find_prompts
    from pathlib import Path
    return _find_prompts(Path(path), exclude)


__all__ = [
    # Core evaluation
    "PromptEval",
    "evaluate",
    "evaluate_directory", 
    "EvalResult",
    "EvalConfig",
    # Tier configuration
    "TIERS",
    "TIER_CONFIGS",
    "get_tier_info",
    "get_tier_models",
    "get_tier_name",
    "list_tiers",
    # Discovery
    "find_prompts",
    # Version
    "__version__",
]
