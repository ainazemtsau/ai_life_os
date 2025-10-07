"""Milestone domain entity."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

MAX_TITLE_LENGTH = 255


@dataclass(frozen=True)
class Milestone:
    """Immutable domain entity representing a milestone.

    A milestone is a verifiable step toward achieving a goal.

    Attributes:
        id: Unique identifier (UUID)
        goal_id: Reference to the associated goal (UUID)
        title: Milestone description (1-255 chars, non-empty after trim)
        due: Optional due date (UTC)
        status: Current status (todo/doing/done/blocked)
        demo_criterion: Verifiable criterion for completion
        blocking: Whether this milestone blocks other work
        date_created: Creation timestamp (UTC)
        date_updated: Last modification timestamp (UTC)
    """

    id: UUID
    goal_id: UUID
    title: str
    due: datetime | None
    status: str
    demo_criterion: str
    blocking: bool
    date_created: datetime
    date_updated: datetime

    def __post_init__(self) -> None:
        """Validate domain invariants."""
        if len(self.title) > MAX_TITLE_LENGTH:
            msg = f"Title cannot exceed {MAX_TITLE_LENGTH} characters"
            raise ValueError(msg)

        if len(self.demo_criterion) > MAX_TITLE_LENGTH:
            msg = f"Demo criterion cannot exceed {MAX_TITLE_LENGTH} characters"
            raise ValueError(msg)
