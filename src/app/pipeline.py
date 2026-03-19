# pipeline.py
"""Pipeline orchestration.

Wires together Validator → Processor → ResultFormatter.
Each component owns its errors (raises RuntimeError).
The pipeline propagates them to FastAPI, which converts them to HTTP 500.

To swap the AI client: pass a different ServiceClient implementation
to Pipeline(client=...) in main.py.
"""

import logging
import time

from app.core.models import PipelineResult
from app.core.validator import Validator
from app.services.client import DummyClient, ServiceClient
from app.services.processor import Processor

logger = logging.getLogger(__name__)

_PROCESS_STEP = "0_pipeline"


class Pipeline:
    """Three-step request orchestration: validate → process → format.

    Args:
        client: AI client satisfying the ServiceClient Protocol.
                Defaults to DummyClient for local development.
    """

    def __init__(self, client: ServiceClient | None = None) -> None:
        effective_client: ServiceClient = client or DummyClient()
        logger.info("Initialising pipeline components...")
        self._validator = Validator()
        self._processor = Processor(client=effective_client)
        logger.info("Pipeline ready", extra={"process_step": _PROCESS_STEP})

    def process(self, query: str) -> PipelineResult:
        """Run a raw query through the full pipeline.

        Args:
            query: Raw user query string from the API.

        Returns:
            PipelineResult with answer, sources, and timing metadata.

        Raises:
            RuntimeError: Propagated from Validator or Processor on failure.
        """
        start = time.monotonic()

        validated = self._validator.validate(query)

        logger.info(
            "Pipeline started",
            extra={"process_step": _PROCESS_STEP, "request_id": validated.request_id},
        )

        processor_result = self._processor.process(validated)

        elapsed_ms = (time.monotonic() - start) * 1000

        result = PipelineResult(
            request_id=processor_result.request_id,
            query=validated.query,
            answer=processor_result.answer,
            sources=processor_result.sources_used,
            processing_time_ms=round(elapsed_ms, 2),
            metadata={
                "sources_count": len(processor_result.sources_used),
                "has_context": len(processor_result.sources_used) > 0,
            },
        )

        logger.info(
            "Pipeline completed",
            extra={
                "process_step": _PROCESS_STEP,
                "request_id": validated.request_id,
                "processing_time_ms": result.processing_time_ms,
            },
        )

        return result
