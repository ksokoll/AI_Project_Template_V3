# processor.py
"""Core processing logic."""

import logging

from app.core.models import ProcessorResult, ServiceRequest
from app.services.client import CompletionRequest, LLMClient
from app.services.retriever import RetrieverProtocol

logger = logging.getLogger(__name__)
_PROCESS_STEP = "2_processor"
_DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant."


class Processor:
    """Orchestrates prompt assembly, AI call, and response parsing.

    Receives LLMClient and RetrieverProtocol via constructor injection.
    Never instantiates AI clients or retrievers directly.

    Args:
        client: LLM client satisfying the LLMClient Protocol.
        retriever: Retriever satisfying the RetrieverProtocol.
            Defaults to None (no retrieval). Pass a real or stub
            retriever to enable RAG.
        system_prompt: System-level instructions for the model.
    """

    def __init__(
        self,
        client: LLMClient,
        retriever: RetrieverProtocol | None = None,
        system_prompt: str = _DEFAULT_SYSTEM_PROMPT,
    ) -> None:
        self._client = client
        self._retriever = retriever
        self._system_prompt = system_prompt

    def process(self, request: ServiceRequest) -> ProcessorResult:
        """Process a validated request through retrieval and generation.

        Args:
            request: Validated service request from the pipeline.

        Returns:
            ProcessorResult with answer and source documents used.

        Raises:
            RuntimeError: If the AI client call fails or returns empty.
        """
        context_docs = self._retrieve(request.query)
        user_prompt = self._build_prompt(request.query, context_docs)

        completion_request = CompletionRequest(
            system=self._system_prompt,
            user=user_prompt,
        )

        try:
            result = self._client.complete(completion_request)
        except Exception as exc:
            raise RuntimeError("Error in AI client response") from exc

        if not result.content or not result.content.strip():
            raise RuntimeError("AI client returned an empty response")

        return ProcessorResult(
            request_id=request.request_id,
            answer=result.content.strip(),
            sources_used=context_docs,
        )

    def _retrieve(self, query: str) -> list[str]:
        """Retrieve context documents if a retriever is configured.

        Args:
            query: Raw query string.

        Returns:
            List of context document strings, or empty list if no
            retriever is configured.
        """
        if self._retriever is None:
            return []
        return self._retriever.retrieve(query)

    @staticmethod
    def _build_prompt(query: str, context_docs: list[str]) -> str:
        """Assemble the user prompt from query and context.

        Args:
            query: Raw query string.
            context_docs: Retrieved document strings.

        Returns:
            Formatted user prompt string.
        """
        if not context_docs:
            return query
        context_block = "\n\n".join(context_docs)
        return (
            f"Context information:\n{context_block}\n\n"
            f"Question: {query}\n\n"
            "Answer based on the context above."
        )