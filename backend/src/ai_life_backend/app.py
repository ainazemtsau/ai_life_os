"""FastAPI application entrypoint with CORS configuration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Life OS API",
    description="Goals Management MVP - Backend API",
    version="0.1.0",
)

# CORS configuration for frontend-backend communication
# Allows requests from Next.js development server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type"],
)

# Include goals router
from ai_life_backend.goals.public import goals_router
app.include_router(goals_router, prefix="/api")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


def main() -> None:
    """Backend bootstrap entry point. Keep it minimal for now."""
    print("AI Life OS backend bootstrap OK")


if __name__ == "__main__":
    main()
