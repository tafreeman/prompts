#!/usr/bin/env python3
"""End-to-end test for the Evaluation Agent with mocked prerequisites.

This test verifies the full pipeline works correctly when prerequisites
are met.
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

# Add project root to path for imports
ROOT_DIR = Path(__file__).parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from tools.agents.evaluation_agent import (
    AgentState,
    CategoryResult,
    EvaluationAgent,
    TaskResult,
    TaskStatus,
)


class TestEndToEndExecution(unittest.TestCase):
    """End-to-end test with mocked external dependencies."""

    @patch("tools.evaluation_agent.check_prerequisites")
    @patch("tools.evaluation_agent.count_prompts_in_category")
    @patch("tools.evaluation_agent.generate_eval_files")
    @patch("tools.evaluation_agent.run_evaluations")
    @patch("tools.evaluation_agent.parse_evaluation_results")
    @patch("tools.evaluation_agent.generate_improvement_plan")
    @patch("tools.evaluation_agent.generate_final_report")
    @patch("tools.evaluation_agent.save_checkpoint")
    @patch("tools.evaluation_agent.clear_checkpoint")
    def test_full_pipeline_dry_run_e2e(
        self,
        mock_clear,
        mock_save,
        mock_report,
        mock_improve,
        mock_parse,
        mock_run_evals,
        mock_gen_files,
        mock_count,
        mock_prereqs,
    ):
        """Test full pipeline execution in dry-run mode."""
        # Mock prerequisite check to pass
        mock_prereqs.return_value = True

        # Mock prompt counting
        mock_count.return_value = 5

        # Mock task results (dry-run returns SKIPPED)
        skip_task = TaskResult(
            task_name="test",
            status=TaskStatus.SKIPPED,
            start_time="2025-12-03T12:00:00",
        )
        mock_gen_files.return_value = skip_task
        mock_run_evals.return_value = skip_task
        mock_improve.return_value = skip_task
        mock_report.return_value = skip_task

        # Mock category results
        mock_parse.return_value = CategoryResult(
            category="test",
            prompts_evaluated=5,
            prompts_passed=4,
            prompts_failed=1,
            pass_rate=0.8,
        )

        # Create agent
        logger = Mock()
        agent = EvaluationAgent(logger=logger, dry_run=True, resume=False)

        # Initialize and run
        self.assertTrue(agent.initialize())
        result = agent.run_full_pipeline()

        # Verify results
        self.assertTrue(result)
        self.assertEqual(agent.state.status, "completed")

        # Verify prerequisite check was called
        mock_prereqs.assert_called_once()

        # Verify checkpoint was saved (at least once during execution)
        self.assertTrue(mock_save.called)

        # Verify final report was generated
        mock_report.assert_called_once()

    @patch("tools.evaluation_agent.check_prerequisites")
    @patch("tools.evaluation_agent.generate_eval_files")
    @patch("tools.evaluation_agent.run_evaluations")
    @patch("tools.evaluation_agent.save_checkpoint")
    def test_single_phase_execution(
        self,
        mock_save,
        mock_run_evals,
        mock_gen_files,
        mock_prereqs,
    ):
        """Test single phase execution."""
        # Mock prerequisite check
        mock_prereqs.return_value = True

        # Mock task results
        complete_task = TaskResult(
            task_name="test",
            status=TaskStatus.COMPLETED,
            start_time="2025-12-03T12:00:00",
        )
        mock_gen_files.return_value = complete_task
        mock_run_evals.return_value = complete_task

        # Create agent
        logger = Mock()
        agent = EvaluationAgent(logger=logger, dry_run=True, resume=False)

        # Initialize and run phase 1
        agent.initialize()
        result = agent.run_phase(1)

        # Verify results
        self.assertTrue(result)

    @patch("tools.evaluation_agent.load_checkpoint")
    def test_resume_from_checkpoint(self, mock_load):
        """Test resuming from a checkpoint."""
        # Mock checkpoint loading
        mock_state = AgentState(
            started_at="2025-12-03T10:00:00",
            current_phase=2,
            completed_categories=["analysis", "business"],
            total_prompts=20,
            total_passed=18,
            total_failed=2,
        )
        mock_load.return_value = mock_state

        # Create agent with resume=True
        logger = Mock()
        agent = EvaluationAgent(logger=logger, dry_run=True, resume=True)

        # Initialize
        result = agent.initialize()

        # Verify checkpoint was loaded
        self.assertTrue(result)
        mock_load.assert_called_once()
        self.assertEqual(agent.state.current_phase, 2)
        self.assertEqual(len(agent.state.completed_categories), 2)

    def test_command_line_interface(self):
        """Test that command line interface is properly structured."""
        import argparse

        # Create parser like main() does
        parser = argparse.ArgumentParser()
        parser.add_argument("--full", action="store_true")
        parser.add_argument("--phase", type=int, choices=[1, 2, 3, 4])
        parser.add_argument("--resume", action="store_true")
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--verbose", "-v", action="store_true")
        parser.add_argument("--clear-checkpoint", action="store_true")

        # Test various argument combinations
        test_cases = [
            (["--full"], {"full": True}),
            (["--phase", "2"], {"phase": 2}),
            (["--resume"], {"resume": True}),
            (["--dry-run"], {"dry_run": True}),
            (["--verbose"], {"verbose": True}),
            (["--full", "--dry-run"], {"full": True, "dry_run": True}),
            (["--phase", "1", "--verbose"], {"phase": 1, "verbose": True}),
        ]

        for args_list, expected in test_cases:
            args = parser.parse_args(args_list)
            for key, value in expected.items():
                self.assertEqual(getattr(args, key), value)


def run_tests():
    """Run all end-to-end tests and return exit code."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
