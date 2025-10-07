---
description: Run quality gates for a single module and emit a READY report (or BLOCKED). Updates docs, suggests SemVer bump and a Conventional Commit message.
---

User input:

$ARGUMENTS
# Expected: MODULE=<module-id> [FIX=1]

Goal
- Validate that the module meets its Definition of Done (tests, lint, contracts, docs-sync).
- If FIX=1, allow minor auto-fixes (e.g., regenerate OpenAPI, re-run linters format).

Preconditions
- `/tasks` and `/fanout-tasks` completed (module playbook present).
- Implementation has been attempted via `/module-implement` (not strictly enforced).

Steps

1) Parse arguments
   - Extract `MODULE` (required). If missing → ERROR.

2) Resolve context
   - `.specify/scripts/bash/setup-plan.sh --json` → { SPECS_DIR, BRANCH }.
   - Load `.specify/memory/public/registry.yaml` → read entry for MODULE:
     , `manifest`, `contract`, `import_hint`, `semver`, `uses`.

3) Quality Gates (ZERO TOLERANCE - Constitution 9.1)
   - **Tests:** Run module tests (unit + integration)
     * MUST pass 100%. NO failing tests allowed.
     * If ANY test fails → **BLOCKED: tests**
   - **Lint:** Run linter (ruff/eslint) on module code
     * MUST be completely clean. NO errors, NO warnings.
     * If ANY lint issue exists → **BLOCKED: lint**
     * NEVER suggest ignoring rules. ALWAYS require refactoring.
   - **Types:** Run type checker (mypy/tsc) on module code
     * MUST pass with NO type errors.
     * If ANY type error exists → **BLOCKED: types**

4) Contracts
   - If `contract` ends with `.yaml` or `.yml` (OpenAPI):
     * (Re)generate spec if FIX=1 (e.g., `python backend/scripts/export_openapi.py`).
     * Lint: `npx @redocly/cli lint <contract>`.
     * Fail if errors present → **BLOCKED: contract**.
   - Else (in-process port / protocols):
     * Run `.specify/scripts/manifest_lint.py` (if available) to check manifest vs exported symbols.
     * Optionally import module with `import_hint` in a dry-run to ensure symbols exist.

5) Docs sync
   - Ensure `.specify/memory/public/<MODULE>.api.md` reflects current public exports (types, usage, changelog):
     * If mismatch detected and FIX=1 → update sections; else → **BLOCKED: docs-sync**.
   - If public surface changed:
     * Propose SemVer bump: MAJOR | MINOR | PATCH (determine from diff type).
     * Write proposal at the end of the READY report.

6) Gate: cross-artifact validators
   - `python .specify/scripts/registry_validate.py`
   - `python .specify/scripts/manifest_lint.py`
   - If fail → **BLOCKED: docs gates**.

7) READY report
   - When all gates pass: print
     * `Module: <MODULE>`
     * `SemVer: <old> -> <new or unchanged>`
     * `Tests: PASS`, `Lint: PASS`, `Types: PASS`, `Contract: PASS`, `Docs-sync: PASS`
     * Suggested commit message (Conventional Commits):
       ```
       feat(<MODULE>): complete module playbook to READY [public-api]

       - tests: add contract/integration/unit
       - impl: [short summary]
       - docs: manifest sync, OpenAPI lint
       - semver: <old> -> <new>
       ```
   - If any gate fails: list **BLOCKED reasons** with actionable fix requirements (NEVER suggest disabling checks).

8) Optional registry status update (if your validator allows it)
   - (If you keep status fields) set:
     * `status: ready`
     * `last_verified: <YYYY-MM-DD>`
     * `last_contract_sha: <calculated or left blank>`
   - If your registry validator rejects extra fields, skip this step and only print the report.

Behavior constraints
- Scope everything to MODULE's code.
- Do not auto-edit other modules; instead, emit **handoff** suggestions.
- **ZERO TOLERANCE:** If ANY quality check fails, module is BLOCKED. NO exceptions.
- **NEVER** suggest disabling lint rules, ignoring type errors, or skipping tests.
- **ALWAYS** provide refactoring suggestions: split functions, use DTOs, extract methods, reduce complexity.

Suggested next step
- If READY: commit manually with the suggested message.
- Else: Fix ALL BLOCKED items via refactoring, then re-run `/module-verify MODULE=<MODULE>`.
