---
description: Create or update the feature specification from a natural language feature description (LEAN + unambiguous).
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

The text the user typed after `/specify` in the triggering message **is** the feature description. Assume you always have it available in this conversation even if `$ARGUMENTS` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that feature description, do this:

1. Run the script `.specify/scripts/bash/create-new-feature.sh --json "$ARGUMENTS"` from repo root and parse its JSON output for **BRANCH_NAME** and **SPEC_FILE**. All file paths must be absolute.  
   **IMPORTANT:** You must run this script **once**. Reuse its JSON to locate and write the spec.

2. Load `.specify/templates/spec-template.md` to understand required sections.

3. Produce the spec content for **SPEC_FILE** using the template, preserving section order and headings. While writing, enforce these **micro-rules**:
   - **No control/garbled glyphs:** replace stray characters, normalize bullets and quotes.
   - **Acceptance scenarios:** use **sequential numbering 1..N**; for variants use dotted form `2.1`, `2.2`. (No duplicate “2.”, no “2a”.)
   - **Normative wording:** use **MUST / SHOULD / MAY** consistently for requirements.
   - **If data is involved:** add a short **“Conventions & Formats”** block in the spec (see template) and:
     - If **identifier format** not specified → add a line with `[NEEDS CLARIFICATION: recommended UUIDv4]`.
     - If **timestamps** not specified → add a line with `[NEEDS CLARIFICATION: recommended RFC 3339 (UTC)]`.
     - If **sorting** is mentioned without field/order → add `[NEEDS CLARIFICATION: specify field + order e.g. date_updated DESC]`.
   - **If HTTP API is implied:** add a line under “Conventions & Formats” → `[NEEDS CLARIFICATION: use structured error format; recommended RFC 7807 Problem Details]`.

4. Write the final content to **SPEC_FILE**.

5. Report completion with branch name, spec file path, and readiness for the next phase.
