"""Tests for Projects and Tasks domain entities."""

import pytest
from datetime import datetime, timezone
from uuid import uuid4

from ai_life_backend.projects.domain.project import Project, ProjectPriority, ProjectRisk
from ai_life_backend.projects.domain.task import (
    Task,
    TaskSize,
    TaskEnergy,
    TaskContinuity,
    TaskClarity,
    TaskRisk,
)


class TestProject:
    """Test Project domain entity."""

    def test_create_standalone_project(self):
        """Test creating a project without a goal."""
        project = Project(
            id=uuid4(),
            goal_id=None,
            title="Standalone Project",
            status="todo",
            priority=ProjectPriority.P1,
            scope="Project scope summary",
            risk=ProjectRisk.GREEN,
            tags=[],
            dependencies=[],
            date_created=datetime.now(timezone.utc),
            date_updated=datetime.now(timezone.utc),
        )
        assert project.goal_id is None
        assert project.title == "Standalone Project"
        assert project.priority == ProjectPriority.P1

    def test_create_project_with_goal(self):
        """Test creating a project linked to a goal."""
        goal_id = uuid4()
        project = Project(
            id=uuid4(),
            goal_id=goal_id,
            title="Goal-linked Project",
            status="doing",
            priority=ProjectPriority.P0,
            scope="Important project",
            risk=ProjectRisk.YELLOW,
            tags=["urgent"],
            dependencies=[],
            date_created=datetime.now(timezone.utc),
            date_updated=datetime.now(timezone.utc),
        )
        assert project.goal_id == goal_id
        assert project.status == "doing"

    def test_project_title_too_long(self):
        """Test that project title validation fails for too long titles."""
        with pytest.raises(ValueError, match="Title cannot exceed"):
            Project(
                id=uuid4(),
                goal_id=None,
                title="x" * 256,
                status="todo",
                priority=ProjectPriority.P2,
                scope="Scope",
                risk=ProjectRisk.GREEN,
                tags=[],
                dependencies=[],
                date_created=datetime.now(timezone.utc),
                date_updated=datetime.now(timezone.utc),
            )

    def test_project_with_dependencies(self):
        """Test project with dependencies."""
        dep1 = uuid4()
        dep2 = uuid4()
        project = Project(
            id=uuid4(),
            goal_id=uuid4(),
            title="Dependent Project",
            status="blocked",
            priority=ProjectPriority.P1,
            scope="Depends on others",
            risk=ProjectRisk.RED,
            tags=[],
            dependencies=[dep1, dep2],
            date_created=datetime.now(timezone.utc),
            date_updated=datetime.now(timezone.utc),
        )
        assert len(project.dependencies) == 2
        assert dep1 in project.dependencies


class TestTask:
    """Test Task domain entity."""

    def test_create_task(self):
        """Test creating a basic task."""
        task = Task(
            id=uuid4(),
            project_id=uuid4(),
            title="Implement feature",
            status="todo",
            dependencies=[],
            size=TaskSize.M,
            energy=TaskEnergy.FOCUS,
            continuity=TaskContinuity.CHAIN,
            clarity=TaskClarity.CLEAR,
            risk=TaskRisk.GREEN,
            context="Context notes",
            date_created=datetime.now(timezone.utc),
            date_updated=datetime.now(timezone.utc),
        )
        assert task.title == "Implement feature"
        assert task.size == TaskSize.M
        assert task.energy == TaskEnergy.FOCUS

    def test_task_with_dependencies(self):
        """Test task with dependencies."""
        dep1 = uuid4()
        dep2 = uuid4()
        task = Task(
            id=uuid4(),
            project_id=uuid4(),
            title="Blocked task",
            status="blocked",
            dependencies=[dep1, dep2],
            size=TaskSize.L,
            energy=TaskEnergy.DEEP,
            continuity=TaskContinuity.PUZZLE,
            clarity=TaskClarity.CLOUDY,
            risk=TaskRisk.YELLOW,
            context="",
            date_created=datetime.now(timezone.utc),
            date_updated=datetime.now(timezone.utc),
        )
        assert len(task.dependencies) == 2
        assert dep1 in task.dependencies

    def test_task_title_validation(self):
        """Test task title length validation."""
        with pytest.raises(ValueError, match="Title cannot exceed"):
            Task(
                id=uuid4(),
                project_id=uuid4(),
                title="x" * 256,
                status="todo",
                dependencies=[],
                size=TaskSize.XS,
                energy=TaskEnergy.LIGHT,
                continuity=TaskContinuity.LINKED,
                clarity=TaskClarity.UNKNOWN,
                risk=TaskRisk.GREEN,
                context="",
                date_created=datetime.now(timezone.utc),
                date_updated=datetime.now(timezone.utc),
            )

    def test_task_all_enum_values(self):
        """Test task with various enum values."""
        task = Task(
            id=uuid4(),
            project_id=uuid4(),
            title="Test task",
            status="done",
            dependencies=[],
            size=TaskSize.XL,
            energy=TaskEnergy.DEEP,
            continuity=TaskContinuity.PUZZLE,
            clarity=TaskClarity.CLEAR,
            risk=TaskRisk.RED,
            context="Complex work",
            date_created=datetime.now(timezone.utc),
            date_updated=datetime.now(timezone.utc),
        )
        assert task.size == TaskSize.XL
        assert task.energy == TaskEnergy.DEEP
        assert task.risk == TaskRisk.RED
