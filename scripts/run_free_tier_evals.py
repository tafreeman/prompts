#!/usr/bin/env python3
"""
Run tiered evaluations against the prompt library using free models only.

This script executes multiple evaluation runs using a mix of:
- Local ONNX models (local:*)
- Ollama models (ollama:*)
- AI Toolkit models (aitk:*)
- GitHub Models (gh:*) - free tier

Usage:
    python scripts/run_free_tier_evals.py
    python scripts/run_free_tier_evals.py --path prompts/analysis
    python scripts/run_free_tier_evals.py --tiers 1 2 --quick
    python scripts/run_free_tier_evals.py --discovery  # Use all discovered models
    python scripts/run_free_tier_evals.py --parallel 2  # Run 2 models in parallel

Environment:
    GITHUB_TOKEN: Required for gh:* models
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


# ============================================================================
# Configuration
# ============================================================================

REPO_ROOT = Path(__file__).resolve().parent.parent

# Default free models to evaluate with (curated for quality/speed balance)
DEFAULT_LOCAL_MODELS = [
    "local:phi4-cpu",
    "local:phi4-gpu",
    "local:phi3.5-cpu",
]

DEFAULT_OLLAMA_MODELS = [
    "ollama:phi4-reasoning:latest",
    "ollama:qwen3:8b",
    "ollama:deepseek-r1:8b",
]

DEFAULT_AITK_MODELS = [
    "aitk:phi-4-mini-reasoning",
    "aitk:phi-4-mini-instruct",
]

# GitHub Models - free tier (rate limited but free)
DEFAULT_GH_MODELS = [
    "gh:microsoft/phi-4-mini-reasoning",
    "gh:openai/gpt-4o-mini",
    "gh:meta/meta-llama-3.1-8b-instruct",
]

# Quick mode uses fewer, faster models (1 local + 1 cloud for parallel)
QUICK_LOCAL_MODELS = ["local:phi4-cpu"]
QUICK_OLLAMA_MODELS = ["ollama:qwen3:8b"]
QUICK_GH_MODELS = ["gh:openai/gpt-4o-mini"]

# Default balanced mode: 1 local + 1 cloud for parallel execution
BALANCED_LOCAL = ["local:phi4-cpu"]
BALANCED_CLOUD = ["gh:openai/gpt-4o-mini"]

# Tiers that make sense for evaluation
EVAL_TIERS = [1, 2, 3]

RESULTS_DIR = REPO_ROOT / "results" / "free-tier-evals"
LOG_DIR = REPO_ROOT / "logs"


@dataclass
class EvalRun:
    """Represents a single evaluation run."""
    path: str
    tier: int
    model: str
    output_file: Path
    status: str = "pending"
    exit_code: Optional[int] = None
    error: Optional[str] = None
    duration_seconds: float = 0.0


@dataclass
class EvalSession:
    """Tracks all runs in an evaluation session."""
    started: datetime = field(default_factory=datetime.now)
    runs: list[EvalRun] = field(default_factory=list)
    
    @property
    def summary(self) -> dict:
        passed = sum(1 for r in self.runs if r.status == "passed")
        failed = sum(1 for r in self.runs if r.status == "failed")
        skipped = sum(1 for r in self.runs if r.status == "skipped")
        return {
            "total": len(self.runs),
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "success_rate": f"{passed / len(self.runs) * 100:.1f}%" if self.runs else "N/A"
        }


# ============================================================================
# Discovery Integration
# ============================================================================

def load_discovery() -> dict:
    """Load available models from discovery_results.json."""
    discovery_path = REPO_ROOT / "discovery_results.json"
    if not discovery_path.exists():
        print(f"⚠️  discovery_results.json not found. Run:")
        print(f"   python -m tools.llm.model_probe --discover --force -o discovery_results.json")
        return {}
    
    try:
        return json.loads(discovery_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"⚠️  Error reading discovery_results.json: {e}")
        return {}


def get_free_models_from_discovery(
    include_local: bool = True,
    include_ollama: bool = True,
    include_aitk: bool = True,
    include_gh: bool = True,
    max_per_provider: int = 5,
) -> list[str]:
    """Extract free models from discovery results."""
    discovery = load_discovery()
    providers = discovery.get("providers", {})
    models: list[str] = []
    
    provider_map = {
        "local_onnx": include_local,
        "ollama": include_ollama,
        "ai_toolkit": include_aitk,
        "github_models": include_gh,
    }
    
    for provider_key, include in provider_map.items():
        if not include:
            continue
        provider_data = providers.get(provider_key, {})
        available = provider_data.get("available", [])
        
        # Filter out non-generation models (whisper, stable-diffusion, embeddings)
        filtered = [
            m for m in available
            if not any(x in m.lower() for x in ["whisper", "stable-diffusion", "minilm", "esrgan", "vision"])
        ]
        
        # Take top N models
        models.extend(filtered[:max_per_provider] if max_per_provider > 0 else filtered)
    
    return models


def check_ollama_available() -> bool:
    """Check if Ollama server is running."""
    import urllib.request
    import urllib.error
    
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    try:
        req = urllib.request.Request(f"{host}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=5):
            return True
    except (urllib.error.URLError, TimeoutError):
        return False


def check_github_token() -> bool:
    """Check if GitHub token is configured."""
    return bool(os.getenv("GITHUB_TOKEN"))


# ============================================================================
# Evaluation Runner
# ============================================================================

def safe_filename(s: str) -> str:
    """Convert a string to a safe filename."""
    return s.replace(":", "-").replace("/", "-").replace("\\", "-").replace(" ", "_")


def run_single_eval(
    path: str,
    tier: int,
    model: str,
    output_dir: Path,
    verbose: bool = False,
    ci: bool = True,
) -> EvalRun:
    """Run a single evaluation."""
    import time
    
    safe_path = safe_filename(path.replace("prompts/", "").rstrip("/") or "all")
    safe_model = safe_filename(model)
    output_file = output_dir / f"{safe_path}__tier{tier}__{safe_model}.json"
    
    run = EvalRun(
        path=path,
        tier=tier,
        model=model,
        output_file=output_file,
    )
    
    # Build command
    cmd = [
        sys.executable, "-m", "tools.prompteval",
        path,
        "--tier", str(tier),
        "--model", model,
        "--output", str(output_file),
    ]
    if verbose:
        cmd.append("--verbose")
    if ci:
        cmd.append("--ci")
    
    start_time = time.time()
    
    try:
        print(f"  🔄 [{model}] tier={tier} path={path}")
        result = subprocess.run(
            cmd,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=600,  # 10 minute timeout per eval
        )
        run.exit_code = result.returncode
        run.duration_seconds = time.time() - start_time
        
        # Check for errors in output JSON
        if output_file.exists():
            try:
                data = json.loads(output_file.read_text(encoding="utf-8"))
                # "errors" > 0 means evaluation errors (not prompt failures)
                # "failed" in JSON is prompts below threshold, which is normal
                if data.get("error"):
                    run.status = "failed"
                    run.error = data.get("error")
                elif data.get("errors", 0) > 0:
                    run.status = "failed"
                    run.error = f"Evaluation errors: {data.get('errors')}"
                elif result.returncode == 0:
                    run.status = "passed"
                    # Include summary info
                    run.error = f"passed={data.get('passed', 0)}/{data.get('total', 0)}, avg={data.get('avg_score', 0):.1f}"
                else:
                    run.status = "failed"
                    run.error = f"Exit code {result.returncode}"
            except json.JSONDecodeError as e:
                run.status = "failed"
                run.error = f"Invalid JSON output: {e}"
        elif result.returncode != 0:
            run.status = "failed"
            run.error = result.stderr[:500] if result.stderr else f"Exit code {result.returncode}"
        else:
            run.status = "passed"
            
    except subprocess.TimeoutExpired:
        run.status = "failed"
        run.error = "Timeout (10 min)"
        run.duration_seconds = time.time() - start_time
    except Exception as e:
        run.status = "failed"
        run.error = str(e)
        run.duration_seconds = time.time() - start_time
    
    status_icon = "✅" if run.status == "passed" else "❌"
    print(f"  {status_icon} [{model}] {run.status} ({run.duration_seconds:.1f}s)")
    
    return run


def run_evaluation_matrix(
    path: str,
    tiers: list[int],
    models: list[str],
    output_dir: Path,
    parallel: int = 1,
    verbose: bool = False,
    ci: bool = True,
) -> EvalSession:
    """Run evaluation matrix across tiers and models."""
    session = EvalSession()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Build list of all runs
    runs_to_execute: list[tuple[str, int, str]] = []
    for tier in tiers:
        for model in models:
            runs_to_execute.append((path, tier, model))
    
    print(f"\n📊 Starting evaluation matrix:")
    print(f"   Path: {path}")
    print(f"   Tiers: {tiers}")
    print(f"   Models: {len(models)}")
    print(f"   Total runs: {len(runs_to_execute)}")
    print(f"   Parallel: {parallel}")
    print(f"   Output: {output_dir}\n")
    
    if parallel > 1:
        # Parallel execution
        with ThreadPoolExecutor(max_workers=parallel) as executor:
            futures = {
                executor.submit(
                    run_single_eval, p, t, m, output_dir, verbose, ci
                ): (p, t, m)
                for p, t, m in runs_to_execute
            }
            for future in as_completed(futures):
                run = future.result()
                session.runs.append(run)
    else:
        # Sequential execution
        for p, t, m in runs_to_execute:
            run = run_single_eval(p, t, m, output_dir, verbose, ci)
            session.runs.append(run)
    
    return session


# ============================================================================
# Report Generation
# ============================================================================

def generate_summary_report(session: EvalSession, output_dir: Path) -> Path:
    """Generate a summary report of the evaluation session."""
    report_path = output_dir / "summary.json"
    
    report = {
        "session": {
            "started": session.started.isoformat(),
            "completed": datetime.now().isoformat(),
            "duration_seconds": (datetime.now() - session.started).total_seconds(),
        },
        "summary": session.summary,
        "runs": [
            {
                "path": r.path,
                "tier": r.tier,
                "model": r.model,
                "status": r.status,
                "exit_code": r.exit_code,
                "duration_seconds": r.duration_seconds,
                "output_file": str(r.output_file),
                "error": r.error,
            }
            for r in session.runs
        ],
        "by_model": {},
        "by_tier": {},
    }
    
    # Aggregate by model
    for run in session.runs:
        if run.model not in report["by_model"]:
            report["by_model"][run.model] = {"passed": 0, "failed": 0, "total": 0}
        report["by_model"][run.model]["total"] += 1
        if run.status == "passed":
            report["by_model"][run.model]["passed"] += 1
        else:
            report["by_model"][run.model]["failed"] += 1
    
    # Aggregate by tier
    for run in session.runs:
        tier_key = f"tier_{run.tier}"
        if tier_key not in report["by_tier"]:
            report["by_tier"][tier_key] = {"passed": 0, "failed": 0, "total": 0}
        report["by_tier"][tier_key]["total"] += 1
        if run.status == "passed":
            report["by_tier"][tier_key]["passed"] += 1
        else:
            report["by_tier"][tier_key]["failed"] += 1
    
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report_path


def print_summary(session: EvalSession) -> None:
    """Print a human-readable summary."""
    summary = session.summary
    
    print("\n" + "=" * 60)
    print("📊 EVALUATION SUMMARY")
    print("=" * 60)
    print(f"Total runs: {summary['total']}")
    print(f"  ✅ Passed: {summary['passed']}")
    print(f"  ❌ Failed: {summary['failed']}")
    print(f"  ⏭️  Skipped: {summary['skipped']}")
    print(f"Success rate: {summary['success_rate']}")
    
    # Group failures by model
    failures = [r for r in session.runs if r.status == "failed"]
    if failures:
        print("\n❌ Failed runs:")
        for run in failures:
            print(f"  • {run.model} (tier {run.tier}): {run.error or 'Unknown error'}")
    
    print("=" * 60)


# ============================================================================
# CLI
# ============================================================================

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run tiered evaluations using free models (local + Ollama + GitHub Models)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default free models
  python scripts/run_free_tier_evals.py

  # Evaluate specific folder
  python scripts/run_free_tier_evals.py --path prompts/analysis

  # Quick mode (fewer models, faster)
  python scripts/run_free_tier_evals.py --quick

  # Use all discovered free models
  python scripts/run_free_tier_evals.py --discovery

  # Specific tiers only
  python scripts/run_free_tier_evals.py --tiers 1 2

  # Parallel execution
  python scripts/run_free_tier_evals.py --parallel 2

  # Skip cloud models (local only)
  python scripts/run_free_tier_evals.py --local-only
        """
    )
    
    parser.add_argument(
        "--path", "-p",
        default="prompts/",
        help="Path to evaluate (default: prompts/)"
    )
    parser.add_argument(
        "--tiers", "-t",
        type=int,
        nargs="+",
        default=[0, 1, 2, 3],
        help="Tiers to run (default: 0 1 2 3 - all tiers)"
    )
    parser.add_argument(
        "--models", "-m",
        nargs="+",
        help="Specific models to use (overrides defaults)"
    )
    parser.add_argument(
        "--discovery",
        action="store_true",
        help="Use all free models from discovery_results.json"
    )
    parser.add_argument(
        "--max-per-provider",
        type=int,
        default=3,
        help="Max models per provider when using --discovery (default: 3)"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Quick mode: use minimal set of fast models"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Full mode: use all default free models (local + ollama + aitk + gh)"
    )
    parser.add_argument(
        "--local-only",
        action="store_true",
        help="Only use local models (no cloud/GitHub)"
    )
    parser.add_argument(
        "--no-gh",
        action="store_true",
        help="Exclude GitHub Models"
    )
    parser.add_argument(
        "--parallel",
        type=int,
        default=2,
        help="Number of parallel evaluations (default: 2 - one local, one cloud)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        default=True,
        help="Verbose output (default: True)"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Quiet mode - disable verbose output"
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        help="Log file path (default: logs/free-tier-eval-<timestamp>.log)"
    )
    parser.add_argument(
        "--no-log-file",
        action="store_true",
        help="Disable log file output"
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=Path,
        default=RESULTS_DIR,
        help=f"Output directory (default: {RESULTS_DIR})"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be run without executing"
    )
    
    return parser.parse_args()


def setup_logging(log_file: Optional[Path], verbose: bool) -> Optional[Path]:
    """Configure logging to file and console."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    if log_file is None:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_file = LOG_DIR / f"free-tier-eval-{timestamp}.log"
    
    # Configure root logger
    level = logging.DEBUG if verbose else logging.INFO
    
    # File handler - always verbose
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(logging.Formatter("%(message)s"))
    
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[file_handler, console_handler]
    )
    
    return log_file


def main() -> int:
    args = parse_args()
    
    # Handle verbose/quiet
    verbose = args.verbose and not args.quiet
    
    # Setup logging (default: enabled with auto log file)
    log_file = None
    if not args.no_log_file:
        log_file = setup_logging(args.log_file, verbose)
        print(f"📝 Log file: {log_file}")
    
    # Determine models to use
    if args.models:
        models = args.models
    elif args.discovery:
        print("🔍 Loading models from discovery_results.json...")
        models = get_free_models_from_discovery(
            include_local=True,
            include_ollama=not args.local_only,
            include_aitk=True,
            include_gh=not args.local_only and not args.no_gh,
            max_per_provider=args.max_per_provider,
        )
        if not models:
            print("❌ No models found in discovery. Run model probe first:")
            print("   python -m tools.llm.model_probe --discover --force -o discovery_results.json")
            return 1
    elif args.quick:
        models = QUICK_LOCAL_MODELS.copy()
        if not args.local_only:
            models.extend(QUICK_OLLAMA_MODELS)
            if not args.no_gh:
                models.extend(QUICK_GH_MODELS)
    elif args.full:
        # Full mode: all default free models
        models = DEFAULT_LOCAL_MODELS.copy()
        if not args.local_only:
            models.extend(DEFAULT_OLLAMA_MODELS)
            models.extend(DEFAULT_AITK_MODELS)
            if not args.no_gh:
                models.extend(DEFAULT_GH_MODELS)
    else:
        # Default: balanced mode - 1 local + 1 cloud for parallel execution
        models = BALANCED_LOCAL.copy()
        if not args.local_only and not args.no_gh:
            models.extend(BALANCED_CLOUD)
    
    # Check prerequisites
    print("\n🔍 Checking prerequisites...")
    
    has_ollama_models = any(m.startswith("ollama:") for m in models)
    has_gh_models = any(m.startswith("gh:") for m in models)
    
    if has_ollama_models and not check_ollama_available():
        print("⚠️  Ollama server not available. Removing ollama:* models.")
        models = [m for m in models if not m.startswith("ollama:")]
    
    if has_gh_models and not check_github_token():
        print("⚠️  GITHUB_TOKEN not set. Removing gh:* models.")
        models = [m for m in models if not m.startswith("gh:")]
    
    if not models:
        print("❌ No models available to run. Check prerequisites:")
        print("   - Local models: Ensure AI Toolkit models are downloaded")
        print("   - Ollama: Start Ollama server (ollama serve)")
        print("   - GitHub: Set GITHUB_TOKEN environment variable")
        return 1
    
    print(f"✅ Using {len(models)} models")
    
    # Show what would run
    print(f"\n📋 Evaluation plan:")
    print(f"   Path: {args.path}")
    print(f"   Tiers: {args.tiers}")
    print(f"   Models ({len(models)}):")
    for m in models:
        print(f"      • {m}")
    print(f"   Total runs: {len(args.tiers) * len(models)}")
    
    if args.dry_run:
        print("\n🔶 Dry run - no evaluations executed")
        return 0
    
    # Create timestamped output directory
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = args.output_dir / timestamp
    
    # Run evaluations
    session = run_evaluation_matrix(
        path=args.path,
        tiers=args.tiers,
        models=models,
        output_dir=output_dir,
        parallel=args.parallel,
        verbose=args.verbose,
    )
    
    # Generate reports
    report_path = generate_summary_report(session, output_dir)
    print(f"\n📄 Summary report: {report_path}")
    
    print_summary(session)
    
    # Return non-zero if any failures
    return 0 if session.summary["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
