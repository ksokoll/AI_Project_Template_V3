# tests/conftest.py
"""Shared pytest fixtures.

MockClient satisfies the ServiceClient Protocol and returns deterministic
responses — no real API calls in unit or integration tests.
"""

import pytest

from app.services.client import ServiceClient


class MockClient:
    """Test double for ServiceClient.

    Returns a fixed response so tests are deterministic and free.
    Conforms to the ServiceClient Protocol without inheriting from it.
    """

    FIXED_RESPONSE = "Mock answer for testing."

    def complete(self, system: str, user: str) -> str:  # noqa: ARG002
        """Return a fixed response regardless of input.

        Args:
            system: Ignored.
            user: Ignored.

        Returns:
            Fixed test response string.
        """
        return self.FIXED_RESPONSE


class FailingClient:
    """Test double that always raises — for error-path tests."""

    def complete(self, system: str, user: str) -> str:  # noqa: ARG002
        """Raise unconditionally to simulate provider failure.

        Args:
            system: Ignored.
            user: Ignored.

        Raises:
            RuntimeError: Always.
        """
        raise RuntimeError("Simulated provider failure")


@pytest.fixture
def mock_client() -> MockClient:
    """Return a deterministic MockClient instance."""
    return MockClient()


@pytest.fixture
def failing_client() -> FailingClient:
    """Return a client that always raises RuntimeError."""
    return FailingClient()


# Verify MockClient satisfies the Protocol at import time
assert isinstance(MockClient(), ServiceClient)
assert isinstance(FailingClient(), ServiceClient)
