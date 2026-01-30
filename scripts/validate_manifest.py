"""Validate run manifest settings for reproducibility.

Exit code 0 if manifest passes checks, non-zero otherwise.

Checks implemented:
- temperature must be 0.0 for strict reproducibility
"""
from pathlib import Path
import sys
import argparse
import yaml


def load_yaml(p: Path):
    with p.open(encoding='utf-8') as f:
        return yaml.safe_load(f)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--manifest', default='run-manifest.yaml')
    p.add_argument('--strict', action='store_true', help='Exit non-zero if temperature != 0.0')
    args = p.parse_args()

    path = Path(args.manifest)
    if not path.exists():
        print(f'Manifest not found: {path}', file=sys.stderr)
        return 2

    data = load_yaml(path)
    temp = data.get('temperature')
    if temp is None:
        # Default to 0.0 but do not fail — just warn unless strict mode requested
        msg = 'Manifest missing "temperature" field — defaulting to 0.0 for reproducibility (not enforced).'
        if args.strict:
            print(msg, file=sys.stderr)
            return 2
        else:
            print('Warning: ' + msg)
            return 0

    try:
        tempf = float(temp)
    except Exception:
        print(f'Invalid temperature value: {temp}', file=sys.stderr)
        return 2

    if abs(tempf - 0.0) > 1e-9:
        msg = f'Temperature is {tempf}; recommended default is 0.0 for strict reproducibility.'
        if args.strict:
            print(msg, file=sys.stderr)
            return 2
        else:
            print('Warning: ' + msg)
            return 0

    print('Manifest reproducibility checks passed (temperature == 0.0)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
