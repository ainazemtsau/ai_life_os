# Backend Goals API Manifest

**Module**: `backend.goals`
**Version**: 0.1.0 (MVP)
**Kind**: Python
**Contract**: [openapi.yaml](./openapi.yaml)

## Overview
REST API for managing personal goals. Provides CRUD operations, filtering by completion status, and server-side persistence to PostgreSQL.

## Public Surface

### Endpoints
All endpoints are prefixed with `/api/goals`.

#### `GET /api/goals`
List all goals, optionally filtered by completion status.

**Query Parameters**:
- `status` (optional): `active` | `done`

**Response**: `200 OK`
```json
{
  "goals": [
    {
      "id": "uuid",
      "title": "string",
      "is_done": boolean,
      "date_created": "ISO 8601",
      "date_updated": "ISO 8601"
    }
  ]
}
```

**Sorting**: Active goals first, then by `date_updated DESC`

---

#### `POST /api/goals`
Create a new goal.

**Request Body**:
```json
{
  "title": "string (1-255 chars, non-empty)"
}
```

**Response**: `201 Created`
```json
{
  "id": "uuid (auto-generated)",
  "title": "string",
  "is_done": false,
  "date_created": "ISO 8601 (auto-generated)",
  "date_updated": "ISO 8601 (auto-generated)"
}
```

**Errors**:
- `422 Unprocessable Entity`: Empty title or title > 255 chars

---

#### `GET /api/goals/{id}`
Get a single goal by UUID.

**Response**: `200 OK` (same schema as POST response)

**Errors**:
- `404 Not Found`: Goal does not exist
- `422 Unprocessable Entity`: Invalid UUID format

---

#### `PATCH /api/goals/{id}`
Update goal title and/or completion status.

**Request Body** (at least one field required):
```json
{
  "title": "string (1-255 chars, optional)",
  "is_done": boolean (optional)
}
```

**Response**: `200 OK` (updated goal, `date_updated` refreshed)

**Errors**:
- `404 Not Found`: Goal does not exist
- `422 Unprocessable Entity`: Validation error or no fields provided

---

#### `DELETE /api/goals/{id}`
Permanently delete a goal.

**Response**: `204 No Content`

**Errors**:
- `404 Not Found`: Goal does not exist

---

## Error Handling

All error responses follow this schema:
```json
{
  "detail": "Human-readable error message",
  "type": "error_type (e.g., validation_error)",
  "status": 422
}
```

Common error messages:
- `"Title cannot be empty or whitespace-only"` (422)
- `"Title cannot exceed 255 characters"` (422)
- `"Goal not found"` (404)
- `"At least one field must be provided"` (422)

---

## Data Validation

### Title Constraints (FR-017, FR-018)
- **Minimum**: 1 character (after trim)
- **Maximum**: 255 characters
- **Enforcement**: Pydantic (API layer) + PostgreSQL CHECK constraint (DB layer)

### ID Format
- **Type**: UUID v4
- **Auto-generated**: Yes (by PostgreSQL `gen_random_uuid()`)

### Timestamps
- **Format**: ISO 8601 with timezone (e.g., `2025-10-04T14:30:00Z`)
- **Auto-generated**: `date_created` on INSERT, `date_updated` on INSERT/UPDATE

---

## Dependencies

This module has **no dependencies** on other modules (foundational feature).

## Usage from Other Modules

### Import Hint
```python
from ai_life_backend.api.goals import router as goals_router

# In main app
app.include_router(goals_router, prefix="/api")
```

### Contract Testing
Contract tests must verify:
1. Response schemas match OpenAPI spec
2. Status codes are correct
3. Error messages are user-friendly
4. Sorting order is correct (active first, then by date_updated DESC)

**Test File**: `backend/tests/contract/test_goals_api.py`

---

## Module Boundaries

### Allowed Directories
- `backend/src/ai_life_backend/domain/goal.py`
- `backend/src/ai_life_backend/repository/goal_repository.py`
- `backend/src/ai_life_backend/services/goal_service.py`
- `backend/src/ai_life_backend/api/goals.py`
- `backend/tests/contract/test_goals_api.py`
- `backend/tests/integration/test_goal_*.py`
- `backend/tests/unit/test_goal_*.py`

### Internal Implementation (Not Public)
- Repository interface (Protocol)
- Service layer methods
- Database models (SQLAlchemy)
- Migration scripts

**Do not import internal implementation details from other modules.**

---

## Performance Characteristics

- **Target Response Time**: <200ms for all endpoints
- **Expected Load**: Single user, ~10-50 goals
- **Database Indexes**: `is_done` (filtering), `date_updated` (sorting)

---

## Security

- **Input Validation**: All inputs validated via Pydantic
- **SQL Injection**: Prevented by SQLAlchemy parameterized queries
- **Authentication**: None (single-user MVP)
- **Future**: Add authentication when multi-user support is needed

---

## Versioning

**Current Version**: 0.1.0

**SemVer Policy**:
- **MAJOR**: Breaking changes to request/response schemas or endpoint paths
- **MINOR**: New endpoints or optional fields
- **PATCH**: Bug fixes, documentation updates

**Next Planned Version**: 0.2.0 (may add pagination if needed)

---

## Changelog

### 0.1.0 (2025-10-04)
- Initial release: CRUD operations, filtering by status
- Server-side persistence to PostgreSQL
- Contract-first design with OpenAPI spec
