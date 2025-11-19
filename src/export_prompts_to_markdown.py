#!/usr/bin/env python3
"""
Export all prompts from get_migrated_prompts_from_legacy_dataset() to individual markdown files.
"""
from load_prompts import get_migrated_prompts_from_legacy_dataset
import os
import re
from datetime import datetime

# Import the helper from load_prompts
import sys
sys.path.insert(0, os.path.dirname(__file__))


def slugify(text):
    """Convert title to a safe filename."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text


def extract_variables(template):
    """Extract [variable] placeholders from template."""
    return list(set(re.findall(r'\[([^\]]+)\]', template)))


def map_category_folder(category):
    """Map category to folder name."""
    mapping = {
        'Development': 'developers',
        'Business': 'business',
        'Analysis': 'analysis',
        'System': 'system',
        'Creative': 'creative'
    }
    return mapping.get(category, 'system')


def infer_difficulty(persona, use_case):
    """Infer difficulty level from persona/use_case."""
    if persona in ('Architect', 'Consultant'):
        return 'advanced'
    if persona in ('Developer', 'Project Manager'):
        if 'Architecture' in use_case or 'Strategy' in use_case:
            return 'advanced'
        return 'intermediate'
    return 'intermediate'


def generate_markdown(prompt):
    """Generate markdown content for a single prompt."""
    variables = extract_variables(prompt['template'])
    difficulty = infer_difficulty(prompt['persona'], prompt['use_case'])

    # Build frontmatter
    frontmatter = f"""---
title: "{prompt['title']}"
category: "{map_category_folder(prompt['category'])}"
tags: [{', '.join(f'"{tag.strip()}"' for tag in prompt['tags'].split(','))}]
author: "Prompts Library Team"
version: "1.0"
date: "{datetime.now().strftime('%Y-%m-%d')}"
difficulty: "{difficulty}"
---

# {prompt['title']}

## Description
{prompt['description']}

## Use Cases
- {prompt['use_case']} for {prompt['persona']} persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```
{prompt['template']}
```

## Variables
"""

    # Add variable documentation
    for var in sorted(variables):
        var_description = var.replace('_', ' ').title()
        frontmatter += f"- `[{var}]`: {var_description}\n"

    if not variables:
        frontmatter += "- This prompt uses fixed text with no customizable variables\n"

    # Add example usage
    frontmatter += f"""
## Example Usage

**Input:**
Replace the bracketed placeholders with your specific values, then use with Claude Sonnet 4.5 or Code 5.

**Output:**
The AI will provide a comprehensive response following the structured format defined in the prompt.

## Tips
- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

## Related Prompts
- Browse other {prompt['persona']} prompts in this category
- Check the {map_category_folder(prompt['category'])} folder for similar templates

## Changelog

### Version 1.0 ({datetime.now().strftime('%Y-%m-%d')})
- Initial version migrated from legacy prompt library
- Optimized for Claude Sonnet 4.5 and Code 5
"""

    return frontmatter


def main():
    """Export all migrated prompts to markdown files."""
    # Get all prompts
    prompts = get_migrated_prompts_from_legacy_dataset()

    # Base directory for prompts
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'prompts')

    print(f"Exporting {len(prompts)} prompts to markdown files...")
    print(f"Base directory: {base_dir}")

    created_count = 0
    skipped_count = 0

    for prompt in prompts:
        # Determine folder
        folder_name = map_category_folder(prompt['category'])
        folder_path = os.path.join(base_dir, folder_name)

        # Ensure folder exists
        os.makedirs(folder_path, exist_ok=True)

        # Generate filename
        filename = slugify(prompt['title']) + '.md'
        filepath = os.path.join(folder_path, filename)

        # Check if file already exists
        if os.path.exists(filepath):
            print(f"  ⚠️  Skipping (exists): {folder_name}/{filename}")
            skipped_count += 1
            continue

        # Generate markdown content
        markdown = generate_markdown(prompt)

        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown)

        print(f"  ✅ Created: {folder_name}/{filename}")
        created_count += 1

    print("\n✅ Export complete!")
    print(f"   Created: {created_count} files")
    print(f"   Skipped: {skipped_count} files (already exist)")
    print("\nNext steps:")
    print("  1. Review the generated markdown files in prompts/")
    print("  2. Run 'python load_prompts.py' to reload the database")
    print("  3. Start the app with 'python app.py' to see all prompts")


if __name__ == '__main__':
    main()
