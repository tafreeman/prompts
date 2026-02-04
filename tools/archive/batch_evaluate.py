#!/usr/bin/env python3
"""Batch Evaluation Script for Prompt Library.

Scans all prompts in the prompts/ directory, identifies prompts with
'effectivenessScore: pending', runs evaluation on each, and optionally
updates frontmatter with calculated scores.

Usage:
    # Dry run - show what would be evaluated
    python tools/batch_evaluate.py --dry-run

    # Evaluate all pending prompts
    python tools/batch_evaluate.py

    # Evaluate specific folder
    python tools/batch_evaluate.py --folder prompts/developers/

    # Limit to N prompts
    python tools/batch_evaluate.py --limit 5

    # Skip prompts that have been evaluated before
    python tools/batch_evaluate.py --skip-scored

    # Output report to specific file
    python tools/batch_evaluate.py --output reports/batch_eval_report.md

Author: Prompts Library Team
Version: 1.0.0
"""

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

# =============================================================================
# CONFIGURATION
# =============================================================================

# Default paths
DEFAULT_PROMPTS_DIR = "prompts"
DEFAULT_OUTPUT_DIR = "docs/reports"

# Files to exclude from evaluation
EXCLUDED_FILES = {
    "README.md",
    "index.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
}

# File patterns to exclude
EXCLUDED_PATTERNS = [
    r"\.agent\.md$",
    r"\.instructions\.md$",
    r"\.template\.md$",
]

# Directories to exclude
EXCLUDED_DIRS = {
    "archive",
    "templates",
    "examples",
    ".git",
    "__pycache__",
    "node_modules",
}

# Minimum score threshold for passing
PASS_THRESHOLD = 7.0


# =============================================================================
# DATA CLASSES
# =============================================================================


@dataclass
class PromptInfo:
    """Information about a single prompt file."""

    file_path: Path
    title: str = ""
    current_score: Optional[float] = None
    score_status: str = "unknown"  # "pending", "scored", "missing"
    frontmatter: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EvaluationResult:
    """Result from evaluating a single prompt."""

    prompt: PromptInfo
    new_score: Optional[float] = None
    grade: str = "N/A"
    passed: bool = False
    error: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchReport:
    """Summary report for batch evaluation."""

    timestamp: str
    total_prompts: int = 0
    evaluated: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    errors: int = 0
    average_score: float = 0.0
    results: List[EvaluationResult] = field(default_factory=list)


# =============================================================================
# FRONTMATTER UTILITIES
# =============================================================================


def parse_frontmatter(content: str) -> Tuple[Optional[Dict[str, Any]], str, str]:
    """Parse YAML frontmatter from markdown content.

    Returns:
        Tuple of (frontmatter_dict, frontmatter_text, body)
    """
    if not content.startswith("---"):
        return None, "", content

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return None, "", content

    fm_text = match.group(1)
    body = content[match.end() :]

    try:
        fm = yaml.safe_load(fm_text)
        return fm, fm_text, body
    except yaml.YAMLError:
        return None, fm_text, body


def update_frontmatter_score(
    filepath: Path, new_score: float, dry_run: bool = False
) -> bool:
    """Update the effectivenessScore in a prompt file's frontmatter.

    Args:
        filepath: Path to the markdown file
        new_score: The new score to set
        dry_run: If True, don't actually modify the file

    Returns:
        True if successful, False otherwise
    """
    try:
        content = filepath.read_text(encoding="utf-8")
        fm, fm_text, body = parse_frontmatter(content)

        if fm is None:
            print(f"  ⚠️  No frontmatter found in {filepath}")
            return False

        # Update the score
        fm["effectivenessScore"] = round(new_score, 1)

        # Update the date
        fm["date"] = datetime.now().strftime("%Y-%m-%d")

        if dry_run:
            print(
                f"  [DRY RUN] Would update {filepath.name}: effectivenessScore = {new_score:.1f}"
            )
            return True

        # Rebuild frontmatter
        new_fm_text = yaml.dump(
            fm, default_flow_style=False, allow_unicode=True, sort_keys=False
        )
        new_content = f"---\n{new_fm_text}---\n{body}"

        filepath.write_text(new_content, encoding="utf-8")
        print(f"  ✅ Updated {filepath.name}: effectivenessScore = {new_score:.1f}")
        return True

    except Exception as e:
        print(f"  ❌ Error updating {filepath}: {e}")
        return False


# =============================================================================
# PROMPT DISCOVERY
# =============================================================================


def is_excluded(filepath: Path) -> bool:
    """Check if a file should be excluded from evaluation."""
    # Check filename
    if filepath.name in EXCLUDED_FILES:
        return True

    # Check patterns
    for pattern in EXCLUDED_PATTERNS:
        if re.search(pattern, filepath.name):
            return True

    # Check directory
    for part in filepath.parts:
        if part in EXCLUDED_DIRS:
            return True

    return False


def discover_prompts(base_dir: Path, folder: Optional[str] = None) -> List[PromptInfo]:
    """Discover all prompt files in the given directory.

    Args:
        base_dir: Base directory to search
        folder: Optional specific folder to search within base_dir

    Returns:
        List of PromptInfo objects
    """
    prompts = []

    search_dir = base_dir / folder if folder else base_dir / DEFAULT_PROMPTS_DIR

    if not search_dir.exists():
        print(f"⚠️  Directory not found: {search_dir}")
        return prompts

    for md_file in search_dir.rglob("*.md"):
        if is_excluded(md_file):
            continue

        try:
            content = md_file.read_text(encoding="utf-8")
            fm, _, _ = parse_frontmatter(content)

            if fm is None:
                continue

            info = PromptInfo(
                file_path=md_file, title=fm.get("title", md_file.stem), frontmatter=fm
            )

            # Check score status
            score = fm.get("effectivenessScore")
            if score is None:
                info.score_status = "missing"
                info.current_score = None
            elif score == "pending":
                info.score_status = "pending"
                info.current_score = None
            else:
                try:
                    info.current_score = float(score)
                    info.score_status = "scored"
                except (ValueError, TypeError):
                    info.score_status = "invalid"

            prompts.append(info)

        except Exception as e:
            print(f"⚠️  Error reading {md_file}: {e}")

    return prompts


def filter_pending_prompts(
    prompts: List[PromptInfo], skip_scored: bool = False
) -> List[PromptInfo]:
    """Filter prompts to only those needing evaluation.

    Args:
        prompts: List of all discovered prompts
        skip_scored: If True, skip prompts that already have a score

    Returns:
        List of prompts needing evaluation
    """
    if skip_scored:
        return [p for p in prompts if p.score_status in ("pending", "missing")]
    else:
        return [p for p in prompts if p.score_status == "pending"]


# =============================================================================
# EVALUATION
# =============================================================================


def run_dual_eval(filepath: Path, runs: int = 2) -> EvaluationResult:
    """Run dual_eval.py on a single prompt file.

    Args:
        filepath: Path to the prompt file
        runs: Number of evaluation runs per model

    Returns:
        EvaluationResult with the evaluation outcome
    """
    result = EvaluationResult(prompt=PromptInfo(file_path=filepath))

    try:
        # Determine script path
        script_dir = Path(__file__).parent.parent
        dual_eval_path = script_dir / "testing" / "evals" / "dual_eval.py"

        if not dual_eval_path.exists():
            # Try alternative location
            dual_eval_path = Path("testing/evals/dual_eval.py")

        if not dual_eval_path.exists():
            result.error = "dual_eval.py not found"
            return result

        # Run the evaluation
        cmd = [
            sys.executable,
            str(dual_eval_path),
            str(filepath),
            "--runs",
            str(runs),
            "--json",  # Request JSON output if supported
        ]

        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            cwd=str(Path(__file__).parent.parent),
        )

        # Parse output
        output = proc.stdout + proc.stderr

        # Try to extract score from output
        # Look for consensus score pattern
        score_match = re.search(
            r"Consensus Score[:\s]+(\d+\.?\d*)/10", output, re.IGNORECASE
        )
        if score_match:
            result.new_score = float(score_match.group(1))

        # Look for grade
        grade_match = re.search(r"Final Grade[:\s]+([A-F][+-]?)", output, re.IGNORECASE)
        if grade_match:
            result.grade = grade_match.group(1)

        # Look for pass/fail
        if "PASS" in output.upper():
            result.passed = True
        elif "FAIL" in output.upper():
            result.passed = False

        # If we couldn't extract a score, check for errors
        if result.new_score is None:
            if proc.returncode != 0:
                result.error = f"Evaluation failed (exit code {proc.returncode})"
            else:
                # Try alternative score extraction
                alt_match = re.search(r"Score[:\s]+(\d+\.?\d*)", output)
                if alt_match:
                    result.new_score = float(alt_match.group(1))

        result.details["stdout"] = proc.stdout[:1000] if proc.stdout else ""
        result.details["stderr"] = proc.stderr[:500] if proc.stderr else ""
        result.details["return_code"] = proc.returncode

    except subprocess.TimeoutExpired:
        result.error = "Evaluation timed out (300s)"
    except Exception as e:
        result.error = str(e)

    return result


def run_simple_evaluation(filepath: Path) -> EvaluationResult:
    """Run a simplified evaluation using prompt_analyzer.py as fallback.

    This is used when dual_eval is not available or fails.
    """
    result = EvaluationResult(prompt=PromptInfo(file_path=filepath))

    try:
        # Try to use the prompt analyzer
        script_dir = Path(__file__).parent
        analyzer_path = script_dir / "analyzers" / "prompt_analyzer.py"

        if analyzer_path.exists():
            cmd = [sys.executable, str(analyzer_path), str(filepath), "--json"]
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(Path(__file__).parent.parent),
            )

            if proc.returncode == 0 and proc.stdout:
                try:
                    data = json.loads(proc.stdout)
                    # Convert 1-5 scale to 1-10 scale
                    if "total_score" in data:
                        result.new_score = data["total_score"] * 2
                    result.grade = data.get("rating_label", "N/A")
                    result.passed = (
                        result.new_score >= PASS_THRESHOLD
                        if result.new_score
                        else False
                    )
                except json.JSONDecodeError:
                    pass

        # Fallback: basic structural analysis
        if result.new_score is None:
            content = filepath.read_text(encoding="utf-8")
            fm, _, body = parse_frontmatter(content)

            score = 5.0  # Base score

            # Check for key elements
            if fm:
                if fm.get("title"):
                    score += 0.5
                if fm.get("intro") or fm.get("description"):
                    score += 0.5
                if fm.get("type"):
                    score += 0.25
                if fm.get("audience"):
                    score += 0.25

            if "## Prompt" in body or "## prompt" in body:
                score += 1.0
            if "```" in body:
                score += 0.5
            if "example" in body.lower():
                score += 0.5
            if "## Usage" in body or "## Tips" in body:
                score += 0.5

            result.new_score = min(10.0, score)
            result.passed = result.new_score >= PASS_THRESHOLD
            result.details["method"] = "structural_analysis"

    except Exception as e:
        result.error = str(e)

    return result


# =============================================================================
# REPORT GENERATION
# =============================================================================


def generate_batch_report(
    report: BatchReport, output_path: Optional[Path] = None
) -> str:
    """Generate a markdown report from batch evaluation results."""

    lines = [
        "# 📊 Batch Evaluation Report",
        "",
        f"**Generated:** {report.timestamp}",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "|--------|-------|",
        f"| Total Prompts Scanned | {report.total_prompts} |",
        f"| Evaluated | {report.evaluated} |",
        f"| ✅ Passed | {report.passed} |",
        f"| ❌ Failed | {report.failed} |",
        f"| ⏭️ Skipped | {report.skipped} |",
        f"| ⚠️ Errors | {report.errors} |",
        f"| **Average Score** | **{report.average_score:.1f}/10** |",
        "",
        "---",
        "",
    ]

    # Results table
    if report.results:
        lines.extend(
            [
                "## Evaluation Results",
                "",
                "| File | Score | Grade | Status |",
                "|------|-------|-------|--------|",
            ]
        )

        for result in sorted(
            report.results, key=lambda r: r.new_score or 0, reverse=True
        ):
            status = "✅" if result.passed else "❌"
            if result.error:
                status = "⚠️"

            score_str = (
                f"{result.new_score:.1f}" if result.new_score is not None else "N/A"
            )
            filename = result.prompt.file_path.name

            lines.append(f"| {filename} | {score_str} | {result.grade} | {status} |")

        lines.extend(["", "---", ""])

    # Error details
    errors = [r for r in report.results if r.error]
    if errors:
        lines.extend(
            [
                "## Errors",
                "",
            ]
        )
        for result in errors:
            lines.append(f"- **{result.prompt.file_path.name}**: {result.error}")
        lines.extend(["", "---", ""])

    # Prompts needing attention
    low_scores = [
        r
        for r in report.results
        if r.new_score is not None and r.new_score < PASS_THRESHOLD
    ]
    if low_scores:
        lines.extend(
            [
                "## Prompts Needing Attention",
                "",
                "These prompts scored below the passing threshold and may need improvement:",
                "",
            ]
        )
        for result in sorted(low_scores, key=lambda r: r.new_score or 0):
            lines.append(
                f"- **{result.prompt.file_path.name}**: {result.new_score:.1f}/10"
            )
        lines.extend([""])

    report_text = "\n".join(lines)

    # Write to file if path provided
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report_text, encoding="utf-8")
        print(f"\n📄 Report saved to: {output_path}")

    return report_text


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Batch evaluation of prompts with pending effectivenessScore"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be evaluated without making changes",
    )
    parser.add_argument(
        "--folder", type=str, help="Specific folder to evaluate (relative to repo root)"
    )
    parser.add_argument(
        "--limit", type=int, default=None, help="Maximum number of prompts to evaluate"
    )
    parser.add_argument(
        "--skip-scored",
        action="store_true",
        help="Skip prompts that already have a score (only evaluate missing/pending)",
    )
    parser.add_argument(
        "--include-all",
        action="store_true",
        help="Include all prompts, not just those with pending scores",
    )
    parser.add_argument(
        "--output", type=str, default=None, help="Output path for the evaluation report"
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=2,
        help="Number of evaluation runs per model (default: 2)",
    )
    parser.add_argument(
        "--update-scores",
        action="store_true",
        help="Update frontmatter with calculated scores (not in dry-run mode)",
    )
    parser.add_argument(
        "--simple",
        action="store_true",
        help="Use simple structural evaluation instead of dual_eval",
    )

    args = parser.parse_args()

    # Determine base directory
    base_dir = Path(__file__).parent.parent
    if not (base_dir / "prompts").exists():
        base_dir = Path.cwd()

    print("=" * 70)
    print("📋 Batch Prompt Evaluation")
    print("=" * 70)

    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made\n")

    # Discover prompts
    print(
        f"🔍 Scanning for prompts in: {base_dir / (args.folder or DEFAULT_PROMPTS_DIR)}"
    )
    all_prompts = discover_prompts(base_dir, args.folder)
    print(f"   Found {len(all_prompts)} prompt files\n")

    # Filter to pending prompts
    if args.include_all:
        prompts_to_evaluate = all_prompts
    else:
        prompts_to_evaluate = filter_pending_prompts(all_prompts, args.skip_scored)

    print(f"📝 Prompts to evaluate: {len(prompts_to_evaluate)}")

    # Show score status breakdown
    pending = sum(1 for p in all_prompts if p.score_status == "pending")
    missing = sum(1 for p in all_prompts if p.score_status == "missing")
    scored = sum(1 for p in all_prompts if p.score_status == "scored")
    print(f"   - Pending: {pending}")
    print(f"   - Missing: {missing}")
    print(f"   - Already scored: {scored}\n")

    # Apply limit
    if args.limit and len(prompts_to_evaluate) > args.limit:
        prompts_to_evaluate = prompts_to_evaluate[: args.limit]
        print(f"   (Limited to {args.limit} prompts)\n")

    if not prompts_to_evaluate:
        print("✅ No prompts need evaluation!")
        return 0

    # Initialize report
    report = BatchReport(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_prompts=len(all_prompts),
        skipped=len(all_prompts) - len(prompts_to_evaluate),
    )

    # Evaluate each prompt
    print("-" * 70)
    scores = []

    for i, prompt in enumerate(prompts_to_evaluate, 1):
        print(f"\n[{i}/{len(prompts_to_evaluate)}] Evaluating: {prompt.title}")
        print(f"    File: {prompt.file_path.name}")

        if args.dry_run:
            print("    [DRY RUN] Would evaluate this prompt")
            report.skipped += 1
            continue

        # Run evaluation
        if args.simple:
            result = run_simple_evaluation(prompt.file_path)
        else:
            result = run_dual_eval(prompt.file_path, args.runs)
            # Fallback to simple if dual_eval fails
            if result.error and "not found" not in result.error.lower():
                print("    ⚠️  Dual eval failed, trying simple evaluation...")
                result = run_simple_evaluation(prompt.file_path)

        result.prompt = prompt
        report.results.append(result)

        if result.error:
            print(f"    ❌ Error: {result.error}")
            report.errors += 1
        elif result.new_score is not None:
            print(f"    📊 Score: {result.new_score:.1f}/10 ({result.grade})")
            scores.append(result.new_score)
            report.evaluated += 1

            if result.passed:
                report.passed += 1
            else:
                report.failed += 1

            # Update frontmatter if requested
            if args.update_scores and not args.dry_run:
                update_frontmatter_score(prompt.file_path, result.new_score)
        else:
            print("    ⚠️  Could not determine score")
            report.errors += 1

    # Calculate average score
    if scores:
        report.average_score = sum(scores) / len(scores)

    # Generate report
    print("\n" + "=" * 70)
    print("📊 EVALUATION COMPLETE")
    print("=" * 70)

    output_path = Path(args.output) if args.output else None
    if output_path is None and not args.dry_run:
        output_path = (
            base_dir
            / DEFAULT_OUTPUT_DIR
            / f"batch_eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )

    report_text = generate_batch_report(report, output_path)

    # Print summary
    print("\n📈 Summary:")
    print(f"   Total evaluated: {report.evaluated}")
    print(f"   Passed: {report.passed}")
    print(f"   Failed: {report.failed}")
    print(f"   Errors: {report.errors}")
    if scores:
        print(f"   Average score: {report.average_score:.1f}/10")

    return 0 if report.errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
