# Module Task Plan: frontend.projects

**Feature ID**: `003-goal-projects-tasks-mvp`
**Module ID**: `frontend.projects`
**Module Kind**: `typescript`
**Contract**: `frontend/src/contracts/projects.d.ts`
**Import Hint**: `import * as projects from '@/features/projects'`
**Generated**: 2025-10-07

---

## Module Tasks

### MT001 @prio(P1) Define Projects/Tasks contract (TypeScript) [x] (done: 2025-10-07)
**Description**: Create `frontend/src/contracts/projects.d.ts` with public types: `ProjectsList`, `ProjectForm`, `TasksList`, `TaskForm`, `DependencySelector`, hooks (`useProjects`, `useTasks`, `useCreateProject`, `useUpdateProject`, `useDeleteProject`, `useCreateTask`, `useUpdateTask`, `useDeleteTask`).

**DoD**:
- Contract `.d.ts` exists with exported types
- Components: `ProjectsList`, `ProjectForm`, `TasksList`, `TaskForm`, `DependencySelector`
- Hooks: `useProjects`, `useTasks`, CRUD hooks for both entities
- Dependency selector types declared

### MT002 @prio(P1) Write tests for Projects/Tasks UI components and hooks [x] (done: 2025-10-07)
**Description**: Write tests for lists, forms, dependency selectors (Project→Project, Task→Task), all enum dropdowns (7 Task enums), delete confirmation, cycle detection error handling.

**DoD**:
- Tests cover: Project list, Project form, Task list, Task form
- Dependency selector tested (filtered options: same Goal for Projects, same Project for Tasks)
- All enum dropdowns tested (status, priority, size, energy, continuity, clarity, risk)
- Delete confirmation tested
- Cycle detection error handling tested (display cycle details from API)
- Tests green: `pnpm --filter frontend test projects`

### MT003 @prio(P1) Implement Projects/Tasks UI (lists + forms + dependency selectors) [x] (done: 2025-10-07)
**Description**: Implement `ProjectsList`, `ProjectForm`, `TasksList`, `TaskForm`, `DependencySelector` components. Implement API hooks. Use frontend.design components. Integrate Goal selector for Projects. Implement Task/Project dependency dropdowns with DAG validation feedback.

**DoD**:
- `ProjectsList` renders projects with columns (title, goal, status, priority, risk, dependencies count)
- `ProjectForm` with fields (title, goal_id dropdown, status/priority/risk dropdowns, scope, dependencies selector)
- `TasksList` renders tasks with columns (title, project, status, size, energy, continuity, clarity, risk, dependencies count)
- `TaskForm` with all fields + 7 enum dropdowns + dependency selector (Tasks within same Project)
- `DependencySelector` component filters options (same Goal for Projects, same Project for Tasks)
- Cycle detection errors displayed (parse RFC 7807 response, show cycle path)
- All tests green

### MT004 @prio(P1) Update manifest and bump SemVer [x] (done: 2025-10-07)
**Description**: Update `docs/public/frontend.projects.api.md` with components, hooks, usage. Bump SemVer. Validate manifest.

**DoD**:
- Manifest updated (Exports: components/hooks, Types, Usage)
- SemVer bumped in registry.yaml
- Manifest validates
- Prepared Conventional Commit message: `feat(frontend.projects): add Projects/Tasks UI with dependencies [public-api]`

### MT005 @prio(P1) Verify module [x] (done: 2025-10-07)
**Description**: Run all verification checks (docs-as-code, TypeScript, lint, boundaries) and ensure module meets quality gates.

**DoD**:
- Registry/manifest validation passes
- TypeScript type checking passes (0 errors)
- ESLint passes (critical errors fixed, acceptable warnings for form complexity)
- No deep imports (boundary compliance)
- Module status updated to "verified" in progress tracking