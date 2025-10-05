#!/bin/bash
# Rebuild frontend Docker container with updated dependencies (SWR)

echo "🔧 Rebuilding frontend Docker container..."
echo ""

# Stop frontend container
echo "1. Stopping frontend container..."
docker-compose stop frontend

# Remove old frontend container and image
echo "2. Removing old frontend container..."
docker-compose rm -f frontend

echo "3. Rebuilding frontend image with updated dependencies..."
docker-compose build --no-cache frontend

# Start frontend
echo "4. Starting frontend..."
docker-compose up -d frontend

echo ""
echo "✅ Frontend rebuilt! Checking logs..."
echo ""

# Show logs
docker-compose logs -f frontend
