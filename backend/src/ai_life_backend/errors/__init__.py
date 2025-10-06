"""Error handling and RFC 7807 Problem Details implementation."""

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .models import Problem


def http_exception_handler(_request: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI HTTPException and return a Problem Details JSON response.

    Parameters
    ----------
    _request : Request
        The incoming HTTP request.
    exc : HTTPException
        The exception raised during request processing.

    Returns:
    -------
    JSONResponse
        A JSON response formatted according to RFC 7807 Problem Details.
    """
    body = Problem(title=exc.detail or "HTTP Error", status=exc.status_code).model_dump()
    return JSONResponse(
        status_code=exc.status_code, content=body, media_type="application/problem+json"
    )


def validation_exception_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle FastAPI RequestValidationError and return a Problem Details JSON response.

    Parameters
    ----------
    _request : Request
        The incoming HTTP request.
    exc : RequestValidationError
        The validation exception raised during request processing.

    Returns:
    -------
    JSONResponse
        A JSON response formatted according to RFC 7807 Problem Details.
    """
    body = Problem(title="Validation Error", status=422, detail=str(exc.errors())).model_dump()
    return JSONResponse(status_code=422, content=body, media_type="application/problem+json")
