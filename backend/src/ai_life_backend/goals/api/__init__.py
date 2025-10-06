"""API layer for goals module."""

from .schemas import (
    ErrorResponse,
    GoalCreateRequest,
    GoalListResponse,
    GoalResponse,
    GoalUpdateRequest,
)

__all__ = [
    "ErrorResponse",
    "GoalCreateRequest",
    "GoalListResponse",
    "GoalResponse",
    "GoalUpdateRequest",
]
