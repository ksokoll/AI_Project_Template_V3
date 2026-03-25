# AI Project Template V3

A minimal, production-oriented starting point for AI/ML services.

Clone, rename the package, wire in your provider, and start building without the boilerplate overhead.

---

## What's Included

```
src/app/
  core/          Config, Pydantic schemas, input validation, domain exceptions
  services/      LLMClient + EmbeddingClient Protocols, CompletionRequest/Result,
                 Processor (injected), optional RetrieverProtocol + KeywordRetriever (RAG)
  prompts/       Versioned prompt library (optional — delete if not LLM-based)
  pipeline.py    Orchestration
  main.py        FastAPI entry point

tests/
  unit/          Behaviour-named unit tests, no I/O
    test_protocols.py   Fitness functions for all Protocol contracts
  integration/   Full pipeline with StubLLMClient, no real API calls
  conftest.py    Shared stubs: StubLLMClient, EmptyLLMClient, FailingLLMClient

docs/
  ARCHITECTURE.md
  BOUNDED_CONTEXTS.md   Boundary rules, error handling strategy, fitness functions
  DEVLOG.md
  decisions/ADR_TEMPLATE.md

.dockerignore
.github/workflows/ci.yml
.pre-commit-config.yaml
Makefile        lint · format · test · test-unit · test-integration · docker-build · run
pyproject.toml  Single source of truth for deps, ruff, mypy, pytest, coverage
Dockerfile      Multi-stage, non-root user
```

---

## Quickstart

```bash
# 1. Clone and rename
git clone https://github.com/ksokoll/AI_Project_Template_V3
cd AI_Project_Template_V3

# 2. Install (choose your provider extra)
pip install -e ".[dev]"         # dev tools only
pip install -e ".[dev,openai]"  # + OpenAI client
pip install -e ".[dev,anthropic]"  # + Anthropic client

# 3. Configure
cp .env.example .env
# Fill in your API key in .env

# 4. Implement your client (services/client.py)
# Replace DummyClient with OpenAIClient or AnthropicClient

# 5. Run
uvicorn app.main:app --reload
# or
make run
```

API docs: http://localhost:8000/docs

---

## Development Workflow

```bash
make format          # ruff format + fix
make lint            # ruff check + mypy
make test            # all tests with coverage
make test-unit       # fast, no I/O
make test-integration
make docker-build
```

Set up pre-commit hooks (recommended):

```bash
pip install pre-commit
pre-commit install
```

---

## Adapting the Template

**Rename the package:** Replace every occurrence of `app` with your package name
in `pyproject.toml`, `src/`, `Dockerfile`, and `main.py`.

**Add your AI provider:** Implement `ServiceClient` in `services/client.py`,
inject it into `Pipeline(client=YourClient())` in `main.py`.

**Enable RAG:** Set `ENABLE_RETRIEVAL=true` in `.env` and point
`KNOWLEDGE_BASE_PATH` to your JSONL file.

**Add a new bounded context:** See `docs/BOUNDED_CONTEXTS.md`.

**Not building an LLM app?** Delete `src/app/prompts/` and the
`_DEFAULT_SYSTEM_PROMPT` constant in `processor.py`.

---

## Project Conventions

**Commit messages:** `<verb> <what> to <why>` — e.g.
`Extract retrieval logic into Retriever to enable unit testing`
Not: `Refactor processor`

**Tests:** Name tests after behaviours, not methods:
`test_validator_rejects_query_below_minimum_length`
Not: `test_validate`

**Docs:** Update `docs/DEVLOG.md` each session. Add an ADR to
`docs/decisions/` for every significant architectural decision.

---

## What This Template Intentionally Excludes

- Terraform / cloud infrastructure (too provider-specific)
- MLflow / experiment tracking (belongs in the concrete project)
- Database integration (add as a new bounded context when needed)
- ML model inference path (see `docs/BOUNDED_CONTEXTS.md` for the extension pattern)

---

## Changelog

With the recent projects, a new set of best practises and enhancements came to my mind that now have
been included here.

### V3.1 (2026-03-25)

**`services/client.py`**
- `complete(system, user) -> str` replaced by typed `CompletionRequest` / `CompletionResult` — preserves temperature, response_format, and token tracking without `**kwargs`
- `EmbeddingClient` added as a separate `@runtime_checkable` Protocol (RAG projects only)
- `DummyEmbeddingClient` added as test stub

**`services/processor.py`**
- `Retriever()` no longer instantiated in `__init__` — receives `RetrieverProtocol | None` via constructor injection
- Prompt call updated to `CompletionRequest`

**`services/retriever.py`**
- `RetrieverProtocol` introduced as `@runtime_checkable` Protocol
- `Retriever` renamed to `KeywordRetriever` with explicit extension point for semantic search

**`tests/conftest.py`**
- Stubs updated to `CompletionRequest` signature
- Protocol assertions added at import time

**`tests/unit/test_protocols.py`** _(new)_
- Fitness function tests for all client Protocol contracts

**`docs/BOUNDED_CONTEXTS.md`**
- Error Handling Strategy table added
- Fitness Functions table added
- `core/exceptions.py` convention documented

**`.dockerignore`** _(new)_


