---
description: Execute the planning workflow with a logic-less template; inject modules from registry.yaml.
---

User input:

$ARGUMENTS

Steps:

1) Run `.specify/scripts/bash/setup-plan.sh --json` → parse { FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH }.

2) Ensure FEATURE_SPEC has a Clarifications section or user override.

3) Read:
   - FEATURE_SPEC (requirements/acceptance)
   - `.specify/memory/constitution.md`
   - `.specify/memory/public/registry.yaml`  ← single source of module truth
4) Heuristics: Suggest design-spikes/ADRs when signals appear in FEATURE_SPEC or $ARGUMENTS:
   - Scaling a concept to N>1 (e.g., multiple bots/providers/groups); need ports/registries/routers
   - New cross-module consumers; need a public surface (in-process port or HTTP contract)
   - Refactor for extensibility (strangler approach)
   - Significant library/pattern/algorithm choice with trade-offs
   - Performance/SLO/security concerns impacting design

   If any signal is found, append a "Recommendations" section to IMPL_PLAN with concrete commands to run, e.g.:
   - `/design-spike "Chatbot capability & routing model" timebox=2d`
   - `/adr "Adopt ChatbotService port + Router" status=Proposed`

(Do not create files here; only suggest. Keep the template logic-less.)
...
(Optional) If you use a logic-less plan-template.md, add placeholders where suggestions should appear:

[SPIKE_RECOMMENDATIONS]

[ADR_RECOMMENDATIONS]


5) Build data for template placeholders:
   - MODULE_API_MATRIX: iterate registry modules; include id/kind/provides/uses/manifest/contract/allowed_dirs/import_hint/semver.
   - HTTP_CONTRACTS_TABLE: subset where `contract` points to OpenAPI file.
   - INPROC_PORTS_TABLE: subset with in-process import_hint (no HTTP).
   - CONTEXT_SUMMARY, VERTICAL_STEPS, NOTES: derive from spec + $ARGUMENTS.

6) Render `.specify/templates/plan-template.md` into IMPL_PLAN by replacing placeholders:
   [CONTEXT_SUMMARY], [MODULE_API_MATRIX], [HTTP_CONTRACTS_TABLE], [INPROC_PORTS_TABLE],
   [VERTICAL_STEPS], [NOTES], [SPEC_PATH], [FEATURE_SPEC_ABS], [BRANCH], [DATE].

7) Validate docs gates:
   `python .specify/scripts/registry_validate.py`
   `python .specify/scripts/manifest_lint.py`
   (fail fast on errors)

8) Report: branch, IMPL_PLAN path, generated sections. Use absolute paths.
