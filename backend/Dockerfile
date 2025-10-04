# Backend dev (Python + uv, UV-only)
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates build-essential \
    && rm -rf /var/lib/apt/lists/*

# install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# deps слой
COPY pyproject.toml README.md ./
# исходники
COPY src ./src

# dev deps (из [project.optional-dependencies].dev)
RUN uv lock && uv sync --all-extras

# плейсхолдер до появления uvicorn/FastAPI
CMD ["bash", "-lc", "echo 'backend container up (placeholder)'; tail -f /dev/null"]
