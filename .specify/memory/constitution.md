<!-- Sync Impact Report:
Version Change: 1.2.0 -> 1.3.0
Principles: Kept; strengthened Clean Code & UV-only package policy
Added Sections: Package Management (UV-only), Clean Code hard constraints expanded
Removed Sections: Any references to non-UV tooling
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
- `/module-tasks <feature-id> <module>` expands file-scoped steps (tests → implementation → integration → polish) **outside** the FANOUT block.
- `/implement MODULE=<name> [FEATURE=<id>]` executes **strictly** within module boundaries.

## Package Management (UV-only)
- **UV is the single source of truth.** Use `pyproject.toml` + `uv.lock`.
- **Required commands:** `uv lock`, `uv sync`, `uv run ...`.
- **Prohibited:** `requirements*.txt`, pip, pip-tools, Poetry, Conda, Hatch build steps (unless explicitly re-approved later).
- Changes that introduce non-UV package management **must be rejected** in review.

## Clean Code & Simplicity (NON-NEGOTIABLE)
- **Readability first:** intention-revealing names, English only, no abbreviations.
- **SOLID strictly enforced:**
  - *S*: single responsibility for modules/classes/functions.
  - *O*: extension via interfaces/composition; avoid modification of stable code.
  - *L*: substitutable abstractions; no surprising side effects.
  - *I*: small, focused interfaces; no “god” interfaces.
  - *D*: depend on abstractions; repositories/services behind contracts.
- **No magic values:** magic numbers/strings are forbidden. Extract to named constants or config in `config/`. Enforced by lint rules (e.g., PLR2004).
- **Small units:** functions ≤ ~40 lines; files ≤ ~300 lines. If larger — split/refactor.
- **Low complexity:** cyclomatic complexity ≤ 8 (Ruff mccabe).
- **Explicit types:** no untyped defs in production; return types required; mypy strict-ish must pass.
- **DRY:** deduplicate logic; extract helpers; forbid copy-paste across modules.
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
- **Lint gate:** `uv run ruff check .` must pass (configured rule set).
- **Type gate:** `uv run mypy src` must pass for the changed module.
- **Test gate:** failing tests first → then passing; tasks cannot be ticked `[x]` until all gates pass.

## Development Workflow
TDD in module tasks; peer reviews verify ethics/privacy; deployments require safety validation.

## Secrets Policy
No secrets in VCS. Use `.env` (ignored) or a secret manager; never log secrets.

## Observability & CI
Structured logs; basic health checks; CI runs lint/type/test gates for impacted modules.

**Version**: 1.3.0 | **Ratified**: 2025-10-04 | **Last Amended**: 2025-10-04