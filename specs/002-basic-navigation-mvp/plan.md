# Implementation Plan: Basic Navigation MVP

**Branch**: `002-basic-navigation-mvp` | **Date**: 2025-10-06 | **Spec**: spec.md
**Input**: Feature specification from /home/anton/code/ai_life_os/specs/002-basic-navigation-mvp/spec.md

---

## Purpose
Freeze high-level design for this feature using **contracts-first**. The template is logic-less; the `/plan` runner injects all concrete details.

## Context & Constraints (from spec)
- **Frontend-only feature** (no backend changes allowed)
- **Dark theme by default** (no theme switcher in this MVP)
- **Single-user context** (no authentication/permissions)
- **Reuse existing modules** where possible
- **Simple navigation**: Dashboard at "/" → Goals at "/goals" in one click
- Browser navigation (back/forward, direct URL access) must work correctly

## Module Map (public surfaces only)

| Module | Status | Kind | Public Surface | Import Pattern |
|--------|--------|------|---------------|----------------|
| **frontend.dashboard** | **Target** | typescript | Dashboard UI components, page exports | `import * as dashboard from '@/features/dashboard'` |
| **frontend.app-shell** | **Target** | typescript | Root layout, routing configuration, theme provider | `import * as appShell from '@/features/app-shell'` |
| frontend.design | Context | typescript | UI primitives (Button, Card, Typography, colors) | `import * as design from '@/features/design'` |
| frontend.goals | Context | typescript | Goals page and components | `import * as goals from '@/features/goals'` |

> Only surfaces listed above are public. Everything else is private implementation.

## Contracts
- HTTP contracts (OpenAPI 3.1), if any:
  *None (frontend-only feature)*

- In-process ports (TS `.d.ts` / Python Protocols), if any:
  | Module | Contract File | Exports |
  |--------|---------------|---------|
  | frontend.dashboard | `frontend/src/contracts/dashboard.d.ts` | Dashboard page component, props types |
  | frontend.app-shell | `frontend/src/contracts/app-shell.d.ts` | Layout components, theme types |

## Vertical Steps (outline)
1. **Create `frontend.dashboard` module** (new bounded context)
   - Bootstrap module entry in registry with initial semver 0.1.0
   - Create public manifest at `docs/public/frontend.dashboard.api.md`
   - Define contract: `frontend/src/contracts/dashboard.d.ts`
   - Scaffold folder: `frontend/src/features/dashboard/`

2. **Create `frontend.app-shell` module** (new bounded context)
   - Bootstrap module entry in registry with initial semver 0.1.0
   - Create public manifest at `docs/public/frontend.app-shell.api.md`
   - Define contract: `frontend/src/contracts/app-shell.d.ts`
   - Scaffold folder: `frontend/src/features/app-shell/`

3. **Define public contracts**
   - Dashboard: page component type, props interface
   - App-shell: layout types, theme configuration, navigation types

4. **Implement dashboard feature**
   - Dashboard page with greeting and placeholder content
   - Navigation link/button to Goals
   - Use `frontend.design` public API for UI components

5. **Implement app-shell routing integration**
   - Root layout with dark theme provider
   - Route configuration: "/" → dashboard, "/goals" → goals page
   - Framework glue in `frontend/src/app/` (owned by app-shell module)

6. **Apply dark theme**
   - Configure dark mode as default in app-shell layout
   - Ensure consistency across all pages

7. **Validate navigation flows**
   - Dashboard → Goals navigation works
   - Browser back/forward navigation works
   - Direct URL access works for both routes

## Gates
- Registry/manifests/contracts exist and validate.
- No deep imports; consumers use only public surfaces.
- SemVer bump on public surface changes; Conventional Commits.

## Risks/Notes
- **New modules required**: `frontend.dashboard` and `frontend.app-shell` are new bounded contexts that must be bootstrapped
- **Router ownership**: `frontend.app-shell` will own `frontend/src/app/**` to manage Next.js routing configuration; keep framework-specific code isolated here
- **Dark theme scope**: Theme configuration lives in app-shell; design system provides dark-compatible primitives
- **Minimal MVP**: No theme switcher, no user preferences persistence; focus on basic navigation flow only

## Machine-readable Scope
<!-- TARGET_MODULES:BEGIN
frontend.dashboard
frontend.app-shell
TARGET_MODULES:END -->
<!-- ROUTER_OWNER: frontend.app-shell -->
