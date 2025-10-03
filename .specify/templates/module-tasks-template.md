# Module Tasks: [MODULE NAME] for Feature [FEATURE NAME]

**Inputs**:
- Global constitution: `.specify/memory/constitution.md`
- Module constitution (optional): `.specify/memory/[module].constitution.md`
- Global tasks file: `.specify/specs/[###-feature-name]/tasks.md`
- Design docs from `/specs/[###-feature-name]/`: `plan.md` (required), `data-model.md`, `contracts/`, `research.md`

**Scope**:
- Work ONLY inside this module’s allowed directories (per plan.md).
- If cross-module changes are required, create a **handoff note/PR stub** instead of editing other modules.

---

## Execution Flow (module)
Read global tasks; filter entries tagged @module([module]).

Merge constitutions: global + module (module overrides specifics).

For each filtered global item, expand into detailed, file-scoped tasks:

Tests First (contract/integration/unit) with explicit file paths

Implementation tasks with explicit file paths

Logging, errors, validation per module rules

Enforce rules:

Tests MUST be authored and MUST FAIL before implementation

[P] only if touching different files and no dependencies

Respect module boundaries (no edits outside this module)

Number tasks MT001, MT002...

Build dependency graph and a small parallel-run example

Validate:

All contracts for this module have tests

All entities mapped to concrete models/services

All endpoints/use-cases implemented or handed off

Return: SUCCESS (module tasks ready for implementation)

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no deps)
- Include **exact file paths** in every task
- Use `tests/*` before `src/*` tasks (TDD)

## Allowed Paths (adapt per plan.md)
- Single project: `src/modules/[module]/**`, `tests/modules/[module]/**`
- Web app: `backend/src/[module]/**`, `tests/backend/[module]/**`
- Mobile: `api/src/[module]/**`, `tests/api/[module]/**`

## Phase A: Setup (module)
- [ ] MT001 Create/verify module skeleton and init files
- [ ] MT002 [P] Configure module-local lint/test fixtures if needed

## Phase B: Tests First (MUST FAIL before C)
- [ ] MT010 [P] Contract test(s) → `tests/.../contract/test_[module]_[case].py`
- [ ] MT011 [P] Integration test(s) → `tests/.../integration/test_[flow].py`
- [ ] MT012 [P] Unit tests for validators → `tests/.../unit/test_[validator].py`

## Phase C: Implementation (ONLY after tests are failing)
- [ ] MT020 [P] Models → `src/.../[module]/models/*.py`
- [ ] MT021 [P] Services → `src/.../[module]/services/*.py`
- [ ] MT022 Endpoints/Handlers → `src/.../[module]/api/*.py`
- [ ] MT023 Input validation
- [ ] MT024 Error handling + structured logging

## Phase D: Integration
- [ ] MT030 Wire services to infra (DB/cache/etc.)
- [ ] MT031 Middleware/cross-cutting per module constitution

## Phase E: Polish
- [ ] MT040 [P] Unit tests coverage targets
- [ ] MT041 Performance checks (budget from constitution)
- [ ] MT042 [P] Update module docs → `docs/modules/[module].md`
- [ ] MT043 Remove duplication / tidy

## Dependencies
- Tests (MT010–MT012) before Implementation (MT020–MT024)
- Models (MT020) often block Services (MT021) and Integration (MT030)

## Parallel Example
Launch MT010–MT012 together:

Contract tests (contract/)

Integration (auth flow)

Unit (validators)

## Notes
- Commit after each task with task ID in the message
- Avoid vague tasks and cross-module edits