"""RED-phase tests for AGENTIC_NO_LLM=1 short-circuit in langchain/models.py.

These tests MUST FAIL until Stage 2 (Amelia) wires the production code.
Production code they target does NOT yet exist:
  - build_placeholder_model() in agentic_v2.langchain.model_builders
  - get_chat_model() short-circuit when agentic_no_llm is true
  - PlaceholderChatModel with _llm_type == "placeholder" and bind_tools no-op
"""

from __future__ import annotations

import pytest

# Skip this entire module at collection time if langchain_core is not installed.
# Users running only the native suite must not be forced to install LangChain.
langchain_core = pytest.importorskip("langchain_core")

from agentic_v2.settings import get_settings
from agentic_v2.langchain.models import get_chat_model

_PLACEHOLDER_PREFIX = "[AGENTIC_NO_LLM placeholder]"


@pytest.fixture(autouse=True)
def _isolate_settings(monkeypatch):
    """Bust the settings LRU cache before and after every test so that
    monkeypatch env changes are visible to get_settings() callers.
    """
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.mark.unit
def test_flag_returns_placeholder_chat_model_without_credentials(monkeypatch):
    """AGENTIC_NO_LLM=1 must let get_chat_model() return a placeholder model
    even when GITHUB_TOKEN is absent — no credential error should be raised.

    FAILS today: get_chat_model() calls build_github_model() which raises
    ValueError("GITHUB_TOKEN environment variable is required...") before
    the flag short-circuit exists.
    """
    monkeypatch.setenv("AGENTIC_NO_LLM", "1")
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    get_settings.cache_clear()

    model = get_chat_model("gh:openai/gpt-4o")

    assert model._llm_type == "placeholder", (
        f"Expected _llm_type='placeholder', got {model._llm_type!r}"
    )


@pytest.mark.unit
def test_flag_placeholder_generates_prefixed_aimessage(monkeypatch):
    """Invoking the placeholder model must return an AIMessage whose content
    starts with the placeholder prefix.

    FAILS today: get_chat_model() never reaches the placeholder path.
    """
    from langchain_core.messages import HumanMessage

    monkeypatch.setenv("AGENTIC_NO_LLM", "1")
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    get_settings.cache_clear()

    model = get_chat_model("gh:openai/gpt-4o")
    result = model.invoke([HumanMessage(content="hi")])

    assert result.content.startswith(_PLACEHOLDER_PREFIX), (
        f"AIMessage content {result.content!r} does not start with "
        f"{_PLACEHOLDER_PREFIX!r}"
    )


@pytest.mark.unit
def test_flag_bind_tools_is_noop_and_still_returns_placeholder(monkeypatch):
    """bind_tools() on the placeholder model must degrade cleanly.

    After binding a tool schema, invoke() must still return a placeholder
    AIMessage — no errors, no real tool calls.

    FAILS today: get_chat_model() never reaches the placeholder path.
    """
    from langchain_core.messages import HumanMessage

    monkeypatch.setenv("AGENTIC_NO_LLM", "1")
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    get_settings.cache_clear()

    bound_model = get_chat_model("gh:openai/gpt-4o").bind_tools(
        [
            {
                "type": "function",
                "function": {
                    "name": "noop",
                    "description": "x",
                    "parameters": {"type": "object", "properties": {}},
                },
            }
        ]
    )
    result = bound_model.invoke([HumanMessage(content="hi")])

    assert result.content.startswith(_PLACEHOLDER_PREFIX), (
        f"After bind_tools(), AIMessage content {result.content!r} does not "
        f"start with {_PLACEHOLDER_PREFIX!r}"
    )


@pytest.mark.unit
def test_flag_unset_still_raises_on_missing_credentials(monkeypatch):
    """When AGENTIC_NO_LLM is absent, get_chat_model('gh:...') must still
    raise ValueError mentioning GITHUB_TOKEN when the token is not set.

    This is the no-regression control — the short-circuit must be strictly
    gated on the flag.
    """
    monkeypatch.delenv("AGENTIC_NO_LLM", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    get_settings.cache_clear()

    with pytest.raises(ValueError, match="GITHUB_TOKEN"):
        get_chat_model("gh:openai/gpt-4o")
