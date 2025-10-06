"""PostgreSQL implementation of GoalRepository."""

from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import Boolean, Column, DateTime, MetaData, String, Table, delete, select, update
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.asyncio import AsyncEngine

from ai_life_backend.goals.domain import Goal

metadata = MetaData()

MAX_TITLE_LENGTH = 255

goals_table = Table(
    "goals",
    metadata,
    Column("id", PG_UUID(as_uuid=True), primary_key=True),
    Column("title", String(MAX_TITLE_LENGTH), nullable=False),
    Column("is_done", Boolean, nullable=False),
    Column("date_created", DateTime(timezone=True), nullable=False),
    Column("date_updated", DateTime(timezone=True), nullable=False),
)


class PostgresGoalRepository:
    """PostgreSQL implementation of GoalRepository Protocol."""

    def __init__(self, engine: AsyncEngine) -> None:
        """Initialize repository with database engine."""
        self._engine = engine

    async def create(self, title: str) -> Goal:
        """Create new goal."""
        if len(title) > MAX_TITLE_LENGTH:
            msg = f"Title cannot exceed {MAX_TITLE_LENGTH} characters"
            raise ValueError(msg)

        async with self._engine.begin() as conn:
            result = await conn.execute(
                goals_table.insert().values(title=title).returning(goals_table)
            )
            row = result.one()
            return Goal(
                id=row.id,
                title=row.title,
                is_done=row.is_done,
                date_created=row.date_created,
                date_updated=row.date_updated,
            )

    async def get_by_id(self, goal_id: UUID) -> Goal | None:
        """Retrieve goal by ID."""
        async with self._engine.connect() as conn:
            result = await conn.execute(select(goals_table).where(goals_table.c.id == goal_id))
            row = result.one_or_none()
            if not row:
                return None
            return Goal(
                id=row.id,
                title=row.title,
                is_done=row.is_done,
                date_created=row.date_created,
                date_updated=row.date_updated,
            )

    async def list_all(self) -> list[Goal]:
        """List all goals, sorted by is_done ASC, date_updated DESC."""
        async with self._engine.connect() as conn:
            result = await conn.execute(
                select(goals_table).order_by(
                    goals_table.c.is_done, goals_table.c.date_updated.desc()
                )
            )
            return [
                Goal(
                    id=row.id,
                    title=row.title,
                    is_done=row.is_done,
                    date_created=row.date_created,
                    date_updated=row.date_updated,
                )
                for row in result.all()
            ]

    async def list_by_status(self, is_done: bool) -> list[Goal]:
        """List goals filtered by completion status, sorted by date_updated DESC."""
        async with self._engine.connect() as conn:
            result = await conn.execute(
                select(goals_table)
                .where(goals_table.c.is_done == is_done)
                .order_by(goals_table.c.date_updated.desc())
            )
            return [
                Goal(
                    id=row.id,
                    title=row.title,
                    is_done=row.is_done,
                    date_created=row.date_created,
                    date_updated=row.date_updated,
                )
                for row in result.all()
            ]

    async def update(
        self,
        goal_id: UUID,
        title: str | None = None,
        is_done: bool | None = None,
    ) -> Goal | None:
        """Update goal fields and refresh date_updated."""
        if title is None and is_done is None:
            msg = "At least one field must be provided"
            raise ValueError(msg)

        if title is not None:
            if not title.strip():
                msg = "Title cannot be empty or whitespace-only"
                raise ValueError(msg)
            if len(title) > MAX_TITLE_LENGTH:
                msg = "Title cannot exceed 255 characters"
                raise ValueError(msg)

        update_values: dict[str, Any] = {"date_updated": datetime.now(UTC)}

        if title is not None:
            update_values["title"] = title
        if is_done is not None:
            update_values["is_done"] = is_done

        async with self._engine.begin() as conn:
            result = await conn.execute(
                update(goals_table)
                .where(goals_table.c.id == goal_id)
                .values(**update_values)
                .returning(goals_table)
            )
            row = result.one_or_none()
            if not row:
                return None
            return Goal(
                id=row.id,
                title=row.title,
                is_done=row.is_done,
                date_created=row.date_created,
                date_updated=row.date_updated,
            )

    async def delete(self, goal_id: UUID) -> bool:
        """Permanently delete a goal."""
        async with self._engine.begin() as conn:
            result = await conn.execute(delete(goals_table).where(goals_table.c.id == goal_id))
            return result.rowcount > 0
