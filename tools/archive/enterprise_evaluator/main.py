#!/usr/bin/env python3
"""
Enterprise Prompt Evaluator CLI
==============================

A standalone tool for evaluating GenAI prompts against the Enterprise Prompt Evaluation Framework.

Usage:
    python main.py path/to/prompt.md
    python main.py path/to/prompt.md --model gh:gpt-4o
    python main.py path/to/prompt.md --output results.json

Author: Prompts Library Team
"""

import argparse
import sys
import os
import json
import time
from pathlib import Path

# Add parent tools directory to path for imports
TOOLS_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(TOOLS_DIR))

# Import from main tools (not local duplicates)
from llm_client import LLMClient
from evaluator import EnterpriseEvaluator


def main():
    parser = argparse.ArgumentParser(
        description="Enterprise Prompt Evaluator - Evaluate prompts against enterprise standards"
    )
    
    # Primary argument: prompt file or directory
    parser.add_argument(
        "target",
        nargs="?",
        help="Path to prompt file (.md) or directory to evaluate"
    )
    
    # Model selection
    parser.add_argument(
        "--model", "-m",
        default="local:phi4mini",
        help="Model to use for evaluation (e.g., local:phi4mini, gh:gpt-4o, azure-foundry:phi4). Default: local:phi4mini"
    )
    
    # Output control
    parser.add_argument(
        "--output", "-o",
        help="Path to save JSON results"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    # Legacy/Utility flags
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if configured model is available"
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive generation mode (not evaluation)"
    )

    parser.add_argument(
        "--temperature",
        type=float,
        default=0.1,
        help="Temperature for generation (default: 0.1)"
    )

    args = parser.parse_args()

    # 1. Check Mode
    if args.check:
        print(f"Checking availability for model: {args.model}")
        try:
            # Try a simple generation to verify
            test_response = LLMClient.generate_text(args.model, "Test connection", max_tokens=10)
            if "Error" in test_response or "not found" in test_response.lower():
                print(f"❌ Verification failed: {test_response}")
                sys.exit(1)
            else:
                print(f"✅ Model '{args.model}' is available and responding.")
                print(f"Sample response: {test_response.strip()}")
                sys.exit(0)
        except Exception as e:
            print(f"❌ Error checking model: {e}")
            sys.exit(1)

    # 2. Interactive Mode
    if args.interactive:
        print(f"Interactive Mode ({args.model}) - Type 'exit' to quit.")
        client = LLMClient()
        while True:
            try:
                user_input = input("\n> ")
                if user_input.lower() in ('exit', 'quit'):
                    break
                
                response = LLMClient.generate_text(
                    args.model, 
                    user_input, 
                    temperature=args.temperature or 0.7
                )
                print("\n" + response)
            except KeyboardInterrupt:
                break
        sys.exit(0)

    # 3. Evaluation Mode (Default)
    if not args.target:
        parser.print_help()
        print("\nError: Please provide a target file or directory to evaluate.")
        sys.exit(1)

    target_path = Path(args.target)
    if not target_path.exists():
        print(f"Error: Target path not found: {target_path}")
        sys.exit(1)

    # Initialize Evaluator
    print(f"Initializing Evaluator with model: {args.model}...")
    try:
        evaluator = EnterpriseEvaluator(
            model_name=args.model,
            temperature=args.temperature
        )
    except Exception as e:
        print(f"Error initializing evaluator: {e}")
        sys.exit(1)

    results = []
    
    # Handle single file
    if target_path.is_file():
        print(f"Evaluating: {target_path.name}...")
        try:
            res = evaluator.evaluate_file(str(target_path))
            results.append(res)
            
            # Print localized summary
            print(f"\nResults for {target_path.name}:")
            print(f"  Score: {res['final_score']:.1f} - {res['performance_level']}")
            print("  Dimensions:")
            for dim in res['dimension_results']:
                print(f"    - {dim['id']:<25}: {dim['score']:>5.1f} ({dim['level']})")
                
        except Exception as e:
            print(f"Failed to evaluate {target_path.name}: {e}")

    # Handle directory
    elif target_path.is_dir():
        files = list(target_path.glob("*.md"))
        print(f"Found {len(files)} markdown files in {target_path}...")
        
        for i, file_path in enumerate(files, 1):
            print(f"[{i}/{len(files)}] Evaluating {file_path.name}...")
            try:
                res = evaluator.evaluate_file(str(file_path))
                results.append(res)
            except Exception as e:
                print(f"  Failed: {e}")

    # Output handling
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({"results": results}, f, indent=2)
        print(f"\nFull results saved to: {output_path}")
    else:
        # If no output file, just save a timestamped log for record keeping
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        log_file = f"eval_log_{timestamp}.jsonl"
        with open(log_file, 'w', encoding='utf-8') as f:
            for r in results:
                f.write(json.dumps(r) + "\n")
        print(f"\nDetailed log saved to: {log_file}")

if __name__ == "__main__":
    main()
