# /new-module <id> kind=(python|typescript) [uses="a,b,c"]

**Goal**
Scaffold a new module, register its public API placeholders, and enforce boundaries.

**Args**
- `<id>`: "side.name" (e.g., backend.repo, frontend.design)
- `kind`: python | typescript
- `uses`: optional csv of module ids this module will depend on

**Steps**
1) Run: `python .specify/scripts/registry_validate.py` (allow empty modules list).
2) Run: `python .specify/scripts/new_module.py --id <id> --kind <kind> --uses "<uses>"`.
3) Run: `python .specify/scripts/registry_validate.py` again.
4) Create module constitution: `.specify/memory/<id>.constitution.md` with module-local rules (paths must match allowed_dirs).
5) Print summary with:
   - manifest path
   - contract path
   - allowed_dirs
   - import_hint
   - uses
6) Add two high-level tasks to the current feature (global `specs/<feature>/tasks.md`):
   - `Create module <id>` (this must be first for this module)
   - `Publish API <id>` (fill manifest/contract; bump semver if needed)

**Notes**
- Do not open or read other modules' sources. Use registry/manifest/contract only.
