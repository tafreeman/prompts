#!/usr/bin/env python3
"""
Integration Tests for Unified Prompt Toolkit
============================================

Verifies the full execution pipeline using the local model (Tier 0).
Requires: Local ONNX model (phi4mini or mistral) in AI Gallery cache.
"""

import sys
import os
import unittest
import subprocess
from pathlib import Path

# Add project root to path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))


class TestPromptToolkitIntegration(unittest.TestCase):
    """Integration tests executing prompt.py against local models."""

    @classmethod
    def setUpClass(cls):
        """Check if local model is available before running tests."""
        sys.path.insert(0, str(SCRIPT_DIR / "tools"))
        
        # Check for library
        try:
            import onnxruntime_genai
        except ImportError:
            raise unittest.SkipTest("onnxruntime-genai not installed")

        # Check for model files
        try:
            from local_model import check_model_available
            if not check_model_available():
                raise unittest.SkipTest("No local ONNX models found in AI Gallery cache")
        except ImportError:
            pass

    def test_run_command_local_provider(self):
        """Test 'run' command with local provider."""
        # Create a temporary prompt file
        prompt_file = SCRIPT_DIR / "temp_test_prompt.md"
        prompt_file.write_text("What is 2+2? Answer in one word.", encoding="utf-8")

        try:
            # Execute prompt.py
            result = subprocess.run(
                [sys.executable, "prompt.py", "run", str(prompt_file), "-p", "local", "--temperature", "0.1"],
                capture_output=True,
                text=True,
                timeout=120,
                encoding="utf-8"
            )

            # Check success
            self.assertEqual(result.returncode, 0, f"Command failed: {result.stderr}")
            self.assertIn("4", result.stdout)
            
        finally:
            if prompt_file.exists():
                prompt_file.unlink()

    def test_run_command_with_system_flag(self):
        """Test 'run' command with system flag."""
        prompt_file = SCRIPT_DIR / "temp_sys_prompt.md"
        prompt_file.write_text("What is 10+10?", encoding="utf-8")

        try:
            result = subprocess.run(
                [sys.executable, "prompt.py", "run", str(prompt_file), "-p", "local", "-s", "Answer in json"],
                capture_output=True,
                text=True,
                timeout=120,
                encoding="utf-8"
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
                [sys.executable, "prompt.py", "eval", str(test_dir), "-t", "1"],
                capture_output=True,
                text=True,
                timeout=60,
                encoding="utf-8"
            )

            self.assertEqual(result.returncode, 0, f"Eval failed: {result.stderr}")
            
        finally:
            # Cleanup
            import shutil
            shutil.rmtree(test_dir)

    def test_cove_command_local(self):
        """Test 'cove' command runs with local provider."""
        result = subprocess.run(
            [sys.executable, "prompt.py", "cove", "What is the capital of France?", "-p", "local", "-n", "1"],
            capture_output=True,
            text=True,
            timeout=120,
            encoding="utf-8"
        )
        
        self.assertEqual(result.returncode, 0)
        # Check for CoVe specific output markers
        self.assertIn("Draft Response", result.stdout)
        self.assertIn("Verification", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
