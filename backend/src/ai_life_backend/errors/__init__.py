# backend/src/ai_life_backend/errors/__init__.py
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from .models import Problem


async def http_exception_handler(request: Request, exc: HTTPException):
    body = Problem(title=exc.detail or "HTTP Error", status=exc.status_code).model_dump()
    return JSONResponse(
        status_code=exc.status_code, content=body, media_type="application/problem+json"
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    body = Problem(title="Validation Error", status=422, detail=str(exc.errors())).model_dump()
    return JSONResponse(status_code=422, content=body, media_type="application/problem+json")
