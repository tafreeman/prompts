"""
Merge per-run JSONL/JSON outputs into a single CSV using the summary JSON.

Usage:
  python scripts/merge_results_csv.py --summary results/<run_id>/summary_<timestamp>.json

Output:
  results/<run_id>/merged_scores_<timestamp>.csv
"""
from pathlib import Path
import json
import csv
import argparse
import sys


def read_jsonl_last(path: Path):
    try:
        text = path.read_text(encoding='utf-8').strip()
        if not text:
            return None
        lines = text.splitlines()
        # try last line
        last = lines[-1]
        return json.loads(last)
    except Exception:
        try:
            return json.loads(path.read_text(encoding='utf-8'))
        except Exception:
            return None


def extract_score(data):
    if not data:
        return None
    for key in ("score", "weighted_score", "weightedScore", "grade_score"):
        if key in data and isinstance(data[key], (int, float)):
            return float(data[key])
    # possible nested
    if isinstance(data, dict):
        for v in data.values():
            if isinstance(v, (int, float)):
                return float(v)
    return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--summary', required=True)
    args = p.parse_args()

    summary_path = Path(args.summary)
    if not summary_path.exists():
        print('Summary file not found:', summary_path, file=sys.stderr)
        return 2

    summary = json.loads(summary_path.read_text(encoding='utf-8'))
    run_dir = summary_path.parent
    timestamp = summary.get('timestamp')
    out_csv = run_dir / f"merged_scores_{timestamp}.csv"

    # We'll collect per-entry data first so we can discover any criteria keys
    rows = []
    criteria_keys = set()
    entry_datas = []
    for e in summary.get('entries', []):
        outfile = Path(e.get('outfile'))
        data = None
        if outfile.exists():
            data = read_jsonl_last(outfile)
        # record criteria keys if present
        if isinstance(data, dict) and 'criteria' in data and isinstance(data['criteria'], dict):
            for k in data['criteria'].keys():
                criteria_keys.add(k)
        entry_datas.append((e, data))

    # Build header with discovered criteria keys (sorted for consistency)
    crit_cols = [f"criteria.{k}" for k in sorted(criteria_keys)]
    header = [
        'run_id','timestamp','prompt','model','seed','outfile','returncode','arg_method',
        'score',
    ] + crit_cols + ['raw_stdout']

    # Now construct rows including per-criteria values
    for e, data in entry_datas:
        score = extract_score(data)
        criteria = data.get('criteria', {}) if isinstance(data, dict) else {}
        row = {
            'run_id': summary.get('run_id'),
            'timestamp': summary.get('timestamp'),
            'prompt': summary.get('prompt'),
            'model': e.get('model'),
            'seed': e.get('seed'),
            'outfile': e.get('outfile'),
            'returncode': e.get('returncode'),
            'arg_method': e.get('arg_method'),
            'score': score,
            'raw_stdout': (e.get('stdout') or '').splitlines()[0] if e.get('stdout') else ''
        }
        # insert criteria columns (None when missing)
        for k in sorted(criteria_keys):
            row[f"criteria.{k}"] = criteria.get(k)
        rows.append(row)

    with out_csv.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print('Wrote merged CSV to', out_csv)
    return 0


if __name__ == '__main__':
    sys.exit(main())
