---
description: Bootstrap one or more modules declared in tasks/plan by creating registry entries, public manifests, contracts and folder scaffolds. Validates docs-as-code gates.
---

User input:

$ARGUMENTS
# Usage:
#   /module-bootstrap MODULE=<id>
#   /module-bootstrap MODULE=<id1>,<id2>
#   /module-bootstrap FROM_TASKS=<feature-id>
#   /module-bootstrap MODULE=<id>[,...] FROM_TASKS=<feature-id>
# Options:
#   DRY_RUN=1   # print planned actions without writing
#   FORCE=1     # overwrite existing non-empty stubs if present
#   USES="<csv>" # optional override for uses when MODULE=<id> is used

Goal
- Create missing modules consistently and atomically:
  * Add entry to `.specify/memory/public/registry.yaml`
  * Create public manifest in `docs/public/<id>.api.md`
  * Create language contract (TS .d.ts / Python protocol) at the path recorded in registry
  * Run validators and print a concise summary

Inputs discovery
1) If `FROM_TASKS=<feature-id>` is provided:
   - Read `specs/<feature-id>/tasks.md`
   - Collect distinct `<id>` from all `@module(<id>)` tags
   - For each `<id>`, try to parse **Uses** from the "Module API Matrix" table (if present)
   - Filter out modules already present in registry
2) If `MODULE=<id>[,<id>...]` is provided:
   - Use the explicit list
   - For each `<id>`, `USES="<csv>"` (if provided) takes precedence
3) If both are provided → take the union (explicit MODULE list can override Uses via `USES=`)

Module typing & naming
- If `<id>` starts with `frontend.` → kind=typescript
- If `<id>` starts with `backend.` → kind=python
- Otherwise: ERROR "Unsupported module namespace"
- Name normalization for file paths:
  * `<name>` = `<id>` without `frontend.`/`backend.` prefix
  * For TS contract filenames, replace dots with dashes (e.g., `app-shell.d.ts`)
  * For `src/features/<name>` use the normalized `<name>` (dots → dashes)

Defaults (unless a module profile is known)
- manifest: `docs/public/<id>.api.md`
- contract:
  * frontend.* → `frontend/src/contracts/<name>.d.ts`
  * backend.*  → `backend/src/ai_life_backend/contracts/<name>_protocols.py`
- import_hint:
  * frontend.* → `import * as <name> from '@/features/<name>'`
  * backend.*  → `from ai_life_backend.<name>.public import *`

Special profiles (hardcoded)
- `frontend.app-shell` additionally owns `frontend/src/app/**` (Next.js App Router glue)

Uses resolution (priority)
1) `USES="<csv>"` argument (if provided for explicit MODULE flow)
2) "Module API Matrix" row in `specs/<feature-id>/tasks.md` (when FROM_TASKS is used)
3) Fallback to empty list `[]`

Procedure
1) Run `.specify/scripts/bash/setup-plan.sh --json` to discover repo/feature context (for logging only)
2) Load and parse `.specify/memory/public/registry.yaml`
3) Build a creation plan for each target module (kind, manifest, contract, import_hint,uses)
4) For each target module:
   - If already present in registry → report "present" and skip creation (unless FORCE and stubs are empty)
   - Insert/Update registry entry fields:
     * kind, semver (`0.1.0` if new), manifest, contract, import_hint, uses, notes
   - Create parent folders as needed
   - Create `docs/public/<id>.api.md` with this minimal stub (if not exists or FORCE):
     ```
     # Public API — <id>
     Version: 0.1.0

     ## Overview
     Module placeholder (to be filled during /module-implement).

     ## Exports
     - (to be defined)

     ## Types
     Contract: <contract-path>

     ## Usage
     ```ts
     // public surface import
     <import_hint>
     ```
     ## Versioning
     - 0.1.0 — initial stub
     ```
   - Create contract stub (if not exists or FORCE):
     * TS (`.d.ts`):
       ```
       /** Public contract — <id>
        *  Version: 0.1.0
        *  This file defines the public TypeScript surface for the module.
        */
       export {};
       ```
     * PY (`_protocols.py`):
       ```
       """Public contract protocols — <id>
       Version: 0.1.0
       Define typing.Protocol interfaces here for cross-module use.
       """
       from typing import Protocol, runtime_checkable

       @runtime_checkable
       class ExampleProtocol(Protocol):
           ...
       ```
5) Write back updated `registry.yaml` atomically
6) Run validators:
python .specify/scripts/registry_validate.py
python .specify/scripts/manifest_lint.py

sql
Копировать код
7) Output summary:
- Table of modules (created/present/updated), manifest paths, contract paths, roots
- If DRY_RUN=1 → print planned actions only
- Next suggested command:
  * `/fanout-tasks <feature-id>` if FROM_TASKS was used
  * otherwise suggest `/fanout-tasks <last-feature-id>` if available

Exit rules & safety
- If a target file exists and is non-empty and FORCE!=1 → skip with warning (do not clobber)
- If registry entry exists but diverges on computed defaults → update only missing fields; print a diff summary
- If no target modules resolved → ERROR "No modules to bootstrap"
- Never touch modules not listed as targets

Examples
- `/module-bootstrap FROM_TASKS=002-basic-navigation-mvp`
- `/module-bootstrap MODULE=frontend.dashboard USES="frontend.design"`
- `/module-bootstrap MODULE=frontend.app-shell FROM_TASKS=002-basic-navigation-mvp`