from __future__ import annotations
from fastapi import APIRouter

# Единый набор ответов с RFC7807 (только application/problem+json)
PROBLEM_RESPONSES = {
    400: {"description": "Bad Request", "content": {"application/problem+json": {"schema": {"$ref": "#/components/schemas/Problem"}}}},
    404: {"description": "Not Found", "content": {"application/problem+json": {"schema": {"$ref": "#/components/schemas/Problem"}}}},
    422: {"description": "Validation Error", "content": {"application/problem+json": {"schema": {"$ref": "#/components/schemas/Problem"}}}},
    500: {"description": "Server Error", "content": {"application/problem+json": {"schema": {"$ref": "#/components/schemas/Problem"}}}},
}

def make_public_router(internal_router: APIRouter) -> APIRouter:
    """
    Оборачивает внутренний роутер, чтобы ко всем операциям применилась
    единая декларация ошибок (Problem). Без model=..., только явный $ref.
    """
    outer = APIRouter(responses=PROBLEM_RESPONSES)
    outer.include_router(internal_router)
    return outer
