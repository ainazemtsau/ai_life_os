"""Task domain entity."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID

MAX_TITLE_LENGTH = 255


class TaskSize(str, Enum):
    """Task size estimation."""

    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"


class TaskEnergy(str, Enum):
    """Task energy requirement."""

    DEEP = "Deep"
    FOCUS = "Focus"
    LIGHT = "Light"


class TaskContinuity(str, Enum):
    """Task continuity type."""

    CHAIN = "chain"
    LINKED = "linked"
    PUZZLE = "puzzle"


class TaskClarity(str, Enum):
    """Task clarity level."""

    CLEAR = "clear"
    CLOUDY = "cloudy"
    UNKNOWN = "unknown"


class TaskRisk(str, Enum):
    """Task risk level."""

    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


@dataclass(frozen=True)
class Task:
    """Immutable domain entity representing a task.

    A task is the smallest planning unit. Tasks belong to exactly one Project
    and may depend on other tasks within the same Project (must be DAG).

    Attributes:
        id: Unique identifier (UUID)
        project_id: Parent project ID (required)
        title: Task title (1-255 chars, non-empty after trim)
        status: Current status (todo/doing/done/blocked)
        dependencies: List of task IDs this task depends on (within same project)
        size: Size estimation (XS/S/M/L/XL)
        energy: Energy requirement (Deep/Focus/Light)
        continuity: Continuity type (chain/linked/puzzle)
        clarity: Clarity level (clear/cloudy/unknown)
        risk: Risk level (green/yellow/red)
        context: Additional context notes
        date_created: Creation timestamp (UTC)
        date_updated: Last modification timestamp (UTC)
    """

    id: UUID
    project_id: UUID
    title: str
    status: str
    dependencies: list[UUID]
    size: TaskSize
    energy: TaskEnergy
    continuity: TaskContinuity
    clarity: TaskClarity
    risk: TaskRisk
    context: str
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
