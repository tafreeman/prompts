#!/usr/bin/env python3
"""
Dual/Multi-Model Evaluation Script
===================================

Runs evaluations across multiple GitHub-hosted models (sequential by default) and cross-validates results.

Usage:
    # Evaluate a prompt file with default models (4 runs each)
    python testing/evals/dual_eval.py prompts/advanced/react-tool-augmented.md

    # Specify models and runs
    python testing/evals/dual_eval.py prompts/advanced/react-tool-augmented.md --runs 3

    # Output to specific file
    python testing/evals/dual_eval.py prompts/advanced/react-tool-augmented.md --output report.md

Author: Prompts Library Team
Version: 1.0.1 - GitHub Models only
"""

import argparse
import subprocess
import json
import sys
import re
import os
import tempfile
import statistics
import threading
import glob as glob_module
from itertools import count
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List, Optional, Tuple, Set, Callable
from dataclasses import dataclass, field


# =============================================================================
# CONFIGURATION
# =============================================================================

# Models to use for evaluation (validated via `gh models list` - Dec 2025)
# Note: Claude models NOT available in gh models - only in Copilot Chat
GH_MODELS = [
    "openai/gpt-4.1",               # GPT-4.1 (fast, reliable)
    "openai/gpt-4o",                # GPT-4o (fast, good quality)
    "openai/gpt-4o-mini",           # GPT-4o mini (fastest)
    "mistral-ai/mistral-small-2503", # Mistral Small (fast alternative)
    "meta/llama-3.3-70b-instruct",  # Llama 3.3 70B (open source)
]

# Combined default model list
EVAL_MODELS = GH_MODELS

# Fatal error detection patterns (lowercase match)
FATAL_ERROR_PATTERNS: List[Tuple[str, str]] = [
    ("model not found", "Model is not available in GitHub Models"),
    ("could not find model", "Model is not available in GitHub Models"),
    ("unknown model", "Model name is invalid"),
    ("you don't have access", "Model access denied"),
    ("not authorized", "GitHub authentication or access issue"),
    ("forbidden", "GitHub authentication or access issue"),
    ("invalid request: model", "Model not supported"),
]

# For Claude models, use Copilot Chat directly or a different evaluation method

# Thresholds
CROSS_VALIDATION_THRESHOLD = 1.5  # Max allowed score difference between models
PASS_THRESHOLD = 7.0
MIN_CRITERION_SCORE = 5.0

# Execution settings
DEFAULT_RUNS_PER_MODEL = 4
DEFAULT_MAX_WORKERS = 1  # Sequential by default to avoid gh CLI contention
EVAL_TIMEOUT_SECONDS = 120  # 2 minutes - fail fast
MAX_CONSECUTIVE_FAILURES = 2  # Stop model after this many consecutive failures

# Logging helpers
LOG_ENTRY_COUNTER = count(1)
LOG_LOCK = threading.Lock()


@dataclass
class EvalResult:
    """Result from a single evaluation run."""
    model: str
    run_number: int
    scores: Dict[str, float] = field(default_factory=dict)
    overall_score: float = 0.0
    grade: str = "N/A"
    passed: bool = False
    pass_reason: str = ""
    reasoning: str = ""
    strengths: List[str] = field(default_factory=list)
    improvements: List[str] = field(default_factory=list)
    summary: str = ""
    raw_response: str = ""
    error: Optional[str] = None


@dataclass
class ModelSummary:
    """Aggregated results for a single model."""
    model: str
    runs_completed: int = 0
    runs_failed: int = 0
    avg_score: float = 0.0
    min_score: float = 0.0
    max_score: float = 0.0
    std_dev: float = 0.0
    pass_rate: float = 0.0
    criterion_averages: Dict[str, float] = field(default_factory=dict)
    all_results: List[EvalResult] = field(default_factory=list)
    fatal_error: Optional[str] = None


@dataclass
class CrossValidationReport:
    """Cross-validation analysis across models."""
    prompt_title: str
    prompt_file: str
    total_runs: int = 0
    models_used: List[str] = field(default_factory=list)
    model_summaries: Dict[str, ModelSummary] = field(default_factory=dict)
    consensus_score: float = 0.0
    score_variance: float = 0.0
    cross_validation_passed: bool = False
    discrepancies: List[str] = field(default_factory=list)
    final_grade: str = "N/A"
    final_pass: bool = False
    combined_strengths: List[str] = field(default_factory=list)
    combined_improvements: List[str] = field(default_factory=list)


@dataclass
class BatchReport:
    """Aggregated results for batch evaluation of multiple prompts."""
    generated_at: str
    total_files: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    average_score: float = 0.0
    results: List[CrossValidationReport] = field(default_factory=list)
    errors: List[Dict[str, str]] = field(default_factory=list)


# =============================================================================
# FILE DISCOVERY & GIT INTEGRATION
# =============================================================================

# Files to exclude from prompt evaluation (not actual prompts)
EXCLUDED_FILENAMES = {
    'README.md',
    'index.md',
    'CHANGELOG.md',
    'CONTRIBUTING.md',
    'LICENSE.md',
}

# File suffixes that indicate non-prompt markdown files
EXCLUDED_SUFFIXES = (
    '.agent.md',
    '.instructions.md',
)

# Directories to exclude from prompt discovery
EXCLUDED_DIRS = {
    'archive',
    'node_modules',
    '.git',
    '__pycache__',
    '.pytest_cache',
}


def is_prompt_file(path: Path) -> bool:
    """
    Check if a markdown file is an actual prompt file (not agent, instruction, etc.).
    
    Args:
        path: Path to check
    
    Returns:
        True if this is a prompt file that should be evaluated
    """
    name = path.name
    
    # Exclude specific filenames
    if name in EXCLUDED_FILENAMES:
        return False
    
    # Exclude files with special suffixes
    for suffix in EXCLUDED_SUFFIXES:
        if name.endswith(suffix):
            return False
    
    # Exclude files in excluded directories
    for part in path.parts:
        if part in EXCLUDED_DIRS:
            return False
    
    return True


def discover_prompt_files(
    paths: List[str],
    *,
    recursive: bool = True,
    pattern: str = "*.md",
    include_all: bool = False
) -> List[Path]:
    """
    Discover prompt files from paths (files or directories).
    
    Automatically excludes non-prompt files:
    - README.md, index.md, CHANGELOG.md, etc.
    - Agent files (*.agent.md)
    - Instruction files (*.instructions.md)
    - Files in archive, node_modules, .git directories
    
    Args:
        paths: List of file paths, directory paths, or glob patterns
        recursive: Whether to search directories recursively
        pattern: Glob pattern for matching files (default: *.md)
        include_all: If True, include all .md files without filtering
    
    Returns:
        List of resolved Path objects to prompt files
    """
    discovered: Set[Path] = set()
    
    for path_str in paths:
        path = Path(path_str)
        
        # Handle glob patterns in the path string itself
        if '*' in path_str or '?' in path_str:
            for match in glob_module.glob(path_str, recursive=True):
                match_path = Path(match)
                if match_path.is_file() and match_path.suffix == '.md':
                    if include_all or is_prompt_file(match_path):
                        discovered.add(match_path.resolve())
            continue
        
        if path.is_file():
            # Single file - add directly if it's a markdown file
            if path.suffix == '.md':
                if include_all or is_prompt_file(path):
                    discovered.add(path.resolve())
                else:
                    print(f"⚠️  Skipping non-prompt file: {path.name}")
            else:
                print(f"⚠️  Skipping non-markdown file: {path}")
        elif path.is_dir():
            # Directory - find all matching files
            if recursive:
                for md_file in path.rglob(pattern):
                    if md_file.is_file():
                        if include_all or is_prompt_file(md_file):
                            discovered.add(md_file.resolve())
            else:
                for md_file in path.glob(pattern):
                    if md_file.is_file():
                        if include_all or is_prompt_file(md_file):
                            discovered.add(md_file.resolve())
        else:
            print(f"⚠️  Path not found: {path}")
    
    # Sort for consistent ordering
    return sorted(discovered)


def get_changed_files(
    base_ref: str = "origin/main",
    paths: Optional[List[str]] = None,
    include_staged: bool = True,
    include_unstaged: bool = True,
    include_all: bool = False
) -> List[Path]:
    """
    Get prompt files changed since base_ref using git.
    
    Automatically excludes non-prompt files (agents, instructions, README, etc.)
    unless include_all is True.
    
    Args:
        base_ref: Git reference to compare against (default: origin/main)
        paths: Optional list of paths to filter (e.g., ['prompts/'])
        include_staged: Include staged changes
        include_unstaged: Include unstaged changes
        include_all: If True, include all .md files without filtering
    
    Returns:
        List of Path objects for changed prompt files
    """
    changed: Set[Path] = set()
    path_filter = paths or ['.']
    
    def add_if_prompt(line: str) -> None:
        """Add file to changed set if it's a valid prompt file."""
        if line and line.endswith('.md'):
            file_path = Path(line)
            if file_path.exists():
                if include_all or is_prompt_file(file_path):
                    changed.add(file_path.resolve())
    
    try:
        # Get changes compared to base ref
        cmd = ['git', 'diff', '--name-only', f'{base_ref}...HEAD', '--'] + path_filter
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                add_if_prompt(line)
        
        # Include staged changes
        if include_staged:
            cmd = ['git', 'diff', '--cached', '--name-only', '--'] + path_filter
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    add_if_prompt(line)
        
        # Include unstaged changes
        if include_unstaged:
            cmd = ['git', 'diff', '--name-only', '--'] + path_filter
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    add_if_prompt(line)
    
    except subprocess.TimeoutExpired:
        print("⚠️  Git command timed out")
    except FileNotFoundError:
        print("⚠️  Git not found - cannot detect changed files")
    except Exception as e:
        print(f"⚠️  Error detecting changed files: {e}")
    
    return sorted(changed)


def create_log_writer(
    log_file: Optional[str],
    prompt_data: Dict[str, Any]
) -> Optional[Callable[[str, int, EvalResult], None]]:
    """Create a callback that appends markdown entries per run."""
    if not log_file:
        return None
    path = Path(log_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"\n## Prompt: {prompt_data['title']}\n"
        f"- File: `{prompt_data['file_path']}`\n"
        f"- Difficulty: {prompt_data['difficulty']}\n"
        f"- Logged: {datetime.now():%Y-%m-%d %H:%M:%S}\n\n"
    )
    with LOG_LOCK:
        if not path.exists():
            path.write_text("", encoding='utf-8')
        with path.open('a', encoding='utf-8') as f:
            f.write(header)
            f.flush()
            os.fsync(f.fileno())
    
    def writer(model: str, run_number: int, result: EvalResult) -> None:
        entry_id = next(LOG_ENTRY_COUNTER)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if result.error:
            status = "❌"
            details = f"Error: {result.error[:200]}"
        else:
            status = "✅" if result.passed else "⚠️"
            details = (
                f"Score {result.overall_score:.2f}/10 ({result.grade}), "
                f"Pass={'YES' if result.passed else 'NO'}"
            )
        line = (
            f"{entry_id}. [{timestamp}] **{model}** run {run_number}: "
            f"{status} {details}\n"
        )
        with LOG_LOCK:
            with path.open('a', encoding='utf-8') as f:
                f.write(line)
                f.flush()
                os.fsync(f.fileno())
    
    return writer


# =============================================================================
# PROMPT FILE PARSING
# =============================================================================

def parse_prompt_file(file_path: str) -> Dict[str, Any]:
    """Parse a markdown prompt file and extract metadata and content."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {file_path}")
    
    content = path.read_text(encoding='utf-8')
    
    # Extract YAML frontmatter
    frontmatter = {}
    body = content
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            import yaml
            try:
                frontmatter = yaml.safe_load(parts[1]) or {}
            except:
                pass
            body = parts[2].strip()
    
    return {
        "title": frontmatter.get("title", path.stem),
        "shortTitle": frontmatter.get("shortTitle", path.stem),
        "difficulty": frontmatter.get("difficulty", "intermediate"),
        "type": frontmatter.get("type", "how_to"),
        "audience": frontmatter.get("audience", []),
        "platforms": frontmatter.get("platforms", []),
        "topics": frontmatter.get("topics", []),
        "content": body,
        "file_path": str(path),
        "word_count": len(body.split()),
    }


def create_temp_eval_file(prompt_data: Dict[str, Any], model: str) -> str:
    """Create a temporary .prompt.yml eval file for a specific prompt."""
    
    # Escape the content for YAML
    content_escaped = prompt_data["content"].replace("\\", "\\\\").replace('"', '\\"')
    
    eval_content = f'''# Auto-generated eval file for dual-model evaluation
name: "{prompt_data['title']} Evaluation"
description: "Dual-model cross-validation evaluation"
model: {model}
modelParameters:
  temperature: 0.3
  max_tokens: 3000

testData:
  - promptTitle: "{prompt_data['title']}"
    promptContent: |
{chr(10).join('      ' + line for line in prompt_data['content'].split(chr(10))[:100])}
    difficulty: "{prompt_data['difficulty']}"
    type: "{prompt_data['type']}"
    wordCount: {prompt_data['word_count']}

messages:
  - role: system
    content: |
      You are an expert prompt engineer performing a rigorous evaluation using the Dual-Rubric System.
      
      ## Evaluation Framework
      
      ### Quality Standards (Core Criteria) - Score 1-10 each:
      1. **Clarity** (25%): Are instructions clear and unambiguous? Can be understood in <30 seconds?
      2. **Specificity** (20%): Enough detail for consistent, reproducible results?
      3. **Actionability** (25%): Can the AI clearly determine what actions to take?
      4. **Structure** (15%): Well-organized with clear sections and formatting?
      5. **Completeness** (15%): Covers all necessary aspects for the use case?
      
      ### Advanced Criteria - Score 1-10 each:
      6. **Factuality**: Are any claims or examples accurate?
      7. **Consistency**: Will it produce reproducible outputs?
      8. **Safety**: Does it avoid harmful patterns or prompt injection vulnerabilities?
      
      ## Reasoning Process (Chain-of-Thought)
      Before scoring, analyze:
      1. What is the prompt trying to achieve?
      2. Who is the target audience?
      3. What could go wrong or be misinterpreted?
      4. How would different AI models interpret this?
      
      ## Pass/Fail Criteria
      - PASS: Overall score >= 7.0 AND no individual criterion < 5.0
      - FAIL: Overall score < 7.0 OR any criterion < 5.0
      
      ## Response Format (JSON only)
      ```json
      {{
        "reasoning": "Step-by-step analysis...",
        "scores": {{
          "clarity": N,
          "specificity": N, 
          "actionability": N,
          "structure": N,
          "completeness": N,
          "factuality": N,
          "consistency": N,
          "safety": N
        }},
        "overall_score": N.N,
        "grade": "A+/A/A-/B+/B/B-/C+/C/C-/D/F",
        "pass": true/false,
        "pass_reason": "Why it passed or failed",
        "strengths": ["strength1", "strength2"],
        "improvements": ["improvement1", "improvement2"],
        "summary": "One-sentence summary"
      }}
      ```

  - role: user
    content: |
      Evaluate this prompt using the dual-rubric system:
      
      **Title:** {{{{promptTitle}}}}
      **Difficulty:** {{{{difficulty}}}}
      **Type:** {{{{type}}}}
      **Word Count:** {{{{wordCount}}}}
      
      **Prompt Content:**
      ```
      {{{{promptContent}}}}
      ```
      
      Provide chain-of-thought reasoning, score each criterion, and determine pass/fail.
      Respond with JSON only.

evaluators:
  - name: has-scores
    string:
      contains: '"scores"'
  - name: has-pass
    string:
      contains: '"pass"'
'''
    
    # Write to temp file
    temp_file = tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.prompt.yml',
        delete=False,
        encoding='utf-8'
    )
    temp_file.write(eval_content)
    temp_file.close()
    
    return temp_file.name


# =============================================================================
# EVALUATION EXECUTION
# =============================================================================

def run_single_eval(
    eval_file: str,
    model: str,
    run_number: int
) -> EvalResult:
    """Run a single evaluation with gh models eval."""
    result = EvalResult(model=model, run_number=run_number)
    
    try:
        proc = subprocess.run(
            ['gh', 'models', 'eval', eval_file, '--json'],
            capture_output=True,
            timeout=EVAL_TIMEOUT_SECONDS,
            encoding='utf-8',
            errors='replace'
        )
        
        if proc.returncode != 0:
            result.error = f"gh models eval failed: {proc.stderr[:200]}"
            return result
        
        if not proc.stdout:
            result.error = "No output from gh models eval"
            return result
        
        # Parse JSON output
        data = json.loads(proc.stdout)
        
        # Extract model response
        for test_result in data.get('testResults', []):
            response = test_result.get('modelResponse', '')
            result.raw_response = response
            
            # Parse JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
                
                result.scores = parsed.get('scores', {})
                result.overall_score = parsed.get('overall_score', 0)
                result.grade = parsed.get('grade', 'N/A')
                result.passed = parsed.get('pass', False)
                result.pass_reason = parsed.get('pass_reason', '')
                result.reasoning = parsed.get('reasoning', '')
                result.strengths = parsed.get('strengths', [])
                result.improvements = parsed.get('improvements', [])
                result.summary = parsed.get('summary', '')
                
    except subprocess.TimeoutExpired:
        result.error = f"Timeout after {EVAL_TIMEOUT_SECONDS}s"
    except json.JSONDecodeError as e:
        result.error = f"JSON parse error: {e}"
    except Exception as e:
        result.error = f"Error: {e}"
    
    return result


def detect_fatal_error_reason(error_message: Optional[str]) -> Optional[str]:
    """Return a human-readable fatal error reason if detected."""
    if not error_message:
        return None
    lower_msg = error_message.lower()
    for pattern, reason in FATAL_ERROR_PATTERNS:
        if pattern in lower_msg:
            return reason
    return None


def run_model_evaluations(
    prompt_data: Dict[str, Any],
    model: str,
    runs: int,
    log_writer: Optional[Callable[[str, int, EvalResult], None]] = None
) -> ModelSummary:
    """Run all evaluation runs for a single model. Fails fast after consecutive failures."""
    summary = ModelSummary(model=model)
    eval_file = create_temp_eval_file(prompt_data, model)
    consecutive_failures = 0
    
    try:
        for run_num in range(1, runs + 1):
            print(f"  Running {model} - Run {run_num}/{runs}...")
            
            result = run_single_eval(eval_file, model, run_num)
            summary.all_results.append(result)
            if log_writer:
                log_writer(model, run_num, result)
            
            if result.error:
                summary.runs_failed += 1
                consecutive_failures += 1
                print(f"    ❌ Error: {result.error[:50]}...")
                fatal_reason = detect_fatal_error_reason(result.error)
                if fatal_reason:
                    summary.fatal_error = result.error
                    print(f"    ⛔ Fatal error detected ({fatal_reason}). Skipping remaining runs for {model}.")
                    break
                
                # Fail fast: stop this model after MAX_CONSECUTIVE_FAILURES
                if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                    print(f"    ⚠️  Skipping remaining runs for {model} (too many failures)")
                    break
            else:
                summary.runs_completed += 1
                consecutive_failures = 0  # Reset on success
                print(f"    ✅ Score: {result.overall_score}/10 ({result.grade})")
    
    finally:
        Path(eval_file).unlink(missing_ok=True)
    
    # Calculate aggregates
    scores = [r.overall_score for r in summary.all_results if not r.error and r.overall_score > 0]
    
    if scores:
        summary.avg_score = statistics.mean(scores)
        summary.min_score = min(scores)
        summary.max_score = max(scores)
        summary.std_dev = statistics.stdev(scores) if len(scores) > 1 else 0
        summary.pass_rate = sum(1 for r in summary.all_results if r.passed) / len(summary.all_results)
        
        # Calculate criterion averages
        all_criteria = {}
        for r in summary.all_results:
            for crit, score in r.scores.items():
                if crit not in all_criteria:
                    all_criteria[crit] = []
                all_criteria[crit].append(score)
        
        for crit, vals in all_criteria.items():
            summary.criterion_averages[crit] = statistics.mean(vals)
    
    return summary


def validate_models(models: List[str]) -> Tuple[List[str], Dict[str, str]]:
    """Validate requested models before running evaluations."""
    valid_models: List[str] = []
    skipped: Dict[str, str] = {}
    seen: Set[str] = set()
    
    for model in models:
        if model in seen:
            continue
        seen.add(model)
        
        try:
            proc = subprocess.run(
                ['gh', 'models', 'view', model],
                capture_output=True,
                timeout=20,
                encoding='utf-8',
                errors='replace'
            )
        except FileNotFoundError as e:
            raise RuntimeError("GitHub CLI (gh) is not installed or not in PATH") from e
        except subprocess.TimeoutExpired:
            skipped[model] = "Timed out validating model with gh"
            continue
        
        if proc.returncode != 0:
            err_text = (proc.stderr or proc.stdout or "Unknown error").strip()
            skipped[model] = f"Model unavailable: {err_text[:180]}"
            continue
        
        valid_models.append(model)
    
    return valid_models, skipped


def run_parallel_evaluations(
    prompt_data: Dict[str, Any],
    models: List[str],
    runs_per_model: int,
    max_workers: int,
    log_writer: Optional[Callable[[str, int, EvalResult], None]] = None
) -> Dict[str, ModelSummary]:
    """Run evaluations for all models in parallel."""
    results = {}
    
    mode = "parallel" if max_workers > 1 else "sequential"
    print(f"\n🚀 Starting {mode} evaluation with {len(models)} models, {runs_per_model} runs each")
    print(f"   Total evaluations: {len(models) * runs_per_model}\n")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(run_model_evaluations, prompt_data, model, runs_per_model, log_writer): model
            for model in models
        }
        
        for future in as_completed(futures):
            model = futures[future]
            try:
                summary = future.result()
                results[model] = summary
                print(f"\n📊 {model}: Avg={summary.avg_score:.1f}, StdDev={summary.std_dev:.2f}, PassRate={summary.pass_rate:.0%}")
            except Exception as e:
                print(f"\n❌ {model}: Failed - {e}")
    
    return results


# =============================================================================
# CROSS-VALIDATION ANALYSIS
# =============================================================================

def cross_validate(
    prompt_data: Dict[str, Any],
    model_summaries: Dict[str, ModelSummary]
) -> CrossValidationReport:
    """Perform cross-validation analysis across all model results."""
    report = CrossValidationReport(
        prompt_title=prompt_data["title"],
        prompt_file=prompt_data["file_path"],
        models_used=list(model_summaries.keys()),
        model_summaries=model_summaries,
    )
    
    # Count total runs
    report.total_runs = sum(s.runs_completed + s.runs_failed for s in model_summaries.values())
    
    # Calculate consensus score (average of model averages)
    model_avgs = [s.avg_score for s in model_summaries.values() if s.avg_score > 0]
    if model_avgs:
        report.consensus_score = statistics.mean(model_avgs)
        report.score_variance = max(model_avgs) - min(model_avgs)
    
    # Check for cross-validation pass
    report.cross_validation_passed = report.score_variance <= CROSS_VALIDATION_THRESHOLD
    
    # Identify discrepancies
    for model, summary in model_summaries.items():
        if summary.avg_score > 0:
            diff = abs(summary.avg_score - report.consensus_score)
            if diff > CROSS_VALIDATION_THRESHOLD:
                report.discrepancies.append(
                    f"{model}: {summary.avg_score:.1f} (diff: {diff:.1f} from consensus)"
                )
    
    # Determine final grade
    if report.consensus_score >= 9.0:
        report.final_grade = "A+"
    elif report.consensus_score >= 8.5:
        report.final_grade = "A"
    elif report.consensus_score >= 8.0:
        report.final_grade = "A-"
    elif report.consensus_score >= 7.5:
        report.final_grade = "B+"
    elif report.consensus_score >= 7.0:
        report.final_grade = "B"
    elif report.consensus_score >= 6.5:
        report.final_grade = "B-"
    elif report.consensus_score >= 6.0:
        report.final_grade = "C+"
    elif report.consensus_score >= 5.5:
        report.final_grade = "C"
    elif report.consensus_score >= 5.0:
        report.final_grade = "C-"
    else:
        report.final_grade = "F"
    
    # Final pass/fail
    report.final_pass = report.consensus_score >= PASS_THRESHOLD
    
    # Combine strengths and improvements from all models
    seen_strengths = set()
    seen_improvements = set()
    
    for summary in model_summaries.values():
        for result in summary.all_results:
            for s in result.strengths:
                if s and s not in seen_strengths:
                    report.combined_strengths.append(s)
                    seen_strengths.add(s)
            for i in result.improvements:
                if i and i not in seen_improvements:
                    report.combined_improvements.append(i)
                    seen_improvements.add(i)
    
    return report


# =============================================================================
# REPORT GENERATION
# =============================================================================

def generate_report(report: CrossValidationReport) -> str:
    """Generate a markdown report from cross-validation results."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    lines = [
        "# 🔬 Dual-Model Cross-Validation Report",
        "",
        f"**Prompt:** {report.prompt_title}",
        f"**File:** `{report.prompt_file}`",
        f"**Generated:** {now}",
        "",
        "---",
        "",
        "## 📊 Executive Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| **Consensus Score** | **{report.consensus_score:.1f}/10** |",
        f"| **Final Grade** | **{report.final_grade}** |",
        f"| **Pass/Fail** | {'✅ PASS' if report.final_pass else '❌ FAIL'} |",
        f"| **Cross-Validation** | {'✅ Passed' if report.cross_validation_passed else '⚠️ Variance > 1.5'} |",
        f"| **Score Variance** | {report.score_variance:.2f} |",
        f"| **Total Runs** | {report.total_runs} |",
        f"| **Models Used** | {len(report.models_used)} |",
        "",
        "---",
        "",
        "## 🤖 Model-by-Model Results",
        "",
        "| Model | Avg Score | Min | Max | StdDev | Pass Rate | Runs |",
        "|-------|-----------|-----|-----|--------|-----------|------|",
    ]
    
    for model, summary in report.model_summaries.items():
        status = "✅" if summary.avg_score >= PASS_THRESHOLD else "❌"
        if summary.fatal_error:
            status = "⛔"
            lines.append(
                f"| {status} {model} | - | - | - | - | 0% | "
                f"{summary.runs_completed}/{summary.runs_completed + summary.runs_failed} |"
            )
        else:
            lines.append(
                f"| {status} {model} | {summary.avg_score:.1f} | {summary.min_score:.1f} | "
                f"{summary.max_score:.1f} | {summary.std_dev:.2f} | {summary.pass_rate:.0%} | "
                f"{summary.runs_completed}/{summary.runs_completed + summary.runs_failed} |"
            )
    
    fatal_notes = [
        (model, summary.fatal_error)
        for model, summary in report.model_summaries.items()
        if summary.fatal_error
    ]
    if fatal_notes:
        lines.extend([
            "",
            "> ⛔ Fatal errors detected:",
            "",
        ])
        for model, error in fatal_notes:
            lines.append(f"- {model}: {error[:200]}")
    
    # Criterion comparison
    lines.extend([
        "",
        "---",
        "",
        "## 📈 Criterion Scores by Model",
        "",
    ])
    
    # Get all criteria
    all_criteria = set()
    for summary in report.model_summaries.values():
        all_criteria.update(summary.criterion_averages.keys())
    
    if all_criteria:
        header = "| Criterion | " + " | ".join(m.split("/")[-1][:12] for m in report.models_used) + " | Avg |"
        separator = "|" + "---|" * (len(report.models_used) + 2)
        lines.append(header)
        lines.append(separator)
        
        for crit in sorted(all_criteria):
            scores = []
            row = f"| {crit.title()} |"
            for model in report.models_used:
                summary = report.model_summaries.get(model)
                if summary and crit in summary.criterion_averages:
                    score = summary.criterion_averages[crit]
                    scores.append(score)
                    status = "✅" if score >= MIN_CRITERION_SCORE else "⚠️"
                    row += f" {status} {score:.1f} |"
                else:
                    row += " - |"
            
            avg = statistics.mean(scores) if scores else 0
            row += f" **{avg:.1f}** |"
            lines.append(row)
    
    # Discrepancies
    if report.discrepancies:
        lines.extend([
            "",
            "---",
            "",
            "## ⚠️ Cross-Validation Discrepancies",
            "",
            "> These models scored significantly different from consensus:",
            "",
        ])
        for disc in report.discrepancies:
            lines.append(f"- {disc}")
    
    # Strengths
    if report.combined_strengths:
        lines.extend([
            "",
            "---",
            "",
            "## 💪 Identified Strengths",
            "",
        ])
        for s in report.combined_strengths[:10]:
            lines.append(f"- {s}")
    
    # Improvements
    if report.combined_improvements:
        lines.extend([
            "",
            "---",
            "",
            "## 🔧 Suggested Improvements",
            "",
        ])
        for i in report.combined_improvements[:10]:
            lines.append(f"- {i}")
    
    # Individual run details
    lines.extend([
        "",
        "---",
        "",
        "## 📋 Individual Run Details",
        "",
    ])
    
    for model, summary in report.model_summaries.items():
        lines.append(f"### {model}")
        lines.append("")
        
        for result in summary.all_results:
            if result.error:
                lines.append(f"- **Run {result.run_number}**: ❌ Error - {result.error[:50]}")
            else:
                passed = "✅" if result.passed else "❌"
                lines.append(
                    f"- **Run {result.run_number}**: {result.overall_score}/10 ({result.grade}) {passed}"
                )
                if result.summary:
                    lines.append(f"  - Summary: {result.summary[:100]}")
        
        lines.append("")
    
    # Methodology
    lines.extend([
        "---",
        "",
        "## 📖 Methodology",
        "",
        "This evaluation uses **Dual-Model Cross-Validation**:",
        "",
        "1. **Multiple Models**: Each prompt evaluated by 5 different LLMs",
        "2. **Multiple Runs**: 4 runs per model for statistical reliability",
        "3. **Dual-Rubric System**: 8 criteria across Quality + Advanced dimensions",
        "4. **Cross-Validation**: Score variance must be ≤ 1.5 between models",
        "5. **Pass Threshold**: Overall ≥ 7.0/10 AND no criterion < 5.0",
        "",
        "### Models Used",
        "",
    ])
    
    for model in report.models_used:
        lines.append(f"- `{model}`")
    
    lines.extend([
        "",
        "### Evaluation Criteria",
        "",
        "| Category | Criterion | Weight |",
        "|----------|-----------|--------|",
        "| Core | Clarity | 25% |",
        "| Core | Specificity | 20% |",
        "| Core | Actionability | 25% |",
        "| Core | Structure | 15% |",
        "| Core | Completeness | 15% |",
        "| Advanced | Factuality | N/A |",
        "| Advanced | Consistency | N/A |",
        "| Advanced | Safety | N/A |",
        "",
        "---",
        "",
        f"*Report generated by dual_eval.py at {now}*",
    ])
    
    return "\n".join(lines)


def print_summary(report: CrossValidationReport):
    """Print a summary to console."""
    print("\n" + "=" * 70)
    print("🔬 CROSS-VALIDATION COMPLETE")
    print("=" * 70)
    print(f"\n📄 Prompt: {report.prompt_title}")
    print(f"📁 File: {report.prompt_file}")
    print(f"\n{'─' * 70}")
    print(f"   Consensus Score: {report.consensus_score:.1f}/10")
    print(f"   Final Grade: {report.final_grade}")
    print(f"   Pass/Fail: {'✅ PASS' if report.final_pass else '❌ FAIL'}")
    print(f"   Cross-Validation: {'✅ Passed' if report.cross_validation_passed else '⚠️ High Variance'}")
    print(f"   Score Variance: {report.score_variance:.2f}")
    print(f"   Total Runs: {report.total_runs}")
    print(f"{'─' * 70}")
    
    print("\n📊 Model Scores:")
    for model, summary in report.model_summaries.items():
        if summary.fatal_error:
            print(f"   ⛔ {model}: Aborted - {summary.fatal_error[:80]}...")
            continue
        status = "✅" if summary.avg_score >= PASS_THRESHOLD else "❌"
        print(f"   {status} {model}: {summary.avg_score:.1f}/10 (±{summary.std_dev:.2f})")
    
    if report.discrepancies:
        print(f"\n⚠️  Discrepancies:")
        for d in report.discrepancies:
            print(f"   - {d}")
    
    print("\n" + "=" * 70 + "\n")


def report_to_dict(report: CrossValidationReport) -> Dict[str, Any]:
    """Convert a CrossValidationReport to a JSON-serializable dictionary."""
    model_summaries_dict = {}
    for model, summary in report.model_summaries.items():
        results_list = []
        for r in summary.all_results:
            results_list.append({
                "run_number": r.run_number,
                "overall_score": r.overall_score,
                "grade": r.grade,
                "passed": r.passed,
                "pass_reason": r.pass_reason,
                "scores": r.scores,
                "strengths": r.strengths,
                "improvements": r.improvements,
                "summary": r.summary,
                "error": r.error,
            })
        model_summaries_dict[model] = {
            "runs_completed": summary.runs_completed,
            "runs_failed": summary.runs_failed,
            "avg_score": round(summary.avg_score, 2),
            "min_score": round(summary.min_score, 2),
            "max_score": round(summary.max_score, 2),
            "std_dev": round(summary.std_dev, 3),
            "pass_rate": round(summary.pass_rate, 3),
            "criterion_averages": {k: round(v, 2) for k, v in summary.criterion_averages.items()},
            "fatal_error": summary.fatal_error,
            "results": results_list,
        }
    
    return {
        "prompt_title": report.prompt_title,
        "prompt_file": report.prompt_file,
        "total_runs": report.total_runs,
        "models_used": report.models_used,
        "consensus_score": round(report.consensus_score, 2),
        "score_variance": round(report.score_variance, 3),
        "cross_validation_passed": report.cross_validation_passed,
        "discrepancies": report.discrepancies,
        "final_grade": report.final_grade,
        "final_pass": report.final_pass,
        "combined_strengths": report.combined_strengths[:10],
        "combined_improvements": report.combined_improvements[:10],
        "model_summaries": model_summaries_dict,
    }


def generate_json_report(reports: List[CrossValidationReport]) -> str:
    """Generate a JSON report from one or more cross-validation results."""
    now = datetime.now().isoformat()
    
    # Calculate batch statistics
    passed = sum(1 for r in reports if r.final_pass)
    failed = len(reports) - passed
    scores = [r.consensus_score for r in reports if r.consensus_score > 0]
    avg_score = statistics.mean(scores) if scores else 0.0
    
    batch_report = {
        "generated_at": now,
        "version": "1.1.0",
        "total_files": len(reports),
        "passed": passed,
        "failed": failed,
        "average_score": round(avg_score, 2),
        "pass_rate": round(passed / len(reports), 3) if reports else 0,
        "results": [report_to_dict(r) for r in reports],
    }
    
    return json.dumps(batch_report, indent=2, ensure_ascii=False)


def generate_batch_markdown_report(reports: List[CrossValidationReport]) -> str:
    """Generate a combined markdown report for batch evaluation."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    passed = sum(1 for r in reports if r.final_pass)
    failed = len(reports) - passed
    scores = [r.consensus_score for r in reports if r.consensus_score > 0]
    avg_score = statistics.mean(scores) if scores else 0.0
    
    lines = [
        "# 📊 Batch Evaluation Report",
        "",
        f"**Generated:** {now}",
        f"**Total Files:** {len(reports)}",
        "",
        "---",
        "",
        "## Executive Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| **Files Evaluated** | {len(reports)} |",
        f"| **Passed** | {passed} ✅ |",
        f"| **Failed** | {failed} ❌ |",
        f"| **Pass Rate** | {passed/len(reports)*100:.1f}% |" if reports else "| **Pass Rate** | N/A |",
        f"| **Average Score** | {avg_score:.1f}/10 |",
        "",
        "---",
        "",
        "## Results by File",
        "",
        "| File | Score | Grade | Status |",
        "|------|-------|-------|--------|",
    ]
    
    for r in sorted(reports, key=lambda x: x.consensus_score, reverse=True):
        status = "✅ PASS" if r.final_pass else "❌ FAIL"
        file_name = Path(r.prompt_file).name
        lines.append(f"| `{file_name}` | {r.consensus_score:.1f} | {r.final_grade} | {status} |")
    
    # Add individual report details
    lines.extend([
        "",
        "---",
        "",
        "## Individual Reports",
        "",
    ])
    
    for r in reports:
        lines.extend([
            f"### {r.prompt_title}",
            "",
            f"**File:** `{r.prompt_file}`",
            f"**Score:** {r.consensus_score:.1f}/10 ({r.final_grade})",
            f"**Status:** {'✅ PASS' if r.final_pass else '❌ FAIL'}",
            "",
        ])
        
        if r.combined_improvements:
            lines.append("**Improvements:**")
            for imp in r.combined_improvements[:3]:
                lines.append(f"- {imp}")
            lines.append("")
    
    lines.extend([
        "---",
        "",
        f"*Report generated by dual_eval.py at {now}*",
    ])
    
    return "\n".join(lines)


def print_batch_summary(reports: List[CrossValidationReport]):
    """Print a summary for batch evaluation."""
    passed = sum(1 for r in reports if r.final_pass)
    failed = len(reports) - passed
    scores = [r.consensus_score for r in reports if r.consensus_score > 0]
    avg_score = statistics.mean(scores) if scores else 0.0
    
    print("\n" + "=" * 70)
    print("📊 BATCH EVALUATION COMPLETE")
    print("=" * 70)
    print(f"\n   Files Evaluated: {len(reports)}")
    print(f"   Passed: {passed} ✅")
    print(f"   Failed: {failed} ❌")
    print(f"   Pass Rate: {passed/len(reports)*100:.1f}%" if reports else "   Pass Rate: N/A")
    print(f"   Average Score: {avg_score:.1f}/10")
    print(f"\n{'─' * 70}")
    
    # Show failing files
    failing = [r for r in reports if not r.final_pass]
    if failing:
        print("\n❌ Failing Prompts:")
        for r in failing:
            print(f"   - {Path(r.prompt_file).name}: {r.consensus_score:.1f}/10 ({r.final_grade})")
    
    print("\n" + "=" * 70 + "\n")


# =============================================================================
# CLI
# =============================================================================

def evaluate_single_file(
    prompt_file: Path,
    models: List[str],
    runs: int,
    max_workers: int,
    log_file: Optional[str] = None,
    quiet: bool = False
) -> Optional[CrossValidationReport]:
    """
    Evaluate a single prompt file and return the report.
    
    Returns None if the file cannot be parsed.
    """
    try:
        prompt_data = parse_prompt_file(str(prompt_file))
        if not quiet:
            print(f"\n📄 Evaluating: {prompt_file.name}")
            print(f"   Title: {prompt_data['title']}")
    except (FileNotFoundError, Exception) as e:
        print(f"❌ Error parsing {prompt_file}: {e}")
        return None
    
    log_writer = create_log_writer(log_file, prompt_data) if log_file else None
    
    # Run evaluations
    model_summaries = run_parallel_evaluations(
        prompt_data,
        models,
        runs,
        max_workers,
        log_writer
    )
    
    # Cross-validate
    report = cross_validate(prompt_data, model_summaries)
    
    if not quiet:
        status = "✅ PASS" if report.final_pass else "❌ FAIL"
        print(f"   Result: {report.consensus_score:.1f}/10 ({report.final_grade}) {status}")
    
    return report


def main():
    parser = argparse.ArgumentParser(
        description="Dual-model cross-validation evaluation for prompts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Evaluate a single prompt file
  python testing/evals/dual_eval.py prompts/developers/code-review.md

  # Evaluate all prompts in a folder
  python testing/evals/dual_eval.py prompts/developers/

  # Evaluate with JSON output for CI/CD
  python testing/evals/dual_eval.py prompts/ --format json --output report.json

  # Evaluate only changed files (for PR validation)
  python testing/evals/dual_eval.py prompts/ --changed-only

  # Use specific models with fewer runs
  python testing/evals/dual_eval.py prompts/advanced/ --models openai/gpt-4o --runs 2

  # Glob pattern support
  python testing/evals/dual_eval.py "prompts/**/*.md" --format json
        """
    )
    
    parser.add_argument(
        "paths",
        nargs="+",
        help="Path(s) to prompt file(s), folder(s), or glob patterns to evaluate"
    )
    parser.add_argument(
        "--runs", "-r",
        type=int,
        default=DEFAULT_RUNS_PER_MODEL,
        help=f"Number of runs per model (default: {DEFAULT_RUNS_PER_MODEL})"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path (format determined by --format or extension)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format: markdown or json (default: markdown)"
    )
    parser.add_argument(
        "--models", "-m",
        nargs="+",
        default=EVAL_MODELS,
        help="Models to use for evaluation"
    )
    parser.add_argument(
        "--log-file",
        help="Append per-run results to this markdown file in real-time"
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=DEFAULT_MAX_WORKERS,
        help=f"Max concurrent model evaluations (default: {DEFAULT_MAX_WORKERS})"
    )
    parser.add_argument(
        "--changed-only",
        action="store_true",
        help="Only evaluate files changed since origin/main (for CI/CD)"
    )
    parser.add_argument(
        "--base-ref",
        default="origin/main",
        help="Git reference for --changed-only comparison (default: origin/main)"
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip model availability validation (faster, use with trusted models)"
    )
    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Don't recursively search directories for prompt files"
    )
    parser.add_argument(
        "--include-all",
        action="store_true",
        help="Include all .md files (agents, instructions, README, etc.)"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress per-file output, only show final summary"
    )
    
    args = parser.parse_args()
    
    # Discover files to evaluate
    if args.changed_only:
        print(f"\n🔍 Detecting changed files (base: {args.base_ref})...")
        prompt_files = get_changed_files(
            base_ref=args.base_ref,
            paths=args.paths,
            include_all=args.include_all
        )
        if not prompt_files:
            print("✅ No changed prompt files detected. Nothing to evaluate.")
            sys.exit(0)
        print(f"   Found {len(prompt_files)} changed file(s)")
    else:
        print(f"\n🔍 Discovering prompt files...")
        prompt_files = discover_prompt_files(
            args.paths,
            recursive=not args.no_recursive,
            include_all=args.include_all
        )
        if not prompt_files:
            print("❌ No prompt files found matching the specified paths.")
            sys.exit(2)
        print(f"   Found {len(prompt_files)} file(s)")
    
    # Validate models (unless skipped)
    if args.skip_validation:
        print("\n⚡ Skipping model validation (--skip-validation)")
        valid_models = args.models
        skipped_models = {}
    else:
        print("\n🔧 Validating models...")
        try:
            valid_models, skipped_models = validate_models(args.models)
        except RuntimeError as e:
            print(f"❌ {e}")
            sys.exit(1)
    
    if skipped_models:
        print("⚠️  Skipping unavailable models:")
        for model, reason in skipped_models.items():
            print(f"   - {model}: {reason}")
    
    if not valid_models:
        print("❌ No valid models available. Exiting.")
        sys.exit(1)
    
    print(f"   Using {len(valid_models)} model(s): {', '.join(m.split('/')[-1] for m in valid_models)}")
    
    if args.max_workers < 1:
        print("❌ --max-workers must be >= 1")
        sys.exit(2)
    
    # Evaluate all files
    reports: List[CrossValidationReport] = []
    errors: List[Dict[str, str]] = []
    
    for prompt_file in prompt_files:
        report = evaluate_single_file(
            prompt_file,
            valid_models,
            args.runs,
            args.max_workers,
            args.log_file,
            args.quiet
        )
        if report:
            reports.append(report)
        else:
            errors.append({"file": str(prompt_file), "error": "Failed to parse or evaluate"})
    
    if not reports:
        print("❌ No prompts were successfully evaluated.")
        sys.exit(1)
    
    # Print summary
    if len(reports) == 1:
        print_summary(reports[0])
    else:
        print_batch_summary(reports)
    
    # Determine output format
    output_format = args.format
    if args.output and args.output.endswith('.json'):
        output_format = "json"
    
    # Generate and save report
    if output_format == "json":
        report_content = generate_json_report(reports)
    else:
        if len(reports) == 1:
            report_content = generate_report(reports[0])
        else:
            report_content = generate_batch_markdown_report(reports)
    
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report_content, encoding='utf-8')
        print(f"📝 Report saved to: {output_path}")
    else:
        # Default output location
        ext = ".json" if output_format == "json" else ".md"
        if len(prompt_files) == 1:
            output_path = Path("testing/evals/results") / f"{prompt_files[0].stem}_dual_eval{ext}"
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = Path("testing/evals/results") / f"batch_eval_{timestamp}{ext}"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report_content, encoding='utf-8')
        print(f"📝 Report saved to: {output_path}")
    
    # Exit code: 0 if all passed, 1 if any failed
    all_passed = all(r.final_pass for r in reports)
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
