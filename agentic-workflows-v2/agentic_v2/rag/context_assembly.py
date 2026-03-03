"""RAG context assembly — token-budget-aware result assembler.

Provides:
- :class:`TokenBudgetAssembler`: Greedily assembles retrieval results into a
  :class:`RAGResponse` within a configurable token budget.
"""

from __future__ import annotations

import logging
from typing import Callable

from .contracts import RAGResponse, RetrievalResult

logger = logging.getLogger(__name__)


def _default_token_estimator(text: str) -> int:
    """Estimate token count as ``len(text) // 4``.

    This is the same heuristic used by ConversationMemory and is a
    reasonable approximation for English text across most tokenizers.

    Args:
        text: The text to estimate tokens for.

    Returns:
        Estimated token count.
    """
    return len(text) // 4


class TokenBudgetAssembler:
    """Assemble retrieval results into a RAGResponse within a token budget.

    Greedily adds results in descending score order until the token budget
    is exhausted.  Never exceeds ``max_tokens``.

    Args:
        max_tokens: Maximum token budget for assembled context.
        token_estimator: Callable that estimates tokens for a given text.
            Defaults to ``len(text) // 4``.
    """

    def __init__(
        self,
        *,
        max_tokens: int = 4000,
        token_estimator: Callable[[str], int] | None = None,
    ) -> None:
        self._max_tokens = max_tokens
        self._estimate_tokens = token_estimator or _default_token_estimator

    def assemble(
        self,
        results: list[RetrievalResult],
        *,
        query: str | None = None,
    ) -> RAGResponse:
        """Assemble retrieval results into a RAGResponse within token budget.

        Results are sorted by score (descending) and greedily added until
        the budget is exhausted.

        Args:
            results: Retrieval results to assemble.
            query: Original query string (included in the response).

        Returns:
            A :class:`RAGResponse` with results that fit within the budget.
        """
        sorted_results = sorted(results, key=lambda r: r.score, reverse=True)

        assembled: list[RetrievalResult] = []
        tokens_used = 0

        for result in sorted_results:
            result_tokens = self._estimate_tokens(result.content)
            if tokens_used + result_tokens > self._max_tokens:
                logger.debug(
                    "Token budget exhausted at %d/%d tokens, "
                    "dropping remaining %d results",
                    tokens_used,
                    self._max_tokens,
                    len(sorted_results) - len(assembled),
                )
                break
            assembled.append(result)
            tokens_used += result_tokens

        return RAGResponse(
            query=query or "",
            results=assembled,
            total_results=len(assembled),
            metadata={
                "max_tokens": self._max_tokens,
                "tokens_used": tokens_used,
                "results_considered": len(results),
                "results_included": len(assembled),
            },
        )
