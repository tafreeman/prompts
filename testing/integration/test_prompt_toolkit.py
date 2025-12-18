#!/usr/bin/env python3
"""
Unit Tests for Unified Prompt Toolkit
======================================

Tests covering:
- Parameter handling (temperature, max_tokens)
- Provider routing
- Error handling
- CLI argument parsing
"""

import sys
import unittest
import os
from unittest.mock import patch
from pathlib import Path

# Add project root to path
REPO_ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "tools"))


class TestLLMClientProviderRouting(unittest.TestCase):
    """Test that provider prefixes route to correct methods."""

    def test_local_prefix_routes_to_local(self):
        """Test local: prefix routes to _call_local."""
        from tools.llm_client import LLMClient
        
        with patch.object(LLMClient, '_call_local', return_value="local response") as mock:
            LLMClient.generate_text("local:phi4mini", "test prompt")
            mock.assert_called_once()
            # Verify args were passed
            args, kwargs = mock.call_args
            self.assertEqual(args[0], "local:phi4mini")
            self.assertEqual(args[1], "test prompt")

    def test_azure_prefix_routes_to_azure(self):
        """Test azure-foundry: prefix routes to _call_azure_foundry."""
        from tools.llm_client import LLMClient
        
        with patch.object(LLMClient, '_call_azure_foundry', return_value="azure response") as mock:
            LLMClient.generate_text("azure-foundry:phi4mini", "test prompt")
            mock.assert_called_once()

    def test_gh_prefix_routes_to_github(self):
        """Test gh: prefix routes to _call_github_models."""
        from tools.llm_client import LLMClient
        
        with patch.object(LLMClient, '_call_github_models', return_value="gh response") as mock:
            LLMClient.generate_text("gh:gpt-4o-mini", "test prompt")
            mock.assert_called_once()

    def test_gemini_routes_to_gemini(self):
        """Test gemini in name routes to _call_gemini."""
        from tools.llm_client import LLMClient
        
        with patch.object(LLMClient, '_call_gemini', return_value="gemini response") as mock:
            LLMClient.generate_text("gemini-1.5-flash", "test prompt")
            mock.assert_called_once()

    def test_claude_routes_to_claude(self):
        """Test claude in name routes to _call_claude."""
        from tools.llm_client import LLMClient
        
        with patch.object(LLMClient, '_call_claude', return_value="claude response") as mock:
            LLMClient.generate_text("claude-3-sonnet", "test prompt")
            mock.assert_called_once()

    def test_gpt_routes_to_openai(self):
        """Test gpt in name routes to _call_openai."""
        from tools.llm_client import LLMClient
        
        with patch.object(LLMClient, '_call_openai', return_value="openai response") as mock:
            LLMClient.generate_text("gpt-4o", "test prompt")
            mock.assert_called_once()

    def test_unknown_provider_returns_error(self):
        """Test unknown provider returns error message."""
        from tools.llm_client import LLMClient
        
        result = LLMClient.generate_text("unknown-model", "test prompt")
        self.assertIn("Unknown model", result)


class TestLLMClientParameterHandling(unittest.TestCase):
    """Test that temperature and max_tokens are passed correctly."""

    def test_local_receives_temperature_and_max_tokens(self):
        """Test _call_local receives temperature and max_tokens."""
        from tools.llm_client import LLMClient
        
        with patch.object(LLMClient, '_call_local', return_value="response") as mock:
            LLMClient.generate_text("local:phi4mini", "prompt", None, 0.5, 1000)
            args, kwargs = mock.call_args
            self.assertEqual(args[3], 0.5)  # temperature
            self.assertEqual(args[4], 1000)  # max_tokens

    def test_azure_receives_temperature_and_max_tokens(self):
        """Test _call_azure_foundry receives temperature and max_tokens."""
        from tools.llm_client import LLMClient
        
        with patch.object(LLMClient, '_call_azure_foundry', return_value="response") as mock:
            LLMClient.generate_text("azure-foundry:phi4mini", "prompt", None, 0.3, 2000)
            args, kwargs = mock.call_args
            self.assertEqual(args[3], 0.3)
            self.assertEqual(args[4], 2000)

    def test_openai_receives_temperature_and_max_tokens(self):
        """Test _call_openai receives temperature and max_tokens."""
        from tools.llm_client import LLMClient
        
        with patch.object(LLMClient, '_call_openai', return_value="response") as mock:
            LLMClient.generate_text("gpt-4o", "prompt", None, 1.0, 8000)
            args, kwargs = mock.call_args
            self.assertEqual(args[3], 1.0)
            self.assertEqual(args[4], 8000)

    def test_default_temperature(self):
        """Test default temperature is 0.7."""
        from tools.llm_client import LLMClient
        
        with patch.object(LLMClient, '_call_local', return_value="response") as mock:
            LLMClient.generate_text("local:phi4mini", "prompt")
            args, kwargs = mock.call_args
            self.assertEqual(args[3], 0.7)  # default temperature

    def test_default_max_tokens(self):
        """Test default max_tokens is 4096."""
        from tools.llm_client import LLMClient
        
        with patch.object(LLMClient, '_call_local', return_value="response") as mock:
            LLMClient.generate_text("local:phi4mini", "prompt")
            args, kwargs = mock.call_args
            self.assertEqual(args[4], 4096)  # default max_tokens


class TestLLMClientErrorHandling(unittest.TestCase):
    """Test error handling for missing API keys and invalid providers."""

    def test_azure_missing_api_key(self):
        """Test Azure returns error when API key missing."""
        from tools.llm_client import LLMClient
        
        with patch.dict(os.environ, {}, clear=True):
            # Remove any existing key
            os.environ.pop('AZURE_FOUNDRY_API_KEY', None)
            result = LLMClient.generate_text("azure-foundry:phi4mini", "test")
            self.assertIn("Error", result)

    def test_openai_missing_api_key(self):
        """Test OpenAI returns error when API key missing."""
        from tools.llm_client import LLMClient
        
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop('OPENAI_API_KEY', None)
            result = LLMClient.generate_text("gpt-4o", "test")
            self.assertIn("Error", result)

    def test_exception_handling_returns_error_message(self):
        """Test that exceptions are caught and returned as error messages."""
        from tools.llm_client import LLMClient
        
        with patch.object(LLMClient, '_call_local', side_effect=Exception("Test error")):
            result = LLMClient.generate_text("local:phi4mini", "test")
            self.assertIn("Error", result)
            self.assertIn("Test error", result)


class TestCLIArgumentParsing(unittest.TestCase):
    """Test CLI argument parsing in prompt.py."""

    def setUp(self):
        """Import parse_args from prompt.py."""
        # Import the module - use resolve() to ensure absolute path
        import importlib.util
        prompt_path = (REPO_ROOT / "prompt.py").resolve()
        spec = importlib.util.spec_from_file_location("prompt", prompt_path)
        self.prompt_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.prompt_module)
        self.parse_args = self.prompt_module.parse_args

    def test_parse_run_command(self):
        """Test parsing run command with file."""
        result = self.parse_args(["run", "test.md"])
        self.assertEqual(result["command"], "run")
        self.assertEqual(result["args"], ["test.md"])

    def test_parse_provider_short_option(self):
        """Test parsing -p provider option."""
        result = self.parse_args(["run", "test.md", "-p", "local"])
        self.assertEqual(result["options"]["provider"], "local")

    def test_parse_provider_long_option(self):
        """Test parsing --provider option."""
        result = self.parse_args(["run", "test.md", "--provider", "github"])
        self.assertEqual(result["options"]["provider"], "github")

    def test_parse_temperature(self):
        """Test parsing --temperature option."""
        result = self.parse_args(["run", "test.md", "--temperature", "0.5"])
        self.assertEqual(result["options"]["temperature"], "0.5")

    def test_parse_max_tokens(self):
        """Test parsing --max-tokens option."""
        result = self.parse_args(["run", "test.md", "--max-tokens", "4000"])
        self.assertEqual(result["options"]["max-tokens"], "4000")

    def test_parse_tier_short_option(self):
        """Test parsing -t tier option."""
        result = self.parse_args(["eval", "prompts/", "-t", "3"])
        self.assertEqual(result["command"], "eval")
        self.assertEqual(result["options"]["tier"], "3")

    def test_parse_output_option(self):
        """Test parsing -o output option."""
        result = self.parse_args(["eval", "prompts/", "-o", "results.json"])
        self.assertEqual(result["options"]["output"], "results.json")

    def test_parse_system_option(self):
        """Test parsing -s system option."""
        result = self.parse_args(["run", "test.md", "-s", "You are helpful"])
        self.assertEqual(result["options"]["system"], "You are helpful")

    def test_parse_cove_command(self):
        """Test parsing cove command with question."""
        result = self.parse_args(["cove", "What", "is", "Python?"])
        self.assertEqual(result["command"], "cove")
        self.assertEqual(result["args"], ["What", "is", "Python?"])

    def test_parse_questions_option(self):
        """Test parsing -n questions option."""
        result = self.parse_args(["cove", "question", "-n", "10"])
        self.assertEqual(result["options"]["questions"], "10")

    def test_parse_verbose_flag(self):
        """Test parsing -v verbose flag."""
        result = self.parse_args(["run", "test.md", "-v"])
        self.assertEqual(result["options"]["verbose"], True)

    def test_parse_multiple_options(self):
        """Test parsing multiple options together."""
        result = self.parse_args([
            "run", "test.md", 
            "-p", "azure", 
            "-m", "phi4mini",
            "--temperature", "0.3",
            "--max-tokens", "2000",
            "-s", "Be concise"
        ])
        self.assertEqual(result["options"]["provider"], "azure")
        self.assertEqual(result["options"]["model"], "phi4mini")
        self.assertEqual(result["options"]["temperature"], "0.3")
        self.assertEqual(result["options"]["max-tokens"], "2000")
        self.assertEqual(result["options"]["system"], "Be concise")


class TestPromptModuleFunctions(unittest.TestCase):
    """Test prompt.py module functions."""

    def setUp(self):
        """Import prompt module."""
        import importlib.util
        prompt_path = (REPO_ROOT / "prompt.py").resolve()
        spec = importlib.util.spec_from_file_location("prompt", prompt_path)
        self.prompt_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.prompt_module)

    def test_providers_dict_exists(self):
        """Test PROVIDERS dictionary exists and has expected providers."""
        providers = self.prompt_module.PROVIDERS
        self.assertIn("local", providers)
        self.assertIn("gh", providers)
        self.assertIn("azure", providers)
        self.assertIn("openai", providers)

    def test_tiers_dict_exists(self):
        """Test TIERS dictionary exists and has expected tiers."""
        tiers = self.prompt_module.TIERS
        self.assertEqual(len(tiers), 8)  # Tiers 0-7 including Windows AI
        self.assertIn(0, tiers)
        self.assertIn(7, tiers)  # Windows AI tier


if __name__ == "__main__":
    # Run tests with verbosity
    unittest.main(verbosity=2)
