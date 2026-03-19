# ── Stage 1: Build ────────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Isolated venv so the entire environment can be copied as one unit.
# This is more robust than copying site-packages + individual binaries,
# and works for any combination of extras (gunicorn, cli tools, etc.).
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY pyproject.toml .
COPY src/ src/

RUN pip install --no-cache-dir .

# ── Stage 2: Production ───────────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Copy the complete venv — no fragile per-binary copies needed
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY src/ src/

# Non-root user for least-privilege execution
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]