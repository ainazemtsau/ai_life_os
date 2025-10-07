# Tasks: Goals Management MVP (foundation)

**Feature Branch**: `001-goals-management-mvp`
**Input**: Design documents from `/home/anton/code/ai_life_os/specs/001-goals-management-mvp/`
**Prerequisites**: ✅ `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

---

## Module API Matrix (global contracts)

> Define the **public surface** for each module. Keep it concise and normative.

### module: backend.goals
**public:**
```
POST   /api/goals              -> GoalResponse (201)
GET    /api/goals              -> GoalListResponse (200)
GET    /api/goals?status=...   -> GoalListResponse (200)
GET    /api/goals/{id}         -> GoalResponse (200)
PATCH  /api/goals/{id}         -> GoalResponse (200)
DELETE /api/goals/{id}         -> 204 No Content
```

### module: frontend.design
**public:**
```typescript
export { Button, Dialog, Input, Label, Card, Badge, cn }
```

### module: frontend.goals
**public:**
```typescript
export { GoalList, GoalForm, GoalItem }
export { useGoals, useGoal, useGoalMutations }
```

---

## Global Tasks by Module (high-level only)

> Tag each with `@module(<name>)` and priority `@prio(P1|P2|P3)`. Do **not** include file-level details here.

### Setup & Infrastructure
- [ ] T001 @module(infra) @prio(P1) Configure PostgreSQL service in docker-compose.yml
- [ ] T002 @module(backend.goals) @prio(P1) Add FastAPI + SQLAlchemy + asyncpg dependencies via uv
- [ ] T003 @module(frontend.goals) @prio(P1) Add SWR dependency via pnpm
- [ ] T004 @module(backend.goals) @prio(P1) Initialize Alembic migrations for goals schema

### Backend Module: backend.goals
- [ ] T010 @module(backend.goals) @prio(P1) Define Goal domain entity (dataclass) with validation
- [ ] T011 @module(backend.goals) @prio(P1) Define GoalRepository Protocol interface
- [ ] T012 @module(backend.goals) @prio(P1) Create PostgreSQL migration for goals table + indexes
- [ ] T013 @module(backend.goals) @prio(P1) Implement PostgresGoalRepository with async methods
- [ ] T014 @module(backend.goals) @prio(P2) Define GoalService with business logic orchestration
- [ ] T015 @module(backend.goals) @prio(P1) Define Pydantic request/response schemas
- [ ] T016 @module(backend.goals) @prio(P1) Implement FastAPI router with 5 endpoints
- [ ] T017 @module(backend.goals) @prio(P2) Add error handling middleware for RFC 7807 responses
- [ ] T018 @module(backend.goals) @prio(P1) Create public facade (goals_router export)

### Frontend Module: frontend.design
- [ ] T020 @module(frontend.design) @prio(P1) Implement Button component with variants
- [ ] T021 @module(frontend.design) @prio(P1) Implement Dialog component (Radix UI wrapper)
- [ ] T022 @module(frontend.design) @prio(P1) Implement Input component with error state
- [ ] T023 @module(frontend.design) @prio(P1) Implement Label component
- [ ] T024 @module(frontend.design) @prio(P2) Implement Card components (Card, CardHeader, CardContent)
- [ ] T025 @module(frontend.design) @prio(P2) Implement Badge component with variants
- [ ] T026 @module(frontend.design) @prio(P1) Implement cn utility (clsx + tailwind-merge)

### Frontend Module: frontend.goals
- [ ] T030 @module(frontend.goals) @prio(P1) Implement Goals API client (HTTP methods)
- [ ] T031 @module(frontend.goals) @prio(P1) Implement useGoals hook (SWR-based list)
- [ ] T032 @module(frontend.goals) @prio(P1) Implement useGoal hook (SWR-based single)
- [ ] T033 @module(frontend.goals) @prio(P1) Implement useGoalMutations hook (create/update/delete with optimistic updates)
- [ ] T034 @module(frontend.goals) @prio(P1) Implement GoalList component with filtering
- [ ] T035 @module(frontend.goals) @prio(P1) Implement GoalForm component (create/edit modes)
- [ ] T036 @module(frontend.goals) @prio(P1) Implement GoalItem component with inline actions

### Testing (Contract & Integration)
- [ ] T040 @module(backend.goals) @prio(P1) Contract test: POST /api/goals validates schema
- [ ] T041 @module(backend.goals) @prio(P1) Contract test: GET /api/goals returns list schema
- [ ] T042 @module(backend.goals) @prio(P1) Contract test: GET /api/goals/{id} validates UUID param
- [ ] T043 @module(backend.goals) @prio(P1) Contract test: PATCH /api/goals/{id} validates request body
- [ ] T044 @module(backend.goals) @prio(P1) Contract test: DELETE /api/goals/{id} returns 204
- [ ] T045 @module(backend.goals) @prio(P2) Integration test: Create → View → Edit → Delete flow
- [ ] T046 @module(backend.goals) @prio(P2) Integration test: Filtering by status (active/done)
- [ ] T047 @module(backend.goals) @prio(P2) Integration test: Validation errors (empty title, title > 255)
- [ ] T048 @module(backend.goals) @prio(P2) Integration test: Concurrent edits (last-write-wins)

### Integration & Wiring
- [ ] T050 @module(backend.goals) @prio(P1) Wire goals router into main FastAPI app
- [ ] T051 @module(frontend.goals) @prio(P1) Wire Goals page to Next.js App Router
- [ ] T052 @module(infra) @prio(P2) Configure CORS for frontend-backend communication

### Polish & Documentation
- [ ] T060 @module(backend.goals) @prio(P2) Update manifest with final exports/types
- [ ] T061 @module(frontend.goals) @prio(P2) Update manifest with final component/hook signatures
- [ ] T062 @module(frontend.design) @prio(P2) Update manifest with design system components
- [ ] T063 @module(backend.goals) @prio(P1) Run registry validators (registry_validate.py, manifest_lint.py)
- [ ] T064 @module(backend.goals) @prio(P3) Performance test: API response times <200ms
- [ ] T065 @module(frontend.goals) @prio(P3) Accessibility audit: WCAG 2.1 AA compliance

---

## Execution Flow (main)

### 1. Load plan.md ✅
- Tech stack: Python 3.11 + FastAPI, TypeScript 5 + Next.js 15
- Libraries: SQLAlchemy 2.0, asyncpg, Pydantic v2, SWR, Radix UI, Tailwind CSS 4
- Structure: Web app (backend/ + frontend/)

### 2. Load optional design docs ✅
- **data-model.md**: Goal entity (id, title, is_done, date_created, date_updated)
- **contracts/**: OpenAPI spec (5 endpoints), TypeScript definitions
- **research.md**: FastAPI, PostgreSQL, SWR decisions
- **quickstart.md**: 10 acceptance scenarios + 6 edge cases

### 3. Generate preliminary tasks (GLOBAL scope)
- Setup: Docker Compose, dependencies, migrations
- Tests: Contract tests per endpoint, integration tests per scenario
- Core: Domain entity, repository, service, API routes, components, hooks
- Integration: Wiring, CORS, error handling
- Polish: Manifests, validators, performance

### 4. Apply task rules
- Different files → mark [P] (handled in module tasks)
- Same file → sequential
- Tests before implementation (TDD mandatory)

### 5. Number tasks sequentially
- T001-T004: Infrastructure
- T010-T018: backend.goals
- T020-T026: frontend.design
- T030-T036: frontend.goals
- T040-T049: Testing
- T050-T052: Integration
- T060-T065: Polish

### 6. Build dependency notes
**Critical Path**:
```
T001-T004 (Setup)
  ↓
T010 → T011 → T012 → T013 (Backend: Domain → Repository)
  ↓
T014 → T015 → T016 (Backend: Service → API)
  ↓
T020-T026 (Frontend: Design System) [can run parallel to backend]
  ↓
T030-T036 (Frontend: Goals UI - depends on backend.goals + frontend.design)
  ↓
T040-T049 (Testing - validates everything)
  ↓
T050-T052 (Integration)
  ↓
T060-T065 (Polish)
```

### 7. Create fan-out plan
**Module task files to be generated** (via `/fanout-tasks` or `/module-tasks`):
- `tasks.by-module/backend.goals-tasks.md` - Detailed backend implementation steps
- `tasks.by-module/frontend.design-tasks.md` - Design system component implementation
- `tasks.by-module/frontend.goals-tasks.md` - Goals UI implementation

### 8. Validate completeness ✅
- [x] All public APIs in Module API Matrix covered by tasks
- [x] Contracts mapped to modules (T040-T044)
- [x] Global tasks free of file-level details (deferred to module tasks)

---

## Phase 3.1: Setup (global infrastructure)

**Priority**: P1 (must complete before any module work)

### T001 @module(infra) @prio(P1) Configure PostgreSQL in docker-compose.yml
**Description**: Add PostgreSQL 15-alpine service with environment variables and volume persistence.

**Dependencies**: None

**Acceptance Criteria**:
- `docker-compose.yml` includes postgres service
- Environment: POSTGRES_DB=ai_life_os, POSTGRES_USER=postgres, POSTGRES_PASSWORD=postgres
- Port 5432 exposed to localhost
- Volume `postgres_data` for persistence

**Validation**:
```bash
docker-compose up -d postgres
docker-compose ps | grep postgres | grep "Up"
```

---

### T002 @module(backend.goals) @prio(P1) Add backend dependencies via uv
**Description**: Install FastAPI, SQLAlchemy 2.0, asyncpg, Pydantic v2, and Alembic.

**Dependencies**: None

**Acceptance Criteria**:
- `backend/pyproject.toml` updated with dependencies
- `backend/uv.lock` regenerated
- `uv sync` completes successfully

**Validation**:
```bash
cd backend && uv sync && uv run python -c "import fastapi, sqlalchemy, asyncpg, pydantic, alembic"
```

---

### T003 @module(frontend.goals) @prio(P1) Add SWR dependency via pnpm
**Description**: Install SWR for React state management.

**Dependencies**: None

**Acceptance Criteria**:
- `frontend/package.json` includes `swr` dependency
- `frontend/pnpm-lock.yaml` updated
- `pnpm install` completes successfully

**Validation**:
```bash
cd frontend && pnpm add swr && pnpm install
```

---

### T004 @module(backend.goals) @prio(P1) Initialize Alembic migrations
**Description**: Set up Alembic for database schema migrations.

**Dependencies**: T002

**Acceptance Criteria**:
- `backend/alembic.ini` configured with asyncpg connection string
- `backend/alembic/` directory structure created
- `env.py` configured for async migrations

**Validation**:
```bash
cd backend && uv run alembic init alembic
```

---

## Phase 3.2: Tests First (TDD) — global acceptance framing

**Note**: Actual test files are generated in module tasks. These are high-level placeholders.

### T040-T044: Contract Tests (backend.goals)
**Coverage Table**:
| Endpoint | Contract Test | Module |
|----------|--------------|---------|
| POST /api/goals | T040 | backend.goals |
| GET /api/goals | T041 | backend.goals |
| GET /api/goals/{id} | T042 | backend.goals |
| PATCH /api/goals/{id} | T043 | backend.goals |
| DELETE /api/goals/{id} | T044 | backend.goals |

**Integration Flows** (mapped to modules):
- User creates goal → T045 (backend.goals)
- User filters goals → T046 (backend.goals)
- Validation error handling → T047 (backend.goals)
- Concurrent edits → T048 (backend.goals)

---

## Phase 3.3: Core (high-level only)

### Backend Module: backend.goals (T010-T018)

#### T010 @module(backend.goals) @prio(P1) Define Goal domain entity
**Description**: Create immutable Goal dataclass with validation invariants.

**Dependencies**: T002

**Acceptance Criteria**:
- Goal dataclass defined with frozen=True
- Fields: id (UUID), title (str), is_done (bool), date_created (datetime), date_updated (datetime)
- `__post_init__` validates title (non-empty, ≤255 chars)
- Raises ValueError for invalid data

**Module Task**: Detailed in `backend.goals-tasks.md`

---

#### T011 @module(backend.goals) @prio(P1) Define GoalRepository Protocol
**Description**: Create repository interface using Python Protocol for dependency inversion.

**Dependencies**: T010

**Acceptance Criteria**:
- GoalRepository Protocol with 6 async methods
- Methods: create, get_by_id, list_all, list_by_status, update, delete
- Type hints fully specified
- Docstrings for each method

**Module Task**: Detailed in `backend.goals-tasks.md`

---

#### T012 @module(backend.goals) @prio(P1) Create PostgreSQL migration
**Description**: Generate Alembic migration for goals table with indexes.

**Dependencies**: T004, T011

**Acceptance Criteria**:
- Migration creates `goals` table with UUID primary key
- Columns: id, title (VARCHAR 255), is_done (BOOLEAN), date_created (TIMESTAMPTZ), date_updated (TIMESTAMPTZ)
- CHECK constraint: `LENGTH(TRIM(title)) > 0`
- Indexes: idx_goals_is_done, idx_goals_date_updated DESC

**Validation**:
```bash
cd backend && uv run alembic upgrade head
```

**Module Task**: Detailed in `backend.goals-tasks.md`

---

#### T013 @module(backend.goals) @prio(P1) Implement PostgresGoalRepository
**Description**: Implement GoalRepository Protocol using SQLAlchemy + asyncpg.

**Dependencies**: T011, T012

**Acceptance Criteria**:
- All 6 Protocol methods implemented
- Async/await throughout
- SQLAlchemy Core (async) for queries
- Proper error handling (converts DB errors to domain exceptions)
- Connection pooling configured

**Module Task**: Detailed in `backend.goals-tasks.md`

---

#### T014 @module(backend.goals) @prio(P2) Define GoalService
**Description**: Create service layer for business logic orchestration.

**Dependencies**: T011

**Acceptance Criteria**:
- GoalService class with dependency injection (takes GoalRepository)
- Methods: create_goal, get_goal, list_goals, update_goal, delete_goal
- Thin layer (mostly delegates to repository for MVP)
- Handles status_filter conversion ('active'/'done' → is_done bool)

**Module Task**: Detailed in `backend.goals-tasks.md`

---

#### T015 @module(backend.goals) @prio(P1) Define Pydantic schemas
**Description**: Create request/response models for FastAPI validation.

**Dependencies**: T010

**Acceptance Criteria**:
- GoalCreateRequest (title: str, field validators)
- GoalUpdateRequest (title: str | None, is_done: bool | None)
- GoalResponse (full Goal representation)
- GoalListResponse (goals: list[GoalResponse])
- ErrorResponse (detail, type, status)

**Module Task**: Detailed in `backend.goals-tasks.md`

---

#### T016 @module(backend.goals) @prio(P1) Implement FastAPI router
**Description**: Create goals router with 5 endpoints following OpenAPI spec.

**Dependencies**: T014, T015

**Acceptance Criteria**:
- Router with prefix `/api/goals`
- 5 endpoints implemented (POST, GET list, GET single, PATCH, DELETE)
- Dependency injection for GoalService
- Proper status codes (201, 200, 204, 404, 422)
- Query param validation for `?status=active|done`

**Module Task**: Detailed in `backend.goals-tasks.md`

---

#### T017 @module(backend.goals) @prio(P2) Add error handling middleware
**Description**: Implement RFC 7807 Problem Details for error responses.

**Dependencies**: T015

**Acceptance Criteria**:
- Exception handler for ValueError → 422
- Exception handler for NotFound → 404
- Error responses follow ErrorResponse schema
- User-friendly error messages

**Module Task**: Detailed in `backend.goals-tasks.md`

---

#### T018 @module(backend.goals) @prio(P1) Create public facade
**Description**: Define public exports for backend.goals module.

**Dependencies**: T016

**Acceptance Criteria**:
- `backend/src/ai_life_backend/goals/public/__init__.py` exports goals_router
- Matches import_hint from registry: `from ai_life_backend.goals.public import goals`
- Internal imports hidden

**Module Task**: Detailed in `backend.goals-tasks.md`

---

### Frontend Module: frontend.design (T020-T026)

#### T020 @module(frontend.design) @prio(P1) Implement Button component
**Description**: Create Button component with CVA variants (default, destructive, outline, ghost, link).

**Dependencies**: T003

**Acceptance Criteria**:
- Button.tsx with variant and size props
- Tailwind CSS styling
- Accessible (ARIA attributes)
- Supports asChild prop for composition

**Module Task**: Detailed in `frontend.design-tasks.md`

---

#### T021 @module(frontend.design) @prio(P1) Implement Dialog component
**Description**: Wrap Radix UI Dialog primitives with Tailwind styling.

**Dependencies**: T003

**Acceptance Criteria**:
- Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle, DialogDescription
- Keyboard navigation (Esc to close)
- Focus trap when open
- Backdrop click to close

**Module Task**: Detailed in `frontend.design-tasks.md`

---

#### T022 @module(frontend.design) @prio(P1) Implement Input component
**Description**: Create Input with error state styling.

**Dependencies**: T003

**Acceptance Criteria**:
- Input with forwardRef for form library compatibility
- Error prop toggles error styling (red border)
- Tailwind CSS classes
- Supports all standard HTML input attributes

**Module Task**: Detailed in `frontend.design-tasks.md`

---

#### T023 @module(frontend.design) @prio(P1) Implement Label component
**Description**: Create accessible Label component wrapping Radix UI Label.

**Dependencies**: T003

**Acceptance Criteria**:
- Label with htmlFor prop
- Proper association with form controls
- Tailwind CSS styling

**Module Task**: Detailed in `frontend.design-tasks.md`

---

#### T024 @module(frontend.design) @prio(P2) Implement Card components
**Description**: Create Card, CardHeader, CardTitle, CardDescription, CardContent.

**Dependencies**: T003

**Acceptance Criteria**:
- All 5 Card subcomponents
- Tailwind CSS styling
- Composable structure

**Module Task**: Detailed in `frontend.design-tasks.md`

---

#### T025 @module(frontend.design) @prio(P2) Implement Badge component
**Description**: Create Badge with variant prop (default, secondary, destructive, outline).

**Dependencies**: T003

**Acceptance Criteria**:
- Badge with CVA variants
- Tailwind CSS styling
- Small, compact design

**Module Task**: Detailed in `frontend.design-tasks.md`

---

#### T026 @module(frontend.design) @prio(P1) Implement cn utility
**Description**: Create class name merger combining clsx and tailwind-merge.

**Dependencies**: T003

**Acceptance Criteria**:
- Function signature: `cn(...inputs: ClassValue[]) => string`
- Handles conditionals, arrays, objects
- Deduplicates Tailwind classes

**Module Task**: Detailed in `frontend.design-tasks.md`

---

### Frontend Module: frontend.goals (T030-T036)

#### T030 @module(frontend.goals) @prio(P1) Implement Goals API client
**Description**: Create HTTP client for backend.goals API consumption.

**Dependencies**: T016 (backend must expose API), T003

**Acceptance Criteria**:
- API client class with 5 methods (listGoals, getGoal, createGoal, updateGoal, deleteGoal)
- Fetch-based HTTP calls to `process.env.NEXT_PUBLIC_API_URL`
- Error handling (network errors, HTTP errors)
- Type-safe (uses Goal, GoalCreateInput, GoalUpdateInput types)

**Module Task**: Detailed in `frontend.goals-tasks.md`

---

#### T031 @module(frontend.goals) @prio(P1) Implement useGoals hook
**Description**: Create SWR-based hook for fetching goals list with filtering.

**Dependencies**: T030

**Acceptance Criteria**:
- Hook signature: `useGoals(filter?: 'all' | 'active' | 'done')`
- Returns: `{ goals, isLoading, error, mutate }`
- Automatic caching and revalidation
- Revalidates on focus/reconnect

**Module Task**: Detailed in `frontend.goals-tasks.md`

---

#### T032 @module(frontend.goals) @prio(P1) Implement useGoal hook
**Description**: Create SWR-based hook for fetching single goal.

**Dependencies**: T030

**Acceptance Criteria**:
- Hook signature: `useGoal(id: string)`
- Returns: `{ goal, isLoading, error, mutate }`
- Returns null if goal not found
- Automatic caching

**Module Task**: Detailed in `frontend.goals-tasks.md`

---

#### T033 @module(frontend.goals) @prio(P1) Implement useGoalMutations hook
**Description**: Create hook for goal mutations with optimistic updates.

**Dependencies**: T030, T031

**Acceptance Criteria**:
- Returns: `{ createGoal, updateGoal, deleteGoal, isMutating }`
- Optimistic UI updates (instant feedback)
- SWR cache invalidation on success
- Rollback on error

**Module Task**: Detailed in `frontend.goals-tasks.md`

---

#### T034 @module(frontend.goals) @prio(P1) Implement GoalList component
**Description**: Create list component with filtering and sorting.

**Dependencies**: T031, T020-T026 (frontend.design)

**Acceptance Criteria**:
- Props: `filter?: 'all' | 'active' | 'done'`, `onGoalClick`, `className`
- Uses useGoals hook
- Displays loading state, error state, empty state
- Renders GoalItem for each goal

**Module Task**: Detailed in `frontend.goals-tasks.md`

---

#### T035 @module(frontend.goals) @prio(P1) Implement GoalForm component
**Description**: Create form for creating/editing goals.

**Dependencies**: T033, T020-T026 (frontend.design)

**Acceptance Criteria**:
- Props: `goal?: Goal`, `onSave`, `onCancel`, `className`
- Create mode (no goal prop) vs Edit mode
- Client-side validation (non-empty, ≤255 chars)
- Character counter
- Uses Input, Label, Button from design system

**Module Task**: Detailed in `frontend.goals-tasks.md`

---

#### T036 @module(frontend.goals) @prio(P1) Implement GoalItem component
**Description**: Create single goal row with inline actions.

**Dependencies**: T033, T020-T026 (frontend.design)

**Acceptance Criteria**:
- Props: `goal`, `onToggle`, `onEdit`, `onDelete`, `className`
- Checkbox for toggling completion
- Visual distinction for active/done (strikethrough, different color)
- Edit and Delete buttons

**Module Task**: Detailed in `frontend.goals-tasks.md`

---

## Phase 3.4: Integration (cross-module wiring)

### T050 @module(backend.goals) @prio(P1) Wire goals router into main app
**Description**: Include goals router in main FastAPI application.

**Dependencies**: T018

**Acceptance Criteria**:
- `backend/src/ai_life_backend/app.py` imports and includes goals_router
- Router prefix: `/api`
- OpenAPI docs available at `/docs` showing goals endpoints

**Validation**:
```bash
cd backend && uv run uvicorn ai_life_backend.app:app --reload
curl http://localhost:8000/docs
```

**Module Task**: Detailed in `backend.goals-tasks.md`

---

### T051 @module(frontend.goals) @prio(P1) Wire Goals page to Next.js App Router
**Description**: Create goals page in Next.js app directory.

**Dependencies**: T034, T035

**Acceptance Criteria**:
- Page at `frontend/src/app/goals/page.tsx`
- Renders GoalForm + GoalList
- Filter state management
- Client component ('use client' directive)

**Validation**:
```bash
cd frontend && pnpm dev
# Visit http://localhost:3000/goals
```

**Module Task**: Detailed in `frontend.goals-tasks.md`

---

### T052 @module(infra) @prio(P2) Configure CORS for frontend-backend
**Description**: Enable CORS in FastAPI to allow frontend requests.

**Dependencies**: T050

**Acceptance Criteria**:
- FastAPI CORS middleware added
- Allow origins: `http://localhost:3000`
- Allow methods: GET, POST, PATCH, DELETE
- Allow headers: Content-Type

**Validation**:
```bash
curl -H "Origin: http://localhost:3000" http://localhost:8000/api/goals
```

**Module Task**: Detailed in `backend.goals-tasks.md`

---

## Phase 3.5: Polish (documentation & validation)

### T060 @module(backend.goals) @prio(P2) Update backend.goals manifest
**Description**: Refresh `.specify/memory/public/backend.goals.api.md` with final implementation details.

**Dependencies**: T018

**Acceptance Criteria**:
- Exports section lists all public functions
- Types section references goals_contracts.py
- Usage examples verified
- Version bumped if API changed (SemVer)

**Module Task**: Detailed in `backend.goals-tasks.md`

---

### T061 @module(frontend.goals) @prio(P2) Update frontend.goals manifest
**Description**: Refresh `.specify/memory/public/frontend.goals.api.md` with final component/hook signatures.

**Dependencies**: T036

**Acceptance Criteria**:
- Components section lists GoalList, GoalForm, GoalItem
- Hooks section lists useGoals, useGoal, useGoalMutations
- Props documented
- Version bumped if API changed

**Module Task**: Detailed in `frontend.goals-tasks.md`

---

### T062 @module(frontend.design) @prio(P2) Update frontend.design manifest
**Description**: Refresh `.specify/memory/public/frontend.design.api.md` with all components.

**Dependencies**: T026

**Acceptance Criteria**:
- All 6 components + cn utility documented
- Props/variants listed
- Usage examples provided

**Module Task**: Detailed in `frontend.design-tasks.md`

---

### T063 @module(backend.goals) @prio(P1) Run registry validators
**Description**: Validate module registry and manifests.

**Dependencies**: T060, T061, T062

**Acceptance Criteria**:
- `python3 .specify/scripts/registry_validate.py` passes
- `python3 .specify/scripts/manifest_lint.py` passes
- No errors in output

**Validation**:
```bash
python3 .specify/scripts/registry_validate.py && python3 .specify/scripts/manifest_lint.py
```

---

### T064 @module(backend.goals) @prio(P3) Performance test API response times
**Description**: Validate API performance meets <200ms requirement.

**Dependencies**: T045

**Acceptance Criteria**:
- All endpoints respond in <200ms (p95)
- Load test with 100 concurrent requests
- Performance report generated

**Module Task**: Detailed in `backend.goals-tasks.md`

---

### T065 @module(frontend.goals) @prio(P3) Accessibility audit
**Description**: Verify WCAG 2.1 AA compliance.

**Dependencies**: T051

**Acceptance Criteria**:
- Keyboard navigation works (Tab, Enter, Esc)
- Screen reader compatible (ARIA labels)
- Color contrast ≥4.5:1
- Focus indicators visible

**Module Task**: Detailed in `frontend.goals-tasks.md`

---

## Fan-out Rules (to module tasks)

Each `@module(<name>)` task will spawn detailed steps in module-specific task files:

### Generated via `/fanout-tasks 001-goals-management-mvp`:
- **`tasks.by-module/backend.goals-tasks.md`**
  - Expands T010-T018, T040-T049, T050, T052, T060, T063, T064
  - File-level steps with exact paths in `backend/src/ai_life_backend/goals/`
  - TDD enforcement (tests must fail first)

- **`tasks.by-module/frontend.design-tasks.md`**
  - Expands T020-T026, T062
  - File-level steps in `frontend/src/features/design/`
  - Component implementation + tests

- **`tasks.by-module/frontend.goals-tasks.md`**
  - Expands T030-T036, T051, T061, T065
  - File-level steps in `frontend/src/features/goals/`
  - Depends on frontend.design completion

### Module task loading:
- Global constitution (`.specify/memory/constitution.md`)
- Module constitution (if exists): `.specify/memory/<module>.constitution.md`
- Public API Registry: `.specify/memory/public/registry.yaml`

---

## Validation Checklist (global gate)

- [x] Every public API in Module API Matrix has at least one `@module(...)` task
  - backend.goals: 5 endpoints → T040-T044 (contract tests) + T016 (implementation)
  - frontend.design: 7 exports → T020-T026
  - frontend.goals: 6 exports → T030-T036

- [x] No file-paths appear in global tasks (deferred to module tasks)

- [x] Priorities set (P1/P2/P3):
  - P1: Critical path (setup, core domain, API, components)
  - P2: Important (service layer, error handling, polish)
  - P3: Nice-to-have (performance tests, accessibility audit)

- [x] Parallel markers not used for cross-module work (module tasks handle parallelization)

- [x] Global acceptance checks mapped to modules:
  - 10 acceptance scenarios → T045-T048 (backend.goals integration tests)
  - 6 edge cases → covered in T047, T048

---

## Parallel Execution Guide

### Phase 1: Setup (sequential)
```bash
# Must run in order
Task T001  # PostgreSQL setup
Task T002  # Backend deps
Task T003  # Frontend deps
Task T004  # Alembic init
```

### Phase 2: Backend Core (mostly sequential due to dependencies)
```bash
Task T010  # Goal entity
Task T011  # Repository Protocol
Task T012  # Migration
Task T013  # Repository impl
Task T014  # Service
Task T015  # Pydantic schemas
Task T016  # FastAPI router
Task T017  # Error handling
Task T018  # Public facade
```

### Phase 3: Frontend (can run parallel to Phase 2)
```bash
# Design system (all parallel - different files)
Task T020 [P]  # Button
Task T021 [P]  # Dialog
Task T022 [P]  # Input
Task T023 [P]  # Label
Task T024 [P]  # Card
Task T025 [P]  # Badge
Task T026 [P]  # cn utility

# Then Goals UI (depends on design system)
Task T030  # API client
Task T031  # useGoals
Task T032  # useGoal
Task T033  # useGoalMutations
Task T034  # GoalList
Task T035  # GoalForm
Task T036  # GoalItem
```

### Phase 4: Testing (parallel per endpoint)
```bash
Task T040 [P]  # POST test
Task T041 [P]  # GET list test
Task T042 [P]  # GET single test
Task T043 [P]  # PATCH test
Task T044 [P]  # DELETE test

# Integration (sequential)
Task T045  # Full flow test
Task T046  # Filter test
Task T047  # Validation test
Task T048  # Concurrent edits test
```

### Phase 5: Integration & Polish
```bash
Task T050  # Wire backend
Task T051  # Wire frontend
Task T052  # CORS

Task T060 [P]  # Backend manifest
Task T061 [P]  # Frontend goals manifest
Task T062 [P]  # Frontend design manifest
Task T063  # Validators
Task T064 [P]  # Performance test
Task T065 [P]  # Accessibility audit
```

---

## Task Agent Command Examples

### Running individual tasks:
```bash
# Setup
claude-code task T001  # Configure PostgreSQL
claude-code task T002  # Add backend deps

# Backend implementation
claude-code task T010  # Goal entity
claude-code task T016  # FastAPI router

# Frontend implementation
claude-code task T034  # GoalList component
```

### Running parallel tasks (design system):
```bash
# All design components can run simultaneously
claude-code task T020 T021 T022 T023 T024 T025 T026 --parallel
```

### Running contract tests in parallel:
```bash
claude-code task T040 T041 T042 T043 T044 --parallel
```

### Running full module:
```bash
# After fanout, run module-specific tasks
claude-code module-tasks backend.goals
claude-code module-tasks frontend.design
claude-code module-tasks frontend.goals
```

---

**Tasks Status**: ✅ READY FOR EXECUTION
**Total Tasks**: 65 global tasks
**Estimated Module Tasks** (after fanout): ~120-150 detailed file-level tasks
**Next Command**: `/fanout-tasks 001-goals-management-mvp` or begin execution with `Task T001`
