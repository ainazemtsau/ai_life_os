# Tasks: [FEATURE NAME]

**Scope**: Target modules only (from plan.md Machine-readable Scope).  
**Source**: plan.md + registry.yaml + spec.md.

---

## Module API Matrix (Target Modules)
| Module ID | Kind | Uses | Manifest | Contract | Import Hint | SemVer |
|-----------|------|------|----------|----------|-------------|--------|
<!-- Filled by /tasks with ONLY target modules -->

---

## Preparation
- [ ] T000 @prio(P1) Bootstrap missing modules via `/module-bootstrap FROM_TASKS=[###-feature]`
- [ ] T001 @prio(P1) Validate docs-as-code:
      ```bash
      python .specify/scripts/registry_validate.py
      python .specify/scripts/manifest_lint.py
      ```

---

## Global Tasks (TDD-first)
<!-- repeated per Target Module -->
- [ ] T0xx **Define contract** @module(<id>) @prio(P1)
- [ ] T0xx **Write tests** @module(<id>) @prio(P1) [TDD]
- [ ] T0xx **Implement** @module(<id>) @prio(P1)
- [ ] T0xx **Update manifest** @module(<id>) @prio(P1)
- [ ] T0xx **Verify module** @module(<id>) @prio(P1)

### Integration (Next.js router glue)
- [ ] T0yy **Enable dark theme globally** @module(<router-owner>) @prio(P1)
- [ ] T0yy **Wire "/" (DashboardRoute)** @module(<router-owner>) @prio(P1)
- [ ] T0yy **Wire "/goals" (GoalsRoute)** @module(<router-owner>) @prio(P1)

---

## Gates
- TDD, no deep imports, manifests & semver synced, CI (lint/typecheck) passes.

## Next
Run: `/module-bootstrap FROM_TASKS=[###-feature]` → `/fanout-tasks [###-feature]`
