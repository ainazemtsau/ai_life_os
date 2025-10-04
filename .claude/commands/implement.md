# /implement MODULE=<module-id> [FEATURE=<feature-id>]

**Purpose**  
Execute the implementation plan **for a single module** using its per-module task file, with hard boundaries and public-API-only access via the Registry.

---

## Expected arguments
- `MODULE=<module-id>` (required). Example: `backend.repo` or `frontend.design`
- `FEATURE=<feature-id>` (optional). Example: `003-goals-agents-mvp`.  
  If omitted, **discover** by reading `specs/*/tasks.by-module/<MODULE>-tasks.md`.

---

## Inputs & Layout (YOUR repo)
- Features live at: `specs/<FEATURE>/`
- Global tasks: `specs/<FEATURE>/tasks.md`
- Per-module tasks: `specs/<FEATURE>/tasks.by-module/<MODULE>-tasks.md`
- Handoff file: `specs/<FEATURE>/handoff.md` (create if missing)
- Constitutions:
  - Global: `.specify/memory/constitution.md`
  - Module-local (optional): `.specify/memory/<MODULE>.constitution.md`
- Public API Registry (MANDATORY): `.specify/memory/public/registry.yaml`
- Validators:  
  - `.specify/scripts/registry_validate.py`  
  - `.specify/scripts/manifest_lint.py`

---

## Procedure (do this in order)

### 1) Argument parsing & discovery
1. Parse user arguments. If `MODULE` missing → **STOP** with error.  
2. If `FEATURE` not provided:
   - Search for `specs/*/tasks.by-module/<MODULE>-tasks.md`.  
   - If exactly one match → use that `<FEATURE>`. Else → **STOP** and request explicit `FEATURE`.
3. Compute absolute paths for all files listed in **Inputs & Layout**.  
   **REQUIRE**: `plan.md` and `<MODULE>-tasks.md` must exist; otherwise instruct to run `/plan` or `/module-tasks`.

### 2) Load context (Registry-driven, NO deep-inspection)
4. Read `.specify/memory/public/registry.yaml`:
   - Find `<MODULE>` entry → read: `allowed_dirs`, `import_hint`, `uses`, `manifest`, `contract`, `semver`.
   - For each module in `uses`, read **their** `manifest` and `contract` too.
5. **Treat dependencies as opaque**:  
   - Use ONLY their MANIFEST + CONTRACT;  
   - **Do NOT** open or scan their source directories;  
   - Imports must follow `import_hint` only.
6. Load constitutions: global + module-local (if any). Enforce clean code gates and boundaries.

### 3) Execute per-module tasks (TDD-first, boundaries enforced)
7. Parse `specs/<FEATURE>/tasks.by-module/<MODULE>-tasks.md`:
   - Identify phases, `[P]` markers (parallel-safe), explicit file paths, dependencies.
   - Ensure all paths are **within `allowed_dirs`** for this module. If not → **STOP** and fix tasks file first.
8. Execute by phases (Setup → Tests → Implementation → Integration → Polish):
   - **TDD**: tests must be authored to fail before implementation.
   - `[P]`: run in parallel only if tasks touch different files and have no deps.
   - Same-file tasks must be sequential.
   - After a task truly passes (tests/linters), mark `[x]` in the module tasks file and commit.

### 4) Public API Docs sync (mandatory)
9. If public exports were changed/added/removed:
   - Update `<MODULE>.manifest` (`.specify/memory/public/*.api.md`): **Exports**, **Types**, **Usage**, **Version: x.y.z**.
   - Update `<MODULE>.contract` (`.d.ts` or `Protocol.py`) accordingly.
   - **SemVer**:  
     - additive (backward-compatible) → MINOR;  
     - breaking change → MAJOR;  
     - bugfix / doc-only → PATCH.
10. Run validators (must pass):
    ```bash
    python .specify/scripts/registry_validate.py
    python .specify/scripts/manifest_lint.py
    ```

### 5) Handoff instead of cross-module edits
11. If some change is needed in another module:
    - Append an entry to `specs/<FEATURE>/handoff.md`:
      - `from`: <MODULE>
      - `to`: <target-module-id>
      - `reason`: <why>
      - `required change`: <API addition/change described via manifest + contract>
      - `blocking`: yes|no
    - **STOP** editing foreign modules.

### 6) Safety rails
- Never modify files outside `<MODULE>` `allowed_dirs`.
- Never import symbols from other modules except via their `import_hint`.
- If the per-module task file lacks explicit paths or includes foreign paths → fix tasks first (do not guess).
- Follow Clean Code & simplicity rules from constitution (SOLID, no magic values, small functions/files, DRY, KISS).

### 7) Completion report
12. Output a concise summary:
    - Completed task IDs
    - Files created/modified
    - API/manifest updates + new SemVer
    - Validators status
    - Any HANDOFF items created

---

## Notes
- This command assumes the module tasks already exist. If not, run `/fanout-tasks <FEATURE>` then `/module-tasks <FEATURE> <MODULE>`.
- Do not “peek” into other modules’ sources. MANIFEST + CONTRACT are the only allowed external knowledge.
