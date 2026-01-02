#!/usr/bin/env python3
"""
Dual Evaluation Scanner
=======================

Scans the prompts folder and runs BOTH evaluation methods on each prompt:
- evaluate_prompt(): Direct 6-criteria scoring
- evaluate_prompt_geval(): G-Eval with Chain-of-Thought

Both are FREE when using local ONNX models!

Usage:
    python tools/scan_prompts_dual.py
    python tools/scan_prompts_dual.py prompts/developers/
    python tools/scan_prompts_dual.py --limit 5
    python tools/scan_prompts_dual.py --output results.json
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))

from local_model import LocalModel


def find_prompts(folder: Path, limit: int = None) -> List[Path]:
    """Find all markdown prompt files in folder."""
    prompts = []
    
    for md_file in sorted(folder.rglob("*.md")):
        # Skip non-prompt files
        if md_file.name in ["README.md", "index.md", "CHANGELOG.md"]:
            continue
        if "_archive" in str(md_file) or "archive" in str(md_file).lower():
            continue
        if md_file.stat().st_size < 100:  # Skip tiny files
            continue
            
        prompts.append(md_file)
        
        if limit and len(prompts) >= limit:
            break
    
    return prompts


def scan_prompts(
    folder: Path,
    limit: int = None,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Scan prompts folder with both evaluation methods.
    
    Returns comprehensive results with scores from both methods.
    """
    prompts = find_prompts(folder, limit)
    
    if not prompts:
        print(f"No prompts found in {folder}")
        return {"error": "No prompts found"}
    
    print(f"\n{'='*70}")
    print(f"DUAL EVALUATION SCAN")
    print(f"{'='*70}")
    print(f"Folder: {folder}")
    print(f"Prompts found: {len(prompts)}")
    print(f"Method 1: evaluate_prompt() - Direct scoring")
    print(f"Method 2: evaluate_prompt_geval() - G-Eval Chain-of-Thought")
    print(f"{'='*70}\n")
    
    # Load model once
    print("Loading local model...")
    try:
        model = LocalModel(verbose=False)
        print(f"✓ Model loaded: {model.model_path}\n")
    except Exception as e:
        print(f"✗ Failed to load model: {e}")
        return {"error": str(e)}
    
    results = {
        "scan_date": datetime.now().isoformat(),
        "folder": str(folder),
        "total_prompts": len(prompts),
        "prompts": [],
        "summary": {
            "direct_avg": 0,
            "geval_avg": 0,
            "combined_avg": 0,
            "high_agreement": 0,  # Scores within 0.5
            "low_agreement": 0,   # Scores differ by > 1.0
        }
    }
    
    direct_scores = []
    geval_scores = []
    
    for i, prompt_path in enumerate(prompts, 1):
        relative_path = prompt_path.relative_to(folder.parent) if folder.parent in prompt_path.parents else prompt_path.name
        
        print(f"[{i}/{len(prompts)}] {relative_path}")
        
        try:
            content = prompt_path.read_text(encoding="utf-8")
            
            # Run direct evaluation
            if verbose:
                print(f"  → Running evaluate_prompt()...", end=" ", flush=True)
            direct_result = model.evaluate_prompt(content)
            direct_score = direct_result.get("overall", 0)
            if verbose:
                print(f"Score: {direct_score}")
            
            # Run G-Eval evaluation
            if verbose:
                print(f"  → Running evaluate_prompt_geval()...", end=" ", flush=True)
            geval_result = model.evaluate_prompt_geval(content)
            geval_score = geval_result.get("overall", 0)
            if verbose:
                print(f"Score: {geval_score}")
            
            # Calculate combined score
            valid_scores = [s for s in [direct_score, geval_score] if s > 0]
            combined_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0
            
            # Check agreement
            score_diff = abs(direct_score - geval_score)
            agreement = "high" if score_diff <= 0.5 else ("low" if score_diff > 1.0 else "medium")
            
            prompt_result = {
                "file": str(relative_path),
                "direct_score": direct_score,
                "geval_score": geval_score,
                "combined_score": round(combined_score, 2),
                "score_difference": round(score_diff, 2),
                "agreement": agreement,
                "direct_details": direct_result.get("scores", {}),
                "geval_details": {c: r.get("score", 0) for c, r in geval_result.get("criteria_results", {}).items()}
            }
            
            results["prompts"].append(prompt_result)
            
            if direct_score > 0:
                direct_scores.append(direct_score)
            if geval_score > 0:
                geval_scores.append(geval_score)
            
            if agreement == "high":
                results["summary"]["high_agreement"] += 1
            elif agreement == "low":
                results["summary"]["low_agreement"] += 1
            
            # Print summary for this prompt
            stars = "⭐" * int(combined_score)
            agreement_icon = "✓" if agreement == "high" else ("⚠" if agreement == "medium" else "✗")
            print(f"  → Combined: {combined_score} {stars} [{agreement_icon} {agreement} agreement]\n")
            
        except Exception as e:
            print(f"  ✗ Error: {e}\n")
            results["prompts"].append({
                "file": str(relative_path),
                "error": str(e)
            })
    
    # Calculate summary stats
    if direct_scores:
        results["summary"]["direct_avg"] = round(sum(direct_scores) / len(direct_scores), 2)
    if geval_scores:
        results["summary"]["geval_avg"] = round(sum(geval_scores) / len(geval_scores), 2)
    
    all_combined = [p.get("combined_score", 0) for p in results["prompts"] if p.get("combined_score", 0) > 0]
    if all_combined:
        results["summary"]["combined_avg"] = round(sum(all_combined) / len(all_combined), 2)
    
    # Print summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"Total prompts scanned: {len(prompts)}")
    print(f"Direct evaluation avg:  {results['summary']['direct_avg']}")
    print(f"G-Eval avg:             {results['summary']['geval_avg']}")
    print(f"Combined avg:           {results['summary']['combined_avg']}")
    print(f"\nAgreement between methods:")
    print(f"  High (within 0.5):    {results['summary']['high_agreement']}")
    print(f"  Low (diff > 1.0):     {results['summary']['low_agreement']}")
    print(f"{'='*70}\n")
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Scan prompts folder with dual evaluation methods"
    )
    parser.add_argument(
        "folder",
        nargs="?",
        default="prompts",
        help="Folder to scan (default: prompts)"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        help="Limit number of prompts to scan"
    )
    parser.add_argument(
        "--output", "-o",
        help="Save results to JSON file"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Less verbose output"
    )
    
    args = parser.parse_args()
    
    # Resolve folder path
    folder = Path(args.folder)
    if not folder.is_absolute():
        # Try relative to script location
        tools_dir = Path(__file__).parent
        repo_root = tools_dir.parent
        folder = repo_root / args.folder
    
    if not folder.exists():
        print(f"Error: Folder not found: {folder}")
        return 1
    
    # Run scan
    results = scan_prompts(folder, limit=args.limit, verbose=not args.quiet)
    
    # Save results if requested
    if args.output:
        output_path = Path(args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to: {output_path}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
