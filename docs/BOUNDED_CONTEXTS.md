# Bounded Contexts

> What belongs where — and how to add new contexts as the project grows.

---

## Current Contexts

### `core/`
Shared infrastructure with no business logic. Nothing in `core/` should import
from `services/` or `prompts/`.

- `config.py` — environment-driven settings (pydantic-settings v2)
- `models.py` — `ServiceRequest` (entry contract) and `PipelineResult`
  (exit contract). Context-local result types live in their own context.
- `validator.py` — input sanitisation and ULID generation
- `exceptions.py` — domain exception classes, one per bounded context.
  Lives in `core/` because `pipeline.py` is the single consumer of all
  exceptions and must not import from individual contexts just for error types.

### `services/`
Application logic: the AI call, retrieval, and orchestration.

- `client.py` — `LLMClient` and `EmbeddingClient` Protocols with
  `CompletionRequest`/`CompletionResult` types. `DummyLLMClient` and
  `DummyEmbeddingClient` for local dev and tests.
  `EmbeddingClient` is only needed for RAG projects — delete if not required.
- `processor.py` — prompt assembly, AI client call, response parsing.
  Receives `LLMClient` and `RetrieverProtocol` via constructor injection.
  Never instantiates clients or retrievers directly.
- `retriever.py` — optional RAG; `RetrieverProtocol` definition and
  `KeywordRetriever` as a keyword-matching placeholder. Replace
  `_score_documents()` with a semantic search implementation for production.
  Delete if not building a RAG pipeline.

### `prompts/` (optional)
Only relevant for LLM-based projects. Delete if not needed.

- `prompt_templates.py` — versioned `PromptTemplate` Pydantic model
- `prompts.py` — prompt library; import from `services/processor.py`

---

## Adding a New Context

When a concern grows beyond a few hundred lines, or when it has a meaningfully
different dependency profile, extract it into a new bounded context under
`src/app/`.

**Example: ML inference alongside LLM calls**

```
src/app/
  ml/
    __init__.py
    predictor.py    # loads model artifact, runs inference
    schemas.py      # Pydantic I/O schemas for the ML service
```

Rules for new contexts:
1. A context may import from `core/`. It must not import from another context
   directly — route through `pipeline.py` instead.
2. Register the context's domain exception in `core/exceptions.py`, not
   locally in the context module.
3. New contexts get their own section in `ARCHITECTURE.md` and at least one
   ADR in `docs/decisions/`.
4. Add pytest fixtures for the new context in `tests/conftest.py`.
5. `LLMClient` and `EmbeddingClient` are the only approved ways to call any
   AI provider. New contexts must not introduce direct API client imports.

---

## Error Handling Strategy

Each bounded context raises its own domain exception on failure.
`pipeline.py` is the single place that catches them and applies the fallback
strategy. Define the strategy explicitly per context before writing code:

| Failure point | Recommended strategy |
|---|---|
| Validation | Re-raise as `ValueError` → HTTP 422 |
| Retrieval | Continue with empty context, flag in metadata |
| Generation | Re-raise → HTTP 500 (nothing to return) |
| Quality check | Fail safe: escalate to human review, return answer |

---

## Fitness Functions

Automated checks that verify architectural characteristics:

| Check | Type | Enforces |
|---|---|---|
| `DummyLLMClient` satisfies `LLMClient` Protocol | Unit | Protocol contract |
| `StubLLMClient` satisfies `LLMClient` Protocol | Unit | Protocol contract |
| `DummyEmbeddingClient` satisfies `EmbeddingClient` Protocol | Unit | Protocol contract |
| Real client implementations satisfy their Protocols | Unit | Production client contract |
| Docker container starts with all required env vars | Smoke | Deployment readiness |

Add a fitness function test for every new client implementation.

---

## Dependency Rules

```
core/         ← no internal imports
services/     ← may import from core/
prompts/      ← may import from core/
pipeline.py   ← may import from core/ and services/
main.py       ← may import from anywhere
```