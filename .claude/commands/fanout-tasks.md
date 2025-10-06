**Goal**
Synchronize GLOBAL tasks (`tasks.md`) into each module’s playbook as a read-only fan-out list,
updating **only** the protected `FANOUT` block. Preserve all manual edits elsewhere.

**Args**
- `<feature-id>`: directory under `specs/` (e.g., `001-goals-management-mvp`)

**Reads**
- `specs/<feature-id>/tasks.md` (GLOBAL tasks; high-level, tagged with @module(...))
- `.specify/memory/public/registry.yaml` (authoritative module set, deps, allowed_dirs)
- `.specify/templates/module-playbook-template.md` (seed template, if a module file is missing)

**Writes**
- `specs/<feature-id>/tasks.by-module/<module-id>.md`
  - Create if missing (seed from **module-playbook-template.md**)
  - Update ONLY the block between:
    `<!-- FANOUT:BEGIN -->` … `<!-- FANOUT:END -->`
  - If the block is missing, append it at the end of file.

**Module detection**
1) Primary: explicit tag `@module(<id>)` in each GLOBAL task line.
2) Validation: `<id>` MUST exist in `registry.yaml`. If unknown → mark as **unknown** in summary.
3) (Optional fallback) If a task has no tag, leave it **unassigned** (listed in summary). Heуристики по путям отключены по умолчанию — требуем явные теги для предсказуемости.

**Order of fan-out**
- Compute a **topological order** from `uses:` in `registry.yaml` (core/providers → dependents).
- Emit summary in that order (Kahn’s algorithm). :contentReference[oaicite:1]{index=1}

**What goes into the FANOUT block**
- Header with module id and date.
- Flat checklist of GLOBAL tasks tagged этим модулем (без путей, без переписывания текста).
- Сохраняем ID задач (например, `T030`) и все теги (`@prio(P1)`, `@owner(...)`, `[P]`).

**What does NOT change**
- Любые разделы вне `FANOUT` блока (твои детальные шаги TDD, DoD, заметки).
- Содержимое `module-playbook-template.md` за пределами блока.

**Procedure**
python .specify/scripts/fanout_tasks.py "<feature-id>"
Output (summary)

Modules (topo order) with counts: backend.core (3), backend.goals (5), …

Unknown @module tags (not in registry)

Unassigned tasks (no @module)

Modules with zero items (OK; just report)
