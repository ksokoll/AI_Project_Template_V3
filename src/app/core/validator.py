# validator.py
"""Input validation and ULID generation."""
import logging
from ulid import ULID
from app.core.config import settings
from app.core.models import ServiceRequest

logger = logging.getLogger(__name__)
_PROCESS_STEP = "1_validation"

class Validator:
    def validate(self, query: str) -> ServiceRequest:
        try:
            request_id = str(ULID())
        except Exception as exc:
            raise RuntimeError("Failed to generate request_id") from exc
        query_clean = query.strip()
        if len(query_clean) < settings.min_query_length:
            raise RuntimeError(f"Query too short (minimum {settings.min_query_length} characters)")
        if len(query_clean) > settings.max_query_length:
            raise RuntimeError(f"Query too long (maximum {settings.max_query_length} characters)")
        logger.info("Validation completed", extra={"process_step": _PROCESS_STEP, "request_id": request_id})
        return ServiceRequest(request_id=request_id, query=query_clean)
