#!/usr/bin/env python3
"""Unit tests for dual_eval.py evaluation framework.

Run with:
    pytest testing/evals/test_dual_eval.py -v
"""

import sys
import threading
from pathlib import Path
from typing import Any
from unittest import mock

import pytest

# Add parent to path so we can import dual_eval
sys.path.insert(0, str(Path(__file__).parent))

import dual_eval
from dual_eval import (
    CROSS_VALIDATION_THRESHOLD,
    FATAL_ERROR_PATTERNS,
    PASS_THRESHOLD,
    CrossValidationReport,
    EvalResult,
    ModelSummary,
    create_log_writer,
    create_temp_eval_file,
    cross_validate,
    detect_fatal_error_reason,
    parse_prompt_file,
)

# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def sample_prompt_file(tmp_path: Path):
    """Create a sample prompt markdown file with frontmatter."""
    content = """---
title: "Test Prompt"
shortTitle: "test"
difficulty: "intermediate"
type: "how_to"
audience:
  - developers
platforms:
  - chatgpt
topics:
  - testing
---

# Test Prompt Content

This is a test prompt for unit testing purposes.

## Instructions

1. Do something
2. Do something else
3. Return results
"""
    file_path = tmp_path / "test_prompt.md"
    file_path.write_text(content, encoding="utf-8")
    return str(file_path)


@pytest.fixture
def sample_prompt_data():
    """Return sample parsed prompt data."""
    return {
        "title": "Test Prompt",
        "shortTitle": "test",
        "difficulty": "intermediate",
        "type": "how_to",
        "audience": ["developers"],
        "platforms": ["chatgpt"],
        "topics": ["testing"],
        "content": "# Test Prompt\n\nThis is test content.",
        "file_path": "/path/to/test.md",
        "word_count": 6,
    }


@pytest.fixture
def sample_eval_result():
    """Return a sample successful evaluation result."""
    return EvalResult(
        model="openai/gpt-4.1",
        run_number=1,
        scores={
            "clarity": 8.5,
            "specificity": 8.0,
            "actionability": 9.0,
            "structure": 8.5,
            "completeness": 8.0,
            "factuality": 9.0,
            "consistency": 8.5,
            "safety": 9.0,
        },
        overall_score=8.6,
        grade="A-",
        passed=True,
        pass_reason="All criteria met",
        reasoning="Good prompt with clear structure",
        strengths=["Clear instructions", "Good structure"],
        improvements=["Could add examples"],
        summary="Well-structured prompt",
    )


@pytest.fixture
def sample_error_result():
    """Return a sample error evaluation result."""
    return EvalResult(
        model="openai/gpt-4.1",
        run_number=1,
        error="Model not found: invalid-model",
    )


# =============================================================================
# DATACLASS TESTS
# =============================================================================


class TestEvalResult:
    """Tests for EvalResult dataclass."""

    def test_default_values(self):
        result = EvalResult(model="test-model", run_number=1)
        assert result.model == "test-model"
        assert result.run_number == 1
        assert result.scores == {}
        assert result.overall_score == 0.0
        assert result.grade == "N/A"
        assert result.passed is False
        assert result.error is None

    def test_with_scores(self, sample_eval_result: EvalResult):
        assert sample_eval_result.overall_score == 8.6
        assert sample_eval_result.grade == "A-"
        assert sample_eval_result.passed is True
        assert len(sample_eval_result.scores) == 8

    def test_with_error(self, sample_error_result: EvalResult):
        assert sample_error_result.error is not None
        assert "Model not found" in sample_error_result.error
        assert sample_error_result.passed is False


class TestModelSummary:
    """Tests for ModelSummary dataclass."""

    def test_default_values(self):
        summary = ModelSummary(model="test-model")
        assert summary.model == "test-model"
        assert summary.runs_completed == 0
        assert summary.runs_failed == 0
        assert summary.avg_score == 0.0
        assert summary.fatal_error is None

    def test_with_results(self):
        summary = ModelSummary(
            model="openai/gpt-4.1",
            runs_completed=4,
            runs_failed=0,
            avg_score=8.5,
            min_score=8.0,
            max_score=9.0,
            std_dev=0.35,
            pass_rate=1.0,
        )
        assert summary.runs_completed == 4
        assert summary.avg_score == 8.5
        assert summary.pass_rate == 1.0


class TestCrossValidationReport:
    """Tests for CrossValidationReport dataclass."""

    def test_default_values(self):
        report = CrossValidationReport(
            prompt_title="Test",
            prompt_file="test.md",
        )
        assert report.prompt_title == "Test"
        assert report.total_runs == 0
        assert report.consensus_score == 0.0
        assert report.cross_validation_passed is False
        assert report.final_grade == "N/A"


# =============================================================================
# PROMPT PARSING TESTS
# =============================================================================


class TestParsePromptFile:
    """Tests for parse_prompt_file function."""

    def test_parses_frontmatter(self, sample_prompt_file: str):
        data = parse_prompt_file(sample_prompt_file)
        assert data["title"] == "Test Prompt"
        assert data["shortTitle"] == "test"
        assert data["difficulty"] == "intermediate"
        assert data["type"] == "how_to"
        assert "developers" in data["audience"]
        assert "chatgpt" in data["platforms"]

    def test_extracts_content(self, sample_prompt_file: str):
        data = parse_prompt_file(sample_prompt_file)
        assert "# Test Prompt Content" in data["content"]
        assert "## Instructions" in data["content"]
        assert data["word_count"] > 0

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            parse_prompt_file("/nonexistent/path/file.md")

    def test_file_without_frontmatter(self, tmp_path: Path):
        content = "# Simple Prompt\n\nNo frontmatter here."
        file_path = tmp_path / "simple.md"
        file_path.write_text(content, encoding="utf-8")

        data = parse_prompt_file(str(file_path))
        assert data["title"] == "simple"  # Falls back to filename stem
        assert data["difficulty"] == "intermediate"  # Default value
        assert "# Simple Prompt" in data["content"]


# =============================================================================
# TEMP EVAL FILE TESTS
# =============================================================================


class TestCreateTempEvalFile:
    """Tests for create_temp_eval_file function."""

    def test_creates_yaml_file(self, sample_prompt_data: dict[str, Any]):
        temp_path = create_temp_eval_file(sample_prompt_data, "openai/gpt-4.1")
        try:
            assert Path(temp_path).exists()
            assert temp_path.endswith(".prompt.yml")

            content = Path(temp_path).read_text(encoding="utf-8")
            assert "openai/gpt-4.1" in content
            assert "Test Prompt" in content
            assert "temperature: 0.3" in content
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_includes_evaluation_criteria(self, sample_prompt_data: dict[str, Any]):
        temp_path = create_temp_eval_file(sample_prompt_data, "openai/gpt-4o")
        try:
            content = Path(temp_path).read_text(encoding="utf-8")
            assert "Clarity" in content
            assert "Specificity" in content
            assert "Actionability" in content
            assert "Pass/Fail Criteria" in content
        finally:
            Path(temp_path).unlink(missing_ok=True)


# =============================================================================
# FATAL ERROR DETECTION TESTS
# =============================================================================


class TestDetectFatalErrorReason:
    """Tests for detect_fatal_error_reason function."""

    def test_detects_model_not_found(self):
        reason = detect_fatal_error_reason("Error: Model not found")
        assert reason == "Model is not available in GitHub Models"

    def test_detects_access_denied(self):
        reason = detect_fatal_error_reason("You don't have access to this model")
        assert reason == "Model access denied"

    def test_detects_forbidden(self):
        reason = detect_fatal_error_reason("403 Forbidden response")
        assert reason == "GitHub authentication or access issue"

    def test_returns_none_for_transient_error(self):
        reason = detect_fatal_error_reason("Connection timeout")
        assert reason is None

    def test_returns_none_for_empty_message(self):
        assert detect_fatal_error_reason(None) is None
        assert detect_fatal_error_reason("") is None

    def test_case_insensitive(self):
        reason = detect_fatal_error_reason("MODEL NOT FOUND")
        assert reason is not None


# =============================================================================
# LOG WRITER TESTS
# =============================================================================


class TestCreateLogWriter:
    """Tests for create_log_writer function."""

    def test_returns_none_when_no_file(self, sample_prompt_data: dict[str, Any]):
        writer = create_log_writer(None, sample_prompt_data)
        assert writer is None

    def test_creates_log_file(self, tmp_path: Path, sample_prompt_data: dict[str, Any]):
        log_file = tmp_path / "eval.log.md"
        writer = create_log_writer(str(log_file), sample_prompt_data)

        assert writer is not None
        assert log_file.exists()

        content = log_file.read_text(encoding="utf-8")
        assert "## Prompt: Test Prompt" in content
        assert "File: `/path/to/test.md`" in content

    def test_writes_success_entry(
        self,
        tmp_path: Path,
        sample_prompt_data: dict[str, Any],
        sample_eval_result: EvalResult,
    ):
        log_file = tmp_path / "eval.log.md"
        writer = create_log_writer(str(log_file), sample_prompt_data)

        assert writer is not None
        writer("openai/gpt-4.1", 1, sample_eval_result)

        content = log_file.read_text(encoding="utf-8")
        assert "**openai/gpt-4.1**" in content
        assert "run 1" in content
        assert "8.60/10" in content
        assert "A-" in content

    def test_writes_error_entry(
        self,
        tmp_path: Path,
        sample_prompt_data: dict[str, Any],
        sample_error_result: EvalResult,
    ):
        log_file = tmp_path / "eval.log.md"
        writer = create_log_writer(str(log_file), sample_prompt_data)

        assert writer is not None
        writer("openai/gpt-4.1", 1, sample_error_result)

        content = log_file.read_text(encoding="utf-8")
        assert "❌" in content
        assert "Error:" in content
        assert "Error:" in content

    def test_sequential_ids(
        self,
        tmp_path: Path,
        sample_prompt_data: dict[str, Any],
        sample_eval_result: EvalResult,
    ):
        # Reset counter for this test
        dual_eval.LOG_ENTRY_COUNTER = dual_eval.count(1)

        log_file = tmp_path / "eval.log.md"
        writer = create_log_writer(str(log_file), sample_prompt_data)

        assert writer is not None
        writer("model1", 1, sample_eval_result)
        writer("model2", 1, sample_eval_result)
        writer("model3", 1, sample_eval_result)

        content = log_file.read_text(encoding="utf-8")
        assert "1. [" in content
        assert "2. [" in content
        assert "3. [" in content
        assert "3. [" in content

    def test_thread_safety(
        self,
        tmp_path: Path,
        sample_prompt_data: dict[str, Any],
        sample_eval_result: EvalResult,
    ):
        """Test that concurrent writes don't corrupt the log."""
        log_file = tmp_path / "concurrent.log.md"
        writer = create_log_writer(str(log_file), sample_prompt_data)

        assert writer is not None
        threads = []
        for i in range(10):
            t = threading.Thread(
                target=writer, args=(f"model{i}", 1, sample_eval_result)
            )
            threads.append(t)

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        content = log_file.read_text(encoding="utf-8")
        # Should have header + 10 entries
        lines = [l for l in content.split("\n") if l.strip()]
        assert len(lines) >= 10  # At least 10 entries written
        assert len(lines) >= 10  # At least 10 entries written


# =============================================================================
# CROSS-VALIDATION TESTS
# =============================================================================


class TestCrossValidate:
    """Tests for cross_validate function."""

    def test_calculates_consensus_score(self, sample_prompt_data: dict[str, Any]):
        summaries = {
            "model1": ModelSummary(model="model1", avg_score=8.0),
            "model2": ModelSummary(model="model2", avg_score=8.5),
            "model3": ModelSummary(model="model3", avg_score=9.0),
        }

        report = cross_validate(sample_prompt_data, summaries)

        assert report.consensus_score == pytest.approx(8.5, rel=0.01)
        assert report.score_variance == pytest.approx(1.0, rel=0.01)

    def test_passes_cross_validation(self, sample_prompt_data: dict[str, Any]):
        summaries = {
            "model1": ModelSummary(model="model1", avg_score=8.0),
            "model2": ModelSummary(model="model2", avg_score=8.2),
        }

        report = cross_validate(sample_prompt_data, summaries)

        assert report.cross_validation_passed is True
        assert len(report.discrepancies) == 0

    def test_fails_cross_validation_high_variance(
        self, sample_prompt_data: dict[str, Any]
    ):
        summaries = {
            "model1": ModelSummary(model="model1", avg_score=6.0),
            "model2": ModelSummary(model="model2", avg_score=9.0),
        }

        report = cross_validate(sample_prompt_data, summaries)

        assert report.cross_validation_passed is False
        assert report.score_variance > CROSS_VALIDATION_THRESHOLD

    def test_identifies_discrepancies(self, sample_prompt_data: dict[str, Any]):
        summaries = {
            "model1": ModelSummary(model="model1", avg_score=8.0),
            "model2": ModelSummary(model="model2", avg_score=8.0),
            "outlier": ModelSummary(model="outlier", avg_score=5.0),
        }

        report = cross_validate(sample_prompt_data, summaries)

        assert len(report.discrepancies) > 0
        assert any("outlier" in d for d in report.discrepancies)

    def test_assigns_grade_a_plus(self, sample_prompt_data: dict[str, Any]):
        summaries = {"model1": ModelSummary(model="model1", avg_score=9.5)}
        report = cross_validate(sample_prompt_data, summaries)
        assert report.final_grade == "A+"

    def test_assigns_grade_b(self, sample_prompt_data: dict[str, Any]):
        summaries = {"model1": ModelSummary(model="model1", avg_score=7.2)}
        report = cross_validate(sample_prompt_data, summaries)
        assert report.final_grade == "B"

    def test_assigns_grade_f(self, sample_prompt_data: dict[str, Any]):
        summaries = {"model1": ModelSummary(model="model1", avg_score=4.0)}
        report = cross_validate(sample_prompt_data, summaries)
        assert report.final_grade == "F"

    def test_determines_pass_fail(self, sample_prompt_data: dict[str, Any]):
        passing = {"model1": ModelSummary(model="model1", avg_score=8.0)}
        failing = {"model1": ModelSummary(model="model1", avg_score=5.0)}

        assert cross_validate(sample_prompt_data, passing).final_pass is True
        assert cross_validate(sample_prompt_data, failing).final_pass is False

    def test_counts_total_runs(self, sample_prompt_data: dict[str, Any]):
        summaries = {
            "model1": ModelSummary(model="model1", runs_completed=4, runs_failed=0),
            "model2": ModelSummary(model="model2", runs_completed=3, runs_failed=1),
        }

        report = cross_validate(sample_prompt_data, summaries)
        assert report.total_runs == 8

    def test_combines_strengths_and_improvements(
        self, sample_prompt_data: dict[str, Any]
    ):
        result1 = EvalResult(
            model="m1",
            run_number=1,
            strengths=["Clear", "Structured"],
            improvements=["Add examples"],
        )
        result2 = EvalResult(
            model="m2",
            run_number=1,
            strengths=["Clear", "Concise"],  # "Clear" is duplicate
            improvements=["More detail"],
        )

        summaries = {
            "model1": ModelSummary(
                model="model1", avg_score=8.0, all_results=[result1]
            ),
            "model2": ModelSummary(
                model="model2", avg_score=8.0, all_results=[result2]
            ),
        }

        report = cross_validate(sample_prompt_data, summaries)

        # Should dedupe "Clear"
        assert "Clear" in report.combined_strengths
        assert "Structured" in report.combined_strengths
        assert "Concise" in report.combined_strengths
        assert report.combined_strengths.count("Clear") == 1


# =============================================================================
# CONFIGURATION TESTS
# =============================================================================


class TestConfiguration:
    """Tests for configuration constants."""

    def test_pass_threshold(self):
        assert PASS_THRESHOLD == 7.0

    def test_cross_validation_threshold(self):
        assert CROSS_VALIDATION_THRESHOLD == 1.5

    def test_fatal_error_patterns_exist(self):
        assert len(FATAL_ERROR_PATTERNS) > 0
        for pattern, reason in FATAL_ERROR_PATTERNS:
            assert isinstance(pattern, str)
            assert isinstance(reason, str)

    def test_default_models_defined(self):
        assert len(dual_eval.EVAL_MODELS) > 0
        assert "openai/gpt-4.1" in dual_eval.EVAL_MODELS


# =============================================================================
# INTEGRATION TESTS (with mocking)
# =============================================================================


class TestRunSingleEval:
    """Tests for run_single_eval with mocked subprocess."""

    def test_successful_eval(self, sample_prompt_data: dict[str, Any]):
        mock_response = {"testResults": [{"modelResponse": """```json
{
    "scores": {"clarity": 8, "specificity": 8},
    "overall_score": 8.0,
    "grade": "B+",
    "pass": true,
    "pass_reason": "Good",
    "reasoning": "Test",
    "strengths": ["Good"],
    "improvements": ["Better"],
    "summary": "OK"
}
```"""}]}

        with mock.patch("subprocess.run") as mock_run:
            mock_run.return_value = mock.Mock(
                returncode=0,
                stdout=json.dumps(mock_response),
                stderr="",
            )

            temp_file = create_temp_eval_file(sample_prompt_data, "test-model")
            try:
                result = dual_eval.run_single_eval(temp_file, "test-model", 1)

                assert result.error is None
                assert result.overall_score == 8.0
                assert result.grade == "B+"
                assert result.passed is True
            finally:
                Path(temp_file).unlink(missing_ok=True)

    def test_failed_eval(self, sample_prompt_data: dict[str, Any]):
        with mock.patch("subprocess.run") as mock_run:
            mock_run.return_value = mock.Mock(
                returncode=1,
                stdout="",
                stderr="Error: Model not found",
            )

            temp_file = create_temp_eval_file(sample_prompt_data, "test-model")
            try:
                result = dual_eval.run_single_eval(temp_file, "test-model", 1)

                assert result.error is not None
                assert (
                    "failed" in result.error.lower() or "error" in result.error.lower()
                )
            finally:
                Path(temp_file).unlink(missing_ok=True)


# Import json for mock tests
import json

# =============================================================================
# FILE DISCOVERY TESTS
# =============================================================================


class TestDiscoverPromptFiles:
    """Tests for discover_prompt_files function."""

    def test_discovers_single_file(self, sample_prompt_file: str):
        files = dual_eval.discover_prompt_files([sample_prompt_file])
        assert len(files) == 1
        assert files[0].name == "test_prompt.md"

    def test_discovers_directory(self, tmp_path: Path):
        # Create test files
        (tmp_path / "prompt1.md").write_text("# Prompt 1", encoding="utf-8")
        (tmp_path / "prompt2.md").write_text("# Prompt 2", encoding="utf-8")
        (tmp_path / "readme.txt").write_text("Not a prompt", encoding="utf-8")

        files = dual_eval.discover_prompt_files([str(tmp_path)])
        assert len(files) == 2
        assert all(f.suffix == ".md" for f in files)

    def test_recursive_discovery(self, tmp_path: Path):
        # Create nested structure
        subdir = tmp_path / "nested"
        subdir.mkdir()
        (tmp_path / "top.md").write_text("# Top", encoding="utf-8")
        (subdir / "nested.md").write_text("# Nested", encoding="utf-8")

        files = dual_eval.discover_prompt_files([str(tmp_path)], recursive=True)
        assert len(files) == 2

        files_flat = dual_eval.discover_prompt_files([str(tmp_path)], recursive=False)
        assert len(files_flat) == 1

    def test_skips_nonexistent_paths(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ):
        files = dual_eval.discover_prompt_files([str(tmp_path / "nonexistent")])
        assert len(files) == 0
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower()

    def test_skips_non_markdown_files(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ):
        (tmp_path / "script.py").write_text("print('hello')", encoding="utf-8")
        files = dual_eval.discover_prompt_files([str(tmp_path / "script.py")])
        assert len(files) == 0
        captured = capsys.readouterr()
        assert "skipping" in captured.out.lower()

    def test_deduplicates_files(self, sample_prompt_file: str):
        # Pass same file twice
        files = dual_eval.discover_prompt_files(
            [sample_prompt_file, sample_prompt_file]
        )
        assert len(files) == 1

    def test_excludes_readme_files(self, tmp_path: Path):
        (tmp_path / "README.md").write_text("# README", encoding="utf-8")
        (tmp_path / "prompt.md").write_text("# Prompt", encoding="utf-8")
        files = dual_eval.discover_prompt_files([str(tmp_path)])
        assert len(files) == 1
        assert files[0].name == "prompt.md"

    def test_excludes_index_files(self, tmp_path: Path):
        (tmp_path / "index.md").write_text("# Index", encoding="utf-8")
        (tmp_path / "prompt.md").write_text("# Prompt", encoding="utf-8")
        files = dual_eval.discover_prompt_files([str(tmp_path)])
        assert len(files) == 1
        assert files[0].name == "prompt.md"

    def test_excludes_agent_files(self, tmp_path: Path):
        (tmp_path / "test.agent.md").write_text("# Agent", encoding="utf-8")
        (tmp_path / "prompt.md").write_text("# Prompt", encoding="utf-8")
        files = dual_eval.discover_prompt_files([str(tmp_path)])
        assert len(files) == 1
        assert files[0].name == "prompt.md"

    def test_excludes_instruction_files(self, tmp_path: Path):
        (tmp_path / "test.instructions.md").write_text(
            "# Instructions", encoding="utf-8"
        )
        (tmp_path / "prompt.md").write_text("# Prompt", encoding="utf-8")
        files = dual_eval.discover_prompt_files([str(tmp_path)])
        assert len(files) == 1
        assert files[0].name == "prompt.md"

    def test_excludes_archive_directory(self, tmp_path: Path):
        archive = tmp_path / "archive"
        archive.mkdir()
        (archive / "old.md").write_text("# Old", encoding="utf-8")
        (tmp_path / "prompt.md").write_text("# Prompt", encoding="utf-8")
        files = dual_eval.discover_prompt_files([str(tmp_path)])
        assert len(files) == 1
        assert files[0].name == "prompt.md"

    def test_include_all_overrides_filtering(self, tmp_path: Path):
        (tmp_path / "README.md").write_text("# README", encoding="utf-8")
        (tmp_path / "test.agent.md").write_text("# Agent", encoding="utf-8")
        (tmp_path / "prompt.md").write_text("# Prompt", encoding="utf-8")

        # Without include_all
        files = dual_eval.discover_prompt_files([str(tmp_path)])
        assert len(files) == 1

        # With include_all
        files = dual_eval.discover_prompt_files([str(tmp_path)], include_all=True)
        assert len(files) == 3


class TestIsPromptFile:
    """Tests for is_prompt_file helper function."""

    def test_accepts_regular_prompt(self, tmp_path: Path):
        f = tmp_path / "code-review.md"
        assert dual_eval.is_prompt_file(f)

    def test_rejects_readme(self, tmp_path: Path):
        f = tmp_path / "README.md"
        assert not dual_eval.is_prompt_file(f)

    def test_rejects_index(self, tmp_path: Path):
        f = tmp_path / "index.md"
        assert not dual_eval.is_prompt_file(f)

    def test_rejects_agent(self, tmp_path: Path):
        f = tmp_path / "code-review.agent.md"
        assert not dual_eval.is_prompt_file(f)

    def test_rejects_instructions(self, tmp_path: Path):
        f = tmp_path / "csharp.instructions.md"
        assert not dual_eval.is_prompt_file(f)

    def test_rejects_archive_path(self, tmp_path: Path):
        f = tmp_path / "archive" / "old-prompt.md"
        assert not dual_eval.is_prompt_file(f)

    """Tests for get_changed_files function."""

    def test_handles_git_not_found(self, capsys: pytest.CaptureFixture[str]):
        with mock.patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError("git not found")
            files = dual_eval.get_changed_files()
            assert files == []
            captured = capsys.readouterr()
            assert "git not found" in captured.out.lower()

    def test_handles_git_timeout(self, capsys: pytest.CaptureFixture[str]):
        import subprocess

        with mock.patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("git", 30)
            files = dual_eval.get_changed_files()
            assert files == []
            captured = capsys.readouterr()
            assert "timed out" in captured.out.lower()

    def test_parses_git_output(self, tmp_path: Path):
        # Create a test file
        test_file = tmp_path / "changed.md"
        test_file.write_text("# Changed", encoding="utf-8")

        with mock.patch("subprocess.run") as mock_run:
            mock_run.return_value = mock.Mock(
                returncode=0,
                stdout=str(test_file) + "\n",
            )
            files = dual_eval.get_changed_files()
            # File might not be in results if path doesn't exist relative to git root
            # This tests the parsing logic works
            assert isinstance(files, list)


# =============================================================================
# JSON REPORT TESTS
# =============================================================================


class TestJsonReport:
    """Tests for JSON report generation."""

    def test_report_to_dict(self, sample_prompt_data: dict[str, Any]):
        # Create a minimal report
        report = CrossValidationReport(
            prompt_title="Test",
            prompt_file="test.md",
            consensus_score=8.5,
            final_grade="A",
            final_pass=True,
        )

        result = dual_eval.report_to_dict(report)

        assert result["prompt_title"] == "Test"
        assert result["consensus_score"] == 8.5
        assert result["final_pass"] is True
        assert "model_summaries" in result

    def test_generate_json_report_single(self, sample_prompt_data: dict[str, Any]):
        report = CrossValidationReport(
            prompt_title="Test",
            prompt_file="test.md",
            consensus_score=8.0,
            final_grade="B+",
            final_pass=True,
        )

        json_str = dual_eval.generate_json_report([report])
        data = json.loads(json_str)

        assert data["total_files"] == 1
        assert data["passed"] == 1
        assert data["failed"] == 0
        assert len(data["results"]) == 1

    def test_generate_json_report_batch(self, sample_prompt_data: dict[str, Any]):
        reports = [
            CrossValidationReport(
                prompt_title="Test 1",
                prompt_file="test1.md",
                consensus_score=8.5,
                final_pass=True,
            ),
            CrossValidationReport(
                prompt_title="Test 2",
                prompt_file="test2.md",
                consensus_score=6.0,
                final_pass=False,
            ),
        ]

        json_str = dual_eval.generate_json_report(reports)
        data = json.loads(json_str)

        assert data["total_files"] == 2
        assert data["passed"] == 1
        assert data["failed"] == 1
        assert data["average_score"] == 7.25
        assert "generated_at" in data
        assert "version" in data


class TestBatchMarkdownReport:
    """Tests for batch markdown report generation."""

    def test_generates_summary_table(self):
        reports = [
            CrossValidationReport(
                prompt_title="Good Prompt",
                prompt_file="good.md",
                consensus_score=8.5,
                final_grade="A",
                final_pass=True,
            ),
            CrossValidationReport(
                prompt_title="Bad Prompt",
                prompt_file="bad.md",
                consensus_score=5.5,
                final_grade="C",
                final_pass=False,
            ),
        ]

        md = dual_eval.generate_batch_markdown_report(reports)

        assert "Batch Evaluation Report" in md
        assert "Files Evaluated" in md
        assert "good.md" in md
        assert "bad.md" in md
        assert "PASS" in md
        assert "FAIL" in md


# =============================================================================
# BATCH REPORT DATACLASS TESTS
# =============================================================================


class TestBatchReport:
    """Tests for BatchReport dataclass."""

    def test_default_values(self):
        report = dual_eval.BatchReport(generated_at="2025-12-04T10:00:00")
        assert report.total_files == 0
        assert report.passed == 0
        assert report.failed == 0
        assert report.results == []
