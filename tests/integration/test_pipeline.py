# test_pipeline.py
import pytest
from app.pipeline import Pipeline
from tests.conftest import FailingClient, MockClient

@pytest.fixture
def pipeline(mock_client: MockClient) -> Pipeline:
    return Pipeline(client=mock_client)

@pytest.mark.integration
def test_pipeline_returns_result_for_valid_query(pipeline: Pipeline) -> None:
    result = pipeline.process("What is the capital of France?")
    assert result.answer != ""

@pytest.mark.integration
def test_pipeline_result_contains_unique_request_id(pipeline: Pipeline) -> None:
    assert pipeline.process("First").request_id != pipeline.process("Second").request_id

@pytest.mark.integration
def test_pipeline_raises_runtime_error_for_query_too_short(pipeline: Pipeline) -> None:
    with pytest.raises(RuntimeError, match="too short"):
        pipeline.process("ab")

@pytest.mark.integration
def test_pipeline_raises_runtime_error_when_client_fails(failing_client: FailingClient) -> None:
    with pytest.raises(RuntimeError, match="Error in AI client response"):
        Pipeline(client=failing_client).process("This will fail")
