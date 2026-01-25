"""Token estimation utilities."""

from __future__ import annotations

from typing import Dict


def estimate_tokens(text: str) -> int:
    """Rough token estimate based on character length.

    Empirically, English text averages ~4 chars per token.
    """
    if not text:
        return 0
    return max(1, len(text) // 4)


def estimate_message_tokens(messages: Dict[str, str]) -> int:
    """Estimate tokens from a dict of message parts."""
    total = 0
    for value in messages.values():
        total += estimate_tokens(str(value))
    return total
