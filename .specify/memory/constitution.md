<!-- Sync Impact Report:
Version Change: 1.3.0 -> 1.4.0
Principles: Kept; added Public API Registry & Contract-First, Module Constitutions, Docs-as-Code gates
Added Sections: Public API Registry (MANDATORY), Contract-First & CDC, Module Constitutions Policy, Docs-as-Code & Release, Command Enforcement
Removed Sections: None
Templates Updated: Compatible
Follow-up TODOs: None
-->
# AI Life OS Constitution

## Core Principles
### AI-First Architecture
Design every component with AI integration in mind; expose clear AI-facing interfaces.

### Autonomous Operation
Self-monitoring & self-healing; minimal human intervention.

### Adaptive Learning (NON-NEGOTIABLE)
Learning cycles must be safe, auditable, and ethical.

### Privacy-First Design
Encrypt at rest & in transit; consent; anonymization where possible.

### Safety & Ethics
Transparent, explainable behavior; hard safety rails.

## Security Requirements
Harden models against adversarial inputs; multi-layer auth; full encryption for user data.

## Project Structure & Module Boundaries
- Monorepo: `frontend/`, `backend/` at repo root.
- Backend src-layout: `backend/src/ai_life_backend/` with subpackages:
  - `api/` (transport), `services/` (use-cases), `repository/` (data access), `domain/` (entities), `config/` (settings).
- Interact only via **public surfaces**; **no cross-module edits**. Use handoff notes/PRs for changes in other modules.
- Assistants must not modify files outside the current module’s allowed directories.

## Spec Kit Workflow Adaptations
- Global feature `tasks.md` contains a **Module API Matrix** and high-level `@module(...)` items (no file paths).
- `/fanout-tasks <feature-id>` creates/refreshes `tasks.by-module/<module>-tasks.md` with a protected **FANOUT** block.
- `/module-tasks <feature-id> <module>` expands file-scoped steps (tests → implementation → integration → polish → **Docs sync**) **outside** the FANOUT block.
- `/implement MODULE=<name> [FEATURE=<id>]` executes **strictly** within module boundaries and loads the **Public API Registry** + module constitutions.

## Public API Registry (MANDATORY)
- Single source of truth: `.specify/memory/public/registry.yaml`.
- Each module entry MUST define: `kind`, `semver`, `manifest` (human-readable `*.api.md`), `contract` (language-level types: `.d.ts` or Python `Protocol`), `import_hint`, `allowed_dirs`, `uses` (list of modules it depends on).
- **Dependencies are opaque**: consuming modules may use ONLY what’s listed in the dependency’s `manifest` + `contract`. Reading or editing dependency sources is forbidden.
- Imports MUST follow `import_hint`. Deep imports are prohibited.

## Contract-First & CDC
- Any new capability or new dependency MUST start with **manifest/contract update** before implementation.
- If a consuming module needs something absent in the dependency API → create a **Handoff** request in `specs/<feature>/handoff.md` describing the required public addition; do not touch the dependency’s code.

## Module Constitutions Policy
- Location: `.specify/memory/<module-id>.constitution.md` (created empty by default when the module is created).
- Loading rules: a module constitution is loaded **only** when generating tasks or implementing **that** module.
- Precedence: global constitution sets the baseline; module constitution may be **stricter** but can never relax global rules.
- Scope: a module constitution may add:
  - Extra style/coding constraints (e.g., smaller complexity limits, naming patterns).
  - Domain invariants and boundaries (e.g., forbidding specific dependencies).
  - Test/lint/type gates customization for the module.
- A module constitution may **not**:
  - Expand `allowed_dirs` (only the registry defines boundaries).
  - Permit reading or editing other modules’ sources.
  - Downgrade Clean Code, security or safety requirements.

## Docs-as-Code & Release Management
- Public surfaces are documented in `*.api.md` (manifests) and language contracts (`.d.ts` / Python `Protocol`).
- Validators MUST pass on module changes:
  - `.specify/scripts/registry_validate.py`
  - `.specify/scripts/manifest_lint.py`
- SemVer is mandatory per module:
  - Additive, backward-compatible changes → **MINOR**.
  - Breaking changes → **MAJOR**.
  - Bugfix or doc-only → **PATCH**.
- Conventional Commits with module scope are required (e.g., `feat(frontend.design): add Button tone=success [public-api]`).

## Package Management (UV-only, backend)
- **UV is the single source of truth.** Use `pyproject.toml` + `uv.lock`.
- Required commands: `uv lock`, `uv sync`, `uv run ...`.
- Prohibited: `requirements*.txt`, pip, pip-tools, Poetry, Conda, Hatch build steps (unless re-approved later).
- Changes introducing non-UV tooling must be rejected.

## Clean Code & Simplicity (NON-NEGOTIABLE)
- **Readability first:** intention-revealing names, English only, no abbreviations.
- **SOLID strictly enforced:**
  - *S*: single responsibility for modules/classes/functions.
  - *O*: prefer extension via interfaces/composition; avoid modification of stable code.
  - *L*: substitutable abstractions; no surprising side effects.
  - *I*: small, focused interfaces; no “god” interfaces.
  - *D*: depend on abstractions; repositories/services behind contracts.
- **No magic values:** magic numbers/strings are forbidden. Extract to named constants or `config/`.
- **Small units:** functions ≤ ~40 lines; files ≤ ~300 lines.
- **Low complexity:** cyclomatic complexity ≤ 8.
- **Explicit types:** no untyped defs in production; return types required; strict-ish typing must pass.
- **DRY:** deduplicate logic; extract helpers.
- **KISS & YAGNI:** MVP for a single user; avoid premature abstractions.
- **No global mutable state:** inject dependencies.
- **Pure where possible:** pure domain logic; side effects at edges (api/infra).
- **Errors:** fail fast with explicit exceptions; no silent catches.
- **Docs:** docstrings for public APIs; comments explain **why**, not **what**.
- **Naming:** `snake_case` (func/vars), `PascalCase` (classes), `UPPER_SNAKE_CASE` (constants).
- **Tests-first:** tasks must write failing tests before implementation.

## Forbidden Constructs
- Wildcard imports, `exec`/`eval`, hidden I/O in getters, “god classes”, circular imports.
- Overuse of inheritance; prefer composition and small protocols.
- Cross-module edits without a handoff note.

## Module Code Gates
- **Backend:** `uv run ruff check .` and `uv run mypy src` must pass for changed modules; tests must pass.
- **Frontend:** ESLint (flat config) and `pnpm typecheck` must pass; Prettier + Tailwind formatting enforced.
- TDD: failing tests first → then passing; tasks cannot be ticked `[x]` until gates pass.

## Development Workflow
TDD in module tasks; peer reviews verify ethics/privacy; deployments require safety validation.

## Secrets Policy
No secrets in VCS. Use `.env` (ignored) or a secret manager; never log secrets.

## Observability & CI
Structured logs; basic health checks; CI runs lint/type/test gates for impacted modules.

**Version**: 1.4.0 | **Ratified**: 2025-10-04 | **Last Amended**: 2025-10-04
