---
description: Generate global and per-module task plans (TDD-first) from plan + registry, with module DoD gates and contract coverage.
---

User input:

$ARGUMENTS

Goal: Create high-quality, minimal-noise task plans that drive implementation module-by-module to "READY" (DoD passed), without cross-module edits.

### High-level behavior
- Read the **single source of truth** for modules: `.specify/memory/public/registry.yaml`.
- Use `plan.md` only for feature scope/context; do not hardcode module IDs in templates.
- Generate:
  1) `specs/<feature>/tasks.md` (global, high-level; no file paths),
  2) `specs/<feature>/tasks.by-module/<module-id>.md` (playbooks; file-level TDD steps; DoD gates).

### Steps

1) Resolve context once:
   - Run `.specify/scripts/bash/setup-plan.sh --json` (repo root).
   - Parse JSON: `FEATURE_SPEC`, `SPECS_DIR`, `IMPL_PLAN`, `BRANCH`. Use **absolute paths** thereafter.
   - If `IMPL_PLAN` missing → ERROR "No implementation plan found — run /plan first."

2) Load inputs:
   - `IMPL_PLAN` (read-only): extract scope notes and (if present) explicit module subset;
   - `.specify/memory/public/registry.yaml`: read **all modules** (id, kind, uses, manifest, contract, import_hint, allowed_dirs, semver).
   - Optional: `specs/<feature>/decisions/*.md` (ADR) to reflect accepted decisions in tasks header.

3) Determine **module set** and order:
   - If `IMPL_PLAN` declares a module list → use it; else include all modules from `registry.yaml`.
   - Build a directed graph via `uses:` and perform **topological sort** to get a safe execution order
     (providers/core first, dependents later).

4) Prepare global task content:
   - Render `.specify/templates/tasks-template.md` into `specs/<feature>/tasks.md` by injecting:
     - `[FEATURE_NAME]`, `[BRANCH]`, `[DATE]`, `[FEATURE_DIR]`,
     - `[MODULE_API_MATRIX]`: a compact table from `registry.yaml` (id, kind, uses, manifest, contract, import_hint, semver),
     - `[GLOBAL_TASKS]`: high-level TDD items, tagged with `@module(<id>)` and `@prio(P1|P2|P3)`,
     - `[RECOMMENDATIONS]`: if missing HTTP contracts for HTTP-facing modules → suggest “export OpenAPI & lint (Redocly CLI)”, if in-process ports missing → suggest adding typed exports (DTO/functions).  
   - **Rules for global tasks**: no file paths; tests before impl (TDD); mark parallel safe items with `[P]` only when modules independent.

5) Fan-out to module playbooks:
   - For each module (in topo order), create/overwrite `specs/<feature>/tasks.by-module/<module-id>.md` from a **module playbook template** (see below).
   - Inject module-specific facts: `allowed_dirs`, `manifest`, `contract`, `import_hint`, current `semver`, and the ordered mini-backlog of steps (tests → impl → docs-sync → verify).
   - Include a **Definition of Done** checklist:
     - Tests green (unit/integration/**contract** where applicable),
     - Lint & type checks pass,
     - Contract exported & **linted** (OpenAPI → Redocly CLI),
     - Manifest updated and consistent with public surface,
     - **SemVer bump** if public surface changed (MAJOR/MINOR/PATCH),
     - Conventional Commits prepared.  
     (SemVer/Conventional Commits enable predictable API evolution and tooling.) :contentReference[oaicite:0]{index=0}

6) Contract coverage:
   - If module has HTTP surface: ensure global task list contains “Export OpenAPI” + “`npx @redocly/cli lint`” items; module playbook must include the exact command block. (Redocly CLI validates OpenAPI 3.1.) :contentReference[oaicite:1]{index=1}
   - If module exposes **in-process port**: ensure playbook includes “public exports match manifest (DTO/functions)” and unit tests **before** impl (TDD). :contentReference[oaicite:2]{index=2}
   - If consumer/provider exists → add **CDC** contract tests (e.g., Pact) in the consumer module playbook. :contentReference[oaicite:3]{index=3}

7) RFC 7807 (optional): if plan/spec mandates structured HTTP errors, add global “Problem Details” coverage task; backends must emit RFC-7807 or equivalent and validate in contract tests. :contentReference[oaicite:4]{index=4}

8) Output & report:
   - Write/overwrite `tasks.md` and all `tasks.by-module/*.md`.
   - Print absolute paths and module execution order.
   - If any module lacks a contract while being consumed, mark **BLOCKED** and recommend creating a Design-Spike/ADR before implementation.

### Behavior constraints
- Never write source code here; only task docs.
- Never cross module boundaries in playbooks; restrict edits to `allowed_dirs` from the registry.
- Keep global tasks short and unambiguous; put file paths only in per-module playbooks.
- Prefer **ports & adapters** structure (in-process ports for same-process, OpenAPI for cross-process). :contentReference[oaicite:5]{index=5}

### Done signal
Finishes successfully when:
- `specs/<feature>/tasks.md` exists and contains a Module API Matrix,
- every selected module has a playbook in `tasks.by-module/`,
- contract coverage tasks are present for all public surfaces,
- topo order printed.
