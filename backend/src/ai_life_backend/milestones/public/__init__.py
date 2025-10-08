"""Public API for backend.milestones — in-process read-only port + HTTP router wrapper."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter

from ai_life_backend.contracts.core_protocols import (
    RFC7807_MIME,
    ProblemDict,
)
from ai_life_backend.core.public import make_public_router
from ai_life_backend.database import get_engine
from ai_life_backend.milestones.api.routes import router as _internal_router
from ai_life_backend.milestones.domain.milestone import Milestone
from ai_life_backend.milestones.repository.postgres_milestone_repository import (
    PostgresMilestoneRepository,
)

# ---------- In-process DTO & read-only port ----------


@dataclass(frozen=True)
class MilestoneDTO:
    """Read-only DTO for same-process consumers. No ORM exposure."""

    id: UUID
    goal_id: UUID
    title: str
    due: datetime | None
    status: str
    demo_criterion: str
    blocking: bool
    date_created: datetime
    date_updated: datetime

    @staticmethod
    def from_domain(milestone: Milestone) -> MilestoneDTO:
        """Convert domain Milestone entity to DTO."""
        return MilestoneDTO(
            id=milestone.id,
            goal_id=milestone.goal_id,
            title=milestone.title,
            due=milestone.due,
            status=milestone.status,
            demo_criterion=milestone.demo_criterion,
            blocking=milestone.blocking,
            date_created=milestone.date_created,
            date_updated=milestone.date_updated,
        )


async def list_milestones() -> list[MilestoneDTO]:
    """List all milestones (read-only).

    Ordering: date_created DESC.
    """
    repo = PostgresMilestoneRepository(get_engine())
    milestones = await repo.list_all()
    return [MilestoneDTO.from_domain(m) for m in milestones]


async def list_milestones_by_goal(goal_id: UUID) -> list[MilestoneDTO]:
    """List milestones for a specific goal (read-only).

    Ordering: due date (nulls first), then date_created DESC.
    """
    repo = PostgresMilestoneRepository(get_engine())
    milestones = await repo.list_by_goal(goal_id)
    return [MilestoneDTO.from_domain(m) for m in milestones]


async def get_milestone(id: UUID) -> MilestoneDTO | None:
    """Retrieve a single milestone by ID (read-only)."""
    repo = PostgresMilestoneRepository(get_engine())
    milestone = await repo.get_by_id(id)
    return None if milestone is None else MilestoneDTO.from_domain(milestone)


# ---------- HTTP public surface (router) ----------
milestones_router: APIRouter = make_public_router(_internal_router)

__all__ = [
    "RFC7807_MIME",
    "MilestoneDTO",  # in-process DTO
    "ProblemDict",  # re-export type for convenience (typing only)
    "get_milestone",  # in-process read function
    "list_milestones",  # in-process read function
    "list_milestones_by_goal",  # in-process read function
    "milestones_router",  # HTTP/FastAPI (cross-process; include in app with prefix="/api")
]
