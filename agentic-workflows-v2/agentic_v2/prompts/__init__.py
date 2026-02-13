"""Prompt templates for agentic_v2 agents.

This module provides system prompts for various agent roles. Prompts are
stored as markdown files and loaded dynamically.
"""

from __future__ import annotations

from functools import lru_cache
import logging
from pathlib import Path
from typing import Optional

from ..storage import get_catalog_store

# Directory containing prompt templates
PROMPTS_DIR = Path(__file__).parent
logger = logging.getLogger(__name__)


def _sync_prompt_to_store(prompt_path: Path) -> None:
    try:
        get_catalog_store().sync_prompt_file(prompt_path)
    except Exception:
        logger.debug("Failed syncing prompt %s to catalog store", prompt_path.name, exc_info=True)


@lru_cache(maxsize=32)
def load_prompt(name: str) -> str:
    """Load a prompt template by name.

    Args:
        name: Prompt name (e.g., 'architect', 'coder', 'tester')
              Extension '.md' is optional.

    Returns:
        The prompt content as a string.

    Raises:
        FileNotFoundError: If prompt file doesn't exist.
    """
    if not name.endswith(".md"):
        name = f"{name}.md"

    prompt_path = PROMPTS_DIR / name
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt not found: {name}")

    _sync_prompt_to_store(prompt_path)
    return prompt_path.read_text(encoding="utf-8")


def list_prompts() -> list[str]:
    """List all available prompt names.

    Returns:
        List of prompt names (without .md extension).
    """
    try:
        get_catalog_store().sync_prompt_directory()
    except Exception:
        logger.debug("Failed syncing prompt directory to catalog store", exc_info=True)
    return [p.stem for p in PROMPTS_DIR.glob("*.md")]


def get_prompt_path(name: str) -> Optional[Path]:
    """Get the path to a prompt file.

    Args:
        name: Prompt name (without .md extension).

    Returns:
        Path to the prompt file, or None if not found.
    """
    prompt_path = PROMPTS_DIR / f"{name}.md"
    return prompt_path if prompt_path.exists() else None


# Pre-defined prompt names for type hints and autocompletion
ANALYST = "analyst"
ARCHITECT = "architect"
CODER = "coder"
DEBUGGER = "debugger"
JUDGE = "judge"
PLANNER = "planner"
REASONER = "reasoner"
RESEARCHER = "researcher"
REVIEWER = "reviewer"
TESTER = "tester"
VALIDATOR = "validator"
VISION = "vision"
WRITER = "writer"

__all__ = [
    "load_prompt",
    "list_prompts",
    "get_prompt_path",
    "PROMPTS_DIR",
    # Prompt name constants
    "ANALYST",
    "ARCHITECT",
    "CODER",
    "DEBUGGER",
    "JUDGE",
    "PLANNER",
    "REASONER",
    "RESEARCHER",
    "REVIEWER",
    "TESTER",
    "VALIDATOR",
    "VISION",
    "WRITER",
]
