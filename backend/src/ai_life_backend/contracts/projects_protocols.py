"""Public contract protocols — backend.projects
Version: 0.1.0
Define typing.Protocol interfaces here for cross-module use.
"""
from typing import Protocol, runtime_checkable


@runtime_checkable
class ProjectReader(Protocol):
    """Read-only query port for Projects."""
    ...


@runtime_checkable
class TaskReader(Protocol):
    """Read-only query port for Tasks."""
    ...
