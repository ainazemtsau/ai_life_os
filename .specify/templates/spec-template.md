# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`  
**Created**: [DATE]  
**Status**: Draft  
**Input**: User description: "$ARGUMENTS"

## Execution Flow (main)
Parse user description from Input
→ If empty: ERROR "No feature description provided"

Extract key concepts from description
→ Identify: actors, actions, data, constraints

For each unclear aspect:
→ Mark with [NEEDS CLARIFICATION: specific question]

Fill User Scenarios & Testing section
→ If no clear user flow: ERROR "Cannot determine user scenarios"

Generate Functional Requirements
→ Use normative wording (MUST / SHOULD / MAY)

Identify Key Entities (if data involved)

Normalize the document
→ Remove stray control/garbled characters
→ Ensure Acceptance Scenarios are numbered 1..N (sub-cases: 2.1, 2.2)

Run Review Checklist
→ If any [NEEDS CLARIFICATION]: WARN "Spec has uncertainties"
→ If implementation details found: ERROR "Remove tech details"

Return: SUCCESS (spec ready for planning)

markdown
Копировать код

---

## ⚡ Quick Guidelines
- ✅ Focus on **WHAT** users need and **WHY**
- ❌ Avoid **HOW** to implement (no tech stack, APIs, code structure)
- 👥 Written for business stakeholders, not developers
- 🧭 Use **clear, testable** language (MUST / SHOULD / MAY)

### Section Requirements
- **Mandatory sections**: Must be completed for every feature
- **Optional sections**: Include only when relevant to the feature
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation
When creating this spec from a user prompt:
1. **Mark ambiguities** with `[NEEDS CLARIFICATION: ...]`
2. **Don't guess** missing policies; propose a short recommended default **inside** the clarification (e.g., “recommended UUIDv4”)
3. **Think like a tester**: each requirement must be **verifiable**
4. Common underspecified areas:
   - User types and permissions
   - Data retention/deletion policies
   - Performance targets and scale
   - Error handling behaviors
   - Integration requirements
   - Security/compliance needs
   - **Data formats (IDs, timestamps), sorting field/order**

---

## User Scenarios & Testing *(mandatory)*

### Primary User Story
[Describe the main user journey in plain language]

### Acceptance Scenarios
1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]
2.1 **Given** [variant setup], **When** [action], **Then** [expected outcome]  
> Use **sequential numbering**. For variants use dotted numbering (`2.1`, `2.2`). Use “Given / When / Then” phrases.

### Edge Cases
- What happens when [boundary condition]?
- How does the system handle [error scenario]?
- What happens when no records match a filter?

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: System **MUST** [specific capability, e.g., "allow users to create items"]
- **FR-002**: System **MUST** [validation, e.g., "reject empty titles"]
- **FR-003**: Users **MUST** be able to [key interaction]
- **FR-004**: System **MUST** [persistence or behavior]
- **FR-005**: System **SHOULD** [non-critical but desired behavior]

*Unclear examples (keep as clarifications, not guesses):*
- **FR-0XX**: System **MUST** authenticate users via [NEEDS CLARIFICATION: method not specified]
- **FR-0XY**: System **MUST** retain data for [NEEDS CLARIFICATION: retention period not specified]

### Conventions & Formats *(include if data/APIs involved)*
- **Identifiers:** [NEEDS CLARIFICATION: preferred `UUIDv4`?]  
- **Timestamps:** [NEEDS CLARIFICATION: preferred `RFC 3339` in UTC?]  
- **Sorting (if applicable):** [NEEDS CLARIFICATION: specify field + order, e.g., `date_updated DESC` within groups]  
- **API error format (if HTTP):** [NEEDS CLARIFICATION: use structured “Problem Details” per RFC 7807?]

### Key Entities *(include if feature involves data)*
- **[Entity 1]**: [What it represents, key attributes (no implementation details)]
- **[Entity 2]**: [What it represents, relationships to other entities]

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Content Quality
- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed
- [ ] **No stray characters; grammar and bullets normalized**

### Requirement Completeness
- [ ] No `[NEEDS CLARIFICATION]` markers remain (or they are justified for handoff)
- [ ] Requirements are **testable and unambiguous**  
- [ ] Success criteria are **measurable**
- [ ] Scope is clearly bounded
- [ ] Dependencies and assumptions identified
- [ ] **Acceptance scenarios numbered 1..N; sub-cases 2.1, 2.2**
- [ ] **If data/APIs present:** ID format, timestamp format, and (if used) sorting **field+order** are specified or explicitly marked as `[NEEDS CLARIFICATION]`

---

## Execution Status
*Updated by main() during processing*

- [ ] User description parsed
- [ ] Key concepts extracted
- [ ] Ambiguities marked
- [ ] User scenarios defined
- [ ] Requirements generated
- [ ] Entities identified
- [ ] Review checklist passed