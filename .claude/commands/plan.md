---
description: Execute the LEAN implementation planning workflow (short tech plan + module boundaries + single-source contracts).
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

Given the implementation details provided as an argument, do this:

1. Run `.specify/scripts/bash/setup-plan.sh --json` and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. All paths must be absolute.
   - BEFORE proceeding, ensure FEATURE_SPEC has a `## Clarifications` section or explicit user override to proceed.

2. Read:
   - FEATURE_SPEC (requirements, acceptance)
   - `.specify/memory/constitution.md`

3. Execute the LEAN plan template:
   - Load `.specify/templates/plan-template.md` (copied to IMPL_PLAN).
   - Input path = FEATURE_SPEC.
   - Generate/update only:
     * `plan.md` (short tech plan)
     * `.specify/memory/public/registry.yaml`
     * `.specify/memory/public/*.api.md` (minimal manifests for each module)
     * Backend HTTP **OpenAPI** at `backend/.../contracts/<feature>_openapi.(yaml|json)` (single source of truth)
   - **Backend communication rule**:
     * Same-process modules **MUST** use an **in-process public port** exported by the provider module (typed functions / DTOs).
     * **HTTP (OpenAPI)** is used only for cross-process/external consumption.
   - Frontend contracts: **none** (types/SDK are generated later from OpenAPI).

4. Validate docs-as-code gates:
   ```bash
   python .specify/scripts/registry_validate.py
   python .specify/scripts/manifest_lint.py
Completion check:

plan.md contains: module map, public surfaces table (In-process Port & HTTP), OpenAPI path, vertical steps.

registry.yaml & manifests exist; OpenAPI path present for each HTTP provider.

Report results with branch name, absolute file paths, and generated artifacts.