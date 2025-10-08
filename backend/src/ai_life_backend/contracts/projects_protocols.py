"""Public contract protocols — backend.projects
Version: 0.1.0
Define typing.Protocol interfaces here for cross-module use.
"""
from typing import Protocol, runtime_checkable
from uuid import UUID

from ai_life_backend.projects.domain.project import Project
from ai_life_backend.projects.domain.task import Task


@runtime_checkable
class ProjectReader(Protocol):
    """Read-only query port for Projects."""

    async def get_by_id(self, project_id: UUID) -> Project | None:
        """Retrieve project by ID."""
        ...

    async def list_all(self) -> list[Project]:
        """List all projects."""
        ...

    async def list_by_goal(self, goal_id: UUID) -> list[Project]:
        """List projects for a specific goal."""
        ...


@runtime_checkable
class TaskReader(Protocol):
    """Read-only query port for Tasks."""

    async def get_by_id(self, task_id: UUID) -> Task | None:
        """Retrieve task by ID."""
        ...

    async def list_all(self) -> list[Task]:
        """List all tasks."""
        ...

    async def list_by_project(self, project_id: UUID) -> list[Task]:
        """List tasks for a specific project."""
        ...
