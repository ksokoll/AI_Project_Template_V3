# config.py
"""Central configuration via pydantic-settings."""
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration."""
    app_name: str = Field(default="AI Service")
    app_version: str = Field(default="0.1.0")
    # openai_api_key: str | None = Field(default=None, env="OPENAI_API_KEY")
    # anthropic_api_key: str | None = Field(default=None, env="ANTHROPIC_API_KEY")
    min_query_length: int = Field(default=3)
    max_query_length: int = Field(default=2000)
    enable_retrieval: bool = Field(default=False)
    knowledge_base_path: str = Field(default="data/knowledge_base.jsonl")
    retrieval_top_k: int = Field(default=3)
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }

settings = Settings()
