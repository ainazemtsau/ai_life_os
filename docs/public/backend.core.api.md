# Public API — backend.core
Version: 0.1.0

## Overview
Cross-cutting helpers for HTTP surfaces. Stable import point for other backend modules.

## Exports
- `make_public_router(internal_router: APIRouter) -> APIRouter` — wraps a feature router and attaches unified RFC7807 error responses
- `PROBLEM_RESPONSES: dict[int, object]` — shared FastAPI `responses` mapping for 400/404/422/500

## Usage
```py
from ai_life_backend.core.public import make_public_router
from .api.routes import router as _internal

public_router = make_public_router(_internal)

Notes

This is the only supported import surface of backend.core for other modules.

Internals (e.g., httpkit) are private and may change.

