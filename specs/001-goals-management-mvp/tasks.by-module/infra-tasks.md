# Module Tasks: infra for Feature 001-goals-management-mvp

**Inputs**:
- Global constitution: `.specify/memory/constitution.md`
- Global tasks file: `specs/001-goals-management-mvp/tasks.md`
- Design docs: `plan.md`, `research.md`

**Scope**:
- Infrastructure and cross-cutting setup tasks
- Repository root configuration files
- No code module - these are prerequisite tasks

---

## Execution Flow (infra)

Infrastructure tasks are **prerequisites** for all module work. They set up:
1. Database services (PostgreSQL via Docker Compose)
2. Cross-cutting middleware (CORS configuration)

These tasks modify root-level configuration files and app-level settings, not module-specific code.

---

## Phase A: Infrastructure Setup

### MT001 [P] Configure PostgreSQL service in docker-compose.yml

**Description**: Add PostgreSQL 15-alpine service to docker-compose.yml for backend data persistence.

**File**: `docker-compose.yml` (repository root)

**Dependencies**: None (can run first)

**Detailed Steps**:
1. Open or create `docker-compose.yml` at repository root
2. Add PostgreSQL service configuration:
   ```yaml
   version: '3.8'

   services:
     postgres:
       image: postgres:15-alpine
       container_name: ai_life_os_postgres
       environment:
         POSTGRES_DB: ai_life_os
         POSTGRES_USER: postgres
         POSTGRES_PASSWORD: postgres
       ports:
         - "5432:5432"
       volumes:
         - postgres_data:/var/lib/postgresql/data
       healthcheck:
         test: ["CMD-SHELL", "pg_isready -U postgres"]
         interval: 10s
         timeout: 5s
         retries: 5

   volumes:
     postgres_data:
   ```

**Acceptance Criteria**:
- [ ] `docker-compose.yml` exists at repository root
- [ ] PostgreSQL service defined with image `postgres:15-alpine`
- [ ] Environment variables set: POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
- [ ] Port 5432 exposed to localhost
- [ ] Volume `postgres_data` configured for persistence
- [ ] Healthcheck configured

**Validation**:
```bash
docker-compose up -d postgres
docker-compose ps | grep postgres | grep "Up"
docker-compose exec postgres psql -U postgres -c "SELECT version();"
```

**Rollback**: `docker-compose down -v` (removes containers and volumes)

---

### MT002 Configure backend environment variables

**Description**: Create `.env` file for backend configuration (database URL, API settings).

**File**: `backend/.env` (git-ignored)

**Dependencies**: MT001

**Detailed Steps**:
1. Create `backend/.env` file (ensure it's in `.gitignore`)
2. Add environment variables:
   ```env
   # Database
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/ai_life_os
   DATABASE_ECHO=false

   # API
   API_HOST=0.0.0.0
   API_PORT=8000
   API_RELOAD=true

   # CORS
   CORS_ORIGINS=["http://localhost:3000"]
   ```

**Acceptance Criteria**:
- [ ] `backend/.env` file created
- [ ] DATABASE_URL points to PostgreSQL from MT001
- [ ] API_HOST, API_PORT configured
- [ ] CORS_ORIGINS includes frontend dev URL
- [ ] File is in `.gitignore`

**Validation**:
```bash
grep "backend/.env" backend/.gitignore || echo "backend/.env" >> backend/.gitignore
cat backend/.env | grep DATABASE_URL
```

---

### MT003 Configure frontend environment variables

**Description**: Create `.env.local` file for frontend configuration (API URL).

**File**: `frontend/.env.local` (git-ignored)

**Dependencies**: None

**Detailed Steps**:
1. Create `frontend/.env.local` file (ensure it's in `.gitignore`)
2. Add environment variables:
   ```env
   # Backend API URL
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

**Acceptance Criteria**:
- [ ] `frontend/.env.local` file created
- [ ] NEXT_PUBLIC_API_URL points to backend API (port 8000)
- [ ] File is in `.gitignore`

**Validation**:
```bash
grep ".env.local" frontend/.gitignore || echo ".env.local" >> frontend/.gitignore
cat frontend/.env.local | grep NEXT_PUBLIC_API_URL
```

---

## Phase B: Cross-Cutting Configuration

### MT010 Configure CORS in FastAPI main app

**Description**: Add CORS middleware to FastAPI app to allow frontend requests.

**File**: `backend/src/ai_life_backend/app.py`

**Dependencies**: Backend app structure must exist (will be created by backend.goals module)

**Detailed Steps**:
1. Open `backend/src/ai_life_backend/app.py`
2. Import CORS middleware:
   ```python
   from fastapi import FastAPI
   from fastapi.middleware.cors import CORSMiddleware
   import os
   ```
3. Create FastAPI app instance
4. Add CORS middleware:
   ```python
   app = FastAPI(
       title="AI Life OS API",
       description="Goals Management MVP",
       version="0.1.0"
   )

   # CORS configuration
   origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

   app.add_middleware(
       CORSMiddleware,
       allow_origins=origins,
       allow_credentials=True,
       allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
       allow_headers=["Content-Type", "Authorization"],
   )
   ```

**Acceptance Criteria**:
- [ ] CORS middleware imported and configured
- [ ] Allowed origins read from environment variable (defaults to localhost:3000)
- [ ] Methods: GET, POST, PATCH, DELETE, OPTIONS
- [ ] Headers: Content-Type, Authorization
- [ ] allow_credentials=True

**Validation**:
```bash
cd backend && uv run uvicorn ai_life_backend.app:app --reload &
sleep 2
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     http://localhost:8000/api/goals
# Should return CORS headers
```

**Note**: This task creates the skeleton of `app.py`. The goals router will be added by backend.goals module (task T050).

---

## Dependencies

```
MT001 (PostgreSQL) → MT002 (Backend .env)
                  ↓
                  MT003 (Frontend .env) [parallel to MT002]
                  ↓
                  MT010 (CORS) - depends on backend app structure
```

## Parallel Execution

**Can run in parallel**:
- MT001 + MT003 (different files, no dependencies)
- MT002 + MT003 (different files, MT002 depends on MT001)

**Sequential**:
- MT010 must run after backend app structure exists (created by backend.goals module setup)

---

## Validation Checklist

After completing infra tasks:
- [ ] Docker Compose PostgreSQL service running
- [ ] `docker-compose ps` shows postgres as "Up"
- [ ] Can connect to PostgreSQL: `psql postgresql://postgres:postgres@localhost:5432/ai_life_os`
- [ ] Backend `.env` file exists with DATABASE_URL
- [ ] Frontend `.env.local` file exists with NEXT_PUBLIC_API_URL
- [ ] CORS configured in FastAPI app (verify with OPTIONS request)

---

<!-- FANOUT:BEGIN -->
## Global Items (source)

*Do not edit this block manually; run `/fanout-tasks` to refresh.*

- [ ] T001 @module(infra) @prio(P1) Configure PostgreSQL service in docker-compose.yml
- [ ] T052 @module(infra) @prio(P2) Configure CORS for frontend-backend communication
<!-- FANOUT:END -->
