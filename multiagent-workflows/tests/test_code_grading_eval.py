"""Tests for code grading evaluation with the new similarity to golden
criterion."""


class TestCodeGradingEvaluation:
    """Test code grading evaluation functionality."""

    def test_similarity_criterion_in_rubric(self):
        """Test that the new similarity criterion is in the rubric."""
        from multiagent_workflows.core.evaluator import WorkflowEvaluator

        evaluator = WorkflowEvaluator()
        rubric = evaluator.rubrics.get("rubrics", {}).get("code_grading", {})

        # Check that static_analysis category exists
        static_analysis = rubric.get("categories", {}).get("static_analysis", {})
        assert static_analysis, "static_analysis category should exist"

        # Check that Code Similarity to Golden criterion exists
        criteria = static_analysis.get("criteria", [])
        similarity_criterion = None
        for criterion in criteria:
            if criterion.get("name") == "Code Similarity to Golden":
                similarity_criterion = criterion
                break

        assert similarity_criterion, "Code Similarity to Golden criterion should exist"
        assert similarity_criterion.get("max_points") == 5, "Should have 5 max points"

    def test_similarity_criterion_scoring(self):
        """Test that the similarity criterion is scored correctly."""
        from multiagent_workflows.core.evaluator import WorkflowEvaluator

        evaluator = WorkflowEvaluator()

        # Test identical outputs
        output = {"code": "print('hello')"}
        golden = {"code": "print('hello')"}

        # Score the criterion directly
        score = evaluator._score_criterion(output, golden, "similarity_golden", {})
        assert score == 100.0, "Identical outputs should score 100%"

        # Test different outputs
        output = {"code": "print('hello')"}
        golden = {"code": "print('world')"}

        score = evaluator._score_criterion(output, golden, "similarity_golden", {})
        assert 0 <= score <= 100, "Score should be between 0 and 100"
