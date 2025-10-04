# /module-tasks <feature-id> <module>

**Goal**
Generate/refresh one module’s detailed task file by merging:
- Global constitution + `<module>.constitution.md` (if present)
- Global tasks for this module (from the FANOUT block)
- Feature design docs (plan.md required)

**Args**
- `<feature-id>` (e.g., `001-ui-llm-get`)
- `<module>` (e.g., `backend`, `frontend`, `repo`, ...)

**Reads**
- `.specify/memory/constitution.md` (global)
- `.specify/memory/<module>.constitution.md` (optional)
- `.specs/<feature-id>/plan.md` (required)
- `.specs/<feature-id>/data-model.md`, `contracts/`, `research.md` (optional)
- `.specs/<feature-id>/tasks.by-module/<module>-tasks.md` (scaffold)

**Writes**
- Update the same file, but:
  - **Do not** modify the protected FANOUT block
  - Expand other sections into file-scoped, TDD-first steps (tests → impl → integration → polish)
  - Enforce boundary rules from constitutions

**Rules**
- Tests must be authored and must fail before implementation
- `[P]` only when tasks touch different files and have no deps
- If cross-module edits are required, generate a **handoff note** instead of changing other modules