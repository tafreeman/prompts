#!/usr/bin/env python3
"""
LATS Library Improvement Script
================================

Automates iterative prompt improvement using the LATS Self-Refine evaluator pattern.

This script:
1. Discovers all prompts in the library (excluding READMEs, indexes, archives)
2. For each prompt, runs the LATS Self-Refine evaluator iteratively
3. Tracks coverage to ensure all sections/folders are evaluated
4. Saves improvement suggestions and final scores
5. Generates a comprehensive improvement report

Usage:
    python run_lats_improvement.py                      # Evaluate all prompts (auto-select model)
    python run_lats_improvement.py --folder advanced    # Specific folder
    python run_lats_improvement.py --model ollama:phi4-reasoning  # Use specific model
    python run_lats_improvement.py --model ollama:deepseek-r1:14b # Use deepseek
    python run_lats_improvement.py --model gh:gpt-4.1   # Use GitHub Models
    python run_lats_improvement.py --max-iterations 5   # Control iteration limit
    python run_lats_improvement.py --threshold 85       # Quality threshold

Supported Models:
    Local (Ollama - FREE, FAST):
      - ollama:phi4-reasoning (default if available)
      - ollama:deepseek-r1:14b
      - ollama:qwen2.5-coder:14b
      - ollama:llama3.3
    
    Cloud (GitHub Models - requires token):
      - gh:gpt-4.1
      - gh:gpt-4o-mini
      - gh:deepseek/deepseek-r1
"""

import sys
import json
import argparse
import time
import urllib.request
import urllib.error
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

# Add tools directory to path
TOOLS_DIR = Path(__file__).parent
REPO_ROOT = TOOLS_DIR.parent
sys.path.insert(0, str(TOOLS_DIR))

from llm_client import LLMClient


# =============================================================================
# MODEL CONFIGURATION
# =============================================================================

# Preferred models in order of preference (local first for speed/cost)
PREFERRED_MODELS = [
    "ollama:phi4-reasoning",      # Best local reasoning model
    "ollama:deepseek-r1:14b",     # Strong reasoning model
    "ollama:qwen2.5-coder:14b",   # Good for code-related prompts
    "gh:gpt-4.1",                 # Cloud fallback (requires GITHUB_TOKEN)
    "gh:gpt-4o-mini",             # Cheaper cloud option
]


def get_available_ollama_models() -> List[str]:
    """Get list of locally available Ollama models."""
    try:
        ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        req = urllib.request.Request(
            f"{ollama_host}/api/tags",
            headers={"Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=2) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            models = []
            for m in data.get("models", []):
                name = m.get("name", "")
                if name:
                    models.append(f"ollama:{name}")
                    # Also add short name without tag
                    short = name.split(":")[0]
                    if short != name:
                        models.append(f"ollama:{short}")
            return models
    except:
        return []


def get_best_available_model(requested: Optional[str] = None) -> str:
    """
    Get the best available model, preferring local Ollama models.
    
    Args:
        requested: Optional specific model request
        
    Returns:
        Best available model string (e.g., "ollama:phi4-reasoning" or "gh:gpt-4.1")
    """
    # If user requested a specific model, validate and return it
    if requested:
        if requested.startswith("ollama:"):
            available = get_available_ollama_models()
            if requested in available or any(requested in m for m in available):
                return requested
            print(f"⚠️  Requested model {requested} not found in Ollama. Available: {available[:5]}")
        elif requested.startswith("gh:"):
            # Assume gh models are available if GITHUB_TOKEN exists
            if os.getenv("GITHUB_TOKEN"):
                return requested
            print(f"⚠️  GitHub token not found for {requested}")
        else:
            # Try as ollama model
            return f"ollama:{requested}"
    
    # Auto-select best available model
    available_ollama = get_available_ollama_models()
    print(f"🔍 Discovered Ollama models: {[m.replace('ollama:', '') for m in available_ollama[:5]]}")
    
    for model in PREFERRED_MODELS:
        if model.startswith("ollama:"):
            # Check if this model or a variant is available
            model_name = model.split(":", 1)[1]
            for avail in available_ollama:
                if model_name in avail:
                    print(f"✅ Selected model: {avail}")
                    return avail
        elif model.startswith("gh:"):
            if os.getenv("GITHUB_TOKEN"):
                print(f"✅ Selected model: {model} (cloud)")
                return model
    
    # Default fallback
    if available_ollama:
        print(f"✅ Selected model: {available_ollama[0]} (first available)")
        return available_ollama[0]
    
    print("⚠️  No local models found, falling back to gh:gpt-4o-mini")
    return "gh:gpt-4o-mini"


@dataclass
class LATS_Result:
    """Result from LATS Self-Refine evaluation."""
    prompt_file: str
    initial_score: float
    final_score: float
    iterations: int
    improvement: float
    threshold_met: bool
    key_changes: List[str]
    duration_seconds: float
    model: str
    timestamp: str


@dataclass
class CoverageReport:
    """Coverage tracking for library evaluation."""
    total_prompts: int
    evaluated: int
    passed: int
    failed: int
    skipped: int
    folders: Dict[str, Dict[str, int]]
    duration_seconds: float
    avg_improvement: float
    results: List[LATS_Result]


def load_lats_evaluator(use_lite: bool = False) -> str:
    """Load the LATS evaluator prompt template.
    
    Args:
        use_lite: If True, load the compact LATS-Lite version (~1.5KB) 
                  optimized for local models. Default False uses full 
                  version (~5.5KB) for cloud models.
    
    Returns:
        The prompt template string ready for variable substitution.
    """
    import json
    
    advanced_dir = REPO_ROOT / "prompts" / "advanced"
    
    if use_lite:
        prompt_file = advanced_dir / "lats-lite.prompt.txt"
        meta_file = advanced_dir / "lats-lite.meta.json"
    else:
        prompt_file = advanced_dir / "lats-full.prompt.txt"
        meta_file = advanced_dir / "lats-full.meta.json"
    
    # Try new separated format first
    if prompt_file.exists():
        with open(prompt_file, "r", encoding="utf-8") as f:
            template = f.read()
        
        # Load metadata for variable defaults if available
        if meta_file.exists():
            try:
                with open(meta_file, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                # Store metadata for later use (e.g., variable defaults)
                load_lats_evaluator._metadata = meta
            except (json.JSONDecodeError, IOError):
                load_lats_evaluator._metadata = {}
        
        return template
    
    # Fallback to legacy .md file format
    if use_lite:
        legacy_path = advanced_dir / "lats-lite-evaluator.md"
    else:
        legacy_path = advanced_dir / "lats-self-refine-evaluator.md"
    
    if not legacy_path.exists():
        raise FileNotFoundError(f"LATS evaluator not found: {prompt_file} or {legacy_path}")
    
    with open(legacy_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract just the prompt template from ```text blocks
    import re
    match = re.search(r'```text\n(.*?)\n```', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Fallback: Extract content after frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2].strip()
    
    return content


def get_lats_metadata(use_lite: bool = False) -> dict:
    """Get metadata for the LATS evaluator.
    
    Returns variable defaults, model compatibility, and other config.
    """
    import json
    
    advanced_dir = REPO_ROOT / "prompts" / "advanced"
    meta_file = advanced_dir / ("lats-lite.meta.json" if use_lite else "lats-full.meta.json")
    
    if meta_file.exists():
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    
    # Return defaults if no metadata file
    return {
        "variables": {
            "QUALITY_THRESHOLD": {"default": "80"},
            "MAX_ITERATIONS": {"default": "5"},
            "GRADING_CRITERIA": {"default": '{"clarity": 25, "effectiveness": 30, "specificity": 20, "completeness": 25}'}
        }
    }


def find_prompts(path: Path, exclude_patterns: List[str] = None) -> List[Path]:
    """Find all actual prompt files, excluding documentation and archives."""
    exclude_patterns = exclude_patterns or [
        "README.md",
        "index.md",
        "archive",
        "_archive",
        "GUIDE",
        "REFERENCE",
    ]
    
    prompts = []
    
    if path.is_file():
        if path.suffix == ".md" and not any(pat.lower() in path.name.lower() for pat in exclude_patterns):
            return [path]
        return []
    
    # Find markdown files
    for md_file in sorted(path.rglob("*.md")):
        # Skip if matches exclusion pattern
        if any(pat.lower() in str(md_file).lower() for pat in exclude_patterns):
            continue
        
        # Skip if in excluded directories
        if any(pat.lower() in str(md_file.parent).lower() for pat in exclude_patterns):
            continue
        
        prompts.append(md_file)
    
    return prompts


def run_lats_iteration(
    prompt_content: str,
    evaluator_template: str,
    model: str,
    iteration: int,
    previous_score: Optional[float] = None,
    previous_feedback: Optional[str] = None,
    threshold: float = 80.0,
    max_iterations: int = 5,
) -> Dict[str, Any]:
    """
    Run a single LATS iteration.
    
    Returns:
        {
            "score": float,
            "threshold_met": bool,
            "feedback": dict with branches A, B, C,
            "revised_prompt": str (if not final iteration)
        }
    """
    
    # Build iteration-specific prompt
    iteration_context = f"""
ITERATION {iteration}/{max_iterations}
{'='*60}

CURRENT THRESHOLD: {threshold}%
"""
    
    if previous_score:
        iteration_context += f"\nPREVIOUS SCORE: {previous_score}%"
    
    if previous_feedback:
        iteration_context += f"\nPREVIOUS FEEDBACK:\n{previous_feedback}\n"
    
    iteration_context += f"""
{'='*60}

PROMPT TO EVALUATE:
---
{prompt_content[:4000]}
---

Execute the LATS Self-Refine evaluation with ALL THREE BRANCHES:
"""
    
    # Insert context into evaluator template
    full_prompt = evaluator_template.replace("{{PROMPT_CONTENT}}", prompt_content[:4000])
    full_prompt = full_prompt.replace("{{QUALITY_THRESHOLD}}", str(threshold))
    full_prompt = full_prompt.replace("{{MAX_ITERATIONS}}", str(max_iterations))
    full_prompt = iteration_context + "\n\n" + full_prompt
    
    # Call model
    response = LLMClient.generate_text(model, full_prompt, max_tokens=4000)
    
    # Parse response
    result = parse_lats_response(response)
    
    return result


def parse_lats_response(response: str) -> Dict[str, Any]:
    """
    Parse LATS evaluator response.
    
    Expected structure:
    - Branch A: Criteria validation
    - Branch B: Scoring with evidence
    - Branch C: Improvement suggestions
    - Synthesis: Final score, threshold check
    """
    import re
    
    # Handle None or empty responses
    if not response:
        return {
            "score": 0.0,
            "threshold_met": False,
            "feedback": {},
            "key_changes": [],
            "raw_response": "ERROR: No response from model",
            "error": "Empty or None response received",
        }
    
    # Extract score (look for multiple patterns)
    # Patterns: "Score: 75.5", "Final Score: 82%", "Overall: 7.5/10", "weighted_score: 85"
    score = 0.0
    score_patterns = [
        r'(?:final\s+)?score[:\s]+(\d+(?:\.\d+)?)\s*%',  # "score: 75%"
        r'(?:final\s+)?score[:\s]+(\d+(?:\.\d+)?)',       # "score: 75"
        r'overall[:\s]+(\d+(?:\.\d+)?)\s*/\s*10',         # "overall: 7.5/10"
        r'weighted_score[:\s]+(\d+(?:\.\d+)?)',           # "weighted_score: 85"
        r'(\d+(?:\.\d+)?)\s*%\s*(?:overall|total|final)', # "75% overall"
        r'\*\*(\d+(?:\.\d+)?)\s*%?\*\*',                  # **75%** or **75**
    ]
    
    for pattern in score_patterns:
        score_match = re.search(pattern, response, re.IGNORECASE)
        if score_match:
            raw_score = float(score_match.group(1))
            # Normalize scores on 1-10 scale to percentage
            if raw_score <= 10:
                score = raw_score * 10  # 7.5 -> 75%
            else:
                score = raw_score  # Already percentage
            break
    
    # Extract threshold met
    threshold_match = re.search(r'threshold[_\s]met[:\s]+(true|false|yes|no)', response, re.IGNORECASE)
    threshold_met = threshold_match and threshold_match.group(1).lower() in ["true", "yes"] if threshold_match else False
    
    # Extract key changes/improvements
    changes = []
    changes_section = re.search(r'(?:key\s+changes|improvements)[:\s]+(.*?)(?=\n\n|\Z)', response, re.IGNORECASE | re.DOTALL)
    if changes_section:
        changes_text = changes_section.group(1)
        # Extract numbered or bulleted items
        changes = re.findall(r'(?:^|\n)\s*[\d\-\*]+\.?\s*(.+?)(?=\n|$)', changes_text, re.MULTILINE)
    
    # Extract branch results
    branches = {}
    for branch_name in ['A', 'B', 'C']:
        branch_pattern = rf'BRANCH\s+{branch_name}[:\s]+(.*?)(?=BRANCH\s+[ABC]|SYNTHESIS|$)'
        branch_match = re.search(branch_pattern, response, re.IGNORECASE | re.DOTALL)
        if branch_match:
            branches[f"branch_{branch_name}"] = branch_match.group(1).strip()[:500]
    
    return {
        "score": score,
        "threshold_met": threshold_met,
        "feedback": branches,
        "key_changes": changes[:5],  # Top 5 changes
        "raw_response": response[:2000],  # Keep larger sample for debugging
    }


def evaluate_prompt_with_lats(
    prompt_path: Path,
    evaluator_template: str,
    model: str = "gh:gpt-4.1",
    threshold: float = 80.0,
    max_iterations: int = 5,
    verbose: bool = True,
) -> LATS_Result:
    """Evaluate a single prompt using LATS Self-Refine pattern."""
    
    start_time = time.time()
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"📊 LATS Evaluation: {prompt_path.name}")
        print(f"{'='*60}")
    
    # Load prompt
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_content = f.read()
    
    iteration = 1
    current_score = 0.0
    initial_score = 0.0
    previous_feedback = None
    all_changes = []
    
    while iteration <= max_iterations:
        if verbose:
            print(f"\n🔄 Iteration {iteration}/{max_iterations}...")
        
        result = run_lats_iteration(
            prompt_content=prompt_content,
            evaluator_template=evaluator_template,
            model=model,
            iteration=iteration,
            previous_score=current_score if iteration > 1 else None,
            previous_feedback=previous_feedback,
            threshold=threshold,
            max_iterations=max_iterations,
        )
        
        current_score = result["score"]
        
        # Debug: show if we got an error or empty response
        if result.get("error"):
            if verbose:
                print(f"   ⚠️  Error: {result['error']}")
        elif verbose and current_score == 0.0:
            # Show part of response to debug score extraction
            raw = result.get("raw_response", "")[:800]
            print(f"   ⚠️  Score extraction failed. Response preview:\n{raw}\n...")
        
        if iteration == 1:
            initial_score = current_score
        
        if verbose:
            print(f"   Score: {current_score:.1f}% (threshold: {threshold}%)")
            if result["key_changes"]:
                print(f"   Changes: {len(result['key_changes'])} improvements identified")
        
        all_changes.extend(result["key_changes"])
        
        # Check if threshold met
        if result["threshold_met"] or current_score >= threshold:
            if verbose:
                print(f"\n✅ Threshold met! Final score: {current_score:.1f}%")
            break
        
        # Prepare feedback for next iteration
        previous_feedback = json.dumps(result["feedback"], indent=2)
        iteration += 1
    
    duration = time.time() - start_time
    improvement = current_score - initial_score
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"📈 Results:")
        print(f"   Initial:     {initial_score:.1f}%")
        print(f"   Final:       {current_score:.1f}%")
        print(f"   Improvement: +{improvement:.1f}%")
        print(f"   Iterations:  {iteration}")
        print(f"   Duration:    {duration:.1f}s")
        print(f"{'='*60}")
    
    return LATS_Result(
        prompt_file=str(prompt_path),
        initial_score=initial_score,
        final_score=current_score,
        iterations=iteration,
        improvement=improvement,
        threshold_met=current_score >= threshold,
        key_changes=list(set(all_changes))[:10],  # Unique top 10
        duration_seconds=round(duration, 1),
        model=model,
        timestamp=datetime.now().isoformat(),
    )


def generate_coverage_report(results: List[LATS_Result], total_prompts: int, duration: float) -> CoverageReport:
    """Generate comprehensive coverage report."""
    
    # Calculate folder-level stats
    folders = {}
    for result in results:
        folder = Path(result.prompt_file).parent.name
        if folder not in folders:
            folders[folder] = {"total": 0, "passed": 0, "failed": 0}
        
        folders[folder]["total"] += 1
        if result.threshold_met:
            folders[folder]["passed"] += 1
        else:
            folders[folder]["failed"] += 1
    
    passed = sum(1 for r in results if r.threshold_met)
    failed = len(results) - passed
    avg_improvement = sum(r.improvement for r in results) / len(results) if results else 0.0
    
    return CoverageReport(
        total_prompts=total_prompts,
        evaluated=len(results),
        passed=passed,
        failed=failed,
        skipped=total_prompts - len(results),
        folders=folders,
        duration_seconds=round(duration, 1),
        avg_improvement=round(avg_improvement, 1),
        results=results,
    )


def save_results(coverage: CoverageReport, output_path: Path):
    """Save results to JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    data = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_prompts": coverage.total_prompts,
            "evaluated": coverage.evaluated,
            "passed": coverage.passed,
            "failed": coverage.failed,
            "skipped": coverage.skipped,
            "avg_improvement": coverage.avg_improvement,
            "duration_seconds": coverage.duration_seconds,
        },
        "folders": coverage.folders,
        "results": [asdict(r) for r in coverage.results],
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Results saved to: {output_path}")


def save_incremental_result(result: LATS_Result, output_path: Path, total_prompts: int):
    """Save individual result immediately after evaluation (incremental backup)."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing results if file exists
    existing_results = []
    if output_path.exists():
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                existing_results = data.get("results", [])
        except (json.JSONDecodeError, IOError):
            pass  # Start fresh if corrupted
    
    # Append new result
    existing_results.append(asdict(result))
    
    # Calculate summary stats
    passed = sum(1 for r in existing_results if r.get("threshold_met", False))
    failed = len(existing_results) - passed
    avg_improvement = sum(r.get("improvement", 0) for r in existing_results) / len(existing_results) if existing_results else 0.0
    
    # Update file with new result
    data = {
        "timestamp": datetime.now().isoformat(),
        "status": "in_progress",
        "summary": {
            "total_prompts": total_prompts,
            "evaluated": len(existing_results),
            "passed": passed,
            "failed": failed,
            "skipped": total_prompts - len(existing_results),
            "avg_improvement": round(avg_improvement, 1),
        },
        "results": existing_results,
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"   💾 Progress saved ({len(existing_results)}/{total_prompts})")


def main():
    parser = argparse.ArgumentParser(
        description="LATS Library Improvement - Systematic prompt evaluation and improvement",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "path",
        nargs="?",
        default="prompts",
        help="Path to prompts directory or specific prompt file (default: prompts)",
    )
    parser.add_argument(
        "--folder",
        help="Evaluate specific folder only (e.g., 'advanced', 'business')",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model to use (e.g., ollama:phi4-reasoning, gh:gpt-4.1). Auto-selects best available if not specified.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=80.0,
        help="Quality threshold percentage (default: 80)",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=5,
        help="Maximum LATS iterations per prompt (default: 5)",
    )
    parser.add_argument(
        "--output",
        default="results/lats-improvement.json",
        help="Output file for results (default: results/lats-improvement.json)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Delay between evaluations in seconds (default: 2.0)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output",
    )
    parser.add_argument(
        "--full-lats",
        action="store_true",
        help="Force full LATS evaluator even for local models (default: auto-selects lite for local)",
    )
    parser.add_argument(
        "--lite",
        action="store_true", 
        help="Force LATS-Lite evaluator even for cloud models",
    )
    
    args = parser.parse_args()
    
    # Set UTF-8 encoding for Windows console
    import sys
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    
    # Select best available model
    print("\n[Model Selection]")
    selected_model = get_best_available_model(args.model)
    
    # Determine if we should use LATS-Lite (for local models)
    is_local_model = selected_model.startswith(("ollama:", "local:", "windows-ai:"))
    
    # Flag logic: --lite forces lite, --full-lats forces full, otherwise auto-detect
    if args.lite:
        use_lite = True
    elif args.full_lats:
        use_lite = False
    else:
        use_lite = is_local_model  # Auto: lite for local, full for cloud
    
    # Load LATS evaluator
    evaluator_type = "LATS-Lite (1.5KB)" if use_lite else "LATS-Full (5.5KB)"
    print(f"\n📥 Loading {evaluator_type} evaluator...")
    try:
        evaluator_template = load_lats_evaluator(use_lite=use_lite)
        metadata = get_lats_metadata(use_lite=use_lite)
        template_size = len(evaluator_template)
        print(f"✅ Loaded from: lats-{'lite' if use_lite else 'full'}.prompt.txt ({template_size:,} chars)")
    except Exception as e:
        print(f"❌ Failed to load evaluator: {e}")
        return 1
    
    # Find prompts - handle both relative and absolute paths
    path = Path(args.path)
    if not path.is_absolute():
        # Make relative paths absolute from REPO_ROOT
        path = REPO_ROOT / path
    
    if args.folder:
        folder_path = Path(args.folder)
        if folder_path.is_absolute():
            path = folder_path
        else:
            path = path / args.folder
    
    if not path.exists():
        print(f"❌ Path not found: {path}")
        return 1
    
    print(f"\n🔍 Discovering prompts in: {path}")
    prompts = find_prompts(path)
    
    if not prompts:
        print("❌ No prompts found")
        return 1
    
    print(f"✅ Found {len(prompts)} prompts to evaluate")
    
    # Show folder breakdown
    folders = {}
    for p in prompts:
        folder = p.parent.name
        folders[folder] = folders.get(folder, 0) + 1
    
    print("\n📁 Coverage by folder:")
    for folder, count in sorted(folders.items()):
        print(f"   {folder}: {count} prompts")
    
    # Run evaluations
    print(f"\n🚀 Starting LATS evaluation (threshold: {args.threshold}%, max iterations: {args.max_iterations})")
    print(f"   Model: {selected_model}")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    results = []
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = REPO_ROOT / output_path
    
    for i, prompt_path in enumerate(prompts, 1):
        print(f"[{i}/{len(prompts)}] {prompt_path.name}")
        
        try:
            result = evaluate_prompt_with_lats(
                prompt_path=prompt_path,
                evaluator_template=evaluator_template,
                model=selected_model,
                threshold=args.threshold,
                max_iterations=args.max_iterations,
                verbose=args.verbose,
            )
            results.append(result)
            
            # Save immediately after each prompt (incremental backup)
            save_incremental_result(result, output_path, len(prompts))
            
        except Exception as e:
            print(f"❌ Error evaluating {prompt_path.name}: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            
            # Save error result so we know it failed
            error_result = LATS_Result(
                prompt_file=str(prompt_path),
                initial_score=0.0,
                final_score=0.0,
                iterations=0,
                improvement=0.0,
                threshold_met=False,
                key_changes=[f"ERROR: {str(e)[:100]}"],
                duration_seconds=0.0,
                model=selected_model,
                timestamp=datetime.now().isoformat(),
            )
            results.append(error_result)
            save_incremental_result(error_result, output_path, len(prompts))
        
        # Delay between prompts
        if args.delay > 0 and i < len(prompts):
            time.sleep(args.delay)
    
    duration = time.time() - start_time
    
    # Generate report
    coverage = generate_coverage_report(results, len(prompts), duration)
    
    # Print summary
    print(f"\n{'='*60}")
    print("📊 LATS EVALUATION SUMMARY")
    print(f"{'='*60}")
    print(f"Total Prompts:    {coverage.total_prompts}")
    print(f"Evaluated:        {coverage.evaluated}")
    print(f"Passed:           {coverage.passed} ({coverage.passed/coverage.evaluated*100:.1f}%)")
    print(f"Failed:           {coverage.failed}")
    print(f"Avg Improvement:  +{coverage.avg_improvement:.1f}%")
    print(f"Total Duration:   {coverage.duration_seconds/60:.1f} minutes")
    print(f"{'='*60}")
    
    # Final save with complete status
    coverage_data = {
        "timestamp": datetime.now().isoformat(),
        "status": "complete",
        "summary": {
            "total_prompts": coverage.total_prompts,
            "evaluated": coverage.evaluated,
            "passed": coverage.passed,
            "failed": coverage.failed,
            "skipped": coverage.skipped,
            "avg_improvement": coverage.avg_improvement,
            "duration_seconds": coverage.duration_seconds,
        },
        "folders": coverage.folders,
        "results": [asdict(r) for r in coverage.results],
    }
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(coverage_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Final results saved to: {output_path}")
    
    return 0 if coverage.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
