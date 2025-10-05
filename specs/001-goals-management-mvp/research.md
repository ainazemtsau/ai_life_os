# Research: Goals Management MVP

**Feature**: Goals Management MVP (foundation)
**Date**: 2025-10-04
**Status**: Complete

## Research Tasks Completed

### 1. Backend Framework: FastAPI
**Decision**: Use FastAPI for REST API implementation
**Rationale**:
- Modern async Python framework with excellent performance
- Built-in OpenAPI/Swagger documentation generation (critical for contract-first development)
- Native Pydantic integration for data validation and serialization
- Type hints support aligns with constitution's strict typing requirements
- Widely adopted, stable ecosystem

**Alternatives Considered**:
- Flask: Lacks built-in async support and OpenAPI generation
- Django REST Framework: Too heavyweight for MVP, enforces Django ORM
- Starlette (bare): Missing higher-level features FastAPI provides

**Implementation Notes**:
- Will use Pydantic v2 for schemas/validation (included with FastAPI)
- Async/await for all handlers
- Automatic OpenAPI spec generation for contract testing

---

### 2. Database: PostgreSQL with SQLAlchemy
**Decision**: PostgreSQL 15+ with SQLAlchemy 2.0 (async)
**Rationale**:
- PostgreSQL provides ACID guarantees for data integrity
- Mature, production-ready with excellent Python support
- Supports JSON columns if future features need semi-structured data
- SQLAlchemy 2.0 async support aligns with FastAPI async design
- Docker Compose makes local development simple

**Alternatives Considered**:
- SQLite: Insufficient for server-side persistence, no concurrent write support
- MongoDB: Overkill for simple relational data (Goal entity)
- Raw SQL: Violates DRY principle, harder to maintain type safety

**Implementation Notes**:
- Use Alembic for migrations (included with SQLAlchemy)
- Repository pattern isolates database logic from business logic
- Connection pooling via asyncpg driver

---

### 3. Frontend State Management: React State + SWR
**Decision**: React built-in state (useState/useReducer) + SWR for server state
**Rationale**:
- SWR provides automatic caching, revalidation, and error handling
- Optimistic UI updates for better UX
- Minimal bundle size, aligns with KISS principle
- No need for Redux/MobX complexity for simple CRUD operations
- Built by Vercel (Next.js creators), excellent Next.js integration

**Alternatives Considered**:
- Redux Toolkit: Too heavyweight for MVP, adds unnecessary complexity
- TanStack Query: Feature parity with SWR but larger bundle
- Zustand: Adds client state management when server state is primary concern

**Implementation Notes**:
- SWR for fetching/mutating goals
- Local React state for UI-only concerns (filter selection, form inputs)
- Automatic revalidation on focus/reconnect

---

### 4. API Design Pattern: RESTful
**Decision**: RESTful API following OpenAPI 3.1 specification
**Rationale**:
- REST is simple, well-understood, and sufficient for CRUD operations
- OpenAPI contracts enable contract testing and documentation
- FastAPI auto-generates OpenAPI spec from code
- Aligns with constitution's contract-first requirement

**Endpoints Design**:
```
GET    /api/goals           - List all goals (with optional ?status=active|done filter)
POST   /api/goals           - Create new goal
GET    /api/goals/{id}      - Get single goal
PATCH  /api/goals/{id}      - Update goal (title or is_done)
DELETE /api/goals/{id}      - Delete goal
```

**Alternatives Considered**:
- GraphQL: Overkill for simple CRUD, adds complexity
- gRPC: Not web-browser friendly, requires code generation
- JSON-RPC: Less standard, harder to document

**Implementation Notes**:
- Use HTTP status codes correctly (200, 201, 404, 422)
- Pydantic schemas for request/response validation
- ISO 8601 timestamps (automatic via Pydantic)

---

### 5. Testing Strategy
**Decision**: Three-tier testing (contract → integration → unit) following TDD
**Rationale**:
- Contract tests verify API spec compliance
- Integration tests validate database + service layer
- Unit tests for domain logic (if any pure functions emerge)
- Aligns with constitution's TDD and Clean Code requirements

**Backend Testing Stack**:
- pytest + pytest-asyncio for async tests
- httpx for API client testing
- pytest fixtures for database setup/teardown
- Contract tests will use generated OpenAPI spec

**Frontend Testing Stack** (future):
- Will use Vitest + React Testing Library when implementation begins
- For MVP, focus on backend contract compliance

---

### 6. Database Schema Design
**Decision**: Single `goals` table with optimized indexing
**Schema**:
```sql
CREATE TABLE goals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL CHECK (LENGTH(TRIM(title)) > 0),
    is_done BOOLEAN NOT NULL DEFAULT FALSE,
    date_created TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    date_updated TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_goals_is_done ON goals(is_done);
CREATE INDEX idx_goals_date_updated ON goals(date_updated DESC);
```

**Rationale**:
- UUID for globally unique IDs (better for distributed systems later)
- VARCHAR(255) matches spec requirement
- CHECK constraint enforces non-empty title at DB level
- TIMESTAMPTZ for proper timezone handling
- Indexes on is_done (filtering) and date_updated (sorting)

---

### 7. Error Handling Strategy
**Decision**: Structured error responses with RFC 7807 Problem Details
**Rationale**:
- Standardized error format improves client error handling
- FastAPI supports this via HTTPException
- Clear error messages meet FR-019 requirement

**Error Response Format**:
```json
{
  "detail": "Title cannot be empty or whitespace-only",
  "type": "validation_error",
  "status": 422
}
```

---

### 8. Module Boundaries & Public API Registry
**Decision**: Define two modules in registry.yaml
**Modules**:
1. `backend.goals` - Goals REST API
2. `frontend.goals` - Goals UI components

**Registry Entries** (to be created in Phase 1):
```yaml
backend.goals:
  kind: python
  semver: "0.1.0"
  manifest: "specs/001-goals-management-mvp/contracts/backend.goals.api.md"
  contract: "specs/001-goals-management-mvp/contracts/openapi.yaml"
  import_hint: "from ai_life_backend.api.goals import router"
  allowed_dirs:
    - "backend/src/ai_life_backend/domain/goal.py"
    - "backend/src/ai_life_backend/repository/goal_repository.py"
    - "backend/src/ai_life_backend/services/goal_service.py"
    - "backend/src/ai_life_backend/api/goals.py"
    - "backend/tests/contract/test_goals_api.py"
  uses: []

frontend.goals:
  kind: typescript
  semver: "0.1.0"
  manifest: "specs/001-goals-management-mvp/contracts/frontend.goals.api.md"
  contract: "specs/001-goals-management-mvp/contracts/goals.d.ts"
  import_hint: "import { GoalList, GoalForm } from '@/components/goals'"
  allowed_dirs:
    - "frontend/src/components/goals/**"
    - "frontend/src/lib/api/goals.ts"
    - "frontend/src/types/goal.ts"
  uses: ["backend.goals"]
```

---

## Dependencies to Add

### Backend (via uv)
```bash
uv add fastapi uvicorn[standard] sqlalchemy[asyncio] asyncpg alembic pydantic-settings
```

### Frontend (via pnpm)
```bash
pnpm add swr
```

---

## Configuration Requirements

### Environment Variables (.env)
```env
# Backend
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/ai_life_os
DATABASE_ECHO=false
API_HOST=0.0.0.0
API_PORT=8000

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Docker Compose Updates
Add PostgreSQL service:
```yaml
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ai_life_os
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## Performance Considerations

### Backend
- Connection pooling: 10 min, 20 max connections (SQLAlchemy defaults)
- Query optimization: Use indexes on is_done and date_updated
- Response time target: <50ms for simple queries (well under 200ms requirement)

### Frontend
- SWR caching reduces redundant API calls
- Optimistic updates for instant UI feedback
- Debounce filter changes (300ms) to prevent excessive requests

---

## Security Considerations

### Input Validation
- Pydantic validates title length (≤255) and non-empty at API layer
- PostgreSQL CHECK constraint as secondary defense
- SQL injection prevented by SQLAlchemy parameterized queries

### Data Protection
- PostgreSQL connection over localhost for MVP (no external exposure)
- Future: TLS for database connections, API authentication

---

## No Remaining Clarifications
All NEEDS CLARIFICATION items from Technical Context have been resolved:
- ✅ Language/Version: Python 3.11, TypeScript 5
- ✅ Dependencies: FastAPI, SQLAlchemy, PostgreSQL, SWR
- ✅ Storage: PostgreSQL
- ✅ Testing: pytest, mypy, ruff (backend); ESLint, TypeScript (frontend)
- ✅ Platform: Web (Linux + browsers)
- ✅ Performance: <200ms API, <100ms UI
- ✅ Constraints: Single-user, last-write-wins, 255 char limit
- ✅ Scale: 1 user, ~10-50 goals

---

**Research Status**: ✅ COMPLETE - Ready for Phase 1 (Design & Contracts)
