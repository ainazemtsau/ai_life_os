# Module Playbook — [MODULE_ID]

**Kind**: [KIND] | **SemVer**: [SEMVER]  
**Manifest**: [MANIFEST_PATH]  
**Contract**: [CONTRACT_PATH]  
**Import hint**: `[IMPORT_HINT]`  
**Allowed dirs**:  
[ALLOWED_DIRS_LIST]

---

## Definition of Done (module READY)
- [ ] Tests green (unit / integration / **contract** if applicable)
- [ ] Lint & type checks pass
- [ ] Public contract exported & validated
  - If HTTP: OpenAPI 3.1 exported and `npx @redocly/cli lint` passes  :contentReference[oaicite:10]{index=10}
  - If in-process: exported DTO/functions match manifest
- [ ] Manifest updated (exports/types/usage) and consistent
- [ ] **SemVer** bumped if public surface changed (MAJOR/MINOR/PATCH)  :contentReference[oaicite:11]{index=11}
- [ ] Conventional Commits prepared for changes  :contentReference[oaicite:12]{index=12}

---

## Tasks (TDD order)
1) **Contract tests** (declare/author; should fail initially) — `@module([MODULE_ID])`
2) **Domain/DTO/port** (if in-process) **or** API schema (if HTTP)
3) **Repository/Service / Hooks/Components** (module internals)
4) **API routes / API client** (as applicable)
5) **Integration checks** (wire by `import_hint` or HTTP)
6) **Docs sync**: update manifest & contract; apply SemVer
7) **Verify READY**: run `/module-verify MODULE=[MODULE_ID]`

> Touch only files inside **Allowed dirs**. Use only public surfaces of other modules (HTTP or `import_hint`). **Do not** deep-import internals.  
> Prefer **Ports & Adapters**: in-process ports for same-process, HTTP contracts for cross-process. :contentReference[oaicite:13]{index=13}
