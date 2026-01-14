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
import re
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

# NOTE:
# PromptEval is now invoked via package structure:
#   - Console script: `prompteval` (defined in pyproject.toml)
#   - Module: `python -m tools.prompteval`
# All imports use proper package paths.

from tools.prompteval.config import EvalConfig, EvalResult, Tier, CriterionScore
from tools.llm_client import LLMClient
from tools.model_probe import ModelProbe


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
    content = content.lstrip()
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
    content = content.lstrip()
    if not content.startswith("---"):
        return content
    
    end = content.find("---", 3)
    if end == -1:
        return content
    return content[end + 3:].strip()


# =============================================================================
# CORE CLASS
# =============================================================================

class PromptEval:
    """
    Unified evaluation engine for prompts.
    Orchestrates structural analysis and LLM-based evaluation logic.
    """

    def __init__(self, config: Optional[EvalConfig] = None):
        self.config = config or EvalConfig()
        self.probe = ModelProbe()
        self.llm_client = LLMClient() 

    def _ensure_model_availability(self):
        """Check if the requested model is available, unless running structural only."""
        if self.config.tier == Tier.STRUCTURAL:
            return

        # Check availability
        status = self.probe.check_model(self.config.model)
        if not status.usable:
            if self.config.model.startswith("local:"):
                print(f"Warning: Model {self.config.model} not found locally.")
            else:
                print(f"Warning: Remote model {self.config.model} may not be accessible.")
    
    def evaluate_file(self, file_path: Path) -> EvalResult:
        """Run full evaluation pipeline on a single file."""
        self._ensure_model_availability()
        start_time = time.time()
        
        # 1. Read file
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            return self._create_error_result(file_path, str(e))

        # 2. Structural Analysis (Always run)
        structural_result = self._run_structural_analysis(file_path, content)
        
        # If structural only, return
        if self.config.tier == Tier.STRUCTURAL:
            structural_result.duration_seconds = time.time() - start_time
            return structural_result

        # 3. LLM Evaluation (G-Eval / CoT)
        try:
            geval_result = self._run_geval(content)
            
            # Merge results
            combined = self._merge_results(structural_result, geval_result)
            combined.duration_seconds = time.time() - start_time
            return combined
            
        except Exception as e:
            print(f"LLM Evaluation failed for {file_path.name}: {e}")
            structural_result.issues.append(f"LLM Eval failed: {str(e)}")
            structural_result.duration_seconds = time.time() - start_time
            return structural_result

    def scan_directory(self, path: Path) -> List[EvalResult]:
        """Scan a directory for prompt files and evaluate them."""
        results = []
        pattern = "**/*.md" if self.config.recursive else "*.md"
        
        if not path.exists():
            print(f"Error: Path {path} not found.")
            return []

        if path.is_file():
            return [self.evaluate_file(path)]

        files = sorted(list(path.glob(pattern)))
        # Filter out non-prompts
        files = [f for f in files if self._is_prompt_file(f)]
        
        total = len(files)
        print(f"Scanning {total} files in {path}...")
        
        for i, f in enumerate(files, 1):
            if self.config.verbose:
                print(f"[{i}/{total}] Evaluating {f.name}...")
            
            try:
                res = self.evaluate_file(f)
                results.append(res)
                
                # Simple progress char if not verbose
                if not self.config.verbose:
                    status = "✓" if res.passed else "✗"
                    print(status, end="", flush=True)
                    
            except Exception as e:
                print(f"Error evaluating {f}: {e}")
                
        if not self.config.verbose:
            print() # Newline after progress dots
            
        return results

    def _is_prompt_file(self, path: Path) -> bool:
        """Filter helper to exclude non-prompt markdown files."""
        if path.name.lower() in ["readme.md", "index.md", "contributing.md", "changelog.md"]:
            return False
        if "_archive" in str(path) or "archive" in str(path).lower():
            return False
        return True

    def _create_error_result(self, path: Path, error: str) -> EvalResult:
        """Create a failed result object."""
        return EvalResult(
            file_path=str(path),
            title=path.stem,
            category="error",
            overall_score=0,
            structural_score=0,
            geval_score=0,
            passed=False,
            issues=[error],
            timestamp=datetime.now().isoformat()
        )

    def _run_structural_analysis(self, path: Path, content: str) -> EvalResult:
        """Static analysis of prompt structure."""
        frontmatter = parse_frontmatter(content)
        body = extract_body(content).lower()
        
        issues = []
        scores = {}
        
        # Criteria definition
        # Align with `reference/frontmatter-schema.md`
        REQUIRED_FIELDS = ["title", "intro", "type"]
        # Align with `templates/prompt-template.md` (keep lightweight for Tier 0)
        EXPECTED_SECTIONS = ["description", "prompt", "variables", "example"]
        
        # 1. Frontmatter
        present = sum(1 for f in REQUIRED_FIELDS if f in frontmatter)
        completeness = (present / len(REQUIRED_FIELDS)) * 100 if REQUIRED_FIELDS else 100
        if completeness < 100:
            missing = [f for f in REQUIRED_FIELDS if f not in frontmatter]
            issues.append(f"Missing frontmatter: {', '.join(missing)}")
        scores["completeness"] = completeness
        
        # 2. Sections
        sections_found = sum(1 for s in EXPECTED_SECTIONS if f"## {s}" in body or f"# {s}" in body)
        section_score = (sections_found / len(EXPECTED_SECTIONS)) * 100 if EXPECTED_SECTIONS else 100
        if section_score < 50:
            issues.append(f"Only {sections_found}/{len(EXPECTED_SECTIONS)} expected sections found")
        scores["sections"] = section_score
        
        # 3. Examples
        has_example = "```" in content or "example" in body
        example_score = 100 if has_example else 0
        if not has_example:
            issues.append("No code examples or example section")
        scores["examples"] = example_score

        # Calculate score
        weights = {"completeness": 0.3, "sections": 0.4, "examples": 0.3}
        overall = sum(scores[k] * weights[k] for k in scores)
        
        return EvalResult(
            file_path=str(path),
            title=frontmatter.get("title", path.stem),
            category=frontmatter.get("category", "unknown"),
            overall_score=round(overall, 1),
            structural_score=round(overall, 1),
            geval_score=None,
            criteria=[
                CriterionScore("structure_completeness", scores["completeness"], 0.3, get_grade(scores["completeness"])),
                CriterionScore("structure_sections", scores["sections"], 0.4, get_grade(scores["sections"])),
                CriterionScore("structure_examples", scores["examples"], 0.3, get_grade(scores["examples"])),
            ],
            grade=get_grade(overall),
            passed=overall >= self.config.threshold,
            issues=issues,
            tier=Tier.STRUCTURAL.value,
            timestamp=datetime.now().isoformat(),
            model="static-analysis"
        )

    def _run_geval(self, content: str) -> Dict[str, Any]:
        """
        Run G-Eval with Chain-of-Thought using LLMClient.
        Adapted from tools/local_model.py
        """
        # Define G-Eval criteria
        criteria_defs = {
            "clarity": "How easy the prompt is to understand and follow. Clear instructions, no ambiguity.",
            "effectiveness": "How likely the prompt is to produce high quality results. Specificity, constraints.",
            "safety": "Assessing if the prompt encourages safe, unbiased, and responsible generation.",
        }
        
        results = {}
        
        for name, desc in criteria_defs.items():
            prompt_text = f"You are an expert AI prompt evaluator.\nEvaluate the following prompt for {name.upper()}.\n\nDefinition: {desc}\n\nEvaluation Steps:\n1. Read the prompt carefully.\n2. Identify strengths and weaknesses related to {name}.\n3. Assign a score from 1-5 (5 is best).\n\nPROMPT:\n```\n{content[:3000]}\n```\n\nResponse Format (JSON ONLY):\n{{\n    \"reasoning\": \"brief explanation\",\n    \"score\": <number 1-5>\n}}\n"
            try:
                # Use LLMClient to generate
                response = self.llm_client.generate_text(
                    model_name=self.config.model,
                    prompt=prompt_text,
                    temperature=0.1,
                    max_tokens=500
                )
                
                # Parse JSON
                data = self._parse_json_response(response)
                score = float(data.get("score", 0)) * 20  # content to 0-100
                results[name] = {
                    "score": score,
                    "reasoning": data.get("reasoning", "")
                }
            except Exception as e:
                # Fallback
                results[name] = {"score": 0, "reasoning": f"Error: {str(e)}"}
        
        return results

    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        """Robust JSON extraction."""
        text = text.strip()
        # Remove code blocks
        if "```" in text:
            match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
            if match:
                text = match.group(1)
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Simple regex fallback for score
            score_match = re.search(r'"score":\s*([\d\.]+)', text)
            reasoning_match = re.search(r'"reasoning":\s*"([^"]+)"', text)
            return {
                "score": float(score_match.group(1)) if score_match else 0,
                "reasoning": reasoning_match.group(1) if reasoning_match else "Could not parse reasoning"
            }

    def _merge_results(self, structural: EvalResult, geval_results: Dict[str, Any]) -> EvalResult:
        """Combine structural and G-Eval scores."""
        structural.tier = self.config.tier.value if isinstance(self.config.tier, Tier) else self.config.tier
        structural.model = self.config.model
        
        # Add G-Eval criteria
        geval_scores = []
        for name, data in geval_results.items():
            s = data["score"]
            structural.criteria.append(CriterionScore(
                name=f"geval_{name}",
                score=s,
                weight=0.2, # Simplified equal weighting for now
                grade=get_grade(s),
                reasoning=data["reasoning"]
            ))
            geval_scores.append(s)
            
        # Update overall score (50% structural, 50% G-Eval)
        avg_geval = sum(geval_scores) / len(geval_scores) if geval_scores else 0
        structural.geval_score = round(avg_geval, 1)
        
        new_overall = (structural.structural_score * 0.4) + (avg_geval * 0.6)
        structural.overall_score = round(new_overall, 1)
        structural.grade = get_grade(new_overall)
        structural.passed = new_overall >= self.config.threshold
        
        return structural


# =============================================================================
# PUBLIC API (re-exported by prompteval.__init__)
# =============================================================================

def evaluate(path: str | Path, config: Optional[EvalConfig] = None) -> EvalResult:
    """Evaluate a single prompt file."""
    p = Path(path)
    cfg = config or EvalConfig(path=p)
    return PromptEval(cfg).evaluate_file(p)


def evaluate_directory(path: str | Path, config: Optional[EvalConfig] = None) -> List[EvalResult]:
    """Evaluate all prompt files in a directory (respects config.recursive)."""
    p = Path(path)
    cfg = config or EvalConfig(path=p)
    return PromptEval(cfg).scan_directory(p)
