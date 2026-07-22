# syntax=docker/dockerfile:1

FROM python:3.12-slim AS builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

RUN pip install --no-cache-dir "poetry>=2.0,<3.0"

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root \
    && rm -rf "$POETRY_CACHE_DIR"

FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN addgroup --system app \
    && adduser --system --ingroup app app

COPY --from=builder /app/.venv /app/.venv
COPY --chown=app:app pyproject.toml poetry.lock ./
COPY --chown=app:app src ./src
COPY --chown=app:app artifacts ./artifacts
COPY --chown=app:app data/processed ./data/processed

USER app

EXPOSE 8080

CMD ["sh", "-c", "exec uvicorn financial_api.api:app --host 0.0.0.0 --port ${PORT} --app-dir src"]
