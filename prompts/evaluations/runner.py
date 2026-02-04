"""Simple evaluation runner POC.

Usage:
    python -m prompts.evaluations.runner path/to/examples/sentiment_eval.yaml --limit 10

This is a minimal, dependency-light runner intended as a proof-of-concept
for the repo migration plan. It reads a small YAML describing test cases and
writes a JSON results file.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


def run_eval(
    yaml_path: str | Path, limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    yaml_path = Path(yaml_path)
    with yaml_path.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    items = cfg.get("items", []) or []
    if limit:
        items = items[:limit]

    results: List[Dict[str, Any]] = []
    for idx, item in enumerate(items, start=1):
        # Minimal POC: echo input and gold label; real runner would call model backends
        prompt = item.get("prompt") if isinstance(item, dict) else str(item)
        gold = item.get("label") if isinstance(item, dict) else None
        simulated_pred = (
            "positive"
            if "good" in prompt.lower() or "positive" in str(gold).lower()
            else "negative"
        )

        result = {
            "id": item.get("id", idx) if isinstance(item, dict) else idx,
            "prompt": prompt,
            "gold": gold,
            "predicted": simulated_pred,
        }
        print(json.dumps(result, ensure_ascii=False))
        results.append(result)

    out_path = cfg.get("output", "eval_results.json")
    out_path = Path(out_path)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(results)} results to {out_path}")
    return results


def _main() -> None:
    p = argparse.ArgumentParser(description="Run a small evaluation YAML (POC)")
    p.add_argument("yaml", help="Path to evaluation YAML")
    p.add_argument("--limit", type=int, default=None, help="Limit number of test cases")
    args = p.parse_args()

    run_eval(args.yaml, args.limit)


if __name__ == "__main__":
    _main()
