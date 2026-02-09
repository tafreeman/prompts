"""Smoke tests for the in-repo `agentic-workflows-v2/` scaffold.

These tests are intentionally lightweight and should not require any network
access or model providers.

Note: The repo-level pytest config (`pytest.ini`) only collects tests under
`testing/`, so we keep these here.
"""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_agentic_v2_on_path() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    pkg_src = repo_root / "agentic-workflows-v2" / "src"
    if not pkg_src.exists():
        raise AssertionError(f"Expected package source directory to exist: {pkg_src}")

    # Prepend so we test the in-repo sources, not some globally installed package.
    sys.path.insert(0, str(pkg_src))


def test_agentic_v2_imports() -> None:
    _ensure_agentic_v2_on_path()

    import agentic_v2  # noqa: F401


def test_agentic_v2_version_is_exposed() -> None:
    _ensure_agentic_v2_on_path()

    import agentic_v2

    assert hasattr(agentic_v2, "__version__")
    assert isinstance(agentic_v2.__version__, str)
    assert agentic_v2.__version__.strip() != ""
