---
description: Generate a lean, TDD-first global task plan scoped ONLY to target modules for the active feature. Auto-insert bootstrap and tag integration work to the router-owning module.
---

User input:

$ARGUMENTS

Goals
- Use ONLY the machine-readable scope from plan.md to decide which modules get tasks.
- Insert a single bootstrap task if any Target Module is missing in the registry.
- Tag all integration (Next.js App Router) tasks with the Router Owner module.
- Do NOT emit tasks or by-module files for context modules.

Steps
1) Run `.specify/scripts/bash/setup-plan.sh --json` → get FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH.
2) Read `IMPL_PLAN` and extract:
   - TARGET_MODULES block between:
     `<!-- TARGET_MODULES:BEGIN` … `TARGET_MODULES:END -->`
   - ROUTER_OWNER from: `<!-- ROUTER_OWNER: <id> -->`
   If not found → ERROR "plan.md missing Machine-readable Scope".
3) Load `.specify/memory/public/registry.yaml` to pull import_hint/allowed_dirs for existing modules.
   - For NEW modules (not in registry), compute defaults:
     * manifest: `docs/public/<id>.api.md`
     * contract: `frontend/src/contracts/<name>.d.ts` (frontend.*) or `backend/src/ai_life_backend/contracts/<name>_protocols.py` (backend.*)
     * import_hint: namespace style
     * allowed_dirs defaults per side
4) Build **Module API Matrix** with ONLY Target Modules. Ensure frontend import hints are namespace style (`import * as <name> from '@/features/<name>'`).
5) **Preparation**:
   - If any Target Module NOT present in registry → add single task:
     `T000 @prio(P1) Bootstrap missing modules via /module-bootstrap FROM_TASKS=<feature-id>`
   - Add validation lines (registry + manifest linters).
6) **Global Tasks (TDD)**:
   - For each Target Module emit:
     - Define contract → tests → implement → update manifest → verify.
7) **Integration (router glue)**:
   - Emit ONLY 3 items and tag them with `@module(<router-owner>)`:
     * Enable dark theme globally (layout.tsx, add `className="dark"`, wrap with AppLayout)
     * Wire "/" with DashboardRoute
     * Wire "/goals" with GoalsRoute
8) Number tasks sequentially (T001…); avoid any file paths (they belong to module playbooks).
9) Save to `specs/<feature-id>/tasks.md`.

Validation
- Target Modules list is non-empty.
- No context modules leaked into Matrix or tasks.
- Integration tasks tagged with router-owner (not pseudo-modules).
- Namespace import hints for frontend modules.

Output
- Path to tasks.md
- Target modules list
- Router-owner id
- Next step suggestion: `/module-bootstrap FROM_TASKS=<feature-id>`
