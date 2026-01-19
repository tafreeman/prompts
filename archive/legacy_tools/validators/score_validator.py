#!/usr/bin/env python3
"""
Score Validator for Prompt Library
Validates effectivenessScore field in prompt frontmatter.

Usage:
    python tools/validators/score_validator.py --all
    python tools/validators/score_validator.py path/to/file.md
    python tools/validators/score_validator.py --folder prompts/developers/
    python tools/validators/score_validator.py --summary
    python tools/validators/score_validator.py --unscored  # List files without scores
"""

import argparse
import sys
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


# =============================================================================
# CONSTANTS
# =============================================================================

MINIMUM_SCORE_NEW = 3.0
MINIMUM_SCORE_EXISTING = 2.5
SCORE_MIN = 1.0
SCORE_MAX = 5.0

RATING_LABELS = {
    (4.5, 5.0): ("⭐⭐⭐⭐⭐", "Excellent"),
    (4.0, 4.4): ("⭐⭐⭐⭐", "Good"),
    (3.0, 3.9): ("⭐⭐⭐", "Acceptable"),
    (2.0, 2.9): ("⭐⭐", "Below Average"),
    (1.0, 1.9): ("⭐", "Poor"),
}


# =============================================================================
# DATA CLASSES
# =============================================================================

class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class Issue:
    severity: Severity
    field: str
    message: str
    suggestion: Optional[str] = None


@dataclass
class ScoreResult:
    file_path: str
    has_score: bool
    score: Optional[float] = None
    rating_stars: Optional[str] = None
    rating_label: Optional[str] = None
    is_valid: bool = True
    issues: List[Issue] = field(default_factory=list)
    
    def add_error(self, field_name: str, message: str, suggestion: Optional[str] = None):
        self.issues.append(Issue(Severity.ERROR, field_name, message, suggestion))
        self.is_valid = False
    
    def add_warning(self, field_name: str, message: str, suggestion: Optional[str] = None):
        self.issues.append(Issue(Severity.WARNING, field_name, message, suggestion))
    
    def add_info(self, field_name: str, message: str, suggestion: Optional[str] = None):
        self.issues.append(Issue(Severity.INFO, field_name, message, suggestion))


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_rating(score: float) -> tuple:
    """Get star rating and label for a score."""
    for (min_score, max_score), (stars, label) in RATING_LABELS.items():
        if min_score <= score <= max_score:
            return stars, label
    return "?", "Unknown"


def extract_frontmatter(content: str) -> Optional[Dict[str, Any]]:
    """Extract YAML frontmatter from markdown content."""
    if not content.strip().startswith('---'):
        return None
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None
    
    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return None


# =============================================================================
# VALIDATOR CLASS
# =============================================================================

class ScoreValidator:
    
    def __init__(self, strict: bool = False):
        """
        Initialize validator.
        
        Args:
            strict: If True, missing scores are errors (not warnings)
        """
        self.strict = strict
    
    def validate_file(self, file_path: Path) -> ScoreResult:
        """Validate effectivenessScore in a single markdown file."""
        result = ScoreResult(file_path=str(file_path), has_score=False)
        
        # Skip non-prompt files
        if file_path.name in ["index.md", "README.md"]:
            result.add_info("skip", "Index/README files don't require scores")
            return result
        
        # Read file
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            result.add_error("file", f"Could not read file: {e}")
            return result
        
        # Extract frontmatter
        frontmatter = extract_frontmatter(content)
        if frontmatter is None:
            result.add_error("frontmatter", "No valid YAML frontmatter found")
            return result
        
        # Check for effectivenessScore
        score = frontmatter.get("effectivenessScore")
        
        if score is None:
            if self.strict:
                result.add_error(
                    "effectivenessScore", 
                    "Missing effectivenessScore field",
                    f"Add 'effectivenessScore: X.X' to frontmatter (minimum {MINIMUM_SCORE_NEW})"
                )
            else:
                result.add_warning(
                    "effectivenessScore",
                    "No effectivenessScore field - prompt has not been scored",
                    "Score this prompt using tools/rubrics/prompt-scoring.yaml"
                )
            return result
        
        result.has_score = True
        
        # Validate score type
        try:
            score = float(score)
        except (ValueError, TypeError):
            result.add_error(
                "effectivenessScore",
                f"Invalid score format: {score}",
                "Score must be a number between 1.0 and 5.0"
            )
            return result
        
        result.score = score
        
        # Validate score range
        if score < SCORE_MIN or score > SCORE_MAX:
            result.add_error(
                "effectivenessScore",
                f"Score {score} is out of range",
                f"Score must be between {SCORE_MIN} and {SCORE_MAX}"
            )
            return result
        
        # Check minimum threshold
        if score < MINIMUM_SCORE_NEW:
            result.add_warning(
                "effectivenessScore",
                f"Score {score} is below minimum threshold ({MINIMUM_SCORE_NEW})",
                "Consider improving this prompt or marking for review"
            )
        
        # Get rating
        stars, label = get_rating(score)
        result.rating_stars = stars
        result.rating_label = label
        
        result.add_info("score", f"Score: {score} {stars} ({label})")
        
        return result
    
    def validate_folder(self, folder_path: Path) -> List[ScoreResult]:
        """Validate all markdown files in a folder."""
        results = []
        for md_file in sorted(folder_path.rglob("*.md")):
            results.append(self.validate_file(md_file))
        return results


# =============================================================================
# OUTPUT FUNCTIONS
# =============================================================================

def print_result(result: ScoreResult, verbose: bool = False):
    """Print validation result for a single file."""
    if result.has_score and result.is_valid:
        status = "✓"
        color = "\033[92m"  # Green
    elif not result.has_score:
        status = "○"  # Empty circle for unscored
        color = "\033[93m"  # Yellow
    else:
        status = "✗"
        color = "\033[91m"  # Red
    
    reset = "\033[0m"
    
    # Get short path
    try:
        short_path = Path(result.file_path).relative_to(Path.cwd())
    except ValueError:
        short_path = result.file_path
    
    # Print main line
    score_str = f" ({result.score})" if result.score else ""
    print(f"{color}{status}{reset} {short_path}{score_str}")
    
    if verbose:
        for issue in result.issues:
            severity_color = {
                Severity.ERROR: "\033[91m",
                Severity.WARNING: "\033[93m",
                Severity.INFO: "\033[94m"
            }.get(issue.severity, "")
            
            severity_label = issue.severity.value.upper()
            print(f"  {severity_color}{severity_label}{reset} [{issue.field}]: {issue.message}")
            if issue.suggestion:
                print(f"    → {issue.suggestion}")


def print_summary(results: List[ScoreResult]):
    """Print summary statistics."""
    total = len(results)
    scored = sum(1 for r in results if r.has_score)
    valid = sum(1 for r in results if r.is_valid and r.has_score)
    unscored = sum(1 for r in results if not r.has_score and r.is_valid)
    errors = sum(1 for r in results if not r.is_valid)
    
    # Calculate average score
    scores = [r.score for r in results if r.score is not None]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    # Count by rating
    ratings = {}
    for r in results:
        if r.rating_label:
            ratings[r.rating_label] = ratings.get(r.rating_label, 0) + 1
    
    print("\n" + "=" * 60)
    print("SCORE SUMMARY")
    print("=" * 60)
    print(f"Total files:     {total}")
    print(f"Scored:          {scored}")
    print(f"Unscored:        {unscored}")
    print(f"Errors:          {errors}")
    print(f"Average score:   {avg_score:.2f}" if scores else "Average score:   N/A")
    
    if ratings:
        print("\nDistribution:")
        for label in ["Excellent", "Good", "Acceptable", "Below Average", "Poor"]:
            count = ratings.get(label, 0)
            if count > 0:
                pct = (count / scored) * 100 if scored else 0
                bar = "█" * int(pct / 5)
                print(f"  {label:<15} {count:>3} ({pct:>5.1f}%) {bar}")
    
    print("=" * 60)
    
    if unscored > 0:
        print(f"\n⚠️  {unscored} files need scoring. Run with --unscored to list them.")


def print_unscored(results: List[ScoreResult]):
    """Print list of files without scores."""
    unscored = [r for r in results if not r.has_score and r.is_valid]
    
    if not unscored:
        print("✅ All files have effectiveness scores!")
        return
    
    print(f"\n📋 Files without effectivenessScore ({len(unscored)} total):\n")
    
    # Group by folder
    by_folder = {}
    for r in unscored:
        folder = str(Path(r.file_path).parent)
        if folder not in by_folder:
            by_folder[folder] = []
        by_folder[folder].append(Path(r.file_path).name)
    
    for folder, files in sorted(by_folder.items()):
        print(f"\n{folder}/")
        for f in sorted(files):
            print(f"  - {f}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Validate effectivenessScore in prompt frontmatter"
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Path to a single markdown file to validate"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all prompts in the repository"
    )
    parser.add_argument(
        "--folder",
        type=str,
        help="Validate all files in a specific folder"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat missing scores as errors"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output for each file"
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show summary statistics"
    )
    parser.add_argument(
        "--unscored",
        action="store_true",
        help="List only files without scores"
    )
    
    args = parser.parse_args()
    
    validator = ScoreValidator(strict=args.strict)
    results = []
    
    if args.file:
        # Single file
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {args.file}")
            return 1
        results = [validator.validate_file(file_path)]
    
    elif args.folder:
        # Folder
        folder_path = Path(args.folder)
        if not folder_path.exists():
            print(f"Error: Folder not found: {args.folder}")
            return 1
        results = validator.validate_folder(folder_path)
    
    elif args.all:
        # All prompts
        prompts_path = Path(__file__).parent.parent.parent / "prompts"
        if prompts_path.exists():
            results = validator.validate_folder(prompts_path)
        else:
            print(f"Error: prompts folder not found at {prompts_path}")
            return 1
    
    else:
        parser.print_help()
        return 0
    
    # Output
    if args.unscored:
        print_unscored(results)
    else:
        for result in results:
            print_result(result, args.verbose)
    
    if args.summary or args.all:
        print_summary(results)
    
    # Exit code based on errors
    has_errors = any(not r.is_valid for r in results)
    return 1 if has_errors else 0


if __name__ == "__main__":
    sys.exit(main())
