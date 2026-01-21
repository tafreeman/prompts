# Registry-Based Prompt Metadata

This document explains the hybrid approach for prompt metadata management.

## Overview

Following the pattern used by Anthropic Cookbook and OpenAI Cookbook, we use a **central registry** ([registry.yaml](../prompts/registry.yaml)) for metadata, keeping prompt files simple.

## Architecture

```
prompts/
├── registry.yaml          # ← All metadata lives here
├── agents/
│   └── code-review.md     # ← Minimal frontmatter (name, description only)
├── developers/
│   └── api-design.md
└── ...
```

## Comparison: Before vs After

### Before (Per-File Frontmatter)
```yaml
---
title: Code Review Assistant
shortTitle: Code Review
intro: An AI assistant that performs thorough code reviews...
type: how_to
difficulty: beginner
audience:
  - senior-engineer
  - junior-engineer
platforms:
  - claude
  - chatgpt
  - github-copilot
topics:
  - code-review
  - quality
author: Prompts Library Team
version: '2.0.0'
date: '2025-12-11'
governance_tags:
  - PII-safe
  - requires-human-review
dataClassification: internal
reviewStatus: approved
subcategory: code-review
framework_compatibility:
  openai: ">=1.0.0"
  anthropic: ">=0.8.0"
performance_metrics:
  complexity_rating: low
  token_usage_estimate: "1000-2000"
testing:
  framework: manual
  validation_status: passed
---
```

### After (Minimal Frontmatter)
```yaml
---
name: Code Review Assistant
description: An AI assistant that performs thorough code reviews
---
```

All other metadata moves to `registry.yaml`:
```yaml
- title: Code Review Assistant
  description: Performs thorough code reviews with constructive feedback
  path: developers/code-review-assistant.md
  categories: [Developers, Code Review]
  platforms: [claude, chatgpt, github-copilot]
  audience: [senior-engineer, junior-engineer]
  difficulty: beginner
  author: Prompts Library Team
  date: "2025-12-11"
  governance:
    classification: internal
    status: approved
    tags: [PII-safe, requires-human-review]
```

## Benefits

| Aspect | Per-File | Registry |
|--------|----------|----------|
| **File simplicity** | 15-20 fields | 2 fields |
| **Bulk updates** | Edit every file | Edit one file |
| **Consistency** | Easy to drift | Single source of truth |
| **Validation** | Per-file scripts | Schema validation |
| **Industry standard** | Unique | Matches Anthropic/OpenAI |

## Required Prompt Frontmatter (New)

Only 2 fields required in prompt files:

```yaml
---
name: Descriptive Name
description: One-line description of what this prompt does
---
```

For agent files (`.agent.md`), add tools:

```yaml
---
name: code_review_agent
description: Expert code reviewer
tools: [search, edit, problems]
---
```

## Registry Schema

See [registry-schema.json](../.github/registry-schema.json) for the full JSON Schema.

### Required Fields
- `title` - Display name
- `path` - File path from `prompts/`
- `categories` - At least one category
- `author` - Owner/team
- `date` - Last update (YYYY-MM-DD)

### Optional Fields
- `description` - Brief summary
- `platforms` - Target AI platforms
- `audience` - Target user roles
- `difficulty` - beginner/intermediate/advanced
- `technique` - Chain-of-thought, ReAct, etc.
- `governance` - Classification, status, tags
- `tags` - Free-form search tags
- `archived` - Boolean for soft-delete

## Migration Path

1. **Phase 1**: Create registry.yaml with existing prompts
2. **Phase 2**: Update validator to read from registry
3. **Phase 3**: Simplify prompt frontmatter
4. **Phase 4**: Update tooling (prompteval, etc.)

## Validation

```bash
# Validate registry against schema
python tools/validators/registry_validator.py

# Generate registry from existing frontmatter (migration helper)
python tools/scripts/migrate_to_registry.py --dry-run
```
