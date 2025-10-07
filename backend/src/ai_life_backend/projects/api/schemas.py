"""Pydantic schemas for Projects and Tasks API."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from ai_life_backend.projects.domain.project import ProjectPriority, ProjectRisk
from ai_life_backend.projects.domain.task import (
    TaskSize,
    TaskEnergy,
    TaskContinuity,
    TaskClarity,
    TaskRisk,
)


# Project schemas
class ProjectCreate(BaseModel):
    """Schema for creating a new project."""

    goal_id: UUID | None = None
    title: str = Field(..., min_length=1, max_length=255)
    status: str = Field(default="todo", pattern="^(todo|doing|done|blocked)$")
    priority: ProjectPriority
    scope: str
    risk: ProjectRisk
    tags: list[str] = Field(default_factory=list)
    dependencies: list[UUID] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Ensure title is not empty after stripping."""
        if not v.strip():
            raise ValueError("Title cannot be empty or whitespace-only")
        return v


class ProjectUpdate(BaseModel):
    """Schema for updating an existing project."""

    title: str | None = Field(None, min_length=1, max_length=255)
    status: str | None = Field(None, pattern="^(todo|doing|done|blocked)$")
    priority: ProjectPriority | None = None
    scope: str | None = None
    risk: ProjectRisk | None = None
    tags: list[str] | None = None
    dependencies: list[UUID] | None = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str | None) -> str | None:
        """Ensure title is not empty after stripping if provided."""
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty or whitespace-only")
        return v


class ProjectResponse(BaseModel):
    """Schema for project response."""

    id: UUID
    goal_id: UUID | None
    title: str
    status: str
    priority: ProjectPriority
    scope: str
    risk: ProjectRisk
    tags: list[str]
    dependencies: list[UUID]
    date_created: datetime
    date_updated: datetime

    model_config = {"from_attributes": True}


# Task schemas
class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    project_id: UUID
    title: str = Field(..., min_length=1, max_length=255)
    status: str = Field(default="todo", pattern="^(todo|doing|done|blocked)$")
    dependencies: list[UUID] = Field(default_factory=list)
    size: TaskSize
    energy: TaskEnergy
    continuity: TaskContinuity
    clarity: TaskClarity
    risk: TaskRisk
    context: str = ""

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Ensure title is not empty after stripping."""
        if not v.strip():
            raise ValueError("Title cannot be empty or whitespace-only")
        return v


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""

    title: str | None = Field(None, min_length=1, max_length=255)
    status: str | None = Field(None, pattern="^(todo|doing|done|blocked)$")
    dependencies: list[UUID] | None = None
    size: TaskSize | None = None
    energy: TaskEnergy | None = None
    continuity: TaskContinuity | None = None
    clarity: TaskClarity | None = None
    risk: TaskRisk | None = None
    context: str | None = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str | None) -> str | None:
        """Ensure title is not empty after stripping if provided."""
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty or whitespace-only")
        return v


class TaskResponse(BaseModel):
    """Schema for task response."""

    id: UUID
    project_id: UUID
    title: str
    status: str
    dependencies: list[UUID]
    size: TaskSize
    energy: TaskEnergy
    continuity: TaskContinuity
    clarity: TaskClarity
    risk: TaskRisk
    context: str
    date_created: datetime
    date_updated: datetime

    model_config = {"from_attributes": True}
