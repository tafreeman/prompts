"""Base evaluator interfaces and registry."""

from __future__ import annotations

import abc
from typing import Any, Dict, Optional, Type


class Evaluator(abc.ABC):
    """Abstract base class for all evaluators."""

    @abc.abstractmethod
    def evaluate(self, output: Any, **kwargs) -> Dict[str, Any]:
        """Evaluate an output.

        Args:
            output: The output to evaluate (string, dict, etc.)
            **kwargs: Additional context (e.g., ground_truth, inputs)

        Returns:
            Dict containing at least 'score' and 'passed'.
        """
        pass


class EvaluatorRegistry:
    """Registry for loading evaluators by name."""

    _registry: Dict[str, Type[Evaluator]] = {}

    @classmethod
    def register(cls, name: str):
        """Decorator to register an evaluator."""

        def wrapper(evaluator_cls: Type[Evaluator]):
            cls._registry[name.lower()] = evaluator_cls
            return evaluator_cls

        return wrapper

    @classmethod
    def get(cls, name: str) -> Optional[Type[Evaluator]]:
        """Get an evaluator class by name."""
        return cls._registry.get(name.lower())

    @classmethod
    def list_available(cls):
        """List registered evaluators."""
        return list(cls._registry.keys())
