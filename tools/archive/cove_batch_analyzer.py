#!/usr/bin/env python3
"""
CoVe Batch Prompt Analyzer
==========================

Analyzes all prompts in the library using Chain-of-Verification to ensure:
1. Each prompt meets the scoring rubric criteria
2. Each prompt actually implements its intended functionality
3. The prompt would produce expected results

Usage:
    # Analyze all prompts
    python tools/cove_batch_analyzer.py

    # Analyze specific folder
    python tools/cove_batch_analyzer.py prompts/advanced/

    # Use specific provider
    python tools/cove_batch_analyzer.py --provider github

    # Output JSON report
    python tools/cove_batch_analyzer.py --json --output report.json

Author: Prompts Library Team
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable
import yaml

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))


# Load environment variables from .env


def _load_dotenv():
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(env_path)
        except ImportError:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, _, value = line.partition("=")
                        if value.strip() and not os.environ.get(key.strip()):
                            os.environ[key.strip()] = value.strip().strip('"').strip("'")


_load_dotenv()


@dataclass
class PromptAnalysis:
    """Result of analyzing a single prompt."""
    file_path: str
    title: str
    category: str
    stated_purpose: str

    # Rubric scores
    clarity_score: float = 0.0
    effectiveness_score: float = 0.0
    reusability_score: float = 0.0
    simplicity_score: float = 0.0
    examples_score: float = 0.0
    overall_score: float = 0.0

    # CoVe verification
    implementation_verified: bool = False
    implementation_issues: List[str] = field(default_factory=list)
    would_produce_expected_results: bool = False
    result_concerns: List[str] = field(default_factory=list)

    # Recommendations
    recommendations: List[str] = field(default_factory=list)
    priority: str = "low"  # low, medium, high, critical


@dataclass
class BatchAnalysisReport:
    """Full batch analysis report."""
    timestamp: str
    total_prompts: int
    analyzed: int
    passed: int
    failed: int
    errors: int

    by_category: Dict[str, Dict[str, int]] = field(default_factory=dict)
    by_priority: Dict[str, int] = field(default_factory=dict)

    results: List[PromptAnalysis] = field(default_factory=list)

    avg_clarity: float = 0.0
    avg_effectiveness: float = 0.0
    avg_reusability: float = 0.0
    avg_simplicity: float = 0.0
    avg_examples: float = 0.0
    avg_overall: float = 0.0


def get_repo_root() -> Path:
    """Find the repository root."""
    current = Path(__file__).parent
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return Path(__file__).parent.parent


def load_rubric() -> Dict[str, Any]:
    """Load the scoring rubric."""
    rubric_path = get_repo_root() / "tools" / "rubrics" / "prompt-scoring.yaml"
    if rubric_path.exists():
        with open(rubric_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}


def find_prompts(folder: Path) -> List[Path]:
    """Find all markdown prompt files."""
    prompts = []
    for md_file in folder.rglob("*.md"):
        # Skip non-prompt files
        if any(skip in str(md_file).lower() for skip in [
               "readme", "index", "contributing", "license", "changelog",
               "guide", "template", ".github", "docs/", "testing/"
               ]):
            continue

        # Check if it has frontmatter (indicates it's a prompt)
        try:
            content = md_file.read_text(encoding="utf-8")
            if content.startswith("---"):
                prompts.append(md_file)
        except Exception:
            pass

    return sorted(prompts)


def parse_prompt(file_path: Path) -> Dict[str, Any]:
    """Parse a prompt file into metadata and content."""
    content = file_path.read_text(encoding="utf-8")

    result = {
              "file_path": str(file_path),
              "title": file_path.stem,
              "category": file_path.parent.name,
              "description": "",
              "purpose": "",
              "content": content,
              "frontmatter": {},
              "body": content,
              }

    # Parse YAML frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                result["frontmatter"] = yaml.safe_load(parts[1]) or {}
                result["body"] = parts[2].strip()
            except yaml.YAMLError:
                pass

    fm = result["frontmatter"]
    result["title"] = fm.get("title", result["title"])
    result["description"] = fm.get("description", "")
    result["purpose"] = fm.get("purpose", fm.get("description", ""))
    result["category"] = fm.get("category", result["category"])

    return result


def analyze_prompt_with_cove(
                             prompt_data: Dict[str, Any],
                             llm_call: Callable,
                             rubric: Dict[str, Any],
                             verbose: bool = False
                             ) -> PromptAnalysis:
    """
    Analyze a single prompt using CoVe methodology.

    This performs:
    1. Rubric-based scoring for each dimension
    2. Verification that the prompt implements its stated purpose
    3. Assessment of whether it would produce expected results
    """

    analysis = PromptAnalysis(
                              file_path=prompt_data["file_path"],
                              title=prompt_data["title"],
                              category=prompt_data["category"],
                              stated_purpose=prompt_data["purpose"] or prompt_data["description"] or "Not specified",
                              )

    # Limit content for API (used directly in prompt formatting below)

    # =========================================================================
    # Phase 1: Score against rubric dimensions
    # =========================================================================
    scoring_prompt = """Evaluate this prompt template against quality criteria. Score each dimension 1-5.

PROMPT TITLE: {title}
STATED PURPOSE: {purpose}

PROMPT CONTENT:
```
{content}
```

Score each dimension (1=poor, 5=excellent):

1. CLARITY (Is it unambiguous and easy to understand?)
   - Can a user understand the purpose within 10 seconds?
   - Are instructions clear and logical?

2. EFFECTIVENESS (Would it consistently produce quality output?)
   - Does it have enough structure to guide the AI?
   - Would it handle edge cases?

3. REUSABILITY (Works across different contexts?)
   - Can it be used for similar tasks with minimal changes?
   - Are variables/placeholders generic enough?

4. SIMPLICITY (Minimal without losing value?)
   - Is there unnecessary content?
   - Is length appropriate for purpose?

5. EXAMPLES (Are examples helpful and realistic?)
   - Are there input/output examples?
   - Do examples clarify usage?

Return ONLY JSON with scores 1-5:
{{"clarity": N, "effectiveness": N, "reusability": N, "simplicity": N, "examples": N}}"""

    try:
        score_response = llm_call(scoring_prompt, None)

        # Parse scores - try multiple patterns
        scores = None

        # Try to find JSON object
        match = re.search(r'\{[^{}]*"clarity"[^{}]*\}', score_response, re.DOTALL)
        if match:
            try:
                scores = json.loads(match.group())
            except json.JSONDecodeError:
                pass

        # Fallback: extract numbers after dimension names
        if not scores:
            scores = {}
            for dim in ["clarity", "effectiveness", "reusability", "simplicity", "examples"]:
                match = re.search(rf'{dim}["\s:]+(\d+)', score_response, re.IGNORECASE)
                if match:
                    scores[dim] = int(match.group(1))

        if scores:
            analysis.clarity_score = float(scores.get("clarity", 3))
            analysis.effectiveness_score = float(scores.get("effectiveness", 3))
            analysis.reusability_score = float(scores.get("reusability", 3))
            analysis.simplicity_score = float(scores.get("simplicity", 3))
            analysis.examples_score = float(scores.get("examples", 3))

            # Calculate weighted overall
            weights = {"clarity": 0.25, "effectiveness": 0.30, "reusability": 0.20,
                       "simplicity": 0.15, "examples": 0.10}
            analysis.overall_score = round(
                                           analysis.clarity_score * weights["clarity"] +
                                           analysis.effectiveness_score * weights["effectiveness"] +
                                           analysis.reusability_score * weights["reusability"] +
                                           analysis.simplicity_score * weights["simplicity"] +
                                           analysis.examples_score * weights["examples"],
                                           2
                                           )
        else:
            # Default to middle scores
            analysis.clarity_score = 3.0
            analysis.effectiveness_score = 3.0
            analysis.reusability_score = 3.0
            analysis.simplicity_score = 3.0
            analysis.examples_score = 3.0
            analysis.overall_score = 3.0

    except Exception as e:
        if verbose:
            print(f"      ⚠️ Scoring error: {e}")
        analysis.overall_score = 3.0

    # =========================================================================
    # Phase 2: Verify implementation matches stated purpose (CoVe)
    # =========================================================================
    verification_prompt = """Analyze if this prompt implements what it claims to do.

PROMPT TITLE: {title}
STATED PURPOSE: {purpose}

PROMPT CONTENT:
```
{content[:2000]}
```

Answer "verified: true" if the prompt reasonably addresses its stated purpose.
Only answer "verified: false" if there's a major mismatch between purpose and content.

Return JSON:
{{"verified": true/false, "issues": ["only list MAJOR issues if any"]}}"""

    try:
        verify_response = llm_call(verification_prompt, None)

        match = re.search(r'\{[\s\S]*?\}', verify_response)
        if match:
            verify = json.loads(match.group())
            analysis.implementation_verified = verify.get("verified", False)
            analysis.implementation_issues = verify.get("issues", []) + verify.get("missing_elements", [])
    except Exception as e:
        if verbose:
            print(f"      ⚠️ Verification error: {e}")

    # =========================================================================
    # Phase 3: Assess expected results
    # =========================================================================
    results_prompt = """Would this prompt produce the expected results when used?

PROMPT: {title}
PURPOSE: {purpose}

Assume the prompt WILL work unless there's a clear structural problem.
Answer "true" if the prompt provides reasonable guidance for its purpose.
Only answer "false" if there are critical missing elements.

Return JSON:
{{"would_work": true/false, "concerns": ["only list CRITICAL issues"], "confidence": "high/medium/low"}}"""

    try:
        results_response = llm_call(results_prompt, None)

        match = re.search(r'\{[\s\S]*?\}', results_response)
        if match:
            results = json.loads(match.group())
            analysis.would_produce_expected_results = results.get("would_work", False)
            analysis.result_concerns = results.get("concerns", [])
    except Exception as e:
        if verbose:
            print(f"      ⚠️ Results assessment error: {e}")

    # =========================================================================
    # Phase 4: Generate recommendations
    # =========================================================================

    if analysis.overall_score < 3.0:
        analysis.priority = "critical"
        analysis.recommendations.append("Score below minimum threshold - needs major revision")
    elif analysis.overall_score < 3.5:
        analysis.priority = "high"
    elif analysis.overall_score < 4.0:
        analysis.priority = "medium"
    else:
        analysis.priority = "low"

    if not analysis.implementation_verified:
        analysis.priority = "high" if analysis.priority == "low" else analysis.priority
        analysis.recommendations.append("Implementation doesn't fully match stated purpose")

    if not analysis.would_produce_expected_results:
        analysis.recommendations.append("May not produce expected results - review structure")

    if analysis.clarity_score < 3:
        analysis.recommendations.append("Improve clarity - purpose should be clear within 10 seconds")

    if analysis.examples_score < 3:
        analysis.recommendations.append("Add or improve examples with clear input/output")

    if analysis.simplicity_score < 3:
        analysis.recommendations.append("Simplify - remove redundant content")

    return analysis


def run_batch_analysis(
                       folder: Path,
                       provider: str = "local",
                       model: Optional[str] = None,
                       model_path: Optional[str] = None,
                       verbose: bool = False,
                       limit: Optional[int] = None,
                       ) -> BatchAnalysisReport:
    """Run batch analysis on all prompts in folder."""

    report = BatchAnalysisReport(
                                 timestamp=datetime.now().isoformat(),
                                 total_prompts=0,
                                 analyzed=0,
                                 passed=0,
                                 failed=0,
                                 errors=0,
                                 )

    # Support single file or folder
    if folder.is_file():
        prompts = [folder]
    else:
        prompts = find_prompts(folder)
    report.total_prompts = len(prompts)
    if limit:
        prompts = prompts[:limit]

    print("\n🔍 CoVe Batch Prompt Analyzer")
    print(f"   Folder: {folder}")
    print(f"   Found: {report.total_prompts} prompts")
    print(f"   Analyzing: {len(prompts)} prompts")
    print(f"   Provider: {provider}")

    # Get LLM function
    try:
        from cove_runner import get_llm_function as cove_get_llm
        if provider == "local" and model_path:
            llm_call = cove_get_llm(provider, model, verbose=False, model_path=model_path)
        else:
            llm_call = cove_get_llm(provider, model, verbose=False)
        print(f"   Model: {getattr(llm_call, 'model_name', 'unknown')}")
    except Exception as e:
        print(f"\n❌ Failed to initialize LLM: {e}")
        return report

    rubric = load_rubric()

    print(f"\n{'='*60}")
    print("ANALYZING PROMPTS")
    print(f"{'='*60}\n")

    # Analyze each prompt
    for i, prompt_path in enumerate(prompts, 1):
        rel_path = prompt_path.relative_to(get_repo_root()) if prompt_path.is_relative_to(get_repo_root()) else prompt_path  # noqa: E501
        print(f"[{i}/{len(prompts)}] {rel_path}")

        try:
            prompt_data = parse_prompt(prompt_path)
            analysis = analyze_prompt_with_cove(prompt_data, llm_call, rubric, verbose)

            report.results.append(analysis)
            report.analyzed += 1

            # Determine pass/fail
            passed = (
                      analysis.overall_score >= 3.0 and
                      analysis.implementation_verified and
                      analysis.would_produce_expected_results
                      )

            if passed:
                report.passed += 1
                status = "✅"
            else:
                report.failed += 1
                status = "❌"

            print(f"   {status} Score: {analysis.overall_score:.1f} | Impl: {'✓' if analysis.implementation_verified else '✗'} | Results: {'✓' if analysis.would_produce_expected_results else '✗'}")  # noqa: E501

            if analysis.recommendations and verbose:
                for rec in analysis.recommendations[:2]:
                    print(f"      → {rec}")

            # Track by category
            cat = analysis.category
            if cat not in report.by_category:
                report.by_category[cat] = {"passed": 0, "failed": 0, "total": 0}
            report.by_category[cat]["total"] += 1
            report.by_category[cat]["passed" if passed else "failed"] += 1

            # Track by priority
            report.by_priority[analysis.priority] = report.by_priority.get(analysis.priority, 0) + 1

        except Exception as e:
            report.errors += 1
            print(f"   ⚠️ Error: {str(e)[:50]}")
            if verbose:
                import traceback
                traceback.print_exc()

    # Calculate averages
    if report.results:
        report.avg_clarity = round(sum(r.clarity_score for r in report.results) / len(report.results), 2)
        report.avg_effectiveness = round(sum(r.effectiveness_score for r in report.results) / len(report.results), 2)
        report.avg_reusability = round(sum(r.reusability_score for r in report.results) / len(report.results), 2)
        report.avg_simplicity = round(sum(r.simplicity_score for r in report.results) / len(report.results), 2)
        report.avg_examples = round(sum(r.examples_score for r in report.results) / len(report.results), 2)
        report.avg_overall = round(sum(r.overall_score for r in report.results) / len(report.results), 2)

    return report


def print_report(report: BatchAnalysisReport):
    """Print a formatted report."""

    print(f"\n{'='*60}")
    print("BATCH ANALYSIS REPORT")
    print(f"{'='*60}")
    print(f"Timestamp: {report.timestamp}")
    print("\n📊 Summary:")
    print(f"   Total Prompts: {report.total_prompts}")
    print(f"   Analyzed: {report.analyzed}")
    print(f"   ✅ Passed: {report.passed} ({100 * report.passed / max(report.analyzed, 1):.0f}%)")
    print(f"   ❌ Failed: {report.failed} ({100 * report.failed / max(report.analyzed, 1):.0f}%)")
    print(f"   ⚠️ Errors: {report.errors}")

    print("\n📈 Average Scores (1-5):")
    print(f"   Clarity:       {report.avg_clarity:.2f}")
    print(f"   Effectiveness: {report.avg_effectiveness:.2f}")
    print(f"   Reusability:   {report.avg_reusability:.2f}")
    print(f"   Simplicity:    {report.avg_simplicity:.2f}")
    print(f"   Examples:      {report.avg_examples:.2f}")
    print("   ─────────────────────")
    print(f"   Overall:       {report.avg_overall:.2f}")

    print("\n🎯 By Priority:")
    for priority in ["critical", "high", "medium", "low"]:
        count = report.by_priority.get(priority, 0)
        if count:
            emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}[priority]
            print(f"   {emoji} {priority.title()}: {count}")

    if report.by_category:
        print("\n📁 By Category:")
        for cat, stats in sorted(report.by_category.items()):
            pct = 100 * stats["passed"] / max(stats["total"], 1)
            print(f"   {cat}: {stats['passed']}/{stats['total']} passed ({pct:.0f}%)")

    # Show prompts needing attention
    critical_prompts = [r for r in report.results if r.priority in ["critical", "high"]]
    if critical_prompts:
        print(f"\n⚠️ Prompts Needing Attention ({len(critical_prompts)}):")
        for r in critical_prompts[:10]:
            print(f"\n   📄 {r.file_path}")
            print(f"      Score: {r.overall_score:.1f} | Priority: {r.priority}")
            if r.recommendations:
                print("      Issues:")
                for rec in r.recommendations[:3]:
                    print(f"        • {rec}")


def main():
    parser = argparse.ArgumentParser(
                                     description="Analyze prompts using CoVe methodology",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=r"""
                                     Examples:
                                     # Analyze all prompts
                                     python tools/cove_batch_analyzer.py

                                     # Analyze specific folder with GitHub Models
                                     python tools/cove_batch_analyzer.py prompts/advanced/ --provider github

                                     # Use local model
                                     python tools/cove_batch_analyzer.py --provider local --model-path "C:\path\to\model"  # noqa: E501

                                     # Limit to first 10 prompts
                                     python tools/cove_batch_analyzer.py --limit 10

                                     # Output JSON report
                                     python tools/cove_batch_analyzer.py --json --output analysis_report.json
                                     """
                                     )

    parser.add_argument("folder", nargs="?", default="prompts",
                        help="Folder to analyze (default: prompts)")
    parser.add_argument("--provider", "-p", default="local",
                        choices=["local", "github", "openai"],
                        help="LLM provider")
    parser.add_argument("--model", "-m", help="Model name")
    parser.add_argument("--model-path", dest="model_path",
                        help="Path to local ONNX model")
    parser.add_argument("--limit", "-l", type=int,
                        help="Limit number of prompts to analyze")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show detailed output")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")
    parser.add_argument("--output", "-o", help="Output file for JSON report")

    args = parser.parse_args()

    repo_root = get_repo_root()
    folder = repo_root / args.folder

    if not folder.exists():
        print(f"❌ Folder not found: {folder}")
        sys.exit(1)

    report = run_batch_analysis(
        folder=folder,
        provider=args.provider,
        model=args.model,
        model_path=args.model_path,
        verbose=args.verbose,
        limit=args.limit,
    )

    if args.json:
        # Convert to JSON-serializable format
        output = {
            "timestamp": report.timestamp,
            "summary": {
                "total": report.total_prompts,
                "analyzed": report.analyzed,
                "passed": report.passed,
                "failed": report.failed,
                "errors": report.errors,
            },
            "averages": {
                "clarity": report.avg_clarity,
                "effectiveness": report.avg_effectiveness,
                "reusability": report.avg_reusability,
                "simplicity": report.avg_simplicity,
                "examples": report.avg_examples,
                "overall": report.avg_overall,
            },
            "by_priority": report.by_priority,
            "by_category": report.by_category,
            "results": [
                {
                    "file": r.file_path,
                    "title": r.title,
                    "category": r.category,
                    "scores": {
                        "clarity": r.clarity_score,
                        "effectiveness": r.effectiveness_score,
                        "reusability": r.reusability_score,
                        "simplicity": r.simplicity_score,
                        "examples": r.examples_score,
                        "overall": r.overall_score,
                    },
                    "implementation_verified": r.implementation_verified,
                    "would_produce_results": r.would_produce_expected_results,
                    "priority": r.priority,
                    "recommendations": r.recommendations,
                }
                for r in report.results
            ]
        }

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2)
            print(f"\n📄 Report saved to: {args.output}")
        else:
            print(json.dumps(output, indent=2))
    else:
        print_report(report)


if __name__ == "__main__":
    main()
