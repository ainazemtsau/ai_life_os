"""Tests for Milestone domain entity."""

import pytest
from datetime import datetime, timezone
from uuid import uuid4

from ai_life_backend.milestones.domain.milestone import Milestone


class TestMilestone:
    """Test Milestone domain entity."""

    def test_create_milestone(self):
        """Test creating a basic milestone."""
        goal_id = uuid4()
        milestone = Milestone(
            id=uuid4(),
            goal_id=goal_id,
            title="Complete MVP",
            due=None,
            status="todo",
            demo_criterion="User can create and list goals",
            blocking=False,
            date_created=datetime.now(timezone.utc),
            date_updated=datetime.now(timezone.utc),
        )
        assert milestone.goal_id == goal_id
        assert milestone.title == "Complete MVP"
        assert milestone.status == "todo"
        assert milestone.blocking is False

    def test_milestone_with_due_date(self):
        """Test milestone with a due date."""
        due_date = datetime(2025, 12, 31, tzinfo=timezone.utc)
        milestone = Milestone(
            id=uuid4(),
            goal_id=uuid4(),
            title="Q4 Milestone",
            due=due_date,
            status="doing",
            demo_criterion="Feature deployed to production",
            blocking=True,
            date_created=datetime.now(timezone.utc),
            date_updated=datetime.now(timezone.utc),
        )
        assert milestone.due == due_date
        assert milestone.blocking is True

    def test_milestone_status_values(self):
        """Test milestone with different status values."""
        for status in ["todo", "doing", "done", "blocked"]:
            milestone = Milestone(
                id=uuid4(),
                goal_id=uuid4(),
                title=f"Milestone {status}",
                due=None,
                status=status,
                demo_criterion="Demo",
                blocking=False,
                date_created=datetime.now(timezone.utc),
                date_updated=datetime.now(timezone.utc),
            )
            assert milestone.status == status

    def test_milestone_title_too_long(self):
        """Test that milestone title validation fails for too long titles."""
        with pytest.raises(ValueError, match="Title cannot exceed"):
            Milestone(
                id=uuid4(),
                goal_id=uuid4(),
                title="x" * 256,
                due=None,
                status="todo",
                demo_criterion="Demo",
                blocking=False,
                date_created=datetime.now(timezone.utc),
                date_updated=datetime.now(timezone.utc),
            )

    def test_milestone_immutability(self):
        """Test that milestone is immutable (frozen dataclass)."""
        milestone = Milestone(
            id=uuid4(),
            goal_id=uuid4(),
            title="Immutable Milestone",
            due=None,
            status="todo",
            demo_criterion="Demo",
            blocking=False,
            date_created=datetime.now(timezone.utc),
            date_updated=datetime.now(timezone.utc),
        )
        with pytest.raises(Exception):  # FrozenInstanceError
            milestone.title = "Modified"  # type: ignore
