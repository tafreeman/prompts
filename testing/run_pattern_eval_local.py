#!/usr/bin/env python3
"""
Run pattern evaluation with local models.

This script demonstrates using local ONNX models to evaluate
pattern conformance for advanced prompts.

Usage:
    # Quick evaluation (1 run) with phi4mini
    python testing/run_pattern_eval_local.py prompts/advanced/CoVe.md output.txt

    # Full evaluation (20 runs) with specific model
    python testing/run_pattern_eval_local.py prompts/advanced/react-tool-augmented.md output.txt --model local:phi3.5 --runs 20

    # With pattern override
    python testing/run_pattern_eval_local.py prompts/advanced/my-prompt.md output.txt --pattern react
"""

import sys
import argparse
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.llm.llm_client import LLMClient
from tools.prompteval.pattern_evaluator import PatternEvaluator, evaluate_pattern
from tools.prompteval.integration import evaluate_with_pattern, detect_pattern_from_frontmatter
from tools.prompteval.parser import detect_pattern, get_available_patterns
from prompttools.parse import parse_frontmatter


def main():
    parser = argparse.ArgumentParser(description="Evaluate pattern conformance with local models")

    parser.add_argument(
        "prompt_file",
        type=str,
        help="Path to prompt file to evaluate (e.g., prompts/advanced/CoVe.md)",
    )

    parser.add_argument(
        "output_file",
        type=str,
        help="Path to file containing model output to evaluate",
    )

    parser.add_argument(
        "--model",
        type=str,
        default="local:phi4mini",
        help="Model to use for judging (default: local:phi4mini). Options: local:phi4mini, local:phi3.5, local:mistral-7b",
    )

    parser.add_argument(
        "--pattern",
        choices=get_available_patterns(),
        help="Override pattern detection (auto-detect if not specified)",
    )

    parser.add_argument(
        "--runs",
        type=int,
        default=1,
        help="Number of evaluation runs (default: 1 for quick test, use 20 for robust evaluation)",
    )

    parser.add_argument(
        "--temperature",
        type=float,
        default=0.1,
        help="Judge sampling temperature (default: 0.1 for consistency)",
    )

    parser.add_argument(
        "--output-json",
        type=str,
        help="Save detailed results to JSON file",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed progress",
    )

    args = parser.parse_args()

    # Validate files exist
    prompt_path = Path(args.prompt_file)
    output_path = Path(args.output_file)

    if not prompt_path.exists():
        print(f"Error: Prompt file not found: {prompt_path}", file=sys.stderr)
        return 1

    if not output_path.exists():
        print(f"Error: Output file not found: {output_path}", file=sys.stderr)
        return 1

    # Load files
    print(f"\n{'='*60}")
    print(f" Pattern Evaluation with Local Models")
    print(f"{'='*60}\n")

    prompt_content = prompt_path.read_text(encoding="utf-8")
    model_output = output_path.read_text(encoding="utf-8")

    # Detect pattern
    pattern_name = args.pattern
    if pattern_name is None:
        # Try frontmatter first
        fm = parse_frontmatter(prompt_content)
        pattern_name = detect_pattern_from_frontmatter(fm)

        if pattern_name is None:
            # Try output detection
            pattern_name = detect_pattern(model_output)

        if pattern_name is None:
            print("Error: Could not auto-detect pattern. Specify --pattern explicitly.", file=sys.stderr)
            print(f"Available patterns: {get_available_patterns()}")
            return 1

    print(f"📄 Prompt: {prompt_path.name}")
    print(f"📝 Output: {output_path.name}")
    print(f"🎯 Pattern: {pattern_name}")
    print(f"🤖 Judge Model: {args.model}")
    print(f"🔁 Runs: {args.runs}")
    print(f"🌡️  Temperature: {args.temperature}")

    # Initialize LLM client
    print(f"\n{'='*60}")
    print(f" Initializing {args.model}...")
    print(f"{'='*60}\n")

    # Create a wrapper class that implements the interface expected by PatternEvaluator
    class LLMClientWrapper:
        def __init__(self, model_name: str):
            self.model_name = model_name

        def complete(self, prompt: str, temperature: float = 0.1) -> str:
            """Call LLM and return response."""
            return LLMClient.generate_text(
                model_name=self.model_name,
                prompt=prompt,
                temperature=temperature,
            )

        def __str__(self):
            return self.model_name

    client = LLMClientWrapper(args.model)

    # Run evaluation
    print(f"\n{'='*60}")
    print(f" Running Evaluation...")
    print(f"{'='*60}\n")

    evaluator = PatternEvaluator(
        llm_client=client,
        num_runs=args.runs,
        temperature=args.temperature,
    )

    if args.runs == 1:
        result = evaluator.quick_evaluate(prompt_content, model_output, pattern_name)
    else:
        result = evaluator.evaluate(prompt_content, model_output, pattern_name)

    # Display results
    print(f"\n{'='*60}")
    print(f" RESULTS")
    print(f"{'='*60}\n")

    print(f"Pattern: {result.pattern_name}")
    print(f"Overall Score: {result.overall_score:.2f}/5.0 ({result.overall_score * 20:.1f}/100)")
    print(f"Pass Rate: {result.pass_rate:.1%}")
    print(f"Hard Gates: {'PASS ✓' if result.passes_hard_gates else 'FAIL ✗'}")

    print(f"\n📊 Dimension Scores (median across {len(result.runs)} runs):")
    for dim, median in sorted(result.dimension_medians.items()):
        stdev = result.dimension_stdevs.get(dim, 0)
        print(f"  {dim:4s}: {median:.2f}/5.0 (σ={stdev:.2f})")

    if result.failure_summary and result.failure_summary.failure_count > 0:
        print(f"\n⚠️  Failures Detected ({result.failure_summary.failure_count} total):")
        for mode in result.failure_summary.failure_modes:
            count = sum(1 for f in result.failure_summary.failures if f.mode.value == mode)
            print(f"  - {mode}: {count}x")

    print(f"\n📈 Statistical Metrics:")
    print(f"  Mean Phase Fidelity: {result.mean_phase_fidelity:.1%}")
    print(f"  Critical Failure Rate: {result.critical_failure_rate:.1%}")
    print(f"  Perfect Pass Rate: {result.perfect_pass_rate:.1%}")

    # Save JSON if requested
    if args.output_json:
        output_json_path = Path(args.output_json)
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(result.to_dict(), f, indent=2)
        print(f"\n💾 Detailed results saved to: {output_json_path}")

    print(f"\n{'='*60}\n")

    # Exit code based on hard gates
    return 0 if result.passes_hard_gates else 1


if __name__ == "__main__":
    sys.exit(main())
