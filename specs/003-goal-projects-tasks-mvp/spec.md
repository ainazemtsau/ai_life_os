Feature Specification: Goals/Projects/Tasks MVP (CRUD + Dependencies)

Feature Branch: [003-goal-projects-tasks-mvp]
Created: 2025-10-07
Status: Draft
Input: Create full-featured management for Goal, Milestone, Project, Task with basic CRUD, REST API, per-entity list pages (no search, no detail pages). Dependencies: Tasks only within their Project; Projects may depend on other Projects within the same Goal; Goals have no dependencies. Single unified status set todo/doing/done/blocked (future per-entity customization allowed). Drop fields mode, daypart_pref, outcome entirely. Enums and dependencies MUST be selectable via dropdowns.

User Scenarios & Testing (mandatory)
Primary User Story

As a single workspace owner, I want list-and-form pages for Goals, Projects, Milestones, and Tasks to manually create, edit, and delete records; set statuses, priorities, and relationships; and define dependencies (Task→Task within one Project; Project→Project within one Goal) so that I can validate the models and basic UI flows without search or detail views.

Acceptance Scenarios

Given an empty system, When I create a Goal with title, priority, deadline?, status, rationale, Then the Goal is persisted and shown in the Goals list.

Given an existing Goal, When I create a Milestone linked to that Goal with title, due?, status, demo_criterion, blocking, Then the Milestone appears in the Milestones list and references the chosen Goal.

Given no Goal selection, When I create a Project as standalone (no goal_id) with title, status, priority, scope, risk, Then the Project saves and is marked standalone in the Projects list.

Given a Goal G with Projects A and B, When I set dependency B depends on A and save, Then it succeeds only if no cycle is formed; When a cycle would form, Then the operation is rejected with an explanation of the conflicting edges.

Given Project A with Tasks A1 and A2, When I set A2 depends on A1, Then it succeeds; When I attempt to depend on a Task from another Project, Then the UI does not offer it (or validation rejects it).

Given any entity, When I change status via dropdown (todo/doing/done/blocked), Then the value is saved and shown in the list.

Given a Task with dependencies, When all its blockers move to done, Then the UI reflects that no blockers remain (e.g., unblocked indicator).

Given a delete action on any entity, When I confirm deletion, Then the record is removed from the list; if dependencies exist, Then the system blocks deletion or asks to remove dependent links first.

Given Task creation/edit form, When I open dropdowns for status, size (XS/S/M/L/XL), energy (Deep/Focus/Light), continuity (chain/linked/puzzle), clarity (clear/cloudy/unknown), risk (green/yellow/red), Then I can select fixed values and save.

Given REST API endpoints, When I perform CRUD on any entity, Then success and error responses follow a structured HTTP error schema using Problem Details. 
RFC Editor

Edge Cases

Creating cyclic dependencies among Tasks or among Projects within a Goal MUST be rejected with a message identifying the cycle.

Deleting a record that others depend on MUST require confirmation and either block the action or offer to remove related dependencies first.

Setting deadline/due in the past SHOULD warn but MAY allow saving.

Standalone Project MUST NOT depend on or be depended upon by Projects of a different Goal (only intra-Goal dependencies are permitted).

Requirements (mandatory)
Functional Requirements

FR-001: The system MUST provide separate list + create/edit forms (CRUD) for Goal, Project, Milestone, Task; no search and no detail pages in this MVP.

FR-002: All entities MUST use a unified status set: todo / doing / done / blocked. Future per-entity customization MAY be introduced without breaking this MVP. (Normative keywords per BCP 14.) 

FR-003: Task.dependencies MUST reference only Tasks within the same Project; the Task dependency graph MUST be a DAG (no cycles).

FR-004: Project MAY have goal_id (standalone allowed). Goals have no dependencies between each other.

FR-005: Project→Project dependencies MUST be allowed only within the same Goal; the Project dependency graph MUST be a DAG (no cycles).

FR-006: Milestone MUST belong to a Goal only (no direct Project link).

FR-007: Enum fields MUST be implemented as dropdowns:

Goal: priority (P0–P3), status.

Project: priority (P0–P3), status, risk (green/yellow/red).

Milestone: status.

Task: status, size (XS/S/M/L/XL), energy (Deep/Focus/Light), continuity (chain/linked/puzzle), clarity (clear/cloudy/unknown), risk (green/yellow/red).

Fields mode, daypart_pref, outcome MUST NOT exist anywhere in the system.

FR-008: Forms MUST validate required fields (e.g., title, required relations) and MUST NOT accept operations that introduce dependency cycles.

FR-009: The REST API MUST expose CRUD for each entity; error responses MUST use Problem Details for HTTP APIs (type/title/status/detail/instance). 
RFC Editor

FR-010: Date/time fields (deadline, due, and audit metadata) MUST be RFC 3339 timestamps in UTC. 
RFC Editor

FR-011: Identifiers MUST be UUIDs (recommended UUIDv4) per the revised UUID specification. 

FR-012: The UI SHOULD simplify dependency selection:

Task form shows a filtered list of Tasks from the same Project (optionally filtered by status).

Project form shows Projects within the selected Goal (standalone Projects see none).

FR-013: Deleting records SHOULD require confirmation; when dependencies exist, the system MUST block deletion or present a guided removal flow first.

FR-014: Default list ordering SHOULD be created_at DESC. Additional explicit sort options MAY be introduced later.

Conventions & Formats (include if data/APIs involved)

Identifiers: UUIDs (recommend UUIDv4) as defined by the updated UUID RFC (successor to RFC 4122). 

Timestamps: RFC 3339 (UTC, Z or explicit offset). 
RFC Editor

API Errors: Structured Problem Details (RFC 7807). Notes: later updates like RFC 9457 exist, but this MVP SHOULD adhere to RFC 7807 baseline. 

Normative Language: MUST/SHOULD/MAY per BCP 14 (RFC 2119; clarified by RFC 8174 to apply only in UPPERCASE). 

Key Entities (include if feature involves data)

Goal — Desired outcome owned by owner=self. Attributes: id, title, priority (P0–P3), deadline?, status, rationale. Relations: milestones[] (1..N), projects[] (0..N; includes Projects linked to this Goal).

Milestone — Verifiable step toward a Goal. Attributes: id, goal_id, title, due?, status, demo_criterion, blocking (bool). Relation: belongs to one Goal.

Project — Work container (may be standalone). Attributes: id, goal_id?, title, status, priority, scope (summary), risk (green/yellow/red), work_items[] (Tasks), tags[]. Relations: optional link to a Goal; may depend on other Projects within the same Goal (DAG).

Task — Smallest planning unit. Attributes: id, project_id, title, status, dependencies[] (Tasks in same Project only), size (XS/S/M/L/XL), energy (Deep/Focus/Light), continuity (chain/linked/puzzle), clarity (clear/cloudy/unknown), risk (green/yellow/red), context. Relations: belongs to one Project; Task graph is a DAG.

Clarifications

Q1 → A: Milestone has no direct link to Project; both attach to Goal.

Q2 → A: Unified statuses todo/doing/done/blocked for all entities; MAY be customized per-entity later.

Q3 → A (+rule): Task dependencies only within the same Project; Task graph is a DAG. Projects may be standalone; Projects within the same Goal MAY depend on each other; Goals have no dependencies.

Q4 → A (amended): Use dropdowns for enums; exclude mode, daypart_pref, outcome from the system entirely.

Q5 → A: Project→Project dependencies within a Goal form a DAG (no cycles).

Review & Acceptance Checklist

Content Quality

 No implementation details (languages, frameworks, file paths)

 Focused on user value and verifiable behaviors

 All mandatory sections completed; clean grammar and bullets

Requirement Completeness

 No unresolved [NEEDS CLARIFICATION] markers

 Requirements are testable and unambiguous

 Scope is clearly bounded (CRUD lists only; no search; no detail views)

 Dependencies and assumptions identified (DAGs for Tasks and Projects)

 Acceptance scenarios sequentially numbered; variants use dotted form

 ID, timestamp, and error formats specified (UUID / RFC 3339 / RFC 7807). 

House Style References

Apply Clean Code, SOLID, KISS/YAGNI principles when shaping requirements and tests (editorial baseline).