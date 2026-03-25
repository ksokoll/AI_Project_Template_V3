# retriever.py
"""Optional retrieval (RAG) component.

Only needed for RAG projects. If you are not building a retrieval-augmented
pipeline, delete this file and remove the retriever parameter from Processor.

RetrieverProtocol defines the contract. KeywordRetriever is a simple
keyword-matching implementation for local development. Replace
_score_documents() with a semantic search implementation (e.g. FAISS,
Pinecone, ChromaDB) when you need production-quality retrieval.
"""

import json
import logging
from typing import Protocol, runtime_checkable

from app.core.config import settings

logger = logging.getLogger(__name__)


# ── Protocol ──────────────────────────────────────────────────────────────────

@runtime_checkable
class RetrieverProtocol(Protocol):
    """Minimal interface every retriever implementation must satisfy.

    The pipeline depends on this Protocol, never on a concrete retriever.
    Swap implementations by passing a different retriever to Processor().
    """

    def retrieve(self, query: str) -> list[str]:
        """Return relevant documents for a query.

        Args:
            query: Raw query string from the user.

        Returns:
            List of document strings ordered by relevance.
            Returns an empty list if no documents are relevant.
        """
        ...


# ── KeywordRetriever ──────────────────────────────────────────────────────────

class KeywordRetriever:
    """Simple keyword-matching retriever for local development.

    Scores documents by counting shared words between query and document.
    Replace _score_documents() with a semantic search implementation for
    production use.

    Args:
        knowledge_base_path: Path to a JSONL file where each line is a
            JSON object with a "text" field. Defaults to
            settings.knowledge_base_path.
    """

    def __init__(self, knowledge_base_path: str | None = None) -> None:
        self._kb_path = knowledge_base_path or settings.knowledge_base_path
        self._knowledge_base: list[dict[str, str]] = []
        if settings.enable_retrieval:
            self._knowledge_base = self._load_knowledge_base()

    def retrieve(self, query: str) -> list[str]:
        """Return top-k relevant documents for a query.

        Args:
            query: Raw query string.

        Returns:
            List of document strings ordered by descending keyword overlap.
            Returns an empty list if retrieval is disabled or no documents
            match.
        """
        if not settings.enable_retrieval or not self._knowledge_base:
            return []
        return self._score_documents(query)

    def _score_documents(self, query: str) -> list[str]:
        """Score documents by keyword overlap with the query.

        Replace this method with a semantic search implementation
        (FAISS, Pinecone, etc.) for production use.

        Args:
            query: Raw query string.

        Returns:
            Top-k document strings ordered by descending overlap score.
        """
        query_words = set(query.lower().split())
        scored = [
            (len(query_words & set(doc.get("text", "").lower().split())), doc.get("text", ""))
            for doc in self._knowledge_base
        ]
        scored = [(score, text) for score, text in scored if score > 0]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [text for _, text in scored[: settings.retrieval_top_k]]

    def _load_knowledge_base(self) -> list[dict[str, str]]:
        """Load knowledge base from JSONL file.

        Returns:
            List of document dicts. Returns empty list if file not found.
        """
        try:
            with open(self._kb_path, encoding="utf-8") as fh:
                return [json.loads(line.strip()) for line in fh if line.strip()]
        except FileNotFoundError:
            logger.warning("Knowledge base file not found at %s", self._kb_path)
            return []