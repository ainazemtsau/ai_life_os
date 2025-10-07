"""backend.core public surface (stable import point).

Export ONLY what other modules are allowed to use from core.
This is the module's facade; internal structure may change without breaking consumers.
"""

from fastapi import APIRouter
from .httpkit import PROBLEM_RESPONSES, make_public_router

__all__ = [
    "APIRouter",            # re-exported typing aid for router signatures (optional)
    "make_public_router",   # wrapper applying unified RFC7807 responses
    "PROBLEM_RESPONSES",    # shared responses mapping
]
