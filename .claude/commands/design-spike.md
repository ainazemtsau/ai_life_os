---
description: Create a time-boxed Design Spike to de-risk uncertain work before implementation.
---

The user input to you can be provided directly by the agent or as a command argument — you MUST consider it before proceeding.

User input:

$ARGUMENTS

Goal: capture a short, throwaway experiment to answer a question (reduce uncertainty), then summarize findings and a recommendation.

Steps:

1) Determine context:
   - FEATURE: from `.specify/scripts/bash/setup-plan.sh --json` (parse FEATURE_SPEC, SPECS_DIR, BRANCH).
   - TITLE: taken from `$ARGUMENTS` (e.g., "Chatbot capability & routing model"). If empty → ERROR "Missing spike title".
   - TIMEBOX: default 1–2 days unless explicitly set via `timebox=<hours|days>` in $ARGUMENTS.

2) Create a spike folder:
   - Path: `<SPECS_DIR>/spikes/<slug-of-title>/`
   - Files:
     * `spike.md` rendered from `.specify/templates/design-spike-template.md`
       Replace placeholders:
       - [TITLE], [TIMEBOX], [CONTEXT], [QUESTIONS], [OPTIONS], [EXPERIMENTS], [FINDINGS], [RECOMMENDATION], [NEXT_STEPS], [SUCCESS_CRITERIA]

3) If $ARGUMENTS includes `experiments=` or `options=`, embed them into the template sections.

4) Output:
   - Print absolute path to the new spike.
   - Remind: "Spikes are throwaway deliverables — merge the learnings, not the code."

References:
- Spikes are time-boxed research used in Scrum/XP/SAFe to reduce risk before committing to a solution. 
