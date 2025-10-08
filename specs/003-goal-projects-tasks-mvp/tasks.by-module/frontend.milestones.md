# Module Task Plan: frontend.milestones

**Feature ID**: `003-goal-projects-tasks-mvp`
**Module ID**: `frontend.milestones`
**Module Kind**: `typescript`
**Contract**: `frontend/src/contracts/milestones.d.ts`
**Import Hint**: `import * as milestones from '@/features/milestones'`
**Generated**: 2025-10-07

---

## Module Tasks

### MT001 @prio(P1) Define Milestones contract (TypeScript) [x] (done: 2025-10-07)
**Description**: Create `frontend/src/contracts/milestones.d.ts` with public components/hooks types: `MilestonesList`, `MilestoneForm`, `useMilestones`, `useCreateMilestone`, `useUpdateMilestone`, `useDeleteMilestone`.

**DoD**:
- Contract `.d.ts` exists with exported types
- Components: `MilestonesList`, `MilestoneForm`
- Hooks: `useMilestones`, `useCreateMilestone`, `useUpdateMilestone`, `useDeleteMilestone`
- Goal selector integration declared

### MT002 @prio(P1) Write tests for Milestones UI components and hooks [x] (done: 2025-10-07)
**Description**: Write React Testing Library tests for `MilestonesList`, `MilestoneForm`, API hooks. Test Goal selector dropdown, status dropdown, delete confirmation, error handling (RFC 7807).

**DoD**:
- Tests cover: list rendering, form validation, Goal dropdown, status dropdown
- Delete confirmation tested
- API error handling tested (RFC 7807 responses)
- Tests green: `pnpm --filter frontend test milestones`

### MT003 @prio(P1) Implement Milestones UI (list + forms) [x] (done: 2025-10-07)
**Description**: Implement `MilestonesList` component (list page), `MilestoneForm` component (create/edit modal/page), API client hooks using `useSWR` or similar. Use `frontend.design` components. Integrate Goal selector from `frontend.goals`.

**DoD**:
- `MilestonesList` component renders list with columns (title, goal, due, status, blocking)
- `MilestoneForm` component with fields (title, goal_id dropdown, due, status dropdown, demo_criterion, blocking checkbox)
- API hooks implemented (fetch, create, update, delete)
- Goal selector integrated (dropdown from backend.goals)
- Uses frontend.design components (Button, Form, Input, Select)
- All tests green

### MT004 @prio(P1) Update manifest and bump SemVer [x] (done: 2025-10-07)
**Description**: Update `docs/public/frontend.milestones.api.md` with components, hooks, usage examples. Bump SemVer. Validate manifest.

**DoD**:
- Manifest updated (Exports: components/hooks, Types, Usage)
- SemVer bumped in registry.yaml
- Manifest validates
- Prepared Conventional Commit message: `feat(frontend.milestones): add Milestones UI [public-api]`

### MT005 @prio(P1) Verify module [x] (done: 2025-10-07)
**Description**: Run all verification checks (docs-as-code, TypeScript, lint, boundaries) and ensure module meets quality gates.

**DoD**:
- Registry/manifest validation passes
- TypeScript type checking passes (0 errors)
- ESLint passes (critical errors fixed, acceptable warnings)
- No deep imports (boundary compliance)
- Module status updated to "verified" in progress tracking