# Public Surface — backend.goals
Version: 0.1.0

## Purpose
Goals module (MVP). CRUD + filtering. **Same-process** consumers use a typed **in-process port**; **cross-process/external** consumers use **HTTP (OpenAPI)**.

## In-process Public Port (same process)
> Import only from: `ai_life_backend.goals.public` (other internals are private).

### DTOs
- `GoalDTO` — `{ id: UUID, title: str, is_done: bool, date_created: datetime, date_updated: datetime }`

### Functions (read-only)
- `async def list_goals(status: Literal['all','active','done']='all') -> list[GoalDTO]`
- `async def get_goal(id: UUID) -> GoalDTO | None`

> Rationale: read operations are safe via port; **mutations go through HTTP** to enforce validation/side-effects consistently.

### Usage (same process)
```py
from ai_life_backend.goals.public import list_goals, GoalDTO

async def build_report():
    items: list[GoalDTO] = await list_goals(status="active")
    # use DTOs; do not access DB/ORM of goals module
HTTP Contract (cross-process / external)
Contract (single source): backend/src/ai_life_backend/contracts/goals_openapi.yaml (OpenAPI 3.1)

GET /api/goals (?status=active|done)

POST /api/goals

GET /api/goals/{id}

PATCH /api/goals/{id}

DELETE /api/goals/{id}

Errors follow RFC 7807 Problem schema (components.schemas.Problem).

Versioning
SemVer bump when public surface changes (in-process port or OpenAPI).

Conventional Commits.

Notes
No deep imports into module internals; DB is private.

If a capability is missing here → raise CDC/handoff request (don’t guess).