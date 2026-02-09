"""Scorer.

Scores workflow outputs against golden examples using configured
rubrics. Integrates with the existing tools/prompteval/ scoring
patterns.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ScoreResult:
    """Result from scoring."""

    total_score: float
    max_score: float
    percentage: float
    passed: bool
    category_scores: Dict[str, float]
    details: Dict[str, Any]


class Scorer:
    """Scores outputs against goldens using rubric weights.

    Supports multiple scoring methods:
    - Exact match
    - Fuzzy match
    - AST comparison (for code)
    - Test execution (for functional correctness)
    """

    def __init__(self, rubrics: Dict[str, Any]):
        """Initialize scorer with rubrics.

        Args:
            rubrics: Rubrics configuration dict
        """
        self.rubrics = rubrics

    def score(
        self,
        output: str,
        golden: str,
        rubric_name: str,
    ) -> ScoreResult:
        """Score output against golden using named rubric.

        Args:
            output: Generated output to score
            golden: Golden/expected output
            rubric_name: Name of rubric to use

        Returns:
            ScoreResult with detailed breakdown
        """
        rubric = self.rubrics.get("rubrics", {}).get(rubric_name, {})
        categories = rubric.get("categories", {})
        pass_threshold = rubric.get("pass_threshold", 70)

        scores: Dict[str, float] = {}
        details: Dict[str, Any] = {}

        for category_name, category in categories.items():
            weight = category.get("weight", 0)

            # Score this category
            category_score = self._score_category(
                output, golden, category_name, category
            )
            scores[category_name] = category_score * weight
            details[category_name] = {
                "raw_score": category_score,
                "weight": weight,
                "weighted_score": category_score * weight,
            }

        # Calculate total
        total_score = sum(scores.values())
        max_score = 100.0
        percentage = (total_score / max_score) * 100
        passed = percentage >= pass_threshold

        return ScoreResult(
            total_score=total_score,
            max_score=max_score,
            percentage=percentage,
            passed=passed,
            category_scores=scores,
            details=details,
        )

    def _score_category(
        self,
        output: str,
        golden: str,
        category_name: str,
        category: Dict[str, Any],
    ) -> float:
        """Score a single category (0-1 scale)."""
        # Use appropriate scoring method based on category
        if "correctness" in category_name.lower():
            return self.score_correctness(output, golden)
        elif "quality" in category_name.lower():
            return self.score_code_quality(output)
        elif "documentation" in category_name.lower():
            return self.score_documentation(output)
        elif "completeness" in category_name.lower():
            return self.score_completeness(output, golden)
        else:
            return self.score_similarity(output, golden)

    def score_correctness(self, output: str, golden: str) -> float:
        """Score functional correctness."""
        # Use fuzzy matching as a baseline
        similarity = SequenceMatcher(None, output, golden).ratio()
        return similarity

    def score_code_quality(self, output: str) -> float:
        """Score code quality based on heuristics."""
        score = 0.8  # Base score

        # Positive indicators
        if "def " in output or "function " in output:
            score += 0.05  # Has functions
        if '"""' in output or "'''" in output:
            score += 0.05  # Has docstrings
        if ": str" in output or ": int" in output or "-> " in output:
            score += 0.05  # Has type hints

        # Negative indicators
        if "TODO" in output:
            score -= 0.1
        if "FIXME" in output:
            score -= 0.1
        if "pass" in output and output.count("pass") > 5:
            score -= 0.1  # Many empty pass statements

        return max(0, min(1, score))

    def score_documentation(self, output: str) -> float:
        """Score documentation presence."""
        score = 0.0

        indicators = [
            ("README", 0.2),
            ("## ", 0.1),
            ("Usage", 0.1),
            ("Example", 0.1),
            ("API", 0.1),
            ('"""', 0.15),
            ("Args:", 0.1),
            ("Returns:", 0.1),
        ]

        for indicator, points in indicators:
            if indicator in output:
                score += points

        return min(1, score)

    def score_completeness(self, output: str, golden: str) -> float:
        """Score completeness based on expected elements."""
        if not golden:
            return 1.0

        # Extract key elements from golden
        golden_lines = set(line.strip() for line in golden.split("\n") if line.strip())
        output_lines = set(line.strip() for line in output.split("\n") if line.strip())

        if not golden_lines:
            return 1.0

        matched = len(golden_lines & output_lines)
        return matched / len(golden_lines)

    def score_similarity(self, output: str, golden: str) -> float:
        """Score based on text similarity."""
        return SequenceMatcher(None, output, golden).ratio()


@dataclass
class ExecutionResult:
    """Result from execution-based scoring."""

    resolved: bool
    return_code: int
    duration_ms: float
    stdout: str = ""
    stderr: str = ""
    error: Optional[str] = None
    test_command: Optional[str] = None


class ExecutionScorer:
    """Execution-based scorer for SWE-bench style tasks.

    This scorer:
    - clones the repository at base_commit
    - applies the model patch and optional test_patch
    - runs the provided test command (or default)
    - returns resolved=True if tests pass (exit code 0)

    It is intentionally optional and fails gracefully if Docker/git
    are not available.
    """

    def __init__(
        self,
        *,
        docker_image: str = "python:3.11-slim",
        timeout_seconds: int = 1200,
        repo_cache_dir: Optional[Path] = None,
        default_test_command: str = "pytest -q",
        setup_commands: Optional[List[str]] = None,
    ) -> None:
        self.docker_image = docker_image
        self.timeout_seconds = timeout_seconds
        self.repo_cache_dir = repo_cache_dir
        self.default_test_command = default_test_command
        self.setup_commands = setup_commands or [
            "apt-get update && apt-get install -y git",
            "python -m pip install -U pip",
            "if [ -f requirements.txt ]; then python -m pip install -r requirements.txt; fi",
            "if [ -f pyproject.toml ]; then python -m pip install -e .; fi",
        ]

    def _ensure_tool(self, name: str) -> None:
        if shutil.which(name) is None:
            raise RuntimeError(f"Required tool not found: {name}")

    def _run(
        self, cmd: List[str], cwd: Optional[Path] = None, timeout: Optional[int] = None
    ) -> subprocess.CompletedProcess:
        return subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )

    def _docker_run_tests(
        self,
        repo: str,
        base_commit: str,
        patches_dir: Path,
        test_command: str,
    ) -> subprocess.CompletedProcess:
        setup = " && ".join(self.setup_commands)
        repo_url = f"https://github.com/{repo}.git"
        command = " && ".join(
            [
                f"git clone {repo_url} /workspace/repo",
                "cd /workspace/repo",
                f"git checkout {base_commit}",
                "if [ -s /patches/model.patch ]; then git apply /patches/model.patch; fi",
                "if [ -s /patches/tests.patch ]; then git apply /patches/tests.patch; fi",
                setup,
                test_command,
            ]
        )
        return self._run(
            [
                "docker",
                "run",
                "--rm",
                "-v",
                f"{patches_dir}:/patches:ro",
                "-w",
                "/workspace",
                self.docker_image,
                "bash",
                "-lc",
                command,
            ],
            timeout=self.timeout_seconds,
        )

    def score_task(self, task: Dict[str, Any], patch: str) -> ExecutionResult:
        """Execute tests for a SWE-bench task and return resolution status."""
        start = time.perf_counter()
        repo = task.get("repo", "")
        base_commit = task.get("base_commit", "")
        test_patch = ""
        test_cases = task.get("test_cases") or []
        if isinstance(test_cases, list) and test_cases:
            test_patch = (
                test_cases[0].get("test_patch", "")
                if isinstance(test_cases[0], dict)
                else ""
            )
        test_command = (
            task.get("test_command")
            or task.get("test_cmd")
            or self.default_test_command
        )

        if not repo or not base_commit:
            return ExecutionResult(
                resolved=False,
                return_code=1,
                duration_ms=0.0,
                error="Task missing repo/base_commit for execution scoring.",
                test_command=test_command,
            )

        try:
            self._ensure_tool("docker")

            with tempfile.TemporaryDirectory(prefix="swebench_") as tmpdir:
                patches_dir = Path(tmpdir) / "patches"
                patches_dir.mkdir(parents=True, exist_ok=True)
                (patches_dir / "model.patch").write_text(patch or "", encoding="utf-8")
                (patches_dir / "tests.patch").write_text(
                    test_patch or "", encoding="utf-8"
                )

                result = self._docker_run_tests(
                    repo=repo,
                    base_commit=base_commit,
                    patches_dir=patches_dir,
                    test_command=test_command,
                )
                duration_ms = (time.perf_counter() - start) * 1000

                return ExecutionResult(
                    resolved=result.returncode == 0,
                    return_code=result.returncode,
                    duration_ms=duration_ms,
                    stdout=result.stdout,
                    stderr=result.stderr,
                    test_command=test_command,
                )
        except Exception as exc:
            duration_ms = (time.perf_counter() - start) * 1000
            return ExecutionResult(
                resolved=False,
                return_code=1,
                duration_ms=duration_ms,
                error=str(exc),
                test_command=test_command,
            )
