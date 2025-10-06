"""Goals Module - Public Contract (Protocol Definitions).

Version: 0.1.0

This contract defines the repository interface that must be implemented
by any concrete repository for the goals module.
"""

from typing import Protocol
from uuid import UUID

from ai_life_backend.goals.domain import Goal


class GoalRepository(Protocol):
    """Repository interface for Goal persistence.

    All implementations must provide these async methods.
    """

    async def create(self, title: str) -> Goal:
        """Create a new goal.

        Args:
            title: Goal title (1-255 characters, non-empty after trim)

        Returns:
            Created Goal entity with generated ID and timestamps

        Raises:
            ValueError: If title is empty or exceeds 255 characters
        """
        ...

    async def get_by_id(self, goal_id: UUID) -> Goal | None:
        """Retrieve a single goal by ID.

        Args:
            goal_id: UUID of the goal

        Returns:
            Goal entity if found, None otherwise
        """
        ...

    async def list_all(self) -> list[Goal]:
        """List all goals.

        Returns:
            List of all goals, sorted by is_done ASC, date_updated DESC
            (active goals first, most recently updated first)
        """
        ...

    async def list_by_status(self, is_done: bool) -> list[Goal]:
        """List goals filtered by completion status.

        Args:
            is_done: True for completed goals, False for active goals

        Returns:
            List of matching goals, sorted by date_updated DESC
        """
        ...

    async def update(
        self, goal_id: UUID, title: str | None = None, is_done: bool | None = None
    ) -> Goal | None:
        """Update a goal's title and/or completion status.

        Args:
            goal_id: UUID of the goal to update
            title: New title (optional)
            is_done: New completion status (optional)

        Returns:
            Updated Goal entity if found, None if goal doesn't exist

        Raises:
            ValueError: If title is empty or exceeds 255 characters
            ValueError: If no fields provided for update
        """
        ...

    async def delete(self, goal_id: UUID) -> bool:
        """Delete a goal permanently.

        Args:
            goal_id: UUID of the goal to delete

        Returns:
            True if goal was deleted, False if goal not found
        """
        ...


__all__ = ["GoalRepository"]
