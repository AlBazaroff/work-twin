FROM python:3.12-slim-trixie

WORKDIR /perceiver_service

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-cache --no-dev --no-install-project

COPY . .

RUN uv sync --locked

ENV PATH="/perceiver_service/.venv/bin:$PATH"
