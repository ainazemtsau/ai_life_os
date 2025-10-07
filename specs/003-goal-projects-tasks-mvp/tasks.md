# Tasks: Goals/Projects/Tasks MVP

**Scope**: Target modules only (from plan.md Machine-readable Scope).
**Source**: plan.md + registry.yaml + spec.md.

---

## Module API Matrix (Target Modules)
| Module ID | Kind | Uses | Manifest | Contract | Import Hint | SemVer |
|-----------|------|------|----------|----------|-------------|--------|
| `backend.projects` | python | backend.core | docs/public/backend.projects.api.md | backend/src/ai_life_backend/contracts/projects_openapi.yaml | `from ai_life_backend.projects.public import *` | 0.1.0 |
| `backend.milestones` | python | backend.core, backend.goals | docs/public/backend.milestones.api.md | backend/src/ai_life_backend/contracts/milestones_openapi.yaml | `from ai_life_backend.milestones.public import *` | 0.1.0 |
| `frontend.projects` | typescript | frontend.design, backend.projects | docs/public/frontend.projects.api.md | frontend/src/contracts/projects.d.ts | `import * as projects from '@/features/projects'` | 0.1.0 |
| `frontend.milestones` | typescript | frontend.design, backend.milestones, backend.goals | docs/public/frontend.milestones.api.md | frontend/src/contracts/milestones.d.ts | `import * as milestones from '@/features/milestones'` | 0.1.0 |
| `frontend.app-shell` | typescript | frontend.dashboard, frontend.goals, frontend.projects, frontend.milestones | docs/public/frontend.app-shell.api.md | frontend/src/contracts/app-shell.d.ts | `import * as appShell from '@/features/app-shell'` | 0.1.0 |

---

## Preparation
- [ ] T000 @prio(P1) Bootstrap missing modules via `/module-bootstrap FROM_TASKS=003-goal-projects-tasks-mvp`
- [ ] T001 @prio(P1) Validate docs-as-code:
      ```bash
      python .specify/scripts/registry_validate.py
      python .specify/scripts/manifest_lint.py
      ```

---

## Global Tasks (TDD-first)

### backend.projects
- [ ] T002 **Define OpenAPI contract for Projects & Tasks** @module(backend.projects) @prio(P1)
  - Define schemas: Project, Task, dependency structures
  - Define endpoints: GET/POST /api/projects, GET/PUT/DELETE /api/projects/{id}
  - Define endpoints: GET/POST /api/tasks, GET/PUT/DELETE /api/tasks/{id}
  - Include DAG validation rules, cycle detection, filtered dependency lists
  - Ensure `servers` present, `security: []`, RFC 7807 error schemas

- [ ] T003 **Define in-process Protocols for Projects & Tasks** @module(backend.projects) @prio(P1)
  - Create `backend/src/ai_life_backend/contracts/projects_protocols.py`
  - Define `ProjectReader`, `TaskReader` (PEP 544 Protocols)

- [ ] T004 **Write tests for backend.projects** @module(backend.projects) @prio(P1) [TDD]
  - Unit tests: models, repository CRUD, DAG validation, cycle detection
  - Integration tests: API endpoints, dependency filtering, error responses
  - Contract tests: OpenAPI compliance

- [ ] T005 **Implement backend.projects** @module(backend.projects) @prio(P1)
  - Models: Project, Task with dependencies[] (DAG validation)
  - Repository: CRUD + dependency graph queries (DFS cycle detection)
  - Services: business rules (Task dependencies scoped to Project; Project dependencies scoped to Goal)
  - API routes: FastAPI routers with RFC 7807 error handling
  - Public re-exports in `ai_life_backend.projects.public`

- [ ] T006 **Update manifest for backend.projects** @module(backend.projects) @prio(P1)
  - Create `docs/public/backend.projects.api.md`
  - Document: Overview, Exports, Types, HTTP endpoints, Usage, Changelog
  - Bump SemVer to 0.1.0

- [ ] T007 **Verify backend.projects** @module(backend.projects) @prio(P1)
  - Run `pytest` (scoped to module paths)
  - Run `ruff`, `mypy`
  - Export OpenAPI: `python backend/scripts/export_openapi.py`
  - Lint OpenAPI: `npx @redocly/cli lint backend/src/ai_life_backend/contracts/projects_openapi.yaml`

### backend.milestones
- [ ] T008 **Define OpenAPI contract for Milestones** @module(backend.milestones) @prio(P1)
  - Define schema: Milestone (belongs to Goal only)
  - Define endpoints: GET/POST /api/milestones, GET/PUT/DELETE /api/milestones/{id}
  - Ensure `servers` present, `security: []`, RFC 7807 error schemas

- [ ] T009 **Define in-process Protocols for Milestones** @module(backend.milestones) @prio(P1)
  - Create `backend/src/ai_life_backend/contracts/milestones_protocols.py`
  - Define `MilestoneReader` (PEP 544 Protocol)

- [ ] T010 **Write tests for backend.milestones** @module(backend.milestones) @prio(P1) [TDD]
  - Unit tests: models, repository CRUD, Goal relationship validation
  - Integration tests: API endpoints, error responses
  - Contract tests: OpenAPI compliance

- [ ] T011 **Implement backend.milestones** @module(backend.milestones) @prio(P1)
  - Model: Milestone with goal_id (required)
  - Repository: CRUD + Goal foreign key validation
  - Services: business rules (Milestone belongs to Goal only)
  - API routes: FastAPI routers with RFC 7807 error handling
  - Public re-exports in `ai_life_backend.milestones.public`

- [ ] T012 **Update manifest for backend.milestones** @module(backend.milestones) @prio(P1)
  - Create `docs/public/backend.milestones.api.md`
  - Document: Overview, Exports, Types, HTTP endpoints, Usage, Changelog
  - Bump SemVer to 0.1.0

- [ ] T013 **Verify backend.milestones** @module(backend.milestones) @prio(P1)
  - Run `pytest` (scoped to module paths)
  - Run `ruff`, `mypy`
  - Export OpenAPI: `python backend/scripts/export_openapi.py`
  - Lint OpenAPI: `npx @redocly/cli lint backend/src/ai_life_backend/contracts/milestones_openapi.yaml`

### frontend.projects
- [ ] T014 **Define TypeScript contract for Projects & Tasks UI** @module(frontend.projects) @prio(P1)
  - Create `frontend/src/contracts/projects.d.ts`
  - Define types: Project, Task, dependency structures
  - Define component types, hooks (useProjects, useTasks), utilities

- [ ] T015 **Write tests for frontend.projects** @module(frontend.projects) @prio(P1) [TDD]
  - Unit tests: components, hooks, dependency selector logic
  - Integration tests: form validation, cycle detection feedback, API client
  - Accessibility tests: dropdown navigation, screen reader support

- [ ] T016 **Implement frontend.projects** @module(frontend.projects) @prio(P1)
  - List pages: Projects, Tasks (default sort: created_at DESC)
  - Forms: Create/Edit with enum dropdowns (status, priority, risk, size, energy, continuity, clarity)
  - Dependency selectors: filtered lists (Tasks from same Project; Projects from same Goal)
  - Validation: required fields, cycle detection feedback
  - Delete flows: confirmation + dependency checks
  - API client hooks (fetch, mutate)
  - Public re-exports in namespace

- [ ] T017 **Update manifest for frontend.projects** @module(frontend.projects) @prio(P1)
  - Create `docs/public/frontend.projects.api.md`
  - Document: Overview, Exports, Components, Hooks, Usage, Changelog
  - Bump SemVer to 0.1.0

- [ ] T018 **Verify frontend.projects** @module(frontend.projects) @prio(P1)
  - Run ESLint (scoped to module paths)
  - Run `tsc` typecheck
  - Run unit tests

### frontend.milestones
- [ ] T019 **Define TypeScript contract for Milestones UI** @module(frontend.milestones) @prio(P1)
  - Create `frontend/src/contracts/milestones.d.ts`
  - Define types: Milestone, Goal relationship
  - Define component types, hooks (useMilestones)

- [ ] T020 **Write tests for frontend.milestones** @module(frontend.milestones) @prio(P1) [TDD]
  - Unit tests: components, hooks, Goal selector logic
  - Integration tests: form validation, API client
  - Accessibility tests

- [ ] T021 **Implement frontend.milestones** @module(frontend.milestones) @prio(P1)
  - List page: Milestones (default sort: created_at DESC)
  - Forms: Create/Edit with enum dropdown (status), Goal selector
  - Validation: required fields (title, goal_id)
  - Delete flows: confirmation
  - API client hooks (fetch, mutate)
  - Public re-exports in namespace

- [ ] T022 **Update manifest for frontend.milestones** @module(frontend.milestones) @prio(P1)
  - Create `docs/public/frontend.milestones.api.md`
  - Document: Overview, Exports, Components, Hooks, Usage, Changelog
  - Bump SemVer to 0.1.0

- [ ] T023 **Verify frontend.milestones** @module(frontend.milestones) @prio(P1)
  - Run ESLint (scoped to module paths)
  - Run `tsc` typecheck
  - Run unit tests

### Integration (Next.js router glue)
- [ ] T024 **Wire /projects route** @module(frontend.app-shell) @prio(P1)
  - Create `frontend/src/app/projects/page.tsx`
  - Import ProjectsListPage from `@/features/projects`
  - Add navigation link in sidebar

- [ ] T025 **Wire /tasks route** @module(frontend.app-shell) @prio(P1)
  - Create `frontend/src/app/tasks/page.tsx`
  - Import TasksListPage from `@/features/projects`
  - Add navigation link in sidebar

- [ ] T026 **Wire /milestones route** @module(frontend.app-shell) @prio(P1)
  - Create `frontend/src/app/milestones/page.tsx`
  - Import MilestonesListPage from `@/features/milestones`
  - Add navigation link in sidebar

- [ ] T027 **Update manifest for frontend.app-shell** @module(frontend.app-shell) @prio(P1)
  - Update `docs/public/frontend.app-shell.api.md`
  - Document new routes: /projects, /tasks, /milestones
  - Bump SemVer (MINOR: additive change)

- [ ] T028 **Verify frontend.app-shell** @module(frontend.app-shell) @prio(P1)
  - Run ESLint (scoped to module paths)
  - Run `tsc` typecheck
  - Verify routing works in dev mode

---

## Gates
- TDD, no deep imports, manifests & semver synced, CI (lint/typecheck) passes.
- All modules reach READY (tests green, contracts validated, manifests updated).

## Next
Run: `/module-bootstrap FROM_TASKS=003-goal-projects-tasks-mvp`
