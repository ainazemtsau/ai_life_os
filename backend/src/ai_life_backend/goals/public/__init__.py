"""Public API for backend.goals — in-process read-only port + HTTP router wrapper."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from uuid import UUID

from fastapi import APIRouter

from ai_life_backend.contracts.core_protocols import (
    RFC7807_MIME,
    ProblemDict,
)
from ai_life_backend.core.public import make_public_router
from ai_life_backend.database import get_engine
from ai_life_backend.goals.api.routes import router as _internal_router
from ai_life_backend.goals.domain import Goal
from ai_life_backend.goals.repository.postgres_goal_repository import PostgresGoalRepository

# ---------- In-process DTO & read-only port ----------


@dataclass(frozen=True)
class GoalDTO:
    """Read-only DTO for same-process consumers. No ORM exposure."""

    id: UUID
    title: str
    is_done: bool
    date_created: datetime
    date_updated: datetime

    @staticmethod
    def from_domain(goal: Goal) -> GoalDTO:
        """Convert domain Goal entity to DTO."""
        return GoalDTO(
            id=goal.id,
            title=goal.title,
            is_done=goal.is_done,
            date_created=goal.date_created,
            date_updated=goal.date_updated,
        )


async def list_goals(status: Literal["all", "active", "done"] = "all") -> list[GoalDTO]:
    """List goals with optional status filter (read-only).

    Ordering: active first, then by date_updated DESC.
    """
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
    repo = PostgresGoalRepository(get_engine())
    goal = await repo.get_by_id(id)
    return None if goal is None else GoalDTO.from_domain(goal)


# ---------- HTTP public surface (router) ----------
goals_router: APIRouter = make_public_router(_internal_router)

__all__ = [
    "RFC7807_MIME",
    "GoalDTO",  # in-process DTO
    "ProblemDict",  # re-export type for convenience (typing only)
    "get_goal",  # in-process read function
    "goals_router",  # HTTP/FastAPI (cross-process; include in app with prefix="/api")
    "list_goals",  # in-process read function
]
