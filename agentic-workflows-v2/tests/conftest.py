"""Shared test fixtures.

Ensures the global LLM client is reset before each test so that
unit tests get a backend-less client (placeholder mode) unless they
explicitly configure one.

The fixture pre-creates a backend-less client so that even calls to
``get_client(auto_configure=True)`` inside agent_resolver return the
placeholder client rather than probing for Ollama/cloud backends.
"""

import pytest

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
