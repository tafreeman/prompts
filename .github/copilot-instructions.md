# GitHub Copilot Instructions for `prompting` Prompt Library

> Audience: GitHub Copilot and similar AI coding assistants used by mid-level and senior engineers maintaining this prompt library.

## Overview

This repository contains a curated prompt library for .NET / C# / SQL Server / MuleSoft development. These instructions guide:

- Maintaining the intended folder and file structure
- Extending prompts using established metadata, format, and personas
- Keeping this repo content-first (not a generic code project)

---

## Repository Structure

```
prompting/
├── README.md                    # Brief description and docs link
├── .github/
│   └── copilot-instructions.md  # This file
├── dotnet-prompts/              # All prompt content
│   ├── developers/              # C#/.NET/SQL developer prompts
│   ├── integration/             # MuleSoft and integration prompts
│   ├── analysis/                # Analysis and triage prompts
│   ├── system/                  # System-level and architecture prompts
│   └── governance/              # Security/compliance prompts
├── docs/                        # Documentation
│   ├── PLAN.md                  # Overall improvement plan and catalog
│   ├── PROMPT_STANDARDS.md      # Required frontmatter and quality bar
│   ├── TODO-PROMPTS.md          # Backlog and status tracking
│   └── dotnet-prompt-library-design.md  # Long-form design and examples
└── instructions/                # Reusable instruction files
    ├── csharp-standards.instructions.md
    ├── project-structure.instructions.md
    ├── razor-standards.instructions.md
    ├── security-compliance.instructions.md
    └── sql-security.instructions.md
```

**Important**: If these folders don't exist, **create them and move existing files** into place rather than adding ad-hoc files at the root.

---

## Prompt File Conventions

All prompt files are **Markdown with YAML frontmatter** and follow a standard section layout.

### Required Frontmatter Structure

```yaml
---
title: "Descriptive Title"
category: "Developer|Integration|Analysis|System|Governance"
tags:
  - tag1
  - tag2
  - tag3
author: "Author Name"
version: "1.0.0"
date: "YYYY-MM-DD"
difficulty: "Beginner|Intermediate|Advanced"
platform: ".NET|Java|MuleSoft|SQL Server"

# Governance Metadata
governance_tags:
  - security-review
  - compliance
data_classification: "Public|Internal|Confidential|Restricted"
risk_level: "Low|Medium|High|Critical"
regulatory_scope:
  - SOC2
  - ISO27001
  - NIST
approval_required: true|false
approval_roles:
  - role1
  - role2
retention_period: "X years"
---
```

### Required Content Sections

Each prompt file must include these sections in order:

1. **`# <Title>`** - Matches `title` in frontmatter
2. **`## Description`** - Clear purpose and scope
3. **`## Use Cases`** - Bullet list of scenarios
4. **`## Prompt`** - The actual template with `[variable_name]` placeholders
5. **`## Variables`** - Table defining all placeholders
6. **`## Example Usage`** - Real-world examples with inputs/outputs
7. **`## Tips`** - Best practices and gotchas
8. **`## Related Prompts`** - Links to complementary prompts
9. **`## Changelog`** - Version history table

### Variable Syntax

Use **square brackets** for all template variables:

✅ **Correct**: `[csharp_code]`, `[database_name]`, `[user_role]`  
❌ **Incorrect**: `{csharp_code}`, `${database_name}`, `<user_role>`

---

## Personas and SDLC Alignment

Prompts are written for specific personas and software development lifecycle phases. See PLAN.md and TODO-PROMPTS.md for the complete catalog.

### Target Personas

- **Developer** (C#, .NET, SQL)
- **QA / Tester**
- **Functional / Business Analyst**
- **Architect**
- **Project Manager**
- **Security Engineer** (governance prompts)

### Persona Language in Prompts

Use explicit role framing in the `## Prompt` section:

```markdown
## Prompt

You are a Senior .NET Architect with expertise in cloud-native design patterns...

**Context:**

- [context_variable]

**Task:**
[task_description]

**Requirements:**

1. [requirement_1]
2. [requirement_2]
```

### Output Format Expectations

Unless a specific prompt overrides it, instruct AI assistants to respond using this structure:

1. **Summary paragraph** – ≤3 sentences capturing goal and constraints.
2. **Bullet list of actions or review findings** – ordered by impact.
3. **Code block examples** – ≤2 focused snippets with language tags.
4. **Fallback note** – what to do or explain if a requirement cannot be met.

---

## How to Modify or Extend the Library

### What This Repository Is

- ✅ A **prompt library** (Markdown documentation)
- ✅ **Templates** for AI-assisted development
- ✅ **Standards and best practices** documentation

### What This Repository Is NOT

- ❌ Application source code
- ❌ Compiled binaries or build artifacts
- ❌ CI/CD pipelines or deployment scripts

### Adding a New Prompt

1. **Choose the correct subfolder** under dotnet-prompts based on persona and category
2. **Copy an existing high-quality prompt** (e.g., `csharp-refactoring-assistant.md`) as a template
3. **Update all sections**:
   - Frontmatter (title, tags, governance metadata)
   - Description, use cases, and prompt text
   - Variables table with examples
   - Real-world example usage
4. **Add to backlog**: Create or update entry in TODO-PROMPTS.md
5. **Follow naming convention**: Use kebab-case (e.g., `sql-query-analyzer.md`)

#### Minimal Frontmatter Example

```yaml
applyTo: "**/*.cs"
audience: "Mid-level backend engineers"
intent: "Enforce secure async data access standards"
version: "2.0"
```

### Changing Standards or Structure

1. **Update PROMPT_STANDARDS.md first** (source of truth)
2. **Adjust affected prompts** to match new standards
3. **Update this file** if structure changes
4. **Document in changelog** of affected files

---

## Style and Tone

### Writing Guidelines

- **Concrete examples**: Use realistic .NET/SQL/MuleSoft scenarios
- **Model-agnostic**: Don't hard-code specific LLM names (e.g., "GPT-4", "Claude") unless the prompt explicitly requires it
- **Targeted snippets**: Short, focused code examples; avoid large copy-paste blocks
- **Professional tone**: Technical but accessible

### Code Examples

- Use proper syntax highlighting (` ```csharp`, ` ```sql`, ` ```xml`)
- Include comments for complex logic
- Show both before/after for refactoring prompts
- Provide realistic context (file paths, namespaces)

---

## What NOT to Do

### Prohibited Actions

❌ **Do not** introduce build tools, CI pipelines, or SDK-based code  
❌ **Do not** change governance fields casually (follow existing risk classifications)  
❌ **Do not** remove or drastically rewrite core docs (`PLAN.md`, `PROMPT_STANDARDS.md`, `TODO-PROMPTS.md`) without updating all three  
❌ **Do not** create new top-level folders without justification  
❌ **Do not** use curly braces `{}` or dollar signs `${}` for variables

### When Making Changes

⚠️ **High-risk prompts** (governance, security) require extra scrutiny  
⚠️ **Breaking changes** to prompt structure must be documented in changelog  
⚠️ **Deprecated prompts** should be marked in frontmatter, not deleted immediately

---

## Quick Reference: Example Prompts

| Prompt File                       | Category   | Persona           | Location                     |
| --------------------------------- | ---------- | ----------------- | ---------------------------- |
| `csharp-refactoring-assistant.md` | Developer  | C# Developer      | `dotnet-prompts/developers/` |
| `sql-query-analyzer.md`           | Developer  | SQL Developer     | `dotnet-prompts/developers/` |
| `dotnet-api-designer.md`          | Developer  | API Developer     | `dotnet-prompts/developers/` |
| `secure-dotnet-code-generator.md` | Governance | Security Engineer | `dotnet-prompts/governance/` |

---

## Version History

| Version | Date       | Changes                                          |
| ------- | ---------- | ------------------------------------------------ |
| 1.0.0   | 2024-XX-XX | Initial instructions                             |
| 1.1.0   | 2025-11-21 | Reformatted for readability and model processing |

---

## Support and Contributions

For questions or suggestions:

1. Check `docs/PROMPT_STANDARDS.md` for detailed guidelines
2. Review `docs/TODO-PROMPTS.md` for planned work
3. Follow the structure of existing high-quality prompts
4. Ensure all required sections and frontmatter are complete

**Remember**: This is a **documentation repository**. All contributions should enhance the prompt library, not turn it into an application codebase.
