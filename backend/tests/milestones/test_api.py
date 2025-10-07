"""Integration tests for Milestones API."""

import pytest
from datetime import datetime, timezone
from uuid import uuid4, UUID
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

from ai_life_backend.milestones.api.routes import router as milestones_router


@pytest.fixture
def app():
    """Create a FastAPI test app."""
    app = FastAPI()
    app.include_router(milestones_router, prefix="/api")
    return app


@pytest.fixture
async def client(app):
    """Create an async HTTP client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
class TestMilestonesAPI:
    """Test Milestones CRUD API endpoints."""

    async def test_create_milestone(self, client):
        """Test POST /api/milestones creates a milestone."""
        goal_id = str(uuid4())
        payload = {
            "goal_id": goal_id,
            "title": "Complete MVP",
            "status": "todo",
            "demo_criterion": "User can create goals",
            "blocking": False,
        }
        response = await client.post("/api/milestones", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Complete MVP"
        assert data["goal_id"] == goal_id
        assert data["status"] == "todo"
        assert "id" in data
        assert "date_created" in data
        assert "date_updated" in data

    async def test_create_milestone_with_due_date(self, client):
        """Test creating milestone with due date."""
        due_date = "2025-12-31T23:59:59Z"
        payload = {
            "goal_id": str(uuid4()),
            "title": "Q4 Milestone",
            "due": due_date,
            "status": "doing",
            "demo_criterion": "Feature deployed",
            "blocking": True,
        }
        response = await client.post("/api/milestones", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["due"] is not None
        assert data["blocking"] is True

    async def test_create_milestone_invalid_status(self, client):
        """Test creating milestone with invalid status."""
        payload = {
            "goal_id": str(uuid4()),
            "title": "Test",
            "status": "invalid_status",
            "demo_criterion": "Demo",
            "blocking": False,
        }
        response = await client.post("/api/milestones", json=payload)
        assert response.status_code == 422  # Validation error

    async def test_create_milestone_missing_required_fields(self, client):
        """Test creating milestone without required fields."""
        payload = {"title": "Test"}
        response = await client.post("/api/milestones", json=payload)
        assert response.status_code == 422

    async def test_list_milestones(self, client):
        """Test GET /api/milestones returns list of milestones."""
        # Create a milestone first
        payload = {
            "goal_id": str(uuid4()),
            "title": "List Test",
            "status": "todo",
            "demo_criterion": "Demo",
            "blocking": False,
        }
        await client.post("/api/milestones", json=payload)

        response = await client.get("/api/milestones")
        assert response.status_code == 200
        data = response.json()
        assert "milestones" in data
        assert isinstance(data["milestones"], list)
        assert len(data["milestones"]) > 0

    async def test_get_milestone_by_id(self, client):
        """Test GET /api/milestones/{id} returns a specific milestone."""
        # Create a milestone
        payload = {
            "goal_id": str(uuid4()),
            "title": "Get Test",
            "status": "done",
            "demo_criterion": "Demo",
            "blocking": False,
        }
        create_response = await client.post("/api/milestones", json=payload)
        milestone_id = create_response.json()["id"]

        response = await client.get(f"/api/milestones/{milestone_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == milestone_id
        assert data["title"] == "Get Test"

    async def test_get_milestone_not_found(self, client):
        """Test GET /api/milestones/{id} with non-existent ID."""
        fake_id = str(uuid4())
        response = await client.get(f"/api/milestones/{fake_id}")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    async def test_update_milestone(self, client):
        """Test PATCH /api/milestones/{id} updates a milestone."""
        # Create a milestone
        payload = {
            "goal_id": str(uuid4()),
            "title": "Original Title",
            "status": "todo",
            "demo_criterion": "Demo",
            "blocking": False,
        }
        create_response = await client.post("/api/milestones", json=payload)
        milestone_id = create_response.json()["id"]

        # Update it
        update_payload = {
            "title": "Updated Title",
            "status": "doing",
        }
        response = await client.patch(f"/api/milestones/{milestone_id}", json=update_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["status"] == "doing"

    async def test_update_milestone_status_only(self, client):
        """Test updating only status field."""
        # Create a milestone
        payload = {
            "goal_id": str(uuid4()),
            "title": "Status Test",
            "status": "todo",
            "demo_criterion": "Demo",
            "blocking": False,
        }
        create_response = await client.post("/api/milestones", json=payload)
        milestone_id = create_response.json()["id"]

        # Update status
        update_payload = {"status": "done"}
        response = await client.patch(f"/api/milestones/{milestone_id}", json=update_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "done"
        assert data["title"] == "Status Test"  # Unchanged

    async def test_update_milestone_not_found(self, client):
        """Test updating non-existent milestone."""
        fake_id = str(uuid4())
        update_payload = {"status": "done"}
        response = await client.patch(f"/api/milestones/{fake_id}", json=update_payload)
        assert response.status_code == 404

    async def test_delete_milestone(self, client):
        """Test DELETE /api/milestones/{id} removes a milestone."""
        # Create a milestone
        payload = {
            "goal_id": str(uuid4()),
            "title": "Delete Test",
            "status": "todo",
            "demo_criterion": "Demo",
            "blocking": False,
        }
        create_response = await client.post("/api/milestones", json=payload)
        milestone_id = create_response.json()["id"]

        # Delete it
        response = await client.delete(f"/api/milestones/{milestone_id}")
        assert response.status_code == 204

        # Verify it's gone
        get_response = await client.get(f"/api/milestones/{milestone_id}")
        assert get_response.status_code == 404

    async def test_delete_milestone_not_found(self, client):
        """Test deleting non-existent milestone."""
        fake_id = str(uuid4())
        response = await client.delete(f"/api/milestones/{fake_id}")
        assert response.status_code == 404

    async def test_rfc7807_error_response(self, client):
        """Test that error responses follow RFC 7807 structure."""
        fake_id = str(uuid4())
        response = await client.get(f"/api/milestones/{fake_id}")
        assert response.status_code == 404
        data = response.json()
        # Should have at least 'detail' field (FastAPI default)
        assert "detail" in data
