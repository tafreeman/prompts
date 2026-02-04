#!/usr/bin/env python3
"""
Multi-Model Batch Evaluator
===========================

Evaluates all prompts in a directory across multiple local models,
generating comparison reports.

Usage:
    python batch_evaluate_models.py
    python batch_evaluate_models.py --prompts-dir path/to/prompts
    python batch_evaluate_models.py --models phi4,mistral,phi3-medium
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core.local_model import MODEL_REGISTRY
from evaluator import EnterpriseEvaluator

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

# Default models to evaluate with (subset for speed, can be overridden)
DEFAULT_MODELS = ["phi4", "phi3.5", "phi3", "mistral", "phi3-medium"]

# Files to skip (index, readme, etc.)
SKIP_FILES = {"README.md", "index.md", "_audit_chain-of-thought-guide.md"}


def get_available_models() -> List[str]:
    """Return list of models that are actually available on disk."""
    available = []
    for key, path in MODEL_REGISTRY.items():
        if path.exists():
            available.append(key)
    return list(set(available))  # Remove duplicates (phi4 == phi4mini)


def evaluate_with_model(
    model_key: str, prompt_files: List[Path], output_dir: Path
) -> Dict[str, Any]:
    """Evaluate all prompts with a single model.

    Supports both local models (phi4, mistral) and remote models
    (gh:gpt-4o, azure-foundry:phi4).

    Returns summary statistics and saves detailed results.
    """
    # Determine if this is a remote model (has prefix like gh:, azure-foundry:, etc.)
    is_remote = ":" in model_key

    if is_remote:
        model_name = model_key  # Use as-is (e.g., "gh:gpt-4o")
        display_name = model_key.replace(":", "_")  # For filenames
    else:
        model_name = f"local:{model_key}"
        display_name = model_key

    print(f"\n{'='*60}")
    print(f"MODEL: {model_key.upper()}")
    print(f"{'='*60}")

    # Only check local model paths for non-remote models
    if not is_remote:
        if model_key not in MODEL_REGISTRY:
            print(f"  ❌ Model '{model_key}' not found in registry")
            return {"model": model_key, "error": "not found", "results": []}

        model_path = MODEL_REGISTRY[model_key]
        if not model_path.exists():
            print(f"  ❌ Model path does not exist: {model_path}")
            return {"model": model_key, "error": "path not found", "results": []}

    # Initialize evaluator
    try:
        evaluator = EnterpriseEvaluator(model_name=model_name, temperature=0.1)
    except Exception as e:
        print(f"  ❌ Failed to initialize: {e}")
        return {"model": model_key, "error": str(e), "results": []}

    results = []
    scores = []

    for i, prompt_file in enumerate(prompt_files, 1):
        print(f"  [{i}/{len(prompt_files)}] {prompt_file.name}...", end=" ", flush=True)

        try:
            start_time = time.time()
            result = evaluator.evaluate_file(str(prompt_file))
            elapsed = time.time() - start_time

            result["evaluation_time_seconds"] = round(elapsed, 2)
            results.append(result)
            scores.append(result["final_score"])

            print(
                f"Score: {result['final_score']:.1f} ({result['performance_level']}) [{elapsed:.1f}s]"
            )

        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({"file": str(prompt_file), "error": str(e)})

    # Calculate summary statistics
    summary = {
        "model": model_key,
        "model_type": "remote" if is_remote else "local",
        "total_prompts": len(prompt_files),
        "successful": len(scores),
        "failed": len(prompt_files) - len(scores),
        "avg_score": round(sum(scores) / len(scores), 2) if scores else 0,
        "min_score": min(scores) if scores else 0,
        "max_score": max(scores) if scores else 0,
        "results": results,
    }

    # Save model-specific results (sanitize filename for remote models)
    safe_name = display_name.replace(":", "_").replace("/", "_")
    output_file = output_dir / f"results_{safe_name}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"  → Saved to: {output_file}")

    return summary


def main():
    parser = argparse.ArgumentParser(
        description="Batch evaluate prompts across multiple local models"
    )

    parser.add_argument(
        "--prompts-dir",
        "-p",
        default=r"d:\source\prompts\prompts\advanced",
        help="Directory containing prompts to evaluate",
    )

    parser.add_argument(
        "--models",
        "-m",
        default=None,
        help="Comma-separated list of models to use (default: all available)",
    )

    parser.add_argument(
        "--output-dir",
        "-o",
        default=None,
        help="Directory to save results (default: ./batch_results_<timestamp>)",
    )

    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=None,
        help="Limit number of prompts to evaluate (for testing)",
    )

    parser.add_argument(
        "--list-models", action="store_true", help="List available models and exit"
    )

    args = parser.parse_args()

    # List models mode
    if args.list_models:
        print("\n📦 Available Local Models:")
        print("-" * 40)
        available = get_available_models()
        for key in sorted(MODEL_REGISTRY.keys()):
            status = "✅" if key in available else "❌"
            print(f"  {status} local:{key}")
        sys.exit(0)

    # Determine models to use
    if args.models:
        models_to_use = [m.strip() for m in args.models.split(",")]
    else:
        # Use all available, removing duplicates
        available = get_available_models()
        # Prefer canonical names
        models_to_use = []
        seen_paths = set()
        for m in DEFAULT_MODELS:
            if m in available:
                path = str(MODEL_REGISTRY[m])
                if path not in seen_paths:
                    models_to_use.append(m)
                    seen_paths.add(path)

    print("\n🚀 Multi-Model Batch Evaluator")
    print("=" * 60)
    print(f"Models: {', '.join(models_to_use)}")

    # Find prompts
    prompts_dir = Path(args.prompts_dir)
    if not prompts_dir.exists():
        print(f"❌ Prompts directory not found: {prompts_dir}")
        sys.exit(1)

    prompt_files = [
        f for f in sorted(prompts_dir.glob("*.md")) if f.name not in SKIP_FILES
    ]

    if args.limit:
        prompt_files = prompt_files[: args.limit]

    print(f"Prompts: {len(prompt_files)} files in {prompts_dir.name}/")

    # Setup output directory
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path(f"batch_results_{timestamp}")

    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output: {output_dir}/")

    # Run evaluations
    all_summaries = []
    start_time = time.time()

    for model in models_to_use:
        try:
            summary = evaluate_with_model(model, prompt_files, output_dir)
            all_summaries.append(summary)
        except KeyboardInterrupt:
            print("\n\n⚠️ Interrupted by user. Saving partial results...")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error with {model}: {e}")
            all_summaries.append({"model": model, "error": str(e)})

    total_time = time.time() - start_time

    # Generate comparison report
    print(f"\n{'='*60}")
    print("COMPARISON SUMMARY")
    print(f"{'='*60}")
    print(f"{'Model':<15} {'Avg Score':>10} {'Min':>8} {'Max':>8} {'Success':>10}")
    print("-" * 60)

    for s in all_summaries:
        if "error" not in s or s.get("successful", 0) > 0:
            print(
                f"{s['model']:<15} {s.get('avg_score', 0):>10.1f} {s.get('min_score', 0):>8.1f} {s.get('max_score', 0):>8.1f} {s.get('successful', 0):>7}/{s.get('total_prompts', 0)}"
            )
        else:
            print(f"{s['model']:<15} {'ERROR':>10} {'-':>8} {'-':>8} {'0/0':>10}")

    print("-" * 60)
    print(f"Total time: {total_time/60:.1f} minutes")

    # Save master summary
    master_summary = {
        "timestamp": datetime.now().isoformat(),
        "prompts_directory": str(prompts_dir),
        "total_prompts": len(prompt_files),
        "models_evaluated": len(all_summaries),
        "total_time_seconds": round(total_time, 2),
        "model_summaries": all_summaries,
    }

    summary_file = output_dir / "comparison_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(master_summary, f, indent=2)

    print(f"\n✅ Master summary saved to: {summary_file}")


if __name__ == "__main__":
    main()
