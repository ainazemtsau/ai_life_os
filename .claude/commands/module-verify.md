---
description: Verify a module (lint, types, tests, boundaries), mark it VERIFIED on success, and WRITE PROGRESS back to tasks and the feature progress log.
---

# Usage
#   /module-verify MODULE=<id> [FEATURE=<feature-id>]
# Behavior:
#   - Validates docs-as-code (registry/manifest), lints/types/tests for the module scope.
#   - On success, marks the module’s “Verify” tasks done and sets status=verified in progress.
#   - On failure, marks status=blocked with a short reason.

User input:

$ARGUMENTS

Checks (adapt to your project)
- boundaries: imports use only public surfaces (scan for deep imports)
- docs: `.specify/scripts/registry_validate.py`, `.specify/scripts/manifest_lint.py`
- frontend TS: `pnpm typecheck`
- frontend lint: `pnpm lint`
- backend tests (if python module): `pytest -q` (module-selective)
- any module-local tests defined in playbook

Steps
1) Discover feature context
   - `.specify/scripts/bash/setup-plan.sh --json` → parse `FEATURE_SPEC`, `IMPL_PLAN`, `SPECS_DIR`, `BRANCH`.
2) Validate module `<id>` belongs to TARGET_MODULES (from plan.md).
3) Run verifications (only for this module’s paths)
   - If any check fails → collect brief error summary.
4) Update PROGRESS
   - If all checks PASS:
     * In `specs/<feature>/tasks.md`: mark the line “Verify <module> module” for this module as `- [x] ... (done: YYYY-MM-DD)`, if present.
     * In `specs/<feature>/tasks.by-module/<module>.md`: mark the Verify task (e.g., `MT… Verify module`) as done with date.
     * Update `specs/<feature>/progress.json`:
       - `modules["<module>"].status = "verified"`
       - `last_run = <ISO8601>`
     * Update/insert row in `specs/<feature>/progress.md` table: Status → **verified**, update counts and timestamp.
     * Append Run Log with “VERIFY PASSED”.
   - If any check FAILS:
     * Do **not** tick Verify tasks.
     * Update `progress.json` with `status = "blocked"`, `last_run`, and `error_summary`.
     * Update/insert row in `progress.md`: Status → **blocked**; add brief reason under a “Run Log” entry (“VERIFY FAILED: …”).
5) Output concise Summary:
   - PASS/FAIL, which checks ran, updated tasks (T/MT IDs), new status, next suggested command.

Guards
- Do not silently mark tasks done on failure.
- Do not touch unrelated modules’ rows.
- Keep messages short; progress files are the durable source of truth.
