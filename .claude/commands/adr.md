---
description: Create an Architecture Decision Record (ADR) to capture a significant decision with context and consequences.
---

The user input to you can be provided directly by the agent or as a command argument — you MUST consider it before proceeding.

User input:

$ARGUMENTS

Rules:
- One ADR per significant decision (format popularized by Michael Nygard).
- Status MUST be one of: Proposed | Accepted | Rejected | Superseded by ADR-XXXX.

Steps:

1) Determine context via `.specify/scripts/bash/setup-plan.sh --json` to get FEATURE_SPEC, SPECS_DIR, BRANCH.

2) Parse arguments:
   - TITLE: from $ARGUMENTS (required), e.g., "Adopt hexagonal port for Chatbot + Registry/Router"
   - STATUS: optional (default "Proposed"). Accept: Proposed|Accepted|Rejected|Superseded by ADR-XXXX
   - LINKS: optional comma-separated references (e.g., spike path, benchmarks)
   - OWNER: optional owner(s)

3) Create ADR file:
   - Directory: `<SPECS_DIR>/decisions/`
   - Filename: `ADR-<YYYYMMDD>-<slug-of-title>.md` (do NOT overwrite existing).
   - Content: render `.specify/templates/adr-template.md`
     Replace placeholders: [TITLE], [STATUS], [DATE], [CONTEXT], [DECISION], [CONSEQUENCES], [ALTERNATIVES], [COMPATIBILITY], [OPERATIONS], [SECURITY], [OWNERS], [LINKS]

4) Output absolute path and brief reminder to reflect ADR in /plan and /tasks.

References:
- ADR: a short record of a significant decision with context and consequences.
