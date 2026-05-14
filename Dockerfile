FROM python:3.12-slim-trixie

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-cache --no-dev --no-install-project

COPY . .

RUN uv sync --locked

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app/perceiver_service/src
