---
description: Bootstrap one or more modules declared in tasks/plan by creating registry entries, public manifests, contracts and folder scaffolds. Validates docs-as-code gates.
---

User input:

$ARGUMENTS
# Usage:
#   /module-bootstrap MODULE=<id>
#   /module-bootstrap FROM_TASKS=<feature-id>
#   /module-bootstrap MODULE=<id1>,<id2>
# Options:
#   DRY_RUN=1   # print planned actions without writing
#   FORCE=1     # overwrite existing empty stubs if present

Goal
- Create missing modules consistently and atomically:
  * Add entry to `.specify/memory/public/registry.yaml`
  * Create public manifest in `docs/public/<id>.api.md`
  * Create language contract (TS .d.ts / Python protocol) as a minimal stub at the path from registry
  * Create directory scaffolds for all `allowed_dirs`
  * Run validators

Inputs discovery
1) If `FROM_TASKS=<feature-id>` is provided:
   - Read `specs/<feature-id>/tasks.md`
   - Collect all `@module(<id>)`
   - Filter out modules already present in registry
2) If `MODULE=<id>[,<id>...]` provided:
   - Use the explicit list
3) If both provided → union

Module typing
- If `<id>` starts with `frontend.` → kind=typescript
- If `<id>` starts with `backend.` → kind=python
- Otherwise: ERROR "Unsupported module namespace"

Defaults (unless a module profile is known)
- manifest: `docs/public/<id>.api.md`
- contract:
  * frontend.* → `frontend/src/contracts/<name>.d.ts`
  * backend.*  → `backend/src/ai_life_backend/contracts/<name>_protocols.py`
  where `<name>` is the part after `frontend.` / `backend.` with dots replaced by dashes.
- import_hint:
  * frontend.* → `import * as <name> from '@/features/<name>'`
  * backend.*  → `from ai_life_backend.<name>.public import *`
  (kebab-case/segment normalization handled by the script)
- allowed_dirs:
  * frontend.* → `frontend/src/features/<name>/**`, `frontend/src/contracts/<name>.d.ts`, `docs/public/<id>.api.md`
  * backend.*  → `backend/src/ai_life_backend/<name>/**`, `backend/tests/<name>/**`

Special profiles (hardcoded minimal logic):
- `frontend.app-shell` additionally owns `frontend/src/app/**` (Next.js App Router glue)

Procedure
1) `.specify/scripts/bash/setup-plan.sh --json` → detect feature dir (for logging)
2) Load/parse `.specify/memory/public/registry.yaml`
3) Build a creation plan for each target module
4) For each module:
   - Insert registry entry with kind/semver/import_hint/uses/allowed_dirs/manifest/contract
   - Create missing parent folders
   - Create `docs/public/<id>.api.md` with a minimal manifest stub:
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
     // import surface:
     <import_hint>
     ```
     ## Versioning
     - 0.1.0 — initial stub
     ```
   - Create contract stub:
     * TS: create `frontend/src/contracts/<name>.d.ts` with empty export surface + basic types docblock
     * PY: create `backend/src/ai_life_backend/contracts/<name>_protocols.py` with a header docstring and Protocol placeholders
   - Create folders for each `allowed_dirs` (no code files yet)
5) Write back updated registry.yaml
6) Run validators:
