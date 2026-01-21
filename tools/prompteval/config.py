"""Legacy configuration objects for tests.

A small subset of the previous PromptEval configuration API is retained to
avoid churn in the test suite.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EvalConfig:
    model: str = "local:phi4mini"
    temperature: float = 0.1
    max_tokens: int = 1024
