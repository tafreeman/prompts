#!/usr/bin/env python3
"""Run evaluate_prompt() on all prompts in prompts/advanced folder.

Features:
- Scans for all available ONNX models in the AI Gallery cache
- Shows which models are available vs in use by other processes
- Lets user select which model to use
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple

sys.path.insert(0, str(Path(__file__).parent))
from local_model import LocalModel
from model_locks import create_model_lock, get_models_in_use

# Known model configurations in AI Gallery
MODEL_CONFIGS = {
    "Phi-4 Mini": {
        "folder": "microsoft--Phi-4-mini-instruct-onnx",
        "subpaths": [
            "main/cpu_and_mobile/cpu-int4-rtn-block-32-acc-level-4",
            "cpu_and_mobile/cpu-int4-rtn-block-32-acc-level-4",
        ],
        "speed": "fastest",
        "quality": "good",
    },
    "Phi-3.5 Mini": {
        "folder": "microsoft--Phi-3.5-mini-instruct-onnx",
        "subpaths": [
            "main/cpu_and_mobile/cpu-int4-awq-block-128-acc-level-4",
            "cpu_and_mobile/cpu-int4-awq-block-128-acc-level-4",
        ],
        "speed": "fast",
        "quality": "good",
    },
    "Phi-3 Mini": {
        "folder": "microsoft--Phi-3-mini-4k-instruct-onnx",
        "subpaths": [
            "main/cpu_and_mobile/cpu-int4-rtn-block-32-acc-level-4",
            "cpu_and_mobile/cpu-int4-rtn-block-32-acc-level-4",
            "cpu-int4-rtn-block-32-acc-level-4",
        ],
        "speed": "fast",
        "quality": "good",
    },
    "Phi-3 Medium": {
        "folder": "microsoft--Phi-3-medium-4k-instruct-onnx-cpu",
        "subpaths": [
            "main/cpu-int4-rtn-block-32-acc-level-4",
            "cpu-int4-rtn-block-32-acc-level-4",
            "",  # Root folder
        ],
        "speed": "slow",
        "quality": "best",
    },
    "Mistral 7B": {
        "folder": "microsoft--mistral-7b-instruct-v0.2-ONNX",
        "subpaths": [
            "main/onnx/cpu_and_mobile/mistral-7b-instruct-v0.2-cpu-int4-rtn-block-32-acc-level-4",
        ],
        "speed": "medium",
        "quality": "great",
    },
}


def get_aigallery_path() -> Path:
    """Get the AI Gallery cache path."""
    return Path.home() / ".cache" / "aigallery"


def scan_available_models() -> Dict[str, Path]:
    """Scan for available ONNX models and return their paths."""
    available = {}
    cache_path = get_aigallery_path()

    if not cache_path.exists():
        return available

    for name, config in MODEL_CONFIGS.items():
        folder_path = cache_path / config["folder"]
        if folder_path.exists():
            # Try each subpath
            for subpath in config["subpaths"]:
                if subpath:
                    full_path = folder_path / subpath
                else:
                    full_path = folder_path

                # Check if this path contains an ONNX model
                if full_path.exists():
                    # Look for genai_config.json or *.onnx files
                    has_config = (full_path / "genai_config.json").exists()
                    has_onnx = list(full_path.glob("*.onnx"))

                    if has_config or has_onnx:
                        available[name] = full_path
                        break

    return available


def display_model_menu(available: Dict[str, Path]) -> Tuple[str, Path]:
    """Display available models and let user select one."""
    print("\n" + "=" * 60)
    print("AVAILABLE LOCAL MODELS")
    print("=" * 60)

    # Check which models are in use (fast file lock check)
    print("\nChecking for models in use...")
    models_in_use = get_models_in_use(available)
    if models_in_use:
        print(f"Found {len(models_in_use)} model(s) in use by other processes")

    models_list = []
    for i, (name, path) in enumerate(available.items(), 1):
        config = MODEL_CONFIGS.get(name, {})
        speed = config.get("speed", "unknown")
        quality = config.get("quality", "unknown")

        # Check if in use
        in_use = name in models_in_use
        status = "🔒 IN USE" if in_use else "✓ Available"

        print(f"\n  [{i}] {name}")
        print(f"      Speed: {speed} | Quality: {quality}")
        print(f"      Status: {status}")
        if in_use:
            print(f"      Info: {models_in_use[name]}")

        models_list.append((name, path, in_use))

    print("\n" + "-" * 60)

    # Get user selection
    while True:
        try:
            choice = input("\nSelect model number (or 'q' to quit): ").strip()

            if choice.lower() == "q":
                print("Cancelled.")
                sys.exit(0)

            idx = int(choice) - 1
            if 0 <= idx < len(models_list):
                name, path, in_use = models_list[idx]

                if in_use:
                    confirm = (
                        input(
                            f"\n⚠️  {name} appears to be in use. Continue anyway? (y/n): "
                        )
                        .strip()
                        .lower()
                    )
                    if confirm != "y":
                        continue

                return name, path
            else:
                print(f"Please enter a number between 1 and {len(models_list)}")

        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\nCancelled.")
            sys.exit(0)


def main():
    # Scan for available models
    print("\nScanning for available ONNX models...")
    available = scan_available_models()

    if not available:
        print("\n❌ No ONNX models found in AI Gallery cache!")
        print(f"   Checked: {get_aigallery_path()}")
        print("\nTo download models, use:")
        print("  - Windows AI Gallery app")
        print("  - Or manually place models in the cache directory")
        sys.exit(1)

    # Let user select model
    model_name, model_path = display_model_menu(available)

    # Get prompts to evaluate
    folder = Path(__file__).parent.parent / "prompts" / "advanced"
    prompts = [
        f
        for f in sorted(folder.glob("*.md"))
        if f.name not in ["README.md", "index.md"]
    ]

    print(f"\n{'='*60}")
    print("DIRECT EVALUATION (evaluate_prompt)")
    print(f"Model: {model_name}")
    print(f"Path: {model_path}")
    print(f"Prompts: {len(prompts)}")
    print(f"{'='*60}\n")

    # Load model
    try:
        model = LocalModel(model_path=str(model_path), verbose=False)
        create_model_lock(model_name)  # Mark model as in use
        print("✓ Model loaded\n")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        sys.exit(1)

    results = []
    for i, p in enumerate(prompts, 1):
        print(f"\n[{i}/{len(prompts)}] {p.name}")
        print("-" * 50)
        try:
            content = p.read_text(encoding="utf-8")
            result = model.evaluate_prompt(content)
            score = result.get("overall", 0)
            scores_detail = result.get("scores", {})
            summary = result.get("summary", "")

            # Display individual criteria scores
            if scores_detail:
                criteria_line = " | ".join(
                    f"{k[:4]}:{v}"
                    for k, v in scores_detail.items()
                    if isinstance(v, (int, float))
                )
                print(f"  Criteria: {criteria_line}")

            # Display summary if available
            if summary:
                # Truncate long summaries
                summary_display = (
                    summary[:100] + "..." if len(summary) > 100 else summary
                )
                print(f"  Summary: {summary_display}")

            print(f"  ★ Overall Score: {score}")

            results.append(
                {
                    "file": p.name,
                    "score": score,
                    "details": scores_detail,
                    "summary": summary,
                }
            )
        except Exception as e:
            print(f"  ❌ Error: {e}")
            results.append({"file": p.name, "error": str(e)})

    # Summary with score distribution
    scores = [r["score"] for r in results if "score" in r and r["score"] > 0]
    avg = sum(scores) / len(scores) if scores else 0

    # Calculate score distribution
    excellent = len([s for s in scores if s >= 9])
    good = len([s for s in scores if 7 <= s < 9])
    fair = len([s for s in scores if 5 <= s < 7])
    poor = len([s for s in scores if s < 5])

    print(f"\n{'='*60}")
    print("SUMMARY - Direct Evaluation")
    print(f"{'='*60}")
    print(f"Model: {model_name}")
    print(f"Prompts evaluated: {len(results)}")
    print(f"Average score: {avg:.2f}")
    print("\nScore Distribution:")
    print(f"  ★★★ Excellent (9+):  {excellent}")
    print(f"  ★★  Good (7-8.9):    {good}")
    print(f"  ★   Fair (5-6.9):    {fair}")
    print(f"  ✗   Poor (<5):       {poor}")

    # Show top and bottom performers
    if scores:
        sorted_results = sorted(
            [r for r in results if "score" in r and r["score"] > 0],
            key=lambda x: x["score"],
            reverse=True,
        )
        print("\n🏆 Top 3:")
        for r in sorted_results[:3]:
            print(f"  {r['score']:.1f} - {r['file']}")

        if len(sorted_results) > 3:
            print("\n⚠️  Needs Improvement:")
            for r in sorted_results[-3:]:
                print(f"  {r['score']:.1f} - {r['file']}")

    print(f"{'='*60}\n")

    # Save results
    output = Path(__file__).parent.parent / "eval_direct_results.json"
    with open(output, "w") as f:
        json.dump(
            {
                "method": "direct",
                "model": model_name,
                "model_path": str(model_path),
                "date": datetime.now().isoformat(),
                "avg_score": round(avg, 2),
                "score_distribution": {
                    "excellent": excellent,
                    "good": good,
                    "fair": fair,
                    "poor": poor,
                },
                "results": results,
            },
            f,
            indent=2,
        )
    print(f"Results saved to: {output}")


if __name__ == "__main__":
    main()
