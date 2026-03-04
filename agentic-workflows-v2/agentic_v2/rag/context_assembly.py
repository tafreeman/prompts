"""RAG context assembly — token-budget-aware result assembler.

Provides:
- :class:`TokenBudgetAssembler`: Greedily assembles retrieval results into a
  :class:`RAGResponse` within a configurable token budget.
- :func:`frame_content`: Wraps retrieved content in delimiter tags for
  prompt injection defense.

Security note:
    Retrieved documents may contain adversarial content designed to hijack
    LLM behavior ("Ignore all previous instructions...").  The delimiter
    framing wraps each chunk in ``<retrieved_context>`` tags, signaling to
    the LLM that the content is **untrusted user-provided data** and should
    not be interpreted as instructions.
"""

from __future__ import annotations

import logging
from typing import Callable

from .contracts import RAGResponse, RetrievalResult

logger = logging.getLogger(__name__)

# Delimiter tags for prompt injection defense.  The LLM system prompt
# should instruct the model to treat content within these tags as
# untrusted retrieved data, never as instructions.
CONTEXT_DELIMITER_START = "<retrieved_context>"
CONTEXT_DELIMITER_END = "</retrieved_context>"

# Overhead tokens per framed chunk (delimiters + newlines).
# Used to account for framing cost in the token budget.
_FRAMING_OVERHEAD_CHARS = (
    len(CONTEXT_DELIMITER_START) + len(CONTEXT_DELIMITER_END) + 2  # newlines
)


def frame_content(content: str) -> str:
    """Wrap retrieved content in delimiter tags for prompt injection defense.

    Args:
        content: Raw retrieved chunk content.

    Returns:
        Content wrapped in ``<retrieved_context>`` delimiters.
    """
    return f"{CONTEXT_DELIMITER_START}\n{content}\n{CONTEXT_DELIMITER_END}"


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

    When ``frame_results`` is enabled (default), each result's content is
    wrapped in ``<retrieved_context>`` delimiters for prompt injection
    defense.  The token budget accounts for the framing overhead.

    Args:
        max_tokens: Maximum token budget for assembled context.
        token_estimator: Callable that estimates tokens for a given text.
            Defaults to ``len(text) // 4``.
        frame_results: Whether to wrap results in injection-defense
            delimiters.  Defaults to ``True``.
    """

    def __init__(
        self,
        *,
        max_tokens: int = 4000,
        token_estimator: Callable[[str], int] | None = None,
        frame_results: bool = True,
    ) -> None:
        self._max_tokens = max_tokens
        self._estimate_tokens = token_estimator or _default_token_estimator
        self._frame_results = frame_results

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

        framing_overhead = (
            self._estimate_tokens("x" * _FRAMING_OVERHEAD_CHARS)
            if self._frame_results
            else 0
        )

        for result in sorted_results:
            result_tokens = (
                self._estimate_tokens(result.content) + framing_overhead
            )
            if tokens_used + result_tokens > self._max_tokens:
                logger.debug(
                    "Token budget exhausted at %d/%d tokens, "
                    "dropping remaining %d results",
                    tokens_used,
                    self._max_tokens,
                    len(sorted_results) - len(assembled),
                )
                break

            if self._frame_results:
                framed = RetrievalResult(
                    content=frame_content(result.content),
                    score=result.score,
                    document_id=result.document_id,
                    chunk_id=result.chunk_id,
                    metadata=result.metadata,
                )
                assembled.append(framed)
            else:
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
                "framing_enabled": self._frame_results,
            },
        )
