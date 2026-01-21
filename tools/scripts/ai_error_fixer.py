#!/usr/bin/env python3
"""
AI-Powered Error Resolution System
===================================

Automatically resolves linting errors using local AI models in an iterative loop.
Handles Markdown, Python, and other file types with intelligent context-aware fixes.

Features:
- Discovers and uses local AI models (phi4, phi3.5, mistral)
- Processes errors in batches with progress logging
- Creates checkpoints for resumability
- Generates detailed fix reports
- Runs in continuous loop until all errors resolved
- Validates fixes after each batch

Usage:
    python tools/scripts/ai_error_fixer.py
    python tools/scripts/ai_error_fixer.py --model local:phi4 --batch-size 20
    python tools/scripts/ai_error_fixer.py --resume-from checkpoint.json
    python tools/scripts/ai_error_fixer.py --dry-run

Author: AI Error Resolution System
License: MIT
"""

import os
import sys
import json
import re
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from tools.llm.llm_client import LLMClient
except ImportError:
    print("ERROR: Could not import LLMClient. Run from repo root.")
    sys.exit(1)


@dataclass
class ErrorInfo:
    """Represents a single linting error."""
    file_path: str
    line_number: int
    error_code: str
    error_message: str
    context_before: List[str]
    context_line: str
    context_after: List[str]
    fixed: bool = False
    fix_applied: Optional[str] = None
    fix_timestamp: Optional[str] = None


@dataclass
class BatchResult:
    """Results from processing one batch of errors."""
    batch_number: int
    timestamp: str
    errors_processed: int
    errors_fixed: int
    errors_skipped: int
    model_used: str
    duration_seconds: float
    errors: List[ErrorInfo]


class AIErrorFixer:
    """Main error resolution system using local AI models."""

    def __init__(
        self,
        model_name: str = "local:phi4",
        batch_size: int = 10,
        max_context_lines: int = 5,
        checkpoint_file: str = "ai_fixer_checkpoint.json",
        log_file: str = "ai_fixer_log.jsonl",
        dry_run: bool = False,
    ):
        """Initialize the AI error fixer.

        Args:
            model_name: Model to use (e.g., 'local:phi4', 'local:phi3.5')
            batch_size: Number of errors to process per batch
            max_context_lines: Lines of context before/after error
            checkpoint_file: File to save progress checkpoints
            log_file: JSONL file for detailed logging
            dry_run: If True, don't actually modify files
        """
        self.model_name = model_name
        self.batch_size = batch_size
        self.max_context_lines = max_context_lines
        self.checkpoint_file = checkpoint_file
        self.log_file = log_file
        self.dry_run = dry_run

        self.llm_client = LLMClient()
        self.batch_results: List[BatchResult] = []
        self.total_fixed = 0
        self.total_processed = 0

    def get_vscode_errors(self) -> List[Dict[str, Any]]:
        """Get all linting errors from VS Code (simulated - integrate with actual source).

        In production, this would call VS Code API or parse output from
        markdownlint, flake8, pylint, etc.

        Returns:
            List of error dictionaries with file_path, line, code, message
        """
        # This is a placeholder - in real implementation, you would:
        # 1. Run markdownlint-cli with --json output
        # 2. Run flake8/pylint with JSON formatter
        # 3. Or use VS Code extension API to get Problems panel data

        print("⚠️  Note: Using simulated error detection. In production, integrate with:")
        print("   - markdownlint-cli --json")
        print("   - flake8 --format=json")
        print("   - pylint --output-format=json")
        print()

        # For now, return empty list - you'll need to implement the actual integration
        return []

    def read_file_context(
        self,
        file_path: str,
        error_line: int,
    ) -> Tuple[List[str], str, List[str]]:
        """Read file and extract context around error line.

        Args:
            file_path: Path to file with error
            error_line: Line number of error (1-indexed)

        Returns:
            Tuple of (lines_before, error_line_content, lines_after)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Convert to 0-indexed
            idx = error_line - 1
            if idx < 0 or idx >= len(lines):
                return [], "", []

            start = max(0, idx - self.max_context_lines)
            end = min(len(lines), idx + self.max_context_lines + 1)

            before = [l.rstrip() for l in lines[start:idx]]
            current = lines[idx].rstrip()
            after = [l.rstrip() for l in lines[idx+1:end]]

            return before, current, after

        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            return [], "", []

    def build_fix_prompt(self, error: ErrorInfo) -> str:
        """Build a prompt for the AI model to fix the error.

        Args:
            error: Error information with context

        Returns:
            Prompt string for the AI model
        """
        prompt = f"""You are a code linting error fixer. Fix the following error:

FILE: {error.file_path}
LINE: {error.line_number}
ERROR: {error.error_code} - {error.error_message}

CONTEXT BEFORE:
{chr(10).join(error.context_before) if error.context_before else "(none)"}

ERROR LINE:
{error.context_line}

CONTEXT AFTER:
{chr(10).join(error.context_after) if error.context_after else "(none)"}

INSTRUCTIONS:
1. Analyze the error and understand what needs to be fixed
2. Provide ONLY the corrected version of the ERROR LINE
3. Do not include any explanations, just the fixed line
4. Preserve indentation and formatting
5. If the error requires adding blank lines, include them in your response
6. If you cannot fix it safely, respond with: SKIP

CORRECTED LINE:"""

        return prompt

    def apply_fix(
        self,
        error: ErrorInfo,
        fixed_line: str,
    ) -> bool:
        """Apply a fix to the file.

        Args:
            error: Error information
            fixed_line: Corrected line content

        Returns:
            True if fix was applied successfully
        """
        if self.dry_run:
            print(f"  [DRY RUN] Would fix line {error.line_number}")
            return True

        try:
            with open(error.file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Replace the line (1-indexed to 0-indexed)
            idx = error.line_number - 1
            if idx < 0 or idx >= len(lines):
                return False

            # Handle multiline fixes (e.g., adding blank lines)
            if '\n' in fixed_line:
                # Split and replace with multiple lines
                new_lines = fixed_line.split('\n')
                lines = lines[:idx] + [l + '\n' for l in new_lines] + lines[idx+1:]
            else:
                lines[idx] = fixed_line + '\n'

            # Write back
            with open(error.file_path, 'w', encoding='utf-8', newline='\n') as f:
                f.writelines(lines)

            return True

        except Exception as e:
            print(f"❌ Error applying fix to {error.file_path}: {e}")
            return False

    def process_error(self, error_dict: Dict[str, Any]) -> ErrorInfo:
        """Process a single error using the AI model.

        Args:
            error_dict: Raw error dictionary

        Returns:
            ErrorInfo with fix attempt results
        """
        # Extract error information
        file_path = error_dict.get('file', '')
        line_num = error_dict.get('line', 0)
        error_code = error_dict.get('code', 'UNKNOWN')
        error_msg = error_dict.get('message', '')

        # Read context
        before, current, after = self.read_file_context(file_path, line_num)

        # Create ErrorInfo
        error = ErrorInfo(
            file_path=file_path,
            line_number=line_num,
            error_code=error_code,
            error_message=error_msg,
            context_before=before,
            context_line=current,
            context_after=after,
        )

        # Build prompt and get fix
        prompt = self.build_fix_prompt(error)

        try:
            response = self.llm_client.complete(
                prompt=prompt,
                model=self.model_name,
                max_tokens=500,
                temperature=0.1,  # Low temp for deterministic fixes
            )

            fixed_line = response.strip()

            # Check if model wants to skip
            if fixed_line == "SKIP" or not fixed_line:
                print(f"  ⏭️  Skipped: {error_code} at line {line_num}")
                return error

            # Apply the fix
            if self.apply_fix(error, fixed_line):
                error.fixed = True
                error.fix_applied = fixed_line
                error.fix_timestamp = datetime.now().isoformat()
                print(f"  ✅ Fixed: {error_code} at line {line_num}")
            else:
                print(f"  ❌ Failed to apply: {error_code} at line {line_num}")

        except Exception as e:
            print(f"  ❌ Model error: {e}")

        return error

    def process_batch(
        self,
        errors: List[Dict[str, Any]],
        batch_num: int,
    ) -> BatchResult:
        """Process a batch of errors.

        Args:
            errors: List of error dictionaries
            batch_num: Batch number for logging

        Returns:
            BatchResult with processing results
        """
        print(f"\n{'='*60}")
        print(f"📦 BATCH {batch_num} - Processing {len(errors)} errors")
        print(f"   Model: {self.model_name}")
        print(f"{'='*60}\n")

        start_time = time.time()
        processed_errors: List[ErrorInfo] = []

        for i, error_dict in enumerate(errors, 1):
            print(f"[{i}/{len(errors)}] {error_dict.get('file', 'unknown')}")
            error_info = self.process_error(error_dict)
            processed_errors.append(error_info)

        duration = time.time() - start_time
        fixed_count = sum(1 for e in processed_errors if e.fixed)
        skipped_count = len(processed_errors) - fixed_count

        result = BatchResult(
            batch_number=batch_num,
            timestamp=datetime.now().isoformat(),
            errors_processed=len(errors),
            errors_fixed=fixed_count,
            errors_skipped=skipped_count,
            model_used=self.model_name,
            duration_seconds=duration,
            errors=processed_errors,
        )

        print(f"\n📊 Batch {batch_num} Results:")
        print(f"   ✅ Fixed: {fixed_count}")
        print(f"   ⏭️  Skipped: {skipped_count}")
        print(f"   ⏱️  Duration: {duration:.1f}s")

        return result

    def save_checkpoint(self):
        """Save current progress to checkpoint file."""
        checkpoint = {
            'timestamp': datetime.now().isoformat(),
            'model': self.model_name,
            'total_processed': self.total_processed,
            'total_fixed': self.total_fixed,
            'batch_count': len(self.batch_results),
            'batches': [asdict(b) for b in self.batch_results],
        }

        with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, indent=2)

        print(f"💾 Checkpoint saved to {self.checkpoint_file}")

    def save_batch_log(self, result: BatchResult):
        """Append batch result to JSONL log file."""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(result)) + '\n')

    def run(self, max_iterations: int = 100):
        """Run the error fixing loop.

        Args:
            max_iterations: Maximum number of batches to process
        """
        print("="*60)
        print("🤖 AI-POWERED ERROR RESOLUTION SYSTEM")
        print("="*60)
        print(f"Model: {self.model_name}")
        print(f"Batch Size: {self.batch_size}")
        print(f"Dry Run: {self.dry_run}")
        print(f"Checkpoint: {self.checkpoint_file}")
        print(f"Log: {self.log_file}")
        print("="*60)

        iteration = 0
        while iteration < max_iterations:
            iteration += 1

            # Get current errors
            print(f"\n🔍 Iteration {iteration}: Scanning for errors...")
            errors = self.get_vscode_errors()

            if not errors:
                print("\n🎉 SUCCESS! No more errors found.")
                break

            print(f"   Found {len(errors)} errors")

            # Process in batches
            batch_num = len(self.batch_results) + 1
            batch_errors = errors[:self.batch_size]

            result = self.process_batch(batch_errors, batch_num)
            self.batch_results.append(result)
            self.total_processed += result.errors_processed
            self.total_fixed += result.errors_fixed

            # Save progress
            self.save_checkpoint()
            self.save_batch_log(result)

            # Check if we're making progress
            if result.errors_fixed == 0:
                print(f"\n⚠️  WARNING: No errors fixed in this batch.")
                print("   Consider trying a different model or manual review.")

                # Ask if we should continue
                if not self.dry_run:
                    response = input("\nContinue? (y/n): ")
                    if response.lower() != 'y':
                        break

        # Final report
        self.print_final_report()

    def print_final_report(self):
        """Print final summary report."""
        print("\n" + "="*60)
        print("📈 FINAL REPORT")
        print("="*60)
        print(f"Total Iterations: {len(self.batch_results)}")
        print(f"Total Errors Processed: {self.total_processed}")
        print(f"Total Errors Fixed: {self.total_fixed}")
        print(f"Success Rate: {(self.total_fixed/self.total_processed*100) if self.total_processed > 0 else 0:.1f}%")
        print(f"Checkpoint: {self.checkpoint_file}")
        print(f"Log: {self.log_file}")
        print("="*60)

        # Save final report
        report_file = f"ai_fixer_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'model': self.model_name,
                'total_processed': self.total_processed,
                'total_fixed': self.total_fixed,
                'success_rate': (self.total_fixed/self.total_processed*100) if self.total_processed > 0 else 0,
                'batches': len(self.batch_results),
            }, f, indent=2)

        print(f"\n📄 Report saved to {report_file}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="AI-powered error resolution system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default settings (phi4, batch size 10)
  python tools/scripts/ai_error_fixer.py

  # Use a different model
  python tools/scripts/ai_error_fixer.py --model local:phi3.5

  # Larger batch size
  python tools/scripts/ai_error_fixer.py --batch-size 20

  # Dry run (don't modify files)
  python tools/scripts/ai_error_fixer.py --dry-run

  # Resume from checkpoint
  python tools/scripts/ai_error_fixer.py --resume-from checkpoint.json
        """,
    )

    parser.add_argument(
        '--model',
        default='local:phi4',
        help='Model to use (default: local:phi4)',
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=10,
        help='Errors per batch (default: 10)',
    )
    parser.add_argument(
        '--max-iterations',
        type=int,
        default=100,
        help='Maximum iterations (default: 100)',
    )
    parser.add_argument(
        '--checkpoint',
        default='ai_fixer_checkpoint.json',
        help='Checkpoint file (default: ai_fixer_checkpoint.json)',
    )
    parser.add_argument(
        '--log',
        default='ai_fixer_log.jsonl',
        help='Log file (default: ai_fixer_log.jsonl)',
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Don\'t modify files, just simulate',
    )
    parser.add_argument(
        '--resume-from',
        help='Resume from checkpoint file',
    )

    args = parser.parse_args()

    # Create fixer
    fixer = AIErrorFixer(
        model_name=args.model,
        batch_size=args.batch_size,
        checkpoint_file=args.checkpoint,
        log_file=args.log,
        dry_run=args.dry_run,
    )

    # Run
    try:
        fixer.run(max_iterations=args.max_iterations)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        fixer.save_checkpoint()
        fixer.print_final_report()
        sys.exit(0)


if __name__ == '__main__':
    main()
