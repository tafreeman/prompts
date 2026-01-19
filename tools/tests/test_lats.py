#!/usr/bin/env python3
"""
Quick LATS Test - Test the LATS automation on a single prompt
"""

import sys
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parents[2]))

from tools.scripts.run_lats_improvement import evaluate_prompt_with_lats, load_lats_evaluator

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Test LATS evaluator on a single prompt")
    parser.add_argument("prompt_file", help="Path to prompt file")
    parser.add_argument("--model", default="gh:gpt-4.1", help="Model to use")
    parser.add_argument("--threshold", type=float, default=80.0, help="Quality threshold")
    parser.add_argument("--max-iterations", type=int, default=5, help="Max iterations")
    
    args = parser.parse_args()
    
    prompt_path = Path(args.prompt_file)
    if not prompt_path.exists():
        print(f"Error: File not found: {prompt_path}")
        return 1
    
    print("Loading LATS evaluator...")
    evaluator = load_lats_evaluator()
    
    print(f"\nTesting on: {prompt_path.name}\n")
    
    result = evaluate_prompt_with_lats(
        prompt_path=prompt_path,
        evaluator_template=evaluator,
        model=args.model,
        threshold=args.threshold,
        max_iterations=args.max_iterations,
        verbose=True,
    )
    
    print(f"\n{'='*60}")
    print("FINAL RESULT:")
    print(f"  File: {result.prompt_file}")
    print(f"  Initial Score: {result.initial_score:.1f}%")
    print(f"  Final Score: {result.final_score:.1f}%")
    print(f"  Improvement: +{result.improvement:.1f}%")
    print(f"  Iterations: {result.iterations}")
    print(f"  Threshold Met: {'✅ YES' if result.threshold_met else '❌ NO'}")
    print(f"  Duration: {result.duration_seconds:.1f}s")
    
    if result.key_changes:
        print(f"\n  Key Changes:")
        for i, change in enumerate(result.key_changes[:5], 1):
            print(f"    {i}. {change}")
    
    print(f"{'='*60}\n")
    
    return 0 if result.threshold_met else 1

if __name__ == "__main__":
    sys.exit(main())
