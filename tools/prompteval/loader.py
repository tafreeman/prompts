# prompteval/loader.py
# Registry-based prompt loader for prompteval
from pathlib import Path

import yaml

REGISTRY_PATH = Path("prompts/registry.yaml")


class PromptRegistry:
    def __init__(self, registry_path=REGISTRY_PATH):
        with registry_path.open("r", encoding="utf-8") as f:
            self.entries = yaml.safe_load(f)

    def list_prompt_paths(self):
        return [entry["path"] for entry in self.entries if "path" in entry]

    def get_metadata(self, path):
        for entry in self.entries:
            if entry.get("path") == path:
                return entry
        return None


# Example usage:
if __name__ == "__main__":
    reg = PromptRegistry()
    print(f"Loaded {len(reg.entries)} prompts from registry.yaml")
    for p in reg.list_prompt_paths()[:5]:
        print(p, reg.get_metadata(p).get("title"))
