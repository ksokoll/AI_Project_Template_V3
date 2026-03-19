# processor.py
"""Core processing logic."""
import logging
from app.core.models import ProcessorResult, ServiceRequest
from app.services.client import ServiceClient
from app.services.retriever import Retriever

logger = logging.getLogger(__name__)
_PROCESS_STEP = "2_processor"
_DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant."

class Processor:
    def __init__(self, client: ServiceClient, system_prompt: str = _DEFAULT_SYSTEM_PROMPT) -> None:
        self._client = client
        self._system_prompt = system_prompt
        self._retriever = Retriever()

    def process(self, request: ServiceRequest) -> ProcessorResult:
        context_docs = self._retriever.retrieve(request.query)
        user_prompt = self._build_prompt(request.query, context_docs)
        try:
            answer = self._client.complete(system=self._system_prompt, user=user_prompt)
        except Exception as exc:
            raise RuntimeError("Error in AI client response") from exc
        if not answer or not answer.strip():
            raise RuntimeError("AI client returned an empty response")
        return ProcessorResult(request_id=request.request_id, answer=answer.strip(), sources_used=context_docs)

    def _build_prompt(self, query: str, context_docs: list[str]) -> str:
        if not context_docs:
            return query
        context_block = "\n\n".join(context_docs)
        return f"Context information:\n{context_block}\n\nQuestion: {query}\n\nAnswer based on the context above."
