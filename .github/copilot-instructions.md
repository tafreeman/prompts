# GitHub Copilot Instructions for Prompts Library

## Repository Overview

This is a community-driven prompt library designed for diverse users—from developers to business professionals. The repository provides well-organized, reusable prompts for AI/LLM interactions across various use cases.

## Working with Copilot

### What Copilot Should Do
When assigned to an issue or PR, Copilot should:
- Add new prompt files following the established template and format
- Update existing prompts to improve clarity, examples, or fix errors
- Enhance documentation for better user understanding
- Fix typos, broken links, or formatting issues
- Ensure all prompts meet quality standards before submission
- Make minimal, focused changes that directly address the issue

### What Copilot Should NOT Do
- Do not modify or delete working prompt files unless specifically requested
- Do not change the repository structure without explicit approval
- Do not add build tools, linters, or testing frameworks (this is a documentation-only repo)
- Do not create prompts outside the established categories without discussion
- Do not make sweeping changes across multiple prompts in a single PR
- Do not add dependencies or executable code

### Task Scoping Guidelines
- Each task should focus on a single prompt or related set of prompts
- New prompts should be complete with all required sections
- Updates should be incremental and reviewable
- Documentation changes should maintain existing tone and style
- Always validate that changes align with repository goals

## Repository Structure

```
prompts/
├── prompts/              # Main prompt collection
│   ├── developers/       # Technical & coding prompts
│   ├── business/         # Business analysis & strategy prompts
│   ├── creative/         # Content creation & marketing prompts
│   ├── analysis/         # Data analysis & research prompts
│   └── system/           # System-level AI agent prompts
├── templates/            # Reusable prompt templates
├── examples/             # Example usage and outputs
├── docs/                 # Documentation and guides
└── .github/             # GitHub configuration and workflows
```

## File Naming Conventions

- Use lowercase filenames with hyphens for word separation
- Examples: `code-review-assistant.md`, `marketing-email-generator.md`
- Avoid: `prompt1.md`, `MyPrompt.md`, spaces in filenames

## Prompt File Format

All prompts MUST follow this standard structure with YAML frontmatter:

```markdown
---
title: "Descriptive Prompt Title"
category: "developers|business|creative|analysis|system"
tags: ["tag1", "tag2", "tag3"]
author: "Author Name"
version: "1.0"
date: "YYYY-MM-DD"
difficulty: "beginner|intermediate|advanced"
---

# Prompt Title

## Description
Brief description of what this prompt does and when to use it.

## Use Cases
- Use case 1
- Use case 2
- Use case 3

## Prompt

[The actual prompt text goes here]

## Variables
- `[variable1]`: Description of what to replace this with
- `[variable2]`: Description of what to replace this with

## Example Usage

**Input:**
```
Example of the prompt with real values
```

**Output:**
```
Example of expected output
```

## Tips
- Tip 1 for better results
- Tip 2 for customization
```

## YAML Frontmatter Requirements

### Required Fields
- `title`: Clear, descriptive title in title case
- `category`: Must be one of: developers, business, creative, analysis, system
- `tags`: Array of relevant tags (minimum 3, maximum 10)
- `author`: Author's name or GitHub username
- `version`: Semantic versioning (e.g., "1.0", "1.1", "2.0")
- `date`: ISO format (YYYY-MM-DD)
- `difficulty`: Must be one of: beginner, intermediate, advanced

### Tag Guidelines
- Use lowercase, hyphenated tags
- Include category-specific tags: `code-generation`, `debugging`, `testing`, `analysis`, `strategy`, etc.
- Include technology tags when relevant: `python`, `javascript`, `react`, etc.
- Include skill level: `beginner`, `intermediate`, or `advanced`

## Quality Standards

All prompts must:
- ✅ Include complete YAML frontmatter with all required fields
- ✅ Have clear, specific descriptions
- ✅ Provide at least 2-3 use cases
- ✅ Include example usage with input and output
- ✅ Define all variables used in the prompt
- ✅ Provide practical tips for better results
- ✅ Be tested and validated before submission
- ✅ Use professional, unbiased language
- ✅ Follow consistent formatting

## Version Management

When updating existing prompts:
- **Minor improvements** (1.0 → 1.1): Typo fixes, clarity improvements, additional examples
- **Major changes** (1.0 → 2.0): Significant rewrites, structural changes
- Update the `version` field in YAML frontmatter
- Update the `date` field to current date
- Add a `## Changelog` section at the bottom documenting changes

Example changelog:
```markdown
## Changelog

### Version 1.1 (2025-11-10)
- Improved clarity in prompt instructions
- Added additional example usage

### Version 1.0 (2025-10-15)
- Initial version
```

## Category Placement Guidelines

### developers/
Technical and coding-related prompts:
- Code generation and review
- Debugging and testing
- Architecture and design
- Documentation
- Refactoring

### business/
Business analysis and strategy:
- Strategic planning
- Market research
- Financial analysis
- Reporting
- Decision-making support

### creative/
Content creation and marketing:
- Copywriting
- Marketing campaigns
- Social media content
- Storytelling
- Brand development

### analysis/
Data analysis and research:
- Data interpretation
- Research synthesis
- Statistical analysis
- Trend analysis
- Insight generation

### system/
System-level AI agent configuration:
- Role definitions
- Behavior guidelines
- General-purpose configurations
- System prompts

## Documentation

When making changes to documentation:
- Keep consistent with existing style and tone
- Update table of contents if adding new sections
- Ensure links are valid and working
- Follow markdown best practices
- Keep language clear and accessible

## Testing Expectations

Before submitting new or updated prompts:
1. Test the prompt with at least 2-3 different inputs
2. Verify outputs match expectations
3. Check for edge cases
4. Ensure all variables are clearly defined
5. Validate YAML frontmatter is properly formatted

## Building and Linting

This repository does not require build steps or linting tools as it contains markdown documentation only. However:
- Ensure markdown syntax is valid
- Check YAML frontmatter can be parsed
- Verify all links are functional
- Use markdown preview to check formatting

## Code Review Focus Areas

When reviewing changes:
1. **Frontmatter Validation**: All required YAML fields present and correctly formatted
2. **Content Quality**: Clear, specific, and useful prompts
3. **Examples**: Practical, realistic examples provided
4. **Consistency**: Follows repository format and style
5. **Categorization**: Prompt is in correct category folder
6. **File Naming**: Follows conventions (lowercase, hyphenated)
7. **Professional Tone**: Language is appropriate and unbiased

## Prohibited Content

Do NOT accept prompts that:
- ❌ Contain plagiarized content
- ❌ Include harmful, malicious, or unethical instructions
- ❌ Violate privacy or security principles
- ❌ Contain spam or promotional content
- ❌ Use biased or discriminatory language

## Contribution Workflow

1. Place new prompts in the appropriate category folder
2. Use the template from `templates/prompt-template.md`
3. Ensure all required fields are complete
4. Test the prompt thoroughly
5. Create descriptive commit messages
6. Reference related issues in PRs

## Commit Message Format

Use clear, descriptive commit messages:
- `Add: [prompt name]` for new prompts
- `Update: [prompt name]` for improvements
- `Fix: [issue description]` for bug fixes
- `Docs: [documentation change]` for documentation updates

Examples:
- `Add: SQL query optimization prompt for developers`
- `Update: Marketing email generator with more examples`
- `Fix: Typo in data analysis prompt YAML frontmatter`
- `Docs: Update README with new category information`

## Examples of Good Contributions

### ✅ Good: Adding a New Prompt
- Create file `prompts/developers/api-design-helper.md`
- Include complete YAML frontmatter with all required fields
- Provide clear description, use cases, and examples
- Test the prompt with real inputs before submission
- Follow the exact template structure

### ✅ Good: Improving an Existing Prompt
- Update version number from 1.0 to 1.1
- Add more detailed example in the Example Usage section
- Clarify variables with better descriptions
- Add a changelog entry explaining improvements

### ✅ Good: Fixing Documentation
- Correct typos in README.md
- Update broken links in documentation
- Improve clarity of instructions in CONTRIBUTING.md
- Add missing information to getting-started guide

### ❌ Avoid: Problematic Changes
- Renaming multiple files without discussion
- Deleting working prompts to "clean up"
- Adding new categories not in the structure
- Modifying YAML structure without approval
- Making changes across many unrelated files

## Additional Notes

- This is a documentation-only repository with no code execution
- Focus on content quality and consistency
- Prioritize user experience for diverse skill levels
- Maintain accessibility for both technical and non-technical users
- Follow existing patterns and conventions
- When in doubt, make smaller, more focused changes
- Always reference the issue you're addressing in commits and PRs
