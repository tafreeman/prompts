#!/usr/bin/env python3
"""
CLI Documentation and Help System
===================================

Provides unified help across all CLI entry points.

Entry Points:
1. prompt.py       - Main user interface (interactive menu, run, eval, cove)
2. prompteval      - Focused evaluation CLI (tiers, parallel, caching)
3. prompt-tools    - Code generation wizard

Usage:
    python -c "from cli_help import print_quick_reference; print_quick_reference()"
"""

import os
import sys

# Fix Windows console encoding
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

QUICK_REFERENCE = """
================================================================================
                         PROMPT TOOLKIT - QUICK REFERENCE
================================================================================

  Entry Points:
  -----------------------------------------------------------------------------
  1. python prompt.py         - Interactive toolkit (recommended for humans)
     - Menu-driven interface for all operations
     - Commands: run, eval, cove, batch, improve, models

  2. prompteval               - Evaluation CLI (recommended for CI/scripts)
     - Focused on prompt evaluation with full control
     - Features: tiers, parallel, caching, inventory

  3. prompt-tools             - Code generation wizard
     - Interactive code artifact creation
     - Commands: create, generate, wizard

  Common Tasks:
  -----------------------------------------------------------------------------
  > Evaluate a folder:
    prompteval prompts/advanced/ --tier 2 --verbose

  > Quick structural check (no LLM):
    prompteval prompts/ --tier 0

  > Cross-model validation:
    prompteval prompts/ --tier 3

  > Parallel evaluation (4 workers):
    prompteval prompts/ --parallel 4

  > With caching (avoid redundant API calls):
    prompteval prompts/ --cache

  > CI mode (exit code based on pass/fail):
    prompteval prompts/ --ci --threshold 70

  > Run a single prompt:
    python prompt.py run prompts/basic/greeting.md

  > Chain-of-Verification:
    python prompt.py cove "When was Python created?"

  Models:
  -----------------------------------------------------------------------------
  Local (FREE, always available):
    phi4, mistral, phi-silica

  Cloud (require GITHUB_TOKEN):
    gpt-4o-mini, gpt-4o, claude-sonnet, gemini-flash

  Ollama (requires Ollama running):
    ollama:llama3, ollama:deepseek-coder, etc.

  Tiers:
  -----------------------------------------------------------------------------
  0 - Structural Only    (instant, no LLM)
  1 - Quick Local        (phi4 x 1)
  2 - Standard Local     (phi4 x 2)         <- DEFAULT
  3 - Cross-Validate     (phi4 + mistral)
  4 - Cloud Quick        (gpt-4o-mini x 1)
  5 - Cloud Standard     (gpt-4o x 2)
  6 - Cloud Cross        (gpt-4o + claude)
  7 - Full Suite         (all available)
================================================================================
"""


def print_quick_reference():
    """Print the quick reference guide."""
    print(QUICK_REFERENCE)


def get_cli_summary():
    """Get a summary of all CLI entry points."""
    return {
        "entry_points": [
            {
                "name": "prompt.py",
                "command": "python prompt.py",
                "description": "Interactive toolkit with menu-driven interface",
                "best_for": "Humans exploring the toolkit",
                "commands": [
                    "run",
                    "eval",
                    "cove",
                    "batch",
                    "improve",
                    "models",
                    "help",
                ],
            },
            {
                "name": "prompteval",
                "command": "prompteval OR python -m prompteval",
                "description": "Focused evaluation CLI with full control",
                "best_for": "CI/CD pipelines and scripts",
                "features": ["tiers", "parallel", "caching", "inventory", "fail-fast"],
            },
            {
                "name": "prompt-tools",
                "command": "prompt-tools",
                "description": "Code generation wizard",
                "best_for": "Creating new code artifacts",
                "commands": ["interactive", "create", "generate", "eval"],
            },
        ],
        "common_tasks": {
            "evaluate_folder": "prompteval prompts/advanced/ --tier 2",
            "structural_only": "prompteval prompts/ --tier 0",
            "cross_validate": "prompteval prompts/ --tier 3",
            "parallel": "prompteval prompts/ --parallel 4",
            "with_cache": "prompteval prompts/ --cache",
            "ci_mode": "prompteval prompts/ --ci --threshold 70",
            "run_prompt": "python prompt.py run prompts/greeting.md",
            "chain_verify": "python prompt.py cove 'question here'",
        },
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        import json

        print(json.dumps(get_cli_summary(), indent=2))
    else:
        print_quick_reference()
