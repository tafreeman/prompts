"""Tests for the benchmark loader utility."""

import json
import unittest
from unittest.mock import MagicMock, patch, mock_open
from pathlib import Path

# Adjust path if needed to ensure tools is importable
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.agents.benchmarks.loader import (
    load_benchmark,
    BenchmarkTask,
    DataSource,
    BENCHMARK_DEFINITIONS,
    BenchmarkDefinition
)

class TestBenchmarkLoader(unittest.TestCase):

    def setUp(self):
        # Create a mock benchmark definition for testing
        self.mock_config = {
            "test-hf": BenchmarkDefinition(
                id="test-hf",
                name="Test HF",
                description="Test HuggingFace",
                source=DataSource.HUGGINGFACE,
                source_url="org/repo",
                source_config={"split": "test"},
                size=10,
                benchmark_type=MagicMock()
            ),
            "test-gh": BenchmarkDefinition(
                id="test-gh",
                name="Test GitHub",
                description="Test GitHub",
                source=DataSource.GITHUB,
                source_url="org/repo",
                source_config={"tasks_path": "tasks/"},
                size=5,
                benchmark_type=MagicMock()
            )
        }
        self.patcher = patch.dict(BENCHMARK_DEFINITIONS, self.mock_config, clear=True)
        self.patcher.start()
        
        # Mock print to avoid unicode errors
        self.print_patcher = patch("builtins.print")
        self.mock_print = self.print_patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.print_patcher.stop()

    def test_load_huggingface(self):
        # Create a mock datasets module
        mock_datasets_module = MagicMock()
        mock_ds = MagicMock()
        mock_item = {
            "instance_id": "swe-1",
            "problem_statement": "Fix bug",
            "repo": "test/repo",
            "base_commit": "abc",
            "patch": "diff",
            "test_patch": "test_diff"
        }
        mock_ds.__iter__.return_value = [mock_item]
        mock_ds.__len__.return_value = 1
        mock_ds.select.return_value = mock_ds
        
        mock_datasets_module.load_dataset.return_value = mock_ds
        
        # Patch sys.modules so 'import datasets' works inside the function
        with patch.dict("sys.modules", {"datasets": mock_datasets_module}):
            # We also need _check_huggingface_available to return True
            # It tries to import datasets, which should work now due to sys.modules patch
            
            # Setup config ID
            self.mock_config["test-hf"].id = "swe-bench-lite"
            
            tasks = load_benchmark("test-hf", use_cache=False)
            
            self.assertEqual(len(tasks), 1)
            self.assertEqual(tasks[0].task_id, "swe-1")

    @patch("tools.agents.benchmarks.loader.urllib.request.urlopen")
    def test_load_github(self, mock_urlopen):
        # Mock file list response
        file_list = [
            {"name": "task1.json", "download_url": "http://example.com/task1.json"}
        ]
        
        # Mock task content response
        task_content = {
            "id": "task1",
            "prompt": "Do this",
            "solution": "Done",
            "language": "python"
        }

        # Context manager mock
        cm = MagicMock()
        cm.__enter__.return_value = cm
        cm.read.side_effect = [
            json.dumps(file_list).encode("utf-8"), # First call: list files
            json.dumps(task_content).encode("utf-8") # Second call: get file
        ]
        mock_urlopen.return_value = cm
        
        tasks = load_benchmark("test-gh", use_cache=False)
        
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].task_id, "task1")
        self.assertEqual(tasks[0].prompt, "Do this")

    @patch("tools.agents.benchmarks.loader.get_cache_path")
    @patch("tools.agents.benchmarks.loader.is_cache_valid")
    @patch("builtins.open", new_callable=mock_open)
    def test_cache_logic(self, mock_file, mock_is_valid, mock_get_path):
        # Test loading FROM cache
        mock_is_valid.return_value = True
        
        cached_data = {
            "data": [
                {
                    "task_id": "cached-1",
                    "benchmark_id": "test-hf",
                    "prompt": "Cached prompt"
                }
            ]
        }
        mock_file.return_value.read.return_value = json.dumps(cached_data)
        
        tasks = load_benchmark("test-hf", use_cache=True)
        
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].task_id, "cached-1")
        # Ensure we didn't call external loaders (no mocks setup for them would fail otherwise)

if __name__ == "__main__":
    unittest.main()
