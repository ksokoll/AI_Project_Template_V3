# prompts.py
"""Versioned prompt library. OPTIONAL."""
from datetime import datetime
from app.prompts.prompt_templates import PromptTemplate

SYSTEM_PROMPT = PromptTemplate(
    name="system", version="1.0.0",
    prompt="You are a helpful AI assistant. Answer concisely and accurately.",
    last_modified=datetime(2026, 1, 1), tested_models=["gpt-4o-mini"],
    author="TODO", description="General-purpose assistant prompt",
)
