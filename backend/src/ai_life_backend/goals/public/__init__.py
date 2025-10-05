"""Public API for backend.goals module — in-process port + HTTP router wrapper."""

from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from uuid import UUID

from fastapi import APIRouter

# Import FastAPI Problem schema model (your RFC7807 model)
from ai_life_backend.errors.models import Problem

# Internal router with actual endpoints (prefix/tags defined inside)
from ..api.routes import router as _internal_router
from ai_life_backend.core.httpkit import make_public_router
from ..domain import Goal
from ..repository.postgres_goal_repository import PostgresGoalRepository


# ---------- In-process DTO & read-only port ----------


@dataclass(frozen=True)
class GoalDTO:
    """
    Read-only Data Transfer Object for same-process consumers.
    Does not expose ORM models.
    """

    id: UUID
    title: str
    is_done: bool
    date_created: datetime
    date_updated: datetime

    @staticmethod
    def from_domain(goal: Goal) -> "GoalDTO":
        return GoalDTO(
            id=goal.id,
            title=goal.title,
            is_done=goal.is_done,
            date_created=goal.date_created,
            date_updated=goal.date_updated,
        )


async def list_goals(status: Literal["all", "active", "done"] = "all") -> list[GoalDTO]:
    """
    List goals with optional status filter (read-only).
    Ordering: active first, then by date_updated DESC.
    """
    from ai_life_backend.database import get_engine

    repo = PostgresGoalRepository(get_engine())
    if status == "active":
        goals = await repo.list_by_status(False)
    elif status == "done":
        goals = await repo.list_by_status(True)
    else:
        goals = await repo.list_all()

    return [GoalDTO.from_domain(g) for g in goals]


async def get_goal(id: UUID) -> GoalDTO | None:
    """Retrieve a single goal by ID (read-only)."""
    from ai_life_backend.database import get_engine

    repo = PostgresGoalRepository(get_engine())
    goal = await repo.get_by_id(id)
    return None if goal is None else GoalDTO.from_domain(goal)


goals_router = make_public_router(_internal_router)

__all__ = [
    "goals_router",  # HTTP/FastAPI (cross-process; included in app with prefix="/api")
    "GoalDTO",  # In-process DTO
    "list_goals",  # In-process read function
    "get_goal",  # In-process read function
]
