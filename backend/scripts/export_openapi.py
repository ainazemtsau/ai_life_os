#!/usr/bin/env python3
"""Export OpenAPI schema from FastAPI application."""
import json
import sys
from pathlib import Path

# Add backend src to path
backend_src = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(backend_src))

from ai_life_backend.app import app


def export_openapi() -> None:
    """Export OpenAPI schema to YAML format."""
    # Get OpenAPI schema
    openapi_schema = app.openapi()

    # Output path
    output_path = Path(__file__).parent.parent / "src" / "ai_life_backend" / "contracts" / "goals_openapi.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write JSON (easier to ensure formatting)
    with open(output_path, "w") as f:
        json.dump(openapi_schema, f, indent=2)

    print(f"✓ OpenAPI schema exported to: {output_path}")


if __name__ == "__main__":
    export_openapi()
