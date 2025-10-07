---
description: Execute the implementation planning workflow using the plan template; freeze contracts-first design and write a machine-readable scope (TARGET_MODULES + ROUTER_OWNER) for downstream tools.
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

Goals
- Generate `plan.md` from the template with clear, contracts-first decisions (no code).
- Record an explicit, machine-readable scope inside `plan.md`:
  - `TARGET_MODULES` — only the modules that will receive work in this feature.
  - `ROUTER_OWNER` — the module that owns framework glue for routing (e.g., Next.js `app/`).
- Keep the plan logic-less: the runner computes content; the template is declarative.

Steps

1) Run `.specify/scripts/bash/setup-plan.sh --json` from the repo root and parse:
   - `FEATURE_SPEC`, `IMPL_PLAN`, `SPECS_DIR`, `BRANCH` (all future paths must be absolute)

2) Gate: Clarifications
   - Load `FEATURE_SPEC` and check for `## Clarifications` with at least one `Session` subheading.
   - If missing **and** ambiguities remain (vague adjectives, unresolved decisions), instruct the user to run `/clarify` first, unless they explicitly said "proceed without clarification".

3) Analyze specification (high level only)
   - Extract: user stories, functional/non-functional requirements, constraints (e.g., "frontend-only"), acceptance criteria.
   - Derive environment constraints that matter to contracts (e.g., HTTP presence, data entities).

4) Read project constitution:
   - `.specify/memory/constitution.md`
   - Enforce: Clean Code gates (SOLID/DRY/KISS), strict module boundaries, docs-as-code, SemVer, Conventional Commits.

5) Compute module partition (bounded contexts)
   - Build a **Module Map**: public surfaces only; everything else is private internals.
   - Decide **which modules actually get work in this feature** (these are the **TARGET_MODULES**).
     Typical patterns for web:
       * Create/extend `frontend.[feature]` for UI of this feature.
       * Add/extend `frontend.app-shell` if routing/layout glue is needed (owner of `frontend/src/app/**`).
       * Reuse `frontend.design`, `frontend.goals`, or backend modules as **context** (no work) unless the spec requires changes.
     - Respect explicit constraints from the spec (e.g., "frontend-only" → do **not** include backend modules as targets).

6) Determine **ROUTER_OWNER**
   - Else, if a module named `frontend.app-shell` is in the target set → use it.
   - Else, omit and do not emit router integration steps (record rationale in notes).

7) Prepare plan content
   - Load `.specify/templates/plan-template.md`.
   - Fill placeholders:
     - `[FEATURE]`, `[BRANCH]`, `[DATE]`, `[SPEC_PATH]`, `[FEATURE_SPEC_ABS]`
     - `[CONTEXT_SUMMARY]` — short summary of constraints from the spec (no frameworks).
     - `[MODULE_API_MATRIX]` — a table of **public** surfaces for **all modules relevant to the feature**, but **mark** which ones are **Target** vs **Context**. Use namespace import hints for frontend (e.g., `import * as dashboard from '@/features/dashboard'`).
     - `[HTTP_CONTRACTS_TABLE]` — only modules that expose an HTTP surface (OpenAPI).
     - `[INPROC_PORTS_TABLE]` — modules exposing in-process ports (TS `.d.ts` / Python Protocols).
     - `[VERTICAL_STEPS]` — outline steps (e.g., create new frontend modules, define contracts, add router glue).
     - `[NOTES]` — risks/trade-offs (e.g., keeping framework glue minimal in `app/`).
   - Append a **machine-readable scope** section at the end of `plan.md`:
     ```
     ## Machine-readable Scope
     <!-- TARGET_MODULES:BEGIN
     <one module id per line, e.g.>
     frontend.dashboard
     frontend.app-shell
     TARGET_MODULES:END -->
     <!-- ROUTER_OWNER: frontend.app-shell -->
     ```

8) Write `IMPL_PLAN` atomically.

9) Validate output
   - Ensure the Machine-readable Scope exists and lists **only** target modules.
   - Ensure Module Map shows **public surfaces only**; no internal details.
   - Ensure no code or framework internals leak into the plan.

10) Report
   - Print branch, plan path, and a summary:
     - Target Modules
     - Router Owner (if any)
     - Contracts created/updated (if applicable)
   - Next command suggestion: `/tasks`

Notes
- Do not fabricate technical stack choices; contracts-first means public surfaces, not framework picks.
- Keep the plan short and crisp; all heavy details live in manifests/contracts later.
