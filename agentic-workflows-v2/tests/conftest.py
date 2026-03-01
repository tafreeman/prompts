"""Shared test fixtures.

Ensures the global LLM client is reset before each test so that
unit tests get a backend-less client (placeholder mode) unless they
explicitly configure one.

The fixture pre-creates a backend-less client so that even calls to
``get_client(auto_configure=True)`` inside agent_resolver return the
placeholder client rather than probing for Ollama/cloud backends.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest
import yaml

from agentic_v2.models.client import get_client, reset_client


@pytest.fixture(autouse=True)
def _reset_llm_client():
    """Pre-create a backend-less global client for each test."""
    reset_client()
    # Eagerly create a backend-less client; subsequent get_client() calls
    # will return this instance because _client is no longer None.
    get_client(auto_configure=False)
    yield
    reset_client()


@pytest.fixture
def mock_backend() -> MagicMock:
    """Return a mock LLM backend that echoes its prompt."""
    backend = MagicMock()
    backend.generate.side_effect = lambda prompt, **_kw: f"mock: {prompt[:50]}"
    return backend


@pytest.fixture
def workflow_dir(tmp_path: Path) -> Path:
    """Temporary directory pre-configured for workflow YAML files."""
    return tmp_path


@pytest.fixture
def simple_workflow_yaml(workflow_dir: Path) -> Path:
    """A minimal single-step workflow YAML for use in tests."""
    data = {
        "name": "test-workflow",
        "description": "Minimal workflow for tests",
        "steps": [
            {
                "name": "step-one",
                "agent": "tier1",
                "description": "First step",
                "depends_on": [],
                "inputs": {"prompt": "hello"},
                "outputs": ["result"],
            }
        ],
    }
    path = workflow_dir / "test_workflow.yaml"
    path.write_text(yaml.dump(data), encoding="utf-8")
    return path


@pytest.fixture
def agent_config() -> dict[str, Any]:
    """Default agent configuration dict for tests."""
    return {
        "tier": "tier1",
        "model": "placeholder",
        "temperature": 0.0,
        "max_tokens": 512,
    }
