---
description: Execute implementation for a SPECIFIC module using per-module tasks (TDD, module boundaries).
---

The user input may be provided as command arguments — you MUST parse and honor it before proceeding.

User input (raw):
$ARGUMENTS

# Expected arguments:
#   MODULE=<module-key>            # REQUIRED (e.g., repo, backend, frontend, api, auth, ...)
#   FEATURE=<feature-id>           # OPTIONAL (e.g., 001-two-modules). If omitted, discover via check-prerequisites.

## 1) Discover feature context and required docs
1. Run from REPO ROOT:
   `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks`
   Parse JSON and extract:
     - FEATURE_DIR (absolute path; e.g., <repo>/.specify/specs/<feature-id>)
     - AVAILABLE_DOCS (list of discovered docs)
   If FEATURE was explicitly provided in $ARGUMENTS, VERIFY it matches FEATURE_DIR; otherwise override FEATURE by detected value.

2. Parse $ARGUMENTS and extract MODULE=<module-key>.
   - If MODULE is missing or empty → HARD ERROR:
     "MODULE is required. Re-run as: /implement MODULE=<name> [FEATURE=<id>]"

3. Compute absolute paths:
   - GLOBAL_TASKS      = {FEATURE_DIR}/tasks.md
   - PLAN              = {FEATURE_DIR}/plan.md
   - MODULE_TASKS      = {FEATURE_DIR}/tasks.by-module/{MODULE}-tasks.md
   - DATA_MODEL (opt)  = {FEATURE_DIR}/data-model.md
   - CONTRACTS_DIR(opt)= {FEATURE_DIR}/contracts/
   - RESEARCH (opt)    = {FEATURE_DIR}/research.md
   - CONST_GLOBAL (opt)= <repo>/.specify/memory/constitution.md
   - CONST_MODULE(opt) = <repo>/.specify/memory/{MODULE}.constitution.md

   VALIDATE:
   - PLAN must exist → else ERROR "plan.md is required, run /plan"
   - MODULE_TASKS must exist → else ERROR:
     "Module tasks not found. Run: /fanout-tasks <feature-id> and /module-tasks <feature-id> <module>"

## 2) Load and analyze implementation context
4. READ (do not skip):
   - MODULE_TASKS: the ONLY source of executable tasks (IDs MT###, [P], exact file paths, phases)
   - PLAN: tech stack, layout, allowed directories / module boundaries
   - CONST_GLOBAL (if exists): cross-cutting constraints
   - CONST_MODULE (if exists): module-specific constraints
   - GLOBAL_TASKS: reference ONLY (public API matrix & mapping), DO NOT execute from here
   - DATA_MODEL / CONTRACTS / RESEARCH: supportive info if present

5. DERIVE allowed directories for this module from PLAN and/or CONST_MODULE.
   If not clearly specified, DEFAULT to:
     - `src/modules/{MODULE}/**` and `tests/modules/{MODULE}/**` (single-project layout)
   ENFORCE: Never edit files outside allowed directories. For cross-module needs, create a HANDOFF note.

## 3) Execute per-module tasks (TDD-first, strict ordering)
6. Parse MODULE_TASKS into phases and tasks with:
   - ID (MT###), [P] marker, description, explicit file paths, and any dependencies.
   - DO NOT invent paths. If a task lacks a path, update the task with a precise path before editing code.

7. For each phase in order (Setup → Tests → Implementation → Integration → Polish):
   Execute tasks respecting:
   - TDD: tests MUST be authored and MUST FAIL before implementation.
   - [P]: only run in parallel when tasks touch DIFFERENT files and have NO dependencies.
   - Same-file tasks MUST run sequentially.

   For each task:
   a) If it's a **test** task:
      - Create/update the test file with assertions that SHOULD FAIL initially.
      - Run tests; confirm they fail with a meaningful assertion.
   b) If it's an **implementation** task:
      - Implement the minimal code to satisfy the failing test(s).
      - Re-run tests; confirm they pass.
   c) If it's an **integration** task:
      - Wire modules/components as specified; never modify other modules directly.
      - If another module needs changes, append a HANDOFF entry instead of editing that module.

   After a task is truly complete:
   - Mark it as `[x]` in MODULE_TASKS (do NOT touch GLOBAL_TASKS).
   - If using VCS, commit with message: `"{MODULE}: {TASK_ID} {1-line summary}"`.

## 4) HANDOFF notes (instead of cross-module edits)
8. If a required change belongs to a different module:
   - Append to `{FEATURE_DIR}/handoff.md` with fields:
     - module: <target-module>
     - reason: <why needed>
     - spec: <public surface / contract to modify>
     - suggested changes (code pointers, file paths)
     - blocking?: yes|no
   - Reference the originating MT task ID.

## 5) Validation & completion
9. When all MT tasks are marked `[x]`:
   - Run the module test suite (targeted paths) and, if available, the full suite.
   - Ensure results align with PLAN and constitutions (global + module).
   - Output a concise summary:
     - Completed task IDs
     - Files created/modified
     - Any HANDOFF entries created
     - Follow-ups (if any)

## 6) Hard safety rails
- NEVER modify files outside the allowed module directories.
- NEVER tick a task to `[x]` without verifying (tests where applicable).
- If MODULE_TASKS appears inconsistent or incomplete, STOP and instruct to re-run:
  `/module-tasks <feature-id> <module>` (or adjust the module tasks file), then resume.
