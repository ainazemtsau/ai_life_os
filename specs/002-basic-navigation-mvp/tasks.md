# Tasks: Basic Navigation MVP

**Feature**: `002-basic-navigation-mvp`
**Branch**: `002-basic-navigation-mvp`
**Plan**: [plan.md](./plan.md)

---

## Module API Matrix (Target Modules Only)

| Module | Import Hint | Contract |
|--------|-------------|----------|
| frontend.dashboard | `import * as dashboard from '@/features/dashboard'` | `frontend/src/contracts/dashboard.d.ts` |
| frontend.app-shell | `import * as appShell from '@/features/app-shell'` | `frontend/src/contracts/app-shell.d.ts` |

---

## Preparation

### T000 @prio(P1) Bootstrap missing modules
Bootstrap new modules `frontend.dashboard` and `frontend.app-shell` via module-bootstrap command:
```bash
/module-bootstrap FROM_TASKS=002-basic-navigation-mvp
```
This will create registry entries, manifests, contracts, and folder scaffolds for both modules.

### T001 @prio(P1) Validate registry and manifests
Run registry and manifest validators to ensure all modules are properly registered:
```bash
# Run registry validation
# Run manifest linting (when available)
```

---

## Module: frontend.dashboard

### T002 @prio(P1) @module(frontend.dashboard) Define dashboard contract
Define TypeScript contract in `frontend/src/contracts/dashboard.d.ts`:
- Dashboard page component type
- Props interface for dashboard configuration
- Export types for public consumption

### T003 @prio(P1) @module(frontend.dashboard) Write dashboard component tests
Create test file with specs for:
- Dashboard renders with greeting message
- Dashboard displays placeholder information
- Dashboard includes navigation link to Goals
- Component accepts and uses props correctly

### T004 @prio(P1) @module(frontend.dashboard) Implement dashboard component
Implement dashboard page component:
- Greeting message display
- Placeholder content section
- Navigation button/link to "/goals" route
- Use `frontend.design` public API for UI components (Button, Card, Typography)
- Export via public hub pattern

### T005 @prio(P1) @module(frontend.dashboard) Update dashboard manifest
Update `docs/public/frontend.dashboard.api.md`:
- Document exported components (DashboardPage)
- Document types and interfaces
- Add usage examples with namespace imports
- Update changelog with initial version

### T006 @prio(P1) @module(frontend.dashboard) Verify dashboard module
Run module verification:
- Tests pass
- Type checks pass
- Contract matches implementation
- Manifest is up-to-date
- SemVer is appropriate (0.1.0 for initial)

---

## Module: frontend.app-shell

### T007 @prio(P1) @module(frontend.app-shell) Define app-shell contract
Define TypeScript contract in `frontend/src/contracts/app-shell.d.ts`:
- Root layout component type
- Theme configuration types
- Navigation/routing types
- Export types for public consumption

### T008 @prio(P1) @module(frontend.app-shell) Write app-shell component tests
Create test file with specs for:
- Root layout renders with dark theme
- Theme is applied correctly to children
- Layout structure is correct
- AppLayout component functionality

### T009 @prio(P1) @module(frontend.app-shell) Implement app-shell layout
Implement root layout component:
- Create AppLayout wrapper component
- Configure dark theme by default
- Export via public hub pattern
- Ensure theme consistency across all pages

### T010 @prio(P1) @module(frontend.app-shell) Update app-shell manifest
Update `docs/public/frontend.app-shell.api.md`:
- Document exported components (AppLayout, theme utilities)
- Document types and interfaces
- Add usage examples with namespace imports
- Update changelog with initial version

### T011 @prio(P1) @module(frontend.app-shell) Verify app-shell module
Run module verification:
- Tests pass
- Type checks pass
- Contract matches implementation
- Manifest is up-to-date
- SemVer is appropriate (0.1.0 for initial)

---

## Integration (Next.js App Router)

### T012 @prio(P1) @module(frontend.app-shell) Enable dark theme globally
Update `frontend/src/app/layout.tsx`:
- Add `className="dark"` to root html element
- Wrap children with AppLayout component from app-shell
- Ensure dark theme is applied consistently

### T013 @prio(P1) @module(frontend.app-shell) Wire "/" route with DashboardRoute
Create `frontend/src/app/page.tsx`:
- Import DashboardRoute from `@/features/app-shell` using namespace import
- Wire route to render DashboardRoute component
- Ensure dark theme applies correctly

### T014 @prio(P1) @module(frontend.app-shell) Wire "/goals" route with GoalsRoute
Update `frontend/src/app/goals/page.tsx`:
- Import GoalsRoute from `@/features/app-shell` using namespace import
- Wire route to render GoalsRoute component
- Verify routing from Dashboard works correctly
- Test browser navigation (back/forward, direct URL)

---

## Definition of Done

For each module:
- [ ] Tests pass (unit tests for components)
- [ ] Type checks pass (`tsc --noEmit`)
- [ ] Contract (`.d.ts`) exists and matches implementation
- [ ] Manifest updated with public API documentation
- [ ] SemVer bumped appropriately (0.1.0 for new modules)
- [ ] No deep imports (consumers use namespace imports only)
- [ ] Lint passes (ESLint)

For integration:
- [ ] Dark theme applied globally
- [ ] "/" route renders Dashboard
- [ ] "/goals" route accessible from Dashboard in one click
- [ ] Browser navigation works (back/forward/direct URL)
- [ ] All acceptance scenarios from spec pass

---

## Next Steps

1. Run `/module-bootstrap FROM_TASKS=002-basic-navigation-mvp` to bootstrap missing modules
2. For each module, run `/module-implement MODULE=<module-id>` in order:
   - `/module-implement MODULE=frontend.dashboard`
   - `/module-implement MODULE=frontend.app-shell`
3. Verify integration tasks manually or via E2E tests
4. Run `/module-verify MODULE=<module-id>` for final validation
