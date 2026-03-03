"""RAG vector store implementations — in-memory store for testing/dev.

Provides:
- :class:`InMemoryVectorStore`: Pure-Python cosine similarity vector store.

.. note::
    A LanceDB-backed vector store (``LanceDBVectorStore``) would be added
    here when the ``lancedb`` optional dependency is installed.  That
    implementation is deferred to a later sprint.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from typing import Sequence

from .contracts import Chunk, RetrievalResult

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class _StoredEntry:
    """Internal storage record pairing a chunk with its embedding."""

    chunk: Chunk
    embedding: tuple[float, ...]


class InMemoryVectorStore:
    """Pure-Python in-memory vector store using cosine similarity.

    Stores chunks and their embeddings in a dict keyed by chunk_id.
    Searches compute cosine similarity against all stored embeddings
    and return the top-k matches.

    Suitable for testing and small-scale development.  Not suitable
    for production workloads.

    Satisfies :class:`VectorStoreProtocol`.
    """

    def __init__(self) -> None:
        self._entries: dict[str, _StoredEntry] = {}
        self._expected_dimensions: int | None = None

    async def add(
        self, chunks: list[Chunk], embeddings: list[list[float]]
    ) -> None:
        """Add chunks with their embeddings to the store.

        Args:
            chunks: Chunks to store.
            embeddings: Corresponding embedding vectors (one per chunk).

        Raises:
            ValueError: If *chunks* and *embeddings* have different lengths.
        """
        if len(chunks) != len(embeddings):
            raise ValueError(
                f"chunks and embeddings must have the same length, "
                f"got {len(chunks)} chunks and {len(embeddings)} embeddings"
            )
        for chunk, embedding in zip(chunks, embeddings):
            if self._expected_dimensions is None and embedding:
                self._expected_dimensions = len(embedding)
            if self._expected_dimensions is not None and len(embedding) != self._expected_dimensions:
                raise ValueError(
                    f"Embedding dimension mismatch: expected "
                    f"{self._expected_dimensions}, got {len(embedding)} "
                    f"for chunk {chunk.chunk_id}"
                )
            self._entries[chunk.chunk_id] = _StoredEntry(
                chunk=chunk,
                embedding=tuple(embedding),
            )

    async def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        **kwargs: object,
    ) -> list[RetrievalResult]:
        """Search for similar chunks using cosine similarity.

        Args:
            query_embedding: The query vector.
            top_k: Maximum number of results to return.

        Returns:
            Ranked list of :class:`RetrievalResult`, highest score first.
        """
        if not self._entries:
            return []

        # Snapshot to avoid RuntimeError if entries mutate during iteration
        entries_snapshot = list(self._entries.values())

        scored: list[tuple[float, _StoredEntry]] = []
        for entry in entries_snapshot:
            similarity = _cosine_similarity(query_embedding, entry.embedding)
            # Clamp to [0.0, 1.0] — negative cosine means opposing vectors
            score = max(0.0, similarity)
            scored.append((score, entry))

        # Sort descending by score
        scored.sort(key=lambda pair: pair[0], reverse=True)

        results: list[RetrievalResult] = []
        for score, entry in scored[:top_k]:
            results.append(
                RetrievalResult(
                    content=entry.chunk.content,
                    score=score,
                    document_id=entry.chunk.document_id,
                    chunk_id=entry.chunk.chunk_id,
                    metadata=dict(entry.chunk.metadata),
                )
            )
        return results

    async def delete(self, document_id: str) -> bool:
        """Delete all chunks for a document.

        Args:
            document_id: The document whose chunks should be removed.

        Returns:
            True if any chunks were deleted, False otherwise.
        """
        to_remove = [
            chunk_id
            for chunk_id, entry in self._entries.items()
            if entry.chunk.document_id == document_id
        ]
        if not to_remove:
            return False
        for chunk_id in to_remove:
            del self._entries[chunk_id]
        logger.info(
            "Deleted %d chunks for document_id=%s", len(to_remove), document_id,
        )
        return True


def _cosine_similarity(vec_a: Sequence[float], vec_b: Sequence[float]) -> float:
    """Compute cosine similarity between two vectors.

    Returns a value in [-1.0, 1.0].  Returns 0.0 if either vector
    has zero magnitude.

    Raises:
        ValueError: If vectors have different dimensions.
    """
    if len(vec_a) != len(vec_b):
        raise ValueError(
            f"Vector dimension mismatch: {len(vec_a)} vs {len(vec_b)}"
        )
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)
