# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]  
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

---

## Execution Flow (performed by `/plan`)

> Goal: lock module boundaries **now**, bootstrap public docs (registry + manifests + contracts), then design **contract-first**.  
> Tasks will be generated later by `/tasks` (no task file here).

### M0. Module Partition & Registry Bootstrap (MANDATORY, executed now)
1) Load `.specify/memory/public/registry.yaml` (create if missing).  
2) Derive **module set** for this feature (bounded contexts; one module = one black box/public API):
   - **frontend.design** — shared design system (if missing → create).
   - **backend.[feature]** — all server responsibility for this feature (internals may have domain/app/infra/api; that’s internal).
   - **frontend.[feature]** — UI for this feature.
   - **backend.core** — *optional*, only if truly cross-cutting (errors, tracing contracts, tiny utilities).
3) For **each required module**:  
   - If absent in registry → run `/new-module <id> kind=(python|typescript) uses="<csv>"`.  
     Examples for a typical web feature:
     - `/new-module backend.[feature] kind=python uses="backend.core"` (omit `backend.core` if not used)
     - `/new-module frontend.design kind=typescript`
     - `/new-module frontend.[feature] kind=typescript uses="frontend.design,backend.[feature]"`
   - Ensure **manifest** `.specify/memory/public/<id>.api.md` and **language contract** exist (`backend`: Protocol/OpenAPI path; `frontend`: `*.d.ts`).  
   - Ensure `allowed_dirs` and `import_hint` are set.
4) **Validate** docs-as-code gates:  
   ```bash
   python .specify/scripts/registry_validate.py
   python .specify/scripts/manifest_lint.py
If any fail → STOP with: "Fix module registry/docs first".

Rationale: modules are bounded contexts with clear external contracts; internals stay private; dependencies go through ports/contracts only. 

0. Load Feature Spec
If missing → ERROR "No feature spec at {path}"

1. Technical Context (scaffold-level only)
Record environment decisions for scaffolding (do not push tech names into tasks):
Backend/Frontend frameworks, DB, tooling.

Frameworks are details of adapters; they don’t shape the domain plan. (Hexagonal) 

2. Constitution Gate (initial)
Public API only via registry + manifest + contract; no cross-module source reading; imports follow import_hint.

Clean Code gates from constitution (SOLID, DRY, KISS; no magic; small functions).

If violated → document deviation or ERROR "Simplify approach first".

3. Phase 0 — research.md (domain/UX unknowns only)
Clarify domain rules, acceptance, UX copy. No low-level tech here.

4. Phase 1 — Design & Contracts (contract-first)
data-model.md: entities and invariants (domain-level, no ORM specifics).

contracts/: HTTP contract for backend.[feature] (OpenAPI); front *.d.ts for public types (DS + feature).

quickstart.md: end-to-end acceptance flow.

No implementation. Provide failing test skeleton descriptions only.

Consumer-Driven Contracts: consumers define expectations; providers evolve safely. 

5. Constitution Gate (post-design)
Re-check boundaries/CDC. If leaks → refactor design and update contracts.

6. Phase 2 — Task Planning (describe only; do NOT create tasks)
/tasks will read Phase 1 artifacts + .specify/templates/tasks-template.md, then generate tasks.md with TDD order and [P] markers.

/fanout-tasks groups by @module(<id>) → specs/[feature]/tasks.by-module/*.md.

/module-tasks expands each module with exact paths inside allowed_dirs, ending with Docs sync:

Update manifest (Exports/Types/Usage/Version)

Update language contract (.d.ts / Protocol / OpenAPI)

SemVer bump (MINOR for additive, MAJOR for breaking; PATCH otherwise)

Run validators: registry_validate.py and manifest_lint.py

Docs treated as code; changes versioned & reviewed. 

STOP — Ready for /tasks (this plan must not create tasks.md)

Module API Matrix (authoritative, filled in M0)
Public surfaces only. Internals (domain/app/infra/api) are private to the module.

Module ID	Kind	Provides (public surface)	Uses	Manifest Path	Contract Path	allowed_dirs (summary)	import_hint	SemVer
backend.[feature]	py	HTTP API (OpenAPI) for this feature	backend.core (optional)	.specify/memory/public/backend.[feature].api.md	backend/src/…/contracts/[feature]_openapi.(yml	py)	backend/src/…/[feature]/**	from ….[feature].public import api
frontend.design	ts	Design system components/tokens	—	.specify/memory/public/frontend.design.api.md	frontend/src/contracts/design.d.ts	frontend/src/components/ds/**	import {…} from '@/components/ds'	0.1.0
frontend.[feature]	ts	Feature UI (uses backend.[feature] + DS)	frontend.design, backend.[feature]	.specify/memory/public/frontend.[feature].api.md	frontend/src/contracts/[feature].d.ts	frontend/src/features/[feature]/**	import * as feature from '@/features/…'	0.1.0
backend.core (*)	py	Cross-cutting primitives (errors, tracing)	—	.specify/memory/public/backend.core.api.md	backend/src/…/contracts/core_protocols.py	backend/src/…/core/**	from …core.public import core	0.1.0

(*) Add only when truly cross-cutting; no domain logic inside.

Technical Context (scaffold snapshot)
Backend/Frontend frameworks, DB, tooling (for environment & scaffolding only).

Keep tasks technology-neutral; contracts drive the work.

SemVer for public APIs; Conventional Commits for history/automation. 

Project Structure (by modules, not layers)
backend/
  src/…/[feature]/**          # internals of backend.[feature] (domain/app/infra/api inside)
  src/…/core/**               # backend.core internals (optional)
  tests/{contract, integration, unit}/**
frontend/
  src/components/ds/**        # frontend.design
  src/features/[feature]/**   # frontend.[feature]
Deliverables from /plan
Module registry updated & validated; manifests + language contracts scaffolded.

research.md, data-model.md, contracts/ (OpenAPI/.d.ts), quickstart.md.

This plan.md with Module API Matrix and gates.

Gates & Policies
Docs-as-Code: manifests/contracts live in repo; changes gated by validators. 

CDC: consumers request changes via handoff; providers evolve contracts safely. 

SemVer + Conventional Commits for public APIs. 

No cross-module source reading; imports follow import_hint; changes only within allowed_dirs.

Clean Code: SOLID/DRY/KISS; no magic values; small, readable units.

Progress Tracking
 M0: Modules bootstrapped (registry/manifests/contracts validated)

 Phase 0: Research complete

 Phase 1: Design complete

 Phase 2: Task planning ready (run /tasks)

 Phase 3: Tasks generated

 Phase 4: Implementation complete

 Phase 5: Validation passed