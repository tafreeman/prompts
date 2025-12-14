#!/usr/bin/env python3
"""
Tiered Prompt Evaluation Runner
================================

Executes prompt evaluations at different cost/depth tiers.

Tiers:
    1. Quick Triage   - $0, seconds    - Structural analysis only
    2. Single Model   - ~$0.05, 1-2min - One LLM evaluation
    3. Cross-Validate - ~$0.30, 5-10min - 3 models × 2 runs each
    4. Full Pipeline  - ~$2-5, 30-60min - 5 models × 4 runs each

Usage:
    # Quick triage (free, fast)
    python tools/tiered_eval.py prompts/socmint/ --tier 1

    # Single model evaluation
    python tools/tiered_eval.py prompts/socmint/company-osint-investigation.md --tier 2

    # Cross-validation (3 models)
    python tools/tiered_eval.py prompts/socmint/company-osint-investigation.md --tier 3

    # Full pipeline (5 models, 4 runs each)
    python tools/tiered_eval.py prompts/socmint/company-osint-investigation.md --tier 4

    # List available models
    python tools/tiered_eval.py --list-models

Author: Prompts Library Team
Version: 1.0.0
"""

import argparse
import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

# =============================================================================
# TIER CONFIGURATION
# =============================================================================

@dataclass
class TierConfig:
    """Configuration for each evaluation tier."""
    name: str
    description: str
    cost_estimate: str
    time_estimate: str
    models: List[str]
    runs_per_model: int
    uses_llm: bool
    tools: List[str]


# =============================================================================
# MODEL DEFINITIONS - Updated December 2025
# =============================================================================

# GitHub Models available via `gh models run` (validated Dec 2025)
# NOTE: Claude/Gemini are NOT available in gh models - only via direct API
GH_AVAILABLE_MODELS = [
    "openai/gpt-4.1",
    "openai/gpt-4o",
    "openai/gpt-4o-mini",
    "mistral-ai/mistral-small-2503",
    "meta/llama-3.3-70b-instruct",
]

# All models (including those requiring direct API access)
ALL_MODELS = {
    # Local models (onnxruntime-genai)
    "local/mistral-7b": {"provider": "local-onnx", "speed": "medium", "quality": "good", "cost": "free"},
    
    # GitHub Models (available via gh models run)
    "openai/gpt-4.1": {"provider": "gh-models", "speed": "fast", "quality": "high", "cost": "free"},
    "openai/gpt-4o": {"provider": "gh-models", "speed": "fast", "quality": "high", "cost": "free"},
    "openai/gpt-4o-mini": {"provider": "gh-models", "speed": "very-fast", "quality": "good", "cost": "free"},
    "mistral-ai/mistral-small-2503": {"provider": "gh-models", "speed": "fast", "quality": "good", "cost": "free"},
    "meta/llama-3.3-70b-instruct": {"provider": "gh-models", "speed": "medium", "quality": "high", "cost": "free"},
    
    # Claude models (Copilot Chat only - NOT gh models)
    "claude-haiku-4.5": {"provider": "copilot-chat", "speed": "fast", "quality": "good", "cost": "included"},
    "claude-sonnet-4": {"provider": "copilot-chat", "speed": "medium", "quality": "high", "cost": "included"},
    "claude-sonnet-4.5": {"provider": "copilot-chat", "speed": "medium", "quality": "very-high", "cost": "included"},
    "claude-opus-4.5": {"provider": "copilot-chat", "speed": "slow", "quality": "exceptional", "cost": "included"},
    
    # GPT-5 models (may require API key)
    "openai/gpt-5-mini": {"provider": "api", "speed": "very-fast", "quality": "good", "cost": "low"},
    "openai/gpt-5": {"provider": "api", "speed": "medium", "quality": "very-high", "cost": "high"},
}

# Model definitions by category (using ONLY gh-models compatible ones for dual_eval)
MODELS = {
    # Local models - Free, no rate limits
    "local": [
        "local/mistral-7b",            # Local ONNX Mistral 7B
    ],
    # Fast/cheap models - Best for quick checks
    "fast": [
        "openai/gpt-4o-mini",         # ⭐ RECOMMENDED: Fastest GitHub Model
        "mistral-ai/mistral-small-2503",
    ],
    # Balanced models - Best for standard evaluation
    "balanced": [
        "openai/gpt-4.1",             # ⭐ RECOMMENDED: Great balance
        "openai/gpt-4o",
        "mistral-ai/mistral-small-2503",
    ],
    # High quality models - Best for thorough evaluation
    "quality": [
        "openai/gpt-4.1",             # ⭐ RECOMMENDED
        "openai/gpt-4o",
        "meta/llama-3.3-70b-instruct",
        "mistral-ai/mistral-small-2503",
        "openai/gpt-4o-mini",
    ],
}

# Best model recommendations by use case
RECOMMENDED_MODELS = {
    "quick_check": "openai/gpt-4o-mini",
    "code_review": "openai/gpt-4.1",
    "standard_eval": "openai/gpt-4o",
    "thorough_eval": "openai/gpt-4.1",
    "multi_model": ["openai/gpt-4o-mini", "openai/gpt-4.1", "mistral-ai/mistral-small-2503"],
    "budget": "openai/gpt-4o-mini",
    "maximum_quality": "meta/llama-3.3-70b-instruct",
}

# Tier definitions
TIERS: Dict[int, TierConfig] = {
    0: TierConfig(
        name="Local Model",
        description="Local ONNX Mistral 7B - free, no rate limits, ~30s/prompt",
        cost_estimate="$0 (local CPU)",
        time_estimate="30-60 seconds per prompt",
        models=["local/mistral-7b"],
        runs_per_model=1,
        uses_llm=True,
        tools=["local_model.py"],
    ),
    1: TierConfig(
        name="Quick Triage",
        description="Structural analysis only - no LLM calls",
        cost_estimate="$0",
        time_estimate="<1 second per prompt",
        models=[],
        runs_per_model=0,
        uses_llm=False,
        tools=["prompt_analyzer.py", "batch_evaluate.py --simple"],
    ),
    2: TierConfig(
        name="Single Model",
        description="One fast LLM evaluation for validation",
        cost_estimate="$0 (free GitHub Model)",
        time_estimate="15-45 seconds",
        models=["openai/gpt-4o-mini"],  # ⭐ BEST: Fastest GitHub Model
        runs_per_model=1,
        uses_llm=True,
        tools=["run_gh_eval.py"],
    ),
    # NOTE: Tiers 3-5 use ONLY gh-models compatible models (dual_eval.py uses `gh models run`)
    # Claude/Gemini are NOT available in gh models - only via Copilot Chat
    3: TierConfig(
        name="Cross-Validation",
        description="3 diverse gh-models × 2 runs for confidence",
        cost_estimate="$0 (free GitHub Models)",
        time_estimate="2-4 minutes",
        models=[
            "openai/gpt-4o-mini",               # Fast baseline
            "openai/gpt-4.1",                   # Quality check
            "mistral-ai/mistral-small-2503",   # Diverse perspective
        ],
        runs_per_model=2,
        uses_llm=True,
        tools=["dual_eval.py"],
    ),
    4: TierConfig(
        name="Full Pipeline",
        description="5 gh-models × 3 runs for release qualification",
        cost_estimate="$0 (free GitHub Models)",
        time_estimate="5-10 minutes",
        models=[
            "openai/gpt-4.1",                   # ⭐ Best GPT on gh-models
            "openai/gpt-4o",                    # Strong GPT
            "meta/llama-3.3-70b-instruct",     # Top open-source
            "openai/gpt-4o-mini",               # Fast cross-check
            "mistral-ai/mistral-small-2503",   # Diverse cross-check
        ],
        runs_per_model=3,
        uses_llm=True,
        tools=["dual_eval.py", "evaluation_agent.py"],
    ),
    5: TierConfig(
        name="Premium Evaluation",
        description="All gh-models × 4 runs for critical prompts",
        cost_estimate="$0 (free GitHub Models)",
        time_estimate="10-20 minutes",
        models=[
            "openai/gpt-4.1",                   # ⭐ Best overall
            "openai/gpt-4o",                    # Strong alternative
            "meta/llama-3.3-70b-instruct",     # Top open-source  
            "mistral-ai/mistral-small-2503",   # Fast diverse check
            "openai/gpt-4o-mini",               # Fast cross-check
        ],
        runs_per_model=4,
        uses_llm=True,
        tools=["dual_eval.py", "evaluation_agent.py"],
    ),
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_repo_root() -> Path:
    """Get the repository root directory."""
    return Path(__file__).parent.parent


def find_prompts(path: str) -> List[Path]:
    """Find all prompt files in a path (file or directory)."""
    target = Path(path)
    
    if target.is_file():
        return [target]
    
    if target.is_dir():
        prompts = []
        for md_file in target.rglob("*.md"):
            # Skip non-prompt files
            if md_file.name in {"README.md", "index.md", "CHANGELOG.md"}:
                continue
            if md_file.name.endswith((".agent.md", ".instructions.md")):
                continue
            if any(part in {"archive", "node_modules", ".git"} for part in md_file.parts):
                continue
            prompts.append(md_file)
        return sorted(prompts)
    
    print(f"Error: Path not found: {path}")
    return []


def run_dual_eval(prompt_path: Path, models: List[str], runs: int, repo_root: Path, timeout: int = 600) -> Dict[str, Any]:
    """
    Run dual_eval.py on a prompt and return parsed results.
    
    dual_eval.py writes JSON to a file, not stdout, so we need to:
    1. Specify an output file path
    2. Run the command
    3. Read and parse the JSON file
    4. Clean up
    """
    import tempfile
    import os
    
    dual_eval_path = repo_root / "testing" / "evals" / "dual_eval.py"
    
    # Create a temp file for the output
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        output_path = Path(tmp.name)
    
    try:
        # Build command - specify explicit output path and quiet mode to reduce emoji output
        cmd = [
            sys.executable, str(dual_eval_path),
            str(prompt_path),
            "--runs", str(runs),
            "--format", "json",
            "--output", str(output_path),
            "--quiet",  # Suppress progress output (avoids encoding issues)
            "--models",
        ] + models
        
        # Set PYTHONIOENCODING to handle emojis in case --quiet isn't enough
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',  # Explicit UTF-8 to handle emojis
            errors='replace',  # Replace undecodable chars instead of crashing
            timeout=timeout,
            cwd=str(repo_root),
            env=env,
        )
        
        # Check if output file was created
        if output_path.exists():
            try:
                eval_data = json.loads(output_path.read_text(encoding='utf-8'))
                # Extract first result if it's a batch report
                if "results" in eval_data and eval_data["results"]:
                    first_result = eval_data["results"][0]
                    return {
                        "success": True,
                        "consensus_score": first_result.get("consensus_score", 0),
                        "cross_validation_passed": first_result.get("cross_validation_passed", False),
                        "final_grade": first_result.get("final_grade", "N/A"),
                        "final_pass": first_result.get("final_pass", False),
                        "score_variance": first_result.get("score_variance", 0),
                        "model_summaries": first_result.get("model_summaries", {}),
                        "combined_strengths": first_result.get("combined_strengths", []),
                        "combined_improvements": first_result.get("combined_improvements", []),
                    }
                else:
                    return {
                        "success": True,
                        "data": eval_data,
                    }
            except json.JSONDecodeError as e:
                return {
                    "success": False,
                    "error": f"JSON parse error: {e}",
                }
        else:
            return {
                "success": False,
                "error": result.stderr[:500] if result.stderr else "No output file created",
            }
            
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Timeout ({timeout} seconds)",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
    finally:
        # Clean up temp file
        if output_path.exists():
            output_path.unlink()


def print_tier_info(tier: int):
    """Print information about a tier."""
    config = TIERS[tier]
    print(f"\n{'='*60}")
    print(f"TIER {tier}: {config.name}")
    print(f"{'='*60}")
    print(f"Description: {config.description}")
    print(f"Cost: {config.cost_estimate}")
    print(f"Time: {config.time_estimate}")
    print(f"Uses LLM: {'Yes' if config.uses_llm else 'No'}")
    if config.models:
        print(f"Models ({len(config.models)}):")
        for model in config.models:
            print(f"  - {model}")
        print(f"Runs per model: {config.runs_per_model}")
        print(f"Total API calls: {len(config.models) * config.runs_per_model}")
    print(f"Tools: {', '.join(config.tools)}")
    print()


# =============================================================================
# TIER EXECUTION FUNCTIONS
# =============================================================================

def run_tier_0(prompts: List[Path], output_dir: Path) -> Dict[str, Any]:
    """
    Tier 0: Local Model - Uses local ONNX Mistral 7B for evaluation ($0, no rate limits)
    Uses: local_model.py --evaluate
    
    Benefits:
    - Completely free (runs locally)
    - No rate limits (process as many prompts as needed)
    - Privacy (no data sent to external APIs)
    - Consistent (same model for all evaluations)
    
    Trade-offs:
    - Slower (~30-60s per prompt on CPU)
    - Single model perspective (no cross-validation)
    """
    results = {
        "tier": 0,
        "name": "Local Model (Mistral 7B ONNX)",
        "prompts_evaluated": 0,
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "total_cost": "$0 (local CPU)",
        "results": [],
    }
    
    repo_root = get_repo_root()
    local_model_path = repo_root / "tools" / "local_model.py"
    
    # Check if local_model.py exists
    if not local_model_path.exists():
        print(f"\n❌ Error: local_model.py not found at {local_model_path}")
        print("   Run: python tools/local_model.py --check to verify model setup")
        return results
    
    # Check if model is available
    print("\n🔍 Checking local model availability...")
    check_result = subprocess.run(
        [sys.executable, str(local_model_path), "--check"],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=str(repo_root),
    )
    
    if check_result.returncode != 0:
        print("\n❌ Local model not available. Setup instructions:")
        print("   1. Install: pip install onnxruntime-genai")
        print("   2. Download Mistral 7B ONNX model from AI Gallery or HuggingFace")
        print("   3. Run: python tools/local_model.py --check")
        return results
    
    model_info = json.loads(check_result.stdout)
    print(f"   ✓ Model found: {model_info.get('found_path', 'unknown')}")
    print(f"   ✓ onnxruntime-genai: {model_info.get('onnxruntime_genai_version', 'unknown')}")
    
    print(f"\n🤖 Running local model evaluation on {len(prompts)} prompts...")
    
    for i, prompt_path in enumerate(prompts, 1):
        rel_path = prompt_path.relative_to(repo_root) if prompt_path.is_relative_to(repo_root) else prompt_path
        print(f"  [{i}/{len(prompts)}] Evaluating: {rel_path}")
        
        try:
            result = subprocess.run(
                [sys.executable, str(local_model_path),
                 "--evaluate", str(prompt_path)],
                capture_output=True,
                text=True,
                timeout=120,  # 2 minutes timeout for local inference
                cwd=str(repo_root),
            )
            
            if result.returncode == 0 and result.stdout:
                try:
                    eval_result = json.loads(result.stdout)
                    overall_score = eval_result.get("overall", 0)
                    
                    # Pass threshold: 7.0 or higher
                    passed = overall_score >= 7.0
                    
                    results["results"].append({
                        "file": str(rel_path),
                        "score": overall_score,
                        "scores": eval_result.get("scores", {}),
                        "summary": eval_result.get("summary", ""),
                        "passed": passed,
                        "model": "local/mistral-7b",
                        "tool": "local_model.py",
                    })
                    
                    status = "✅" if passed else "❌"
                    print(f"       {status} Score: {overall_score}/10")
                    
                    if passed:
                        results["passed"] += 1
                    else:
                        results["failed"] += 1
                        
                except json.JSONDecodeError as e:
                    results["results"].append({
                        "file": str(rel_path),
                        "error": f"JSON parse error: {e}",
                        "raw_output": result.stdout[:500],
                        "tool": "local_model.py",
                    })
                    results["errors"] += 1
                    print(f"       ⚠️ JSON parse error")
            else:
                results["results"].append({
                    "file": str(rel_path),
                    "error": result.stderr or "Unknown error",
                    "tool": "local_model.py",
                })
                results["errors"] += 1
                print(f"       ⚠️ Error: {result.stderr[:50] if result.stderr else 'Unknown'}")
                
        except subprocess.TimeoutExpired:
            results["results"].append({
                "file": str(rel_path),
                "error": "Timeout (>120s)",
                "tool": "local_model.py",
            })
            results["errors"] += 1
            print(f"       ⚠️ Timeout")
        except Exception as e:
            results["results"].append({
                "file": str(rel_path),
                "error": str(e),
                "tool": "local_model.py",
            })
            results["errors"] += 1
            print(f"       ⚠️ Error: {e}")
        
        results["prompts_evaluated"] += 1
    
    return results


def run_tier_1(prompts: List[Path], output_dir: Path) -> Dict[str, Any]:
    """
    Tier 1: Quick Triage - Structural analysis only ($0)
    Uses: prompt_analyzer.py + batch_evaluate.py --simple
    """
    results = {
        "tier": 1,
        "prompts_evaluated": 0,
        "total_cost": "$0",
        "results": [],
    }
    
    repo_root = get_repo_root()
    
    # Run prompt_analyzer.py for detailed structural analysis
    print("\n📊 Running structural analysis with prompt_analyzer.py...")
    
    for prompt_path in prompts:
        rel_path = prompt_path.relative_to(repo_root) if prompt_path.is_relative_to(repo_root) else prompt_path
        print(f"  Analyzing: {rel_path}")
        
        try:
            result = subprocess.run(
                [sys.executable, str(repo_root / "tools" / "analyzers" / "prompt_analyzer.py"),
                 "--file", str(prompt_path), "--json"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(repo_root),
            )
            
            if result.returncode == 0 and result.stdout:
                try:
                    analysis = json.loads(result.stdout)
                    results["results"].append({
                        "file": str(rel_path),
                        "score": analysis.get("total_score", 0),
                        "rating": analysis.get("rating_label", "Unknown"),
                        "dimensions": {
                            "clarity": analysis.get("clarity", {}).get("score", 0),
                            "effectiveness": analysis.get("effectiveness", {}).get("score", 0),
                            "reusability": analysis.get("reusability", {}).get("score", 0),
                            "simplicity": analysis.get("simplicity", {}).get("score", 0),
                            "examples": analysis.get("examples", {}).get("score", 0),
                        },
                        "tool": "prompt_analyzer.py",
                    })
                except json.JSONDecodeError:
                    # Fall back to basic analysis
                    results["results"].append({
                        "file": str(rel_path),
                        "score": "N/A",
                        "tool": "prompt_analyzer.py",
                        "error": "Could not parse JSON output",
                    })
            else:
                results["results"].append({
                    "file": str(rel_path),
                    "error": result.stderr or "Unknown error",
                    "tool": "prompt_analyzer.py",
                })
                
        except subprocess.TimeoutExpired:
            results["results"].append({
                "file": str(rel_path),
                "error": "Timeout",
                "tool": "prompt_analyzer.py",
            })
        except Exception as e:
            results["results"].append({
                "file": str(rel_path),
                "error": str(e),
                "tool": "prompt_analyzer.py",
            })
        
        results["prompts_evaluated"] += 1
    
    return results


def run_tier_2(prompts: List[Path], output_dir: Path) -> Dict[str, Any]:
    """
    Tier 2: Single Model - One fast LLM evaluation (~$0.05)
    Uses: gh models run with gpt-4o-mini
    """
    config = TIERS[2]
    model = config.models[0]
    
    results = {
        "tier": 2,
        "model": model,
        "prompts_evaluated": 0,
        "total_cost": config.cost_estimate,
        "results": [],
    }
    
    repo_root = get_repo_root()
    
    print(f"\n🤖 Running single-model evaluation with {model}...")
    
    for prompt_path in prompts:
        rel_path = prompt_path.relative_to(repo_root) if prompt_path.is_relative_to(repo_root) else prompt_path
        print(f"  Evaluating: {rel_path}")
        
        # Read prompt content
        try:
            content = prompt_path.read_text(encoding="utf-8")
        except Exception as e:
            results["results"].append({
                "file": str(rel_path),
                "error": f"Could not read file: {e}",
            })
            continue
        
        # Build evaluation prompt
        eval_prompt = f"""Evaluate this prompt template on a 1-10 scale for each criterion.
Return JSON with scores and brief reasoning.

Criteria:
- clarity: Is it unambiguous and easy to understand?
- specificity: Enough detail for consistent outputs?
- actionability: Can the AI determine what to do?
- structure: Well-organized with clear sections?
- completeness: Covers all necessary aspects?
- safety: Avoids harmful patterns?

Prompt to evaluate:
```
{content[:4000]}
```

Return ONLY valid JSON:
{{"scores": {{"clarity": N, "specificity": N, "actionability": N, "structure": N, "completeness": N, "safety": N}}, "overall": N, "summary": "brief assessment"}}"""

        try:
            result = subprocess.run(
                ["gh", "models", "run", model, "--", eval_prompt],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(repo_root),
            )
            
            if result.returncode == 0:
                # Try to parse JSON from response
                response = result.stdout.strip()
                try:
                    # Find JSON in response
                    import re
                    json_match = re.search(r'\{.*\}', response, re.DOTALL)
                    if json_match:
                        eval_data = json.loads(json_match.group())
                        overall_score = eval_data.get("overall", 0)
                        results["results"].append({
                            "file": str(rel_path),
                            "model": model,
                            "scores": eval_data.get("scores", {}),
                            "overall": overall_score,
                            "final_pass": overall_score >= 7.0,  # Same threshold as dual_eval
                            "summary": eval_data.get("summary", ""),
                            "tool": "gh models run",
                        })
                    else:
                        results["results"].append({
                            "file": str(rel_path),
                            "model": model,
                            "raw_response": response[:500],
                            "error": "Could not parse JSON from response",
                        })
                except json.JSONDecodeError:
                    results["results"].append({
                        "file": str(rel_path),
                        "model": model,
                        "raw_response": response[:500],
                        "error": "Invalid JSON in response",
                    })
            else:
                results["results"].append({
                    "file": str(rel_path),
                    "model": model,
                    "error": result.stderr or "Unknown error",
                })
                
        except subprocess.TimeoutExpired:
            results["results"].append({
                "file": str(rel_path),
                "model": model,
                "error": "Timeout (120s)",
            })
        except FileNotFoundError:
            print("Error: 'gh' CLI not found. Install GitHub CLI and gh-models extension.")
            results["results"].append({
                "file": str(rel_path),
                "error": "gh CLI not found",
            })
            break
        
        results["prompts_evaluated"] += 1
    
    return results


def run_tier_3(prompts: List[Path], output_dir: Path) -> Dict[str, Any]:
    """
    Tier 3: Cross-Validation - 3 models × 2 runs
    Uses: dual_eval.py with multi-model consensus
    """
    config = TIERS[3]
    
    results = {
        "tier": 3,
        "models": config.models,
        "runs_per_model": config.runs_per_model,
        "prompts_evaluated": 0,
        "total_cost": config.cost_estimate,
        "results": [],
    }
    
    repo_root = get_repo_root()
    dual_eval_path = repo_root / "testing" / "evals" / "dual_eval.py"
    
    if not dual_eval_path.exists():
        print(f"Error: dual_eval.py not found at {dual_eval_path}")
        return results
    
    print(f"\n🔄 Running cross-validation with {len(config.models)} models × {config.runs_per_model} runs...")
    print(f"   Models: {', '.join(config.models)}")
    
    for prompt_path in prompts:
        rel_path = prompt_path.relative_to(repo_root) if prompt_path.is_relative_to(repo_root) else prompt_path
        print(f"\n  Evaluating: {rel_path}")
        
        # Use helper function to run dual_eval and get JSON results
        eval_result = run_dual_eval(
            prompt_path=prompt_path,
            models=config.models,
            runs=config.runs_per_model,
            repo_root=repo_root,
            timeout=600,  # 10 minutes
        )
        
        if eval_result.get("success"):
            results["results"].append({
                "file": str(rel_path),
                "consensus_score": eval_result.get("consensus_score", 0),
                "cross_validation_passed": eval_result.get("cross_validation_passed", False),
                "final_grade": eval_result.get("final_grade", "N/A"),
                "final_pass": eval_result.get("final_pass", False),
                "model_summaries": eval_result.get("model_summaries", {}),
                "combined_strengths": eval_result.get("combined_strengths", []),
                "combined_improvements": eval_result.get("combined_improvements", []),
                "tool": "dual_eval.py",
            })
        else:
            results["results"].append({
                "file": str(rel_path),
                "error": eval_result.get("error", "Unknown error"),
                "tool": "dual_eval.py",
            })
        
        results["prompts_evaluated"] += 1
    
    return results


def run_tier_4(prompts: List[Path], output_dir: Path) -> Dict[str, Any]:
    """
    Tier 4: Full Pipeline - 5 models × 3 runs
    Uses: dual_eval.py with full model set
    """
    config = TIERS[4]
    
    results = {
        "tier": 4,
        "models": config.models,
        "runs_per_model": config.runs_per_model,
        "prompts_evaluated": 0,
        "total_cost": config.cost_estimate,
        "results": [],
    }
    
    repo_root = get_repo_root()
    dual_eval_path = repo_root / "testing" / "evals" / "dual_eval.py"
    
    if not dual_eval_path.exists():
        print(f"Error: dual_eval.py not found at {dual_eval_path}")
        return results
    
    print(f"\n🚀 Running full pipeline with {len(config.models)} models × {config.runs_per_model} runs...")
    print(f"   Models: {', '.join(config.models)}")
    print(f"   Total API calls per prompt: {len(config.models) * config.runs_per_model}")
    
    for prompt_path in prompts:
        rel_path = prompt_path.relative_to(repo_root) if prompt_path.is_relative_to(repo_root) else prompt_path
        print(f"\n  Evaluating: {rel_path}")
        
        # Use helper function to run dual_eval and get JSON results
        eval_result = run_dual_eval(
            prompt_path=prompt_path,
            models=config.models,
            runs=config.runs_per_model,
            repo_root=repo_root,
            timeout=900,  # 15 minutes
        )
        
        if eval_result.get("success"):
            results["results"].append({
                "file": str(rel_path),
                "consensus_score": eval_result.get("consensus_score", 0),
                "score_variance": eval_result.get("score_variance", 0),
                "cross_validation_passed": eval_result.get("cross_validation_passed", False),
                "final_grade": eval_result.get("final_grade", "N/A"),
                "final_pass": eval_result.get("final_pass", False),
                "model_summaries": eval_result.get("model_summaries", {}),
                "combined_strengths": eval_result.get("combined_strengths", []),
                "combined_improvements": eval_result.get("combined_improvements", []),
                "tool": "dual_eval.py",
            })
        else:
            results["results"].append({
                "file": str(rel_path),
                "error": eval_result.get("error", "Unknown error"),
                "tool": "dual_eval.py",
            })
        
        results["prompts_evaluated"] += 1
    
    return results


def run_tier_5(prompts: List[Path], output_dir: Path) -> Dict[str, Any]:
    """
    Tier 5: Premium Evaluation - All gh-models × 4 runs
    Uses: dual_eval.py with maximum configuration
    """
    config = TIERS[5]
    
    results = {
        "tier": 5,
        "models": config.models,
        "runs_per_model": config.runs_per_model,
        "prompts_evaluated": 0,
        "total_cost": config.cost_estimate,
        "results": [],
    }
    
    repo_root = get_repo_root()
    dual_eval_path = repo_root / "testing" / "evals" / "dual_eval.py"
    
    if not dual_eval_path.exists():
        print(f"Error: dual_eval.py not found at {dual_eval_path}")
        return results
    
    print(f"\n💎 Running premium evaluation with {len(config.models)} models × {config.runs_per_model} runs...")
    print(f"   Models: {', '.join(config.models)}")
    print(f"   Total API calls per prompt: {len(config.models) * config.runs_per_model}")
    
    for prompt_path in prompts:
        rel_path = prompt_path.relative_to(repo_root) if prompt_path.is_relative_to(repo_root) else prompt_path
        print(f"\n  Evaluating: {rel_path}")
        
        # Use helper function to run dual_eval and get JSON results
        eval_result = run_dual_eval(
            prompt_path=prompt_path,
            models=config.models,
            runs=config.runs_per_model,
            repo_root=repo_root,
            timeout=1200,  # 20 minutes for premium tier
        )
        
        if eval_result.get("success"):
            results["results"].append({
                "file": str(rel_path),
                "consensus_score": eval_result.get("consensus_score", 0),
                "score_variance": eval_result.get("score_variance", 0),
                "cross_validation_passed": eval_result.get("cross_validation_passed", False),
                "final_grade": eval_result.get("final_grade", "N/A"),
                "final_pass": eval_result.get("final_pass", False),
                "model_summaries": eval_result.get("model_summaries", {}),
                "combined_strengths": eval_result.get("combined_strengths", []),
                "combined_improvements": eval_result.get("combined_improvements", []),
                "tool": "dual_eval.py",
            })
        else:
            results["results"].append({
                "file": str(rel_path),
                "error": eval_result.get("error", "Unknown error"),
                "tool": "dual_eval.py",
            })
        
        results["prompts_evaluated"] += 1
    
    return results


# =============================================================================
# REPORT GENERATION
# =============================================================================

def generate_report(results: Dict[str, Any], output_path: Path):
    """Generate a markdown report from evaluation results."""
    tier = results.get("tier", 0)
    config = TIERS.get(tier, TIERS[1])
    
    lines = [
        f"# Tier {tier} Evaluation Report: {config.name}",
        f"",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Cost Estimate:** {results.get('total_cost', 'N/A')}",
        f"**Prompts Evaluated:** {results.get('prompts_evaluated', 0)}",
        f"",
    ]
    
    if config.models:
        lines.extend([
            f"## Models Used",
            f"",
        ])
        for model in config.models:
            lines.append(f"- `{model}`")
        lines.extend([
            f"",
            f"**Runs per model:** {config.runs_per_model}",
            f"",
        ])
    
    lines.extend([
        f"## Results",
        f"",
        f"| File | Score | Grade | Status |",
        f"|------|-------|-------|--------|",
    ])
    
    for r in results.get("results", []):
        file_name = Path(r.get("file", "")).name
        
        if "error" in r:
            lines.append(f"| {file_name} | - | - | ❌ {r['error'][:30]} |")
        elif tier == 0:
            # Local model results
            score = r.get("score", "N/A")
            passed = r.get("passed", False)
            status = "✅ PASS" if passed else "❌ FAIL"
            lines.append(f"| {file_name} | {score}/10 | N/A | {status} |")
        elif tier == 1:
            score = r.get("score", "N/A")
            rating = r.get("rating", "N/A")
            lines.append(f"| {file_name} | {score}/5.0 | {rating} | ✅ |")
        else:
            score = r.get("consensus_score") or r.get("overall") or r.get("score", "N/A")
            grade = r.get("final_grade", "N/A")
            passed = r.get("cross_validation_passed") or r.get("final_pass", False) or r.get("passed", False)
            status = "✅ PASS" if passed else "❌ FAIL"
            lines.append(f"| {file_name} | {score}/10 | {grade} | {status} |")
    
    lines.extend([
        f"",
        f"---",
        f"*Report generated by tiered_eval.py*",
    ])
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n📄 Report saved to: {output_path}")


def print_summary(results: Dict[str, Any]):
    """Print a summary of evaluation results."""
    tier = results.get("tier", 0)
    config = TIERS.get(tier, TIERS[1])
    
    print(f"\n{'='*60}")
    print(f"EVALUATION SUMMARY - Tier {tier}: {config.name}")
    print(f"{'='*60}")
    print(f"Prompts evaluated: {results.get('prompts_evaluated', 0)}")
    print(f"Estimated cost: {results.get('total_cost', 'N/A')}")
    
    passed = 0
    failed = 0
    errors = 0
    scores = []
    
    for r in results.get("results", []):
        if "error" in r:
            errors += 1
        elif r.get("passed") or r.get("cross_validation_passed") or r.get("final_pass"):
            passed += 1
            if r.get("consensus_score"):
                scores.append(r["consensus_score"])
            elif r.get("score"):
                scores.append(r["score"])
        elif r.get("score"):
            scores.append(r["score"])
            if tier == 1:
                passed += 1 if r["score"] >= 3.0 else 0
                failed += 1 if r["score"] < 3.0 else 0
            else:
                failed += 1
        else:
            failed += 1
    
    print(f"\nResults:")
    print(f"  ✅ Passed: {passed}")
    print(f"  ❌ Failed: {failed}")
    print(f"  ⚠️  Errors: {errors}")
    
    if scores:
        avg_score = sum(scores) / len(scores)
        print(f"\nAverage score: {avg_score:.2f}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Tiered Prompt Evaluation Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Tiers:
  0  Local Model      $0, ~30s/prompt  Mistral 7B ONNX (no rate limits!)
  1  Quick Triage     $0, <1s          Structural analysis only
  2  Single Model     $0, 15-45s       gpt-4o-mini (1 run via GitHub Models)
  3  Cross-Validate   $0, 2-4m         3 models × 2 runs (gpt-4o-mini, gpt-4.1, mistral)
  4  Full Pipeline    $0, 5-10m        5 models × 3 runs (gh-models)
  5  Premium          $0, 10-20m       5 models × 4 runs (gh-models)

Recommended for Different Scenarios:
  Bulk eval (no limits):  --tier 0   (local Mistral 7B, unlimited)
  Quick check:            --tier 1   (structural only, fastest)  
  Standard eval:          --tier 2   (single model, balanced)
  Confidence check:       --tier 3   (3 models, cross-validation)
  Release qualification:  --tier 4   (5 models, thorough)
  Critical prompts:       --tier 5   (5 models, maximum confidence)

Examples:
  python tools/tiered_eval.py prompts/socmint/ --tier 0       # Local model, no rate limits
  python tools/tiered_eval.py prompts/socmint/ --tier 1       # Structural analysis
  python tools/tiered_eval.py prompts/advanced/react.md --tier 3  # Cross-validation
  python tools/tiered_eval.py prompts/ --tier 2 --limit 5     # Sample 5 prompts
  python tools/tiered_eval.py prompts/critical.md --tier 5    # Premium eval
        """,
    )
    
    parser.add_argument("path", nargs="?", help="Prompt file or directory to evaluate")
    parser.add_argument("--tier", "-t", type=int, choices=[0, 1, 2, 3, 4, 5], default=1,
                        help="Evaluation tier (1-5)")
    parser.add_argument("--output", "-o", help="Output report path")
    parser.add_argument("--limit", "-l", type=int, help="Limit number of prompts to evaluate")
    parser.add_argument("--list-models", action="store_true", help="List available models")
    parser.add_argument("--list-tiers", action="store_true", help="List all tiers with details")
    parser.add_argument("--recommend", action="store_true", help="Show model recommendations")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of report")
    
    args = parser.parse_args()
    
    # List models
    if args.list_models:
        print("\n" + "=" * 70)
        print("AVAILABLE MODELS")
        print("=" * 70)
        for category, model_list in MODELS.items():
            print(f"\n{category.upper()}:")
            for model in model_list:
                info = ALL_MODELS.get(model, {})
                speed = info.get("speed", "unknown")
                quality = info.get("quality", "unknown")
                cost = info.get("cost", "unknown")
                star = "⭐" if model in [RECOMMENDED_MODELS["quick_check"], 
                                         RECOMMENDED_MODELS["standard_eval"],
                                         RECOMMENDED_MODELS["maximum_quality"]] else "  "
                print(f"  {star} {model:<35} speed:{speed:<10} quality:{quality:<12} cost:{cost}")
        return
    
    # Show recommendations
    if args.recommend:
        print("\n" + "=" * 70)
        print("MODEL RECOMMENDATIONS BY USE CASE")
        print("=" * 70)
        print(f"""
┌────────────────────┬─────────────────────────────────┬─────────────────────────┐
│ Use Case           │ Recommended Model               │ Why                     │
├────────────────────┼─────────────────────────────────┼─────────────────────────┤
│ Quick Check        │ openai/gpt-4o-mini              │ Fastest gh-model        │
│ Standard Eval      │ openai/gpt-4.1                  │ Best balance            │
│ Thorough Eval      │ openai/gpt-4.1                  │ Best gh-model quality   │
│ Budget Conscious   │ openai/gpt-4o-mini              │ Free & fast             │
│ Maximum Quality    │ meta/llama-3.3-70b-instruct     │ Top open-source         │
└────────────────────┴─────────────────────────────────┴─────────────────────────┘

Multi-Model Cross-Validation (recommended combo):
  1. openai/gpt-4o-mini              - Fast baseline
  2. openai/gpt-4.1                  - Quality verification  
  3. mistral-ai/mistral-small-2503   - Diverse perspective

Available GitHub Models (via `gh models run`):
  • openai/gpt-4.1               - Best overall
  • openai/gpt-4o                - Strong alternative
  • openai/gpt-4o-mini           - Fastest
  • mistral-ai/mistral-small-2503 - Good diversity
  • meta/llama-3.3-70b-instruct  - Top open-source

NOTE: Claude and Gemini models are only available via Copilot Chat,
      NOT via `gh models run`. Use them directly in chat for evaluation.
""")
        return
    
    # List tiers
    if args.list_tiers:
        print("\n" + "=" * 60)
        print("EVALUATION TIERS")
        print("=" * 60)
        for tier_num in sorted(TIERS.keys()):
            print_tier_info(tier_num)
        return
    
    # Require path for evaluation
    if not args.path:
        parser.print_help()
        print("\nError: Please provide a path to evaluate or use --list-models / --list-tiers")
        sys.exit(1)
    
    # Find prompts
    prompts = find_prompts(args.path)
    
    if not prompts:
        print(f"No prompt files found in: {args.path}")
        sys.exit(1)
    
    # Apply limit
    if args.limit:
        prompts = prompts[:args.limit]
    
    print(f"\n📋 Found {len(prompts)} prompt(s) to evaluate")
    print_tier_info(args.tier)
    
    # Set up output directory
    repo_root = get_repo_root()
    output_dir = repo_root / "docs" / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Run evaluation
    tier_runners = {
        0: run_tier_0,
        1: run_tier_1,
        2: run_tier_2,
        3: run_tier_3,
        4: run_tier_4,
        5: run_tier_5,
    }
    
    runner = tier_runners.get(args.tier)
    if not runner:
        print(f"Error: Unknown tier {args.tier}")
        sys.exit(1)
    
    results = runner(prompts, output_dir)
    
    # Output
    if args.json:
        print(json.dumps(results, indent=2, default=str))
    else:
        print_summary(results)
        
        # Generate report
        if args.output:
            report_path = Path(args.output)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = output_dir / f"tier{args.tier}_eval_{timestamp}.md"
        
        generate_report(results, report_path)


if __name__ == "__main__":
    main()
