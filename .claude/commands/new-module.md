---
description: (Deprecated alias) Create a single module by delegating to /module-bootstrap. Prefer /module-bootstrap FROM_TASKS=<feature-id>.
---

User input:

$ARGUMENTS
# Usage:
#   /new-module <id> kind=(python|typescript) [uses="a,b,c"] [FORCE=1] [DRY_RUN=1]

Status
- DEPRECATED as a primary workflow step.
- Prefer: /module-bootstrap FROM_TASKS=<feature-id>  (bulk, consistent with tasks)
- This command calls /module-bootstrap MODULE=<id> under the hood and fills inferred fields.

Behavior
1) Validate <id> format: "frontend.*" or "backend.*".
2) Infer kind from prefix if kind is omitted.
3) Build a module creation plan:
   - manifest: docs/public/<id>.api.md
   - contract:
     * frontend.* → frontend/src/contracts/<name>.d.ts
     * backend.*  → backend/src/ai_life_backend/contracts/<name>_protocols.py
   - import_hint:
     * frontend.* → import * as <name> from '@/features/<name>'
     * backend.*  → from ai_life_backend.<name>.public import *
   - uses: from `uses="a,b,c"` if provided, else [].
   - Special cases:
     * frontend.app-shell additionally owns frontend/src/app/**
4) Delegate to /module-bootstrap:
   - /module-bootstrap MODULE=<id> [FORCE=1] [DRY_RUN=1]
5) Run validators:
   - python .specify/scripts/registry_validate.py
   - python .specify/scripts/manifest_lint.py

Notes
- Does NOT modify feature tasks; generate tasks via /tasks and /fanout-tasks.
- Prefer bulk creation via /module-bootstrap FROM_TASKS to keep plan ↔ tasks ↔ registry in sync.

Examples
- /new-module frontend.dashboard kind=typescript uses="frontend.design"
- /new-module frontend.app-shell kind=typescript uses="frontend.design,frontend.dashboard,frontend.goals"
- /new-module backend.reports kind=python
