# services/client.py
"""Service client abstraction.

Defines the Protocol that all AI/LLM clients must implement.
Swap out the implementation in config.py or via dependency injection —
the pipeline never imports a concrete client directly.

Implementations to add per project:
    - OpenAIClient: wrap openai.OpenAI
    - AnthropicClient: wrap anthropic.Anthropic
    - LocalClient: wrap a local model (e.g. Ollama, llama.cpp)
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class ServiceClient(Protocol):
    """Minimal interface every AI/LLM client must satisfy.

    Add methods here as your project requires (e.g. embed(), stream()).
    Keep the interface as narrow as possible — only what the processor needs.
    """

    def complete(self, system: str, user: str) -> str:
        """Generate a completion for the given prompt pair.

        Args:
            system: System-level instructions for the model.
            user: The user-facing query or task.

        Returns:
            Model response as a plain string.

        Raises:
            RuntimeError: If the underlying API call fails.
        """
        ...


# ── Dummy implementation (replace with your real client) ──────────────────────

class DummyClient:
    """Placeholder client for local development and unit tests.

    Returns a deterministic string without any external calls.
    Replace this with a real implementation before deploying.
    """

    def complete(self, system: str, user: str) -> str:  # noqa: ARG002
        """Return a static placeholder response.

        Args:
            system: Ignored in dummy mode.
            user: Echoed back in the response.

        Returns:
            Placeholder string indicating dummy mode is active.
        """
        return f"[DummyClient] Received: {user[:80]}"
