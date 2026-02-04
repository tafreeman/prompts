import unittest
from unittest.mock import patch

from tools.dynamic_eval_manager import manage_evaluations


class TestDynamicEvalManager(unittest.TestCase):
    @patch("tools.dynamic_eval_manager.psutil.cpu_percent")
    @patch("tools.dynamic_eval_manager.psutil.virtual_memory")
    @patch("tools.dynamic_eval_manager.evaluate_prompt")
    def test_manage_evaluations(
        self, mock_evaluate_prompt, mock_virtual_memory, mock_cpu_percent
    ):
        # Mock system performance metrics
        mock_cpu_percent.side_effect = [50, 80, 60, 50]  # Simulate CPU usage
        mock_virtual_memory.return_value.percent = 50  # Simulate memory usage

        # Mock evaluate_prompt to return a predictable result
        mock_evaluate_prompt.side_effect = lambda prompt_id: f"Result for {prompt_id}"

        # Define test parameters
        prompts = [f"prompt_{i}" for i in range(1, 6)]  # 5 prompts
        max_concurrent_requests = 2
        cpu_threshold = 75
        memory_threshold = 70

        # Run the evaluation manager
        results = manage_evaluations(
            prompts, max_concurrent_requests, cpu_threshold, memory_threshold
        )

        # Assertions
        self.assertEqual(len(results), len(prompts))  # Ensure all prompts are evaluated
        self.assertListEqual(
            results, [f"Result for prompt_{i}" for i in range(1, 6)]
        )  # Check results
        mock_evaluate_prompt.assert_called()  # Ensure evaluate_prompt was called
        self.assertEqual(
            mock_evaluate_prompt.call_count, len(prompts)
        )  # Called once per prompt

    @patch("tools.dynamic_eval_manager.psutil.cpu_percent")
    @patch("tools.dynamic_eval_manager.psutil.virtual_memory")
    def test_system_monitoring(self, mock_virtual_memory, mock_cpu_percent):
        from tools.dynamic_eval_manager import monitor_system

        # Mock system performance metrics
        mock_cpu_percent.return_value = 85
        mock_virtual_memory.return_value.percent = 65

        # Run the system monitor
        cpu_usage, memory_usage = monitor_system()

        # Assertions
        self.assertEqual(cpu_usage, 85)
        self.assertEqual(memory_usage, 65)


if __name__ == "__main__":
    unittest.main()
