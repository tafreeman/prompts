"""Feature flags for agentic-workflows-v2.

Flags gate new capabilities so they can be enabled independently in dev
and disabled by default in production.  Values are resolved in order:

1. YAML config file (if provided)
2. Environment variable override (``AGENTIC_FF_<UPPER_NAME>=true``)
3. Dataclass defaults (all ``False``)
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_ENV_PREFIX = "AGENTIC_FF_"


@dataclass
class FeatureFlags:
    """Boolean feature gates."""

    iterative_strategy: bool = False
    per_agent_scoring: bool = False
    microsoft_adapter: bool = False
    docker_runtime: bool = False


def load_feature_flags(config_path: Path | str | None = None) -> FeatureFlags:
    """Build a ``FeatureFlags`` instance from optional YAML + env vars."""
    values: dict[str, Any] = {}

    # 1. Load from YAML if provided
    if config_path is not None:
        path = Path(config_path)
        if path.is_file():
            try:
                import yaml

                raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
                ff_section = raw.get("feature_flags", raw)
                if isinstance(ff_section, dict):
                    values.update(ff_section)
            except Exception:
                logger.warning("Failed to load feature flags from %s", path, exc_info=True)

    # 2. Apply env-var overrides
    for f in fields(FeatureFlags):
        env_key = f"{_ENV_PREFIX}{f.name.upper()}"
        env_val = os.environ.get(env_key)
        if env_val is not None:
            values[f.name] = env_val.strip().lower() in {"1", "true", "yes", "on"}

    # 3. Build dataclass, ignoring unknown keys
    known = {f.name for f in fields(FeatureFlags)}
    filtered = {k: v for k, v in values.items() if k in known}
    return FeatureFlags(**filtered)


# ---------------------------------------------------------------------------
# Global singleton
# ---------------------------------------------------------------------------

_default_flags: FeatureFlags | None = None


def get_flags() -> FeatureFlags:
    """Return the lazily-initialised global ``FeatureFlags``."""
    global _default_flags
    if _default_flags is None:
        _default_flags = load_feature_flags()
    return _default_flags


def reset_flags() -> None:
    """Reset the global singleton (useful in tests)."""
    global _default_flags
    _default_flags = None


def is_enabled(flag_name: str) -> bool:
    """Check a flag by name on the global instance."""
    return getattr(get_flags(), flag_name, False)
