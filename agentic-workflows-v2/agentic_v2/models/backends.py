"""LLM backend implementations.

Provides concrete backends for:
- GitHub Models API (gh:* models)
- OpenAI API (openai:* models)
- Anthropic Claude API (anthropic:* models)
- Google Gemini API (gemini:* models)
- Ollama local models (ollama:* models)
- Multi-backend dispatcher (routes by model prefix)
- Mock backend for testing

Implementation classes live in submodules; this module re-exports
everything so that ``from agentic_v2.models.backends import X`` keeps
working unchanged.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from typing import Any, AsyncIterator

from .backends_base import LLMBackend
from .backends_cloud import (
    AnthropicBackend,
    GeminiBackend,
    GitHubModelsBackend,
    OpenAIBackend,
)
from .backends_local import OllamaBackend

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Multi-backend dispatcher
# ---------------------------------------------------------------------------

# Map model prefix -> backend provider name
PREFIX_MAP: dict[str, str] = {
    "gh:": "github",
    "openai:": "openai",
    "anthropic:": "anthropic",
    "gemini:": "gemini",
    "ollama:": "ollama",
    "local:": "ollama",  # local models route through Ollama
}


@dataclass
class MultiBackend(LLMBackend):
    """Dispatches to the correct backend based on model prefix.

    This allows the router to suggest models from any provider and have
    them automatically handled by the right backend.
    """

    backends: dict[str, LLMBackend] = field(default_factory=dict)

    def _get_backend(self, model: str) -> LLMBackend:
        for prefix, provider in PREFIX_MAP.items():
            if model.startswith(prefix):
                backend = self.backends.get(provider)
                if backend is None:
                    raise RuntimeError(
                        f"No backend configured for provider '{provider}' "
                        f"(model: {model})"
                    )
                return backend

        # No prefix -- try OpenAI as default (bare model names like "gpt-4o")
        if "openai" in self.backends:
            return self.backends["openai"]

        raise RuntimeError(
            f"Cannot determine backend for model '{model}'. "
            f"Available backends: {list(self.backends.keys())}"
        )

    async def complete(
        self,
        model: str,
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> str:
        return await self._get_backend(model).complete(
            model, prompt, max_tokens, temperature, **kwargs
        )

    async def complete_chat(
        self,
        model: str,
        messages: list[dict[str, Any]],
        max_tokens: int = 4096,
        temperature: float = 0.7,
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return await self._get_backend(model).complete_chat(
            model, messages, max_tokens, temperature, tools, **kwargs
        )

    async def complete_stream(
        self, model: str, prompt: str, **kwargs: Any
    ) -> AsyncIterator[str]:
        async for chunk in self._get_backend(model).complete_stream(
            model, prompt, **kwargs
        ):
            yield chunk

    async def close(self) -> None:
        for backend in self.backends.values():
            if hasattr(backend, "close"):
                await backend.close()


@dataclass
class MockBackend(LLMBackend):
    """Mock backend for testing.

    Returns configurable responses without making real API calls.
    """

    default_response: str = "This is a mock response."
    responses: dict[str, str] = field(default_factory=dict)
    call_history: list[dict[str, Any]] = field(default_factory=list)

    def set_response(self, pattern: str, response: str) -> None:
        """Set a canned response for prompts containing pattern."""
        self.responses[pattern] = response

    async def complete(
        self,
        model: str,
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> str:
        """Return mock response."""
        self.call_history.append(
            {
                "method": "complete",
                "model": model,
                "prompt": prompt,
                "kwargs": kwargs,
            }
        )

        # Check for pattern matches
        for pattern, response in self.responses.items():
            if pattern.lower() in prompt.lower():
                return response

        return self.default_response

    async def complete_chat(
        self,
        model: str,
        messages: list[dict[str, Any]],
        max_tokens: int = 4096,
        temperature: float = 0.7,
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Return mock chat response."""
        self.call_history.append(
            {
                "method": "complete_chat",
                "model": model,
                "messages": messages,
                "tools": tools,
                "kwargs": kwargs,
            }
        )

        # Get last user message for pattern matching
        last_user = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                last_user = msg.get("content", "")
                break

        # Check for pattern matches
        for pattern, response in self.responses.items():
            if pattern.lower() in last_user.lower():
                return {"content": response, "tool_calls": None}

        return {"content": self.default_response, "tool_calls": None}


# ---------------------------------------------------------------------------
# Factory functions
# ---------------------------------------------------------------------------


def get_backend(provider: str = "github") -> LLMBackend:
    """Factory function to get a single LLM backend.

    Args:
        provider: One of 'github', 'openai', 'anthropic', 'gemini', 'ollama', 'mock'

    Returns:
        Configured LLM backend
    """
    if provider == "github":
        return GitHubModelsBackend()
    elif provider == "openai":
        return OpenAIBackend()
    elif provider == "anthropic":
        return AnthropicBackend()
    elif provider == "gemini":
        return GeminiBackend()
    elif provider == "ollama":
        return OllamaBackend()
    elif provider == "mock":
        return MockBackend()
    else:
        raise ValueError(f"Unknown provider: {provider}")


def auto_configure_backend() -> LLMBackend:
    """Auto-detect available API keys and build a MultiBackend.

    Probes env vars in priority order and registers all available backends.
    Returns a MultiBackend that dispatches based on model prefix.

    Loads .env files from the project root if ``python-dotenv`` is
    installed, so API keys stored there are picked up automatically.
    """
    # Load .env files (project root -> parent) without overwriting
    # already-set env vars.
    try:
        from pathlib import Path

        from dotenv import load_dotenv

        # Walk upwards from this file looking for .env
        for parent in Path(__file__).resolve().parents:
            env_path = parent / ".env"
            if env_path.is_file():
                load_dotenv(env_path, override=False)
                logger.debug("Loaded env from %s", env_path)
                break
    except ImportError:
        pass

    backends: dict[str, LLMBackend] = {}

    # OpenAI -- most common, check first
    if os.environ.get("OPENAI_API_KEY"):
        try:
            backends["openai"] = OpenAIBackend()
            logger.info("Registered OpenAI backend")
        except ValueError:
            pass

    # Anthropic
    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            backends["anthropic"] = AnthropicBackend()
            logger.info("Registered Anthropic backend")
        except ValueError:
            pass

    # GitHub Models (check both GITHUB_TOKEN and GH_TOKEN)
    if os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"):
        try:
            backends["github"] = GitHubModelsBackend()
            logger.info("Registered GitHub Models backend")
        except ValueError:
            pass

    # Gemini
    if os.environ.get("GEMINI_API_KEY"):
        try:
            backends["gemini"] = GeminiBackend()
            logger.info("Registered Gemini backend")
        except ValueError:
            pass

    # Ollama (always register -- it's local and free)
    backends["ollama"] = OllamaBackend()

    if not backends:
        raise RuntimeError(
            "No LLM backends available. Set at least one of: "
            "OPENAI_API_KEY, ANTHROPIC_API_KEY, GITHUB_TOKEN, GEMINI_API_KEY"
        )

    logger.info("Auto-configured backends: %s", ", ".join(sorted(backends.keys())))
    return MultiBackend(backends=backends)


__all__ = [
    # Re-exported from submodules for backward compatibility
    "LLMBackend",
    "GitHubModelsBackend",
    "OpenAIBackend",
    "AnthropicBackend",
    "GeminiBackend",
    "OllamaBackend",
    # Defined here
    "PREFIX_MAP",
    "MultiBackend",
    "MockBackend",
    "get_backend",
    "auto_configure_backend",
]
