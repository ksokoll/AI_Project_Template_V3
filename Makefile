.PHONY: lint format test test-unit test-integration docker-build run clean

# ── Toolchain ─────────────────────────────────────────────────────────────────

lint:
	ruff check src/ tests/
	mypy src/

format:
	ruff format src/ tests/
	ruff check --fix src/ tests/

# ── Tests ─────────────────────────────────────────────────────────────────────

test:
	pytest --cov=src --cov-report=term-missing

test-unit:
	pytest -m unit

test-integration:
	pytest -m integration

# ── Docker ────────────────────────────────────────────────────────────────────

docker-build:
	docker build -t app:dev .

run:
	docker run --env-file .env -p 8000:8000 app:dev

# ── Housekeeping ──────────────────────────────────────────────────────────────

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache"   -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete
