#!/usr/bin/env python3
"""Prompteval Registry Integration.

Loads prompt metadata from prompts/registry.yaml instead of per-file
frontmatter.
"""

from pathlib import Path

import yaml

REGISTRY_PATH = Path("prompts/registry.yaml")


def load_registry():
    with REGISTRY_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def list_prompt_files():
    registry = load_registry()
    return [entry["path"] for entry in registry if "path" in entry]


if __name__ == "__main__":
    registry = load_registry()
    print(f"Loaded {len(registry)} prompt entries from registry.yaml")
    for entry in registry[:5]:
        print(entry["path"], "-", entry.get("title", ""))
