# PostgreSQL "role does not exist" Fix

## Problem

You're seeing this error:
```
FATAL: role "postgres" does not exist
```

This happens because the PostgreSQL Docker volume was initialized without proper environment variables.

## Solution

You need to **completely reset** the database volume. This will delete all existing data.

### Option 1: Automated Fix (Recommended)

Run the fix script:

```bash
./fix-database.sh
```

This script will:
1. Stop all containers
2. Remove the corrupted database volume
3. Restart database with correct initialization
4. Run migrations
5. Start all services

### Option 2: Manual Fix

If you prefer to do it manually:

**Step 1: Stop everything**
```bash
docker-compose down
```

**Step 2: Remove the database volume**
```bash
docker volume rm ai_life_os_db_data
```

**Step 3: Start just the database**
```bash
docker-compose up -d db
```

**Step 4: Wait for database to initialize**
```bash
# Wait about 10 seconds, then check:
docker-compose logs db
# You should see "database system is ready to accept connections"
```

**Step 5: Run migrations**
```bash
cd backend
uv run alembic upgrade head
cd ..
```

**Step 6: Start all services**
```bash
docker-compose up -d
```

## Verification

After the fix, verify everything works:

**1. Check database connection:**
```bash
docker-compose exec db psql -U postgres -d ai_life_os -c "SELECT version();"
```

Should show PostgreSQL version without errors.

**2. Check tables exist:**
```bash
docker-compose exec db psql -U postgres -d ai_life_os -c "\dt"
```

Should show the `goals` table.

**3. Check backend API:**
```bash
curl http://localhost:8000/health
```

Should return: `{"status":"ok"}`

**4. Check frontend:**

Visit http://localhost:3000 - should show Goals UI.

## Why This Happened

The database volume was created before the `.env` file was properly configured, or the environment variables weren't passed correctly during the first initialization. PostgreSQL only reads `POSTGRES_USER` during the **first** initialization of the data directory.

Once initialized, changing `.env` doesn't help - you must delete the volume and re-initialize.

## Prevention

To avoid this in future:
1. Always ensure `.env` exists and is correct **before** first `docker-compose up`
2. If changing database credentials, always remove the volume first
3. Use `docker-compose down -v` to remove volumes when doing a full reset

## Data Loss Warning

⚠️ **This fix deletes all data in the database!**

If you have important data:
1. Export it first: `docker-compose exec db pg_dump -U postgres ai_life_os > backup.sql`
2. After fix, restore: `cat backup.sql | docker-compose exec -T db psql -U postgres ai_life_os`

For MVP development, there's no data to lose, so it's safe to proceed.
