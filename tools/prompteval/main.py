#!/usr/bin/env python3
"""Prompteval main entry (registry-based)

This script demonstrates loading prompt files and metadata from
registry.yaml.
"""

from tools.prompteval.loader import PromptRegistry

if __name__ == "__main__":
    reg = PromptRegistry()
    print(f"Loaded {len(reg.entries)} prompts from registry.yaml")
    for path in reg.list_prompt_paths():
        meta = reg.get_metadata(path)
        print(
            f"{path}: {meta.get('title')} | Platforms: {meta.get('platforms')} | Audience: {meta.get('audience')}"
        )
        # Here you would load and evaluate the prompt file as needed
        # with Path('prompts/' + path).open('r', encoding='utf-8') as f:
        #     prompt_content = f.read()
        #     ...
