#!/usr/bin/env python3
"""
Integration Tests for Unified Prompt Toolkit
============================================

Verifies the full execution pipeline using the local model (Tier 0).
Requires: Local ONNX model (phi4mini or mistral) in AI Gallery cache.

These tests are marked as 'slow' and skipped by default in pytest.
Run with: pytest -m slow to include them.
"""

import subprocess
import sys
import unittest
from pathlib import Path

import pytest

# Add project root to path
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parents[1]
sys.path.insert(0, str(REPO_ROOT))


@pytest.mark.slow
class TestPromptToolkitIntegration(unittest.TestCase):
    """Integration tests executing prompt.py against local models.

    These tests are slow (load ONNX models) and marked with @pytest.mark.slow.
    Skip by default with: pytest -m "not slow"
    Run only these with: pytest -m slow
    """

    @classmethod
    def setUpClass(cls):
        """Check if local model is available before running tests."""
        sys.path.insert(0, str(REPO_ROOT / "tools"))

        # Check for library
        try:
            import onnxruntime_genai
        except ImportError:
            raise unittest.SkipTest("onnxruntime-genai not installed")

        # Check for model files
        try:
            from local_model import check_model_available

            if not check_model_available():
                raise unittest.SkipTest(
                    "No local ONNX models found in AI Gallery cache"
                )
        except ImportError:
            pass

    def test_run_command_local_provider(self):
        """Test 'run' command with local provider."""
        # Create a temporary prompt file
        prompt_file = SCRIPT_DIR / "temp_test_prompt.md"
        prompt_file.write_text("What is 2+2? Answer in one word.", encoding="utf-8")

        try:
            # Execute prompt.py - increase timeout for slow model loading
            result = subprocess.run(
                [
                    sys.executable,
                    str(REPO_ROOT / "prompt.py"),
                    "run",
                    str(prompt_file),
                    "-p",
                    "local",
                    "--temperature",
                    "0.1",
                ],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes for model loading
                encoding="utf-8",
                cwd=str(REPO_ROOT),
            )

            # Check success
            self.assertEqual(result.returncode, 0, f"Command failed: {result.stderr}")
            # LLM responses vary - just check we got a non-empty response
            self.assertIn("Response", result.stdout)

        finally:
            if prompt_file.exists():
                prompt_file.unlink()

    def test_run_command_with_system_flag(self):
        """Test 'run' command with system flag."""
        prompt_file = SCRIPT_DIR / "temp_sys_prompt.md"
        prompt_file.write_text("What is 10+10?", encoding="utf-8")

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    str(REPO_ROOT / "prompt.py"),
                    "run",
                    str(prompt_file),
                    "-p",
                    "local",
                    "-s",
                    "Answer in json",
                ],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes for model loading
                encoding="utf-8",
                cwd=str(REPO_ROOT),
            )

            self.assertEqual(result.returncode, 0)
            # Response should likely be JSON-formatted if system prompt worked
            # Note: Checking for "{" might be flaky depending on model, but reasonable for integration test

        finally:
            if prompt_file.exists():
                prompt_file.unlink()

    def test_eval_command_structure(self):
        """Test 'eval' command runs (smoke test)."""
        # Create a dummy directory with one prompt
        test_dir = SCRIPT_DIR / "temp_eval_test"
        test_dir.mkdir(exist_ok=True)
        (test_dir / "test.md").write_text("Hello world", encoding="utf-8")

        try:
            # Run quick structure check (Tier 1)
            result = subprocess.run(
                [
                    sys.executable,
                    str(REPO_ROOT / "prompt.py"),
                    "eval",
                    str(test_dir),
                    "-t",
                    "1",
                ],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes
                encoding="utf-8",
                cwd=str(REPO_ROOT),
            )

            self.assertEqual(result.returncode, 0, f"Eval failed: {result.stderr}")

        finally:
            # Cleanup
            import shutil

            shutil.rmtree(test_dir)

    def test_cove_command_local(self):
        """Test 'cove' command runs with local provider."""
        result = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "prompt.py"),
                "cove",
                "What is the capital of France?",
                "-p",
                "local",
                "-n",
                "1",
            ],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutes for model loading
            encoding="utf-8",
            cwd=str(REPO_ROOT),
        )

        self.assertEqual(result.returncode, 0, f"CoVe failed: {result.stderr}")
        # Check for CoVe output - look for phase markers (output format may vary)
        output = result.stdout.lower()
        has_cove_markers = (
            "phase" in output
            or "verification" in output
            or "draft" in output
            or "cove" in output
        )
        self.assertTrue(
            has_cove_markers,
            f"Expected CoVe output markers, got: {result.stdout[:200]}",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
