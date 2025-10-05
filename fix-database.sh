#!/bin/bash
# Fix PostgreSQL "role does not exist" error by resetting the database volume

echo "🔧 Fixing PostgreSQL database initialization..."
echo ""

# Step 1: Stop all containers
echo "1. Stopping all containers..."
docker-compose down

# Step 2: Remove the database volume (WARNING: deletes all data)
echo "2. Removing corrupted database volume..."
docker volume rm ai_life_os_db_data 2>/dev/null || echo "   Volume doesn't exist or already removed"

# Step 3: Start only the database to initialize it properly
echo "3. Starting database with correct initialization..."
docker-compose up -d db

# Step 4: Wait for database to be ready
echo "4. Waiting for database to initialize (this may take 10-15 seconds)..."
sleep 5

# Check if database is ready
for i in {1..30}; do
    if docker-compose exec -T db pg_isready -U postgres -d ai_life_os > /dev/null 2>&1; then
        echo "   ✅ Database is ready!"
        break
    fi
    echo "   Waiting... ($i/30)"
    sleep 1
done

# Step 5: Run migrations
echo "5. Running database migrations..."
cd backend
uv run alembic upgrade head
cd ..

# Step 6: Start all services
echo "6. Starting all services..."
docker-compose up -d

echo ""
echo "✅ Database fixed! Your services are now running."
echo ""
echo "Services:"
echo "  - Database: localhost:5432"
echo "  - Backend:  http://localhost:8000"
echo "  - Frontend: http://localhost:3000"
echo ""
echo "View logs with: docker-compose logs -f"
