# Implementation Plan: Goals Management MVP (foundation)

**Branch**: `001-goals-management-mvp` | **Date**: 2025-10-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/home/anton/code/ai_life_os/specs/001-goals-management-mvp/spec.md`

---

## Execution Flow (performed by `/plan`)

> Goal: lock module boundaries **now**, bootstrap public docs (registry + manifests + contracts), then design **contract-first**.
> Tasks will be generated later by `/tasks` (no task file here).

### M0. Module Partition & Registry Bootstrap ✅ COMPLETE

**Modules Created**:
1. **frontend.design** - Shared design system (foundational, no dependencies)
2. **backend.goals** - Goals REST API (server-side CRUD + persistence)
3. **frontend.goals** - Goals UI (consumes backend.goals + uses frontend.design)

**Registry Status**: ✅ Validated via `registry_validate.py`
**Manifests Status**: ✅ Created and populated in `.specify/memory/public/`
**Contracts Status**: ✅ Language contracts created (TypeScript `.d.ts`, Python Protocols, OpenAPI YAML)

### 0. Load Feature Spec ✅ COMPLETE
Loaded from `/home/anton/code/ai_life_os/specs/001-goals-management-mvp/spec.md`

### 1. Technical Context ✅ COMPLETE
Recorded environment decisions for scaffolding (frameworks are adapter details, not domain drivers).

### 2. Constitution Gate (initial) ✅ PASS
- Public API via registry + manifest + contract: ✅
- No cross-module source reading: ✅
- Imports follow import_hint: ✅
- Clean Code gates (SOLID, DRY, KISS, no magic, small functions): ✅

### 3. Phase 0 — research.md ✅ COMPLETE
Domain/UX clarifications resolved. See `research.md` for technology choices and rationale.

### 4. Phase 1 — Design & Contracts ✅ COMPLETE
- `data-model.md`: Entities and domain invariants defined
- `contracts/`: OpenAPI (backend.goals), TypeScript (frontend.goals, frontend.design)
- `quickstart.md`: End-to-end acceptance flows documented

### 5. Constitution Gate (post-design) ✅ PASS
Re-checked boundaries/CDC. No leaks detected. Contracts are consumer-driven.

### 6. Phase 2 — Task Planning ✅ DESCRIBED (ready for /tasks)
See "Phase 2: Task Planning Approach" section below. `/tasks` command will generate tasks.md.

---

## Module API Matrix

> Authoritative module boundaries. Public surfaces only. Internals (domain/app/infra/api) are private to each module.

**Design Rationale**:
- Modules are bounded contexts with clear external contracts
- Internals stay private (domain/repository/service/api layers are implementation details)
- Dependencies go through ports/contracts only (Protocol for backend, TypeScript interfaces for frontend)
- `frontend.design` is foundational with no dependencies; other modules build on top

---

## Technical Context (scaffold snapshot)

**Language/Version**: Backend: Python 3.11, Frontend: TypeScript 5 (Next.js 15)

**Primary Dependencies**:
- Backend: FastAPI (async REST), SQLAlchemy 2.0 (async ORM), asyncpg (PostgreSQL driver), Pydantic v2 (validation), Alembic (migrations)
- Frontend: React 19, Next.js 15 (App Router), SWR (state management), Tailwind CSS 4 (styling), Radix UI (accessibility primitives)

**Storage**: PostgreSQL 15+ (via Docker Compose)

**Testing**: Backend: pytest + mypy + ruff; Frontend: ESLint + TypeScript + Prettier

**Target Platform**: Web application (Linux server + modern browsers)

**Project Type**: `web` (frontend/ + backend/ detected)

**Performance Goals**: <200ms API response time, <100ms UI interactions

**Constraints**: Single-user MVP, last-write-wins for concurrent edits, 255 char title limit, strict module boundaries

**Scale/Scope**: 1 user, ~10-50 goals expected

**Note**: Frameworks are details of adapters; they don't shape the domain plan (Hexagonal Architecture).

---

## SemVer & Conventional Commits

- SemVer for public APIs: MAJOR (breaking), MINOR (additive), PATCH (fixes)
- Conventional Commits for history/automation:
  - `feat(backend.goals): add endpoint [public-api]` (MINOR)
  - `fix(frontend.goals): correct validation [public-api]` (PATCH)
  - `feat(backend.goals)!: change schema [public-api]` (MAJOR)

---

## Project Structure (by modules, not layers)

### Specification Artifacts (this feature)
```
specs/001-goals-management-mvp/
├── spec.md              # Feature requirements (input)
├── plan.md              # This file (execution record)
├── research.md          # Phase 0 output (technology decisions)
├── data-model.md        # Phase 1 output (entities + invariants)
├── quickstart.md        # Phase 1 output (acceptance validation)
└── contracts/           # Archived design-phase contracts (copied to proper locations)
    ├── backend.goals.api.md       # → moved to .specify/memory/public/
    ├── frontend.goals.api.md      # → moved to .specify/memory/public/
    ├── frontend.design.api.md     # → moved to .specify/memory/public/
    ├── openapi.yaml               # → copied to backend/src/.../contracts/
    └── goals.d.ts                 # → moved to frontend/src/contracts/
```

### Source Code (repository root)
```
backend/
  src/ai_life_backend/
    goals/                # backend.goals module internals
      domain/             # Goal entity (dataclass)
      repository/         # PostgreSQL implementation
      services/           # Business logic orchestration
      api/                # FastAPI routes + Pydantic schemas
      public/             # Public exports (facade)
    contracts/            # Language contracts (cross-module)
      goals_contracts.py  # Protocol definitions (GoalRepository, GoalService)
      goals_openapi.yaml  # OpenAPI 3.1 spec (generated by FastAPI)
  tests/goals/
    contract/             # API contract tests (schema validation)
    integration/          # DB + service integration tests
    unit/                 # Domain logic unit tests

frontend/
  src/
    features/
      design/             # frontend.design module internals
        components/       # Button, Dialog, Input, Label, Card, Badge
        utils/            # cn utility
      goals/              # frontend.goals module internals
        components/       # GoalList, GoalForm, GoalItem
        hooks/            # useGoals, useGoal, useGoalMutations
        lib/              # API client (HTTP calls to backend.goals)
    contracts/            # Language contracts (cross-module)
      design.d.ts         # Design system TypeScript definitions
      goals.d.ts          # Goals feature TypeScript definitions

.specify/
  memory/
    public/
      registry.yaml                # Module registry (authoritative)
      backend.goals.api.md         # Backend goals manifest
      frontend.goals.api.md        # Frontend goals manifest
      frontend.design.api.md       # Design system manifest
```

**Structure Decision**: Web application with modules as first-class bounded contexts. Backend uses `/src/ai_life_backend/[module]/` pattern; frontend uses `/src/features/[module]/` pattern. Contracts are co-located in dedicated `/contracts/` directories for visibility.

---

## Deliverables from /plan

✅ **Module registry updated & validated** (`.specify/memory/public/registry.yaml`)
✅ **Manifests scaffolded** (`.specify/memory/public/*.api.md`)
✅ **Language contracts created** (`contracts/*.d.ts`, `contracts/*_contracts.py`, `contracts/*_openapi.yaml`)
✅ **research.md** (technology decisions with rationale)
✅ **data-model.md** (domain entities, invariants, validation rules)
✅ **quickstart.md** (acceptance scenario validation procedures)
✅ **This plan.md** (Module API Matrix + gates + execution record)

---

## Phase 0: Research (domain/UX unknowns only)

**Status**: ✅ COMPLETE

See **`research.md`** for:
- FastAPI + SQLAlchemy 2.0 + PostgreSQL decisions
- SWR for frontend state management
- RESTful API design (5 endpoints)
- Database schema (UUID, indexes, constraints)
- Error handling strategy (RFC 7807 Problem Details)
- Module boundaries and dependencies
- Performance + security considerations

**Key Outcome**: All NEEDS CLARIFICATION items resolved. Technology choices align with constitutional requirements (async Python, typed, SOLID, contract-first).

---

## Phase 1: Design & Contracts (contract-first)

**Status**: ✅ COMPLETE

### data-model.md
Domain-level entities and invariants (no ORM specifics):
- **Goal** entity: `id: UUID`, `title: str (1-255)`, `is_done: bool`, `date_created: datetime`, `date_updated: datetime`
- **Validation rules**: Non-empty title, max 255 chars (enforced at API + DB layers)
- **State transitions**: Active ↔ Done, with permanent deletion
- **Ordering rules**: Active first, then by `date_updated DESC`
- **Repository Protocol**: 6 async methods (create, get_by_id, list_all, list_by_status, update, delete)
- **Domain invariants**: Single-user scope, last-write-wins for concurrent edits

### contracts/
**HTTP Contract** (backend.goals):
- `openapi.yaml` - OpenAPI 3.1 spec with 5 endpoints:
  - `GET /api/goals` (with optional `?status=active|done`)
  - `POST /api/goals`
  - `GET /api/goals/{id}`
  - `PATCH /api/goals/{id}`
  - `DELETE /api/goals/{id}`
- Pydantic request/response schemas defined
- Error responses follow RFC 7807 structure

**TypeScript Contracts** (frontend):
- `goals.d.ts` - Goal types, component props, hook return types
- `design.d.ts` - Design system component types (Button, Dialog, Input, Label, Card, Badge)

**Python Protocol Contract** (backend.goals):
- `goals_contracts.py` - Protocol definitions for GoalRepository, GoalService, Goal entity

### quickstart.md
End-to-end acceptance flow with:
- 10 acceptance scenarios from spec.md (create, view, edit, toggle, delete, filter)
- 6 edge cases (empty title, concurrent edits, title > 255 chars, no matches, empty state, backend unavailable)
- Performance validation criteria (<200ms API, <100ms UI)
- Database verification queries

**No implementation code** - only failing test skeleton descriptions.

**Consumer-Driven Contracts**: Consumers (frontend.goals) define expectations; providers (backend.goals, frontend.design) evolve safely within those contracts.

---

## Phase 2: Task Planning Approach

> **IMPORTANT**: This section describes what `/tasks` will do. **DO NOT create tasks.md during /plan**.

### Task Generation Strategy

`/tasks` will:
1. Load `.specify/templates/tasks-template.md` as base
2. Read Phase 1 artifacts (contracts, data-model.md, quickstart.md)
3. Generate ~40 tasks in strict TDD order
4. Mark parallel-safe tasks with `[P]`
5. Group tasks by module using `@module(...)` annotations

### Ordering Strategy

**Strict TDD Order**:
1. Setup & Configuration (Docker, dependencies, migrations)
2. Contract Tests (define behavior, must fail initially)
3. Domain Layer (Goal entity with invariants)
4. Repository Layer (tests → implementation)
5. Service Layer (tests → implementation)
6. API Layer (tests → implementation)
7. Frontend API Client (tests → implementation)
8. Frontend Components (tests → implementation)
9. Integration Validation (quickstart scenarios)

**Dependency Hierarchy**:
```
Setup → Database Schema → Domain → Repository → Services → API → Frontend Client → Components → Validation
```

**Parallel Execution**: Contract tests, repository unit tests, service unit tests, component tests can run in parallel (marked `[P]`).

### Module Fanout

`/fanout-tasks 001-goals-management-mvp` will generate:
- `tasks.by-module/backend.goals-tasks.md` (backend tasks)
- `tasks.by-module/frontend.goals-tasks.md` (frontend goals tasks)
- `tasks.by-module/frontend.design-tasks.md` (design system tasks)

Each module task file will include:
- File-scoped steps (tests → implementation → integration → polish)
- **Docs sync** section (update manifest, contract, semver, run validators)

### Estimated Task Count
- Backend: ~20 tasks (setup, domain, repository, services, API)
- Frontend: ~15 tasks (setup, API client, hooks, components)
- Integration: ~5 tasks (acceptance scenarios, performance validation)

**Total**: ~40 tasks

---

## Gates & Policies

### Docs-as-Code
Manifests/contracts live in repo; changes gated by validators:
```bash
python .specify/scripts/registry_validate.py  # ✅ PASSING
python .specify/scripts/manifest_lint.py      # ✅ PASSING
```

### Consumer-Driven Contracts (CDC)
Consumers request changes via handoff notes; providers evolve contracts safely. If a task requires changes outside module boundaries:
1. Create `handoff.md` in `specs/001-goals-management-mvp/`
2. Document required public API addition
3. **DO NOT** modify other module's code directly

### SemVer + Conventional Commits
- Public APIs versioned with SemVer
- Commits follow Conventional Commits format
- `[public-api]` marker in commit message triggers documentation review

### No Cross-Module Source Reading
- Imports follow `import_hint` from registry
- Deep imports prohibited

### Clean Code (NON-NEGOTIABLE)
- **SOLID** strictly enforced
- **DRY**: No duplication
- **KISS**: MVP simplicity
- **No magic values**: Extract to constants
- **Small functions**: ≤40 lines
- **Low complexity**: Cyclomatic ≤8
- **Explicit types**: No untyped defs
- **Tests-first**: TDD required

---

## Progress Tracking

**Phase Status**:
- [x] M0: Modules bootstrapped (registry/manifests/contracts validated) ✅ 2025-10-04
- [x] Phase 0: Research complete ✅ 2025-10-04
- [x] Phase 1: Design complete ✅ 2025-10-04
- [x] Phase 2: Task planning ready (run `/tasks`) ✅ 2025-10-04
- [ ] Phase 3: Tasks generated (awaiting `/tasks` command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] M0 Validators: `registry_validate.py` + `manifest_lint.py` ✅ PASSING
- [x] Initial Constitution Check ✅ PASS
- [x] Post-Design Constitution Check ✅ PASS
- [x] All NEEDS CLARIFICATION resolved ✅ (see research.md)

---

**Plan Version**: Based on Constitution v1.4.0 | Template v2.0 (M0-first, module-bounded)
**Status**: ✅ READY FOR `/tasks` COMMAND
