#!/usr/bin/env python3
"""
Auto-fix common Markdown lint errors across the repository.

Fixes:
- MD031: Fenced code blocks should be surrounded by blank lines
- MD032: Lists should be surrounded by blank lines
- Trailing whitespace on blank lines
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple


def fix_md031_code_fences(lines: List[str]) -> Tuple[List[str], int]:
    """Fix MD031: Add blank lines around fenced code blocks."""
    fixed_lines = []
    changes = 0
    in_code_block = False
    fence_pattern = re.compile(r'^(\s*)```')
    
    for i, line in enumerate(lines):
        is_fence = fence_pattern.match(line)
        
        if is_fence:
            if not in_code_block:
                # Opening fence - ensure blank line before
                if i > 0 and fixed_lines and fixed_lines[-1].strip():
                    fixed_lines.append('')
                    changes += 1
                fixed_lines.append(line)
                in_code_block = True
            else:
                # Closing fence - add line first, then ensure blank after
                fixed_lines.append(line)
                in_code_block = False
                # Check if next line exists and needs blank line
                if i + 1 < len(lines) and lines[i + 1].strip():
                    # Will add blank line on next iteration
                    pass
        else:
            # Not a fence line
            if i > 0 and not in_code_block:
                # Check if previous line was closing fence
                prev_line = lines[i - 1] if i > 0 else ''
                if fence_pattern.match(prev_line) and line.strip():
                    # Previous was closing fence, current is non-empty, need blank
                    if not (fixed_lines and fixed_lines[-1] == ''):
                        fixed_lines.append('')
                        changes += 1
            fixed_lines.append(line)
    
    return fixed_lines, changes


def fix_md032_lists(lines: List[str]) -> Tuple[List[str], int]:
    """Fix MD032: Add blank lines around lists."""
    fixed_lines = []
    changes = 0
    list_pattern = re.compile(r'^(\s*)[-*+](\s+|$)')
    ordered_pattern = re.compile(r'^(\s*)\d+\.(\s+|$)')
    
    for i, line in enumerate(lines):
        is_list_item = list_pattern.match(line) or ordered_pattern.match(line)
        prev_line = lines[i - 1] if i > 0 else ''
        next_line = lines[i + 1] if i + 1 < len(lines) else ''
        
        prev_is_list = list_pattern.match(prev_line) or ordered_pattern.match(prev_line)
        next_is_list = list_pattern.match(next_line) or ordered_pattern.match(next_line)
        
        if is_list_item:
            # First item in list - need blank line before
            if i > 0 and not prev_is_list and prev_line.strip():
                if not (fixed_lines and fixed_lines[-1] == ''):
                    fixed_lines.append('')
                    changes += 1
            
            fixed_lines.append(line)
            
            # Last item in list - need blank line after
            if i + 1 < len(lines) and not next_is_list and next_line.strip():
                # Will add on next iteration
                pass
        else:
            # Not a list item
            if i > 0 and (list_pattern.match(prev_line) or ordered_pattern.match(prev_line)):
                # Previous was list item, current is non-empty non-list
                if line.strip() and not (fixed_lines and fixed_lines[-1] == ''):
                    fixed_lines.append('')
                    changes += 1
            fixed_lines.append(line)
    
    return fixed_lines, changes


def fix_trailing_whitespace(lines: List[str]) -> Tuple[List[str], int]:
    """Remove trailing whitespace from blank lines."""
    fixed_lines = []
    changes = 0
    
    for line in lines:
        if line.strip() == '' and line != '':
            # Blank line with whitespace
            fixed_lines.append('')
            changes += 1
        else:
            fixed_lines.append(line)
    
    return fixed_lines, changes


def fix_markdown_file(file_path: Path) -> Tuple[int, str]:
    """Fix a single Markdown file. Returns (num_changes, status_message)."""
    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.splitlines()
        
        total_changes = 0
        
        # Apply fixes in order
        lines, changes = fix_md031_code_fences(lines)
        total_changes += changes
        
        lines, changes = fix_md032_lists(lines)
        total_changes += changes
        
        lines, changes = fix_trailing_whitespace(lines)
        total_changes += changes
        
        if total_changes > 0:
            # Write back with original line endings preserved
            new_content = '\n'.join(lines)
            if content.endswith('\n'):
                new_content += '\n'
            file_path.write_text(new_content, encoding='utf-8')
            return total_changes, f"Fixed {total_changes} issues"
        else:
            return 0, "No changes needed"
    
    except Exception as e:
        return 0, f"Error: {str(e)}"


def main():
    """Main entry point."""
    repo_root = Path(__file__).parent.parent.parent
    
    # Find all Markdown files
    md_files = list(repo_root.glob('**/*.md'))
    
    # Exclude certain directories
    excluded_dirs = {'.venv', 'node_modules', '.git', '__pycache__', '_archive'}
    md_files = [
        f for f in md_files 
        if not any(excluded in f.parts for excluded in excluded_dirs)
    ]
    
    print(f"Found {len(md_files)} Markdown files to process")
    print("=" * 60)
    
    total_files_changed = 0
    total_changes = 0
    skipped = []
    
    for md_file in sorted(md_files):
        rel_path = md_file.relative_to(repo_root)
        changes, status = fix_markdown_file(md_file)
        
        if changes > 0:
            total_files_changed += 1
            total_changes += changes
            print(f"✓ {rel_path}: {status}")
        elif "Error" in status:
            skipped.append((rel_path, status))
            print(f"✗ {rel_path}: {status}")
    
    print("=" * 60)
    print(f"\nSummary:")
    print(f"  Files processed: {len(md_files)}")
    print(f"  Files changed: {total_files_changed}")
    print(f"  Total fixes applied: {total_changes}")
    
    if skipped:
        print(f"\nSkipped {len(skipped)} files due to errors:")
        for path, reason in skipped:
            print(f"  - {path}: {reason}")
    
    return 0 if not skipped else 1


if __name__ == '__main__':
    sys.exit(main())
