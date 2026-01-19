#!/usr/bin/env python3
"""Fix all auto-fixable lint issues in one pass."""
import re
from pathlib import Path


def fix_all_issues(content: str) -> tuple:
    """Apply all auto-fixes."""
    changes = {'tables': 0, 'headings': 0}
    
    # Fix table spacing
    pattern = re.compile(r'\|(-+)\|')
    content, changes['tables'] = pattern.subn(r'| \1 |', content)
    
    # Fix heading punctuation
    pattern = re.compile(r'^(#{1,6}\s+.+?)([.!?…]+)\s*$', re.MULTILINE)
    content, changes['headings'] = pattern.subn(r'\1', content)
    
    return content, changes


def main():
    repo_root = Path(__file__).parent.parent.parent
    md_files = list(repo_root.glob('**/*.md'))
    excluded = {'.venv', 'node_modules', '.git', '__pycache__', '_archive'}
    md_files = [f for f in md_files if not any(e in f.parts for e in excluded)]
    
    total = {'tables': 0, 'headings': 0, 'files': 0}
    
    for md_file in md_files:
        try:
            content = md_file.read_text(encoding='utf-8')
            new_content, changes = fix_all_issues(content)
            
            if sum(changes.values()) > 0:
                md_file.write_text(new_content, encoding='utf-8')
                total['tables'] += changes['tables']
                total['headings'] += changes['headings']
                total['files'] += 1
        except Exception as e:
            print(f"✗ Error: {md_file.relative_to(repo_root)}: {e}")
    
    print(f"\n{'='*60}")
    print(f"✓ Fixed {total['tables']} table spacing issues")
    print(f"✓ Fixed {total['headings']} heading punctuation issues")
    print(f"✓ Modified {total['files']} files")
    print(f"{'='*60}")
    return 0


if __name__ == '__main__':
    exit(main())
