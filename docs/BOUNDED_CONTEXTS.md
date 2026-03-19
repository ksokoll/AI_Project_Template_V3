# Bounded Contexts

> What belongs where — and how to add new contexts as the project grows.

---

## Current Contexts

### `core/`
Shared infrastructure with no business logic. Nothing in `core/` should import from `services/` or `prompts/`.

- `config.py` — environment-driven settings (pydantic-settings)
- `models.py` — Pydantic schemas that define the contracts between pipeline stages
- `validator.py` — input sanitisation and ULID generation

### `services/`
Application logic: the AI call, retrieval, and orchestration.

- `client.py` — `ServiceClient` Protocol + `DummyClient` placeholder
- `processor.py` — prompt assembly, AI client call, response parsing
- `retriever.py` — optional RAG; replace `_score_documents()` for semantic search

### `prompts/` (optional)
Only relevant for LLM-based projects. Delete if not needed.

- `prompt_templates.py` — versioned `PromptTemplate` Pydantic model
- `prompts.py` — prompt library; import from `services/processor.py`

---

## Adding a New Context

When a concern grows beyond a few hundred lines, or when it has a meaningfully different dependency profile, extract it into a new bounded context under `src/app/`.

**Example: ML inference alongside LLM calls**

```
src/app/
  ml/
    __init__.py
    predictor.py    # loads model artifact, runs inference
    schemas.py      # Pydantic I/O schemas for the ML service
```

Rules for new contexts:
1. A context may import from `core/`. It must not import from another context directly — route through `pipeline.py` instead.
2. New contexts get their own section in `ARCHITECTURE.md` and at least one ADR in `docs/decisions/`.
3. Add `pytest` fixtures for the new context in `tests/conftest.py`.

---

## Dependency Rules (enforced by code review, not tooling)

```
core/         ← no internal imports
services/     ← may import from core/
prompts/      ← may import from core/
pipeline.py   ← may import from core/ and services/
main.py       ← may import from anywhere
```
