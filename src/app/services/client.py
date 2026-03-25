# services/client.py
"""AI client abstractions.

Defines two Protocols that all AI client implementations must satisfy:
- LLMClient: text generation via structured CompletionRequest/CompletionResult
- EmbeddingClient: vector embedding generation (only needed for RAG projects)

These are kept separate because their signatures and consumers differ.
Collapsing them into one Protocol would be a forced abstraction.

All pipeline components depend on these Protocols, never on a concrete
client. Swapping providers requires only a new implementation here.

Implementations to add per project:
    - OpenAILLMClient: wrap openai.OpenAI chat completions
    - AnthropicLLMClient: wrap anthropic.Anthropic messages
    - OpenAIEmbeddingClient: wrap openai.OpenAI embeddings (RAG only)
    - LocalLLMClient: wrap a local model (e.g. Ollama, llama.cpp)
"""

from typing import Any, Protocol, runtime_checkable

from pydantic import BaseModel, Field


# ── Request / Result types ────────────────────────────────────────────────────

class CompletionRequest(BaseModel):
    """Parameters for a single LLM completion call.

    Carries all call-site-specific overrides so that LLMClient.complete()
    has a stable, typed signature without **kwargs catch-alls.

    Add fields here as your project requires (e.g. stop_sequences, stream).
    Keep the interface as narrow as possible — only what consumers need.
    """

    system: str
    user: str
    temperature: float = Field(default=0.3)
    response_format: dict[str, Any] | None = Field(default=None)
    max_tokens: int = Field(default=500)


class CompletionResult(BaseModel):
    """Result of a single LLM completion call."""

    content: str
    tokens_used: int = 0


# ── Protocols ─────────────────────────────────────────────────────────────────

@runtime_checkable
class LLMClient(Protocol):
    """Minimal interface every text-generation client must satisfy.

    Used by all components that make LLM calls (processor, classifier,
    judge, etc.). Extend CompletionRequest if you need additional
    parameters — do not change this signature.
    """

    def complete(self, request: CompletionRequest) -> CompletionResult:
        """Generate a completion for the given prompt pair.

        Args:
            request: Typed completion parameters including system prompt,
                user message, temperature, response format, and token limit.

        Returns:
            CompletionResult with the model response and token usage.

        Raises:
            RuntimeError: If the underlying API call fails.
        """
        ...


@runtime_checkable
class EmbeddingClient(Protocol):
    """Minimal interface every embedding client must satisfy.

    Only needed for RAG projects. Delete if you are not building
    a retrieval-augmented pipeline.
    """

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embedding vectors for a list of texts.

        Args:
            texts: List of strings to embed. Must not be empty.

        Returns:
            List of float vectors, one per input text.
            Vector dimensionality is model-dependent.

        Raises:
            RuntimeError: If the underlying API call fails.
        """
        ...


# ── Dummy implementations (local dev + unit tests) ────────────────────────────

class DummyLLMClient:
    """Deterministic LLM client for local development and unit tests.

    Returns a static response without any external calls.
    Replace with a real implementation before deploying.
    """

    def complete(self, request: CompletionRequest) -> CompletionResult:
        """Return a static placeholder response.

        Args:
            request: Ignored except for echoing the first 80 chars of user.

        Returns:
            CompletionResult with placeholder content and zero token usage.
        """
        return CompletionResult(
            content=f"[DummyLLMClient] Received: {request.user[:80]}",
            tokens_used=0,
        )


class DummyEmbeddingClient:
    """Deterministic embedding client for local development and unit tests.

    Returns zero-vectors without any external calls. Only needed for RAG
    projects — delete if you are not building a retrieval pipeline.
    """

    _DIMENSIONS: int = 1536  # matches text-embedding-3-small output size

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Return a list of zero-vectors matching input length.

        Args:
            texts: List of strings to embed.

        Returns:
            List of zero-vectors, one per input text.
        """
        return [[0.0] * self._DIMENSIONS for _ in texts]