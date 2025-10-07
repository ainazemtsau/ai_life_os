# Module Tasks: backend.goals for Feature 001-goals-management-mvp

**Inputs**:
- Global constitution: `.specify/memory/constitution.md`
- Module manifest: `.specify/memory/public/backend.goals.api.md`
- Module contract: `backend/src/ai_life_backend/contracts/goals_contracts.py`
- Global tasks: `specs/001-goals-management-mvp/tasks.md`
- Design docs: `plan.md`, `data-model.md`, `research.md`, `quickstart.md`

**Scope**:
- Work ONLY inside `backend/src/ai_life_backend/goals/**` and `backend/tests/goals/**`
- Dependencies: None (foundational module, uses `"-"`)
- If cross-module changes needed → create handoff note

**Allowed Directories** (from registry):
- `backend/src/ai_life_backend/goals/**`
- `backend/tests/goals/**`

---

## Phase A: Setup & Dependencies

### MT001 Add backend dependencies via uv

**Global Task**: T002

**Description**: Install FastAPI, SQLAlchemy 2.0, asyncpg, Pydantic v2, Alembic via uv.

**File**: `backend/pyproject.toml`

**Dependencies**: None

**Steps**:
1. Navigate to `backend/` directory
2. Run uv commands:
   ```bash
   cd backend
   uv add "fastapi[standard]>=0.115.0"
   uv add "sqlalchemy[asyncio]>=2.0.0"
   uv add "asyncpg>=0.29.0"
   uv add "alembic>=1.13.0"
   uv add "pydantic>=2.0.0"
   uv add "pydantic-settings>=2.0.0"
   uv sync
   ```

**Acceptance Criteria**:
- [ ] `pyproject.toml` dependencies section updated
- [ ] `uv.lock` regenerated
- [ ] `uv sync` completes without errors
- [ ] Can import: `import fastapi, sqlalchemy, asyncpg, alembic, pydantic`

**Validation**:
```bash
cd backend && uv run python -c "import fastapi, sqlalchemy, asyncpg, alembic, pydantic; print('✓ All imports successful')"
```

---

### MT002 Initialize Alembic for database migrations

**Global Task**: T004

**Description**: Set up Alembic migration framework with async support.

**Files**:
- `backend/alembic.ini`
- `backend/alembic/env.py`
- `backend/alembic/versions/` (directory)

**Dependencies**: MT001

**Steps**:
1. Initialize Alembic:
   ```bash
   cd backend
   uv run alembic init alembic
   ```

2. Update `alembic.ini` - set sqlalchemy.url:
   ```ini
   sqlalchemy.url = postgresql+asyncpg://postgres:postgres@localhost:5432/ai_life_os
   ```

3. Update `alembic/env.py` for async:
   ```python
   from logging.config import fileConfig
   from sqlalchemy import pool
   from sqlalchemy.engine import Connection
   from sqlalchemy.ext.asyncio import async_engine_from_config
   import asyncio

   # ... existing imports ...

   config = context.config

   # Override sqlalchemy.url from environment if available
   import os
   if os.getenv("DATABASE_URL"):
       config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

   # ... existing code ...

   async def run_async_migrations() -> None:
       connectable = async_engine_from_config(
           config.get_section(config.config_ini_section, {}),
           prefix="sqlalchemy.",
           poolclass=pool.NullPool,
       )

       async with connectable.connect() as connection:
           await connection.run_sync(do_run_migrations)

       await connectable.dispose()

   def run_migrations_online() -> None:
       asyncio.run(run_async_migrations())
   ```

**Acceptance Criteria**:
- [ ] `alembic.ini` exists with correct database URL
- [ ] `alembic/env.py` configured for async migrations
- [ ] `alembic/versions/` directory created
- [ ] Can run: `uv run alembic current`

**Validation**:
```bash
cd backend && uv run alembic current
```

---

### MT003 Create module directory structure

**Description**: Set up backend.goals module skeleton with all required subdirectories.

**Directories to create**:
```
backend/src/ai_life_backend/goals/
├── __init__.py
├── domain/
│   └── __init__.py
├── repository/
│   └── __init__.py
├── services/
│   └── __init__.py
├── api/
│   └── __init__.py
└── public/
    └── __init__.py

backend/tests/goals/
├── __init__.py
├── contract/
│   └── __init__.py
├── integration/
│   └── __init__.py
└── unit/
    └── __init__.py
```

**Dependencies**: None

**Steps**:
```bash
cd backend
mkdir -p src/ai_life_backend/goals/{domain,repository,services,api,public}
mkdir -p tests/goals/{contract,integration,unit}
touch src/ai_life_backend/goals/__init__.py
touch src/ai_life_backend/goals/{domain,repository,services,api,public}/__init__.py
touch tests/goals/__init__.py
touch tests/goals/{contract,integration,unit}/__init__.py
```

**Acceptance Criteria**:
- [ ] All directories exist
- [ ] All `__init__.py` files created

---

## Phase B: Tests First (TDD - MUST FAIL before implementation)

### MT010 [P] Create Goal domain entity

**Global Task**: T010

**Description**: Implement immutable Goal dataclass with validation.

**File**: `backend/src/ai_life_backend/goals/domain/goal.py`

**Dependencies**: MT003

**Steps**:
1. Create `backend/src/ai_life_backend/goals/domain/goal.py`:
```python
"""Goal domain entity."""
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class Goal:
    """
    Immutable domain entity representing a personal goal.

    Attributes:
        id: Unique identifier (UUID)
        title: Goal description (1-255 chars, non-empty after trim)
        is_done: Completion status
        date_created: Creation timestamp (UTC)
        date_updated: Last modification timestamp (UTC)
    """

    id: UUID
    title: str
    is_done: bool
    date_created: datetime
    date_updated: datetime

    def __post_init__(self) -> None:
        """Validate domain invariants."""
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty or whitespace-only")
        if len(self.title) > 255:
            raise ValueError("Title cannot exceed 255 characters")
```

2. Export from `backend/src/ai_life_backend/goals/domain/__init__.py`:
```python
"""Domain entities for goals module."""
from .goal import Goal

__all__ = ["Goal"]
```

**Acceptance Criteria**:
- [ ] Goal dataclass defined with `frozen=True`
- [ ] All 5 fields typed: id, title, is_done, date_created, date_updated
- [ ] `__post_init__` validates title (non-empty, ≤255 chars)
- [ ] Raises ValueError for invalid data
- [ ] Exported from domain/__init__.py

**Test** (create after implementation):
```bash
cd backend && uv run python -c "
from ai_life_backend.goals.domain import Goal
from uuid import uuid4
from datetime import datetime, timezone

# Valid goal
g = Goal(id=uuid4(), title='Test', is_done=False, date_created=datetime.now(timezone.utc), date_updated=datetime.now(timezone.utc))
print('✓ Valid goal created')

# Invalid: empty title
try:
    Goal(id=uuid4(), title='  ', is_done=False, date_created=datetime.now(timezone.utc), date_updated=datetime.now(timezone.utc))
    print('✗ Should have raised ValueError')
except ValueError as e:
    print('✓ Empty title rejected:', e)
"
```

---

### MT011 Create PostgreSQL migration for goals table

**Global Task**: T012

**Description**: Generate Alembic migration to create goals table with indexes.

**File**: `backend/alembic/versions/001_create_goals_table.py` (filename will be auto-generated)

**Dependencies**: MT002, MT010

**Steps**:
1. Generate migration:
   ```bash
   cd backend
   uv run alembic revision -m "create goals table"
   ```

2. Edit the generated file in `alembic/versions/`:
```python
"""create goals table

Revision ID: 001
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'goals',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('is_done', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('date_created', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('date_updated', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.CheckConstraint("LENGTH(TRIM(title)) > 0", name='check_title_not_empty')
    )

    # Indexes for filtering and sorting
    op.create_index('idx_goals_is_done', 'goals', ['is_done'])
    op.create_index('idx_goals_date_updated', 'goals', [sa.text('date_updated DESC')])


def downgrade() -> None:
    op.drop_index('idx_goals_date_updated', table_name='goals')
    op.drop_index('idx_goals_is_done', table_name='goals')
    op.drop_table('goals')
```

**Acceptance Criteria**:
- [ ] Migration file created in `alembic/versions/`
- [ ] `upgrade()` creates goals table with UUID primary key
- [ ] Columns: id, title (VARCHAR 255), is_done (BOOLEAN), date_created (TIMESTAMPTZ), date_updated (TIMESTAMPTZ)
- [ ] CHECK constraint: `LENGTH(TRIM(title)) > 0`
- [ ] Indexes: idx_goals_is_done, idx_goals_date_updated DESC
- [ ] `downgrade()` drops table and indexes

**Validation**:
```bash
cd backend
docker-compose up -d postgres
uv run alembic upgrade head
uv run alembic current  # Should show migration applied
```

**Verification Query**:
```sql
-- Connect to database and run:
\d goals
-- Should show table structure with indexes
```

---

### MT012 Implement PostgresGoalRepository

**Global Task**: T013

**Description**: Implement GoalRepository Protocol using SQLAlchemy + asyncpg.

**File**: `backend/src/ai_life_backend/goals/repository/postgres_goal_repository.py`

**Dependencies**: MT010, MT011

**Steps** (abbreviated - full implementation is ~200 lines):

1. Create SQLAlchemy model mapping:
```python
"""PostgreSQL implementation of GoalRepository."""
from typing import cast
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import Table, Column, String, Boolean, DateTime, MetaData, select, update, delete
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.asyncio import AsyncEngine
from ai_life_backend.goals.domain import Goal

metadata = MetaData()

goals_table = Table(
    'goals',
    metadata,
    Column('id', PG_UUID(as_uuid=True), primary_key=True),
    Column('title', String(255), nullable=False),
    Column('is_done', Boolean, nullable=False),
    Column('date_created', DateTime(timezone=True), nullable=False),
    Column('date_updated', DateTime(timezone=True), nullable=False),
)


class PostgresGoalRepository:
    """PostgreSQL implementation of GoalRepository Protocol."""

    def __init__(self, engine: AsyncEngine) -> None:
        self._engine = engine

    async def create(self, title: str) -> Goal:
        """Create new goal."""
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        if len(title) > 255:
            raise ValueError("Title cannot exceed 255 characters")

        async with self._engine.begin() as conn:
            result = await conn.execute(
                goals_table.insert().values(title=title).returning(goals_table)
            )
            row = result.one()
            return Goal(
                id=row.id,
                title=row.title,
                is_done=row.is_done,
                date_created=row.date_created,
                date_updated=row.date_updated,
            )

    async def get_by_id(self, goal_id: UUID) -> Goal | None:
        """Retrieve goal by ID."""
        async with self._engine.connect() as conn:
            result = await conn.execute(
                select(goals_table).where(goals_table.c.id == goal_id)
            )
            row = result.one_or_none()
            if not row:
                return None
            return Goal(
                id=row.id,
                title=row.title,
                is_done=row.is_done,
                date_created=row.date_created,
                date_updated=row.date_updated,
            )

    async def list_all(self) -> list[Goal]:
        """List all goals, sorted by is_done ASC, date_updated DESC."""
        async with self._engine.connect() as conn:
            result = await conn.execute(
                select(goals_table).order_by(goals_table.c.is_done, goals_table.c.date_updated.desc())
            )
            return [
                Goal(id=row.id, title=row.title, is_done=row.is_done, date_created=row.date_created, date_updated=row.date_updated)
                for row in result.all()
            ]

    # ... implement list_by_status, update, delete similarly
```

2. Export from `backend/src/ai_life_backend/goals/repository/__init__.py`

**Acceptance Criteria**:
- [ ] All 6 Protocol methods implemented
- [ ] Uses SQLAlchemy async API
- [ ] Proper error handling (ValueError for validation)
- [ ] Returns domain Goal entities, not DB rows
- [ ] Uses `async with` for connection management

**Test**:
Create `backend/tests/goals/integration/test_postgres_goal_repository.py` (run after implementation validates it works)

---

### MT020-MT024 [P] Contract Tests (5 endpoints)

**Global Tasks**: T040-T044

**Description**: Create contract tests for all 5 API endpoints that validate OpenAPI schema compliance.

**Files**:
- `backend/tests/goals/contract/test_goals_api_contract.py`

**Dependencies**: MT011 (database must exist)

**Combined Test File** (all 5 endpoints):
```python
"""Contract tests for Goals API - validate OpenAPI compliance."""
import pytest
from fastapi.testclient import TestClient
from uuid import uuid4


@pytest.fixture
def client():
    """Create test client for goals API."""
    from ai_life_backend.app import app
    return TestClient(app)


class TestGoalsAPIContract:
    """Contract tests validating OpenAPI schema compliance."""

    def test_post_goals_validates_schema(self, client):
        """T040: POST /api/goals validates request/response schema."""
        # Valid request
        response = client.post("/api/goals", json={"title": "Test Goal"})
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["title"] == "Test Goal"
        assert data["is_done"] is False
        assert "date_created" in data
        assert "date_updated" in data

        # Invalid: missing title
        response = client.post("/api/goals", json={})
        assert response.status_code == 422

        # Invalid: empty title
        response = client.post("/api/goals", json={"title": "  "})
        assert response.status_code == 422

        # Invalid: title too long
        response = client.post("/api/goals", json={"title": "a" * 256})
        assert response.status_code == 422

    def test_get_goals_returns_list_schema(self, client):
        """T041: GET /api/goals returns GoalListResponse schema."""
        response = client.get("/api/goals")
        assert response.status_code == 200
        data = response.json()
        assert "goals" in data
        assert isinstance(data["goals"], list)

        # Test with filter
        response = client.get("/api/goals?status=active")
        assert response.status_code == 200

        response = client.get("/api/goals?status=done")
        assert response.status_code == 200

        # Invalid filter
        response = client.get("/api/goals?status=invalid")
        assert response.status_code == 422

    def test_get_goal_by_id_validates_uuid(self, client):
        """T042: GET /api/goals/{id} validates UUID parameter."""
        # Invalid UUID format
        response = client.get("/api/goals/not-a-uuid")
        assert response.status_code == 422

        # Valid UUID but not found
        response = client.get(f"/api/goals/{uuid4()}")
        assert response.status_code == 404

    def test_patch_goal_validates_request_body(self, client):
        """T043: PATCH /api/goals/{id} validates request schema."""
        # Create goal first
        create_response = client.post("/api/goals", json={"title": "Original"})
        goal_id = create_response.json()["id"]

        # Valid update: title only
        response = client.patch(f"/api/goals/{goal_id}", json={"title": "Updated"})
        assert response.status_code == 200
        assert response.json()["title"] == "Updated"

        # Valid update: is_done only
        response = client.patch(f"/api/goals/{goal_id}", json={"is_done": True})
        assert response.status_code == 200
        assert response.json()["is_done"] is True

        # Invalid: no fields provided
        response = client.patch(f"/api/goals/{goal_id}", json={})
        assert response.status_code == 422

        # Invalid: empty title
        response = client.patch(f"/api/goals/{goal_id}", json={"title": ""})
        assert response.status_code == 422

    def test_delete_goal_returns_204(self, client):
        """T044: DELETE /api/goals/{id} returns 204 No Content."""
        # Create goal first
        create_response = client.post("/api/goals", json={"title": "To Delete"})
        goal_id = create_response.json()["id"]

        # Delete
        response = client.delete(f"/api/goals/{goal_id}")
        assert response.status_code == 204
        assert response.content == b""

        # Verify deleted
        response = client.get(f"/api/goals/{goal_id}")
        assert response.status_code == 404
```

**Acceptance Criteria**:
- [ ] All 5 tests pass (after implementation)
- [ ] Tests validate request schemas (Pydantic validation)
- [ ] Tests validate response schemas (structure, types)
- [ ] Tests check status codes (201, 200, 204, 404, 422)
- [ ] Tests are marked [P] - can run in parallel

**Validation**:
```bash
cd backend && uv run pytest tests/goals/contract/ -v
# Should FAIL initially (TDD), PASS after implementation
```

---

(Continuing with remaining implementation tasks MT030-MT070...)

## Phase C: Implementation (after tests fail)

### MT030 Define Pydantic schemas

**Global Task**: T015

**File**: `backend/src/ai_life_backend/goals/api/schemas.py`

**Implementation** (abbreviated):
```python
"""Pydantic schemas for Goals API."""
from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime


class GoalCreateRequest(BaseModel):
    """Request schema for creating a goal."""
    title: str = Field(..., min_length=1, max_length=255)

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty or whitespace-only")
        return v


class GoalUpdateRequest(BaseModel):
    """Request schema for updating a goal."""
    title: str | None = Field(None, min_length=1, max_length=255)
    is_done: bool | None = None

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty or whitespace-only")
        return v


class GoalResponse(BaseModel):
    """Response schema for a goal."""
    id: UUID
    title: str
    is_done: bool
    date_created: datetime
    date_updated: datetime

    class Config:
        from_attributes = True


class GoalListResponse(BaseModel):
    """Response schema for list of goals."""
    goals: list[GoalResponse]


class ErrorResponse(BaseModel):
    """Error response schema (RFC 7807)."""
    detail: str
    type: str | None = None
    status: int | None = None
```

---

### MT040 Implement FastAPI router

**Global Task**: T016

**File**: `backend/src/ai_life_backend/goals/api/routes.py`

**Implementation** (abbreviated - ~150 lines full):
```python
"""FastAPI router for Goals API."""
from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from typing import Literal
from .schemas import GoalCreateRequest, GoalUpdateRequest, GoalResponse, GoalListResponse
from ..repository.postgres_goal_repository import PostgresGoalRepository
from ..domain import Goal

router = APIRouter(prefix="/goals", tags=["goals"])


def get_repository() -> PostgresGoalRepository:
    """Dependency injection for repository."""
    from ai_life_backend.database import get_engine
    return PostgresGoalRepository(get_engine())


@router.post("", response_model=GoalResponse, status_code=201)
async def create_goal(
    request: GoalCreateRequest,
    repo: PostgresGoalRepository = Depends(get_repository)
) -> GoalResponse:
    """Create a new goal."""
    try:
        goal = await repo.create(request.title)
        return GoalResponse.model_validate(goal)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("", response_model=GoalListResponse)
async def list_goals(
    status: Literal["active", "done"] | None = Query(None),
    repo: PostgresGoalRepository = Depends(get_repository)
) -> GoalListResponse:
    """List all goals with optional status filter."""
    if status == "active":
        goals = await repo.list_by_status(False)
    elif status == "done":
        goals = await repo.list_by_status(True)
    else:
        goals = await repo.list_all()

    return GoalListResponse(goals=[GoalResponse.model_validate(g) for g in goals])


@router.get("/{goal_id}", response_model=GoalResponse)
async def get_goal(
    goal_id: UUID,
    repo: PostgresGoalRepository = Depends(get_repository)
) -> GoalResponse:
    """Get a single goal by ID."""
    goal = await repo.get_by_id(goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return GoalResponse.model_validate(goal)


@router.patch("/{goal_id}", response_model=GoalResponse)
async def update_goal(
    goal_id: UUID,
    request: GoalUpdateRequest,
    repo: PostgresGoalRepository = Depends(get_repository)
) -> GoalResponse:
    """Update a goal's title and/or completion status."""
    if request.title is None and request.is_done is None:
        raise HTTPException(status_code=422, detail="At least one field must be provided")

    try:
        goal = await repo.update(goal_id, request.title, request.is_done)
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        return GoalResponse.model_validate(goal)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.delete("/{goal_id}", status_code=204)
async def delete_goal(
    goal_id: UUID,
    repo: PostgresGoalRepository = Depends(get_repository)
) -> None:
    """Delete a goal permanently."""
    success = await repo.delete(goal_id)
    if not success:
        raise HTTPException(status_code=404, detail="Goal not found")
```

---

### MT050 Create public facade

**Global Task**: T018

**File**: `backend/src/ai_life_backend/goals/public/__init__.py`

```python
"""Public API for backend.goals module."""
from ..api.routes import router as goals_router

__all__ = ["goals_router"]
```

---

## Phase D: Integration

### MT060 Wire goals router into main app

**Global Task**: T050

**File**: `backend/src/ai_life_backend/app.py`

```python
"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="AI Life OS API",
    description="Goals Management MVP",
    version="0.1.0"
)

# CORS (from infra MT010)
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Include goals router
from ai_life_backend.goals.public import goals_router
app.include_router(goals_router, prefix="/api")
```

---

## Phase E: Docs Sync (MANDATORY)

### MT070 Update manifest and contract

**Global Tasks**: T060, T063

**Steps**:
1. Update `.specify/memory/public/backend.goals.api.md` - verify all exports listed
2. Verify `backend/src/ai_life_backend/contracts/goals_contracts.py` is current
3. Bump SemVer in registry if public API changed (0.1.0 → 0.2.0 if breaking)
4. Run validators:
```bash
python3 .specify/scripts/registry_validate.py
python3 .specify/scripts/manifest_lint.py
```

**Acceptance Criteria**:
- [ ] Manifest lists: goals_router export
- [ ] Contract has: Goal, GoalRepository protocols
- [ ] SemVer bumped if needed
- [ ] Validators pass

---

## Dependencies Graph

```
MT001 (deps) → MT002 (alembic) → MT011 (migration)
MT003 (dirs) → MT010 (Goal entity)
MT010 + MT011 → MT012 (repository)
MT012 → MT030 (schemas) → MT040 (router) → MT050 (public) → MT060 (wire)
MT020-MT024 (contract tests) - can run parallel after MT060
MT070 (docs sync) - final step
```

---

<!-- FANOUT:BEGIN -->
## Global Items (source)

*Do not edit this block manually; run `/fanout-tasks` to refresh.*

- [ ] T002 @module(backend.goals) @prio(P1) Add FastAPI + SQLAlchemy + asyncpg dependencies via uv
- [ ] T004 @module(backend.goals) @prio(P1) Initialize Alembic migrations for goals schema
- [ ] T010 @module(backend.goals) @prio(P1) Define Goal domain entity (dataclass) with validation
- [ ] T011 @module(backend.goals) @prio(P1) Define GoalRepository Protocol interface
- [ ] T012 @module(backend.goals) @prio(P1) Create PostgreSQL migration for goals table + indexes
- [ ] T013 @module(backend.goals) @prio(P1) Implement PostgresGoalRepository with async methods
- [ ] T014 @module(backend.goals) @prio(P2) Define GoalService with business logic orchestration
- [ ] T015 @module(backend.goals) @prio(P1) Define Pydantic request/response schemas
- [ ] T016 @module(backend.goals) @prio(P1) Implement FastAPI router with 5 endpoints
- [ ] T017 @module(backend.goals) @prio(P2) Add error handling middleware for RFC 7807 responses
- [ ] T018 @module(backend.goals) @prio(P1) Create public facade (goals_router export)
- [ ] T040 @module(backend.goals) @prio(P1) Contract test: POST /api/goals validates schema
- [ ] T041 @module(backend.goals) @prio(P1) Contract test: GET /api/goals returns list schema
- [ ] T042 @module(backend.goals) @prio(P1) Contract test: GET /api/goals/{id} validates UUID param
- [ ] T043 @module(backend.goals) @prio(P1) Contract test: PATCH /api/goals/{id} validates request body
- [ ] T044 @module(backend.goals) @prio(P1) Contract test: DELETE /api/goals/{id} returns 204
- [ ] T045 @module(backend.goals) @prio(P2) Integration test: Create → View → Edit → Delete flow
- [ ] T046 @module(backend.goals) @prio(P2) Integration test: Filtering by status (active/done)
- [ ] T047 @module(backend.goals) @prio(P2) Integration test: Validation errors (empty title, title > 255)
- [ ] T048 @module(backend.goals) @prio(P2) Integration test: Concurrent edits (last-write-wins)
- [ ] T050 @module(backend.goals) @prio(P1) Wire goals router into main FastAPI app
- [ ] T060 @module(backend.goals) @prio(P2) Update manifest with final exports/types
- [ ] T063 @module(backend.goals) @prio(P1) Run registry validators (registry_validate.py, manifest_lint.py)
- [ ] T064 @module(backend.goals) @prio(P3) Performance test: API response times <200ms
<!-- FANOUT:END -->
