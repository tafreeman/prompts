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

# Auto-register built-in adapters
from . import native as _native_adapter
from .registry import AdapterRegistry, get_registry

try:
    from . import langchain as _langchain_adapter
except ImportError:  # pragma: no cover — optional dependency
    pass

__all__ = [
    "AdapterRegistry",
    "get_registry",
]
