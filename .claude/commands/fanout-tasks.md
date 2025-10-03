# /fanout-tasks <feature-id>

**Goal**
Split the GLOBAL feature task file into per-module scaffolds (no deep expansion). Refresh only the protected _FANOUT_ block in each module file.

**Args**
- `<feature-id>`: directory under `.specify/specs/` (e.g., `001-ui-llm-get`)

**Reads**
- `.specify/specs/<feature-id>/tasks.md` (global)
- `.specify/templates/module-tasks-template.md` (optional scaffold)

**Writes**
- `.specify/specs/<feature-id>/tasks.by-module/<module>-tasks.md`
  - Create if missing (seed from template if present)
  - Update ONLY the block between:
    `<!-- FANOUT:BEGIN --> ... <!-- FANOUT:END -->`

**Module detection**
1) Prefer explicit `@module(<name>)` tag in the task line.
2) If missing, infer by path hints:
   - `backend/` → `backend`
   - `frontend/` → `frontend`
   - `api/` → `api`
   - `repo/` → `repo`
   - `ios/` → `ios`
   - `android/` → `android`
   (Extend in the helper script if needed.)

**Procedure**
```bash
python .specify/scripts/fanout_tasks.py "<feature-id>"
```

Notes

Do NOT load module constitutions here; this is a pure fan-out step.
Print a summary of modules and item counts when done.
If some items have no detectable module, list them as "unassigned" in the summary.