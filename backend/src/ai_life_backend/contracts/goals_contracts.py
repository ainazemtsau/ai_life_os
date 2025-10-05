"""
Public API Contract: backend.goals
Version: 0.1.0

Protocol definitions for Goals Management module.
Defines repository and service interfaces for dependency inversion.
"""

from typing import Protocol
from uuid import UUID
from datetime import datetime


class Goal(Protocol):
    """
    Domain entity representing a personal goal.

    Immutable value object with auto-generated timestamps.
    """

    id: UUID
    title: str  # 1-255 characters, non-empty after trim
    is_done: bool  # Completion status
    date_created: datetime  # ISO 8601 with timezone
    date_updated: datetime  # ISO 8601 with timezone, refreshed on any modification


class GoalRepository(Protocol):
    """
    Repository interface for Goal persistence.

    All methods are async for compatibility with asyncio/asyncpg.
    Implementations must handle database errors and convert to domain exceptions.
    """

    async def create(self, title: str) -> Goal:
        """
        Create a new goal with auto-generated id and timestamps.

        Args:
            title: Goal title (1-255 chars, non-empty after trim)

        Returns:
            Created Goal entity

        Raises:
            ValueError: If title is invalid (empty, too long)
        """
        ...

    async def get_by_id(self, goal_id: UUID) -> Goal | None:
        """
        Retrieve goal by UUID.

        Args:
            goal_id: Unique goal identifier

        Returns:
            Goal if found, None otherwise
        """
        ...

    async def list_all(self) -> list[Goal]:
        """
        List all goals, sorted by (is_done ASC, date_updated DESC).

        Returns:
            List of goals (active first, then done; within each group, most recent first)
        """
        ...

    async def list_by_status(self, is_done: bool) -> list[Goal]:
        """
        List goals filtered by completion status, sorted by date_updated DESC.

        Args:
            is_done: True for completed goals, False for active goals

        Returns:
            Filtered list of goals (most recent first)
        """
        ...

    async def update(
        self,
        goal_id: UUID,
        title: str | None = None,
        is_done: bool | None = None,
    ) -> Goal | None:
        """
        Update goal fields and refresh date_updated.

        At least one of title or is_done must be provided.

        Args:
            goal_id: Goal to update
            title: New title (optional, 1-255 chars if provided)
            is_done: New completion status (optional)

        Returns:
            Updated Goal if found and updated, None if not found

        Raises:
            ValueError: If title is invalid or no fields provided
        """
        ...

    async def delete(self, goal_id: UUID) -> bool:
        """
        Permanently delete a goal.

        Args:
            goal_id: Goal to delete

        Returns:
            True if goal was deleted, False if goal was not found
        """
        ...


class GoalService(Protocol):
    """
    Service interface for Goal business logic.

    Orchestrates repository calls and enforces business rules.
    Thin service layer for MVP (mostly delegates to repository).
    """

    async def create_goal(self, title: str) -> Goal:
        """Create a new goal."""
        ...

    async def get_goal(self, goal_id: UUID) -> Goal | None:
        """Get a single goal by ID."""
        ...

    async def list_goals(self, status_filter: str | None = None) -> list[Goal]:
        """
        List goals with optional status filter.

        Args:
            status_filter: 'active', 'done', or None for all
        """
        ...

    async def update_goal(
        self,
        goal_id: UUID,
        title: str | None = None,
        is_done: bool | None = None,
    ) -> Goal | None:
        """Update a goal's title and/or completion status."""
        ...

    async def delete_goal(self, goal_id: UUID) -> bool:
        """Delete a goal permanently."""
        ...
