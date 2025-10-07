"""In-memory implementation of Project repository for MVP."""

from datetime import UTC, datetime
from uuid import UUID, uuid4

from ai_life_backend.projects.domain.project import Project, ProjectPriority, ProjectRisk


class InMemoryProjectRepository:
    """In-memory implementation of ProjectRepository.

    Note: This is a temporary implementation for MVP.
    Will be replaced with PostgreSQL repository once migrations are in place.
    """

    def __init__(self) -> None:
        """Initialize empty repository."""
        self._projects: dict[UUID, Project] = {}

    async def create(
        self,
        goal_id: UUID | None,
        title: str,
        status: str,
        priority: ProjectPriority,
        scope: str,
        risk: ProjectRisk,
        tags: list[str],
        dependencies: list[UUID],
    ) -> Project:
        """Create a new project."""
        now = datetime.now(UTC)
        project = Project(
            id=uuid4(),
            goal_id=goal_id,
            title=title,
            status=status,
            priority=priority,
            scope=scope,
            risk=risk,
            tags=tags,
            dependencies=dependencies,
            date_created=now,
            date_updated=now,
        )
        self._projects[project.id] = project
        return project

    async def get_by_id(self, project_id: UUID) -> Project | None:
        """Retrieve project by ID."""
        return self._projects.get(project_id)

    async def list_all(self) -> list[Project]:
        """List all projects, sorted by date_created DESC."""
        return sorted(
            self._projects.values(),
            key=lambda p: p.date_created,
            reverse=True,
        )

    async def list_by_goal(self, goal_id: UUID) -> list[Project]:
        """List projects for a specific goal."""
        return [p for p in self._projects.values() if p.goal_id == goal_id]

    async def update(
        self,
        project_id: UUID,
        title: str | None = None,
        status: str | None = None,
        priority: ProjectPriority | None = None,
        scope: str | None = None,
        risk: ProjectRisk | None = None,
        tags: list[str] | None = None,
        dependencies: list[UUID] | None = None,
    ) -> Project | None:
        """Update project fields."""
        project = self._projects.get(project_id)
        if not project:
            return None

        # Create updated project (immutable)
        updated = Project(
            id=project.id,
            goal_id=project.goal_id,
            title=title if title is not None else project.title,
            status=status if status is not None else project.status,
            priority=priority if priority is not None else project.priority,
            scope=scope if scope is not None else project.scope,
            risk=risk if risk is not None else project.risk,
            tags=tags if tags is not None else project.tags,
            dependencies=dependencies if dependencies is not None else project.dependencies,
            date_created=project.date_created,
            date_updated=datetime.now(UTC),
        )
        self._projects[project_id] = updated
        return updated

    async def delete(self, project_id: UUID) -> bool:
        """Delete a project."""
        if project_id in self._projects:
            del self._projects[project_id]
            return True
        return False
