"""FastAPI routers for Projects and Tasks API."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from ai_life_backend.projects.api.schemas import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)
from ai_life_backend.projects.repository.in_memory_project_repository import (
    InMemoryProjectRepository,
)
from ai_life_backend.projects.repository.in_memory_task_repository import (
    InMemoryTaskRepository,
)
from ai_life_backend.projects.services.dag_validator import (
    DagValidator,
    CycleDetectedError,
)

# Temporary in-memory storage for MVP
# TODO: Replace with proper DI and PostgreSQL repos once migrations are ready
_project_repo = InMemoryProjectRepository()
_task_repo = InMemoryTaskRepository()
_dag_validator = DagValidator()


def get_project_repository() -> InMemoryProjectRepository:
    """Dependency for project repository."""
    return _project_repo


def get_task_repository() -> InMemoryTaskRepository:
    """Dependency for task repository."""
    return _task_repo


def get_dag_validator() -> DagValidator:
    """Dependency for DAG validator."""
    return _dag_validator


ProjectRepoDep = Annotated[InMemoryProjectRepository, Depends(get_project_repository)]
TaskRepoDep = Annotated[InMemoryTaskRepository, Depends(get_task_repository)]
DagValidatorDep = Annotated[DagValidator, Depends(get_dag_validator)]

# Projects router
projects_router = APIRouter(prefix="/projects", tags=["projects"])


@projects_router.post("", response_model=ProjectResponse, status_code=201)
async def create_project(
    request: ProjectCreate,
    repo: ProjectRepoDep,
    validator: DagValidatorDep,
) -> ProjectResponse:
    """Create a new project."""
    try:
        # Validate dependencies form DAG if provided
        if request.dependencies:
            # Build dependency graph including the new project
            all_projects = await repo.list_all()
            graph = {p.id: list(p.dependencies) for p in all_projects}
            # Add new project's dependencies to graph for validation
            # (using a temporary ID for validation)
            from uuid import uuid4

            temp_id = uuid4()
            graph[temp_id] = request.dependencies
            validator.validate(graph)

        project = await repo.create(
            goal_id=request.goal_id,
            title=request.title,
            status=request.status,
            priority=request.priority,
            scope=request.scope,
            risk=request.risk,
            tags=request.tags,
            dependencies=request.dependencies,
        )
        return ProjectResponse.model_validate(project)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    except CycleDetectedError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@projects_router.get("", response_model=list[ProjectResponse])
async def list_projects(repo: ProjectRepoDep) -> list[ProjectResponse]:
    """List all projects."""
    projects = await repo.list_all()
    return [ProjectResponse.model_validate(p) for p in projects]


@projects_router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: UUID, repo: ProjectRepoDep) -> ProjectResponse:
    """Get a specific project by ID."""
    project = await repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectResponse.model_validate(project)


@projects_router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: UUID,
    request: ProjectUpdate,
    repo: ProjectRepoDep,
    validator: DagValidatorDep,
) -> ProjectResponse:
    """Update a project."""
    try:
        # Validate dependencies if being updated
        if request.dependencies is not None:
            all_projects = await repo.list_all()
            graph = {
                p.id: (
                    list(request.dependencies) if p.id == project_id else list(p.dependencies)
                )
                for p in all_projects
            }
            validator.validate(graph)

        project = await repo.update(
            project_id=project_id,
            title=request.title,
            status=request.status,
            priority=request.priority,
            scope=request.scope,
            risk=request.risk,
            tags=request.tags,
            dependencies=request.dependencies,
        )
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return ProjectResponse.model_validate(project)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    except CycleDetectedError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@projects_router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: UUID, repo: ProjectRepoDep) -> None:
    """Delete a project."""
    deleted = await repo.delete(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")


# Tasks router
tasks_router = APIRouter(prefix="/tasks", tags=["tasks"])


@tasks_router.post("", response_model=TaskResponse, status_code=201)
async def create_task(
    request: TaskCreate,
    repo: TaskRepoDep,
    validator: DagValidatorDep,
) -> TaskResponse:
    """Create a new task."""
    try:
        # Validate dependencies form DAG if provided
        if request.dependencies:
            # Get all tasks for the same project
            project_tasks = await repo.list_by_project(request.project_id)
            graph = {t.id: list(t.dependencies) for t in project_tasks}
            # Add new task's dependencies to graph for validation
            from uuid import uuid4

            temp_id = uuid4()
            graph[temp_id] = request.dependencies

            # Validate that dependencies are within the same project
            for dep_id in request.dependencies:
                dep_task = await repo.get_by_id(dep_id)
                if not dep_task:
                    raise ValueError(f"Dependency task {dep_id} not found")
                if dep_task.project_id != request.project_id:
                    raise ValueError("Task dependencies must be within the same project")

            validator.validate(graph)

        task = await repo.create(
            project_id=request.project_id,
            title=request.title,
            status=request.status,
            dependencies=request.dependencies,
            size=request.size,
            energy=request.energy,
            continuity=request.continuity,
            clarity=request.clarity,
            risk=request.risk,
            context=request.context,
        )
        return TaskResponse.model_validate(task)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    except CycleDetectedError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@tasks_router.get("", response_model=list[TaskResponse])
async def list_tasks(repo: TaskRepoDep) -> list[TaskResponse]:
    """List all tasks."""
    tasks = await repo.list_all()
    return [TaskResponse.model_validate(t) for t in tasks]


@tasks_router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: UUID, repo: TaskRepoDep) -> TaskResponse:
    """Get a specific task by ID."""
    task = await repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse.model_validate(task)


@tasks_router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    request: TaskUpdate,
    repo: TaskRepoDep,
    validator: DagValidatorDep,
) -> TaskResponse:
    """Update a task."""
    try:
        # Get existing task to check project_id
        existing_task = await repo.get_by_id(task_id)
        if not existing_task:
            raise HTTPException(status_code=404, detail="Task not found")

        # Validate dependencies if being updated
        if request.dependencies is not None:
            # Validate dependencies are within same project
            for dep_id in request.dependencies:
                dep_task = await repo.get_by_id(dep_id)
                if not dep_task:
                    raise ValueError(f"Dependency task {dep_id} not found")
                if dep_task.project_id != existing_task.project_id:
                    raise ValueError("Task dependencies must be within the same project")

            # Validate DAG
            project_tasks = await repo.list_by_project(existing_task.project_id)
            graph = {
                t.id: (
                    list(request.dependencies) if t.id == task_id else list(t.dependencies)
                )
                for t in project_tasks
            }
            validator.validate(graph)

        task = await repo.update(
            task_id=task_id,
            title=request.title,
            status=request.status,
            dependencies=request.dependencies,
            size=request.size,
            energy=request.energy,
            continuity=request.continuity,
            clarity=request.clarity,
            risk=request.risk,
            context=request.context,
        )
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return TaskResponse.model_validate(task)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    except CycleDetectedError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@tasks_router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: UUID, repo: TaskRepoDep) -> None:
    """Delete a task."""
    deleted = await repo.delete(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
