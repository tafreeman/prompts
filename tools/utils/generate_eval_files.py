#!/usr/bin/env python3
"""Generate gh-models eval files from prompt library markdown files.

This script reads prompts from the library and creates .prompt.yml files
compatible with `gh models eval` for automated evaluation.

Usage:
    python generate_eval_files.py prompts/developers
    python generate_eval_files.py prompts/developers --output testing/evals
    python generate_eval_files.py prompts/developers --limit 5
"""

import argparse
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """Extract YAML frontmatter and body from markdown content."""
    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)

    if frontmatter_match:
        try:
            metadata = yaml.safe_load(frontmatter_match.group(1)) or {}
        except yaml.YAMLError:
            metadata = {}
        body = frontmatter_match.group(2)
    else:
        metadata = {}
        body = content

    return metadata, body


def extract_prompt_content(body: str) -> str:
    """Extract the main prompt content from the markdown body."""
    # Look for a code block after "## Prompt" section
    prompt_section = re.search(
        r"##\s*Prompt\s*\n+```(?:text|markdown)?\s*\n(.*?)```",
        body,
        re.DOTALL | re.IGNORECASE,
    )

    if prompt_section:
        return prompt_section.group(1).strip()

    # Fallback: look for any substantial code block
    code_blocks = re.findall(r"```(?:text|markdown)?\s*\n(.*?)```", body, re.DOTALL)
    if code_blocks:
        # Return the longest code block (likely the main prompt)
        return max(code_blocks, key=len).strip()

    # Last resort: use the body after removing code blocks
    cleaned = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    return cleaned.strip()[:2000]  # Limit length


def load_prompt_file(file_path: Path) -> Optional[Dict[str, Any]]:
    """Load and parse a single prompt file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        metadata, body = parse_frontmatter(content)
        prompt_content = extract_prompt_content(body)

        if not prompt_content or len(prompt_content) < 50:
            print(f"  Skipping {file_path.name}: No substantial prompt content found")
            return None

        return {
            "file_path": str(file_path),
            "file_name": file_path.stem,
            "metadata": metadata,
            "prompt_content": prompt_content,
        }
    except Exception as e:
        print(f"  Error loading {file_path}: {e}")
        return None


def discover_prompts(
    directory: str, limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Discover and load prompt files from a directory."""
    root = Path(directory)
    exclude_names = {"index", "readme", "agents_guide"}

    prompts = []
    for file_path in sorted(root.glob("**/*.md")):
        if file_path.stem.lower() in exclude_names:
            continue

        prompt_data = load_prompt_file(file_path)
        if prompt_data:
            prompts.append(prompt_data)

        if limit and len(prompts) >= limit:
            break

    return prompts


def generate_eval_file(
    prompts: List[Dict[str, Any]],
    output_path: Path,
    model: str = "openai/gpt-4o-mini",
    name: str = "Prompt Library Evaluation",
) -> str:
    """Generate a gh-models eval YAML file."""

    # Build test data from prompts
    test_data = []
    for p in prompts:
        meta = p["metadata"]
        test_case = {
            "promptTitle": meta.get("title", p["file_name"]),
            "promptContent": p["prompt_content"],
            "difficulty": meta.get("difficulty", "intermediate"),
            "type": meta.get("type", "how_to"),
            "category": str(Path(p["file_path"]).parent.name),
        }
        test_data.append(test_case)

    eval_config = {
        "name": name,
        "description": f"Automated evaluation of {len(prompts)} prompts from the library",
        "model": model,
        "modelParameters": {"temperature": 0.3, "max_tokens": 2000},
        "testData": test_data,
        "messages": [
            {
                "role": "system",
                "content": """You are an expert prompt engineer evaluating AI prompts for quality and effectiveness.

## Evaluation Process (Chain-of-Thought)
First, carefully analyze the prompt step-by-step:
1. Read the entire prompt to understand its intent
2. Identify the target audience and use case
3. Assess each criterion individually with specific evidence
4. Consider industry best practices (OpenAI, Anthropic, Google)
5. Formulate actionable improvements

## Evaluation Criteria (score 1-10 each):

### Core Quality
1. **Clarity** - How clear and unambiguous are the instructions?
2. **Specificity** - Does it provide enough detail for consistent outputs?
3. **Actionability** - Can the AI clearly determine what actions to take?
4. **Structure** - Is it well-organized with clear sections?
5. **Completeness** - Does it cover all necessary aspects?

### Advanced Quality (Industry Best Practices)
6. **Factuality** - Are any claims/examples accurate? No misleading information?
7. **Consistency** - Will it produce reproducible, reliable outputs?
8. **Safety** - Does it avoid harmful patterns, biases, or jailbreak vulnerabilities?

## Grading Scale
- A (8.5-10): Excellent - production ready
- B (7.0-8.4): Good - minor improvements possible  
- C (5.5-6.9): Average - several areas need work
- D (4.0-5.4): Below Average - significant rework needed
- F (<4.0): Fails - major issues, not usable

## Pass/Fail Thresholds
- PASS: Overall score >= 7.0 AND no individual criterion < 5.0
- FAIL: Overall score < 7.0 OR any criterion < 5.0

Respond with JSON in this exact format:
{
  "reasoning": "<2-3 sentences explaining your chain-of-thought analysis>",
  "scores": {
    "clarity": <1-10>,
    "specificity": <1-10>,
    "actionability": <1-10>,
    "structure": <1-10>,
    "completeness": <1-10>,
    "factuality": <1-10>,
    "consistency": <1-10>,
    "safety": <1-10>
  },
  "overall_score": <weighted average>,
  "grade": "<A/B/C/D/F>",
  "pass": <true/false>,
  "strengths": ["<strength1>", "<strength2>"],
  "improvements": ["<improvement1>", "<improvement2>"],
  "summary": "<brief 1-2 sentence summary>"
}""",
            },
            {
                "role": "user",
                "content": """Evaluate this prompt from our library:

**Title:** {{promptTitle}}
**Category:** {{category}}
**Difficulty:** {{difficulty}}
**Type:** {{type}}

**Prompt Content:**
```
{{promptContent}}
```

Provide your evaluation as JSON.""",
            },
        ],
        "evaluators": [
            {
                "name": "valid-json",
                "description": "Response must be valid JSON with scores",
                "string": {"contains": '"scores"'},
            },
            {
                "name": "has-overall-score",
                "description": "Response includes overall score",
                "string": {"contains": '"overall_score"'},
            },
            {
                "name": "has-grade",
                "description": "Response includes letter grade",
                "string": {"contains": '"grade"'},
            },
            {
                "name": "has-pass-fail",
                "description": "Response includes pass/fail determination",
                "string": {"contains": '"pass"'},
            },
            {
                "name": "has-reasoning",
                "description": "Response includes chain-of-thought reasoning",
                "string": {"contains": '"reasoning"'},
            },
            {
                "name": "has-safety-score",
                "description": "Response includes safety evaluation",
                "string": {"contains": '"safety"'},
            },
            {
                "name": "has-summary",
                "description": "Response includes summary",
                "string": {"contains": '"summary"'},
            },
        ],
    }

    # Write YAML file
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        # Add header comment
        f.write("# Auto-generated evaluation file\n")
        f.write(f"# Generated from: {len(prompts)} prompts\n")
        f.write(f"# Run with: gh models eval {output_path}\n\n")
        yaml.dump(
            eval_config,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )

    return str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Generate gh-models eval files from prompt library"
    )
    parser.add_argument("directory", help="Directory containing prompt markdown files")
    parser.add_argument(
        "--output",
        "-o",
        default="testing/evals",
        help="Output directory for eval files (default: testing/evals)",
    )
    parser.add_argument(
        "--model",
        "-m",
        default="openai/gpt-4o-mini",
        help="Model to use for evaluation (default: openai/gpt-4o-mini)",
    )
    parser.add_argument(
        "--limit", "-l", type=int, help="Limit number of prompts to include"
    )
    parser.add_argument(
        "--batch-size",
        "-b",
        type=int,
        default=10,
        help="Max prompts per eval file (default: 10)",
    )

    args = parser.parse_args()

    print(f"Discovering prompts in: {args.directory}")
    prompts = discover_prompts(args.directory, args.limit)
    print(f"Found {len(prompts)} prompts")

    if not prompts:
        print("No prompts found!")
        return

    # Generate eval files (split into batches if needed)
    output_dir = Path(args.output)
    category = Path(args.directory).name

    if len(prompts) <= args.batch_size:
        # Single file
        output_path = output_dir / f"{category}-eval.prompt.yml"
        result = generate_eval_file(
            prompts,
            output_path,
            model=args.model,
            name=f"{category.title()} Prompts Evaluation",
        )
        print(f"Generated: {result}")
    else:
        # Multiple files
        for i in range(0, len(prompts), args.batch_size):
            batch = prompts[i : i + args.batch_size]
            batch_num = i // args.batch_size + 1
            output_path = output_dir / f"{category}-eval-{batch_num}.prompt.yml"
            result = generate_eval_file(
                batch,
                output_path,
                model=args.model,
                name=f"{category.title()} Prompts Evaluation (Batch {batch_num})",
            )
            print(f"Generated: {result}")

    print("\nRun evaluations with:")
    print(f"  gh models eval {output_dir}/{category}-eval*.prompt.yml")
    print(
        f"  gh models eval {output_dir}/{category}-eval*.prompt.yml --json > results.json"
    )


if __name__ == "__main__":
    main()
