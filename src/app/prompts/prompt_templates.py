# prompt_templates.py
"""Pydantic model for versioned prompt definitions. OPTIONAL."""
from datetime import datetime
from pydantic import BaseModel

class PromptTemplate(BaseModel):
    name: str
    version: str
    prompt: str
    last_modified: datetime
    tested_models: list[str]
    author: str = "Unknown"
    description: str = ""
