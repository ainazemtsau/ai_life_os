"""Project domain entity."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID

MAX_TITLE_LENGTH = 255


class ProjectPriority(str, Enum):
    """Project priority levels."""

    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class ProjectRisk(str, Enum):
    """Project risk levels."""

    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


@dataclass(frozen=True)
class Project:
    """Immutable domain entity representing a project.

    A project is a work container that may be standalone or linked to a Goal.
    Projects within the same Goal may depend on each other (must be DAG).

    Attributes:
        id: Unique identifier (UUID)
        goal_id: Optional link to parent Goal (None for standalone projects)
        title: Project title (1-255 chars, non-empty after trim)
        status: Current status (todo/doing/done/blocked)
        priority: Priority level (P0-P3)
        scope: Project scope summary
        risk: Risk assessment (green/yellow/red)
        tags: List of tags
        dependencies: List of project IDs this project depends on (within same Goal)
        date_created: Creation timestamp (UTC)
        date_updated: Last modification timestamp (UTC)
    """

    id: UUID
    goal_id: UUID | None
    title: str
    status: str
    priority: ProjectPriority
    scope: str
    risk: ProjectRisk
    tags: list[str]
    dependencies: list[UUID]
    date_created: datetime
    date_updated: datetime

    def __post_init__(self) -> None:
        """Validate domain invariants."""
        if len(self.title) > MAX_TITLE_LENGTH:
            msg = f"Title cannot exceed {MAX_TITLE_LENGTH} characters"
            raise ValueError(msg)
        if not self.title.strip():
            msg = "Title cannot be empty"
            raise ValueError(msg)
