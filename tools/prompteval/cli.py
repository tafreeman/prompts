#!/usr/bin/env python3
"""
PromptEval Unified CLI
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Optional

try:
    from tools.prompteval.config import EvalConfig, Tier
    from tools.prompteval.core import PromptEval
except ImportError:
    from .config import EvalConfig, Tier
    from .core import PromptEval

def main():
    parser = argparse.ArgumentParser(description="Unified Prompt Evaluation CLI")
    
    # Core arguments
    parser.add_argument("path", help="Path to prompt file or directory", nargs="?", default="prompts")
    parser.add_argument("--tier", "-t", type=int, default=2, help="Evaluation tier (0=Structural, 1=Local, 2=G-Eval)")
    parser.add_argument("--model", "-m", default="local:phi4mini", help="Model to use (e.g. local:phi4mini, gh:gpt-4o)")
    parser.add_argument("--threshold", type=float, default=70.0, help="Pass threshold score (0-100)")
    
    # Output and execution
    parser.add_argument("--output", "-o", help="Output file path (json/md)")
    parser.add_argument("--format", choices=["console", "json", "markdown"], default="console", help="Output format")
    parser.add_argument("--parallel", "-p", type=int, default=1, help="Number of parallel evaluations")
    parser.add_argument("--recursive", "-r", action="store_true", default=True, help="Scan recursively")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Validation
    target_path = Path(args.path)
    if not target_path.exists():
        print(f"Error: Path not found: {target_path}")
        sys.exit(1)
        
    # Configuration
    config = EvalConfig(
        tier=Tier(args.tier),
        threshold=args.threshold,
        model=args.model,
        path=target_path,
        output=Path(args.output) if args.output else None,
        output_format=args.format,
        verbose=args.verbose,
        parallel=args.parallel
    )
    
    if args.verbose:
        print(f"Configuration: {config}")
        
    # Execution
    engine = PromptEval(config)
    
    try:
        if target_path.is_file():
            results = [engine.evaluate_file(target_path)]
        else:
            results = engine.scan_directory(target_path)
    except Exception as e:
        print(f"Fatal Error: {e}")
        sys.exit(1)
        
    # Output handling
    if args.output:
        out_path = Path(args.output)
        with open(out_path, "w", encoding="utf-8") as f:
            data = [r.to_dict() for r in results]
            if len(data) == 1:
                data = data[0]
            json.dump(data, f, indent=2)
        print(f"Results saved to {out_path}")
        
    # Console summary
    if not args.output or args.verbose:
        passed = sum(1 for r in results if r.passed)
        print(f"\nSummary: {passed}/{len(results)} passed (Threshold: {config.threshold})")

if __name__ == "__main__":
    main()











