"""HTTP utilities for creating public API routers with RFC 7807 Problem responses."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

# Unified set of responses with RFC7807 (only application/problem+json)
PROBLEM_RESPONSES: dict[int | str, dict[str, Any]] = {
    400: {
        "description": "Bad Request",
        "content": {
            "application/problem+json": {"schema": {"$ref": "#/components/schemas/Problem"}}
        },
    },
    404: {
        "description": "Not Found",
        "content": {
            "application/problem+json": {"schema": {"$ref": "#/components/schemas/Problem"}}
        },
    },
    422: {
        "description": "Validation Error",
        "content": {
            "application/problem+json": {"schema": {"$ref": "#/components/schemas/Problem"}}
        },
    },
    500: {
        "description": "Server Error",
        "content": {
            "application/problem+json": {"schema": {"$ref": "#/components/schemas/Problem"}}
        },
    },
}


def make_public_router(internal_router: APIRouter) -> APIRouter:
    """Wrap internal router to apply unified Problem error declarations.

    Applies unified RFC 7807 Problem Details error declarations to all operations.
    Uses explicit $ref references instead of model definitions.
    """
    outer = APIRouter(responses=PROBLEM_RESPONSES)
    outer.include_router(internal_router)
    return outer
