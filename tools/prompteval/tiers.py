#!/usr/bin/env python3
"""
PromptEval Tiers Module
=======================

Centralized tier configuration for prompt evaluation.
Import tier definitions from here to avoid circular imports and provide
a clean public API.

Usage:
    from prompteval.tiers import TIERS, TIER_CONFIGS, get_tier_info
    
    tier_info = TIERS.get(2)
    # {'name': 'Local G-Eval', 'models': ['mistral'], ...}
"""

from typing import Dict, Any, List

# =============================================================================
# TIER CONFIGURATIONS
# =============================================================================

TIER_CONFIGS: Dict[int, Dict[str, Any]] = {
    0: {"name": "Structural", "models": [], "runs": 1, "cost": "$0", "time": "<1s"},
    1: {"name": "Local Quick", "models": ["phi4"], "runs": 1, "cost": "$0", "time": "~30s"},
    2: {"name": "Local G-Eval", "models": ["mistral"], "runs": 1, "cost": "$0", "time": "~60s"},
    3: {"name": "Local Cross", "models": ["phi4", "mistral", "phi3.5"], "runs": 2, "cost": "$0", "time": "~5min"},
    4: {"name": "Cloud Quick", "models": ["deepseek-r1"], "runs": 1, "cost": "~$0.01", "time": "~5s"},
    5: {"name": "Cloud Cross", "models": ["gpt-4o-mini", "deepseek-r1", "llama-70b"], "runs": 2, "cost": "~$0.10", "time": "~30s"},
    6: {"name": "Premium", "models": ["phi4", "mistral", "deepseek-r1", "gpt-4.1", "llama-70b"], "runs": 3, "cost": "~$0.30", "time": "~2min"},
    7: {"name": "Enterprise", "models": ["phi4", "mistral", "deepseek-r1", "gpt-4.1", "llama-70b"], "runs": 4, "cost": "~$0.50", "time": "~5min"},
}

# Alias for backward compatibility
TIERS = TIER_CONFIGS


def get_tier_info(tier: int) -> Dict[str, Any]:
    """
    Get configuration for a specific tier.
    
    Args:
        tier: Tier number (0-7)
        
    Returns:
        Dict with keys: name, models, runs, cost, time
        
    Raises:
        ValueError: If tier number is invalid
    """
    if tier not in TIER_CONFIGS:
        raise ValueError(f"Invalid tier {tier}. Valid tiers: {list(TIER_CONFIGS.keys())}")
    return TIER_CONFIGS[tier]


def get_tier_models(tier: int) -> List[str]:
    """Get the models used for a specific tier."""
    return get_tier_info(tier).get("models", [])


def get_tier_name(tier: int) -> str:
    """Get the human-readable name for a tier."""
    return get_tier_info(tier).get("name", f"Tier {tier}")


def list_tiers() -> None:
    """Print all tier configurations."""
    print("\nEvaluation Tiers:")
    print("-" * 70)
    for t, c in TIER_CONFIGS.items():
        models_str = ", ".join(c["models"]) if c["models"] else "None (structural only)"
        print(f"  Tier {t}: {c['name']}")
        print(f"    Models: {models_str}")
        print(f"    Runs: {c['runs']}, Cost: {c['cost']}, Time: {c['time']}")
        print()


__all__ = [
    "TIERS",
    "TIER_CONFIGS",
    "get_tier_info",
    "get_tier_models",
    "get_tier_name",
    "list_tiers",
]
