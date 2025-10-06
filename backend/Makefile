fmt:
	uv run ruff format .

fix:
	uv run ruff check . --fix

lint:
	uv run ruff check .

typecheck:
	uv run mypy .

test:
	uv run pytest -q -ra --maxfail=1

qa:
	uv run ruff format .
	uv run ruff check . --fix
	uv run ruff check .
	uv run mypy .
	uv run pytest -q -ra --maxfail=1 --cov=src/ai_life_backend --cov-report=term-missing

ci:
	uv run ruff format . --check
	uv run ruff check . --exit-non-zero-on-fix
	uv run ruff check .
	uv run mypy .
	uv run pytest -q -ra --maxfail=1 --cov=src/ai_life_backend --cov-report=term-missing
