# test_processor.py
import pytest
from app.core.models import ServiceRequest
from app.services.processor import Processor
from tests.conftest import FailingClient, MockClient

@pytest.fixture
def sample_request() -> ServiceRequest:
    return ServiceRequest(request_id="01TEST00000000000000000000", query="What is Python?")

@pytest.fixture
def processor(mock_client: MockClient) -> Processor:
    return Processor(client=mock_client)

@pytest.mark.unit
def test_processor_returns_result_with_correct_request_id(processor: Processor, sample_request: ServiceRequest) -> None:
    assert processor.process(sample_request).request_id == sample_request.request_id

@pytest.mark.unit
def test_processor_returns_non_empty_answer(processor: Processor, sample_request: ServiceRequest) -> None:
    assert processor.process(sample_request).answer != ""

@pytest.mark.unit
def test_processor_returns_empty_sources_when_retrieval_disabled(processor: Processor, sample_request: ServiceRequest) -> None:
    assert processor.process(sample_request).sources_used == []

@pytest.mark.unit
def test_processor_raises_runtime_error_when_client_fails(failing_client: FailingClient, sample_request: ServiceRequest) -> None:
    with pytest.raises(RuntimeError, match="Error in AI client response"):
        Processor(client=failing_client).process(sample_request)
