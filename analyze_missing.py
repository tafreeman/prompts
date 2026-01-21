#!/usr/bin/env python3
"""
Analyze what's missing: registry entries vs file sections.

This script compares:
1. Files that exist but aren't in registry.yaml
2. Files with missing H2 sections (Description, Prompt, Variables, Example)
3. Cross-reference to determine what needs to be added where
"""

import re
from pathlib import Path
import yaml

def load_registry():
    """Load registry.yaml and extract all paths."""
    registry_path = Path('prompts/registry.yaml')
    try:
        with registry_path.open('r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if not data or not isinstance(data, list):
            return {}
        
        # Create dict mapping path -> entry
        registry = {}
        for entry in data:
            if 'path' in entry:
                registry[entry['path']] = entry
        
        return registry
    except Exception as e:
        print(f"Error loading registry: {e}")
        return {}


def find_all_prompts():
    """Find all prompt markdown files."""
    prompts_dir = Path('prompts')
    md_files = []
    
    for md_file in prompts_dir.rglob('*.md'):
        if md_file.name in ('index.md', 'README.md'):
            continue
        
        rel_path = md_file.relative_to(prompts_dir)
        md_files.append(str(rel_path).replace('\\', '/'))
    
    return sorted(md_files)


def extract_sections(file_path):
    """Extract H2 sections from a markdown file."""
    try:
        content = Path(f'prompts/{file_path}').read_text(encoding='utf-8')
        sections = re.findall(r'^## (.+)$', content, re.MULTILINE)
        return [s.strip() for s in sections]
    except Exception as e:
        return []


def analyze_missing_sections(file_path):
    """Check which standard sections are missing from a file."""
    sections = extract_sections(file_path)
    sections_lower = [s.lower() for s in sections]
    
    required = {
        'Description': 'description' in sections_lower,
        'Prompt': 'prompt' in sections_lower,
        'Variables': 'variables' in sections_lower or 'variable' in sections_lower,
        'Example': any(x in sections_lower for x in ['example', 'example usage', 'usage']),
    }
    
    missing = [key for key, present in required.items() if not present]
    return missing, sections


def main():
    print("=" * 80)
    print("Registry vs File Content Analysis")
    print("=" * 80)
    print()
    
    # Load registry
    registry = load_registry()
    print(f"Registry entries: {len(registry)}")
    
    # Find all files
    all_files = find_all_prompts()
    print(f"Total prompt files: {len(all_files)}")
    print()
    
    # Compare
    in_registry = set(registry.keys())
    on_disk = set(all_files)
    
    missing_from_registry = on_disk - in_registry
    missing_from_disk = in_registry - on_disk
    
    print(f"Files missing from registry: {len(missing_from_registry)}")
    print(f"Registry entries with no file: {len(missing_from_disk)}")
    print()
    
    if missing_from_disk:
        print("⚠️  Registry entries pointing to missing files:")
        for path in sorted(missing_from_disk)[:10]:
            print(f"  - {path}")
        if len(missing_from_disk) > 10:
            print(f"  ... and {len(missing_from_disk) - 10} more")
        print()
    
    # Analyze section completeness
    print("=" * 80)
    print("Section Completeness Analysis")
    print("=" * 80)
    print()
    
    files_with_all_sections = 0
    files_missing_sections = 0
    section_stats = {
        'Description': 0,
        'Prompt': 0,
        'Variables': 0,
        'Example': 0,
    }
    
    incomplete_files = []
    
    for file_path in all_files:
        missing, actual_sections = analyze_missing_sections(file_path)
        
        if not missing:
            files_with_all_sections += 1
        else:
            files_missing_sections += 1
            incomplete_files.append((file_path, missing, actual_sections))
            
            for section in missing:
                section_stats[section] += 1
    
    print(f"Files with all required sections: {files_with_all_sections}")
    print(f"Files missing sections: {files_missing_sections}")
    print()
    
    print("Missing sections breakdown:")
    for section, count in sorted(section_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {section}: {count} files missing")
    print()
    
    # Show examples of incomplete files
    if incomplete_files:
        print("=" * 80)
        print("Sample of Files Missing Sections (first 10)")
        print("=" * 80)
        print()
        
        for file_path, missing, actual_sections in incomplete_files[:10]:
            in_reg = "✓" if file_path in registry else "✗"
            print(f"{in_reg} {file_path}")
            print(f"   Missing: {', '.join(missing)}")
            print(f"   Has: {', '.join(actual_sections[:5])}")
            if len(actual_sections) > 5:
                print(f"        ... and {len(actual_sections) - 5} more")
            print()
    
    # Summary
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print()
    print(f"1. {len(missing_from_registry)} files need to be added to registry.yaml")
    print(f"2. {files_missing_sections} files need standard sections added")
    print(f"3. Most commonly missing: {max(section_stats.items(), key=lambda x: x[1])[0]} ({max(section_stats.values())} files)")
    print()
    
    # Recommendation
    print("Recommendation:")
    print("  • Files NOT in registry.yaml: Add entries to registry.yaml")
    print("  • Files missing sections: Add ## Description, ## Prompt, ## Variables, ## Example")
    print("  • The validation expects both:")
    print("    1. Minimal frontmatter (name, description, type)")
    print("    2. Standard H2 sections in file body")
    print("  • Registry.yaml provides discovery metadata, files provide usage instructions")


if __name__ == '__main__':
    main()
