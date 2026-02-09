#!/usr/bin/env python3
"""Compatibility wrapper for prompt validation.

VS Code tasks and docs reference `tools/validate_prompts.py`. The
implementation lives in `tools/scripts/validate_prompts.py`.
"""

from tools.scripts.validate_prompts import main

if __name__ == "__main__":
    raise SystemExit(main())
