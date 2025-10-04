# /module-tasks <feature-id> <module-id>

**Reads**
- `specs/<feature-id>/plan.md`
- `specs/<feature-id>/tasks.md` (global)
- `.specify/memory/public/registry.yaml`
- MANIFEST + CONTRACT for `<module-id>` and for all modules in its `uses` list
- Global constitution + `.specify/memory/<module-id>.constitution.md` (if exists)

**Rules**
- Treat all dependencies as opaque: use their MANIFEST/CONTRACT only; do not read their sources.
- Respect `allowed_dirs` boundaries for `<module-id>`.
- If dependent API is missing → append a HANDOFF to `specs/<feature-id>/handoff.md` for the owner module.

**Expand**
- Generate detailed tasks in `specs/<feature-id>/tasks.by-module/<module-id>-tasks.md`:
  - Phases: Setup → Tests → Implementation → Integration → Polish → **Docs sync**
  - Each task must include concrete file paths inside `allowed_dirs`.
  - **Docs sync** must include:
    - Update MANIFEST (add/change exports)
    - Update CONTRACT (.d.ts/Protocol)
    - Bump module SemVer if public API changed
    - Run: `python .specify/scripts/registry_validate.py`
    - Run: `python .specify/scripts/manifest_lint.py`

**Output**
- Overwrite only outside the protected FANOUT block.
