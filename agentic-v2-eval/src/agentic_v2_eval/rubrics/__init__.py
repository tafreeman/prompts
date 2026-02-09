"""Evaluation rubrics for scoring criteria.

This module provides rubric loading and management utilities.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

RUBRICS_DIR = Path(__file__).parent


def load_rubric(name: str = "default") -> dict[str, Any]:
    """Load a rubric by name.

    Args:
        name: Rubric name (without .yaml extension). Default is "default".

    Returns:
        Rubric configuration dictionary.

    Raises:
        FileNotFoundError: If rubric file doesn't exist.
    """
    rubric_path = RUBRICS_DIR / f"{name}.yaml"
    if not rubric_path.exists():
        raise FileNotFoundError(f"Rubric not found: {name}")

    with rubric_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def list_rubrics() -> list[str]:
    """List all available rubric names.

    Returns:
        List of rubric names (without .yaml extension).
    """
    return [p.stem for p in RUBRICS_DIR.glob("*.yaml")]


__all__ = [
    "load_rubric",
    "list_rubrics",
    "RUBRICS_DIR",
]
