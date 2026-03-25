# tests/conftest.py
"""Shared pytest fixtures and stubs.

Stubs here are available to all test levels.
Import in test files via pytest fixture injection or direct import.
"""

import pytest

from app.services.client import CompletionRequest, CompletionResult, LLMClient


# ── Reusable LLM stubs ────────────────────────────────────────────────────────

class StubLLMClient:
    """Configurable stub returning a preset response.

    Args:
        content: String returned as completion content.
        tokens_used: Token count to report in CompletionResult.
    """

    def __init__(self, content: str = "[StubLLMClient] default response", tokens_used: int = 10) -> None:
        self._content = content
        self._tokens_used = tokens_used

    def complete(self, request: CompletionRequest) -> CompletionResult:
        return CompletionResult(content=self._content, tokens_used=self._tokens_used)


class EmptyLLMClient:
    """Stub returning an empty string."""

    def complete(self, request: CompletionRequest) -> CompletionResult:
        return CompletionResult(content="", tokens_used=0)


class FailingLLMClient:
    """Stub that always raises RuntimeError."""

    def complete(self, request: CompletionRequest) -> CompletionResult:
        raise RuntimeError("Simulated provider failure")


# ── Protocol assertions ───────────────────────────────────────────────────────

# Verify stubs satisfy the Protocol at import time.
# If a stub drifts from the Protocol signature, this fails at collection,
# not at serving time.
assert isinstance(StubLLMClient(), LLMClient)
assert isinstance(EmptyLLMClient(), LLMClient)
assert isinstance(FailingLLMClient(), LLMClient)


# ── Pytest fixtures ───────────────────────────────────────────────────────────

@pytest.fixture()
def stub_llm_client() -> StubLLMClient:
    """Return a deterministic StubLLMClient instance."""
    return StubLLMClient()


@pytest.fixture()
def failing_llm_client() -> FailingLLMClient:
    """Return a client that always raises RuntimeError."""
    return FailingLLMClient()