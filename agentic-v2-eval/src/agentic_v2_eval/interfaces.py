"""Interfaces for Agentic V2 Evaluation."""

from typing import Any, Protocol, runtime_checkable

@runtime_checkable
class LLMClientProtocol(Protocol):
    """Protocol for LLM interactions to decouple evaluation from specific clients."""

    def generate_text(
        self,
        model_name: str,
        prompt: str,
        temperature: float = 0.1,
        max_tokens: int = 1000,
        **kwargs: Any,
    ) -> str:
        """Generate text from a prompt."""
        ...

class Evaluator(Protocol):
    """Protocol for specific evaluation strategies."""

    def evaluate(self, output: str, expected: str | None = None, **kwargs: Any) -> dict[str, Any]:
        """Evaluate an output against expectations."""
        ...
