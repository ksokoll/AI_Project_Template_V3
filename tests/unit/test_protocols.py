# tests/unit/test_protocols.py
"""Fitness functions: verify that all client implementations satisfy their Protocols.

These tests are architecture guards. If a client implementation drifts
from the Protocol signature, these fail immediately — not at serving time.

Add a test here for every new client implementation you add to services/client.py.
"""

import pytest

from app.services.client import (
    CompletionRequest,
    DummyLLMClient,
    EmbeddingClient,
    LLMClient,
    DummyEmbeddingClient,
)
from tests.conftest import EmptyLLMClient, FailingLLMClient, StubLLMClient


@pytest.mark.unit
class TestLLMClientProtocol:
    def test_dummy_llm_client_satisfies_protocol(self) -> None:
        assert isinstance(DummyLLMClient(), LLMClient)

    def test_stub_llm_client_satisfies_protocol(self) -> None:
        assert isinstance(StubLLMClient(), LLMClient)

    def test_empty_llm_client_satisfies_protocol(self) -> None:
        assert isinstance(EmptyLLMClient(), LLMClient)

    def test_failing_llm_client_satisfies_protocol(self) -> None:
        assert isinstance(FailingLLMClient(), LLMClient)

    def test_dummy_llm_client_returns_completion_result(self) -> None:
        client = DummyLLMClient()
        result = client.complete(CompletionRequest(system="sys", user="hello"))
        assert result.content
        assert result.tokens_used == 0

    def test_dummy_llm_client_echoes_user_message(self) -> None:
        client = DummyLLMClient()
        result = client.complete(CompletionRequest(system="sys", user="test query"))
        assert "test query" in result.content


@pytest.mark.unit
class TestEmbeddingClientProtocol:
    def test_dummy_embedding_client_satisfies_protocol(self) -> None:
        assert isinstance(DummyEmbeddingClient(), EmbeddingClient)

    def test_dummy_embedding_client_returns_one_vector_per_input(self) -> None:
        client = DummyEmbeddingClient()
        result = client.embed(["foo", "bar", "baz"])
        assert len(result) == 3

    def test_dummy_embedding_client_vector_has_correct_dimensions(self) -> None:
        client = DummyEmbeddingClient()
        result = client.embed(["foo"])
        assert len(result[0]) == 1536

    def test_dummy_embedding_client_returns_zero_vectors(self) -> None:
        client = DummyEmbeddingClient()
        result = client.embed(["foo"])
        assert all(v == 0.0 for v in result[0])