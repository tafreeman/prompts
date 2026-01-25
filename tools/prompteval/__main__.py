#!/usr/bin/env python3
"""`python -m tools.prompteval` entrypoint.

The VS Code tasks in this repo call `python -m tools.prompteval <path> --tier N`.
This module provides that CLI and keeps a couple of small helper functions used by tests.

Note: This CLI uses `tools.prompteval.core.evaluate` for baseline scoring.
Pattern scoring is available via `tools.prompteval.integration`.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from tools.prompteval.core import TIERS, evaluate


def _print_tiers() -> None:
    print("\nAvailable tiers (tools.prompteval):")
    for tier_num in sorted(TIERS.keys()):
        cfg = TIERS.get(tier_num, {})
        name = str(cfg.get("name", f"Tier {tier_num}"))
        model = cfg.get("model")
        method = cfg.get("method")
        model_txt = str(model) if model is not None else "(none)"
        print(f"  {tier_num}: {name} | model={model_txt} | method={method}")


def _print_models_from_discovery() -> int:
    """Print available models from discovery_results.json if present.

    Returns:
        0 if printed successfully, else 1.
    """
    try:
        discovery_path = Path("discovery_results.json")
        if not discovery_path.exists():
            print(
                "discovery_results.json not found. Run: "
                "python -m tools.llm.model_probe --discover --force -o discovery_results.json"
            )
            return 1

        data = json.loads(discovery_path.read_text(encoding="utf-8"))
        providers = (data or {}).get("providers", {})
        print("\nDiscovered available models:")
        for provider_name, payload in providers.items():
            available = payload.get("available") if isinstance(payload, dict) else None
            if not available:
                continue
            print(f"\n[{provider_name}]")
            for m in available:
                print(f"  {m}")
        return 0
    except Exception as e:
        print(f"Error reading discovery_results.json: {e}")
        return 1


def _normalize_score_to_pct(score: float | int | None) -> float:
    """Normalize common judge score formats to 0..100.

    Supports:
    - 0..1 fractions (e.g., 0.5 => 50)
    - 1..10 rubric scores (e.g., 10 => 100, 1 => 0)
    - already-normalized percents (e.g., 75 => 75)

    Any negative values clamp to 0; values >100 clamp to 100.
    """
    if score is None:
        return 0.0

    try:
        s = float(score)
    except (TypeError, ValueError):
        return 0.0

    if s <= 0:
        return 0.0

    # Rubric 1..10 (check this FIRST - 1=worst=0%, 10=best=100%)
    if 1 <= s <= 10:
        return max(0.0, min(100.0, (s - 1.0) / 9.0 * 100.0))

    # Fraction (0 < s < 1)
    if s < 1:
        return max(0.0, min(100.0, s * 100.0))

    # Percent-ish (already 0-100 scale or beyond)
    return max(0.0, min(100.0, s))


def _to_jsonable(obj: Any) -> Any:
    if is_dataclass(obj):
        return asdict(obj)
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, dict):
        return {k: _to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_jsonable(v) for v in obj]
    return obj


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Prompt evaluation (tiered)")
    parser.add_argument("path", nargs="?", help="Prompt file or folder to evaluate")
    parser.add_argument("--tier", type=int, default=2, help="Evaluation tier (0-3)")
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Override tier default model (e.g., local:phi4-gpu, ollama:gpt-oss:20b, aitk:phi-4-mini-reasoning)",
    )
    parser.add_argument("--list-tiers", action="store_true", help="List available tiers and exit")
    parser.add_argument("--list-models", action="store_true", help="List discovered available models and exit")
    parser.add_argument("--verbose", action="store_true", help="Print progress")
    parser.add_argument("--ci", action="store_true", help="CI-friendly output")
    parser.add_argument(
        "--include-all",
        action="store_true",
        help="Include all .md files in a folder (do not exclude README/index/agent/instructions)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Write JSON results to this file",
    )
    args = parser.parse_args(argv)

    # Listing / discovery helpers (do not require a path).
    if args.list_tiers:
        _print_tiers()
        return 0
    if args.list_models:
        return _print_models_from_discovery()

    if not args.path:
        parser.error("path is required unless --list-tiers or --list-models is provided")

    result = evaluate(
        args.path,
        tier=args.tier,
        model=args.model,
        verbose=args.verbose,
        include_all=bool(args.include_all),
    )
    payload = _to_jsonable(result)

    if args.output:
        Path(args.output).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    else:
        print(json.dumps(payload, indent=2))

    # Exit non-zero if any failures when evaluating a batch.
    try:
        failed = getattr(result, "failed", 0)
        errors = getattr(result, "errors", 0)
        return 1 if (failed or errors) else 0
    except Exception:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
