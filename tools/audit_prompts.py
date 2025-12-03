#!/usr/bin/env python3
"""
Prompt Library Auditor
Scans the prompt library (prompts/ folder only), runs validation on all prompt files,
and generates a migration report. Excludes agent files, instruction files, and other
non-prompt markdown files.
"""

import os
import json
import csv
import glob
import fnmatch
from pathlib import Path
from validators.prompt_validator import PromptValidationFramework

# =============================================================================
# FILE FILTERING - Only process actual prompt files
# =============================================================================

# Patterns to EXCLUDE from auditing (not prompt content files)
EXCLUDED_PATTERNS = [
    # Agent and instruction files (functional config, not prompts)
    '*.agent.md',
    '*.instructions.md',
    # Index and navigation files
    'index.md',
    'README.md',
    # GitHub/config directories
    '.github/**/*',
    # Documentation files (not prompts)
    'docs/**/*',
    'CONTRIBUTING.md',
    'SECURITY.md',
    'LICENSE',
    # Agent directories
    'agents/**/*',
    # Templates (meant to be copied, not used directly)
    'templates/**/*',
    # Archive
    '**/archive/**/*',
]

# Directories to EXCLUDE entirely
EXCLUDED_DIRS = {
    '.git',
    'node_modules',
    '__pycache__',
    'bin',
    'obj',
    '.venv',
    'venv',
    'docs',
    'agents',
    '.github',
    'templates',
    'archive',
}


def should_exclude_file(file_path: str, root_dir: str) -> bool:
    """
    Determine if a file should be excluded from auditing.
    
    Args:
        file_path: Absolute path to the file
        root_dir: Root directory being scanned
        
    Returns:
        True if the file should be excluded, False if it should be audited
    """
    try:
        rel_path = os.path.relpath(file_path, root_dir).replace('\\', '/')
    except ValueError:
        rel_path = os.path.basename(file_path)
    
    filename = os.path.basename(file_path)
    
    # Check filename patterns
    for pattern in EXCLUDED_PATTERNS:
        if fnmatch.fnmatch(filename, pattern):
            return True
        if fnmatch.fnmatch(rel_path, pattern):
            return True
    
    # Check if any parent directory is excluded
    path_parts = Path(file_path).parts
    if any(part in EXCLUDED_DIRS for part in path_parts):
        return True
    
    return False


def scan_directory(root_dir):
    """Recursively find all prompt .md files, excluding non-prompt files"""
    files = []
    for root, dirs, filenames in os.walk(root_dir):
        # Skip excluded directories entirely (modifies dirs in-place)
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        
        for filename in filenames:
            if filename.endswith('.md'):
                file_path = os.path.join(root, filename)
                if not should_exclude_file(file_path, root_dir):
                    files.append(file_path)
    return files

def audit_library(root_dir, output_file="audit_report.csv"):
    """Audit all prompts in the library (excludes non-prompt files)"""
    print(f"Scanning {root_dir}...")
    print(f"Excluding: agent files, instruction files, index.md, README.md, docs/, agents/, templates/")
    files = scan_directory(root_dir)
    print(f"Found {len(files)} prompt files to audit.")
    
    if not files:
        print("\nNo prompt files found. Make sure you're scanning a directory containing prompts.")
        print("This auditor only processes files in prompts/ folders, excluding:")
        print("  - *.agent.md, *.instructions.md")
        print("  - index.md, README.md")
        print("  - docs/, agents/, templates/, .github/ directories")
        return
    
    framework = PromptValidationFramework()
    results = []
    
    print("Running validation...")
    for i, file_path in enumerate(files):
        try:
            report = framework.validate_prompt(file_path)
            results.append({
                'file_path': file_path,
                'filename': os.path.basename(file_path),
                'overall_score': report.overall_score,
                'structure_score': report.structure_score,
                'metadata_score': report.metadata_score,
                'performance_score': report.performance_score,
                'security_score': report.security_score,
                'error_count': sum(1 for issue in report.issues if issue.level.value == 'error'),
                'warning_count': sum(1 for issue in report.issues if issue.level.value == 'warning')
            })
            if (i + 1) % 10 == 0:
                print(f"Processed {i + 1}/{len(files)} files...")
        except Exception as e:
            print(f"Error validating {file_path}: {e}")
            
    # Sort by score (ascending) to find worst files first
    results.sort(key=lambda x: x['overall_score'])
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['file_path', 'filename', 'overall_score', 'structure_score', 'metadata_score', 'performance_score', 'security_score', 'error_count', 'warning_count']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
        
    print(f"\nAudit complete. Report saved to {output_file}")
    
    # Print summary of worst offenders
    print("\nTop 10 Files Requiring Attention:")
    print(f"{'Score':<10} {'File':<50}")
    print("-" * 60)
    for r in results[:10]:
        print(f"{r['overall_score']:<10.1f} {r['filename']:<50}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Audit prompt library (excludes agent files, instructions, docs, etc.)",
        epilog="""
Examples:
  python audit_prompts.py prompts/
  python audit_prompts.py prompts/developers/ --output dev_audit.csv
  
This tool only audits actual prompt files. It automatically excludes:
  - *.agent.md files (GitHub Copilot agents)
  - *.instructions.md files (Copilot instructions)
  - index.md and README.md files
  - docs/, agents/, templates/, .github/ directories
        """
    )
    parser.add_argument("directory", help="Directory to scan (typically 'prompts/')")
    parser.add_argument("--output", default="audit_report.csv", help="Output CSV file")
    args = parser.parse_args()
    
    audit_library(args.directory, args.output)
