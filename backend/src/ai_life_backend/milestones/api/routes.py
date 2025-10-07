"""FastAPI router for Milestones API."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from ai_life_backend.database import get_engine
from ai_life_backend.milestones.api.schemas import (
    MilestoneCreateRequest,
    MilestoneListResponse,
    MilestoneResponse,
    MilestoneUpdateRequest,
)
from ai_life_backend.milestones.repository.postgres_milestone_repository import (
    PostgresMilestoneRepository,
)

router = APIRouter(prefix="/milestones", tags=["milestones"])


def get_repository() -> PostgresMilestoneRepository:
    """Dependency to get the milestone repository."""
    return PostgresMilestoneRepository(get_engine())


RepoDep = Annotated[PostgresMilestoneRepository, Depends(get_repository)]


@router.post("", response_model=MilestoneResponse, status_code=201)
async def create_milestone(request: MilestoneCreateRequest, repo: RepoDep) -> MilestoneResponse:
    """Create a new milestone.

    Args:
        request: Milestone creation data
        repo: Milestone repository

    Returns:
        The created milestone

    Raises:
        HTTPException: If validation fails (422)
    """
    try:
        milestone = await repo.create(
            goal_id=request.goal_id,
            title=request.title,
            status=request.status,
            demo_criterion=request.demo_criterion,
            blocking=request.blocking,
            due=request.due,
        )
        return MilestoneResponse.model_validate(milestone)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@router.get("", response_model=MilestoneListResponse)
async def list_milestones(repo: RepoDep) -> MilestoneListResponse:
    """List all milestones.

    Args:
        repo: Milestone repository

    Returns:
        List of all milestones
    """
    milestones = await repo.list_all()
    return MilestoneListResponse(
        milestones=[MilestoneResponse.model_validate(m) for m in milestones]
    )


@router.get("/{milestone_id}", response_model=MilestoneResponse)
async def get_milestone(milestone_id: UUID, repo: RepoDep) -> MilestoneResponse:
    """Get a milestone by ID.

    Args:
        milestone_id: The milestone ID
        repo: Milestone repository

    Returns:
        The milestone

    Raises:
        HTTPException: If milestone not found (404)
    """
    milestone = await repo.get_by_id(milestone_id)
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    return MilestoneResponse.model_validate(milestone)


@router.patch("/{milestone_id}", response_model=MilestoneResponse)
async def update_milestone(
    milestone_id: UUID, request: MilestoneUpdateRequest, repo: RepoDep
) -> MilestoneResponse:
    """Update a milestone.

    Args:
        milestone_id: The milestone ID
        request: Fields to update
        repo: Milestone repository

    Returns:
        The updated milestone

    Raises:
        HTTPException: If no fields provided (422), if milestone not found (404),
                      or if validation fails (422)
    """
    # Check that at least one field is provided
    if all(
        v is None
        for v in [
            request.title,
            request.status,
            request.demo_criterion,
            request.blocking,
        ]
    ) and not hasattr(request, "due"):
        raise HTTPException(status_code=422, detail="At least one field must be provided")

    try:
        milestone = await repo.update(
            milestone_id,
            title=request.title,
            due=request.due,
            status=request.status,
            demo_criterion=request.demo_criterion,
            blocking=request.blocking,
        )
        if not milestone:
            raise HTTPException(status_code=404, detail="Milestone not found")
        return MilestoneResponse.model_validate(milestone)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@router.delete("/{milestone_id}", status_code=204)
async def delete_milestone(milestone_id: UUID, repo: RepoDep) -> None:
    """Delete a milestone.

    Args:
        milestone_id: The milestone ID
        repo: Milestone repository

    Raises:
        HTTPException: If milestone not found (404)
    """
    success = await repo.delete(milestone_id)
    if not success:
        raise HTTPException(status_code=404, detail="Milestone not found")
