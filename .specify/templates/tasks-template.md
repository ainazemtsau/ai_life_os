# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`  
**Prerequisites**: `plan.md` (required); optional: `research.md`, `data-model.md`, `contracts/`

---

## Module API Matrix (global contracts)
> Define the **public surface** for each module. Keep it concise and normative.
module: repo
public:

get_user(user_id) -> User

save_user(user: User) -> None

module: auth
public:

issue_token(user_id) -> Token

verify_token(token) -> UserId | Error

## Global Tasks by Module (high-level only)
> Tag each with `@module(<name>)` and priority `@prio(P1|P2|P3)`. Do **not** include file-level details here.
- [ ] T001 @module(repo) @prio(P1) Add `get_user(user_id)` to repo public surface
- [ ] T002 @module(auth) @prio(P1) Expose `issue_token` and `verify_token` with stable contracts
- [ ] T003 @module(api)  @prio(P2) Wire `/api/users/{id}` to repo.get_user

---

## Execution Flow (main)
Load plan.md from the feature directory
→ If not found: ERROR "No implementation plan found"
→ Extract: tech stack, libraries, structure

Load optional design docs:
→ data-model.md: Extract entities → model tasks
→ contracts/: Each file → contract test task
→ research.md: Extract decisions → setup tasks

Generate preliminary tasks (GLOBAL scope):
→ Setup (thin): env, baseline CI hooks
→ Tests (thin): global acceptance checks, mappings to modules
→ Core & Integration: ONLY high-level items tagged by @module(...)
→ Polish (thin): docs stubs

Apply task rules:
→ Different files = mark [P] for parallel (later resolved in module tasks)
→ Same file = sequential (no [P])
→ Tests before implementation (TDD is mandatory everywhere)

Number tasks sequentially (T001, T002...)

Build dependency notes (high-level), but defer file paths to module tasks

Create fan-out plan: group tasks by @module(...)

Validate completeness:
→ Are all public APIs in "Module API Matrix" covered by tasks?
→ Are contracts mapped to modules?
→ Are global tasks free of file-level details?

Return: SUCCESS (global tasks ready for fan-out)

## Format: `[ID] [P?] Description`
- Keep high-level descriptions here; **no exact file paths**.
- Add tags: `@module(<name>)`, `@prio(P1|P2|P3)`, optional `@owner(@anton)`
- File paths and granular steps belong to **module task files**.

## Path Conventions (informative)
- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Module task writers MUST adjust to `plan.md` structure.

## Phase 3.1: Setup (thin, global)
- [ ] T010 Create/verify base project structure per implementation plan
- [ ] T011 Initialize language/runtime, CI stub, and shared linting
- [ ] T012 [P] Configure formatting & commit hooks

## Phase 3.2: Tests First (TDD) — global acceptance framing
> These are **global** placeholders; actual test files are generated in module tasks.
- [ ] T020 Define contract coverage table (contracts/ → module mapping)
- [ ] T021 Define integration flows (user registration, auth) mapped to modules

## Phase 3.3: Core (high-level only)
- [ ] T030 @module(repo) Provide user retrieval capability
- [ ] T031 @module(auth) Provide token issuing/verification capability
- [ ] T032 @module(api) Expose `GET /api/users/{id}`

## Phase 3.4: Integration (high-level only)
- [ ] T040 Cross-module wiring (API → service → repo)
- [ ] T041 Logging and cross-cutting concerns enumerated by module

## Phase 3.5: Polish (global)
- [ ] T050 Definition-of-Done checklist updated
- [ ] T051 Update `docs/` index for feature

## Fan-out Rules (to module tasks)
- Each `@module(<name>)` item spawns a module task file `{{module}}-tasks.md`
- Module tasks:
  - expand into file-level steps with exact paths
  - enforce TDD (tests must fail first)
  - load constitutions: global + `<module>.constitution.md`
  - respect module boundaries and only touch allowed directories

## Validation Checklist (global gate)
- [ ] Every public API in the Matrix has at least one `@module(...)` task
- [ ] No file-paths appear in global tasks
- [ ] Priorities set (P1/P2/P3)
- [ ] Parallel markers are not used to force cross-module work
- [ ] Global acceptance checks mapped to modules