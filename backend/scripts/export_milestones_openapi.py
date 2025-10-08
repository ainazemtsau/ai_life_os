#!/usr/bin/env python3
"""Export Milestones OpenAPI schema from the FastAPI application."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from types import ModuleType

# Ensure backend/src is importable
ROOT = Path(__file__).resolve().parents[1]  # .../backend
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

# Optional YAML support
yaml: ModuleType | None
try:
    import yaml  # pip install pyyaml
except Exception:
    yaml = None

# Import FastAPI app
try:
    from ai_life_backend.app import app
except ModuleNotFoundError as e:
    missing = str(e).split("'")[1]
    print(f"[ERROR] Missing Python package: {missing}")
    print("Fix: activate your project virtualenv and install FastAPI")
    sys.exit(1)


def export_openapi(out_path: Path) -> None:
    """Export OpenAPI schema to a JSON or YAML file."""
    schema = app.openapi()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.suffix.lower() in {".yml", ".yaml"} and yaml is not None:
        out_path.write_text(
            yaml.safe_dump(schema, sort_keys=False, allow_unicode=True), encoding="utf-8"
        )
    else:
        out_path.write_text(json.dumps(schema, indent=2), encoding="utf-8")


if __name__ == "__main__":
    out = ROOT / "src" / "ai_life_backend" / "contracts" / "milestones_openapi.yaml"
    export_openapi(out)
    print(f"✓ Milestones OpenAPI schema exported to: {out}")
