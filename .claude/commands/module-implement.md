---
description: Implement a module strictly within allowed_dirs, update public docs, and WRITE PROGRESS back to tasks and a feature-level progress log.
---

# Usage
#   /module-implement MODULE=<id> [FEATURE=<feature-id>] [ONLY=contract|tests|impl|docs]
# Behavior:
#   - If FEATURE not provided: auto-detect via `.specify/scripts/bash/setup-plan.sh --json`
#   - If per-module playbook missing: run `/fanout-tasks <feature-id>` first (only for Target Modules)
#   - Execute the next logical chunk (contract → tests → implementation → docs) unless ONLY=… limits scope
#   - Update progress checkboxes and logs for all steps actually performed in THIS run

User input:

$ARGUMENTS

Goals
- Perform module implementation steps WITHOUT crossing module boundaries (respect allowed_dirs from registry.yaml).
- Keep code minimal and clean (SOLID/DRY/KISS). Tests-first where applicable.
- Sync public docs (manifest + contract) when exports change.
- Persist PROGRESS for visibility:
  - Update checkboxes in:
    * `specs/<feature>/tasks.md` (T-ids with @module(<id>))
    * `specs/<feature>/tasks.by-module/<module>.md` (MT-ids)
  - Update or create:
    * `specs/<feature>/progress.md` (human table + run log)
    * `specs/<feature>/progress.json` (machine state)

Steps
1) Discover feature context
   - Run `.specify/scripts/bash/setup-plan.sh --json` → parse `FEATURE_SPEC`, `IMPL_PLAN`, `SPECS_DIR`, `BRANCH`.
   - If FEATURE=<id> provided, ensure it matches the discovered directory.
2) Validate module `<id>`
   - Read `specs/<feature>/plan.md` and extract:
     * target list from `<!-- TARGET_MODULES:BEGIN ... END -->`
     * router-owner (if relevant)
   - If `<id>` not in TARGET_MODULES → ERROR (do not implement context modules here).
3) Ensure per-module playbook exists
   - Path: `specs/<feature>/tasks.by-module/<module>.md`
   - If missing → run `/fanout-tasks <feature>` to generate only Target Modules, then continue.
4) Load registry entry for `<id>` from `.specify/memory/public/registry.yaml` (or `docs/public/registry.yaml`, per your project).
   - Capture `allowed_dirs`, `contract`, `manifest`, `import_hint`, `semver`.
5) Decide execution scope
   - If ONLY=… → limit steps to that scope.
   - Default order to attempt:
     a) contract (create/update `.d.ts` or protocol stubs)
     b) tests (write failing tests)
     c) implementation (code to pass tests)
     d) docs (sync manifest with public API)
6) Execute within allowed_dirs
   - Write/update files only in `allowed_dirs`, `contract`, `manifest`.
   - Respect “public surface only” for imports (use `import_hint`).
   - Keep code small, typed, with explicit boundaries.
7) Update PROGRESS (very important)
   - Identify DONE T-ids in `specs/<feature>/tasks.md` with `@module(<id>)` that correspond to steps performed in THIS run (e.g., “Define contract”, “Write tests”, “Implement”, “Update manifest”). Replace `- [ ]` → `- [x]` and append ` (done: YYYY-MM-DD)`.
   - Identify DONE MT-ids in `specs/<feature>/tasks.by-module/<module>.md` (same logic). Replace `- [ ]` → `- [x]` and append ` (done: YYYY-MM-DD)`.
   - Update/Create `specs/<feature>/progress.json`:
     ```json
     {
       "feature": "<feature-id>",
       "updated_at": "<ISO8601>",
       "modules": {
         "<module-id>": {
           "status": "in_progress",
           "last_run": "<ISO8601>",
           "done_ids": ["Txxx","MTyyy", "..."],
           "totals": {"global": {"done": n, "total": N}, "module": {"done": m, "total": M}}
         }
       }
     }
     ```
     - Merge with existing JSON if present; only update the current module.
   - Update/Create `specs/<feature>/progress.md`:
     - Ensure a table exists (create if missing):
       ```
       | Module | Status | Global tasks (done/total) | Module tasks (done/total) | Last run |
       |--------|--------|---------------------------|----------------------------|----------|
       ```
     - Replace the row for `<module-id>` or append it with computed counts and timestamp. Status here after implement is typically **in_progress** (final “verified” will be set by /module-verify).
     - Append a “Run Log” entry:
       ```
       ### Run YYYY-MM-DD HH:MM
       - module: <module-id>
       - steps: contract? tests? impl? docs?
       - files touched: <short list>
       - notes: <short note if any>
       ```
8) Output a concise summary to chat:
   - Module, steps performed, changed files, updated task IDs, progress counts, next recommended command.

Validation & Guards
- Do not edit files outside allowed_dirs/contract/manifest.
- Do not mark “Verify module” as done (belongs to /module-verify).
- If tests fail after implementation → set status “blocked” in progress row and include a short failure summary.

Notes
- This command is idempotent: re-runs mark only newly completed steps.
- Keep commit atomic per module step (the repo commit itself is outside the scope of this command).
