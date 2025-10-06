"""Pydantic schemas for Goals API."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class GoalCreateRequest(BaseModel):
    """Request schema for creating a goal."""

    title: str = Field(..., min_length=1, max_length=255)

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate that title is not empty or whitespace-only."""
        if not v.strip():
            msg = "Title cannot be empty or whitespace-only"
            raise ValueError(msg)
        return v


class GoalUpdateRequest(BaseModel):
    """Request schema for updating a goal."""

    title: str | None = Field(None, min_length=1, max_length=255)
    is_done: bool | None = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str | None) -> str | None:
        """Validate that title is not empty or whitespace-only if provided."""
        if v is not None and not v.strip():
            msg = "Title cannot be empty or whitespace-only"
            raise ValueError(msg)
        return v


class GoalResponse(BaseModel):
    """Response schema for a goal."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    is_done: bool
    date_created: datetime
    date_updated: datetime


class GoalListResponse(BaseModel):
    """Response schema for list of goals."""

    goals: list[GoalResponse]


class ErrorResponse(BaseModel):
    """Error response schema (RFC 7807)."""

    detail: str
    type: str | None = None
    status: int | None = None


class Problem(BaseModel):
    """RFC 7807 Problem Details for HTTP APIs."""

    type: str = Field(
        default="about:blank", description="A URI reference that identifies the problem type"
    )
    title: str = Field(description="A short, human-readable summary of the problem type")
    status: int = Field(description="The HTTP status code")
    detail: str | None = Field(
        default=None, description="A human-readable explanation specific to this occurrence"
    )
    instance: str | None = Field(
        default=None, description="A URI reference that identifies the specific occurrence"
    )
