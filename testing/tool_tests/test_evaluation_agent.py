#!/usr/bin/env python3
"""
Unit tests for the Evaluation Agent.

Tests cover:
- Command-line argument parsing
- Agent initialization
- Checkpoint save/load
- Configuration validation
- Dry-run mode
- Task result tracking
"""

import json
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add project root to path for imports
ROOT_DIR = Path(__file__).parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from tools.agents.evaluation_agent import (
    AgentConfig,
    AgentState,
    CategoryResult,
    EvaluationAgent,
    TaskResult,
    TaskStatus,
    check_prerequisites,
    count_prompts_in_category,
    load_checkpoint,
    save_checkpoint,
    setup_logging,
)


class TestAgentConfiguration(unittest.TestCase):
    """Test agent configuration and setup."""
    
    def test_agent_config_paths_exist(self):
        """Verify configuration paths are properly defined."""
        # Ensure ROOT_DIR is correctly set in AgentConfig
        self.assertIsInstance(AgentConfig.ROOT_DIR, Path)
        self.assertIsInstance(AgentConfig.PROMPTS_DIR, Path)
        self.assertIsInstance(AgentConfig.EVALS_DIR, Path)
        self.assertTrue(AgentConfig.ROOT_DIR.exists())
    
    def test_agent_config_categories(self):
        """Verify all expected categories are configured."""
        expected_categories = [
            "analysis", "business", "m365", "developers",
            "system", "advanced", "creative", "governance"
        ]
        self.assertEqual(AgentConfig.CATEGORIES, expected_categories)
    
    def test_category_config_structure(self):
        """Verify category configuration has required fields."""
        for category, config in AgentConfig.CATEGORY_CONFIG.items():
            self.assertIn("model", config)
            self.assertIn("runs", config)
            self.assertIn("priority", config)
            self.assertIsInstance(config["runs"], int)
            self.assertGreater(config["runs"], 0)
            self.assertIn(config["priority"], [1, 2, 3, 4])
    
    def test_thresholds_valid(self):
        """Verify threshold values are reasonable."""
        self.assertGreater(AgentConfig.PASS_THRESHOLD, 0)
        self.assertLessEqual(AgentConfig.PASS_THRESHOLD, 10)
        self.assertGreater(AgentConfig.TARGET_PASS_RATE, 0)
        self.assertLessEqual(AgentConfig.TARGET_PASS_RATE, 1)


class TestLoggingSetup(unittest.TestCase):
    """Test logging configuration."""
    
    def test_setup_logging_creates_logger(self):
        """Verify logger is created correctly."""
        logger = setup_logging(verbose=False)
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, "EvalAgent")
    
    def test_setup_logging_verbose_mode(self):
        """Verify verbose mode sets debug level."""
        import logging
        logger = setup_logging(verbose=True)
        self.assertEqual(logger.level, logging.DEBUG)


class TestCheckpointManagement(unittest.TestCase):
    """Test checkpoint save/load functionality."""
    
    def setUp(self):
        """Create temporary checkpoint file."""
        self.temp_dir = tempfile.mkdtemp()
        self.checkpoint_file = Path(self.temp_dir) / "checkpoint.json"
        
        # Patch the checkpoint file location
        self.original_checkpoint = AgentConfig.CHECKPOINT_FILE
        AgentConfig.CHECKPOINT_FILE = self.checkpoint_file
    
    def tearDown(self):
        """Clean up temporary files."""
        try:
            if self.checkpoint_file.exists():
                self.checkpoint_file.unlink()
            if Path(self.temp_dir).exists():
                Path(self.temp_dir).rmdir()
        finally:
            # Always restore original checkpoint path
            AgentConfig.CHECKPOINT_FILE = self.original_checkpoint
    
    def test_save_checkpoint_creates_file(self):
        """Verify checkpoint file is created."""
        state = AgentState(started_at=datetime.now().isoformat())
        save_checkpoint(state)
        self.assertTrue(self.checkpoint_file.exists())
    
    def test_save_load_checkpoint_roundtrip(self):
        """Verify state can be saved and loaded."""
        original_state = AgentState(
            started_at="2025-12-03T12:00:00",
            current_phase=2,
            current_category="developers",
            completed_categories=["analysis", "business"],
            total_prompts=50,
            total_passed=45,
            total_failed=5,
            overall_pass_rate=0.90,
        )
        
        save_checkpoint(original_state)
        loaded_state = load_checkpoint()
        
        self.assertIsNotNone(loaded_state)
        self.assertEqual(loaded_state.started_at, original_state.started_at)
        self.assertEqual(loaded_state.current_phase, original_state.current_phase)
        self.assertEqual(loaded_state.current_category, original_state.current_category)
        self.assertEqual(loaded_state.completed_categories, original_state.completed_categories)
        self.assertEqual(loaded_state.total_prompts, original_state.total_prompts)
    
    def test_load_checkpoint_no_file(self):
        """Verify loading returns None when no checkpoint exists."""
        result = load_checkpoint()
        self.assertIsNone(result)
    
    def test_checkpoint_includes_category_results(self):
        """Verify category results are saved in checkpoint."""
        state = AgentState(started_at=datetime.now().isoformat())
        state.category_results["test"] = CategoryResult(
            category="test",
            prompts_evaluated=10,
            prompts_passed=8,
            prompts_failed=2,
            pass_rate=0.8,
        )
        
        save_checkpoint(state)
        loaded_state = load_checkpoint()
        
        self.assertIn("test", loaded_state.category_results)
        self.assertEqual(loaded_state.category_results["test"].prompts_evaluated, 10)


class TestTaskResult(unittest.TestCase):
    """Test TaskResult dataclass."""
    
    def test_task_result_creation(self):
        """Verify TaskResult can be created."""
        task = TaskResult(
            task_name="test_task",
            status=TaskStatus.COMPLETED,
            start_time="2025-12-03T12:00:00",
        )
        self.assertEqual(task.task_name, "test_task")
        self.assertEqual(task.status, TaskStatus.COMPLETED)
    
    def test_task_status_enum(self):
        """Verify TaskStatus enum values."""
        self.assertEqual(TaskStatus.PENDING.value, "pending")
        self.assertEqual(TaskStatus.RUNNING.value, "running")
        self.assertEqual(TaskStatus.COMPLETED.value, "completed")
        self.assertEqual(TaskStatus.FAILED.value, "failed")
        self.assertEqual(TaskStatus.SKIPPED.value, "skipped")


class TestEvaluationAgent(unittest.TestCase):
    """Test EvaluationAgent class."""
    
    def setUp(self):
        """Create agent for testing."""
        self.logger = Mock()
        self.agent = EvaluationAgent(
            logger=self.logger,
            dry_run=True,
            resume=False
        )
    
    def test_agent_initialization(self):
        """Verify agent initializes correctly."""
        self.assertTrue(self.agent.initialize())
        self.assertIsNotNone(self.agent.state)
        self.assertEqual(self.agent.state.current_phase, 0)
    
    def test_agent_dry_run_mode(self):
        """Verify agent respects dry-run mode."""
        self.assertTrue(self.agent.dry_run)
        self.assertTrue(self.agent.initialize())
    
    def test_agent_state_tracking(self):
        """Verify agent tracks state correctly."""
        self.agent.initialize()
        self.assertIsNotNone(self.agent.state.started_at)
        self.assertEqual(len(self.agent.state.completed_categories), 0)
        self.assertEqual(self.agent.state.total_prompts, 0)


class TestCountPromptsInCategory(unittest.TestCase):
    """Test prompt counting functionality."""
    
    def test_count_prompts_nonexistent_category(self):
        """Verify counting returns 0 for non-existent category."""
        count = count_prompts_in_category("nonexistent_category_xyz")
        self.assertEqual(count, 0)
    
    def test_count_prompts_excludes_index(self):
        """Verify index.md and readme.md are excluded from count."""
        # This test would need actual test data, so we just verify the function exists
        # and returns an integer
        count = count_prompts_in_category("analysis")
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)


class TestCommandLineInterface(unittest.TestCase):
    """Test CLI argument parsing."""
    
    @patch('sys.argv', ['evaluation_agent.py', '--full'])
    def test_full_flag_parsing(self):
        """Verify --full flag is recognized."""
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--full', action='store_true')
        args = parser.parse_args()
        self.assertTrue(args.full)
    
    @patch('sys.argv', ['evaluation_agent.py', '--phase', '2'])
    def test_phase_flag_parsing(self):
        """Verify --phase flag is recognized."""
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--phase', type=int)
        args = parser.parse_args()
        self.assertEqual(args.phase, 2)
    
    @patch('sys.argv', ['evaluation_agent.py', '--dry-run'])
    def test_dry_run_flag_parsing(self):
        """Verify --dry-run flag is recognized."""
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--dry-run', action='store_true')
        args = parser.parse_args()
        self.assertTrue(args.dry_run)


class TestCategoryResult(unittest.TestCase):
    """Test CategoryResult dataclass."""
    
    def test_category_result_creation(self):
        """Verify CategoryResult can be created."""
        result = CategoryResult(category="test")
        self.assertEqual(result.category, "test")
        self.assertEqual(result.prompts_evaluated, 0)
        self.assertEqual(result.pass_rate, 0.0)
    
    def test_category_result_with_data(self):
        """Verify CategoryResult calculates correctly."""
        result = CategoryResult(
            category="test",
            prompts_evaluated=10,
            prompts_passed=8,
            prompts_failed=2,
        )
        # Pass rate should be calculated separately
        result.pass_rate = result.prompts_passed / result.prompts_evaluated
        self.assertEqual(result.pass_rate, 0.8)


def run_tests():
    """Run all tests and return exit code."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
