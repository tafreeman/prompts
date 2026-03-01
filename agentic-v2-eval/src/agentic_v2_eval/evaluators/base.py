"""Abstract evaluator base class and name-based evaluator registry.

All concrete evaluators (LLM, pattern, quality, standard) inherit from
:class:`Evaluator` and register themselves via the
:meth:`EvaluatorRegistry.register` decorator so they can be looked up
by name at runtime.
"""

from __future__ import annotations

import abc
from typing import Any, Dict, Optional, Type


class Evaluator(abc.ABC):
    """Abstract base class that all evaluator implementations must extend.

    Subclasses implement :meth:`evaluate` to return a dict containing
    at minimum ``score`` (float) and ``passed`` (bool).
    """

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
    """Singleton registry mapping lowercase names to evaluator classes.

    Evaluator classes self-register at import time via the
    ``@EvaluatorRegistry.register("name")`` decorator.

    Example::

        @EvaluatorRegistry.register("custom")
        class CustomEvaluator(Evaluator):
            ...

        cls = EvaluatorRegistry.get("custom")
    """

    _registry: Dict[str, Type[Evaluator]] = {}

    @classmethod
    def register(cls, name: str):
        """Decorator to register an evaluator class under *name*.

        Args:
            name: Case-insensitive lookup key.

        Returns:
            Decorator that stores the class and returns it unchanged.
        """

        def wrapper(evaluator_cls: Type[Evaluator]):
            cls._registry[name.lower()] = evaluator_cls
            return evaluator_cls

        return wrapper

    @classmethod
    def get(cls, name: str) -> Optional[Type[Evaluator]]:
        """Retrieve a registered evaluator class by name.

        Args:
            name: Case-insensitive evaluator name.

        Returns:
            The evaluator class, or ``None`` if not registered.
        """
        return cls._registry.get(name.lower())

    @classmethod
    def list_available(cls):
        """Return the names of all registered evaluators."""
        return list(cls._registry.keys())
