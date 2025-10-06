# Public API — backend.core
Version: 0.1.0

## Overview
Cross-cutting utilities for backend modules. **No domain logic.**  
Focus: consistent error representation (RFC 7807 Problem Details) and tiny helpers reused across features.

## Exports (in-process only)
### errors (RFC 7807 helpers)
- `ProblemDetails` — lightweight dataclass (type, title, status, detail?, instance?)
- `problem(*, title: str, status: int, detail: str | None = None, type: str | None = None, instance: str | None = None) -> dict`
  - Build a Problem Details dict (serializable).
- `http_error(*, title: str, status: int = 400, detail: str | None = None, type: str | None = None) -> Exception`
  - Raise/return an exception suitable for FastAPI handlers with `application/problem+json` payload.

> These helpers standardize error shape across modules (providers) and simplify consumer handling.

### utils (minimal, optional)
- `utcnow() -> datetime` — timezone-aware UTC `datetime` (for consistent stamping in tests/impl).

> Keep this module small; add only widely reused, cross-cutting bits.

## Types
- `ProblemDetails`:
  ```py
  from dataclasses import dataclass
  @dataclass(frozen=True)
  class ProblemDetails:
      type: str | None
      title: str
      status: int
      detail: str | None = None
      instance: str | None = None
