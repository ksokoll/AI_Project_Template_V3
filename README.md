# AI Project Template V3

A minimal, production-oriented starting point for AI/ML services.

Clone, rename the package, wire in your provider, and start building —
without the boilerplate overhead.

---

## What's Included

```
src/app/
  core/          Config, Pydantic schemas, input validation
  services/      ServiceClient Protocol, Processor, optional Retriever (RAG)
  prompts/       Versioned prompt library (optional — delete if not LLM-based)
  pipeline.py    Orchestration
  main.py        FastAPI entry point

tests/
  unit/          Behaviour-named unit tests, no I/O
  integration/   Full pipeline with MockClient

docs/
  ARCHITECTURE.md
  BOUNDED_CONTEXTS.md
  DEVLOG.md
  decisions/ADR_TEMPLATE.md

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

## Version History

| Version | Description |
|---|---|
| V1 | Initial LLM template |
| V2 | Added error handling, logging, prompt library (Chip Huyen pattern) |
| V3 | src-layout, Protocol-based DI, test pyramid, CI/CD, Docker, Makefile |
