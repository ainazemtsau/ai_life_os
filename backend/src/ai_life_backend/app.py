"""AI Life OS FastAPI application with goals management API."""

from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from ai_life_backend.goals.public import goals_router
from ai_life_backend.milestones.public import milestones_router

app = FastAPI(
    title="AI Life OS API",
    description="Goals Management MVP - Backend API",
    version="0.1.0",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type"],
)


app.include_router(goals_router, prefix="/api", tags=["goals"])
app.include_router(milestones_router, prefix="/api", tags=["milestones"])


@app.get(
    "/health",
    tags=["health"],
    responses={
        400: {
            "description": "Bad Request",
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
    },
)
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


def custom_openapi() -> dict[str, Any]:
    """Generate custom OpenAPI schema with RFC7807 Problem schema."""
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # 1) RFC7807 Problem — схема в components
    schema.setdefault("components", {}).setdefault("schemas", {})["Problem"] = {
        "type": "object",
        "properties": {
            "type": {"type": "string", "format": "uri"},
            "title": {"type": "string"},
            "status": {"type": "integer"},
            "detail": {"type": "string"},
            "instance": {"type": "string", "format": "uri"},
        },
        "required": ["title", "status"],
        "additionalProperties": True,
    }

    # 2) servers — требуется Redocly (no-empty-servers)
    schema["servers"] = [
        {"url": "http://localhost:8000", "description": "Local dev"},
        # при деплое добавишь продовый URL здесь
    ]

    # 3) security на корне — даже если публично, объявляем пустой массив
    # удовлетворяет правилу security-defined
    schema["security"] = []  # означает: креды не требуются, и это явно задокументировано

    # 4) license в info — закрывает info-license
    info = schema.setdefault("info", {})
    info.setdefault("license", {"name": "Proprietary (internal)"})
    # можно указать MIT, если хочешь: {"name": "MIT", "url": "https://opensource.org/licenses/MIT"}

    # (опционально) описания тегов
    schema["tags"] = [
        {"name": "goals", "description": "Goals management endpoints"},
        {"name": "milestones", "description": "Milestones management endpoints"},
        {"name": "health", "description": "Health checks"},
    ]

    app.openapi_schema = schema
    return app.openapi_schema


# Override the openapi method to use our custom schema
app.openapi = custom_openapi  # type: ignore[method-assign]
