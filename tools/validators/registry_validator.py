#!/usr/bin/env python3
"""
Registry Validator Script

Validates prompts/registry.yaml against .github/registry-schema.json.
"""

import json
import sys
from pathlib import Path
import yaml
import jsonschema

REGISTRY_PATH = Path('prompts/registry.yaml')
SCHEMA_PATH = Path('.github/registry-schema.json')


def main():
    try:
        with REGISTRY_PATH.open('r', encoding='utf-8') as f:
            registry = yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading registry.yaml: {e}")
        sys.exit(1)

    try:
        with SCHEMA_PATH.open('r', encoding='utf-8') as f:
            schema = json.load(f)
    except Exception as e:
        print(f"Error reading registry-schema.json: {e}")
        sys.exit(1)

    try:
        jsonschema.validate(instance=registry, schema=schema)
        print("✓ registry.yaml is valid against registry-schema.json")
    except jsonschema.ValidationError as e:
        print(f"✗ registry.yaml validation error:\n{e.message}")
        sys.exit(2)

if __name__ == "__main__":
    main()
