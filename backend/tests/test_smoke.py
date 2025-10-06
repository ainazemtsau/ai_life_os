"""Smoke test to ensure basic imports work."""

from ai_life_backend.app import app


def test_imports() -> None:
    """Test that basic imports work without errors."""
    assert app is not None
    assert app.title == "AI Life OS API"
