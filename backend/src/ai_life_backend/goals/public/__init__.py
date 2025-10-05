"""Public API for backend.goals module - in-process port."""
from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from uuid import UUID

from ..api.routes import router as goals_router
from ..domain import Goal
from ..repository.postgres_goal_repository import PostgresGoalRepository


@dataclass(frozen=True)
class GoalDTO:
    """
    Data Transfer Object for Goal entity.

    Read-only DTO for same-process consumers. Does not expose ORM models.

    Attributes:
        id: Unique identifier (UUID)
        title: Goal description
        is_done: Completion status
        date_created: Creation timestamp (UTC)
        date_updated: Last modification timestamp (UTC)
    """
    id: UUID
    title: str
    is_done: bool
    date_created: datetime
    date_updated: datetime

    @staticmethod
    def from_domain(goal: Goal) -> "GoalDTO":
        """Convert domain Goal to DTO."""
        return GoalDTO(
            id=goal.id,
            title=goal.title,
            is_done=goal.is_done,
            date_created=goal.date_created,
            date_updated=goal.date_updated,
        )


async def list_goals(status: Literal['all', 'active', 'done'] = 'all') -> list[GoalDTO]:
    """
    List goals with optional status filter (read-only).

    Returns goals ordered by: active first, then by date_updated DESC.

    Args:
        status: Filter by status - 'all', 'active' (not done), or 'done'

    Returns:
        List of GoalDTO objects

    Raises:
        RuntimeError: If database connection fails
    """
    from ai_life_backend.database import get_engine

    repo = PostgresGoalRepository(get_engine())

    if status == 'active':
        goals = await repo.list_by_status(False)
    elif status == 'done':
        goals = await repo.list_by_status(True)
    else:  # 'all'
        goals = await repo.list_all()

    return [GoalDTO.from_domain(g) for g in goals]


async def get_goal(id: UUID) -> GoalDTO | None:
    """
    Retrieve a single goal by ID (read-only).

    Args:
        id: Goal UUID

    Returns:
        GoalDTO if found, None otherwise

    Raises:
        RuntimeError: If database connection fails
    """
    from ai_life_backend.database import get_engine

    repo = PostgresGoalRepository(get_engine())
    goal = await repo.get_by_id(id)

    if goal is None:
        return None

    return GoalDTO.from_domain(goal)


__all__ = [
    "goals_router",  # HTTP/FastAPI (cross-process)
    "GoalDTO",       # In-process DTO
    "list_goals",    # In-process read function
    "get_goal",      # In-process read function
]
