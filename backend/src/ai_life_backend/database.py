"""Database configuration and engine management."""

from functools import lru_cache
import os

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


@lru_cache(maxsize=1)
def get_engine() -> AsyncEngine:
    """Create and return a cached SQLAlchemy AsyncEngine for the database connection."""
    url = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_life_os",
    )
    return create_async_engine(url, echo=False)
