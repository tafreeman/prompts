#!/usr/bin/env python3
"""
Error Collector - Integration with markdownlint, flake8, pylint
================================================================

Collects linting errors from various sources and normalizes them into a
unified format for the AI error fixer.

Supported sources:
- markdownlint-cli (Markdown files)
- flake8 (Python files)
- pylint (Python files)
- VS Code Problems API (if available)

Usage:
    python tools/scripts/error_collector.py --output errors.json
    python tools/scripts/error_collector.py --markdown-only
    python tools/scripts/error_collector.py --python-only

Author: Error Collector System
License: MIT
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List


class ErrorCollector:
    """Collects and normalizes errors from various linting tools."""

    def __init__(self, repo_root: str = "."):
        """Initialize error collector.

        Args:
            repo_root: Root directory of repository
        """
        self.repo_root = Path(repo_root).resolve()
        self.errors: List[Dict[str, Any]] = []

    def collect_markdownlint_errors(self) -> int:
        """Collect errors from markdownlint-cli.

        Returns:
            Number of errors collected
        """
        print("🔍 Collecting Markdown errors...")

        # Check if markdownlint-cli is installed
        try:
            result = subprocess.run(
                ["markdownlint", "--version"],
                capture_output=True,
                text=True,
                cwd=self.repo_root,
            )
            if result.returncode != 0:
                print(
                    "  ⚠️  markdownlint not found. Install with: npm install -g markdownlint-cli"
                )
                return 0
        except FileNotFoundError:
            print(
                "  ⚠️  markdownlint not found. Install with: npm install -g markdownlint-cli"
            )
            return 0

        # Run markdownlint with JSON output
        # Note: Standard markdownlint-cli doesn't have --json, so we parse text output
        try:
            result = subprocess.run(
                [
                    "markdownlint",
                    "**/*.md",
                    "--ignore",
                    "node_modules",
                    "--ignore",
                    ".venv",
                    "--ignore",
                    "_archive",
                ],
                capture_output=True,
                text=True,
                cwd=self.repo_root,
            )

            # Parse output (format: file:line message)
            # Example: docs/README.md:89 MD022/blanks-around-headings Headings should be...
            lines = result.stdout.split("\n")
            count = 0

            for line in lines:
                if not line.strip():
                    continue

                # Parse format: filepath:line[:column] CODE/name message
                match = line.split(":", 2)
                if len(match) < 3:
                    continue

                file_path = match[0].strip()
                try:
                    line_num = int(match[1].strip())
                except ValueError:
                    continue

                rest = match[2].strip()

                # Extract error code and message
                parts = rest.split(" ", 1)
                if len(parts) < 2:
                    continue

                error_code = parts[0].strip()
                error_message = parts[1].strip()

                self.errors.append(
                    {
                        "file": str(self.repo_root / file_path),
                        "line": line_num,
                        "column": 1,
                        "code": error_code,
                        "message": error_message,
                        "source": "markdownlint",
                        "severity": "warning",
                    }
                )
                count += 1

            print(f"  ✅ Found {count} Markdown errors")
            return count

        except Exception as e:
            print(f"  ❌ Error running markdownlint: {e}")
            return 0

    def collect_flake8_errors(self) -> int:
        """Collect errors from flake8.

        Returns:
            Number of errors collected
        """
        print("🔍 Collecting flake8 errors...")

        # Check if flake8 is installed
        try:
            result = subprocess.run(
                [sys.executable, "-m", "flake8", "--version"],
                capture_output=True,
                text=True,
                cwd=self.repo_root,
            )
            if result.returncode != 0:
                print("  ⚠️  flake8 not found. Install with: pip install flake8")
                return 0
        except Exception:
            print("  ⚠️  flake8 not found. Install with: pip install flake8")
            return 0

        # Run flake8 with JSON output (requires flake8-json plugin or parse text)
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "flake8",
                    ".",
                    "--exclude=.venv,node_modules,_archive,.git",
                    "--max-line-length=120",
                ],
                capture_output=True,
                text=True,
                cwd=self.repo_root,
            )

            # Parse output (format: file:line:column: CODE message)
            # Example: tools/llm.py:42:80: E501 line too long (121 > 120 characters)
            lines = result.stdout.split("\n")
            count = 0

            for line in lines:
                if not line.strip():
                    continue

                # Parse format: filepath:line:column: CODE message
                match = line.split(":", 4)
                if len(match) < 5:
                    continue

                file_path = match[0].strip()
                try:
                    line_num = int(match[1].strip())
                    column = int(match[2].strip())
                except ValueError:
                    continue

                rest = match[4].strip()

                # Extract error code and message
                parts = rest.split(" ", 1)
                if len(parts) < 2:
                    continue

                error_code = parts[0].strip()
                error_message = parts[1].strip()

                self.errors.append(
                    {
                        "file": str(self.repo_root / file_path),
                        "line": line_num,
                        "column": column,
                        "code": error_code,
                        "message": error_message,
                        "source": "flake8",
                        "severity": "warning",
                    }
                )
                count += 1

            print(f"  ✅ Found {count} flake8 errors")
            return count

        except Exception as e:
            print(f"  ❌ Error running flake8: {e}")
            return 0

    def collect_pylint_errors(self) -> int:
        """Collect errors from pylint.

        Returns:
            Number of errors collected
        """
        print("🔍 Collecting pylint errors...")

        # Check if pylint is installed
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pylint", "--version"],
                capture_output=True,
                text=True,
                cwd=self.repo_root,
            )
            if result.returncode != 0:
                print("  ⚠️  pylint not found. Install with: pip install pylint")
                return 0
        except Exception:
            print("  ⚠️  pylint not found. Install with: pip install pylint")
            return 0

        # Run pylint with JSON output
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pylint",
                    ".",
                    "--output-format=json",
                    "--ignore=.venv,node_modules,_archive,.git",
                    "--max-line-length=120",
                ],
                capture_output=True,
                text=True,
                cwd=self.repo_root,
            )

            # Parse JSON output
            if result.stdout:
                pylint_errors = json.loads(result.stdout)
                count = 0

                for error in pylint_errors:
                    self.errors.append(
                        {
                            "file": str(self.repo_root / error.get("path", "")),
                            "line": error.get("line", 0),
                            "column": error.get("column", 0),
                            "code": error.get("message-id", "UNKNOWN"),
                            "message": error.get("message", ""),
                            "source": "pylint",
                            "severity": error.get("type", "warning"),
                        }
                    )
                    count += 1

                print(f"  ✅ Found {count} pylint errors")
                return count
            else:
                print("  ✅ No pylint errors found")
                return 0

        except Exception as e:
            print(f"  ❌ Error running pylint: {e}")
            return 0

    def collect_all(
        self,
        markdown: bool = True,
        python_flake8: bool = True,
        python_pylint: bool = False,
    ) -> int:
        """Collect errors from all sources.

        Args:
            markdown: Collect Markdown errors
            python_flake8: Collect flake8 errors
            python_pylint: Collect pylint errors

        Returns:
            Total number of errors collected
        """
        total = 0

        if markdown:
            total += self.collect_markdownlint_errors()

        if python_flake8:
            total += self.collect_flake8_errors()

        if python_pylint:
            total += self.collect_pylint_errors()

        return total

    def save(self, output_file: str):
        """Save collected errors to JSON file.

        Args:
            output_file: Path to output JSON file
        """
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "timestamp": Path(output_file).stem,
                    "total_errors": len(self.errors),
                    "errors": self.errors,
                },
                f,
                indent=2,
            )

        print(f"\n💾 Saved {len(self.errors)} errors to {output_file}")

    def get_errors(self) -> List[Dict[str, Any]]:
        """Get collected errors.

        Returns:
            List of error dictionaries
        """
        return self.errors


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Collect linting errors from various sources",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--output",
        "-o",
        default="collected_errors.json",
        help="Output JSON file (default: collected_errors.json)",
    )
    parser.add_argument(
        "--markdown-only",
        action="store_true",
        help="Only collect Markdown errors",
    )
    parser.add_argument(
        "--python-only",
        action="store_true",
        help="Only collect Python errors",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root directory (default: .)",
    )
    parser.add_argument(
        "--use-pylint",
        action="store_true",
        help="Also run pylint (slower, more strict)",
    )

    args = parser.parse_args()

    # Create collector
    collector = ErrorCollector(repo_root=args.repo_root)

    # Collect errors
    print("=" * 60)
    print("📊 ERROR COLLECTION SYSTEM")
    print("=" * 60)

    markdown = not args.python_only
    python = not args.markdown_only

    total = collector.collect_all(
        markdown=markdown,
        python_flake8=python,
        python_pylint=args.use_pylint and python,
    )

    print("\n" + "=" * 60)
    print(f"📈 COLLECTION COMPLETE: {total} errors found")
    print("=" * 60)

    # Save to file
    collector.save(args.output)

    print("\nNext: Run AI fixer with this error file")
    print(f"  python tools/scripts/ai_error_fixer.py --errors {args.output}")


if __name__ == "__main__":
    main()
