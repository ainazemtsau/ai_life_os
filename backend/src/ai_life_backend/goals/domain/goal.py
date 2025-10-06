"""Goal domain entity."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

MAX_TITLE_LENGTH = 255


@dataclass(frozen=True)
class Goal:
    """Immutable domain entity representing a personal goal.

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
        if len(self.title) > MAX_TITLE_LENGTH:
            msg = f"Title cannot exceed {MAX_TITLE_LENGTH} characters"
            raise ValueError(msg)
