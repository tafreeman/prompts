#!/usr/bin/env python3
"""Prompt File Metadata Checker (Registry Mode)

Checks that every prompt file in prompts/ has a corresponding entry in
prompts/registry.yaml, and that all registry entries point to an
existing file.
"""

import sys
from pathlib import Path

import yaml

REGISTRY_PATH = Path("prompts/registry.yaml")
PROMPTS_DIR = Path("prompts")


def main():
    try:
        with REGISTRY_PATH.open("r", encoding="utf-8") as f:
            registry = yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading registry.yaml: {e}")
        sys.exit(1)

    # Build set of all .md files (excluding index.md, README.md)
    prompt_files = set(
        str(p.relative_to(PROMPTS_DIR)).replace("\\", "/")
        for p in PROMPTS_DIR.rglob("*.md")
        if p.name not in ("index.md", "README.md")
    )

    # Build set of all registry paths
    registry_paths = set()
    for entry in registry:
        path = entry.get("path")
        if not path:
            print(f"✗ Registry entry missing 'path': {entry.get('name', '[no name]')}")
            continue
        registry_paths.add(path)
        # Check file exists
        if not (PROMPTS_DIR / path).exists():
            print(f"✗ Registry path does not exist: {path}")

    # Check every file is in registry
    missing = prompt_files - registry_paths
    if missing:
        print("✗ Files missing from registry.yaml:")
        for m in sorted(missing):
            print(f"  - {m}")
    else:
        print("✓ All prompt files are listed in registry.yaml")

    # Check every registry entry points to a file
    extra = registry_paths - prompt_files
    if extra:
        print("✗ Registry entries with missing files:")
        for e in sorted(extra):
            print(f"  - {e}")
    else:
        print("✓ All registry entries point to existing files")


if __name__ == "__main__":
    main()
