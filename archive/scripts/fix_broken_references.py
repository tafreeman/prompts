"""
Comprehensive Broken References Fix Script
Fixes all path issues and creates WIP stub files for missing prompts
"""

import re
import sys
from pathlib import Path
from datetime import datetime

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Base directory
BASE_DIR = Path(r"d:\source\prompts")

# Template for WIP prompt files - matches templates/prompt-template.md structure
WIP_PROMPT_TEMPLATE = """---
title: {title}
shortTitle: {short_title}
intro: Work in progress - This prompt is currently under development.
type: how_to
difficulty: beginner
audience:
  - junior-engineer
  - senior-engineer
platforms:
  - github-copilot
  - claude
  - chatgpt
topics:
  - {category}
author: Prompts Library Team
version: '0.1.0'
date: '{date}'
governance_tags:
  - WIP
  - requires-review
dataClassification: internal
reviewStatus: draft
effectivenessScore: 0.0
---

# {title}

<!-- Score: ⭐⭐⭐ (0.0) - WIP - Not yet scored -->

**⚠️ WORK IN PROGRESS ⚠️**

This prompt is currently under development and not yet ready for production use.

## Description

[Provide a clear, concise description (2-3 sentences max) of what this prompt does and the problem it solves.]

## Prompt

```text
[Write your actual prompt here. Be specific, clear, and provide all necessary context.
 Use [VARIABLE_NAME] for values users should replace.]
```

## Variables

| Variable | Description |
|----------|-------------|
| `[VARIABLE_1]` | What to put here |
| `[VARIABLE_2]` | What this represents |

## Example

**Input:**

```text
Show a concrete example with real values filled in.
```

**Output:**

```text
Example of what the AI would generate.
```

## Tips

- Tip 1: How to customize for specific needs
- Tip 2: Common pitfalls to avoid
- Tip 3: Suggestions for better results

## Related Prompts

- [Related Prompt 1](../path/to/prompt.md)
- [Related Prompt 2](../path/to/prompt.md)

---

## Contributor Checklist

Before submitting, verify:

- [ ] `effectivenessScore` set (score with `tools/rubrics/prompt-scoring.yaml`)
- [ ] All required frontmatter fields populated
- [ ] Description is 2-3 sentences max
- [ ] Variables documented in table format
- [ ] Example has realistic input/output
- [ ] Tips are actionable (max 5)
- [ ] Related prompts are relevant (max 3)
"""

# Files to create with their metadata
MISSING_FILES = {
                 # Business prompts
                 "prompts/business/financial-modeling-expert.md": {
                 "title": "Financial Modeling Expert",
                 "short_title": "Financial Modeling",
                 "category": "business"
                 },
    "prompts/business/project-charter-creator.md": {
                                                    "title": "Project Charter Creator",
                                                    "short_title": "Project Charter",
                                                    "category": "business"
                                                    },
    "prompts/business/sales-strategy-consultant.md": {
                                                      "title": "Sales Strategy Consultant",
                                                      "short_title": "Sales Strategy",
                                                      "category": "business"
                                                      },

    # Creative prompts
    "prompts/creative/marketing-campaign-strategist.md": {
                                                          "title": "Marketing Campaign Strategist",
                                                          "short_title": "Marketing Campaign",
                                                          "category": "creative"
                                                          },

    # Developer prompts
    "prompts/developers/bug-finder.md": {
                                         "title": "Bug Finder and Fixer",
                                         "short_title": "Bug Finder",
                                         "category": "developers"
                                         },
    "prompts/developers/database-migration-specialist.md": {
                                                            "title": "Database Migration Specialist",
                                                            "short_title": "DB Migration",
                                                            "category": "developers"
                                                            },
    "prompts/developers/refactoring-specialist.md": {
                                                     "title": "Refactoring Specialist",
                                                     "short_title": "Refactoring",
                                                     "category": "developers"
                                                     },

    # Governance prompts
    "prompts/governance/cross-border-transfer-assessment.md": {
                                                               "title": "Cross-Border Transfer Assessment",
                                                               "short_title": "Cross-Border Transfer",
                                                               "category": "governance"
                                                               },

    # OSINT/SOCMINT prompts
    "prompts/socmint/attribution-analysis.md": {
                                                "title": "Attribution Analysis",
                                                "short_title": "Attribution",
                                                "category": "socmint"
                                                },
    "prompts/socmint/threat-intelligence.md": {
                                               "title": "Threat Intelligence Analysis",
                                               "short_title": "Threat Intelligence",
                                               "category": "socmint"
                                               },
    "prompts/socmint/timeline-reconstruction.md": {
                                                   "title": "Timeline Reconstruction",
                                                   "short_title": "Timeline",
                                                   "category": "socmint"
                                                   },
    "prompts/socmint/domain-investigation.md": {
                                                "title": "Domain Investigation",
                                                "short_title": "Domain OSINT",
                                                "category": "socmint"
                                                },
    "prompts/socmint/email-investigation.md": {
                                               "title": "Email Investigation",
                                               "short_title": "Email OSINT",
                                               "category": "socmint"
                                               },
    "prompts/socmint/phone-investigation.md": {
                                               "title": "Phone Investigation",
                                               "short_title": "Phone OSINT",
                                               "category": "socmint"
                                               },
    "prompts/socmint/username-investigation.md": {
                                                  "title": "Username Investigation",
                                                  "short_title": "Username OSINT",
                                                  "category": "socmint"
                                                  },
    "prompts/socmint/instagram-osint.md": {
                                           "title": "Instagram OSINT Investigation",
                                           "short_title": "Instagram OSINT",
                                           "category": "socmint"
                                           },
    "prompts/socmint/telegram-osint.md": {
                                          "title": "Telegram OSINT Investigation",
                                          "short_title": "Telegram OSINT",
                                          "category": "socmint"
                                          },

    # Workflow files
    "workflows/business-planning-blueprint.md": {
                                                 "title": "Business Planning Blueprint",
                                                 "short_title": "Business Blueprint",
                                                 "category": "workflow"
                                                 },
    "workflows/incident-response-playbook.md": {
                                                "title": "Incident Response Playbook",
                                                "short_title": "Incident Response",
                                                "category": "workflow"
                                                },

    # Template files
    "templates/roi-calculator.md": {
                                    "title": "ROI Calculator Template",
                                    "short_title": "ROI Calculator",
                                    "category": "template"
                                    },

    # Resource files
    "resources/osint_tool_evaluation.md": {
                                           "title": "OSINT Tool Evaluation",
                                           "short_title": "Tool Evaluation",
                                           "category": "resource"
                                           },
    "resources/osint_research_resources.md": {
                                              "title": "OSINT Research Resources",
                                              "short_title": "Research Resources",
                                              "category": "resource"
                                              },

    # Technique files
    "techniques/chain-of-thought-analysis.md": {
                                                "title": "Chain-of-Thought Analysis Technique",
                                                "short_title": "CoT Analysis",
                                                "category": "technique"
                                                },
    "techniques/react-knowledge-base.md": {
                                           "title": "ReAct Knowledge Base Pattern",
                                           "short_title": "ReAct KB",
                                           "category": "technique"
                                           },

    # Additional prompt files
    "prompts/advanced/reflection-data-pipeline-risk-review.md": {
                                                                 "title": "Reflection: Data Pipeline Risk Review",
                                                                 "short_title": "Pipeline Risk Review",
                                                                 "category": "advanced"
                                                                 },
    "prompts/governance/risk-assessment.md": {
                                              "title": "Risk Assessment Framework",
                                              "short_title": "Risk Assessment",
                                              "category": "governance"
                                              },
}

# Path replacements to apply across all markdown files
PATH_REPLACEMENTS = [
                     # Directory renames
                     (r'governance-compliance/', 'governance/'),
                     (r'advanced-techniques/', 'advanced/'),

                     # Specific file renames
                     (r'code-documentation-generator\.md', 'documentation-generator.md'),
                     (r'technical-documentation-specialist\.md', 'documentation-generator.md'),
                     (r'sql-query-optimizer-advanced\.md', 'sql-query-analyzer.md'),
                     (r'ai-risk-assessment\.md', 'ai-ml-privacy-risk-assessment.md'),
                     (r'vendor-risk-assessment\.md', 'vendor-security-review.md'),
                     (r'resource-planning-assistant\.md', 'resource-allocation-optimizer.md'),
                     (r'techniques/index\.md', 'techniques/README.md'),
                     (r'\./sdlc-blueprint\.md', './sdlc.md'),

                     # Specific path corrections
                     (r'docs/domain-schemas\.md', 'guides/domain-schemas.md'),
                     (r'\./domain-schemas\.md', '../guides/domain-schemas.md'),

                     # OSINT reference corrections
                     (r'socmint/socmint-investigator\.md', '../prompts/socmint/socmint-investigator.md'),
                     (r'techniques/react-osint-research\.md', '../prompts/advanced/osint-research-react.md'),

                     # Wrong directory corrections (system vs developers)
    (r'developers/cloud-architecture-consultant\.md', 'system/cloud-architecture-consultant.md'),
    (r'developers/solution-architecture-designer\.md', 'system/solution-architecture-designer.md'),
    (r'system/devops-pipeline-architect\.md', 'developers/devops-pipeline-architect.md'),
]

# File-specific complex replacements
FILE_SPECIFIC_FIXES = {
                       ".agent/workflows/coderev.md": [
                       # Fix over-corrected paths (too many../)
        (r'\.\./\.\./\.\./\.\./\.\./\.\./agents/', '../../agents/'),
        (r'\.\./\.\./\.\./\.\./\.\./\.\./prompts/', '../../prompts/'),
        (r'\.\./\.\./\.\./\.\./\.\./\.\./techniques/', '../../techniques/'),
    ],

    ".github/agents/AGENTS_GUIDE.md": [
                                       (r'(?<!\.\./)\.\./CONTRIBUTING\.md', '../../CONTRIBUTING.md'),
                                       (r'(?<!\.\./)\.\./docs/', '../../docs/'),
                                       ],

    ".github/agents/README.md": [
                                 (r'(?<!\.\./)\.\./CONTRIBUTING\.md', '../../CONTRIBUTING.md'),
                                 ],

    "techniques/README.md": [
                             (r'\.\./\.\./CONTRIBUTING\.md', '../CONTRIBUTING.md'),
                             ],

    "docs/reports/FULL_EVALUATION_REPORT.md": [
                                               (r'(?<!\.\./)(TOT_EVALUATION_REPORT\.md)', '../TOT_EVALUATION_REPORT.md'),
                                               (r'(?<!\.\./)(prompt-effectiveness-scoring-methodology\.md)', '../prompt-effectiveness-scoring-methodology.md'),
                                               ],

    "workflows/incident-response.md": [
                                       # security-code-auditor is in developers, not governance
                                       (r'\.\./prompts/governance/security-code-auditor\.md', '../prompts/developers/security-code-auditor.md'),
                                       ],

    "workflows/sdlc.md": [
                          # security-code-auditor is in developers, not governance
                          (r'\.\./prompts/governance/security-code-auditor\.md', '../prompts/developers/security-code-auditor.md'),
                          ],

   "templates/prompt-improvement-template.md": [
                                                # Fix resource-allocation-optimizer path
                                                (r'(?<!\.\./)(resource-allocation-optimizer\.md)', '../prompts/business/resource-allocation-optimizer.md'),
                                                ],

    "docs/create-osint-library-prompt.md": [
                                            # Fix relative paths for OSINT prompts that are in prompts/socmint
                                            (r'(?<!\.\./)(?<!prompts/)socmint/', '../prompts/socmint/'),
                                            (r'(?<!\.\./)(?<!prompts/)analysis/attribution-analysis\.md', '../prompts/socmint/attribution-analysis.md'),
                                            (r'(?<!\.\./)(?<!prompts/)analysis/threat-intelligence\.md', '../prompts/socmint/threat-intelligence.md'),
                                            (r'(?<!\.\./)(?<!prompts/)analysis/timeline-reconstruction\.md', '../prompts/socmint/timeline-reconstruction.md'),
                                            (r'(?<!\.\./)(?<!prompts/)investigation/', '../prompts/socmint/'),
                                            (r'(?<!\.\./)(?<!prompts/)techniques/', '../techniques/'),
                                            ],
}

# Workflow files - need to remove one ../
WORKFLOW_FILES = [
                  "workflows/business-planning.md",
                  "workflows/incident-response.md",
                  "workflows/sdlc.md",
                  "workflows/data-pipeline.md",
                  ]

WORKFLOW_REPLACEMENTS = [
                         (r'\.\./\.\./prompts/', '../prompts/'),
                         (r'\.\./\.\./CONTRIBUTING\.md', '../CONTRIBUTING.md'),
                         ]


def create_wip_file(file_path: Path, metadata: dict):
    """Create a WIP stub file with proper frontmatter"""
    today = datetime.now().strftime('%Y-%m-%d')

    content = WIP_PROMPT_TEMPLATE.format(
                                         title=metadata['title'],
                                         short_title=metadata['short_title'],
                                         category=metadata['category'],
                                         date=today
                                         )

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding='utf-8')
    print(f"✅ Created WIP file: {file_path.relative_to(BASE_DIR)}")


def apply_path_fixes(file_path: Path, content: str) -> str:
    """Apply all path fixes to file content"""
    original_content = content

    # Apply global replacements
    for pattern, replacement in PATH_REPLACEMENTS:
        content = re.sub(pattern, replacement, content)

    # Apply file-specific fixes
    rel_path = file_path.relative_to(BASE_DIR).as_posix()
    if rel_path in FILE_SPECIFIC_FIXES:
        for pattern, replacement in FILE_SPECIFIC_FIXES[rel_path]:
            content = re.sub(pattern, replacement, content)

    # Apply workflow-specific fixes
    if rel_path in WORKFLOW_FILES:
        for pattern, replacement in WORKFLOW_REPLACEMENTS:
            content = re.sub(pattern, replacement, content)

    # Return content and indicate if changed
    return content, content != original_content


def fix_all_markdown_files():
    """Fix all markdown files in the repository"""
    fixed_count = 0
    error_count = 0

    # Find all markdown files
    md_files = list(BASE_DIR.rglob("*.md"))

    print(f"\n🔍 Found {len(md_files)} markdown files to process...")

    for md_file in md_files:
        try:
            # Skip files in certain directories
            rel_path = md_file.relative_to(BASE_DIR).as_posix()
            if any(skip in rel_path for skip in ['node_modules', '.git', 'bin', 'obj']):
                continue

            # Read file
            content = md_file.read_text(encoding='utf-8')

            # Apply fixes
            new_content, changed = apply_path_fixes(md_file, content)

            if changed:
                # Write back
                md_file.write_text(new_content, encoding='utf-8')
                fixed_count += 1
                print(f"✏️  Fixed: {rel_path}")

        except Exception as e:
            error_count += 1
            print(f"❌ Error processing {md_file.relative_to(BASE_DIR)}: {e}")

    return fixed_count, error_count


def main():
    """Main execution function"""
    print("=" * 80)
    print("BROKEN REFERENCES FIX SCRIPT")
    print("=" * 80)

    # Step 1: Create missing WIP files
    print("\n📝 STEP 1: Creating WIP stub files for missing prompts...")
    print("-" * 80)

    created_count = 0
    for file_path, metadata in MISSING_FILES.items():
        full_path = BASE_DIR / file_path
        if not full_path.exists():
            create_wip_file(full_path, metadata)
            created_count += 1
        else:
            print(f"⏭️  Skipped (already exists): {file_path}")

    print(f"\n✅ Created {created_count} WIP files")

    # Step 2: Fix all path references
    print("\n🔧 STEP 2: Fixing path references in all markdown files...")
    print("-" * 80)

    fixed_count, error_count = fix_all_markdown_files()

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ WIP files created: {created_count}")
    print(f"✏️  Files with fixes applied: {fixed_count}")
    print(f"❌ Errors encountered: {error_count}")
    print("\n✨ All fixes completed!")
    print("\n📋 Next steps:")
    print("   1. Review the changes with: git dif")
    print("   2. Run the broken references checker again")
    print("   3. Commit the changes if everything looks good")
    print("=" * 80)


if __name__ == "__main__":
    main()
