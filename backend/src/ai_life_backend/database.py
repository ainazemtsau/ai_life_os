"""Database configuration and engine management."""

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

_engine: AsyncEngine | None = None


def get_engine() -> AsyncEngine:
    """Get or create async database engine."""
    global _engine
    if _engine is None:
        database_url = os.getenv(
            "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_life_os"
        )
        _engine = create_async_engine(database_url, echo=False)
    return _engine
