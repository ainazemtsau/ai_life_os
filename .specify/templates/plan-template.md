# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]  
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

---

## Goal (LEAN)
Fix **module boundaries** and **public surfaces** now. Keep **one HTTP contract = OpenAPI** (backend). No `.d.ts`, no Python Protocols. Generate tasks later via `/tasks`.

## 1) Context & Constraints (short)
Key constraints (e.g., single-user, last-write-wins), non-goals (keep it minimal).

## 2) Module Map
- **backend.[feature]** — REST API (single source = OpenAPI).
- **frontend.[feature]** — UI using backend.[feature].
- **frontend.design** — design system (use only if present/required).

## 3) Public Surfaces (authoritative)
| Module | Kind | What is public | How to use |
|---|---|---|---|
| backend.[feature] | py | Endpoints per OpenAPI (GET/POST/PATCH/DELETE …); errors = RFC 7807 `Problem` | Contract: `backend/src/.../contracts/[feature]_openapi.yaml` |
| frontend.design | ts | { Button, Dialog, Input, Label, Card, Badge } | `import { Button } from '@/features/design'` |
| frontend.[feature] | ts | { components, hooks } | `import { GoalList } from '@/features/[feature]'` |

> Anything not listed here is **private**.

## 4) Contracts
- **OpenAPI 3.1** for backend HTTP modules (single source of truth). Include `components.schemas.Problem` per RFC 7807.  
- Frontend consumes OpenAPI → types/SDK are generated outside `/plan`.

## 5) Vertical Steps (outline for /tasks, ~8–10)
1) DB/migrations  
2) Endpoints (contract tests → implementation)  
3) Export/validate OpenAPI  
4) Generate TS types/SDK from OpenAPI  
5) Frontend data client  
6) UI: list + create  
7) UI: edit/toggle/delete  
8) Validations/empty states  
9) E2E from spec  
10) Polish errors (RFC 7807)

## 6) Risks & Notes (short)

## 7) Gates
- `registry.yaml` updated; minimal manifests exist; OpenAPI path present.
- No deep imports across modules; only public surfaces/contract usage.
- SemVer bump only when OpenAPI changes; Conventional Commits.
