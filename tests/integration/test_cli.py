"""
Integration tests for CLI execution.
Feature: 001-goal-two-tiny
Module: app
Phase: B (Tests First - MUST FAIL before implementation)

These tests validate FR-001 (CLI entry point) and FR-004 (display greeting).
"""

import subprocess
import sys
import unittest


class TestCLIExecution(unittest.TestCase):
    """Integration tests for the CLI application."""

    def test_cli_execution_produces_output(self):
        """
        Test that 'python -m src.app' prints greeting to stdout.
        Validates: FR-001 (CLI entry point), FR-004 (display greeting)
        Expected: MUST FAIL (no implementation yet)
        """
        result = subprocess.run(
            [sys.executable, "-m", "src.app"],
            capture_output=True,
            text=True,
            cwd="C:/Users/Anton/StudioProjects/ai_life_os"
        )

        # Verify output is not empty
        self.assertTrue(
            len(result.stdout.strip()) > 0,
            "CLI should produce non-empty output"
        )

        # Verify output contains greeting-like text
        self.assertIn(
            "Hello",
            result.stdout,
            "Output should contain a greeting"
        )

    def test_cli_execution_success(self):
        """
        Test that CLI exits with code 0 (success).
        Validates: FR-001 (CLI entry point)
        Expected: MUST FAIL (no implementation yet)
        """
        result = subprocess.run(
            [sys.executable, "-m", "src.app"],
            capture_output=True,
            text=True,
            cwd="C:/Users/Anton/StudioProjects/ai_life_os"
        )

        self.assertEqual(
            result.returncode,
            0,
            "CLI should exit with code 0"
        )


if __name__ == "__main__":
    unittest.main()
