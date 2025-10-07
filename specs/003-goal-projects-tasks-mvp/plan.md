# Implementation Plan: Goals/Projects/Tasks MVP

**Branch**: `003-goal-projects-tasks-mvp` | **Date**: 2025-10-07 | **Spec**: spec.md
**Input**: Feature specification from `/home/anton/code/ai_life_os/specs/003-goal-projects-tasks-mvp/spec.md`

---

## Purpose
Freeze high-level design for this feature using **contracts-first**. The template is logic-less; the `/plan` runner injects all concrete details.

## Context & Constraints (from spec)
- **Scope**: CRUD list + forms only; no search, no detail pages in this MVP
- **Entities**: Goal, Milestone, Project, Task
- **Dependencies**: Tasks → Tasks (within same Project, DAG); Projects → Projects (within same Goal, DAG); Goals have no dependencies
- **Unified status**: `todo` / `doing` / `done` / `blocked` for all entities (future per-entity customization allowed)
- **Removed fields**: `mode`, `daypart_pref`, `outcome` must NOT exist
- **Enum dropdowns required** for: priority, status, size, energy, continuity, clarity, risk
- **Data formats**: UUIDs (v4), RFC 3339 timestamps (UTC), RFC 7807 Problem Details for errors
- **Standalone Projects**: allowed (no `goal_id` required)
- **Milestone scope**: belongs to Goal only (no direct Project link)

## Module Map (public surfaces only)

| Module | Role | Public Surface | Import Hint | Target? |
|--------|------|----------------|-------------|---------|
| `backend.core` | Cross-cutting primitives | Types, errors, utilities via Protocols | `from ai_life_backend.core.public import *` | **Context** |
| `backend.goals` | Goals domain (existing) | HTTP: `/api/goals` (OpenAPI) | `from ai_life_backend.goals.public import *` | **Context** |
| `backend.projects` | Projects/Tasks domain | HTTP: `/api/projects`, `/api/tasks` (OpenAPI); in-process Protocols for read-only queries | `from ai_life_backend.projects.public import *` | **Target** ✓ |
| `backend.milestones` | Milestones domain | HTTP: `/api/milestones` (OpenAPI); in-process Protocols | `from ai_life_backend.milestones.public import *` | **Target** ✓ |
| `frontend.design` | Design system | UI components, styles via TS `.d.ts` | `import * as design from '@/features/design'` | **Context** |
| `frontend.goals` | Goals UI (existing) | Goals-related UI components | `import * as goals from '@/features/goals'` | **Context** |
| `frontend.projects` | Projects/Tasks UI | List + CRUD forms for Projects, Tasks; dependency selectors | `import * as projects from '@/features/projects'` | **Target** ✓ |
| `frontend.milestones` | Milestones UI | List + CRUD forms for Milestones | `import * as milestones from '@/features/milestones'` | **Target** ✓ |
| `frontend.app-shell` | Routing & navigation | Next.js App Router glue (`frontend/src/app/**`) | `import * as appShell from '@/features/app-shell'` | **Target** ✓ |

> Only surfaces listed above are public. Everything else is private implementation.

## Contracts

### HTTP contracts (OpenAPI 3.1)

| Module | Contract Path | Endpoints | Notes |
|--------|---------------|-----------|-------|
| `backend.projects` | `backend/src/ai_life_backend/contracts/projects_openapi.yaml` | `GET/POST /api/projects`, `GET/PUT/DELETE /api/projects/{id}`, `GET/POST /api/tasks`, `GET/PUT/DELETE /api/tasks/{id}` | Includes dependency validation (DAG); cycle detection; filtered dependency lists |
| `backend.milestones` | `backend/src/ai_life_backend/contracts/milestones_openapi.yaml` | `GET/POST /api/milestones`, `GET/PUT/DELETE /api/milestones/{id}` | Milestone belongs to Goal only |

**Requirements**:
- `servers` present; `security: []` (explicit no-auth for MVP)
- Structured errors (RFC 7807 Problem Details) **recommended** but optional
- Pass `npx @redocly/cli lint`

### In-process ports (TS `.d.ts` / Python Protocols)

| Module | Contract Path | Exports | Notes |
|--------|---------------|---------|-------|
| `backend.projects` | `backend/src/ai_life_backend/contracts/projects_protocols.py` | `ProjectReader`, `TaskReader` (read-only query ports) | PEP 544 Protocols |
| `backend.milestones` | `backend/src/ai_life_backend/contracts/milestones_protocols.py` | `MilestoneReader` | PEP 544 Protocols |
| `frontend.projects` | `frontend/src/contracts/projects.d.ts` | React component types, hooks, utilities | TypeScript `.d.ts` |
| `frontend.milestones` | `frontend/src/contracts/milestones.d.ts` | React component types, hooks | TypeScript `.d.ts` |

## Vertical Steps (outline)

1. **Create new backend modules**: `backend.projects`, `backend.milestones`
   - Define OpenAPI contracts (entities, CRUD endpoints, dependency rules)
   - Define Python Protocols for in-process read-only ports
   - Register modules in `.specify/memory/public/registry.yaml`

2. **Implement backend domain logic** (TDD):
   - Models: Project, Task (with dependencies[], DAG validation), Milestone
   - Repositories: CRUD + dependency graph queries (detect cycles)
   - Services: business rules (e.g., Task dependencies scoped to Project, Project dependencies scoped to Goal)
   - API routes: FastAPI routers with RFC 7807 error handling

3. **Export & validate HTTP contracts**:
   - Run `backend/scripts/export_openapi.py` to generate OpenAPI YAML
   - Lint: `npx @redocly/cli lint backend/src/ai_life_backend/contracts/projects_openapi.yaml`
   - Lint: `npx @redocly/cli lint backend/src/ai_life_backend/contracts/milestones_openapi.yaml`

4. **Create new frontend modules**: `frontend.projects`, `frontend.milestones`
   - Define TypeScript contracts (`.d.ts`)
   - Register modules in `.specify/memory/public/registry.yaml`

5. **Implement frontend UI** (TDD):
   - List pages: Projects, Tasks, Milestones (default sort: `created_at DESC`)
   - Forms: Create/Edit with enum dropdowns (status, priority, size, energy, continuity, clarity, risk)
   - Dependency selectors: filtered lists (Tasks from same Project; Projects from same Goal)
   - Validation: required fields, cycle detection feedback
   - Delete flows: confirmation + dependency checks
   - API client hooks (fetch, mutate)

6. **Router integration** (`frontend.app-shell`):
   - Add routes: `/projects`, `/tasks`, `/milestones`
   - Wire up navigation links in app shell/sidebar
   - Update Next.js App Router glue in `frontend/src/app/**`

7. **Manifests & documentation**:
   - Create/update `docs/public/backend.projects.api.md`
   - Create/update `docs/public/backend.milestones.api.md`
   - Create/update `docs/public/frontend.projects.api.md`
   - Create/update `docs/public/frontend.milestones.api.md`
   - Update `docs/public/frontend.app-shell.api.md` (new routes)

8. **Quality gates**:
   - Backend: `pytest`, `ruff`, `mypy` (scoped to module paths)
   - Frontend: ESLint, `tsc`, unit tests (scoped to module paths)
   - Contract validation (OpenAPI lint, Protocol consistency)
   - SemVer bumps; Conventional Commits prepared

## Gates
- Registry/manifests/contracts exist and validate.
- No deep imports; consumers use only public surfaces.
- SemVer bump on public surface changes; Conventional Commits.
- Tests green (unit/integration/contract).
- Lint & type checks pass.

## Risks/Notes
- **New module creation**: Four new modules (`backend.projects`, `backend.milestones`, `frontend.projects`, `frontend.milestones`) require careful scaffolding and registry setup.
- **Dependency graph validation**: Cycle detection must be robust; consider graph traversal algorithms (DFS for cycle detection in DAG).
- **Dropdown UX**: Enum selectors must be clearly labeled and filterable (e.g., Task dependency dropdown shows only Tasks from same Project).
- **Standalone Projects**: UI must handle optional `goal_id` gracefully (e.g., Project form allows "No Goal" selection).
- **Migration risk**: If existing data exists, migration scripts may be needed (out of scope for this plan; address in implementation if required).
- **App Router glue**: Keep framework-specific code minimal in `frontend/src/app/**`; delegate logic to feature modules.

## Machine-readable Scope
<!-- TARGET_MODULES:BEGIN
backend.projects
backend.milestones
frontend.projects
frontend.milestones
frontend.app-shell
TARGET_MODULES:END -->
<!-- ROUTER_OWNER: frontend.app-shell -->
