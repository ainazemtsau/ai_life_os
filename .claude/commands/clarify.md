---
description: Drive a short clarification round to remove ambiguities before /plan.
---

User input:

$ARGUMENTS

Goal: produce a concise Q&A so requirements are testable and unambiguous, without heavy interactive loops.

Steps:

1) Run `.specify/scripts/bash/setup-plan.sh --json` to get FEATURE_SPEC, SPECS_DIR, BRANCH.

2) Scan FEATURE_SPEC for ambiguity hotspots (brief pass):
   - vague adjectives; missing limits; undefined terms; edge cases
   - non-functional targets (performance/reliability/security) stated without metrics
   Use RFC 2119 wording (MUST/SHOULD/MAY) and INVEST for story quality.

3) Create or update `<SPECS_DIR>/clarifications.md` using `.specify/templates/clarify-template.md`.
   Fill sections: Context (1–3 bullets), Q&A (each answer dated), Open Items.

4) If technical uncertainty is detected (trade-offs, scale-out, refactor signals), **suggest**:
   - `/design-spike "<topic>" timebox=1d`
   - then `/adr "<decision title>" status=Proposed`
   (Don’t create them here; only suggest.)

5) Write `clarifications.md` and print:
   - absolute path, number of OPEN items,
   - recommendation to proceed to `/plan` only if OPEN == 0 or user overrides.

Behavior:
- Keep it short; no more than ~10 Q&A bullets per run.
- Do NOT rewrite the spec file here; keep clarifications isolated.
- Prefer measurable language (RFC 2119). Use spikes/ADRs for design choices.
