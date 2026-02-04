"""Command-line interface for prompttools.

Usage:
    prompttools evaluate prompts/           # Evaluate all prompts
    prompttools validate prompts/           # Validate structure only
    prompttools generate "your prompt"      # Direct LLM call

    # With options
    prompttools evaluate prompts/ --tier 2  # Use cloud model
    prompttools evaluate prompts/ --model gh:gpt-4o-mini
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional


def main(args: Optional[list] = None) -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="prompttools",
        description="Simple, effective prompt evaluation and validation",
    )
    parser.add_argument("--version", action="version", version="prompttools 1.0.0")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ==========================================================================
    # EVALUATE command
    # ==========================================================================
    eval_parser = subparsers.add_parser(
        "evaluate", aliases=["eval", "e"], help="Evaluate prompts (get scores)"
    )
    eval_parser.add_argument(
        "path", type=Path, help="Prompt file or directory to evaluate"
    )
    eval_parser.add_argument(
        "--tier",
        "-t",
        type=int,
        choices=[0, 1, 2, 3],
        default=1,
        help="Evaluation tier: 0=structural, 1=local, 2=cloud, 3=premium (default: 1)",
    )
    eval_parser.add_argument(
        "--model", "-m", type=str, help="Specific model to use (overrides tier)"
    )
    eval_parser.add_argument(
        "--threshold", type=float, default=70.0, help="Pass threshold (default: 70)"
    )
    eval_parser.add_argument(
        "--output", "-o", type=Path, help="Output file (JSON or Markdown)"
    )
    eval_parser.add_argument(
        "--quiet", "-q", action="store_true", help="Minimal output"
    )

    # ==========================================================================
    # VALIDATE command
    # ==========================================================================
    val_parser = subparsers.add_parser(
        "validate", aliases=["val", "v"], help="Validate prompt structure (no LLM)"
    )
    val_parser.add_argument(
        "path", type=Path, help="Prompt file or directory to validate"
    )
    val_parser.add_argument(
        "--strict", action="store_true", help="Treat warnings as errors"
    )

    # ==========================================================================
    # GENERATE command
    # ==========================================================================
    gen_parser = subparsers.add_parser(
        "generate", aliases=["gen", "g"], help="Generate text with an LLM"
    )
    gen_parser.add_argument("prompt", type=str, help="The prompt to send")
    gen_parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="local:phi4mini",
        help="Model to use (default: local:phi4mini)",
    )
    gen_parser.add_argument(
        "--system", "-s", type=str, default="", help="System prompt"
    )

    # ==========================================================================
    # MODELS command
    # ==========================================================================
    models_parser = subparsers.add_parser("models", help="List available models")
    models_parser.add_argument(
        "--provider",
        "-p",
        type=str,
        help="Filter by provider (local, ollama, gh, etc.)",
    )
    models_parser.add_argument(
        "--probe", action="store_true", help="Test which models are actually available"
    )

    # Parse arguments
    parsed = parser.parse_args(args)

    if not parsed.command:
        parser.print_help()
        return 0

    # Execute command
    try:
        if parsed.command in ("evaluate", "eval", "e"):
            return _cmd_evaluate(parsed)
        elif parsed.command in ("validate", "val", "v"):
            return _cmd_validate(parsed)
        elif parsed.command in ("generate", "gen", "g"):
            return _cmd_generate(parsed)
        elif parsed.command == "models":
            return _cmd_models(parsed)
        else:
            parser.print_help()
            return 1
    except KeyboardInterrupt:
        print("\nCancelled.")
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def _cmd_evaluate(args) -> int:
    """Execute the evaluate command."""
    from .evaluate import TIERS, evaluate

    verbose = not args.quiet

    if verbose:
        tier_name = TIERS.get(args.tier, {}).get("name", f"Tier {args.tier}")
        print("\n📊 PromptTools Evaluation")
        print(f"   Path: {args.path}")
        print(f"   Tier: {tier_name}")
        if args.model:
            print(f"   Model: {args.model}")
        print()

    result = evaluate(
        args.path,
        model=args.model,
        tier=args.tier,
        threshold=args.threshold,
        verbose=verbose,
    )

    # Handle single result vs batch
    if hasattr(result, "results"):  # BatchResult
        if verbose:
            print(f"\n{'='*50}")
            print(f"Results: {result.passed}/{result.total} passed")
            print(f"Average Score: {result.avg_score:.1f}")
            print(f"Duration: {result.duration:.1f}s")

        if args.output:
            _write_output(result, args.output)

        return 0 if result.passed == result.total else 1
    else:  # EvalResult
        if verbose:
            status = "✓ PASSED" if result.passed else "✗ FAILED"
            print(f"\n{status}: {result.score:.0f}/100 ({result.grade})")
            if result.improvements:
                print("\nSuggestions:")
                for imp in result.improvements[:3]:
                    print(f"  • {imp}")

        return 0 if result.passed else 1


def _cmd_validate(args) -> int:
    """Execute the validate command."""
    from .validate import print_validation_summary, validate, validate_batch

    path = args.path

    if path.is_file():
        result = validate(path)

        if result.is_valid:
            print(f"✓ {path}: Valid")
        else:
            print(
                f"✗ {path}: {result.error_count} errors, {result.warning_count} warnings"
            )
            for issue in result.issues:
                print(f"  {issue}")

        if args.strict:
            return 0 if result.is_valid and result.warning_count == 0 else 1
        return 0 if result.is_valid else 1

    else:
        results = validate_batch(path)
        print_validation_summary(results)

        has_errors = any(not r.is_valid for r in results.values())
        if args.strict:
            has_warnings = any(r.warning_count > 0 for r in results.values())
            return 1 if has_errors or has_warnings else 0
        return 1 if has_errors else 0


def _cmd_generate(args) -> int:
    """Execute the generate command."""
    from .llm import generate

    response = generate(
        model=args.model,
        prompt=args.prompt,
        system=args.system,
    )

    print(response)
    return 0


def _cmd_models(args) -> int:
    """Execute the models command."""
    from .llm import list_models, probe

    models = list_models(provider=args.provider)

    if args.probe:
        print("Probing models (this may take a moment)...\n")
        for m in models:
            available = probe(m)
            status = "✓" if available else "✗"
            print(f"  {status} {m}")
    else:
        for m in models:
            print(f"  {m}")

    print(f"\n{len(models)} models found")
    return 0


def _write_output(result, output_path: Path) -> None:
    """Write results to file."""
    if output_path.suffix == ".json":
        data = {
            "total": result.total,
            "passed": result.passed,
            "failed": result.failed,
            "avg_score": result.avg_score,
            "duration": result.duration,
            "results": [
                {
                    "file": r.file,
                    "score": r.score,
                    "grade": r.grade,
                    "passed": r.passed,
                    "criteria": r.criteria,
                }
                for r in result.results
            ],
        }
        output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    else:
        # Markdown
        lines = [
            "# Evaluation Results",
            "",
            f"- **Total**: {result.total}",
            f"- **Passed**: {result.passed}",
            f"- **Average Score**: {result.avg_score:.1f}",
            f"- **Duration**: {result.duration:.1f}s",
            "",
            "## Results",
            "",
            "| File | Score | Grade | Status |",
            "|------|-------|-------|--------|",
        ]
        for r in result.results:
            status = "✓" if r.passed else "✗"
            lines.append(
                f"| {Path(r.file).name} | {r.score:.0f} | {r.grade} | {status} |"
            )

        output_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"\nResults written to: {output_path}")


if __name__ == "__main__":
    sys.exit(main())
