"""FastAPI router for Goals API."""

from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from ai_life_backend.database import get_engine
from ai_life_backend.goals.api.schemas import (
    GoalCreateRequest,
    GoalListResponse,
    GoalResponse,
    GoalUpdateRequest,
)
from ai_life_backend.goals.repository.postgres_goal_repository import PostgresGoalRepository

router = APIRouter(prefix="/goals", tags=["goals"])


def get_repository() -> PostgresGoalRepository:
    return PostgresGoalRepository(get_engine())


RepoDep = Annotated[PostgresGoalRepository, Depends(get_repository)]
StatusFilter = Annotated[Literal["active", "done"] | None, Query()]


@router.post("", response_model=GoalResponse, status_code=201)
async def create_goal(request: GoalCreateRequest, repo: RepoDep) -> GoalResponse:
    try:
        goal = await repo.create(request.title)
        return GoalResponse.model_validate(goal)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@router.get("", response_model=GoalListResponse)
async def list_goals(repo: RepoDep, status: StatusFilter = None) -> GoalListResponse:
    if status == "active":
        goals = await repo.list_by_status(False)
    elif status == "done":
        goals = await repo.list_by_status(True)
    else:
        goals = await repo.list_all()
    return GoalListResponse(goals=[GoalResponse.model_validate(g) for g in goals])


@router.get("/{goal_id}", response_model=GoalResponse)
async def get_goal(goal_id: UUID, repo: RepoDep) -> GoalResponse:
    goal = await repo.get_by_id(goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return GoalResponse.model_validate(goal)


@router.patch("/{goal_id}", response_model=GoalResponse)
async def update_goal(goal_id: UUID, request: GoalUpdateRequest, repo: RepoDep) -> GoalResponse:
    """Update a goal's title and/or completion status.

    Args:
        goal_id (UUID): The unique identifier of the goal to update.
        request (GoalUpdateRequest): The fields to update (title and/or is_done).
        repo (PostgresGoalRepository): The repository instance for database operations.

    Returns:
        GoalResponse: The updated goal.

    Raises:
        HTTPException: If no fields are provided, or if the goal is not found, or if validation
        fails.
    """
    if request.title is None and request.is_done is None:
        raise HTTPException(status_code=422, detail="At least one field must be provided")
    try:
        goal = await repo.update(goal_id, request.title, request.is_done)
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        return GoalResponse.model_validate(goal)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@router.delete("/{goal_id}", status_code=204)
async def delete_goal(goal_id: UUID, repo: RepoDep) -> None:
    """Delete a goal by its ID.

    Raises a 404 HTTPException if the goal is not found.
    """
    success = await repo.delete(goal_id)
    if not success:
        raise HTTPException(status_code=404, detail="Goal not found")
