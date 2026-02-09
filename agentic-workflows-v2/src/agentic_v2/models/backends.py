"""LLM backend implementations.

Provides concrete backends for:
- GitHub Models API
- Ollama local models
- Mock backend for testing
"""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, AsyncIterator, Optional

import httpx


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

    token: str = field(default_factory=lambda: os.environ.get("GITHUB_TOKEN", ""))
    base_url: str = "https://models.inference.ai.azure.com"
    timeout: float = 120.0
    _client: Optional[httpx.AsyncClient] = field(default=None, repr=False)

    def __post_init__(self):
        if not self.token:
            raise ValueError(
                "GITHUB_TOKEN environment variable required for GitHub Models"
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

        # Strip provider prefix if present
        model_name = model.replace("gh:", "")

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
        return data.get("response", "")

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

        return {
            "content": message.get("content", ""),
            "tool_calls": message.get("tool_calls"),
            "finish_reason": "stop",
            "model": model_name,
        }

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()


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


def get_backend(provider: str = "github") -> LLMBackend:
    """Factory function to get an LLM backend.

    Args:
        provider: One of 'github', 'ollama', 'mock'

    Returns:
        Configured LLM backend
    """
    if provider == "github":
        return GitHubModelsBackend()
    elif provider == "ollama":
        return OllamaBackend()
    elif provider == "mock":
        return MockBackend()
    else:
        raise ValueError(f"Unknown provider: {provider}")
