"""Adapter layer — pluggable execution engine backends.

Provides :func:`get_registry` for discovering and instantiating
execution engine adapters.  Built-in adapters are auto-registered
on import.

Usage::

    from agentic_v2.adapters import get_registry

    registry = get_registry()
    engine = registry.get_adapter("native")
    result = await engine.execute(dag, ctx)
"""

from .registry import AdapterRegistry, get_registry

# Auto-register built-in adapters
from . import native as _native_adapter  # noqa: F401 — triggers registration

try:
    from . import langchain as _langchain_adapter  # noqa: F401 — triggers registration
except ImportError:  # pragma: no cover — optional dependency
    pass

__all__ = [
    "AdapterRegistry",
    "get_registry",
]
