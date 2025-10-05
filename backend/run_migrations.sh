#!/bin/bash
# Database migration script for backend.goals

set -e

echo "Waiting for PostgreSQL to be ready..."
sleep 3

echo "Running Alembic migrations..."
DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/ai_life_os" uv run alembic upgrade head

echo "✓ Migrations complete!"
