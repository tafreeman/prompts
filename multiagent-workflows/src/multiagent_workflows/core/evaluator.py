"""
Workflow Evaluator

Integrates with the existing evaluation framework to:
- Load datasets with golden examples
- Score workflow outputs against goldens
- Generate evaluation reports
- Compare to baselines
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml


@dataclass
class EvaluationResult:
    """Result from workflow evaluation."""
    workflow_name: str
    total_score: float
    max_score: float
    percentage: float
    grade: str
    passed: bool
    category_scores: Dict[str, Dict[str, Any]]
    feedback: str
    strengths: List[str]
    weaknesses: List[str]


class WorkflowEvaluator:
    """
    Evaluates workflow outputs using configured rubrics.
    
    Integrates with tools/prompteval/ patterns for consistent evaluation.
    
    Example:
        evaluator = WorkflowEvaluator()
        result = await evaluator.evaluate_workflow(
            workflow_name="fullstack_generation",
            output={"code": "...", "tests": "..."},
            golden={"code": "...", "tests": "..."},
        )
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize evaluator.
        
        Args:
            config: Optional configuration override
        """
        self.config = config or self._load_default_config()
        self.rubrics = self._load_rubrics()
        self._golden_cache: Dict[str, Dict[str, Any]] = {}
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default evaluation configuration."""
        config_path = Path(__file__).parent.parent.parent / "config" / "evaluation.yaml"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {}
    
    def _load_rubrics(self) -> Dict[str, Any]:
        """Load scoring rubrics."""
        # Look for rubrics.yaml in the config directory relative to the project root
        rubrics_path = Path(__file__).parent.parent.parent.parent / "config" / "rubrics.yaml"
        if not rubrics_path.exists():
            # Fallback to config directory relative to current file
            rubrics_path = Path(__file__).parent.parent.parent / "config" / "rubrics.yaml"
        if rubrics_path.exists():
            with open(rubrics_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {}
    
    def has_golden(self, workflow_name: str, inputs: Dict[str, Any]) -> bool:
        """Check if golden output exists for given inputs."""
        golden_dir = Path(self.config.get("paths", {}).get("golden", "./evaluation/golden"))
        golden_path = golden_dir / workflow_name
        return golden_path.exists()
    
    async def load_golden(
        self,
        workflow_name: str,
        inputs: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """Load golden output for comparison."""
        cache_key = f"{workflow_name}:{hash(str(inputs))}"
        if cache_key in self._golden_cache:
            return self._golden_cache[cache_key]
        
        golden_dir = Path(self.config.get("paths", {}).get("golden", "./evaluation/golden"))
        golden_path = golden_dir / workflow_name / "golden.json"
        
        if golden_path.exists():
            with open(golden_path, "r", encoding="utf-8") as f:
                golden = json.load(f)
                self._golden_cache[cache_key] = golden
                return golden
        
        return None
    
    async def score_output(
        self,
        output: Dict[str, Any],
        workflow_name: str,
        inputs: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Score workflow output against golden example.
        
        Args:
            output: Workflow output to score
            workflow_name: Name of workflow for rubric selection
            inputs: Original inputs (for golden lookup)
            
        Returns:
            Scoring result with breakdown
        """
        golden = await self.load_golden(workflow_name, inputs)
        
        if golden is None:
            return {
                "error": "No golden output available for comparison",
                "total_score": 0,
                "passed": False,
            }
        
        # Get rubric for this workflow
        rubric = self.rubrics.get("rubrics", {}).get(workflow_name, {})
        if not rubric:
            rubric = self.rubrics.get("rubrics", {}).get("fullstack_generation", {})
        
        return self._score_with_rubric(output, golden, rubric)
    
    def _score_with_rubric(
        self,
        output: Dict[str, Any],
        golden: Dict[str, Any],
        rubric: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Score output using the specified rubric."""
        categories = rubric.get("categories", {})
        total_points = rubric.get("total_points", 100)
        pass_threshold = rubric.get("pass_threshold", 70)
        
        category_scores: Dict[str, Dict[str, Any]] = {}
        weighted_total = 0.0
        weight_sum = 0.0
        
        strengths: List[str] = []
        weaknesses: List[str] = []
        
        for category_name, category in categories.items():
            weight = category.get("weight", 0)
            weight_sum += weight
            
            # Score category
            score = self._score_category(output, golden, category_name, category)
            weighted_score = score * weight
            weighted_total += weighted_score
            
            category_scores[category_name] = {
                "score": score,
                "weight": weight,
                "weighted_score": weighted_score,
                "max": 100,
            }
            
            # Track strengths/weaknesses
            if score >= 80:
                strengths.append(f"{category_name}: {score:.0f}%")
            elif score < 60:
                weaknesses.append(f"{category_name}: {score:.0f}%")
        
        # Calculate final score
        final_score = weighted_total / weight_sum if weight_sum > 0 else 0
        percentage = (final_score / 100) * 100
        passed = final_score >= pass_threshold
        grade = self._calculate_grade(final_score)
        
        return {
            "total_score": round(final_score, 2),
            "max_score": total_points,
            "percentage": round(percentage, 2),
            "grade": grade,
            "passed": passed,
            "category_scores": category_scores,
            "feedback": self._generate_feedback(category_scores, passed),
            "strengths": strengths,
            "weaknesses": weaknesses,
        }
    
    def _score_category(
        self,
        output: Dict[str, Any],
        golden: Dict[str, Any],
        category_name: str,
        category: Dict[str, Any],
    ) -> float:
        """Score a single category."""
        criteria = category.get("criteria", [])
        if not criteria:
            return self._basic_similarity(output, golden) * 100
        
        total_score = 0.0
        total_points = 0
        
        for criterion in criteria:
            points = criterion.get("points", 10)
            total_points += points
            
            # Score criterion based on name
            criterion_name = criterion.get("name", "").lower().replace(" ", "_")
            score = self._score_criterion(output, golden, criterion_name, criterion)
            total_score += score * points / 100
        
        return (total_score / total_points * 100) if total_points > 0 else 0
    
    def _score_criterion(
        self,
        output: Dict[str, Any],
        golden: Dict[str, Any],
        criterion_name: str,
        criterion: Dict[str, Any],
    ) -> float:
        """Score a single criterion (0-100)."""
        # Functional correctness: compare with golden
        if "correct" in criterion_name or "coverage" in criterion_name:
            return self._score_correctness(output, golden)
        
        # Code quality: check for quality indicators
        if "quality" in criterion_name or "standards" in criterion_name:
            return self._score_code_quality(output)
        
        # Documentation: check for documentation elements
        if "document" in criterion_name or "comment" in criterion_name:
            return self._score_documentation(output)
        
        # Completeness: check for required elements
        if "complete" in criterion_name:
            return self._score_completeness(output, golden)
            
        # Code similarity to golden standard
        if "similarity" in criterion_name and "golden" in criterion_name:
            return self._score_correctness(output, golden)
        
        # Default: similarity-based scoring
        return self._basic_similarity(output, golden) * 100
    
    def _score_correctness(
        self,
        output: Dict[str, Any],
        golden: Dict[str, Any],
    ) -> float:
        """Score functional correctness."""
        output_str = json.dumps(output, sort_keys=True, default=str)
        golden_str = json.dumps(golden, sort_keys=True, default=str)
        
        similarity = SequenceMatcher(None, output_str, golden_str).ratio()
        return similarity * 100
    
    def _score_code_quality(self, output: Dict[str, Any]) -> float:
        """Score code quality based on indicators."""
        output_str = str(output)
        score = 80.0  # Base score
        
        # Deductions
        if "TODO" in output_str or "FIXME" in output_str:
            score -= 10
        if "pass  # " in output_str:  # Empty pass statements
            score -= 5
        if len(output_str) > 100000:  # Very long output
            score -= 10
        
        # Bonuses
        if "def test_" in output_str or "async def test_" in output_str:
            score += 5
        if '"""' in output_str or "'''" in output_str:  # Docstrings
            score += 5
        if "typing" in output_str or ": str" in output_str:  # Type hints
            score += 5
        
        return max(0, min(100, score))
    
    def _score_documentation(self, output: Dict[str, Any]) -> float:
        """Score documentation presence."""
        output_str = str(output)
        score = 0.0
        
        indicators = [
            ("README", 20),
            ("## ", 10),
            ("### ", 5),
            ("Usage", 10),
            ("Example", 10),
            ("API", 10),
            ('"""', 15),
            ("# ", 5),
            ("Installation", 10),
            ("Configuration", 5),
        ]
        
        for indicator, points in indicators:
            if indicator in output_str:
                score += points
        
        return min(100, score)
    
    def _score_completeness(
        self,
        output: Dict[str, Any],
        golden: Dict[str, Any],
    ) -> float:
        """Score completeness based on golden keys."""
        golden_keys = set(self._flatten_keys(golden))
        output_keys = set(self._flatten_keys(output))
        
        if not golden_keys:
            return 100.0
        
        matched = len(golden_keys & output_keys)
        return (matched / len(golden_keys)) * 100
    
    def _flatten_keys(self, d: Dict[str, Any], prefix: str = "") -> List[str]:
        """Flatten dictionary keys."""
        keys = []
        for k, v in d.items():
            key = f"{prefix}.{k}" if prefix else k
            keys.append(key)
            if isinstance(v, dict):
                keys.extend(self._flatten_keys(v, key))
        return keys
    
    def _basic_similarity(
        self,
        output: Dict[str, Any],
        golden: Dict[str, Any],
    ) -> float:
        """Calculate basic similarity between outputs."""
        output_str = json.dumps(output, sort_keys=True, default=str)
        golden_str = json.dumps(golden, sort_keys=True, default=str)
        
        return SequenceMatcher(None, output_str, golden_str).ratio()
    
    def _calculate_grade(self, score: float) -> str:
        """Calculate letter grade from score."""
        grade_scale = self.rubrics.get("scoring", {}).get("grade_scale", {
            "A": [90, 100],
            "B": [80, 89],
            "C": [70, 79],
            "D": [60, 69],
            "F": [0, 59],
        })
        
        for grade, (min_score, max_score) in grade_scale.items():
            if min_score <= score <= max_score:
                return grade
        
        return "F"
    
    def _generate_feedback(
        self,
        category_scores: Dict[str, Dict[str, Any]],
        passed: bool,
    ) -> str:
        """Generate feedback summary."""
        if passed:
            feedback = "✅ Workflow passed evaluation. "
        else:
            feedback = "❌ Workflow did not meet the passing threshold. "
        
        # Identify top and bottom categories
        sorted_cats = sorted(
            category_scores.items(),
            key=lambda x: x[1]["score"],
            reverse=True,
        )
        
        if sorted_cats:
            top = sorted_cats[0]
            feedback += f"Strongest area: {top[0]} ({top[1]['score']:.0f}%). "
            
            if len(sorted_cats) > 1:
                bottom = sorted_cats[-1]
                feedback += f"Area for improvement: {bottom[0]} ({bottom[1]['score']:.0f}%)."
        
        return feedback
    
    async def evaluate_workflow(
        self,
        workflow_name: str,
        output: Dict[str, Any],
        golden: Optional[Dict[str, Any]] = None,
    ) -> EvaluationResult:
        """
        Evaluate a workflow output.
        
        Args:
            workflow_name: Workflow name for rubric selection
            output: Output to evaluate
            golden: Optional golden output (loads from cache if not provided)
            
        Returns:
            EvaluationResult with detailed scores
        """
        if golden is None:
            golden = await self.load_golden(workflow_name, {})
            if golden is None:
                golden = {}
        
        rubric = self.rubrics.get("rubrics", {}).get(workflow_name, {})
        if not rubric:
            rubric = self.rubrics.get("rubrics", {}).get("fullstack_generation", {})
        
        result = self._score_with_rubric(output, golden, rubric)
        
        return EvaluationResult(
            workflow_name=workflow_name,
            total_score=result["total_score"],
            max_score=result["max_score"],
            percentage=result["percentage"],
            grade=result["grade"],
            passed=result["passed"],
            category_scores=result["category_scores"],
            feedback=result["feedback"],
            strengths=result["strengths"],
            weaknesses=result["weaknesses"],
        )
    
    async def generate_report(
        self,
        results: List[EvaluationResult],
        output_path: Optional[Path] = None,
    ) -> str:
        """Generate evaluation report."""
        lines = [
            "# Workflow Evaluation Report",
            "",
            f"**Total Workflows Evaluated**: {len(results)}",
            f"**Passed**: {sum(1 for r in results if r.passed)}",
            f"**Failed**: {sum(1 for r in results if not r.passed)}",
            "",
            "## Summary",
            "",
            "| Workflow | Score | Grade | Status |",
            "|----------|-------|-------|--------|",
        ]
        
        for r in results:
            status = "✅ Pass" if r.passed else "❌ Fail"
            lines.append(f"| {r.workflow_name} | {r.total_score:.1f}% | {r.grade} | {status} |")
        
        lines.extend(["", "## Details", ""])
        
        for r in results:
            lines.extend([
                f"### {r.workflow_name}",
                "",
                f"**Score**: {r.total_score:.1f}/{r.max_score} ({r.percentage:.1f}%)",
                f"**Grade**: {r.grade}",
                "",
                "**Category Scores**:",
                "",
            ])
            
            for cat, scores in r.category_scores.items():
                lines.append(f"- {cat}: {scores['score']:.1f}%")
            
            lines.extend([
                "",
                f"**Feedback**: {r.feedback}",
                "",
            ])
            
            if r.strengths:
                lines.append("**Strengths**: " + ", ".join(r.strengths))
            if r.weaknesses:
                lines.append("**Weaknesses**: " + ", ".join(r.weaknesses))
            
            lines.append("")
        
        report = "\n".join(lines)
        
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(report)
        
        return report
