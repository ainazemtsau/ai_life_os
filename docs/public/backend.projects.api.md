# Public API — backend.projects
Version: 0.1.0

## Overview
Projects and Tasks domain module. Provides CRUD operations, dependency management with DAG (Directed Acyclic Graph) validation, and HTTP API for Projects and Tasks entities.

**Key features**:
- CRUD operations for Projects and Tasks
- DAG validation for dependencies (prevents cycles)
- Task dependencies scoped to same Project
- Project dependencies scoped to same Goal
- Unified status set: todo/doing/done/blocked
- Rich enums for task properties (size, energy, continuity, clarity, risk)

## Exports

### API Routers
- `projects_router` — FastAPI router for `/api/projects` endpoints
- `tasks_router` — FastAPI router for `/api/tasks` endpoints

### Domain Entities
- `Project` — Immutable project entity with dependencies
- `Task` — Immutable task entity with dependencies
- `ProjectPriority` — Enum (P0, P1, P2, P3)
- `ProjectRisk` — Enum (green, yellow, red)
- `TaskSize` — Enum (XS, S, M, L, XL)
- `TaskEnergy` — Enum (Deep, Focus, Light)
- `TaskContinuity` — Enum (chain, linked, puzzle)
- `TaskClarity` — Enum (clear, cloudy, unknown)
- `TaskRisk` — Enum (green, yellow, red)

### In-Process Protocols (Read-only)
- `ProjectReader` — Protocol for querying projects
- `TaskReader` — Protocol for querying tasks

## Types
Contract: backend/src/ai_life_backend/contracts/projects_openapi.yaml
In-process: backend/src/ai_life_backend/contracts/projects_protocols.py

## HTTP Endpoints

### Projects
- `POST /api/projects` — Create project (validates DAG if dependencies provided)
- `GET /api/projects` — List all projects (sorted by date_created DESC)
- `GET /api/projects/{id}` — Get project by ID
- `PUT /api/projects/{id}` — Update project (validates DAG if dependencies changed)
- `DELETE /api/projects/{id}` — Delete project

### Tasks
- `POST /api/tasks` — Create task (validates DAG and project scope)
- `GET /api/tasks` — List all tasks (sorted by date_created DESC)
- `GET /api/tasks/{id}` — Get task by ID
- `PUT /api/tasks/{id}` — Update task (validates DAG and project scope)
- `DELETE /api/tasks/{id}` — Delete task

## Usage

### Importing the module
```python
# Import public API
from ai_life_backend.projects.public import (
    projects_router,
    tasks_router,
    Project,
    Task,
    ProjectPriority,
    TaskSize,
)

# Import protocols for read-only access
from ai_life_backend.contracts.projects_protocols import ProjectReader, TaskReader
```

### Using the routers (in main FastAPI app)
```python
from fastapi import FastAPI
from ai_life_backend.projects.public import projects_router, tasks_router

app = FastAPI()
app.include_router(projects_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")
```

## Implementation Notes

### MVP Limitations
- **In-memory storage**: Current implementation uses in-memory repositories for rapid MVP development
- **Database migration required**: PostgreSQL schema needs to be created (see handoff.md)
- **No authentication**: Security is marked as `[]` (no auth) for MVP
- **No pagination**: All list endpoints return full collections

### Future Enhancements
- Replace in-memory repos with PostgreSQL implementations
- Add pagination for list endpoints
- Add filtering by status, project, goal
- Add bulk operations
- Add dependency visualization endpoint

## Versioning
- 0.1.0 — Initial implementation with in-memory storage, DAG validation, full CRUD
