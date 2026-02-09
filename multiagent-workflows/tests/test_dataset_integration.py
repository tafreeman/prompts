import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add repo root to path
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

from tools.agents.benchmarks.datasets import BENCHMARK_DEFINITIONS, DataSource
from tools.agents.benchmarks.loader import load_benchmark


class TestDatasetIntegration(unittest.TestCase):
    """Test that the dataset tool correctly links to authoritative sources and
    can fetch fresh data."""

    def test_humaneval_source_definition(self):
        """Verify HumanEval is configured to pull from OpenAI's HuggingFace
        repo."""
        benchmark = BENCHMARK_DEFINITIONS.get("humaneval")
        self.assertIsNotNone(benchmark)
        self.assertEqual(benchmark.source, DataSource.HUGGINGFACE)
        self.assertEqual(benchmark.source_url, "openai/openai_humaneval")
        self.assertEqual(benchmark.benchmark_type.value, "function_level")

    def test_swebench_lite_source_definition(self):
        """Verify SWE-bench Lite is configured to pull from Princeton-NLP's
        repo."""
        benchmark = BENCHMARK_DEFINITIONS.get("swe-bench-lite")
        self.assertIsNotNone(benchmark)
        self.assertEqual(benchmark.source, DataSource.HUGGINGFACE)
        self.assertEqual(benchmark.source_url, "princeton-nlp/SWE-bench_Lite")
        self.assertEqual(benchmark.benchmark_type.value, "software_engineering")

    @patch("tools.agents.benchmarks.loader._load_from_huggingface")
    @patch("tools.agents.benchmarks.loader._check_huggingface_available")
    def test_fresh_fetch_invocation(self, mock_check, mock_load):
        """Verify that attempting to load with use_cache=False triggers the
        direct loader for the specific source."""
        mock_check.return_value = True
        mock_load.return_value = []

        # Attempt to load HumanEval without cache
        load_benchmark("humaneval", use_cache=False)

        # Check that the direct loader was called
        mock_load.assert_called_once()

        # Check that it was passed the correct benchmark definition
        args, _ = mock_load.call_args
        benchmark_arg = args[0]
        self.assertEqual(benchmark_arg.id, "humaneval")
        self.assertEqual(benchmark_arg.source_url, "openai/openai_humaneval")

        print(
            "\n✓ Verified tool attempts to fetch fresh data from openai/openai_humaneval"
        )

    @patch("tools.agents.benchmarks.loader.urllib.request.urlopen")
    def test_github_source_link(self, mock_urlopen):
        """Verify that GitHub-sourced benchmarks link to the correct API
        endpoint."""
        # Mock response setup
        mock_list_response = MagicMock()
        mock_list_response.read.return_value = (
            b'[{"name": "task_1.json", "download_url": "http://github.com/d/t1.json"}]'
        )
        mock_list_response.__enter__.return_value = mock_list_response

        mock_file_response = MagicMock()
        mock_file_response.read.return_value = b'{"id": "t1", "prompt": "p"}'
        mock_file_response.__enter__.return_value = mock_file_response

        # Return list first, then file
        mock_urlopen.side_effect = [mock_list_response, mock_file_response]

        # Attempt to load a GitHub-based benchmark (CodeClash)
        load_benchmark("codeclash", limit=1, use_cache=False)

        # Verify the URL requested matches the repo structure
        # We expect at least one call. The first one should be the API call.
        self.assertTrue(mock_urlopen.called)
        first_call_args = mock_urlopen.call_args_list[0]
        req = first_call_args[0][0]  # first arg of first call

        # codeclash source_url is "codeclash-eval/codeclash"
        self.assertIn("api.github.com/repos/codeclash-eval/codeclash", req.full_url)
        print("\n✓ Verified tool links to correct GitHub API endpoint")


if __name__ == "__main__":
    unittest.main()
