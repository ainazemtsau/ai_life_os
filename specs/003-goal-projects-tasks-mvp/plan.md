# Implementation Plan: Goals/Projects/Tasks MVP (CRUD + Dependencies)

**Branch**: `003-goal-projects-tasks-mvp` | **Date**: 2025-10-07 | **Spec**: spec.md
**Input**: Feature specification from /home/anton/code/ai_life_os/specs/003-goal-projects-tasks-mvp/spec.md

---

## Purpose
Freeze high-level design for this feature using **contracts-first**. The template is logic-less; the `/plan` runner injects all concrete details.

## Context & Constraints (from spec)
- **Scope**: CRUD for Goals, Milestones, Projects, Tasks with list + form pages only (no search, no detail views).
- **Dependencies**: Task→Task within same Project (DAG); Project→Project within same Goal (DAG); Goals have no dependencies.
- **Status**: Unified set (todo/doing/done/blocked) for all entities.
- **Enums**: Dropdowns for priority, status, size, energy, continuity, clarity, risk. Exclude mode, daypart_pref, outcome entirely.
- **Identifiers**: UUIDs (v4 recommended); Timestamps: RFC 3339 (UTC); API errors: RFC 7807 Problem Details.
- **Delete**: Requires confirmation; blocked when dependencies exist.
- **Frontend-only constraint**: Spec implies backend modules already exist; frontend modules are the primary target.

## Module Map (public surfaces only)

| Module ID               | Role        | Public Surface                                                                 | Import Hint                                 |
|-------------------------|-------------|--------------------------------------------------------------------------------|---------------------------------------------|
| **backend.core**        | Context     | Cross-cutting types, errors, utilities (no domain logic)                      | `from ai_life_backend.core.public import *` |
| **backend.goals**       | Context     | HTTP: GET/POST/PATCH/DELETE `/api/goals`; In-process: read-only queries       | `from ai_life_backend.goals.public import *`|
| **backend.milestones**  | **Target**  | HTTP: CRUD `/api/milestones`; In-process: read-only queries                   | `from ai_life_backend.milestones.public import *`|
| **backend.projects**    | **Target**  | HTTP: CRUD `/api/projects`, `/api/tasks`; In-process: read-only queries       | `from ai_life_backend.projects.public import *`|
| **frontend.design**     | Context     | Foundational design system (Button, Form, Input, Select, etc.)                | `import * as design from '@/features/design'`|
| **frontend.goals**      | Context     | Goals UI (list/forms); API client hooks for backend.goals                     | `import * as goals from '@/features/goals'` |
| **frontend.projects**   | **Target**  | Projects & Tasks UI: list pages, CRUD forms, dependency selectors             | `import * as projects from '@/features/projects'`|
| **frontend.milestones** | **Target**  | Milestones UI: list page, CRUD forms, Goal selector                           | `import * as milestones from '@/features/milestones'`|
| **frontend.app-shell**  | **Target**  | App shell, routing glue (owns `frontend/src/app/**`), nav integration         | `import * as appShell from '@/features/app-shell'`|

> Only surfaces listed above are public. Everything else is private implementation.

## Contracts
- HTTP contracts (OpenAPI 3.1), if any:

| Module ID              | Contract Path                                                     | Notes                                                                 |
|------------------------|-------------------------------------------------------------------|-----------------------------------------------------------------------|
| backend.milestones     | backend/src/ai_life_backend/contracts/milestones_openapi.yaml    | CRUD endpoints for Milestones; RFC 7807 error responses              |
| backend.projects       | backend/src/ai_life_backend/contracts/projects_openapi.yaml      | CRUD endpoints for Projects & Tasks; dependency validation (DAG)     |

- In-process ports (TS `.d.ts` / Python Protocols), if any:

| Module ID              | Contract Path                                   | Notes                                                   |
|------------------------|-------------------------------------------------|---------------------------------------------------------|
| frontend.projects      | frontend/src/contracts/projects.d.ts            | Public components/hooks for Projects/Tasks UI           |
| frontend.milestones    | frontend/src/contracts/milestones.d.ts          | Public components/hooks for Milestones UI               |
| frontend.app-shell     | frontend/src/contracts/app-shell.d.ts           | Navigation/routing integration points                   |

## Vertical Steps (outline)

1. **Backend.milestones**: Update or create OpenAPI contract for Milestone CRUD (`/api/milestones`); implement Goal association, status dropdown validation; export contract; write/update tests (unit + integration); update manifest + SemVer.

2. **Backend.projects**: Update or create OpenAPI contract for Project CRUD (`/api/projects`) and Task CRUD (`/api/tasks`); implement dependency validation (DAG for Task→Task within Project; DAG for Project→Project within Goal); add enum validators (status, priority, size, energy, continuity, clarity, risk); export contract; write/update tests (unit + integration + contract); update manifest + SemVer.

3. **Frontend.milestones**: Create list page (`/milestones`) with CRUD forms; integrate Goal selector (dropdown from backend.goals); use frontend.design components; implement API client hooks (fetch/create/edit/delete); export public components/hooks; update contract `.d.ts`; write tests; update manifest + SemVer.

4. **Frontend.projects**: Create list pages for Projects (`/projects`) and Tasks (`/tasks`); implement CRUD forms with dependency selectors (Task→Task within Project; Project→Project within Goal); integrate dropdowns for all enums; use frontend.design components; implement API client hooks; export public components/hooks; update contract `.d.ts`; write tests; update manifest + SemVer.

5. **Frontend.app-shell**: Add routes for `/milestones`, `/projects`, `/tasks` in `frontend/src/app/`; integrate navigation links; update public exports if needed; update contract `.d.ts`; write tests; update manifest + SemVer.

## Gates
- Registry/manifests/contracts exist and validate.
- No deep imports; consumers use only public surfaces.
- SemVer bump on public surface changes; Conventional Commits.
- OpenAPI contracts pass `npx @redocly/cli lint`.
- Tests green (unit/integration/contract); lint & type checks pass.
- DAG validation enforced for Task dependencies and Project dependencies.

## Risks/Notes
- **Spec constraint**: Feature is primarily frontend + backend API extension. Backend modules (milestones, projects) already exist in registry; implementation will likely extend them (not create from scratch).
- **Dependency validation complexity**: Cycle detection for Tasks (within Project) and Projects (within Goal) must be robust; recommend graph traversal utilities in backend.core or inline implementation with tests.
- **Enum proliferation**: Task entity has 7 enum fields (status, size, energy, continuity, clarity, risk, priority). Ensure dropdowns are consistent and validated both client and server side.
- **Delete confirmation UX**: Deleting records with dependencies requires explicit user flow (block + message, or guided removal). Frontend must handle 409/400 responses gracefully.
- **Frontend.app-shell minimal glue**: Keep routing integration minimal; avoid embedding business logic in `app/` files. Use public exports from feature modules.
- **Milestone-Project link**: Spec clarifies Milestones attach to Goals only (no direct Project link). Ensure this is reflected in contracts and UI.

## Machine-readable Scope
<!-- TARGET_MODULES:BEGIN
backend.milestones
backend.projects
frontend.milestones
frontend.projects
frontend.app-shell
TARGET_MODULES:END -->
<!-- ROUTER_OWNER: frontend.app-shell -->
