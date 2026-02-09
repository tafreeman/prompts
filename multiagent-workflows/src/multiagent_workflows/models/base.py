"""Base Model Provider.

Abstract base class for model provider implementations.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, AsyncIterator, Dict, List, Optional


@dataclass
class ProviderConfig:
    """Configuration for a model provider."""

    name: str
    endpoint: Optional[str] = None
    api_key_env: Optional[str] = None
    timeout_seconds: int = 120


@dataclass
class GenerationParams:
    """Parameters for text generation."""

    temperature: float = 0.7
    max_tokens: int = 4096
    top_p: float = 1.0
    stop_sequences: Optional[List[str]] = None


class BaseModelProvider(ABC):
    """Abstract base class for model provider implementations.

    Subclasses should implement:
    - generate(): Synchronous generation
    - generate_async(): Async generation
    - stream(): Streaming generation
    - list_models(): List available models
    - check_health(): Health check
    """

    def __init__(self, config: ProviderConfig):
        self.config = config

    @abstractmethod
    async def generate(
        self,
        model_id: str,
        prompt: str,
        system_prompt: Optional[str] = None,
        params: Optional[GenerationParams] = None,
    ) -> str:
        """Generate text from a prompt."""
        pass

    @abstractmethod
    async def stream(
        self,
        model_id: str,
        prompt: str,
        system_prompt: Optional[str] = None,
        params: Optional[GenerationParams] = None,
    ) -> AsyncIterator[str]:
        """Stream text generation."""
        pass

    @abstractmethod
    async def list_models(self) -> List[Dict[str, Any]]:
        """List available models from this provider."""
        pass

    @abstractmethod
    async def check_health(self) -> bool:
        """Check if the provider is healthy and available."""
        pass
