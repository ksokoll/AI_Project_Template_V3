# retriever.py
"""Optional retrieval (RAG) component."""
import json, logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class Retriever:
    def __init__(self) -> None:
        self._knowledge_base: list[dict[str, str]] = []
        if settings.enable_retrieval:
            self._knowledge_base = self._load_knowledge_base()

    def retrieve(self, query: str) -> list[str]:
        if not settings.enable_retrieval or not self._knowledge_base:
            return []
        query_words = set(query.lower().split())
        scored = [(len(query_words & set(d.get("text","").lower().split())), d.get("text",""))
                  for d in self._knowledge_base]
        scored = [(s, t) for s, t in scored if s > 0]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [t for _, t in scored[:settings.retrieval_top_k]]

    def _load_knowledge_base(self) -> list[dict[str, str]]:
        try:
            with open(settings.knowledge_base_path, encoding="utf-8") as fh:
                return [json.loads(line.strip()) for line in fh]
        except FileNotFoundError:
            logger.warning("Knowledge base file not found")
            return []
