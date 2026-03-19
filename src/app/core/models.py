# models.py
"""Pydantic schemas for pipeline I/O."""
from pydantic import BaseModel, Field, field_validator

class ServiceRequest(BaseModel):
    request_id: str
    query: str

    @field_validator("query")
    @classmethod
    def query_must_not_be_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Query cannot be empty")
        return value.strip()

class ProcessorResult(BaseModel):
    request_id: str
    answer: str
    sources_used: list[str] = Field(default_factory=list)

class PipelineResult(BaseModel):
    request_id: str
    query: str
    answer: str
    sources: list[str] = Field(default_factory=list)
    processing_time_ms: float = 0.0
    metadata: dict[str, object] = Field(default_factory=dict)
