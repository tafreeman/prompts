#!/usr/bin/env python3
"""Report duplicate headings for manual review."""
import re
from pathlib import Path
from collections import defaultdict


def find_duplicate_headings(content: str) -> list:
    """Find duplicate headings in content."""
    heading_pattern = re.compile(r'^(#{1,6})\s+(.+?)$', re.MULTILINE)
    headings = defaultdict(list)
    
    for match in heading_pattern.finditer(content):
        level = len(match.group(1))
        text = match.group(2).strip()
        headings[text].append(level)
    
    duplicates = [text for text, levels in headings.items() if len(levels) > 1]
    return duplicates


def main():
    repo_root = Path(__file__).parent.parent.parent
    md_files = list(repo_root.glob('**/*.md'))
    excluded = {'.venv', 'node_modules', '.git', '__pycache__', '_archive'}
    md_files = [f for f in md_files if not any(e in f.parts for e in excluded)]
    
    report = []
    total_duplicates = 0
    
    for md_file in md_files:
        try:
            content = md_file.read_text(encoding='utf-8')
            duplicates = find_duplicate_headings(content)
            
            if duplicates:
                report.append({
                    'file': str(md_file.relative_to(repo_root)),
                    'duplicates': duplicates
                })
                total_duplicates += len(duplicates)
        except Exception as e:
            print(f"✗ Error processing {md_file.relative_to(repo_root)}: {e}")
    
    # Write report
    output_file = repo_root / 'DUPLICATE_HEADINGS_REPORT.md'
    with output_file.open('w', encoding='utf-8') as f:
        f.write('# Duplicate Headings Report\n\n')
        f.write(f'**Generated**: {Path(__file__).name}\n\n')
        f.write(f'Found **{len(report)}** files with **{total_duplicates}** duplicate headings\n\n')
        f.write('---\n\n')
        
        for item in sorted(report, key=lambda x: x['file']):
            f.write(f'## {item["file"]}\n\n')
            for dup in sorted(item['duplicates']):
                f.write(f'- `{dup}`\n')
            f.write('\n')
    
    print(f"\n{'='*60}")
    print(f"Report written to: {output_file}")
    print(f"Files with duplicates: {len(report)}")
    print(f"Total duplicate headings: {total_duplicates}")
    return 0


if __name__ == '__main__':
    exit(main())
