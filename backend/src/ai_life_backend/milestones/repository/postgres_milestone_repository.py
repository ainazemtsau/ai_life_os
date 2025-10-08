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

from ai_life_backend.milestones.domain.milestone import (
    CreateMilestoneInput,
    Milestone,
    UpdateMilestoneInput,
)

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

    async def create(self, input_data: CreateMilestoneInput) -> Milestone:
        """Create new milestone."""
        if len(input_data.title) > MAX_TITLE_LENGTH:
            msg = f"Title cannot exceed {MAX_TITLE_LENGTH} characters"
            raise ValueError(msg)

        if len(input_data.demo_criterion) > MAX_TITLE_LENGTH:
            msg = f"Demo criterion cannot exceed {MAX_TITLE_LENGTH} characters"
            raise ValueError(msg)

        async with self._engine.begin() as conn:
            result = await conn.execute(
                milestones_table.insert()
                .values(
                    goal_id=input_data.goal_id,
                    title=input_data.title,
                    due=input_data.due,
                    status=input_data.status,
                    demo_criterion=input_data.demo_criterion,
                    blocking=input_data.blocking,
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
                .order_by(
                    milestones_table.c.due.nullsfirst(),
                    milestones_table.c.date_created.desc(),
                )
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

    @staticmethod
    def _validate_update_input(input_data: UpdateMilestoneInput) -> None:
        """Validate update input data."""
        has_updates = any(
            [
                input_data.title is not None,
                input_data.due is not None,
                input_data.status is not None,
                input_data.demo_criterion is not None,
                input_data.blocking is not None,
            ]
        )
        if not has_updates:
            msg = "At least one field must be provided"
            raise ValueError(msg)

        if input_data.title is not None and not input_data.title.strip():
            msg = "Title cannot be empty or whitespace-only"
            raise ValueError(msg)

        if input_data.demo_criterion is not None and not input_data.demo_criterion.strip():
            msg = "Demo criterion cannot be empty or whitespace-only"
            raise ValueError(msg)

        if input_data.title and len(input_data.title) > MAX_TITLE_LENGTH:
            msg = f"Title cannot exceed {MAX_TITLE_LENGTH} characters"
            raise ValueError(msg)

        if input_data.demo_criterion and len(input_data.demo_criterion) > MAX_TITLE_LENGTH:
            msg = f"Demo criterion cannot exceed {MAX_TITLE_LENGTH} characters"
            raise ValueError(msg)

    @staticmethod
    def _build_update_dict(input_data: UpdateMilestoneInput) -> dict[str, Any]:
        """Build dictionary of values to update."""
        update_values: dict[str, Any] = {"date_updated": datetime.now(UTC)}

        if input_data.title is not None:
            update_values["title"] = input_data.title
        if input_data.due is not None:
            update_values["due"] = input_data.due
        if input_data.status is not None:
            update_values["status"] = input_data.status
        if input_data.demo_criterion is not None:
            update_values["demo_criterion"] = input_data.demo_criterion
        if input_data.blocking is not None:
            update_values["blocking"] = input_data.blocking

        return update_values

    async def update(
        self, milestone_id: UUID, input_data: UpdateMilestoneInput
    ) -> Milestone | None:
        """Update milestone fields and refresh date_updated."""
        self._validate_update_input(input_data)
        update_values = self._build_update_dict(input_data)

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
