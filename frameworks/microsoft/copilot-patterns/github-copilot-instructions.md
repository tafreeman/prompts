---
title: "GitHub Copilot Instruction Patterns"
category: "frameworks"
subcategory: "microsoft"
technique_type: "copilot-instructions"
framework_compatibility:
  vscode: ">=1.80.0"
  github-copilot: ">=1.0.0"
difficulty: "beginner"
use_cases:
  - code-generation
  - code-review
  - refactoring
  - documentation
performance_metrics:
  productivity_improvement: "30-50%"
  accuracy_improvement: "20-30%"
version: "1.0.0"
author: "AI Research Team"
last_updated: "2025-11-23"
tags:
  - github-copilot
  - vscode
  - copilot-instructions
  - workspace
---

# GitHub Copilot Instruction Patterns

## Purpose

Leverage GitHub Copilot's workspace instructions feature (`.github/copilot-instructions.md`) to provide persistent context and coding standards to Copilot across your entire project.

## Overview

GitHub Copilot reads a special file (`.github/copilot-instructions.md`) in your repository root to understand project-specific context, coding standards, and patterns. This ensures consistent, high-quality suggestions aligned with your codebase.

## Instruction File Structure

### Basic Template

```markdown
# Copilot Instructions for [Project Name]

## Project Context

- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Purpose**: Prompt engineering toolkit and repository

## Coding Standards

### Python Style

- Use type hints for all function signatures
- Follow PEP 8 strictly
- Maximum line length: 100 characters
- Use dataclasses for data structures
- Prefer f-strings for formatting

### Documentation

- All public functions must have docstrings (Google style)
- Include usage examples in docstrings
- Use meaningful variable names (no abbreviations)

### Error Handling

- Use specific exception types, not bare `except:`
- Always log errors with context
- Validate inputs at function boundaries

## Project-Specific Patterns

### Prompt Templates

When creating prompt templates:

- Use YAML frontmatter for metadata
- Include `title`, `category`, `difficulty`, `use_cases`
- Provide concrete usage examples
- Document performance characteristics

### Validation

- All prompts must pass `tools/validators/prompt_validator.py`
- Minimum validation score: 80/100
- Include metadata schema compliance checks

## File Organization

- Prompts: `techniques/[category]/[pattern]/`
- Tools: `tools/[validators|generators|benchmarks]/`
- Examples: `examples/[notebooks|case-studies]/`

## Common Tasks

### Creating a New Prompt Template

1. Create directory: `techniques/[category]/[pattern-name]/`
2. Add `[pattern-name].md` with YAML frontmatter
3. Include prompt template, usage examples, and implementation code
4. Validate with: `python tools/validators/prompt_validator.py [file]`

### Adding Framework Integration

1. Create file in `frameworks/[framework-name]/`
2. Follow existing patterns (see `frameworks/langchain/` for reference)
3. Include SDK-specific code examples
4. Document compatibility versions
```

## VS Code Workspace Settings

Create `.vscode/settings.json` to enhance Copilot's understanding:

```json
{
	"github.copilot.enable": {
		"*": true,
		"yaml": true,
		"markdown": true,
		"plaintext": false
	},
	"github.copilot.editor.enableAutoCompletions": true,
	"github.copilot.advanced": {
		"debug.overrideEngine": "gpt-4",
		"debug.testOverrideProxyUrl": "",
		"debug.overrideProxyUrl": ""
	},
	"files.associations": {
		"*.copilot": "markdown",
		"*copilot-instructions.md": "markdown"
	},
	"python.analysis.typeCheckingMode": "strict",
	"python.linting.enabled": true,
	"python.linting.pylintEnabled": true,
	"python.formatting.provider": "black",
	"editor.formatOnSave": true,
	"[python]": {
		"editor.defaultFormatter": "ms-python.black-formatter",
		"editor.codeActionsOnSave": {
			"source.organizeImports": true
		}
	},
	"[markdown]": {
		"editor.wordWrap": "on",
		"editor.quickSuggestions": {
			"comments": "on",
			"strings": "on",
			"other": "on"
		}
	}
}
```

## Inline Instructions with Comments

Use special comments to guide Copilot inline:

```python
# Copilot: Generate a function that validates prompt metadata against schema
# Requirements:
# - Accept metadata dict and schema dict as parameters
# - Return ValidationResult with score and errors list
# - Use pydantic for validation if available
# - Handle missing required fields gracefully

def validate_metadata(metadata: Dict, schema: Dict) -> ValidationResult:
    # Copilot will generate implementation here
    pass
```

## Chat Participants for Context

When using Copilot Chat, leverage workspace context:

```
@workspace How do I create a new reflexion pattern following our conventions?

@workspace /explain the prompt validation flow

@workspace /fix the metadata schema validation in this file

@workspace /tests Generate unit tests for the ContextOptimizer class
```

## Best Practices

1. **Keep Instructions Updated**: Update `.github/copilot-instructions.md` as patterns evolve.
2. **Be Specific**: Provide concrete examples, not vague guidance.
3. **Use Structured Format**: Use headers, lists, and code blocks for clarity.
4. **Include Anti-Patterns**: Tell Copilot what NOT to do (e.g., "Don't use `eval()`").
5. **Version Constraints**: Specify exact versions for dependencies to avoid compatibility issues.

## Example: Project-Specific Instruction File

```markdown
# Copilot Instructions: Prompt Engineering Toolkit

## Core Principles

- **Validation First**: Every prompt must be validated before commit
- **Metadata Complete**: No prompt without full YAML frontmatter
- **Examples Required**: All patterns must include working code examples
- **Framework Agnostic**: Core patterns should work across LangChain, Anthropic, OpenAI

## Avoid These Patterns

- ❌ Hardcoded API keys (use environment variables)
- ❌ Prompts without metadata
- ❌ Code examples without error handling
- ❌ Using `print()` for logging (use `logging` module)

## When Generating Prompts

- ✅ Start with YAML frontmatter (title, category, difficulty, use_cases, etc.)
- ✅ Include a "Purpose" section explaining the pattern
- ✅ Provide a template with {{placeholder}} syntax
- ✅ Show a complete usage example
- ✅ Add Python implementation code
- ✅ Link to related patterns

## Testing

Run validation before committing:
\`\`\`bash
python tools/validators/prompt_validator.py path/to/prompt.md
\`\`\`
```

## Related Patterns

- [Anthropic Claude Patterns](../anthropic/claude_patterns.py)
- [OpenAI Integration](../openai/openai_utilities.py)
