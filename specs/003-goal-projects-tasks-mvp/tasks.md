# Global Task Plan: Goals/Projects/Tasks MVP (CRUD + Dependencies)

**Feature ID**: `003-goal-projects-tasks-mvp`
**Branch**: `003-goal-projects-tasks-mvp`
**Generated**: 2025-10-07

---

## Target Modules (5)

| Module ID              | Kind       | Contract                                                     | Import Hint                                      |
|------------------------|------------|--------------------------------------------------------------|--------------------------------------------------|
| backend.milestones     | python     | backend/src/ai_life_backend/contracts/milestones_openapi.yaml | `from ai_life_backend.milestones.public import *` |
| backend.projects       | python     | backend/src/ai_life_backend/contracts/projects_openapi.yaml   | `from ai_life_backend.projects.public import *`   |
| frontend.milestones    | typescript | frontend/src/contracts/milestones.d.ts                        | `import * as milestones from '@/features/milestones'` |
| frontend.projects      | typescript | frontend/src/contracts/projects.d.ts                          | `import * as projects from '@/features/projects'`   |
| frontend.app-shell     | typescript | frontend/src/contracts/app-shell.d.ts                         | `import * as appShell from '@/features/app-shell'` |

**Router Owner**: `frontend.app-shell`

---

## Tasks (TDD + Integration)

### T001 @prio(P1) @module(backend.milestones) Define Milestone OpenAPI contract
**Description**: Create or update `milestones_openapi.yaml` with CRUD endpoints (`GET /api/milestones`, `POST /api/milestones`, `PATCH /api/milestones/{id}`, `DELETE /api/milestones/{id}`). Include Goal association (`goal_id`), unified status enum (todo/doing/done/blocked), RFC 7807 error responses, RFC 3339 timestamps, UUIDs.

**DoD**:
- OpenAPI 3.1 contract exists at contract path
- All required fields defined (id, goal_id, title, due?, status, demo_criterion, blocking, created_at, updated_at)
- Status enum: [todo, doing, done, blocked]
- Error responses follow RFC 7807 (type, title, status, detail, instance)
- Contract passes: `npx @redocly/cli lint backend/src/ai_life_backend/contracts/milestones_openapi.yaml`

---

### T002 @prio(P1) @module(backend.milestones) Write contract tests for Milestone API
**Description**: Write contract/integration tests that verify Milestone CRUD endpoints against the OpenAPI spec. Test Goal association validation, status transitions, RFC 7807 error responses, delete with dependencies blocked.

**DoD**:
- Tests cover: GET list, POST create, PATCH update, DELETE
- Goal association validated (goal_id must exist)
- Status enum validated (reject invalid values)
- Delete blocked when dependencies exist (or require confirmation flow)
- Error responses match RFC 7807 structure
- Tests green: `pytest backend/tests/integration/test_milestones_api.py`

---

### T003 @prio(P1) @module(backend.milestones) Implement Milestone CRUD service and router
**Description**: Implement SQLAlchemy model, service layer (CRUD operations, Goal validation), FastAPI router. Export OpenAPI spec via script. Ensure DAG validation if milestone dependencies are added later.

**DoD**:
- SQLAlchemy model matches contract schema
- Alembic migration created for milestones table
- Service layer implements CRUD + Goal validation
- FastAPI router wired; responses match OpenAPI spec
- OpenAPI exported: `uv run python backend/scripts/export_openapi.py`
- All tests green (unit + integration)

---

### T004 @prio(P1) @module(backend.milestones) Update manifest and bump SemVer
**Description**: Update `docs/public/backend.milestones.api.md` with new/updated exports, types, usage examples. Bump SemVer (MINOR if additive, MAJOR if breaking). Validate manifest.

**DoD**:
- Manifest updated (Exports, Types, Usage, Changelog)
- SemVer bumped in registry.yaml
- Manifest validates (no errors)
- Prepared Conventional Commit message: `feat(backend.milestones): add Milestone CRUD API [public-api]`

---

### T005 @prio(P1) @module(backend.projects) Update Project/Task OpenAPI contract with dependencies
**Description**: Update `projects_openapi.yaml` to include Project dependencies (within same Goal, DAG), Task dependencies (within same Project, DAG), all enums (status, priority, size, energy, continuity, clarity, risk), RFC 7807 errors.

**DoD**:
- Project schema includes: `dependencies` (array of Project IDs), `goal_id?` (nullable)
- Task schema includes: `dependencies` (array of Task IDs within same Project), enums (status, size, energy, continuity, clarity, risk)
- Dependency validation rules documented (DAG, same Goal/Project)
- Error responses for cycle detection (400/409 with cycle details)
- Contract passes: `npx @redocly/cli lint backend/src/ai_life_backend/contracts/projects_openapi.yaml`

---

### T006 @prio(P1) @module(backend.projects) Write contract tests for Project/Task dependencies and enums
**Description**: Write tests for dependency validation (cycle detection for Projects and Tasks), enum validation (all 7 Task enums), delete with dependencies blocked, RFC 7807 error responses.

**DoD**:
- Tests cover: Project→Project dependencies (DAG within Goal), Task→Task dependencies (DAG within Project)
- Cycle detection tested (reject cycles with clear error)
- Enum validation tested (all Task enums: size, energy, continuity, clarity, risk)
- Delete blocked when dependencies exist
- Tests green: `pytest backend/tests/integration/test_projects_api.py`

---

### T007 @prio(P1) @module(backend.projects) Implement dependency validation and DAG enforcement
**Description**: Implement graph traversal utilities (cycle detection) for Project and Task dependencies. Update service layer with dependency validation. Update SQLAlchemy models with dependency relations.

**DoD**:
- DAG validation utility functions (detect cycles, validate same Goal/Project constraints)
- SQLAlchemy models updated (dependency foreign keys, join tables if needed)
- Alembic migration for dependency columns/tables
- Service layer enforces DAG on create/update
- Enum validators for all Task fields (status, size, energy, continuity, clarity, risk)
- All tests green (unit + integration)

---

### T008 @prio(P1) @module(backend.projects) Update manifest and bump SemVer
**Description**: Update `docs/public/backend.projects.api.md` with dependency fields, enums, usage examples. Bump SemVer. Validate manifest.

**DoD**:
- Manifest updated (dependency fields, enum types, usage)
- SemVer bumped in registry.yaml
- Manifest validates
- Prepared Conventional Commit message: `feat(backend.projects): add Project/Task dependencies and enums [public-api]`

---

### T009 @prio(P1) @module(frontend.milestones) Define Milestones contract (TypeScript)
**Description**: Create `frontend/src/contracts/milestones.d.ts` with public components/hooks types: `MilestonesList`, `MilestoneForm`, `useMilestones`, `useCreateMilestone`, `useUpdateMilestone`, `useDeleteMilestone`.

**DoD**:
- Contract `.d.ts` exists with exported types
- Components: `MilestonesList`, `MilestoneForm`
- Hooks: `useMilestones`, `useCreateMilestone`, `useUpdateMilestone`, `useDeleteMilestone`
- Goal selector integration declared

---

### T010 @prio(P1) @module(frontend.milestones) Write tests for Milestones UI components and hooks
**Description**: Write React Testing Library tests for `MilestonesList`, `MilestoneForm`, API hooks. Test Goal selector dropdown, status dropdown, delete confirmation, error handling (RFC 7807).

**DoD**:
- Tests cover: list rendering, form validation, Goal dropdown, status dropdown
- Delete confirmation tested
- API error handling tested (RFC 7807 responses)
- Tests green: `pnpm --filter frontend test milestones`

---

### T011 @prio(P1) @module(frontend.milestones) Implement Milestones UI (list + forms)
**Description**: Implement `MilestonesList` component (list page), `MilestoneForm` component (create/edit modal/page), API client hooks using `useSWR` or similar. Use `frontend.design` components. Integrate Goal selector from `frontend.goals`.

**DoD**:
- `MilestonesList` component renders list with columns (title, goal, due, status, blocking)
- `MilestoneForm` component with fields (title, goal_id dropdown, due, status dropdown, demo_criterion, blocking checkbox)
- API hooks implemented (fetch, create, update, delete)
- Goal selector integrated (dropdown from backend.goals)
- Uses frontend.design components (Button, Form, Input, Select)
- All tests green

---

### T012 @prio(P1) @module(frontend.milestones) Update manifest and bump SemVer
**Description**: Update `docs/public/frontend.milestones.api.md` with components, hooks, usage examples. Bump SemVer. Validate manifest.

**DoD**:
- Manifest updated (Exports: components/hooks, Types, Usage)
- SemVer bumped in registry.yaml
- Manifest validates
- Prepared Conventional Commit message: `feat(frontend.milestones): add Milestones UI [public-api]`

---

### T013 @prio(P1) @module(frontend.projects) Define Projects/Tasks contract (TypeScript)
**Description**: Create `frontend/src/contracts/projects.d.ts` with public types: `ProjectsList`, `ProjectForm`, `TasksList`, `TaskForm`, `DependencySelector`, hooks (`useProjects`, `useTasks`, `useCreateProject`, `useUpdateProject`, `useDeleteProject`, `useCreateTask`, `useUpdateTask`, `useDeleteTask`).

**DoD**:
- Contract `.d.ts` exists with exported types
- Components: `ProjectsList`, `ProjectForm`, `TasksList`, `TaskForm`, `DependencySelector`
- Hooks: `useProjects`, `useTasks`, CRUD hooks for both entities
- Dependency selector types declared

---

### T014 @prio(P1) @module(frontend.projects) Write tests for Projects/Tasks UI components and hooks
**Description**: Write tests for lists, forms, dependency selectors (Project→Project, Task→Task), all enum dropdowns (7 Task enums), delete confirmation, cycle detection error handling.

**DoD**:
- Tests cover: Project list, Project form, Task list, Task form
- Dependency selector tested (filtered options: same Goal for Projects, same Project for Tasks)
- All enum dropdowns tested (status, priority, size, energy, continuity, clarity, risk)
- Delete confirmation tested
- Cycle detection error handling tested (display cycle details from API)
- Tests green: `pnpm --filter frontend test projects`

---

### T015 @prio(P1) @module(frontend.projects) Implement Projects/Tasks UI (lists + forms + dependency selectors)
**Description**: Implement `ProjectsList`, `ProjectForm`, `TasksList`, `TaskForm`, `DependencySelector` components. Implement API hooks. Use frontend.design components. Integrate Goal selector for Projects. Implement Task/Project dependency dropdowns with DAG validation feedback.

**DoD**:
- `ProjectsList` renders projects with columns (title, goal, status, priority, risk, dependencies count)
- `ProjectForm` with fields (title, goal_id dropdown, status/priority/risk dropdowns, scope, dependencies selector)
- `TasksList` renders tasks with columns (title, project, status, size, energy, continuity, clarity, risk, dependencies count)
- `TaskForm` with all fields + 7 enum dropdowns + dependency selector (Tasks within same Project)
- `DependencySelector` component filters options (same Goal for Projects, same Project for Tasks)
- Cycle detection errors displayed (parse RFC 7807 response, show cycle path)
- All tests green

---

### T016 @prio(P1) @module(frontend.projects) Update manifest and bump SemVer
**Description**: Update `docs/public/frontend.projects.api.md` with components, hooks, usage. Bump SemVer. Validate manifest.

**DoD**:
- Manifest updated (Exports: components/hooks, Types, Usage)
- SemVer bumped in registry.yaml
- Manifest validates
- Prepared Conventional Commit message: `feat(frontend.projects): add Projects/Tasks UI with dependencies [public-api]`

---

### T017 @prio(P1) @module(frontend.app-shell) Add routes for Milestones, Projects, Tasks
**Description**: Add Next.js App Router pages: `/milestones/page.tsx`, `/projects/page.tsx`, `/tasks/page.tsx`. Wire with feature module components. Add navigation links. Keep glue minimal (no business logic in `app/`).

**DoD**:
- Pages exist: `frontend/src/app/milestones/page.tsx`, `frontend/src/app/projects/page.tsx`, `frontend/src/app/tasks/page.tsx`
- Pages import and render feature components: `<milestones.MilestonesList />`, `<projects.ProjectsList />`, `<projects.TasksList />`
- Navigation links added (sidebar/header) for `/milestones`, `/projects`, `/tasks`
- No business logic in page files (delegate to feature modules)
- Tests green (routing tests)

---

### T018 @prio(P1) @module(frontend.app-shell) Update manifest and bump SemVer
**Description**: Update `docs/public/frontend.app-shell.api.md` with new routes. Bump SemVer. Validate manifest.

**DoD**:
- Manifest updated (new routes documented)
- SemVer bumped in registry.yaml
- Manifest validates
- Prepared Conventional Commit message: `feat(frontend.app-shell): add routes for Milestones, Projects, Tasks [public-api]`

---

## Validation Checklist
- [ ] All Target Modules are in the registry (no bootstrap needed)
- [ ] All tasks tagged with correct module
- [ ] Integration tasks (T017-T018) tagged with router-owner (`frontend.app-shell`)
- [ ] No context modules (backend.core, backend.goals, frontend.design, frontend.goals, frontend.dashboard) in tasks
- [ ] Frontend import hints use namespace style (`import * as <name> from '@/features/<name>'`)
- [ ] TDD order: contract → tests → implement → manifest → verify

---

## Next Steps
All target modules exist in registry. No bootstrap needed.

**Proceed with**:
```bash
# Implement each module in sequence
/module-implement MODULE=backend.milestones
/module-implement MODULE=backend.projects
/module-implement MODULE=frontend.milestones
/module-implement MODULE=frontend.projects
/module-implement MODULE=frontend.app-shell
```

Or fan out tasks to per-module playbooks:
```bash
/fanout-tasks 003-goal-projects-tasks-mvp
```
