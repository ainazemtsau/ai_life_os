"""Pydantic schemas for Milestones API."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


# Status type matching the unified status set from the spec
MilestoneStatus = Literal["todo", "doing", "done", "blocked"]


class MilestoneCreateRequest(BaseModel):
    """Request schema for creating a milestone."""

    goal_id: UUID
    title: str = Field(..., min_length=1, max_length=255)
    due: datetime | None = None
    status: MilestoneStatus = "todo"
    demo_criterion: str = Field(..., min_length=1, max_length=255)
    blocking: bool = False

    @field_validator("title", "demo_criterion")
    @classmethod
    def not_empty_or_whitespace(cls, v: str) -> str:
        """Validate that field is not empty or whitespace-only."""
        if not v.strip():
            msg = "Field cannot be empty or whitespace-only"
            raise ValueError(msg)
        return v


class MilestoneUpdateRequest(BaseModel):
    """Request schema for updating a milestone."""

    title: str | None = Field(None, min_length=1, max_length=255)
    due: datetime | None = None
    status: MilestoneStatus | None = None
    demo_criterion: str | None = Field(None, min_length=1, max_length=255)
    blocking: bool | None = None

    @field_validator("title", "demo_criterion")
    @classmethod
    def not_empty_or_whitespace(cls, v: str | None) -> str | None:
        """Validate that field is not empty or whitespace-only if provided."""
        if v is not None and not v.strip():
            msg = "Field cannot be empty or whitespace-only"
            raise ValueError(msg)
        return v


class MilestoneResponse(BaseModel):
    """Response schema for a milestone."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    goal_id: UUID
    title: str
    due: datetime | None
    status: str
    demo_criterion: str
    blocking: bool
    date_created: datetime
    date_updated: datetime


class MilestoneListResponse(BaseModel):
    """Response schema for list of milestones."""

    milestones: list[MilestoneResponse]
