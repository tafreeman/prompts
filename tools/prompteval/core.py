#!/usr/bin/env python3
"""
PromptEval Core - Unified Evaluation Engine
============================================

Consolidates functionality from:
- tiered_eval.py (tier system)
- evaluate_library.py (dual rubric scoring)
- local_model.py (G-Eval + direct evaluation)
- cove_batch_analyzer.py (CoVe scoring dimensions)

This is a LEAN implementation that imports and orchestrates existing tools
rather than duplicating their logic.
"""

import sys
import json
import yaml
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum

# Add parent tools directory to path for imports
TOOLS_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(TOOLS_DIR))

# =============================================================================
# DATA CLASSES
# =============================================================================

class Tier(Enum):
    """Evaluation tiers with increasing rigor and cost."""
    STRUCTURAL = 0      # No LLM - structural analysis only ($0, <1s)
    LOCAL_QUICK = 1     # Single local model, 1 run ($0, ~30s)
    LOCAL_GEVAL = 2     # Local model with G-Eval reasoning ($0, ~60s)
    LOCAL_CROSS = 3     # 3 local models x 2 runs ($0, ~5min)
    CLOUD_QUICK = 4     # Single cloud model ($0.01, ~5s)
    CLOUD_CROSS = 5     # 3 cloud models x 2 runs ($0.10, ~30s)
    PREMIUM = 6         # 5 models x 3 runs + reproducibility ($0.30, ~2min)
    ENTERPRISE = 7      # Full pipeline + CoVe ($0.50, ~5min)


@dataclass
class CriterionScore:
    """Score for a single evaluation criterion."""
    name: str
    score: float           # 0-100 normalized
    weight: float          # 0.0-1.0
    grade: str             # "Exceptional", "Proficient", etc.
    reasoning: str = ""    # G-Eval reasoning (if available)
    

@dataclass
class EvalResult:
    """Complete evaluation result for a prompt."""
    file_path: str
    title: str
    category: str
    
    # Scores
    overall_score: float           # 0-100 weighted average
    structural_score: float        # 0-100 from static analysis
    geval_score: Optional[float]   # 0-100 from G-Eval (if run)
    
    # Breakdown
    criteria: List[CriterionScore] = field(default_factory=list)
    
    # Metadata
    grade: str = ""                # "Exceptional", "Proficient", etc.
    passed: bool = False           # Met threshold?
    threshold: float = 70.0
    
    # Execution info
    model: str = ""
    tier: int = 2
    duration_seconds: float = 0.0
    timestamp: str = ""
    
    # Recommendations
    recommendations: List[str] = field(default_factory=list)
    issues: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass  
class EvalConfig:
    """Configuration for evaluation run."""
    tier: int = 2
    threshold: float = 70.0
    model: str = "local:phi4mini"
    methods: List[str] = field(default_factory=lambda: ["structural", "geval"])
    rubric_path: Optional[str] = None
    output_format: str = "console"  # console, json, markdown
    output_path: Optional[str] = None
    verbose: bool = False
    parallel: int = 1
    
    # Scoring weights (from prompt-scoring.yaml)
    weights: Dict[str, float] = field(default_factory=lambda: {
        "clarity": 0.25,
        "effectiveness": 0.30,
        "reusability": 0.20,
        "simplicity": 0.15,
        "examples": 0.10,
    })


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_grade(score: float) -> str:
    """Convert score to grade label."""
    if score >= 90:
        return "Exceptional"
    elif score >= 80:
        return "Proficient"
    elif score >= 70:
        return "Competent"
    elif score >= 60:
        return "Developing"
    else:
        return "Inadequate"


def get_grade_emoji(score: float) -> str:
    """Get emoji representation of grade."""
    if score >= 90:
        return "⭐⭐⭐⭐⭐"
    elif score >= 80:
        return "⭐⭐⭐⭐"
    elif score >= 70:
        return "⭐⭐⭐"
    elif score >= 60:
        return "⭐⭐"
    else:
        return "⭐"


def parse_frontmatter(content: str) -> Dict[str, Any]:
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}
    
    try:
        end = content.find("---", 3)
        if end == -1:
            return {}
        yaml_content = content[3:end].strip()
        return yaml.safe_load(yaml_content) or {}
    except Exception:
        return {}


def extract_body(content: str) -> str:
    """Extract body content after frontmatter."""
    if not content.startswith("---"):
        return content
    
    end = content.find("---", 3)
    if end == -1:
        return content
    return content[end + 3:].strip()


# =============================================================================
# STRUCTURAL ANALYZER (Tier 0 - No LLM)
# =============================================================================

class StructuralAnalyzer:
    """
    Static analysis of prompt structure without LLM calls.
    Based on evaluate_library.py criteria.
    """
    
    # Required frontmatter fields
    REQUIRED_FIELDS = ["title", "intro", "category", "type"]
    
    # Expected sections in body
    EXPECTED_SECTIONS = [
        "description", "prompt", "variables", "example", 
        "usage", "tips", "related"
    ]
    
    def analyze(self, file_path: Path) -> EvalResult:
        """Analyze prompt structure and return score."""
        content = file_path.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(content)
        body = extract_body(content).lower()
        
        issues = []
        scores = {}
        
        # 1. Frontmatter completeness (25%)
        present = sum(1 for f in self.REQUIRED_FIELDS if f in frontmatter)
        completeness = (present / len(self.REQUIRED_FIELDS)) * 100
        if completeness < 100:
            missing = [f for f in self.REQUIRED_FIELDS if f not in frontmatter]
            issues.append(f"Missing frontmatter: {', '.join(missing)}")
        scores["completeness"] = completeness
        
        # 2. Section presence (25%)
        sections_found = sum(1 for s in self.EXPECTED_SECTIONS if f"## {s}" in body or f"# {s}" in body)
        section_score = (sections_found / len(self.EXPECTED_SECTIONS)) * 100
        if section_score < 50:
            issues.append(f"Only {sections_found}/{len(self.EXPECTED_SECTIONS)} expected sections found")
        scores["sections"] = section_score
        
        # 3. Example quality (20%)
        has_example = "```" in content or "example" in body
        example_score = 100 if has_example else 0
        if not has_example:
            issues.append("No code examples or example section found")
        scores["examples"] = example_score
        
        # 4. Research foundation (15%)
        has_research = any(term in body for term in ["research", "arxiv", "paper", "study"])
        research_score = 100 if has_research else 50  # Not required, but bonus
        scores["research"] = research_score
        
        # 5. Governance tags (15%)
        has_governance = "governance_tags" in frontmatter or "dataclassification" in str(frontmatter).lower()
        governance_score = 100 if has_governance else 60
        if not has_governance:
            issues.append("Missing governance tags")
        scores["governance"] = governance_score
        
        # Calculate weighted average
        weights = [0.25, 0.25, 0.20, 0.15, 0.15]
        overall = sum(s * w for s, w in zip(scores.values(), weights))
        
        return EvalResult(
            file_path=str(file_path),
            title=frontmatter.get("title", file_path.stem),
            category=frontmatter.get("category", "unknown"),
            overall_score=round(overall, 1),
            structural_score=round(overall, 1),
            geval_score=None,
            criteria=[
                CriterionScore("completeness", scores["completeness"], 0.25, get_grade(scores["completeness"])),
                CriterionScore("sections", scores["sections"], 0.25, get_grade(scores["sections"])),
                CriterionScore("examples", scores["examples"], 0.20, get_grade(scores["examples"])),
                CriterionScore("research", scores["research"], 0.15, get_grade(scores["research"])),
                CriterionScore("governance", scores["governance"], 0.15, get_grade(scores["governance"])),
            ],
            grade=get_grade(overall),
            passed=overall >= 70,
            issues=issues,
            tier=0,
            timestamp=datetime.now().isoformat(),
        )


# =============================================================================
# G-EVAL SCORER (Tier 2+ - Uses LLM)
# =============================================================================

class GEvalScorer:
    """
    G-Eval style LLM-as-judge scoring.
    Imports and uses local_model.py's evaluate_prompt_geval() method.
    """
    
    def __init__(self, model_name: str = "local:phi4mini", verbose: bool = False):
        self.model_name = model_name
        self.verbose = verbose
        self._model = None
        
    def _get_model(self):
        """Lazy load the model."""
        if self._model is None:
            if self.model_name.startswith("local:"):
                from local_model import LocalModel
                self._model = LocalModel(verbose=self.verbose)
            else:
                from llm_client import LLMClient
                self._model = LLMClient()
        return self._model
    
    def evaluate(self, file_path: Path, structural_result: Optional[EvalResult] = None) -> EvalResult:
        """
        Evaluate prompt using G-Eval methodology.
        
        G-Eval (NeurIPS 2023):
        1. Generate evaluation steps (Chain-of-Thought)
        2. LLM judges on 1-5 scale per criterion
        3. Normalize to 0-100
        """
        content = file_path.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(content)
        
        model = self._get_model()
        
        # Use local_model's G-Eval implementation
        if self.model_name.startswith("local:"):
            import time
            start = time.time()
            
            result = model.evaluate_prompt_geval(content)
            
            duration = time.time() - start
            
            # Parse G-Eval result
            overall = result.get("overall", 0)  # 1-10 scale from local_model
            scores = result.get("scores", {})
            criteria_results = result.get("criteria_results", {})
            
            # Build criteria list
            criteria = []
            weight_map = {
                "clarity": 0.25,
                "effectiveness": 0.30,
                "reusability": 0.20,
                "simplicity": 0.15,
                "examples": 0.10,
            }
            
            for name, score in scores.items():
                # Normalize 1-10 to 0-100
                normalized = (score - 1) / 9 * 100 if score > 0 else 0
                reasoning = ""
                if name in criteria_results:
                    cr = criteria_results[name]
                    if isinstance(cr, dict):
                        reasoning = cr.get("summary", "")
                
                criteria.append(CriterionScore(
                    name=name,
                    score=round(normalized, 1),
                    weight=weight_map.get(name, 0.20),
                    grade=get_grade(normalized),
                    reasoning=reasoning[:200] if reasoning else "",
                ))
            
            # Normalize overall from 1-10 to 0-100
            overall_normalized = (overall - 1) / 9 * 100 if overall > 0 else 0
            
            # Combine with structural if available
            if structural_result:
                combined = (structural_result.structural_score * 0.15) + (overall_normalized * 0.85)
            else:
                combined = overall_normalized
            
            return EvalResult(
                file_path=str(file_path),
                title=frontmatter.get("title", file_path.stem),
                category=frontmatter.get("category", "unknown"),
                overall_score=round(combined, 1),
                structural_score=structural_result.structural_score if structural_result else 0,
                geval_score=round(overall_normalized, 1),
                criteria=criteria,
                grade=get_grade(combined),
                passed=combined >= 70,
                model=self.model_name,
                tier=2,
                duration_seconds=round(duration, 1),
                timestamp=datetime.now().isoformat(),
                recommendations=self._generate_recommendations(criteria),
            )
        else:
            # Cloud model path - use llm_client
            raise NotImplementedError("Cloud G-Eval not yet implemented")
    
    def _generate_recommendations(self, criteria: List[CriterionScore]) -> List[str]:
        """Generate improvement recommendations based on lowest scores."""
        recommendations = []
        sorted_criteria = sorted(criteria, key=lambda c: c.score)
        
        for c in sorted_criteria[:2]:  # Bottom 2
            if c.score < 70:
                recommendations.append(f"Improve {c.name}: currently {c.score:.0f}% ({c.grade})")
        
        return recommendations


# =============================================================================
# MAIN EVALUATOR
# =============================================================================

class PromptEval:
    """
    Main evaluation orchestrator.
    
    Usage:
        evaluator = PromptEval(tier=2, threshold=75)
        result = evaluator.evaluate("prompts/example.md")
        results = evaluator.evaluate_directory("prompts/advanced/")
    """
    
    def __init__(
        self,
        tier: int = 2,
        threshold: float = 70.0,
        model: str = "local:phi4mini",
        verbose: bool = False,
        config: Optional[EvalConfig] = None,
    ):
        self.config = config or EvalConfig(
            tier=tier,
            threshold=threshold,
            model=model,
            verbose=verbose,
        )
        self.structural_analyzer = StructuralAnalyzer()
        self.geval_scorer = GEvalScorer(model, verbose) if tier >= 1 else None
        
    def evaluate(self, path: Union[str, Path]) -> EvalResult:
        """Evaluate a single prompt file."""
        file_path = Path(path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Prompt not found: {file_path}")
        
        if not file_path.suffix == ".md":
            raise ValueError(f"Expected .md file, got: {file_path.suffix}")
        
        # Tier 0: Structural only
        structural_result = self.structural_analyzer.analyze(file_path)
        
        if self.config.tier == 0:
            structural_result.tier = 0
            structural_result.passed = structural_result.overall_score >= self.config.threshold
            return structural_result
        
        # Tier 1+: Add G-Eval
        if self.geval_scorer:
            result = self.geval_scorer.evaluate(file_path, structural_result)
            result.threshold = self.config.threshold
            result.passed = result.overall_score >= self.config.threshold
            return result
        
        return structural_result
    
    def evaluate_directory(
        self, 
        path: Union[str, Path],
        exclude_patterns: List[str] = None,
    ) -> List[EvalResult]:
        """Evaluate all prompts in a directory."""
        dir_path = Path(path)
        exclude_patterns = exclude_patterns or ["README.md", "index.md"]
        
        if not dir_path.is_dir():
            raise NotADirectoryError(f"Not a directory: {dir_path}")
        
        results = []
        prompt_files = sorted(dir_path.glob("**/*.md"))
        
        for file_path in prompt_files:
            # Skip excluded files
            if any(p in file_path.name for p in exclude_patterns):
                continue
            
            # Skip archive directories
            if "archive" in str(file_path).lower():
                continue
                
            try:
                result = self.evaluate(file_path)
                results.append(result)
            except Exception as e:
                if self.config.verbose:
                    print(f"Error evaluating {file_path}: {e}")
        
        return results


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def evaluate(
    path: Union[str, Path],
    tier: int = 2,
    threshold: float = 70.0,
    model: str = "local:phi4mini",
) -> EvalResult:
    """
    Evaluate a single prompt file.
    
    Args:
        path: Path to prompt file
        tier: Evaluation tier (0-7)
        threshold: Minimum passing score
        model: Model to use for LLM evaluation
        
    Returns:
        EvalResult with scores and recommendations
    """
    evaluator = PromptEval(tier=tier, threshold=threshold, model=model)
    return evaluator.evaluate(path)


def evaluate_directory(
    path: Union[str, Path],
    tier: int = 2,
    threshold: float = 70.0,
    model: str = "local:phi4mini",
) -> List[EvalResult]:
    """
    Evaluate all prompts in a directory.
    
    Args:
        path: Path to directory
        tier: Evaluation tier (0-7)
        threshold: Minimum passing score
        model: Model to use for LLM evaluation
        
    Returns:
        List of EvalResult for each prompt
    """
    evaluator = PromptEval(tier=tier, threshold=threshold, model=model)
    return evaluator.evaluate_directory(path)


# =============================================================================
# MAIN (for testing)
# =============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="PromptEval - Evaluate prompts")
    parser.add_argument("path", help="Path to prompt file or directory")
    parser.add_argument("-t", "--tier", type=int, default=2, help="Evaluation tier (0-7)")
    parser.add_argument("--threshold", type=float, default=70.0, help="Pass threshold")
    parser.add_argument("-m", "--model", default="local:phi4mini", help="Model to use")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-o", "--output", help="Output file (json)")
    
    args = parser.parse_args()
    
    path = Path(args.path)
    
    if path.is_file():
        result = evaluate(path, tier=args.tier, threshold=args.threshold, model=args.model)
        print(f"\n{'='*60}")
        print(f"File: {result.file_path}")
        print(f"Score: {result.overall_score}% ({result.grade})")
        print(f"Passed: {'✓' if result.passed else '✗'} (threshold: {result.threshold}%)")
        print(f"{'='*60}")
        
        if result.criteria:
            print("\nCriteria:")
            for c in result.criteria:
                print(f"  {c.name}: {c.score:.0f}% ({c.grade})")
        
        if result.recommendations:
            print("\nRecommendations:")
            for r in result.recommendations:
                print(f"  - {r}")
        
        if args.output:
            with open(args.output, "w") as f:
                json.dump(result.to_dict(), f, indent=2)
            print(f"\nSaved to: {args.output}")
    
    elif path.is_dir():
        results = evaluate_directory(path, tier=args.tier, threshold=args.threshold, model=args.model)
        
        passed = sum(1 for r in results if r.passed)
        avg = sum(r.overall_score for r in results) / len(results) if results else 0
        
        print(f"\n{'='*60}")
        print(f"Directory: {path}")
        print(f"Prompts: {len(results)} | Passed: {passed}/{len(results)}")
        print(f"Average: {avg:.1f}%")
        print(f"{'='*60}")
        
        # Show each result
        for r in sorted(results, key=lambda x: x.overall_score, reverse=True):
            status = "✓" if r.passed else "✗"
            print(f"  {status} {r.overall_score:5.1f}% {r.title[:40]}")
        
        if args.output:
            with open(args.output, "w") as f:
                json.dump([r.to_dict() for r in results], f, indent=2)
            print(f"\nSaved to: {args.output}")
    
    else:
        print(f"Error: Path not found: {path}")
        sys.exit(1)
