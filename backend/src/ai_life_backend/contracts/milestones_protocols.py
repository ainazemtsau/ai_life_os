"""Public contract protocols — backend.milestones
Version: 0.1.0
Define typing.Protocol interfaces here for cross-module use.
"""
from typing import Protocol, runtime_checkable


@runtime_checkable
class MilestoneReader(Protocol):
    """Read-only query port for Milestones."""
    ...
