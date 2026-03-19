# test_validator.py
import pytest
from app.core.validator import Validator

@pytest.fixture
def validator() -> Validator:
    return Validator()

@pytest.mark.unit
def test_validator_returns_service_request_for_valid_query(validator: Validator) -> None:
    result = validator.validate("What is the weather today?")
    assert result.query == "What is the weather today?"

@pytest.mark.unit
def test_validator_strips_leading_and_trailing_whitespace(validator: Validator) -> None:
    assert validator.validate("  hello  ").query == "hello"

@pytest.mark.unit
def test_validator_generates_unique_request_ids_per_call(validator: Validator) -> None:
    assert validator.validate("q1").request_id != validator.validate("q2").request_id

@pytest.mark.unit
def test_validator_rejects_query_below_minimum_length(validator: Validator) -> None:
    with pytest.raises(RuntimeError, match="too short"):
        validator.validate("ab")

@pytest.mark.unit
def test_validator_rejects_empty_string(validator: Validator) -> None:
    with pytest.raises(RuntimeError, match="too short"):
        validator.validate("")

@pytest.mark.unit
def test_validator_rejects_whitespace_only_string(validator: Validator) -> None:
    with pytest.raises(RuntimeError, match="too short"):
        validator.validate("   ")

@pytest.mark.unit
def test_validator_rejects_query_above_maximum_length(validator: Validator) -> None:
    with pytest.raises(RuntimeError, match="too long"):
        validator.validate("x" * 2001)
