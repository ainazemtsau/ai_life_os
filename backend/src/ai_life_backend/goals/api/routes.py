"""FastAPI router for Goals API."""
from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from typing import Literal
from .schemas import GoalCreateRequest, GoalUpdateRequest, GoalResponse, GoalListResponse
from ..repository.postgres_goal_repository import PostgresGoalRepository
from ..domain import Goal

router = APIRouter(prefix="/goals", tags=["goals"])


def get_repository() -> PostgresGoalRepository:
    """Dependency injection for repository."""
    from ai_life_backend.database import get_engine
    return PostgresGoalRepository(get_engine())


@router.post("", response_model=GoalResponse, status_code=201)
async def create_goal(
    request: GoalCreateRequest,
    repo: PostgresGoalRepository = Depends(get_repository)
) -> GoalResponse:
    """Create a new goal."""
    try:
        goal = await repo.create(request.title)
        return GoalResponse.model_validate(goal)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("", response_model=GoalListResponse)
async def list_goals(
    status: Literal["active", "done"] | None = Query(None),
    repo: PostgresGoalRepository = Depends(get_repository)
) -> GoalListResponse:
    """List all goals with optional status filter."""
    if status == "active":
        goals = await repo.list_by_status(False)
    elif status == "done":
        goals = await repo.list_by_status(True)
    else:
        goals = await repo.list_all()

    return GoalListResponse(goals=[GoalResponse.model_validate(g) for g in goals])


@router.get("/{goal_id}", response_model=GoalResponse)
async def get_goal(
    goal_id: UUID,
    repo: PostgresGoalRepository = Depends(get_repository)
) -> GoalResponse:
    """Get a single goal by ID."""
    goal = await repo.get_by_id(goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return GoalResponse.model_validate(goal)


@router.patch("/{goal_id}", response_model=GoalResponse)
async def update_goal(
    goal_id: UUID,
    request: GoalUpdateRequest,
    repo: PostgresGoalRepository = Depends(get_repository)
) -> GoalResponse:
    """Update a goal's title and/or completion status."""
    if request.title is None and request.is_done is None:
        raise HTTPException(status_code=422, detail="At least one field must be provided")

    try:
        goal = await repo.update(goal_id, request.title, request.is_done)
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        return GoalResponse.model_validate(goal)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.delete("/{goal_id}", status_code=204)
async def delete_goal(
    goal_id: UUID,
    repo: PostgresGoalRepository = Depends(get_repository)
) -> None:
    """Delete a goal permanently."""
    success = await repo.delete(goal_id)
    if not success:
        raise HTTPException(status_code=404, detail="Goal not found")
