#!/usr/bin/env python3
"""
Repository Documentation Generator
Reads files from a directory and sends to LLM for documentation.
"""

import os
import sys
import argparse
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from tools.llm_client import LLMClient


def get_file_contents(directory: str, max_files: int = 20) -> str:
    """Read all relevant files from a directory."""
    dir_path = Path(directory)
    if not dir_path.exists():
        return f"Directory {directory} does not exist"
    
    contents = []
    file_count = 0
    
    for item in sorted(dir_path.rglob("*")):
        if item.is_file() and file_count < max_files:
            # Skip binary, cache, etc.
            if any(skip in str(item) for skip in ["__pycache__", ".pyc", ".git", ".png", ".jpg"]):
                continue
            
            ext = item.suffix.lower()
            if ext in [".py", ".md", ".json", ".yaml", ".yml", ".txt"]:
                try:
                    content = item.read_text(encoding="utf-8", errors="ignore")
                    # Truncate large files
                    if len(content) > 5000:
                        content = content[:5000] + "\n... [TRUNCATED]"
                    
                    rel_path = item.relative_to(dir_path.parent)
                    contents.append(f"\n{'='*60}\n## FILE: {rel_path}\n{'='*60}\n{content}")
                    file_count += 1
                except Exception as e:
                    contents.append(f"\n## FILE: {item.name} - Error reading: {e}")
    
    return f"Found {file_count} files in {directory}:\n" + "\n".join(contents)


def generate_documentation(directory: str, model: str = "gh:openai/gpt-4o", output: str = None):
    """Generate documentation for a directory."""
    
    print(f"📁 Reading files from: {directory}")
    file_contents = get_file_contents(directory)
    
    prompt = f"""Analyze the following files and create comprehensive documentation.

For each file, document:
- **Function**: What it does (2-3 sentences)
- **Parameters**: CLI args, function params, env vars
- **Outputs**: What it produces
- **Workflow Usage**: How it fits with other files
- **Value Assessment**: KEEP / CONSOLIDATE / ARCHIVE recommendation

{file_contents}

---

Now generate the documentation in Markdown format:

# {directory} Reference Documentation

## Summary
[Overview of this directory]

## Files
[Document each file using the template above]

## Recommendations
[Consolidation and improvement suggestions]
"""
    
    print(f"🤖 Sending to {model}...")
    print(f"   Prompt size: {len(prompt):,} chars")
    
    response = LLMClient.generate_text(model, prompt, temperature=0.3, max_tokens=16000)
    
    if output:
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        Path(output).write_text(response, encoding="utf-8")
        print(f"✅ Saved to: {output}")
    else:
        print("\n" + response)
    
    return response


def main():
    parser = argparse.ArgumentParser(description="Generate documentation for a directory")
    parser.add_argument("directory", help="Directory to document (e.g., tools/)")
    parser.add_argument("-m", "--model", default="gh:openai/gpt-4o", help="Model to use")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("--max-files", type=int, default=20, help="Max files to read")
    
    args = parser.parse_args()
    
    generate_documentation(args.directory, args.model, args.output)


if __name__ == "__main__":
    main()
