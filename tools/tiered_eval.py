#!/usr/bin/env python3
"""Backward-compatible shim for the old `tiered_eval.py` CLI.

This repo consolidated evaluation tooling into `prompteval`.

Why this file exists:
  - Existing VS Code tasks and docs may still call `python tools/tiered_eval.py ...`.
  - Keeping this shim avoids breaking end-user workflows.

Behavior:
  - Forwards all CLI args to `python -m prompteval`.
"""

from __future__ import annotations

import runpy
import sys


def main() -> int:
    # Preserve argv semantics; `prompteval` will parse flags like --tier, --list-tiers, etc.
    sys.argv[0] = "prompteval"
    runpy.run_module("prompteval", run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
