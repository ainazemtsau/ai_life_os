# Public API — backend.milestones
Version: 0.2.0

## Overview
Milestones domain module. Provides CRUD operations and HTTP API for Milestones linked to Goals.

A Milestone is a verifiable step toward achieving a Goal. Each milestone has:
- Goal association (required foreign key)
- Title and demo criterion for verification
- Optional due date
- Unified status (todo/doing/done/blocked)
- Blocking flag to indicate if it blocks other work

## Exports

### HTTP API (cross-process)
- `milestones_router: APIRouter` — FastAPI router for HTTP endpoints (include with prefix="/api")

### In-Process API (same-process read-only)
- `MilestoneDTO` — Read-only data transfer object
- `list_milestones() -> list[MilestoneDTO]` — List all milestones
- `list_milestones_by_goal(goal_id: UUID) -> list[MilestoneDTO]` — List milestones for a specific goal
- `get_milestone(id: UUID) -> MilestoneDTO | None` — Get milestone by ID

### RFC 7807 Support
- `RFC7807_MIME` — MIME type constant for Problem Details
- `ProblemDict` — TypedDict for Problem Details structure

## Types

### Domain Entity
```python
@dataclass(frozen=True)
class Milestone:
    id: UUID
    goal_id: UUID
    title: str
    due: datetime | None
    status: str  # "todo" | "doing" | "done" | "blocked"
    demo_criterion: str
    blocking: bool
    date_created: datetime
    date_updated: datetime
```

### DTO (In-Process)
```python
@dataclass(frozen=True)
class MilestoneDTO:
    id: UUID
    goal_id: UUID
    title: str
    due: datetime | None
    status: str
    demo_criterion: str
    blocking: bool
    date_created: datetime
    date_updated: datetime
```

### HTTP Contract
OpenAPI 3.1: `backend/src/ai_life_backend/contracts/milestones_openapi.yaml`

**Endpoints:**
- `POST /api/milestones` — Create milestone (201)
- `GET /api/milestones` — List all milestones (200)
- `GET /api/milestones/{id}` — Get milestone by ID (200, 404)
- `PATCH /api/milestones/{id}` — Update milestone (200, 404, 422)
- `DELETE /api/milestones/{id}` — Delete milestone (204, 404)

**Status Enum:** `"todo" | "doing" | "done" | "blocked"`

**Error Responses:** RFC 7807 Problem Details

## Usage

### HTTP API
```python
from fastapi import FastAPI
from ai_life_backend.milestones.public import milestones_router

app = FastAPI()
app.include_router(milestones_router, prefix="/api")
```

### In-Process API
```python
from ai_life_backend.milestones.public import list_milestones, get_milestone

# List all milestones
milestones = await list_milestones()

# List milestones for a specific goal
goal_milestones = await list_milestones_by_goal(goal_id)

# Get single milestone
milestone = await get_milestone(milestone_id)
```

## Dependencies
- `backend.core` — Cross-cutting utilities (RFC 7807, timestamps)
- `backend.goals` — Goal association (foreign key constraint)

## Versioning
- 0.2.0 — Full CRUD implementation with HTTP API and in-process read-only port
- 0.1.0 — Initial stub
