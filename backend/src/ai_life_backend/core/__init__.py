"""Core utilities and error handling for AI Life Backend."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, HTTPException

from ai_life_backend.contracts.core_protocols import (
    RFC7807_MIME,
    HttpErrorFactory,
    ProblemBuilder,
    ProblemDict,
)
from ai_life_backend.core.httpkit import make_public_router as _make_public_router


def utcnow() -> datetime:
    """Timezone-aware UTC timestamp (single source of truth)."""
    return datetime.now(UTC)


def problem(
    *,
    title: str,
    status: int,
    detail: str | None = None,
    type: str | None = None,
    instance: str | None = None,
) -> Mapping[str, Any]:
    """Build RFC7807-compatible dict (serializable)."""
    p: ProblemDict = {"title": title, "status": status}
    if type is not None:
        p["type"] = type
    if detail is not None:
        p["detail"] = detail
    if instance is not None:
        p["instance"] = instance
    return dict(p)


def http_error(
    *,
    title: str,
    status: int = 400,
    detail: str | None = None,
    type: str | None = None,
    instance: str | None = None,
) -> Exception:
    """Create an exception for RFC 7807 Problem response.

    Creates an HTTPException that will be translated by the web layer
    to `application/problem+json` response.
    """
    payload = problem(title=title, status=status, detail=detail, type=type, instance=instance)
    return HTTPException(status_code=status, detail=payload)


def make_public_router(internal_router: APIRouter) -> APIRouter:
    """Create public API router with unified RFC 7807 error responses."""
    return _make_public_router(internal_router)


__all__ = [
    "RFC7807_MIME",
    "HttpErrorFactory",
    "ProblemBuilder",
    "ProblemDict",
    "http_error",
    "make_public_router",
    "problem",
    "utcnow",
]
