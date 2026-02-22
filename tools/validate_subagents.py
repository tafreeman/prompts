#!/usr/bin/env python3
"""
Minimal validator for docs/subagents.yml
Checks that each subagent definition contains required fields and basic typing.

Usage:
  python tools/validate_subagents.py docs/subagents.yml

Exit codes:
  0 - success
  2 - validation errors
"""
import sys
import argparse
from pathlib import Path

try:
    import yaml
except Exception as e:
    print("Missing dependency 'PyYAML'. Install with: pip install pyyaml", file=sys.stderr)
    raise

REQUIRED_FIELDS = [
    "task_name",
    "description",
    "output_path",
    "acceptance_criteria",
    "sample_prompt",
    "input_schema",
    "output_schema",
]


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    p = argparse.ArgumentParser(description="Validate docs/subagents.yml structure")
    p.add_argument("file", nargs="?", default="docs/subagents.yml", help="Path to subagents YAML file")
    args = p.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(2)

    data = load_yaml(path)
    # Support both list-of-items or {subagents: [...]} formats
    if isinstance(data, dict) and "subagents" in data and isinstance(data["subagents"], list):
        items = data["subagents"]
    elif isinstance(data, list):
        items = data
    else:
        print("ERROR: Unexpected YAML top-level structure. Expect list or {subagents: [...]}",
              file=sys.stderr)
        sys.exit(2)

    errors = []
    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"Entry #{idx} is not a mapping/dict")
            continue
        for field in REQUIRED_FIELDS:
            if field not in item:
                errors.append(f"Entry #{idx} missing required field: {field}")
        # Basic type checks (optional)
        if "sample_prompt" in item and not isinstance(item["sample_prompt"], (str,)):
            errors.append(f"Entry #{idx} sample_prompt should be a string")
        if "input_schema" in item and not isinstance(item["input_schema"], (dict,)):
            errors.append(f"Entry #{idx} input_schema should be a mapping/object")
        if "output_schema" in item and not isinstance(item["output_schema"], (dict,)):
            errors.append(f"Entry #{idx} output_schema should be a mapping/object")

    if errors:
        print("Validation failed:")
        for e in errors:
            print(" - ", e)
        sys.exit(2)

    print(f"OK: validated {len(items)} subagent entr{'y' if len(items)==1 else 'ies'} in {path}")
    sys.exit(0)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Minimal validator for docs/subagents.yml
Checks that each subagent definition contains required fields and basic typing.

Usage:
  python tools/validate_subagents.py docs/subagents.yml

Exit codes:
  0 - success
  2 - validation errors
"""
import sys
import argparse
from pathlib import Path

try:
    import yaml
except Exception as e:
    print("Missing dependency 'PyYAML'. Install with: pip install pyyaml", file=sys.stderr)
    raise

REQUIRED_FIELDS = [
    "task_name",
    "description",
    "output_path",
    "acceptance_criteria",
    "sample_prompt",
    "input_schema",
    "output_schema",
]


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    p = argparse.ArgumentParser(description="Validate docs/subagents.yml structure")
    p.add_argument("file", nargs="?", default="docs/subagents.yml", help="Path to subagents YAML file")
    args = p.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(2)

    data = load_yaml(path)
    # Support both list-of-items or {subagents: [...]} formats
    if isinstance(data, dict) and "subagents" in data and isinstance(data["subagents"], list):
        items = data["subagents"]
    elif isinstance(data, list):
        items = data
    else:
        print("ERROR: Unexpected YAML top-level structure. Expect list or {subagents: [...]}", file=sys.stderr)
        sys.exit(2)

    errors = []
    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"Entry #{idx} is not a mapping/dict")
            continue
        for field in REQUIRED_FIELDS:
            if field not in item:
                errors.append(f"Entry #{idx} missing required field: {field}")
        # Basic type checks (optional)
        if "sample_prompt" in item and not isinstance(item["sample_prompt"], (str,)):
            errors.append(f"Entry #{idx} sample_prompt should be a string")
        if "input_schema" in item and not isinstance(item["input_schema"], (dict,)):
            errors.append(f"Entry #{idx} input_schema should be a mapping/object")
        if "output_schema" in item and not isinstance(item["output_schema"], (dict,)):
            errors.append(f"Entry #{idx} output_schema should be a mapping/object")

    if errors:
        print("Validation failed:")
        for e in errors:
            print(" - ", e)
        sys.exit(2)

    print(f"OK: validated {len(items)} subagent entr{'y' if len(items)==1 else 'ies'} in {path}")
    sys.exit(0)


if __name__ == "__main__":
    main()
