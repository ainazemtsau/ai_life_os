# /publish-api <module-id>

**Goal**
Review and update MANIFEST/CONTRACT for the module and validate the registry.

**Steps**
1) Open: registry.yaml, <manifest>, <contract>.
2) Update exports, types, usage, and Version: x.y.z (SemVer).
3) Run: `python .specify/scripts/registry_validate.py` and `python .specify/scripts/manifest_lint.py`.
4) Commit with Conventional Commit, scope = <module-id> (e.g., `feat(backend.repo): add list_goals filter [public-api]`).
