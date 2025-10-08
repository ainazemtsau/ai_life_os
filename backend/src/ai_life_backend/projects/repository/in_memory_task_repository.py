"""In-memory implementation of Task repository for MVP."""

from datetime import UTC, datetime
from uuid import UUID, uuid4

from ai_life_backend.projects.domain.task import (
    Task,
    TaskSize,
    TaskEnergy,
    TaskContinuity,
    TaskClarity,
    TaskRisk,
)


class InMemoryTaskRepository:
    """In-memory implementation of TaskRepository.

    Note: This is a temporary implementation for MVP.
    Will be replaced with PostgreSQL repository once migrations are in place.
    """

    def __init__(self) -> None:
        """Initialize empty repository."""
        self._tasks: dict[UUID, Task] = {}

    async def create(
        self,
        project_id: UUID,
        title: str,
        status: str,
        dependencies: list[UUID],
        size: TaskSize,
        energy: TaskEnergy,
        continuity: TaskContinuity,
        clarity: TaskClarity,
        risk: TaskRisk,
        context: str,
    ) -> Task:
        """Create a new task."""
        now = datetime.now(UTC)
        task = Task(
            id=uuid4(),
            project_id=project_id,
            title=title,
            status=status,
            dependencies=dependencies,
            size=size,
            energy=energy,
            continuity=continuity,
            clarity=clarity,
            risk=risk,
            context=context,
            date_created=now,
            date_updated=now,
        )
        self._tasks[task.id] = task
        return task

    async def get_by_id(self, task_id: UUID) -> Task | None:
        """Retrieve task by ID."""
        return self._tasks.get(task_id)

    async def list_all(self) -> list[Task]:
        """List all tasks, sorted by date_created DESC."""
        return sorted(
            self._tasks.values(),
            key=lambda t: t.date_created,
            reverse=True,
        )

    async def list_by_project(self, project_id: UUID) -> list[Task]:
        """List tasks for a specific project."""
        return [t for t in self._tasks.values() if t.project_id == project_id]

    async def update(
        self,
        task_id: UUID,
        title: str | None = None,
        status: str | None = None,
        dependencies: list[UUID] | None = None,
        size: TaskSize | None = None,
        energy: TaskEnergy | None = None,
        continuity: TaskContinuity | None = None,
        clarity: TaskClarity | None = None,
        risk: TaskRisk | None = None,
        context: str | None = None,
    ) -> Task | None:
        """Update task fields."""
        task = self._tasks.get(task_id)
        if not task:
            return None

        # Create updated task (immutable)
        updated = Task(
            id=task.id,
            project_id=task.project_id,
            title=title if title is not None else task.title,
            status=status if status is not None else task.status,
            dependencies=dependencies if dependencies is not None else task.dependencies,
            size=size if size is not None else task.size,
            energy=energy if energy is not None else task.energy,
            continuity=continuity if continuity is not None else task.continuity,
            clarity=clarity if clarity is not None else task.clarity,
            risk=risk if risk is not None else task.risk,
            context=context if context is not None else task.context,
            date_created=task.date_created,
            date_updated=datetime.now(UTC),
        )
        self._tasks[task_id] = updated
        return updated

    async def delete(self, task_id: UUID) -> bool:
        """Delete a task."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
