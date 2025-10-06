
---

## 3) Modules & Public Surfaces
A **module** is a bounded context with a public API. Consumers may use **only** what’s published.

**Registry (MANDATORY):** `.specify/memory/public/registry.yaml` — single source of truth.
Each module entry MUST define:
- `kind` (`python` | `typescript`)
- `semver` (module version)
- `manifest` → `docs/public/<module>.api.md` (human-readable)
- `contract` → language-level contract:
  - Backend HTTP: `backend/src/.../contracts/<name>_openapi.yaml`
  - Backend in-process: Python Protocols in `backend/src/.../contracts/*.py`
  - Frontend: `frontend/src/contracts/*.d.ts`
- `import_hint` (how consumers import public in-process API)
- `allowed_dirs` (paths the assistant may touch)
- `uses` (dependencies by module id)

**Rules:**
- **No cross-module source reading/editing.** Use only public contracts/manifests.
- Imports MUST follow `import_hint`. **No deep imports**.
- Any missing capability → create **handoff** (`specs/<feature>/handoff.md`) — do not patch providers directly (CDC).

---

## 4) Contracts: HTTP vs In-Process
We support two kinds of public interfaces:

### 4.1 HTTP Contracts (cross-process)
- **OpenAPI 3.1** lives under `backend/src/.../contracts/*.yaml`.
- Export via script (e.g., `backend/scripts/export_openapi.py`).
- Minimal requirements for lint:
  - Root: `servers` present, `security: []` (explicit “no auth” for MVP)
  - Pass **Redocly CLI** lint.
- Structured errors (RFC 7807) are **RECOMMENDED** but **OPTIONAL** at MVP:
  - You MAY wrap routers with a shared error response map (e.g., `core.httpkit`).
  - Do not block features purely on Problem schema presence; quality improves over time.

### 4.2 In-Process Contracts (same process)
- Backend: **PEP 544 Protocols** in `backend/.../contracts/*.py`.
- Frontend: **TypeScript `*.d.ts`** under `frontend/src/contracts/`.
- Public implementations are re-exported through module **public hubs** (e.g., `ai_life_backend/<module>/public`).
- Consumers import **only** via `import_hint`.

---

## 5) Manifests (human-readable)
- Location: `docs/public/<module>.api.md`.
- Contents (concise): Overview, **Exports** (what is public), **Types**, **Usage**, **Versioning (Changelog)**.
- Any change to public surface ⇒ update manifest & bump SemVer.

---

## 6) Versioning & Commits
- **SemVer per module:** MAJOR (breaking), MINOR (additive), PATCH (fix).
- **Conventional Commits** with module scope:
  - `feat(backend.goals): add GET /api/goals [public-api]`
  - `fix(frontend.design): correct Button props [public-api]`

---

## 7) Command Flow & Gates (Spec Kit)
**Sequence (default):**
1. `/specify` → create `spec.md` (WHAT, not HOW).
2. `/clarify` → up to 5 targeted questions; record answers into spec.
3. *(optional)* `/research-brief` → short fact pack; no code.
4. *(as needed)* `/design-spike` → explore approaches (trade-offs).
5. *(as needed)* `/adr` → decide & record the chosen option.
6. `/plan` (thin) → scope, **no hardcoded modules**, link ADR/spike; re-use registry.
7. `/tasks` → generate `tasks.md` + `tasks.by-module/*.md` (playbooks with DoD).
8. `/fanout-tasks <feature-id>` → sync global → per-module **FANOUT** blocks.
9. `/module-implement MODULE=<id>` → TDD implementation **only in allowed_dirs**.
10. `/module-verify MODULE=<id>` → quality gates, READY report (or BLOCKED).
11. Manual commit (use suggested Conventional Commit).

**Gates (must pass before READY):**
- Tests (unit/integration/**contract**) are green for the module.
- Lint & type checks are clean (scoped to module).
- Contract exported & validated (OpenAPI lint or Protocol/d.ts consistency).
- Manifest updated & SemVer bump applied (if public surface changed).
- Registry & manifest validators pass.

---

## 8) Module Definition of Done (DoD)
A module is **READY** when:
- [ ] Tests green (unit / integration / **contract** if applicable).
- [ ] Lint & type checks pass.
- [ ] Public contract present & validated:
  - HTTP: OpenAPI 3.1 exported + `npx @redocly/cli lint` passes.
  - In-process: exported symbols match manifest/Protocols/`*.d.ts`.
- [ ] Manifest in `docs/public/` is up to date (Exports/Types/Usage/Changelog).
- [ ] **SemVer** bumped appropriately; Conventional Commit prepared.

---

## 9) Clean Code Rules (enforced)
- **Readability first**, intention-revealing names, English identifiers.
- **SOLID** strictly:
  - S: single responsibility (modules/classes/functions).
  - O: extend via interfaces/composition; avoid modifying stable code.
  - L: substitutable abstractions; no surprising side effects.
  - I: small interfaces; avoid “god” interfaces.
  - D: depend on abstractions; repositories/services behind contracts.
- **KISS/YAGNI**, **DRY**.
- Functions ≤ 40 lines; files ≈ ≤ 300 lines; cyclomatic complexity ≤ 8.
- Explicit types everywhere; no untyped prod functions.
- No global mutable state; side effects at the edges (api/infra).
- Fail fast; explicit exceptions; no silent catches.
- Docstrings for public APIs; comments explain **why**, not **what**.

---

## 10) Tools & Quality (tool-neutral, scoped)
**Backend (Python):**
- Use `pyproject.toml` if available; venv or uv — **allowed** (don’t mix in one module).
- **Linters/Types/Tests:** `ruff`, `mypy`, `pytest` (scoped to module paths).

**Frontend (TypeScript/React):**
- Package manager: `pnpm` or `npm` (project-level choice).
- **Lint/Types/Format:** ESLint, `tsc`, Prettier, Tailwind conventions.

**HTTP Contracts:** `npx @redocly/cli lint <openapi.yaml>`.

---

## 11) Security, Privacy, Observability
- No secrets in VCS; use `.env` (ignored) or a secret manager.
- Log minimally and never log secrets or PII.
- Health checks are available; structured logs preferred.
- If/when auth appears, document root `securitySchemes` (OpenAPI).

---

## 12) Violations & Handoffs
- Need something from another module? Write **handoff** in `specs/<feature>/handoff.md` (CDC request). Do **not** edit foreign sources.
- If a rule must be bent, record rationale in an ADR and **scope it narrowly**.

---

## 13) Status
**Version:** 1.5.0  
**Ratified:** 2025-10-06  
**Last Amended:** 2025-10-06
