"""LangChain execution engine adapter.

Auto-registers the :class:`LangChainEngine` adapter when this package
is imported, provided that the LangChain/LangGraph dependencies are
available.  If they are not installed, registration is silently skipped.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

try:
    from ...core.errors import AdapterError
    from ..registry import get_registry
    from .engine import LangChainEngine

    get_registry().register("langchain", LangChainEngine)
except ImportError:
    logger.debug(
        "LangChain/LangGraph not installed — skipping langchain adapter registration"
    )
except AdapterError:
    # Adapter may already be registered (e.g. during test re-imports).
    # Log and continue rather than crashing the import chain.
    logger.debug("langchain adapter registration skipped (already registered?)")

__all__ = ["LangChainEngine"]
