"""
Tools Package
=============

Prompt evaluation and management tools for the prompts repository.

Key modules:
- prompteval: Unified prompt evaluation CLI and library
- llm_client: Multi-provider LLM client
- model_probe: Model discovery and availability checking
- validators: Prompt frontmatter and content validators

Usage:
    # After: pip install -e .
    from tools.prompteval import evaluate, TIERS
    from tools.llm.llm_client import LLMClient
    from tools.llm.model_probe import is_model_usable
"""

__version__ = "1.0.0"
