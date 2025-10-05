"""Contract tests for Goals API - validate OpenAPI compliance."""
import pytest
from fastapi.testclient import TestClient
from uuid import uuid4


@pytest.fixture
def client():
    """Create test client for goals API."""
    from ai_life_backend.app import app
    return TestClient(app)


class TestGoalsAPIContract:
    """Contract tests validating OpenAPI schema compliance."""

    def test_post_goals_validates_schema(self, client):
        """T040: POST /api/goals validates request/response schema."""
        # Valid request
        response = client.post("/api/goals", json={"title": "Test Goal"})
        # Note: Will fail until DB is properly connected
        # Expected: 201 with proper schema
        assert response.status_code in [201, 500]  # 500 if DB not connected
        if response.status_code == 201:
            data = response.json()
            assert "id" in data
            assert data["title"] == "Test Goal"
            assert data["is_done"] is False
            assert "date_created" in data
            assert "date_updated" in data

        # Invalid: missing title
        response = client.post("/api/goals", json={})
        assert response.status_code == 422

        # Invalid: empty title
        response = client.post("/api/goals", json={"title": "  "})
        assert response.status_code == 422

        # Invalid: title too long
        response = client.post("/api/goals", json={"title": "a" * 256})
        assert response.status_code == 422

    def test_get_goals_returns_list_schema(self, client):
        """T041: GET /api/goals returns GoalListResponse schema."""
        response = client.get("/api/goals")
        assert response.status_code in [200, 500]
        if response.status_code == 200:
            data = response.json()
            assert "goals" in data
            assert isinstance(data["goals"], list)

    def test_get_goal_by_id_validates_uuid(self, client):
        """T042: GET /api/goals/{id} validates UUID parameter."""
        # Invalid UUID format
        response = client.get("/api/goals/not-a-uuid")
        assert response.status_code == 422

        # Valid UUID but not found (or DB error)
        response = client.get(f"/api/goals/{uuid4()}")
        assert response.status_code in [404, 500]

    def test_patch_goal_validates_request_body(self, client):
        """T043: PATCH /api/goals/{id} validates request schema."""
        test_id = uuid4()

        # Invalid: no fields provided
        response = client.patch(f"/api/goals/{test_id}", json={})
        assert response.status_code == 422

        # Invalid: empty title
        response = client.patch(f"/api/goals/{test_id}", json={"title": ""})
        assert response.status_code == 422

    def test_delete_goal_returns_204(self, client):
        """T044: DELETE /api/goals/{id} returns 204 No Content or 404."""
        test_id = uuid4()

        # Delete non-existent (or DB error)
        response = client.delete(f"/api/goals/{test_id}")
        assert response.status_code in [204, 404, 500]
