# Tasks: [FEATURE_NAME]

**Branch**: `[BRANCH]` | **Date**: [DATE]  
**Feature dir**: [FEATURE_DIR]

---

## Module API Matrix (from registry.yaml)
[MODULE_API_MATRIX]

> Public surfaces only. Internals remain private to each module. Use only `import_hint` (in-process) or HTTP (OpenAPI).

---

## Global Tasks (high-level; no file paths)
[GLOBAL_TASKS]

Guidelines:
- Tag each item with `@module(<id>)` and priority `@prio(P1|P2|P3)`.
- Mark `[P]` only if modules are independent.
- **TDD-first**: write/declare tests before implementation. :contentReference[oaicite:6]{index=6}
- Keep this section technology-agnostic; details live in module playbooks.

---

## Recommendations (preconditions & risks)
[RECOMMENDATIONS]

Common preconditions:
- HTTP modules must export **OpenAPI 3.1** and pass **Redocly CLI** lint. :contentReference[oaicite:7]{index=7}
- In-process ports must be typed and match the manifest.
- If consumer/provider coupling exists, add **CDC** tests (e.g., Pact). :contentReference[oaicite:8]{index=8}
- Definition of Done applies per module; do not proceed to next module until **READY**. :contentReference[oaicite:9]{index=9}

---

## Fan-out
Per-module playbooks created under: `tasks.by-module/`.

Execution order (topological by dependencies):
1. Core/providers
2. Feature backends
3. Feature frontends

> Finish a module to **READY** before starting the next (DoD gate).
