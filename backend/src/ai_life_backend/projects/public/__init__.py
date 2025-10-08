"""Public API for backend.projects module.

This module exposes the public surface for cross-module use.
Consumers should only import from this module using the import_hint:
    from ai_life_backend.projects.public import *

For HTTP access, use the REST API endpoints defined in the OpenAPI contract.
"""

from ai_life_backend.projects.api.routes import projects_router, tasks_router
from ai_life_backend.projects.domain import (
    Project,
    ProjectPriority,
    ProjectRisk,
    Task,
    TaskSize,
    TaskEnergy,
    TaskContinuity,
    TaskClarity,
    TaskRisk,
)

__all__ = [
    # API routers
    "projects_router",
    "tasks_router",
    # Domain entities
    "Project",
    "ProjectPriority",
    "ProjectRisk",
    "Task",
    "TaskSize",
    "TaskEnergy",
    "TaskContinuity",
    "TaskClarity",
    "TaskRisk",
]
