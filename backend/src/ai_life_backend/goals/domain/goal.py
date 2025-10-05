"""Goal domain entity."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class Goal:
    """
    Immutable domain entity representing a personal goal.

    Attributes:
        id: Unique identifier (UUID)
        title: Goal description (1-255 chars, non-empty after trim)
        is_done: Completion status
        date_created: Creation timestamp (UTC)
        date_updated: Last modification timestamp (UTC)
    """

    id: UUID
    title: str
    is_done: bool
    date_created: datetime
    date_updated: datetime

    def __post_init__(self) -> None:
        """Validate domain invariants."""
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty or whitespace-only")
        if len(self.title) > 255:
            raise ValueError("Title cannot exceed 255 characters")
