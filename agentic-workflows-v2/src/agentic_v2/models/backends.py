"""LLM backend implementations.

Provides concrete backends for:
- GitHub Models API (gh:* models)
- OpenAI API (openai:* models)
- Anthropic Claude API (anthropic:* models)
- Google Gemini API (gemini:* models)
- Ollama local models (ollama:* models)
- Multi-backend dispatcher (routes by model prefix)
- Mock backend for testing
"""

from __future__ import annotations

import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, AsyncIterator, Optional

import httpx

logger = logging.getLogger(__name__)


class LLMBackend(ABC):
    """Abstract base class for LLM backends."""

    @abstractmethod
    async def complete(
        self,
        model: str,
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> str:
        """Send completion request."""
        pass

    @abstractmethod
    async def complete_chat(
        self,
        model: str,
        messages: list[dict[str, Any]],
        max_tokens: int = 4096,
        temperature: float = 0.7,
        tools: Optional[list[dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Send chat completion request with tool support."""
        pass

    async def complete_stream(
        self, model: str, prompt: str, **kwargs: Any
    ) -> AsyncIterator[str]:
        """Send streaming completion request.

        Default: non-streaming fallback.
        """
        result = await self.complete(model, prompt, **kwargs)
        yield result

    def count_tokens(self, text: str, model: str) -> int:
        """Estimate token count.

        Default: simple word-based estimate.
        """
        # Rough approximation: 1 token ≈ 4 chars
        return len(text) // 4 + 1


@dataclass
class GitHubModelsBackend(LLMBackend):
    """Backend for GitHub Models API.

    Uses the Azure AI Inference endpoint via GitHub token.
    """

    token: str = field(
        default_factory=lambda: (
            os.environ.get("GITHUB_TOKEN", "")
            or os.environ.get("GH_TOKEN", "")
        ),
        repr=False,
    )
    base_url: str = "https://models.inference.ai.azure.com"
    timeout: float = 120.0
    _client: Optional[httpx.AsyncClient] = field(default=None, repr=False)

    def __post_init__(self):
        if not self.token:
            raise ValueError(
                "GITHUB_TOKEN or GH_TOKEN environment variable required for GitHub Models"
            )

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json",
                },
            )
        return self._client

    async def complete(
        self,
        model: str,
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> str:
        """Send completion as a chat message."""
        messages = [{"role": "user", "content": prompt}]
        result = await self.complete_chat(
            model, messages, max_tokens, temperature, **kwargs
        )
        return result.get("content", "")

    async def complete_chat(
        self,
        model: str,
        messages: list[dict[str, Any]],
        max_tokens: int = 4096,
        temperature: float = 0.7,
        tools: Optional[list[dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Send chat completion request."""
        client = await self._get_client()

        # Strip provider prefix and org prefix (e.g. "gh:openai/gpt-4o-mini" -> "gpt-4o-mini")
        model_name = model.removeprefix("gh:")
        if "/" in model_name:
            model_name = model_name.split("/", 1)[1]

        payload: dict[str, Any] = {
            "model": model_name,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        response = await client.post("/chat/completions", json=payload)
        response.raise_for_status()

        data = response.json()
        choice = data.get("choices", [{}])[0]
        message = choice.get("message", {})

        return {
            "content": message.get("content", ""),
            "tool_calls": message.get("tool_calls"),
            "finish_reason": choice.get("finish_reason"),
            "model": data.get("model"),
            "usage": data.get("usage", {}),
        }

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()


@dataclass
class OpenAIBackend(LLMBackend):
    """Backend for OpenAI API."""

    api_key: str = field(
        default_factory=lambda: os.environ.get("OPENAI_API_KEY", ""),
        repr=False,
    )
    base_url: str = "https://api.openai.com/v1"
    timeout: float = 120.0
    _client: Optional[httpx.AsyncClient] = field(default=None, repr=False)

    def __post_init__(self):
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable required")

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )
        return self._client

    async def complete(
        self,
        model: str,
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> str:
        messages = [{"role": "user", "content": prompt}]
        result = await self.complete_chat(
            model, messages, max_tokens, temperature, **kwargs
        )
        return result.get("content", "")

    async def complete_chat(
        self,
        model: str,
        messages: list[dict[str, Any]],
        max_tokens: int = 4096,
        temperature: float = 0.7,
        tools: Optional[list[dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        client = await self._get_client()

        model_name = model.removeprefix("openai:")

        payload: dict[str, Any] = {
            "model": model_name,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        response = await client.post("/chat/completions", json=payload)
        response.raise_for_status()

        data = response.json()
        choice = data.get("choices", [{}])[0]
        message = choice.get("message", {})

        return {
            "content": message.get("content", ""),
            "tool_calls": message.get("tool_calls"),
            "finish_reason": choice.get("finish_reason"),
            "model": data.get("model"),
            "usage": data.get("usage", {}),
        }

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()


@dataclass
class AnthropicBackend(LLMBackend):
    """Backend for Anthropic Claude API."""

    api_key: str = field(
        default_factory=lambda: os.environ.get("ANTHROPIC_API_KEY", ""),
        repr=False,
    )
    base_url: str = "https://api.anthropic.com"
    timeout: float = 120.0
    api_version: str = "2023-06-01"
    _client: Optional[httpx.AsyncClient] = field(default=None, repr=False)

    def __post_init__(self):
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable required")

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": self.api_version,
                    "Content-Type": "application/json",
                },
            )
        return self._client

    async def complete(
        self,
        model: str,
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> str:
        messages = [{"role": "user", "content": prompt}]
        result = await self.complete_chat(
            model, messages, max_tokens, temperature, **kwargs
        )
        return result.get("content", "")

    async def complete_chat(
        self,
        model: str,
        messages: list[dict[str, Any]],
        max_tokens: int = 4096,
        temperature: float = 0.7,
        tools: Optional[list[dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        client = await self._get_client()

        model_name = model.removeprefix("anthropic:")

        payload: dict[str, Any] = {
            "model": model_name,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        if tools:
            # Convert OpenAI tool format to Anthropic format
            anthropic_tools = []
            for tool in tools:
                func = tool.get("function", tool)
                anthropic_tools.append({
                    "name": func.get("name", ""),
                    "description": func.get("description", ""),
                    "input_schema": func.get("parameters", {}),
                })
            payload["tools"] = anthropic_tools

        response = await client.post("/v1/messages", json=payload)
        response.raise_for_status()

        data = response.json()
        content_blocks = data.get("content", [])

        # Extract text from content blocks
        text_parts = []
        tool_calls = []
        for block in content_blocks:
            if block.get("type") == "text":
                text_parts.append(block.get("text", ""))
            elif block.get("type") == "tool_use":
                tool_calls.append(block)

        return {
            "content": "\n".join(text_parts),
            "tool_calls": tool_calls or None,
            "finish_reason": data.get("stop_reason", "end_turn"),
            "model": data.get("model"),
            "usage": data.get("usage", {}),
        }

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()


@dataclass
class GeminiBackend(LLMBackend):
    """Backend for Google Gemini API."""

    api_key: str = field(
        default_factory=lambda: os.environ.get("GEMINI_API_KEY", ""),
        repr=False,
    )
    base_url: str = "https://generativelanguage.googleapis.com/v1beta"
    timeout: float = 120.0
    _client: Optional[httpx.AsyncClient] = field(default=None, repr=False)

    def __post_init__(self):
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable required")

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
            )
        return self._client

    async def complete(
        self,
        model: str,
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> str:
        messages = [{"role": "user", "content": prompt}]
        result = await self.complete_chat(
            model, messages, max_tokens, temperature, **kwargs
        )
        return result.get("content", "")

    async def complete_chat(
        self,
        model: str,
        messages: list[dict[str, Any]],
        max_tokens: int = 4096,
        temperature: float = 0.7,
        tools: Optional[list[dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        client = await self._get_client()

        model_name = model.removeprefix("gemini:")

        # Convert chat messages to Gemini format
        contents = []
        for msg in messages:
            role = msg.get("role", "user")
            # Gemini uses "user" and "model" roles
            gemini_role = "model" if role == "assistant" else "user"
            contents.append({
                "role": gemini_role,
                "parts": [{"text": msg.get("content", "")}],
            })

        payload: dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": temperature,
            },
        }

        url = f"/models/{model_name}:generateContent"
        headers = {"x-goog-api-key": self.api_key}
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()
        candidates = data.get("candidates", [{}])
        if not candidates:
            return {"content": "", "tool_calls": None, "finish_reason": "error"}

        parts = candidates[0].get("content", {}).get("parts", [])
        text_parts = [p.get("text", "") for p in parts if "text" in p]

        return {
            "content": "\n".join(text_parts),
            "tool_calls": None,
            "finish_reason": candidates[0].get("finishReason", "STOP"),
            "model": model_name,
            "usage": data.get("usageMetadata", {}),
        }

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()


@dataclass
class OllamaBackend(LLMBackend):
    """Backend for Ollama local models."""

    base_url: str = "http://localhost:11434"
    timeout: float = 300.0  # Local models can be slower
    _client: Optional[httpx.AsyncClient] = field(default=None, repr=False)

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
            )
        return self._client

    async def complete(
        self,
        model: str,
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> str:
        """Send completion request to Ollama."""
        client = await self._get_client()

        # Strip provider prefix if present
        model_name = model.replace("ollama:", "")

        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
            },
        }

        response = await client.post("/api/generate", json=payload)
        response.raise_for_status()

        data = response.json()
        # Reasoning models (qwen3, deepseek-r1, phi4-reasoning) put their
        # chain-of-thought in a "thinking" field and may leave "response"
        # empty.  Fall back to "thinking" content when "response" is blank.
        text = data.get("response", "")
        if not text.strip():
            text = data.get("thinking", "")
        return text

    async def complete_chat(
        self,
        model: str,
        messages: list[dict[str, Any]],
        max_tokens: int = 4096,
        temperature: float = 0.7,
        tools: Optional[list[dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Send chat completion request to Ollama."""
        client = await self._get_client()

        # Strip provider prefix if present
        model_name = model.replace("ollama:", "")

        payload: dict[str, Any] = {
            "model": model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
            },
        }

        # Ollama supports tools for some models
        if tools:
            payload["tools"] = tools

        response = await client.post("/api/chat", json=payload)
        response.raise_for_status()

        data = response.json()
        message = data.get("message", {})

        # Reasoning models may return content in "thinking" with empty "content"
        content = message.get("content", "")
        if not content.strip():
            content = message.get("thinking", "")

        return {
            "content": content,
            "tool_calls": message.get("tool_calls"),
            "finish_reason": "stop",
            "model": model_name,
        }

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()


# ---------------------------------------------------------------------------
# Multi-backend dispatcher
# ---------------------------------------------------------------------------

# Map model prefix → backend provider name
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

        # No prefix — try OpenAI as default (bare model names like "gpt-4o")
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
        tools: Optional[list[dict[str, Any]]] = None,
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
        tools: Optional[list[dict[str, Any]]] = None,
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
    # Load .env files (project root → parent) without overwriting
    # already-set env vars.
    try:
        from dotenv import load_dotenv
        from pathlib import Path

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

    # OpenAI — most common, check first
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

    # Ollama (always register — it's local and free)
    backends["ollama"] = OllamaBackend()

    if not backends:
        raise RuntimeError(
            "No LLM backends available. Set at least one of: "
            "OPENAI_API_KEY, ANTHROPIC_API_KEY, GITHUB_TOKEN, GEMINI_API_KEY"
        )

    logger.info(
        "Auto-configured backends: %s", ", ".join(sorted(backends.keys()))
    )
    return MultiBackend(backends=backends)
