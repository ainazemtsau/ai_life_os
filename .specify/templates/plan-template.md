# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]  
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

---

## Goal (LEAN)
Freeze **module boundaries** and **public surfaces** now. Keep **one HTTP contract = OpenAPI** (backend) for external/cross-process use. Inside the same process, use a **typed in-process public port** (DTOs). No duplicate contracts (.d.ts/Protocols).

## 1) Context & Constraints (short)
Key constraints (single-user, last-write-wins, etc.).

## 2) Module Map
- **backend.[feature]** — REST API for external/cross-process + in-process public port for same-process consumers.
- **frontend.[feature]** — UI consuming backend.[feature].
- **frontend.design** — design system (use only if present/required).

## 3) Public Surfaces (authoritative)
| Module | Kind | In-process Port (same process) | HTTP Contract (cross-process/external) | How to use |
|---|---|---|---|---|
| backend.[feature] | py | `from ai_life_backend.[feature].public import ...` (DTOs; read-only unless stated) | `backend/src/.../contracts/[feature]_openapi.yaml` (OpenAPI 3.1; errors = RFC7807 `Problem`) | import or call via generated client |
| frontend.design | ts | `import { Button, ... } from '@/features/design'` | — | import entrypoint only |
| frontend.[feature] | ts | `import { components/hooks } from '@/features/[feature]'` | — | import entrypoint only |

> Anything not listed here is **private**.

## 4) Contracts
- **OpenAPI 3.1** for backend HTTP surfaces (single source of truth; include `components.schemas.Problem` per RFC 7807). :contentReference[oaicite:1]{index=1}
- In-process ports: typed functions returning **DTOs** (no ORM leakage).

## 5) Vertical Steps (outline for /tasks, ~8–10)
1) DB/migrations  
2) In-process port (DTOs + functions) + tests  
3) Endpoints (contract tests → implementation)  
4) Export/validate OpenAPI (FastAPI auto-docs) :contentReference[oaicite:2]{index=2}  
5) Generate TS types/SDK from OpenAPI  
6) Frontend data client  
7) UI: list + create  
8) UI: edit/toggle/delete  
9) E2E from spec  
10) Polish errors (RFC 7807)

## 6) Risks & Notes (short)

## 7) Gates
- `registry.yaml` updated; manifests exist; OpenAPI path present.
- **Same-process use = in-process port**; **HTTP only cross-process**.
- No deep imports; only public surfaces/contract usage.
- SemVer bump only when **public surface** changes (OpenAPI or in-process port); Conventional Commits.
