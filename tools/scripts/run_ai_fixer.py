"""
AI Error Fixer - Integrated System
===================================

Complete end-to-end error resolution system:
1. Collects errors from markdownlint/flake8/pylint
2. Uses local AI models to fix errors intelligently
3. Runs in iterative batches with checkpointing
4. Generates detailed reports and logs

Quick Start:
    # Run everything automatically (collect + fix)
    python tools/scripts/run_ai_fixer.py

    # Use a specific model
    python tools/scripts/run_ai_fixer.py --model local:phi3.5

    # Dry run (no file modifications)
    python tools/scripts/run_ai_fixer.py --dry-run

    # Resume from previous run
    python tools/scripts/run_ai_fixer.py --resume

Architecture:
    1. error_collector.py - Gathers errors from linters
    2. ai_error_fixer.py - AI-powered fix application
    3. run_ai_fixer.py - Orchestrates the full workflow (this file)

Author: Integrated Error Resolution System
License: MIT
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from tools.llm.llm_client import LLMClient
    from tools.scripts.error_collector import ErrorCollector
except ImportError as e:
    print(f"ERROR: Could not import required modules: {e}")
    print("Make sure you're running from repo root with venv activated.")
    sys.exit(1)


class IntegratedAIFixer:
    """Orchestrates error collection and AI-powered fixing."""

    def __init__(
        self,
        model_name: str = "local:phi4",
        batch_size: int = 10,
        max_iterations: int = 50,
        dry_run: bool = False,
        checkpoint_dir: str = "ai_fixer_checkpoints",
    ):
        """Initialize integrated fixer.

        Args:
            model_name: AI model to use for fixing
            batch_size: Errors to process per batch
            max_iterations: Maximum number of fix iterations
            dry_run: Don't modify files
            checkpoint_dir: Directory for checkpoints and logs
        """
        self.model_name = model_name
        self.batch_size = batch_size
        self.max_iterations = max_iterations
        self.dry_run = dry_run

        # Create checkpoint directory
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(exist_ok=True)

        # Initialize LLM client
        self.llm_client = LLMClient()

        # Tracking
        self.iteration = 0
        self.total_fixed = 0
        self.total_processed = 0
        self.start_time = time.time()

    def collect_errors(self) -> List[Dict[str, Any]]:
        """Collect current errors from all linters.

        Returns:
            List of error dictionaries
        """
        print(f"\n🔍 Collecting errors (iteration {self.iteration})...")

        collector = ErrorCollector()
        collector.collect_all(
            markdown=True,
            python_flake8=True,
            python_pylint=False,  # Too slow for iterations
        )

        errors = collector.get_errors()
        print(f"   Found {len(errors)} total errors")

        return errors

    def build_fix_prompt(self, error: Dict[str, Any], context: str) -> str:
        """Build prompt for AI model to fix error.

        Args:
            error: Error dictionary
            context: File context around error

        Returns:
            Prompt string
        """
        return f"""Fix this linting error:

FILE: {error['file']}
LINE: {error['line']}
ERROR: {error['code']} - {error['message']}
SOURCE: {error['source']}

CONTEXT:
{context}

TASK:
1. Analyze the error and understand what's needed
2. Provide the corrected version of the problematic section
3. For Markdown blank line errors (MD022, MD032): Add blank lines before/after
4. For duplicate headings (MD024): Rename to be unique with context
5. For multiple H1 (MD025): Convert extra H1s to H2
6. For emphasis as heading (MD036): Convert to proper heading syntax
7. For missing code language (MD040): Add language identifier to fence
8. Preserve all formatting, indentation, and style

If you cannot safely fix this, respond with exactly: SKIP

CORRECTED OUTPUT:"""

    def read_context(self, file_path: str, line_num: int, context_lines: int = 5) -> str:
        """Read file context around error line.

        Args:
            file_path: Path to file
            line_num: Error line number (1-indexed)
            context_lines: Lines before/after to include

        Returns:
            Context string with line numbers
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            start = max(0, line_num - context_lines - 1)
            end = min(len(lines), line_num + context_lines)

            context_lines_list = []
            for i in range(start, end):
                marker = ">>> " if i == line_num - 1 else "    "
                context_lines_list.append(f"{marker}{i+1:4d}: {lines[i].rstrip()}")

            return '\n'.join(context_lines_list)

        except Exception as e:
            return f"[Error reading file: {e}]"

    def apply_fix(
        self,
        file_path: str,
        line_num: int,
        fixed_content: str,
        error_code: str,
    ) -> bool:
        """Apply fix to file.

        Args:
            file_path: Path to file
            line_num: Line to fix (1-indexed)
            fixed_content: New content
            error_code: Error code for context

        Returns:
            True if fix applied successfully
        """
        if self.dry_run:
            return True

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            idx = line_num - 1

            # Handle special cases based on error code
            if error_code.startswith('MD022') or error_code.startswith('MD032'):
                # Blank line errors - insert blank lines
                if '\n\n' in fixed_content:
                    # AI provided multiple lines
                    new_lines = fixed_content.split('\n')
                    lines = lines[:idx] + [l + '\n' for l in new_lines if l] + lines[idx:]
                else:
                    # Just add blank line before/after
                    if 'Below' in fixed_content or idx > 0:
                        lines.insert(idx + 1, '\n')  # Add after
                    if 'Above' in fixed_content or idx < len(lines):
                        lines.insert(idx, '\n')  # Add before
            else:
                # Direct replacement
                lines[idx] = fixed_content.rstrip() + '\n'

            with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
                f.writelines(lines)

            return True

        except Exception as e:
            print(f"      ❌ Error applying fix: {e}")
            return False

    def fix_error(self, error: Dict[str, Any]) -> bool:
        """Fix a single error using AI model.

        Args:
            error: Error dictionary

        Returns:
            True if fixed successfully
        """
        # Read context
        context = self.read_context(
            error['file'],
            error['line'],
            context_lines=5,
        )

        # Build prompt
        prompt = self.build_fix_prompt(error, context)

        try:
            # Get fix from AI
            response = self.llm_client.complete(
                prompt=prompt,
                model=self.model_name,
                max_tokens=300,
                temperature=0.1,
            )

            fixed = response.strip()

            # Check for skip
            if fixed == "SKIP" or not fixed:
                return False

            # Apply fix
            success = self.apply_fix(
                error['file'],
                error['line'],
                fixed,
                error['code'],
            )

            return success

        except Exception as e:
            print(f"      ❌ Model error: {e}")
            return False

    def process_batch(self, errors: List[Dict[str, Any]]) -> Dict[str, int]:
        """Process a batch of errors.

        Args:
            errors: List of errors to fix

        Returns:
            Dictionary with counts (fixed, skipped, failed)
        """
        print(f"\n{'='*60}")
        print(f"📦 BATCH {self.iteration}")
        print(f"   Model: {self.model_name}")
        print(f"   Errors: {len(errors)}")
        print(f"{'='*60}")

        results = {'fixed': 0, 'skipped': 0, 'failed': 0}

        for i, error in enumerate(errors, 1):
            file_name = Path(error['file']).name
            code = error['code']
            line = error['line']

            print(f"  [{i:2d}/{len(errors)}] {file_name}:{line} {code}...", end=' ')

            if self.fix_error(error):
                print("✅")
                results['fixed'] += 1
            else:
                print("⏭️")
                results['skipped'] += 1

        self.total_processed += len(errors)
        self.total_fixed += results['fixed']

        print(f"\n📊 Batch Results: ✅ {results['fixed']} fixed, ⏭️ {results['skipped']} skipped")

        return results

    def save_checkpoint(self, errors_remaining: int):
        """Save checkpoint of current state.

        Args:
            errors_remaining: Number of errors left
        """
        checkpoint = {
            'timestamp': datetime.now().isoformat(),
            'iteration': self.iteration,
            'model': self.model_name,
            'batch_size': self.batch_size,
            'total_processed': self.total_processed,
            'total_fixed': self.total_fixed,
            'errors_remaining': errors_remaining,
            'elapsed_seconds': time.time() - self.start_time,
        }

        checkpoint_file = self.checkpoint_dir / f"checkpoint_{self.iteration:03d}.json"
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, indent=2)

    def run(self):
        """Run the integrated fixing loop."""
        print("="*60)
        print("🤖 AI-POWERED ERROR RESOLUTION SYSTEM")
        print("="*60)
        print(f"Model: {self.model_name}")
        print(f"Batch Size: {self.batch_size}")
        print(f"Max Iterations: {self.max_iterations}")
        print(f"Dry Run: {self.dry_run}")
        print(f"Checkpoint Dir: {self.checkpoint_dir}")
        print("="*60)

        while self.iteration < self.max_iterations:
            self.iteration += 1

            # Collect current errors
            errors = self.collect_errors()

            if not errors:
                print("\n🎉 SUCCESS! All errors resolved!")
                break

            # Process batch
            batch = errors[:self.batch_size]
            results = self.process_batch(batch)

            # Save checkpoint
            self.save_checkpoint(len(errors) - results['fixed'])

            # Check progress
            if results['fixed'] == 0:
                print("\n⚠️  No errors fixed in this batch.")
                response = input("Continue? (y/n): ")
                if response.lower() != 'y':
                    break

            # Brief pause between iterations
            time.sleep(2)

        # Final report
        self.print_report()

    def print_report(self):
        """Print final report."""
        elapsed = time.time() - self.start_time

        print("\n" + "="*60)
        print("📈 FINAL REPORT")
        print("="*60)
        print(f"Model: {self.model_name}")
        print(f"Iterations: {self.iteration}")
        print(f"Total Processed: {self.total_processed}")
        print(f"Total Fixed: {self.total_fixed}")
        print(f"Success Rate: {(self.total_fixed/self.total_processed*100) if self.total_processed > 0 else 0:.1f}%")
        print(f"Time Elapsed: {elapsed/60:.1f} minutes")
        print(f"Checkpoints: {self.checkpoint_dir}")
        print("="*60)

        # Save final report
        report_file = self.checkpoint_dir / "final_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'model': self.model_name,
                'iterations': self.iteration,
                'total_processed': self.total_processed,
                'total_fixed': self.total_fixed,
                'success_rate': (self.total_fixed/self.total_processed*100) if self.total_processed > 0 else 0,
                'elapsed_seconds': elapsed,
            }, f, indent=2)

        print(f"\n📄 Report saved to {report_file}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Integrated AI error fixing system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with defaults (phi4, batch 10, auto-collect errors)
  python tools/scripts/run_ai_fixer.py

  # Use different model
  python tools/scripts/run_ai_fixer.py --model local:phi3.5

  # Larger batches
  python tools/scripts/run_ai_fixer.py --batch-size 20

  # Dry run (test without modifying files)
  python tools/scripts/run_ai_fixer.py --dry-run

  # More iterations
  python tools/scripts/run_ai_fixer.py --max-iterations 100
        """,
    )

    parser.add_argument(
        '--model',
        default='local:phi4',
        help='AI model to use (default: local:phi4)',
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
        default=50,
        help='Maximum iterations (default: 50)',
    )
    parser.add_argument(
        '--checkpoint-dir',
        default='ai_fixer_checkpoints',
        help='Checkpoint directory (default: ai_fixer_checkpoints)',
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Test run without modifying files',
    )

    args = parser.parse_args()

    # Create fixer
    fixer = IntegratedAIFixer(
        model_name=args.model,
        batch_size=args.batch_size,
        max_iterations=args.max_iterations,
        dry_run=args.dry_run,
        checkpoint_dir=args.checkpoint_dir,
    )

    # Run
    try:
        fixer.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        fixer.print_report()
        sys.exit(0)


if __name__ == '__main__':
    main()
