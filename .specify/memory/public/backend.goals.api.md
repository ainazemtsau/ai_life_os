# Public API — backend.goals
Version: 0.1.0

## Overview
REST API for managing personal goals (MVP). Provides CRUD operations, filtering by completion status, and server-side persistence to PostgreSQL. This is the foundational feature module that establishes patterns for future backend features.

## Exports
### HTTP Endpoints (via FastAPI router)
- `GET /api/goals` - List all goals with optional `?status=active|done` filter
- `POST /api/goals` - Create new goal from `{title: string}`
- `GET /api/goals/{id}` - Retrieve single goal by UUID
- `PATCH /api/goals/{id}` - Update goal (title and/or is_done)
- `DELETE /api/goals/{id}` - Permanently delete goal

All endpoints return JSON responses following OpenAPI 3.1 specification.

## Types
Contract: `backend/src/ai_life_backend/contracts/goals_contracts.py` (Protocol-based repository interface)

Additional contract: OpenAPI spec will be generated at `backend/src/ai_life_backend/contracts/goals_openapi.yaml` by FastAPI

**Key domain types:**
- `Goal` - Immutable dataclass (id: UUID, title: str, is_done: bool, date_created: datetime, date_updated: datetime)
- `GoalRepository` - Protocol defining data access methods (create, get_by_id, list_all, list_by_status, update, delete)

**Request/Response schemas (Pydantic):**
- `GoalCreateRequest` - {title: str (1-255 chars)}
- `GoalUpdateRequest` - {title?: str, is_done?: bool}
- `GoalResponse` - Full goal representation with timestamps
- `GoalListResponse` - {goals: GoalResponse[]}
- `ErrorResponse` - {detail: str, type?: str, status?: int}

## Usage
```py
# In main FastAPI app
from ai_life_backend.goals.public import goals_router

app.include_router(goals_router, prefix="/api")
```

## Stability
- exports: **experimental** (v0.1.0 - first release, API may evolve)
- types: **experimental** (domain model and protocols may refine)

## Dependencies
- No module dependencies (foundational feature)
- External: FastAPI, SQLAlchemy 2.0, asyncpg, Pydantic v2

## Versioning
- **0.1.0** - Initial MVP release
- SemVer policy: MAJOR for breaking API changes, MINOR for new endpoints/optional fields, PATCH for bug fixes

## Notes
- All operations async (asyncio/asyncpg)
- Validation at Pydantic layer + PostgreSQL constraints
- Last-write-wins for concurrent modifications (no optimistic locking in MVP)
- Single-user scope (no auth/multi-tenancy)
