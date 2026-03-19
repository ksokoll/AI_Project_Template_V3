# main.py
"""FastAPI application entry point."""
import logging
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.core.config import settings
from app.pipeline import Pipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name, version=settings.app_version)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class QueryRequest(BaseModel):
    query: str

_pipeline_instance: Pipeline | None = None

def get_pipeline() -> Pipeline:
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = Pipeline()
    return _pipeline_instance

@app.get("/")
async def root() -> dict[str, str]:
    return {"status": "running", "service": settings.app_name}

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy"}

@app.post("/process")
async def process_query(request: QueryRequest, pipeline: Pipeline = Depends(get_pipeline)) -> dict[str, object]:
    result = pipeline.process(request.query)
    return result.model_dump()

@app.on_event("startup")
async def startup_event() -> None:
    logger.info("Starting %s v%s", settings.app_name, settings.app_version)
    get_pipeline()
