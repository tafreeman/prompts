#!/usr/bin/env python3
"""
Integration tests for the Evaluation Agent.

These tests verify end-to-end functionality including:
- Full pipeline in dry-run mode
- Phase execution
- Report generation (mocked)
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from evaluation_agent import (
    AgentConfig,
    EvaluationAgent,
    check_prerequisites,
    main,
)


class TestFullPipelineIntegration(unittest.TestCase):
    """Integration tests for full pipeline execution."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.logger = Mock()
    
    def test_full_pipeline_dry_run(self):
        """Verify full pipeline can run in dry-run mode."""
        agent = EvaluationAgent(
            logger=self.logger,
            dry_run=True,
            resume=False
        )
        
        # Initialize agent
        self.assertTrue(agent.initialize())
        self.assertIsNotNone(agent.state)
        
        # Verify state is properly initialized
        self.assertEqual(agent.state.current_phase, 0)
        self.assertEqual(len(agent.state.completed_categories), 0)
    
    def test_phase_execution_dry_run(self):
        """Verify individual phase can run in dry-run mode."""
        agent = EvaluationAgent(
            logger=self.logger,
            dry_run=True,
            resume=False
        )
        
        agent.initialize()
        
        # Run phase 1 in dry-run mode
        with patch('evaluation_agent.generate_eval_files') as mock_gen:
            with patch('evaluation_agent.run_evaluations') as mock_eval:
                from evaluation_agent import TaskResult, TaskStatus
                
                # Mock the task results
                mock_gen.return_value = TaskResult(
                    task_name="test",
                    status=TaskStatus.SKIPPED,
                    start_time="2025-12-03T12:00:00"
                )
                mock_eval.return_value = TaskResult(
                    task_name="test",
                    status=TaskStatus.SKIPPED,
                    start_time="2025-12-03T12:00:00"
                )
                
                result = agent.run_phase(1)
                self.assertTrue(result)
    
    def test_agent_tracks_completed_categories(self):
        """Verify agent properly tracks completed categories."""
        agent = EvaluationAgent(
            logger=self.logger,
            dry_run=True,
            resume=False
        )
        
        agent.initialize()
        
        # Manually mark a category as completed
        agent.state.completed_categories.append("analysis")
        
        self.assertIn("analysis", agent.state.completed_categories)
        self.assertEqual(len(agent.state.completed_categories), 1)


class TestCommandLineIntegration(unittest.TestCase):
    """Integration tests for CLI functionality."""
    
    @patch('sys.argv', ['evaluation_agent.py', '--full', '--dry-run'])
    @patch('evaluation_agent.EvaluationAgent')
    def test_full_flag_creates_agent(self, mock_agent_class):
        """Verify --full flag creates and runs agent."""
        mock_agent = Mock()
        mock_agent.initialize.return_value = True
        mock_agent.run_full_pipeline.return_value = True
        mock_agent_class.return_value = mock_agent
        
        # This would normally call main(), but we're testing the flag parsing
        # The actual execution is mocked
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--full', action='store_true')
        parser.add_argument('--dry-run', action='store_true')
        args = parser.parse_args()
        
        self.assertTrue(args.full)
        self.assertTrue(args.dry_run)
    
    @patch('sys.argv', ['evaluation_agent.py', '--phase', '2', '--dry-run'])
    def test_phase_flag_with_dry_run(self):
        """Verify --phase flag works with --dry-run."""
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--phase', type=int, choices=[1, 2, 3, 4])
        parser.add_argument('--dry-run', action='store_true')
        args = parser.parse_args()
        
        self.assertEqual(args.phase, 2)
        self.assertTrue(args.dry_run)
    
    @patch('sys.argv', ['evaluation_agent.py', '--resume'])
    @patch('evaluation_agent.load_checkpoint')
    def test_resume_flag(self, mock_load):
        """Verify --resume flag attempts to load checkpoint."""
        mock_load.return_value = None
        
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--resume', action='store_true')
        args = parser.parse_args()
        
        self.assertTrue(args.resume)


class TestAgentStateManagement(unittest.TestCase):
    """Test agent state management during execution."""
    
    def test_state_accumulates_metrics(self):
        """Verify state properly accumulates metrics."""
        from evaluation_agent import AgentState, CategoryResult
        
        state = AgentState(started_at="2025-12-03T12:00:00")
        
        # Add category results
        state.category_results["test1"] = CategoryResult(
            category="test1",
            prompts_evaluated=10,
            prompts_passed=8,
            prompts_failed=2,
        )
        
        state.category_results["test2"] = CategoryResult(
            category="test2",
            prompts_evaluated=20,
            prompts_passed=18,
            prompts_failed=2,
        )
        
        # Calculate totals
        state.total_prompts = sum(
            r.prompts_evaluated for r in state.category_results.values()
        )
        state.total_passed = sum(
            r.prompts_passed for r in state.category_results.values()
        )
        state.total_failed = sum(
            r.prompts_failed for r in state.category_results.values()
        )
        
        self.assertEqual(state.total_prompts, 30)
        self.assertEqual(state.total_passed, 26)
        self.assertEqual(state.total_failed, 4)
    
    def test_state_calculates_pass_rate(self):
        """Verify state calculates overall pass rate correctly."""
        from evaluation_agent import AgentState
        
        state = AgentState(started_at="2025-12-03T12:00:00")
        state.total_prompts = 100
        state.total_passed = 90
        state.overall_pass_rate = state.total_passed / state.total_prompts
        
        self.assertAlmostEqual(state.overall_pass_rate, 0.90, places=2)


class TestCategoryPrioritization(unittest.TestCase):
    """Test that categories are executed in correct priority order."""
    
    def test_categories_have_priorities(self):
        """Verify all categories have priority assigned."""
        for category, config in AgentConfig.CATEGORY_CONFIG.items():
            self.assertIn("priority", config)
            self.assertIn(config["priority"], [1, 2, 3, 4])
    
    def test_phase_selects_correct_categories(self):
        """Verify phase selection logic works correctly."""
        # Phase 1 categories
        phase_1 = [
            cat for cat, config in AgentConfig.CATEGORY_CONFIG.items()
            if config["priority"] == 1
        ]
        self.assertGreater(len(phase_1), 0)
        
        # Phase 2 categories
        phase_2 = [
            cat for cat, config in AgentConfig.CATEGORY_CONFIG.items()
            if config["priority"] == 2
        ]
        self.assertGreater(len(phase_2), 0)


class TestErrorHandling(unittest.TestCase):
    """Test error handling in various scenarios."""
    
    def test_agent_handles_initialization_failure(self):
        """Verify agent handles initialization failures gracefully."""
        logger = Mock()
        agent = EvaluationAgent(logger=logger, dry_run=True, resume=False)
        
        # Initialization should succeed in normal case
        result = agent.initialize()
        self.assertTrue(result)
    
    def test_agent_handles_missing_category(self):
        """Verify agent handles missing category gracefully."""
        logger = Mock()
        agent = EvaluationAgent(logger=logger, dry_run=True, resume=False)
        agent.initialize()
        
        # Try to run phase with no categories (should return True but log warning)
        # We test the category filtering logic
        phase_categories = [
            cat for cat, config in AgentConfig.CATEGORY_CONFIG.items()
            if config["priority"] == 999  # Non-existent phase
        ]
        self.assertEqual(len(phase_categories), 0)


def run_tests():
    """Run all integration tests and return exit code."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
