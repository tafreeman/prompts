#!/usr/bin/env python3
"""
Prompt Library Auditor
Scans the prompt library, runs validation on all files, and generates a migration report.
"""

import os
import json
import csv
import glob
from pathlib import Path
from validators.prompt_validator import PromptValidationFramework

def scan_directory(root_dir):
    """Recursively find all .md files"""
    files = []
    for root, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.md'):
                files.append(os.path.join(root, filename))
    return files

def audit_library(root_dir, output_file="audit_report.csv"):
    """Audit all prompts in the library"""
    print(f"Scanning {root_dir}...")
    files = scan_directory(root_dir)
    print(f"Found {len(files)} prompt files.")
    
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
    parser = argparse.ArgumentParser(description="Audit prompt library")
    parser.add_argument("directory", help="Directory to scan")
    parser.add_argument("--output", default="audit_report.csv", help="Output CSV file")
    args = parser.parse_args()
    
    audit_library(args.directory, args.output)
