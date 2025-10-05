# Data Model: Goals Management MVP

**Feature**: Goals Management MVP (foundation)
**Date**: 2025-10-04
**Status**: Complete

## Entity: Goal

### Overview
Represents a personal objective or task the user wants to accomplish. Goals are simple, trackable items with a title, completion status, and timestamps for creation and modification.

### Attributes

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, AUTO-GENERATED | Unique identifier, auto-generated on creation |
| `title` | String (VARCHAR 255) | NOT NULL, NON-EMPTY (trimmed), MAX 255 chars | Descriptive text of the goal |
| `is_done` | Boolean | NOT NULL, DEFAULT false | Completion status (false = active, true = done) |
| `date_created` | Timestamp (with timezone) | NOT NULL, AUTO-GENERATED | ISO 8601 timestamp when goal was created |
| `date_updated` | Timestamp (with timezone) | NOT NULL, AUTO-UPDATED | ISO 8601 timestamp of last modification |

### Validation Rules (from FR-017, FR-018)

1. **Title Non-Empty** (FR-017):
   - `title.trim().length > 0`
   - Enforced at: API layer (Pydantic), Database layer (CHECK constraint)
   - Error: `422 Unprocessable Entity` with message "Title cannot be empty or whitespace-only"

2. **Title Max Length** (FR-018):
   - `title.length <= 255`
   - Enforced at: API layer (Pydantic), Database layer (VARCHAR 255)
   - Error: `422 Unprocessable Entity` with message "Title cannot exceed 255 characters"

3. **ID Uniqueness**:
   - Auto-generated UUID ensures uniqueness
   - Enforced at: Database layer (PRIMARY KEY)

### State Transitions

```
[Created] → is_done = false
    ↓
[Active] ←→ [Done]
    ↑      ↓
    └──────┘
(toggle via PATCH /api/goals/{id})

[Active/Done] → [Deleted]
(permanent removal via DELETE /api/goals/{id})
```

**State Transition Rules**:
- Goals are created in "Active" state (`is_done = false`) by default
- Can toggle between Active ↔ Done via PATCH operation
- Title can be edited in any state
- Deletion is permanent (no soft delete for MVP)
- `date_updated` is refreshed on ANY modification (title or is_done)

### Relationships
**None** - Single entity, no foreign keys for MVP (future features may add User, Category, etc.)

---

## Domain Invariants

### Single-User Scope (FR-034)
- No `user_id` field required for MVP
- All goals belong to the single application user
- Future: Add `user_id` when multi-user support is needed

### Concurrent Modification (FR-036)
- **Strategy**: Last-write-wins
- **Behavior**: Most recent PATCH/DELETE overwrites previous state
- **No Conflict Detection**: No optimistic locking, ETags, or version fields for MVP
- **Rationale**: Single user, low collision probability; complexity not justified

### Ordering Rules (FR-012, FR-013)
Goals are sorted by:
1. **Primary**: `is_done` (false before true) → Active goals first
2. **Secondary**: `date_updated DESC` → Most recently modified first within each group

**SQL Equivalent**:
```sql
SELECT * FROM goals
ORDER BY is_done ASC, date_updated DESC;
```

---

## Database Schema

### PostgreSQL Table Definition
```sql
CREATE TABLE goals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL CHECK (LENGTH(TRIM(title)) > 0),
    is_done BOOLEAN NOT NULL DEFAULT FALSE,
    date_created TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    date_updated TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index for filtering by completion status (FR-014, FR-015)
CREATE INDEX idx_goals_is_done ON goals(is_done);

-- Index for sorting by modification date (FR-013)
CREATE INDEX idx_goals_date_updated ON goals(date_updated DESC);
```

### Index Strategy
- `idx_goals_is_done`: Supports fast filtering for active/done queries
- `idx_goals_date_updated`: Supports efficient sorting by most recent updates
- Combined with `ORDER BY is_done, date_updated DESC`, PostgreSQL query planner can optimize the sort

---

## API Data Transfer Objects (DTOs)

### GoalCreateRequest
```json
{
  "title": "string (1-255 chars, non-empty after trim)"
}
```
**Validation**: Pydantic schema enforces title constraints (FR-017, FR-018)

### GoalUpdateRequest
```json
{
  "title": "string (1-255 chars, optional)",
  "is_done": "boolean (optional)"
}
```
**Validation**: At least one field must be provided; title follows same rules as create

### GoalResponse
```json
{
  "id": "uuid",
  "title": "string",
  "is_done": "boolean",
  "date_created": "ISO 8601 timestamp",
  "date_updated": "ISO 8601 timestamp"
}
```
**Serialization**: Pydantic auto-converts datetime to ISO 8601

### GoalListResponse
```json
{
  "goals": [
    { /* GoalResponse */ },
    { /* GoalResponse */ }
  ]
}
```
**Ordering**: Pre-sorted by backend per FR-012/FR-013

---

## Repository Interface

### GoalRepository Protocol (Python)
```python
from typing import Protocol
from uuid import UUID
from .domain.goal import Goal

class GoalRepository(Protocol):
    async def create(self, title: str) -> Goal:
        """Create new goal with auto-generated id and timestamps."""
        ...

    async def get_by_id(self, goal_id: UUID) -> Goal | None:
        """Retrieve goal by id, return None if not found."""
        ...

    async def list_all(self) -> list[Goal]:
        """List all goals, sorted by (is_done ASC, date_updated DESC)."""
        ...

    async def list_by_status(self, is_done: bool) -> list[Goal]:
        """List goals filtered by completion status, sorted by date_updated DESC."""
        ...

    async def update(self, goal_id: UUID, title: str | None, is_done: bool | None) -> Goal | None:
        """Update goal fields, refresh date_updated, return None if not found."""
        ...

    async def delete(self, goal_id: UUID) -> bool:
        """Delete goal, return True if deleted, False if not found."""
        ...
```

**Design Notes**:
- Protocol defines contract (interface segregation, DIP)
- Repository implementations are swappable (e.g., PostgresGoalRepository for prod, InMemoryGoalRepository for tests)
- All methods are async (FastAPI async pattern)

---

## Domain Entity (Python)

### Goal Dataclass
```python
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class Goal:
    """Immutable domain entity representing a goal."""
    id: UUID
    title: str
    is_done: bool
    date_created: datetime
    date_updated: datetime

    def __post_init__(self) -> None:
        """Validate invariants."""
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty or whitespace-only")
        if len(self.title) > 255:
            raise ValueError("Title cannot exceed 255 characters")
```

**Design Rationale**:
- Immutable (`frozen=True`) prevents accidental mutation
- Validates invariants at construction (fail-fast)
- Pure data structure, no business logic (SRP)

---

## Frontend TypeScript Interface

### Goal Type
```typescript
// frontend/src/types/goal.ts
export interface Goal {
  id: string;           // UUID as string
  title: string;
  isDone: boolean;      // camelCase for TypeScript convention
  dateCreated: string;  // ISO 8601 string
  dateUpdated: string;  // ISO 8601 string
}

export interface GoalCreateInput {
  title: string;
}

export interface GoalUpdateInput {
  title?: string;
  isDone?: boolean;
}
```

**Naming Convention**: Backend uses `snake_case` (Python), Frontend uses `camelCase` (TypeScript). API layer handles conversion.

---

## Data Flow

### Create Goal Flow
```
[User Input: title]
  ↓ (Frontend validation: 1-255 chars, non-empty)
[POST /api/goals {"title": "..."}]
  ↓ (Pydantic validation)
[GoalService.create_goal(title)]
  ↓ (Business logic layer)
[GoalRepository.create(title)]
  ↓ (Database INSERT)
[PostgreSQL: Auto-generate id, date_created, date_updated]
  ↓ (Return Goal entity)
[API Response: GoalResponse JSON]
  ↓ (SWR cache update)
[Frontend: Display new goal]
```

### Update Goal Flow (Toggle Completion)
```
[User Action: Click checkbox]
  ↓ (Optimistic UI update)
[PATCH /api/goals/{id} {"is_done": true}]
  ↓ (Pydantic validation)
[GoalService.update_goal(id, is_done=True)]
  ↓ (Business logic layer)
[GoalRepository.update(id, is_done=True)]
  ↓ (Database UPDATE, refresh date_updated)
[PostgreSQL: UPDATE goals SET is_done=true, date_updated=NOW() WHERE id=...]
  ↓ (Return updated Goal)
[API Response: GoalResponse JSON]
  ↓ (SWR revalidates, resolves optimistic update)
[Frontend: Confirm UI state]
```

### Filter Goals Flow
```
[User Action: Select "Active" filter]
  ↓ (Frontend state update)
[GET /api/goals?status=active]
  ↓ (Query param validation)
[GoalService.list_goals(is_done=False)]
  ↓ (Business logic layer)
[GoalRepository.list_by_status(is_done=False)]
  ↓ (Database SELECT with WHERE clause)
[PostgreSQL: SELECT * FROM goals WHERE is_done=false ORDER BY date_updated DESC]
  ↓ (Return list[Goal])
[API Response: GoalListResponse JSON]
  ↓ (SWR cache update)
[Frontend: Display filtered goals]
```

---

## Edge Cases Handling

### Empty Title Submission (Edge Case #1)
- **Detection**: Pydantic validation (API layer)
- **Response**: `422 Unprocessable Entity`
- **Message**: "Title cannot be empty or whitespace-only"
- **Frontend**: Display error message, prevent submission

### Title Exceeds 255 Characters (Edge Case #3)
- **Detection**: Pydantic validation (API layer)
- **Response**: `422 Unprocessable Entity`
- **Message**: "Title cannot exceed 255 characters"
- **Frontend**: Character counter, disable submit when limit exceeded

### Concurrent Edits (Edge Case #2)
- **Strategy**: Last-write-wins (FR-036)
- **Behavior**: Second PATCH overwrites first without error
- **Frontend**: SWR revalidation shows latest state on focus/reconnect

### Filter with No Matches (Edge Case #4)
- **Response**: `200 OK` with `{"goals": []}`
- **Frontend**: Display "No goals found" message

### No Goals at All (Edge Case #5)
- **Response**: `200 OK` with `{"goals": []}`
- **Frontend**: Display empty state with "Create your first goal" prompt

### Backend Unavailable (Edge Case #6, FR-022-FR-025)
- **Detection**: SWR network error handler
- **Frontend Behavior**:
  - Display error banner: "Cannot connect to server. Please check your connection."
  - Disable all action buttons (Create, Edit, Delete)
  - Show cached goals (if any) with stale indicator
  - Auto-retry on reconnect (SWR's onReconnect)

---

## Summary

**Entities**: 1 (Goal)
**Tables**: 1 (goals)
**Indexes**: 2 (is_done, date_updated)
**DTOs**: 4 (Create, Update, Response, ListResponse)
**Repository Methods**: 6 (create, get_by_id, list_all, list_by_status, update, delete)

**Validation Layers**:
1. Frontend: Client-side validation for UX
2. API (Pydantic): Primary validation enforcement
3. Database (CHECK, NOT NULL): Defense in depth

**Design Principles Applied**:
- ✅ Single Responsibility: Goal entity has one purpose
- ✅ Dependency Inversion: Service depends on Repository protocol, not implementation
- ✅ Explicit Types: All fields typed (Python, TypeScript)
- ✅ Fail Fast: Validation at construction and API boundary
- ✅ Immutable Domain: Goal dataclass is frozen

---

**Phase 1 Status**: Data model complete - Ready for contract generation
