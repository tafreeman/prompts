"""Update an existing run summary JSON to include per-criterion aggregated
statistics by scanning the per-run output files listed in the summary.

Usage:
  python scripts/update_summary_with_criteria.py --summary results/<run_id>/summary_<timestamp>.json

This is a convenience script for adding `criteria_stats` to an existing summary
without re-running the full evaluation matrix.
"""

import argparse
import json
import math
import statistics
from pathlib import Path


def read_jsonl_last(path: Path):
    try:
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            return None
        lines = text.splitlines()
        last = lines[-1]
        return json.loads(last)
    except Exception:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--summary", required=True)
    args = p.parse_args()

    summary_path = Path(args.summary)
    if not summary_path.exists():
        print("Summary file not found:", summary_path)
        return 2

    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    criteria_map = {}
    for e in summary.get("entries", []):
        outfile = Path(e.get("outfile"))
        if outfile.exists():
            data = read_jsonl_last(outfile)
            if (
                isinstance(data, dict)
                and "criteria" in data
                and isinstance(data["criteria"], dict)
            ):
                for ck, cv in data["criteria"].items():
                    if isinstance(cv, (int, float)):
                        criteria_map.setdefault(str(ck), []).append(float(cv))

    if criteria_map:
        crit_stats = {}
        for ck, vals in criteria_map.items():
            n = len(vals)
            mean = statistics.mean(vals)
            stdev = statistics.stdev(vals) if n > 1 else 0.0
            se = stdev / math.sqrt(n) if n > 1 else 0.0
            ci_low = mean - 1.96 * se
            ci_high = mean + 1.96 * se
            crit_stats[ck] = {
                "n": n,
                "mean": mean,
                "stdev": stdev,
                "95%_ci": [ci_low, ci_high],
            }
        summary["criteria_stats"] = crit_stats
    else:
        summary["criteria_stats"] = None

    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("Updated summary with criteria_stats:", summary_path)
    return 0


if __name__ == "__main__":
    import json
    import sys

    sys.exit(main())
