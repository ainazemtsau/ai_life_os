# Implementation Plan: Basic Navigation MVP

**Branch**: 002-basic-navigation-mvp | **Date**: 2025-10-06 | **Spec**: specs/002-basic-navigation-mvp/spec.md

**Input**: Feature specification from /home/anton/code/ai_life_os/specs/002-basic-navigation-mvp/spec.md

---

## Purpose

Freeze high-level design for this feature using **contracts-first**. Keep template logic-less: all module/data details are injected by the /plan runner.

## Context & Constraints (from spec)

This feature establishes a Dashboard page as the application's entry point at the root path ("/"), providing users with a greeting and placeholder information. Users must be able to navigate from the Dashboard to the existing Goals page ("/goals") in a single click. The entire application must render in dark theme by default, with no theme switcher in this iteration.

**Constraints:**
- Frontend-only implementation (no backend changes)
- Reuse existing modules where possible
- Single-user context
- Dark theme must be the default across all pages
- Simple and clean UX
- Prepare navigation infrastructure for future complexity

## Module Map (auto-generated)

| Module ID | Kind | Version | Provides | Uses | Manifest | Contract | Allowed Dirs | Import Hint |
|-----------|------|---------|----------|------|----------|----------|--------------|-------------|
| **backend.core** | python | 0.1.0 | Cross-cutting primitives (types, errors, utilities) | - | docs/public/backend.core.api.md | backend/src/ai_life_backend/contracts/core_protocols.py | backend/src/ai_life_backend/core/**, backend/tests/core/** | from ai_life_backend.core.public import * |
| **backend.goals** | python | 0.1.0 | Goals feature (HTTP + in-process queries) | - | docs/public/backend.goals.api.md | backend/src/ai_life_backend/contracts/goals_openapi.yaml | backend/src/ai_life_backend/goals/**, backend/tests/goals/** | from ai_life_backend.goals.public import * |
| **frontend.design** | typescript | 0.1.0 | Foundational design system | - | docs/public/frontend.design.api.md | frontend/src/contracts/design.d.ts | frontend/src/features/design/**, frontend/src/contracts/design.d.ts | import * as design from '@/features/design' |
| **frontend.goals** | typescript | 0.1.0 | Goals UI | frontend.design, backend.goals | docs/public/frontend.goals.api.md | frontend/src/contracts/goals.d.ts | frontend/src/features/goals/**, frontend/src/contracts/goals.d.ts | import * as goals from '@/features/goals' |

> Only surfaces listed above are public. Everything else is private implementation.

## Contracts

- HTTP contracts (OpenAPI 3.1) for modules that expose HTTP:

| Module | Contract Path | Purpose |
|--------|---------------|---------|
| backend.goals | backend/src/ai_life_backend/contracts/goals_openapi.yaml | Goals CRUD operations over HTTP |

- In-process ports (typed DTO/functions) for same-process consumption:

| Module | Contract Path | Purpose |
|--------|---------------|---------|
| backend.core | backend/src/ai_life_backend/contracts/core_protocols.py | Core primitives and protocols |
| frontend.design | frontend/src/contracts/design.d.ts | Design system components and types |
| frontend.goals | frontend/src/contracts/goals.d.ts | Goals UI components and types |

## Vertical Steps (outline)

### 1. Create Dashboard Module (NEW)

**Module**: frontend.dashboard (NEW)

- **Registry entry**: Add frontend.dashboard to .specify/memory/public/registry.yaml
  - kind: typescript
  - semver: 0.1.0
  - manifest: docs/public/frontend.dashboard.api.md
  - contract: frontend/src/contracts/dashboard.d.ts
  - import_hint: import { DashboardPage } from '@/features/dashboard'
  - allowed_dirs:
    - frontend/src/features/dashboard/**
    - frontend/src/contracts/dashboard.d.ts
    - docs/public/frontend.dashboard.api.md
  - uses: [frontend.design]

- **Contract**: Create frontend/src/contracts/dashboard.d.ts
  ```typescript
  export interface DashboardPageProps {
    // Props if needed in future
  }
  export function DashboardPage(props: DashboardPageProps): JSX.Element;
  ```

- **Manifest**: Create docs/public/frontend.dashboard.api.md
  - Document: DashboardPage component and its purpose
  - No internal components exposed (all private)

- **Implementation**:
  - `frontend/src/features/dashboard/pages/DashboardPage.tsx`
    - Greeting: "Welcome to AI Life OS"
    - Placeholder: "Your personal productivity companion"
    - Navigation button: "View Goals" (Next.js Link to "/goals")
    - Use Card, Button from design system
  - `frontend/src/features/dashboard/index.ts`
    - Export only: `DashboardPage`

**Why this design:**
- Dashboard is a feature module, same level as Goals
- Self-contained, reusable page component
- App-shell decides when/where to render it

---

### 2. Create App Shell Module (NEW)

**Module**: frontend.app-shell (NEW)

- **Registry entry**: Add frontend.app-shell to .specify/memory/public/registry.yaml
  - kind: typescript
  - semver: 0.1.0
  - manifest: docs/public/frontend.app-shell.api.md
  - contract: frontend/src/contracts/app-shell.d.ts
  - import_hint: import { AppLayout, DashboardRoute, GoalsRoute } from '@/features/app-shell'
  - allowed_dirs:
    - frontend/src/features/app-shell/**
    - frontend/src/contracts/app-shell.d.ts
    - docs/public/frontend.app-shell.api.md
  - uses: [frontend.design, frontend.dashboard, frontend.goals]

- **Contract**: Create frontend/src/contracts/app-shell.d.ts
  ```typescript
  export interface AppLayoutProps {
    children: React.ReactNode;
  }
  export function AppLayout(props: AppLayoutProps): JSX.Element;

  export function DashboardRoute(): JSX.Element;
  export function GoalsRoute(): JSX.Element;
  ```

- **Manifest**: Create docs/public/frontend.app-shell.api.md
  - Document: AppLayout (layout wrapper), route components
  - Purpose: Navigation infrastructure

- **Implementation**:

  **A. Layout component:**
  - `frontend/src/features/app-shell/components/AppLayout.tsx`
    ```typescript
    // For MVP: simple wrapper
    // Future: navbar with Home/Goals links, sidebar slot, breadcrumbs
    export function AppLayout({ children }: AppLayoutProps) {
      return (
        <div className="min-h-screen bg-background text-foreground">
          {/* Future: <AppNavbar /> */}
          <main>{children}</main>
        </div>
      );
    }
    ```

  **B. Route components:**
  - `frontend/src/features/app-shell/routes/DashboardRoute.tsx`
    ```typescript
    import { DashboardPage } from '@/features/dashboard';

    export function DashboardRoute() {
      return <DashboardPage />;
    }
    ```

  - `frontend/src/features/app-shell/routes/GoalsRoute.tsx`
    ```typescript
    import { GoalList } from '@/features/goals';

    export function GoalsRoute() {
      return (
        <div className="mx-auto max-w-4xl space-y-6 p-6">
          <div className="space-y-2">
            <h1 className="text-3xl font-bold tracking-tight">Goals</h1>
            <p className="text-muted-foreground">
              Manage your personal goals and track your progress
            </p>
          </div>
          <GoalList />
        </div>
      );
    }
    ```

  - `frontend/src/features/app-shell/index.ts`
    - Export: AppLayout, DashboardRoute, GoalsRoute

**Why this design:**
- **AppLayout** = reusable layout shell (ready for navbar/sidebar)
- **Route components** = thin wrappers that compose feature modules
- **Feature modules stay pure** - no routing knowledge
- **Easy to extend** - add new routes without touching feature modules

---

### 3. Enable Dark Theme Globally

**Module**: Application root (Next.js config - outside module boundaries)

- **Implementation**:
  - Edit `frontend/src/app/layout.tsx`
    - Add `className="dark"` to `<html>` tag
    - Wrap children with `<AppLayout>` from app-shell

  ```tsx
  import { AppLayout } from '@/features/app-shell';

  export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
      <html lang="en" className="dark">
        <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
          <AppLayout>{children}</AppLayout>
        </body>
      </html>
    );
  }
  ```

**Why:**
- Dark theme CSS variables already exist in `globals.css` (lines 81-113)
- Just activate with `className="dark"`
- No design system changes needed

---

### 4. Wire App Shell to Next.js Router

**Module**: Application root (Next.js App Router - minimal glue code)

**Implementation:**

**A. Root page (Dashboard):**
- Edit `frontend/src/app/page.tsx`
  ```tsx
  import { DashboardRoute } from '@/features/app-shell';

  export default function Page() {
    return <DashboardRoute />;
  }
  ```

**B. Goals page:**
- Create `frontend/src/app/goals/page.tsx`
  ```tsx
  import { GoalsRoute } from '@/features/app-shell';

  export default function Page() {
    return <GoalsRoute />;
  }
  ```

**Why this design:**
- Next.js `app/` files are **minimal glue code** - just imports
- All logic lives in modules (app-shell, dashboard, goals)
- Easy to test: app-shell routes work independently of Next.js
- Framework-agnostic: could swap Next.js for another router easily

---

### 5. Integration & Testing

**Test scenarios:**
1. Navigate to "/" → Dashboard renders with greeting + placeholder + "View Goals" button
2. Click "View Goals" → navigates to "/goals" (single click)
3. Navigate directly to "/goals" → Goals page renders
4. Browser back from "/goals" → returns to Dashboard
5. Dark theme applied on both pages (background dark, text light)
6. Page refresh on either route → page reloads correctly

**Quality gates:**
- ESLint passes (no deep imports)
- TypeScript typecheck passes
- All imports via public APIs (@/features/dashboard, @/features/app-shell, etc.)
- No business logic in `frontend/src/app/` files

---

### 6. Documentation Sync

- Update `docs/public/frontend.dashboard.api.md` with final API
- Update `docs/public/frontend.app-shell.api.md` with final API
- Run validation:
  - `python .specify/scripts/registry_validate.py`
  - `python .specify/scripts/manifest_lint.py`
- Commit with Conventional Commit message

---

## Gates

- Registry/manifests/contracts exist and validate
- No deep imports; consumers use only public surfaces
- SemVer bump on public surface changes; Conventional Commits
- ESLint and `pnpm typecheck` must pass
- Dark theme applied consistently across all pages

---

## Risks/Notes

### Architecture: Feature Modules at Same Level

**Decision**: Dashboard and Goals are both **feature modules** at the same level. App-shell orchestrates them.

**Module hierarchy:**
```
frontend.design      (primitives - no dependencies)
    ↓
frontend.dashboard   (feature - uses design)
frontend.goals       (feature - uses design)
    ↓
frontend.app-shell   (orchestrator - uses dashboard + goals + design)
    ↓
Next.js app/         (framework glue - uses app-shell)
```

**Benefits:**
- Clear separation of concerns
- Feature modules are reusable and testable
- Navigation complexity stays in app-shell
- Easy to add new features (create module → add route in app-shell)

---

### Next.js App Router: Minimal Glue Code

Files in `frontend/src/app/` contain **zero business logic** - just imports and renders from app-shell.

**Acceptable in app/:**
- Importing route components from app-shell
- Next.js-specific metadata (page titles, SEO)
- Next.js data fetching wrappers (if needed later)

**NOT acceptable in app/:**
- UI components
- Business logic
- Direct imports from feature modules (must go through app-shell)

---

### Future Extensions Ready

**App-shell is designed to grow:**

**Now (MVP):**
- AppLayout: simple wrapper
- 2 routes: Dashboard, Goals

**Future:**
- AppLayout: navbar with Home/Goals/Settings links
- AppLayout: sidebar for navigation tree
- AppLayout: breadcrumbs, user menu
- Route components: add auth guards, analytics, breadcrumb data
- New routes: Settings, Profile, etc.

All extensions happen **in app-shell module** - feature modules stay unchanged.

---

### Module Creation Order

1. **frontend.dashboard** (no new dependencies)
2. **frontend.app-shell** (depends on dashboard + goals)
3. **Wire Next.js app/** (depends on app-shell)

---

### Dark Theme Already Exists

No design system changes needed - dark theme CSS variables already defined in `frontend/src/app/globals.css:81-113`. Just activate globally with `className="dark"`.

---

### No Backend Changes

Per spec constraints, no backend modules modified. All work is frontend-only.
