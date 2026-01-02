"""
Execute advanced technique research prompt against the prompts folder.
Analyzes tool maturity, validation approaches, and best practices.
"""
import sys
from pathlib import Path
import os

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent / "tools"))

from llm_client import LLMClient

def collect_prompts_summary(prompts_dir: Path) -> str:
    """Collect a summary of all prompts in the folder for analysis."""
    summary_lines = ["# Prompts Folder Analysis\n\n"]
    
    for subdir in sorted(prompts_dir.iterdir()):
        if subdir.is_dir():
            summary_lines.append(f"## {subdir.name}/\n")
            prompt_files = list(subdir.glob("*.md"))
            summary_lines.append(f"Contains {len(prompt_files)} prompt files:\n")
            for pf in sorted(prompt_files)[:10]:  # Limit to first 10 per folder
                summary_lines.append(f"- {pf.name}\n")
            if len(prompt_files) > 10:
                summary_lines.append(f"- ... and {len(prompt_files) - 10} more\n")
            summary_lines.append("\n")
        elif subdir.suffix == ".md":
            summary_lines.append(f"- {subdir.name}\n")
    
    return "".join(summary_lines)

def main():
    # Paths
    prompts_dir = Path(__file__).parent / "prompts"
    research_prompt_path = Path(__file__).parent / "tools" / "advanced-technique-research-tools-PromptOnly.md"
    
    # Read the research prompt
    with open(research_prompt_path, "r", encoding="utf-8") as f:
        research_prompt = f.read()
    
    # Collect prompts folder summary
    prompts_summary = collect_prompts_summary(prompts_dir)
    
    # Combine: research prompt + context about the prompts folder
    full_prompt = f"""{research_prompt}

---

## Context: Repository Prompts Folder

The following is a summary of the prompts folder structure to analyze:

{prompts_summary}

Please analyze this prompt library using the research framework above. Focus on:
1. Tool maturity and benchmarking approaches
2. Validation and assessment techniques
3. Scoring methodologies
4. Recommendations for improvement
"""

    print("=" * 60)
    print("EXECUTING RESEARCH ANALYSIS ON PROMPTS FOLDER")
    print("=" * 60)
    print(f"Research prompt: {research_prompt_path.name}")
    print(f"Target folder: {prompts_dir}")
    print(f"Model: gh:gpt-4o-mini (GitHub Models - FREE)")
    print("=" * 60)
    print()
    
    # Execute using GitHub Models
    result = LLMClient.generate_text(
        model_name="gh:gpt-4o-mini",
        prompt=full_prompt,
        temperature=0.7,
        max_tokens=4096
    )
    
    print(result)
    
    # Save results
    output_path = Path(__file__).parent / "research_analysis_output.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Research Analysis Output\n\n")
        f.write(f"**Generated:** {__import__('datetime').datetime.now().isoformat()}\n\n")
        f.write(f"**Model:** gh:gpt-4o-mini\n\n")
        f.write("---\n\n")
        f.write(result)
    
    print("\n" + "=" * 60)
    print(f"Results saved to: {output_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
