"""PostgreSQL implementation of MilestoneRepository."""

from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    MetaData,
    String,
    Table,
    delete,
    select,
    update,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.asyncio import AsyncEngine

from ai_life_backend.milestones.domain.milestone import Milestone

metadata = MetaData()

MAX_TITLE_LENGTH = 255

milestones_table = Table(
    "milestones",
    metadata,
    Column("id", PG_UUID(as_uuid=True), primary_key=True),
    Column("goal_id", PG_UUID(as_uuid=True), ForeignKey("goals.id"), nullable=False),
    Column("title", String(MAX_TITLE_LENGTH), nullable=False),
    Column("due", DateTime(timezone=True), nullable=True),
    Column("status", String(50), nullable=False),
    Column("demo_criterion", String(MAX_TITLE_LENGTH), nullable=False),
    Column("blocking", Boolean, nullable=False),
    Column("date_created", DateTime(timezone=True), nullable=False),
    Column("date_updated", DateTime(timezone=True), nullable=False),
)


class PostgresMilestoneRepository:
    """PostgreSQL implementation of MilestoneRepository Protocol."""

    def __init__(self, engine: AsyncEngine) -> None:
        """Initialize repository with database engine."""
        self._engine = engine

    async def create(
        self,
        goal_id: UUID,
        title: str,
        status: str,
        demo_criterion: str,
        blocking: bool,
        due: datetime | None = None,
    ) -> Milestone:
        """Create new milestone."""
        if len(title) > MAX_TITLE_LENGTH:
            msg = f"Title cannot exceed {MAX_TITLE_LENGTH} characters"
            raise ValueError(msg)

        if len(demo_criterion) > MAX_TITLE_LENGTH:
            msg = f"Demo criterion cannot exceed {MAX_TITLE_LENGTH} characters"
            raise ValueError(msg)

        async with self._engine.begin() as conn:
            result = await conn.execute(
                milestones_table.insert()
                .values(
                    goal_id=goal_id,
                    title=title,
                    due=due,
                    status=status,
                    demo_criterion=demo_criterion,
                    blocking=blocking,
                )
                .returning(milestones_table)
            )
            row = result.one()
            return Milestone(
                id=row.id,
                goal_id=row.goal_id,
                title=row.title,
                due=row.due,
                status=row.status,
                demo_criterion=row.demo_criterion,
                blocking=row.blocking,
                date_created=row.date_created,
                date_updated=row.date_updated,
            )

    async def get_by_id(self, milestone_id: UUID) -> Milestone | None:
        """Retrieve milestone by ID."""
        async with self._engine.connect() as conn:
            result = await conn.execute(
                select(milestones_table).where(milestones_table.c.id == milestone_id)
            )
            row = result.one_or_none()
            if not row:
                return None
            return Milestone(
                id=row.id,
                goal_id=row.goal_id,
                title=row.title,
                due=row.due,
                status=row.status,
                demo_criterion=row.demo_criterion,
                blocking=row.blocking,
                date_created=row.date_created,
                date_updated=row.date_updated,
            )

    async def list_all(self) -> list[Milestone]:
        """List all milestones, sorted by date_created DESC."""
        async with self._engine.connect() as conn:
            result = await conn.execute(
                select(milestones_table).order_by(milestones_table.c.date_created.desc())
            )
            return [
                Milestone(
                    id=row.id,
                    goal_id=row.goal_id,
                    title=row.title,
                    due=row.due,
                    status=row.status,
                    demo_criterion=row.demo_criterion,
                    blocking=row.blocking,
                    date_created=row.date_created,
                    date_updated=row.date_updated,
                )
                for row in result.all()
            ]

    async def list_by_goal(self, goal_id: UUID) -> list[Milestone]:
        """List milestones for a specific goal, sorted by due date and date_created."""
        async with self._engine.connect() as conn:
            result = await conn.execute(
                select(milestones_table)
                .where(milestones_table.c.goal_id == goal_id)
                .order_by(milestones_table.c.due.nullsfirst(), milestones_table.c.date_created.desc())
            )
            return [
                Milestone(
                    id=row.id,
                    goal_id=row.goal_id,
                    title=row.title,
                    due=row.due,
                    status=row.status,
                    demo_criterion=row.demo_criterion,
                    blocking=row.blocking,
                    date_created=row.date_created,
                    date_updated=row.date_updated,
                )
                for row in result.all()
            ]

    async def update(
        self,
        milestone_id: UUID,
        title: str | None = None,
        due: datetime | None | object = None,  # object is sentinel for "not provided"
        status: str | None = None,
        demo_criterion: str | None = None,
        blocking: bool | None = None,
    ) -> Milestone | None:
        """Update milestone fields and refresh date_updated."""
        _UNSET = object()  # Sentinel value to distinguish None from "not provided"

        if all(
            v is None or (v is _UNSET)
            for v in [title, due if due is not _UNSET else _UNSET, status, demo_criterion, blocking]
        ):
            msg = "At least one field must be provided"
            raise ValueError(msg)

        if title is not None:
            if not title.strip():
                msg = "Title cannot be empty or whitespace-only"
                raise ValueError(msg)
            if len(title) > MAX_TITLE_LENGTH:
                msg = f"Title cannot exceed {MAX_TITLE_LENGTH} characters"
                raise ValueError(msg)

        if demo_criterion is not None:
            if not demo_criterion.strip():
                msg = "Demo criterion cannot be empty or whitespace-only"
                raise ValueError(msg)
            if len(demo_criterion) > MAX_TITLE_LENGTH:
                msg = f"Demo criterion cannot exceed {MAX_TITLE_LENGTH} characters"
                raise ValueError(msg)

        update_values: dict[str, Any] = {"date_updated": datetime.now(UTC)}

        if title is not None:
            update_values["title"] = title
        if due is not _UNSET:
            update_values["due"] = due
        if status is not None:
            update_values["status"] = status
        if demo_criterion is not None:
            update_values["demo_criterion"] = demo_criterion
        if blocking is not None:
            update_values["blocking"] = blocking

        async with self._engine.begin() as conn:
            result = await conn.execute(
                update(milestones_table)
                .where(milestones_table.c.id == milestone_id)
                .values(**update_values)
                .returning(milestones_table)
            )
            row = result.one_or_none()
            if not row:
                return None
            return Milestone(
                id=row.id,
                goal_id=row.goal_id,
                title=row.title,
                due=row.due,
                status=row.status,
                demo_criterion=row.demo_criterion,
                blocking=row.blocking,
                date_created=row.date_created,
                date_updated=row.date_updated,
            )

    async def delete(self, milestone_id: UUID) -> bool:
        """Permanently delete a milestone."""
        async with self._engine.begin() as conn:
            result = await conn.execute(
                delete(milestones_table).where(milestones_table.c.id == milestone_id)
            )
            return result.rowcount > 0
