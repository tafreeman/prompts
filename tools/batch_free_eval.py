#!/usr/bin/env python3
"""
Batch Smart Model Evaluator
===========================

Runs prompt evaluations with intelligent model selection:
- Simple prompts: Free/mini models only
- Complex prompts: Escalate to premium models for better accuracy

Complexity detection based on:
- Length, nested structures, multi-step reasoning requirements
- Domain-specific terminology, code blocks, etc.

Usage:
    python tools/batch_free_eval.py testing/evals/advanced
    python tools/batch_free_eval.py testing/evals/advanced --output results.json
    python tools/batch_free_eval.py testing/evals/advanced --allow-premium
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple

# Model tiers by capability and cost
MODEL_TIERS = {
    "free": [
        "openai/gpt-4o-mini",
        "openai/gpt-4.1-nano",
        "openai/gpt-5-nano",
        "mistral-ai/ministral-3b",
        "meta/meta-llama-3.1-8b-instruct",
        "microsoft/phi-4-mini-instruct",
    ],
    "standard": [
        "openai/gpt-4.1-mini",
        "openai/gpt-5-mini",
        "mistral-ai/mistral-small-2503",
        "microsoft/phi-4",
        "deepseek/deepseek-v3-0324",
    ],
    "premium": [
        "openai/gpt-4o",
        "openai/gpt-4.1",
        "openai/gpt-5",
        "openai/o3-mini",
        "openai/o4-mini",
        "meta/llama-3.3-70b-instruct",
        "deepseek/deepseek-r1",
        "xai/grok-3",
    ],
    "reasoning": [
        "openai/o1",
        "openai/o3",
        "microsoft/phi-4-reasoning",
        "microsoft/mai-ds-r1",
        "deepseek/deepseek-r1-0528",
    ],
}

# Complexity indicators
COMPLEXITY_PATTERNS = {
    "high": [
        r"multi-?step",
        r"chain.?of.?thought",
        r"reasoning",
        r"tree.?of.?thoughts",
        r"reflection",
        r"self.?critique",
        r"recursive",
        r"nested",
        r"{{.*{{",  # Nested variables
        r"```[\s\S]*```[\s\S]*```",  # Multiple code blocks
    ],
    "medium": [
        r"analyze",
        r"evaluate",
        r"compare",
        r"synthesize",
        r"```",  # Code block
        r"{{.*}}",  # Variables
        r"\|.*\|.*\|",  # Tables
    ],
}


def assess_complexity(content: str) -> Tuple[str, float, List[str]]:
    """
    Assess prompt complexity and return tier recommendation.
    
    Returns:
        Tuple of (tier, score, reasons)
    """
    score = 0.0
    reasons = []
    
    # Length-based scoring
    length = len(content)
    if length > 5000:
        score += 3
        reasons.append(f"Long prompt ({length} chars)")
    elif length > 2000:
        score += 1.5
        reasons.append(f"Medium-length prompt ({length} chars)")
    
    # Pattern-based scoring
    for pattern in COMPLEXITY_PATTERNS["high"]:
        if re.search(pattern, content, re.IGNORECASE):
            score += 2
            reasons.append(f"High-complexity pattern: {pattern[:30]}")
    
    for pattern in COMPLEXITY_PATTERNS["medium"]:
        if re.search(pattern, content, re.IGNORECASE):
            score += 1
            reasons.append(f"Medium-complexity pattern: {pattern[:30]}")
    
    # Structure indicators
    sections = len(re.findall(r'^#+\s', content, re.MULTILINE))
    if sections > 5:
        score += 1.5
        reasons.append(f"Multiple sections ({sections})")
    
    # Code blocks
    code_blocks = len(re.findall(r'```', content))
    if code_blocks > 4:
        score += 1
        reasons.append(f"Multiple code blocks ({code_blocks // 2})")
    
    # Determine tier
    if score >= 6:
        tier = "reasoning"
    elif score >= 4:
        tier = "premium"
    elif score >= 2:
        tier = "standard"
    else:
        tier = "free"
    
    return tier, score, reasons


def select_models_for_prompt(content: str, allow_premium: bool = False) -> List[str]:
    """Select appropriate models based on prompt complexity."""
    tier, score, reasons = assess_complexity(content)
    
    # Always include free models
    models = MODEL_TIERS["free"][:3]  # Top 3 free models
    
    if allow_premium:
        if tier == "reasoning":
            models.extend(MODEL_TIERS["reasoning"][:2])
            models.extend(MODEL_TIERS["premium"][:1])
        elif tier == "premium":
            models.extend(MODEL_TIERS["premium"][:2])
            models.extend(MODEL_TIERS["standard"][:1])
        elif tier == "standard":
            models.extend(MODEL_TIERS["standard"][:2])
    else:
        # Only free/standard when premium not allowed
        if tier in ("premium", "reasoning"):
            models.extend(MODEL_TIERS["standard"][:2])
        elif tier == "standard":
            models.extend(MODEL_TIERS["standard"][:1])
    
    return list(dict.fromkeys(models))  # Remove duplicates, preserve order

def run_gh_model_eval(eval_file: str, model: str) -> Dict[str, Any]:
    """Run evaluation using a GitHub model."""
    try:
        # Read the eval file content
        with open(eval_file, 'r', encoding='utf-8') as f:
            content = f.read()[:3000]  # Truncate for API limits
        
        prompt = f"""Evaluate this prompt template on a 1-10 scale for each criterion.
Return ONLY valid JSON with scores and brief reasoning.

Criteria:
- clarity: Is it unambiguous and easy to understand?
- specificity: Enough detail for consistent outputs?
- actionability: Can the AI determine what to do?
- structure: Well-organized with clear sections?
- completeness: Covers all necessary aspects?
- safety: Avoids harmful patterns?

Prompt to evaluate:
```
{content}
```

Return ONLY valid JSON in this exact format:
{{"scores": {{"clarity": N, "specificity": N, "actionability": N, "structure": N, "completeness": N, "safety": N}}, "overall": N, "summary": "brief assessment"}}"""

        # Run gh models run command
        result = subprocess.run(
            ["gh", "models", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode != 0:
            return {
                "error": result.stderr or "Unknown error",
                "rc": result.returncode,
                "model": model,
                "eval_file": eval_file
            }
        
        # Parse JSON from response
        response = result.stdout.strip()
        
        # Try to extract JSON from response
        try:
            # Find JSON in response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                data = json.loads(json_str)
                data["model"] = model
                data["eval_file"] = eval_file
                data["source"] = "github"
                return data
        except json.JSONDecodeError:
            pass
        
        return {
            "raw_response": response[:500],
            "model": model,
            "eval_file": eval_file,
            "source": "github",
            "error": "Could not parse JSON"
        }
        
    except subprocess.TimeoutExpired:
        return {"error": "Timeout", "model": model, "eval_file": eval_file}
    except Exception as e:
        return {"error": str(e), "model": model, "eval_file": eval_file}


def run_local_model_eval(eval_file: str) -> Dict[str, Any]:
    """Run evaluation using local ONNX model."""
    try:
        # Import local model
        sys.path.insert(0, str(Path(__file__).parent))
        from local_model import LocalModel
        
        # Read eval file
        with open(eval_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Initialize and run
        model = LocalModel(verbose=False)
        result = model.evaluate_prompt(content)
        result["model"] = "local:mistral-7b-instruct"
        result["eval_file"] = eval_file
        result["source"] = "local-onnx"
        return result
        
    except Exception as e:
        return {
            "error": str(e),
            "model": "local:mistral-7b-instruct",
            "eval_file": eval_file,
            "source": "local-onnx"
        }


def aggregate_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Aggregate evaluation results."""
    by_file = {}
    by_model = {}
    
    for r in results:
        eval_file = r.get("eval_file", "unknown")
        model = r.get("model", "unknown")
        overall = r.get("overall", r.get("overall_score", 0))
        
        # By file
        if eval_file not in by_file:
            by_file[eval_file] = {"scores": [], "models": []}
        if overall:
            by_file[eval_file]["scores"].append(overall)
            by_file[eval_file]["models"].append(model)
        
        # By model
        if model not in by_model:
            by_model[model] = {"scores": [], "files": []}
        if overall:
            by_model[model]["scores"].append(overall)
            by_model[model]["files"].append(eval_file)
    
    # Calculate averages
    summary = {
        "by_file": {},
        "by_model": {},
        "overall_average": 0,
        "total_evals": len(results),
        "successful_evals": sum(1 for r in results if r.get("overall", r.get("overall_score")))
    }
    
    all_scores = []
    for f, data in by_file.items():
        if data["scores"]:
            avg = sum(data["scores"]) / len(data["scores"])
            summary["by_file"][Path(f).name] = {
                "average": round(avg, 2),
                "scores": data["scores"],
                "models": data["models"]
            }
            all_scores.extend(data["scores"])
    
    for m, data in by_model.items():
        if data["scores"]:
            avg = sum(data["scores"]) / len(data["scores"])
            summary["by_model"][m] = {
                "average": round(avg, 2),
                "count": len(data["scores"])
            }
    
    if all_scores:
        summary["overall_average"] = round(sum(all_scores) / len(all_scores), 2)
    
    return summary


def main():
    parser = argparse.ArgumentParser(description="Batch evaluate prompts with smart model selection")
    parser.add_argument("folder", help="Folder containing .prompt.yml files")
    parser.add_argument("--output", "-o", default="batch_eval_results.json", help="Output file")
    parser.add_argument("--gh-only", action="store_true", help="Only use GitHub models")
    parser.add_argument("--local-only", action="store_true", help="Only use local models")
    parser.add_argument("--models", nargs="+", help="Specific GH models to use (overrides smart selection)")
    parser.add_argument("--allow-premium", action="store_true", help="Allow premium models for complex prompts")
    parser.add_argument("--show-complexity", action="store_true", help="Show complexity analysis only")
    args = parser.parse_args()
    
    # Find eval files
    folder = Path(args.folder)
    if folder.is_file():
        eval_files = [folder]
    else:
        eval_files = list(folder.glob("*.prompt.yml"))
    
    if not eval_files:
        print(f"No .prompt.yml files found in {folder}")
        sys.exit(1)
    
    print(f"Found {len(eval_files)} eval files")
    print(f"Premium models: {'ENABLED' if args.allow_premium else 'DISABLED'}")
    
    # Show complexity analysis if requested
    if args.show_complexity:
        print("\n" + "="*60)
        print("COMPLEXITY ANALYSIS")
        print("="*60)
        for ef in eval_files:
            with open(ef, 'r', encoding='utf-8') as f:
                content = f.read()
            tier, score, reasons = assess_complexity(content)
            print(f"\n{ef.name}:")
            print(f"  Tier: {tier.upper()} (score: {score:.1f})")
            print(f"  Reasons: {', '.join(reasons[:3])}")
            models = select_models_for_prompt(content, args.allow_premium)
            print(f"  Selected models: {', '.join(models)}")
        return
    
    use_local = not args.gh_only
    use_gh = not args.local_only
    
    results = []
    timestamp = datetime.now().isoformat()
    
    # Run evaluations
    for i, eval_file in enumerate(eval_files, 1):
        with open(eval_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Smart model selection (unless specific models provided)
        if args.models:
            gh_models = args.models
        else:
            gh_models = select_models_for_prompt(content, args.allow_premium)
        
        tier, score, reasons = assess_complexity(content)
        print(f"\n[{i}/{len(eval_files)}] {eval_file.name}")
        print(f"  Complexity: {tier.upper()} (score: {score:.1f})")
        print(f"  Models: {', '.join(gh_models)}")
        
        # Local model
        if use_local:
            print("  → Running local ONNX model...")
            start = time.time()
            result = run_local_model_eval(str(eval_file))
            result["duration_s"] = round(time.time() - start, 2)
            result["complexity_tier"] = tier
            result["complexity_score"] = score
            results.append(result)
            overall = result.get("overall", "N/A")
            print(f"    Score: {overall}")
        
        # GitHub models
        if use_gh:
            for model in gh_models:
                print(f"  → Running {model}...")
                start = time.time()
                result = run_gh_model_eval(str(eval_file), model)
                result["duration_s"] = round(time.time() - start, 2)
                result["complexity_tier"] = tier
                result["complexity_score"] = score
                results.append(result)
                overall = result.get("overall", result.get("overall_score", "N/A"))
                if "error" in result:
                    print(f"    Error: {result['error'][:50]}")
                else:
                    print(f"    Score: {overall}")
                time.sleep(1)  # Rate limiting
    
    # Aggregate and save
    summary = aggregate_results(results)
    
    output = {
        "timestamp": timestamp,
        "summary": summary,
        "results": results
    }
    
    output_path = Path(args.output)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n{'='*60}")
    print("EVALUATION SUMMARY")
    print(f"{'='*60}")
    print(f"Total evaluations: {summary['total_evals']}")
    print(f"Successful: {summary['successful_evals']}")
    print(f"Overall average score: {summary['overall_average']}")
    print(f"\nBy Model:")
    for model, data in summary["by_model"].items():
        print(f"  {model}: {data['average']} (n={data['count']})")
    print(f"\nBy File:")
    for f, data in summary["by_file"].items():
        print(f"  {f}: {data['average']}")
    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()
