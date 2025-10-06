# AI Life Backend (MVP) — UV Only

## Dev Quickstart
```bash
cd backend
uv lock                 # create/update uv.lock (commit it)
uv sync --all-extras    # installs dev deps from [project.optional-dependencies].dev
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest -q
```
# Check code
```bash
make qa
'''