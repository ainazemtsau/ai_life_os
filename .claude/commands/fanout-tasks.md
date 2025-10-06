# /fanout-tasks <feature-id>

**Goal**
Split the GLOBAL feature task file into per-module playbooks ONLY for modules referenced by `@module(<id>)` tags. Do not generate files for modules with zero tasks.

**Args**
- `<feature-id>`: directory under `specs/` (e.g., `002-basic-navigation-mvp`)

**Reads**
- `specs/<feature-id>/tasks.md` (global)
- `.specify/templates/module-tasks-template.md` (optional scaffold)

**Writes**
- `specs/<feature-id>/tasks.by-module/<module>-tasks.md`
  - Create if missing (seed from template if present)
  - Update ONLY the block between:
    `<!-- FANOUT:BEGIN --> ... <!-- FANOUT:END -->`

**Module detection (STRICT)**
- Parse `tasks.md`, collect distinct modules from `@module(<id>)` tags.
- DO NOT include modules absent in tags (even if present in registry.yaml or plan.md).
- If none found → ERROR "No module-tagged tasks to fan out."

**Procedure**
```bash
python .specify/scripts/fanout_tasks.py "<feature-id>"
