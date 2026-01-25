---
name: GitHub Copilot Instruction Patterns
description: A prompt for github copilot instruction patterns tasks.
type: how_to
---
## Description

## Prompt

```text
# Copilot Instructions for [PROJECT_NAME]

## Project Context
- **Language**: [PRIMARY_LANGUAGE]
- **Framework**: [FRAMEWORK]
- **Purpose**: [PROJECT_DESCRIPTION]

## Coding Standards
[CODING_STANDARDS_LIST]

## Project-Specific Patterns
[PATTERN_DEFINITIONS]

## Avoid These Patterns
[ANTI_PATTERNS_LIST]
```

A prompt for github copilot instruction patterns tasks.

## Description

## Prompt

```text
# Copilot Instructions for [PROJECT_NAME]

## Project Context
- **Language**: [PRIMARY_LANGUAGE]
- **Framework**: [FRAMEWORK]
- **Purpose**: [PROJECT_DESCRIPTION]

## Coding Standards
[CODING_STANDARDS_LIST]

## Project-Specific Patterns
[PATTERN_DEFINITIONS]

## Avoid These Patterns
[ANTI_PATTERNS_LIST]
```

A prompt for github copilot instruction patterns tasks.


# GitHub Copilot Instruction Patterns

## Description

This pattern shows how to use GitHub Copilot's workspace instructions feature (`.github/copilot-instructions.md`) to provide persistent project context, coding standards, and patterns. Ensures consistent, high-quality AI suggestions aligned with your codebase conventions.

## Prompt

```text
# Copilot Instructions for [PROJECT_NAME]

## Project Context
- **Language**: [PRIMARY_LANGUAGE]
- **Framework**: [FRAMEWORK]
- **Purpose**: [PROJECT_DESCRIPTION]

## Coding Standards
[CODING_STANDARDS_LIST]

## Project-Specific Patterns
[PATTERN_DEFINITIONS]

## Avoid These Patterns
[ANTI_PATTERNS_LIST]
```

## Variables

| Variable                  | Description                       | Example                           |
| ------------------------- | --------------------------------- | --------------------------------- |
| `[PROJECT_NAME]`          | Name of your project              | "Prompt Engineering Toolkit"      |
| `[PRIMARY_LANGUAGE]`      | Main programming language         | "Python 3.11+"                    |
| `[FRAMEWORK]`             | Primary framework used            | "FastAPI"                         |
| `[CODING_STANDARDS_LIST]` | Bullet list of coding conventions | "Use type hints, Follow PEP 8..." |
| `[ANTI_PATTERNS_LIST]`    | Patterns to avoid                 | "❌ Hardcoded API keys"           |

## Example

**File**: `.github/copilot-instructions.md`

```markdown
# Copilot Instructions for API Service

## Project Context

- **Language**: TypeScript 5.0
- **Framework**: Express.js
- **Purpose**: REST API for user management

## Coding Standards

- Use async/await, not callbacks
- All endpoints must have OpenAPI documentation
- Validate inputs with Zod schemas

## Avoid These Patterns

- ❌ Using `any` type
- ❌ Synchronous file operations
```

## Purpose

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

```text
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

- [Anthropic Claude Patterns](../../anthropic/claude_patterns.py)
- [OpenAI Integration](../../openai/openai_utilities.py)## Variables

| Variable | Description |
|---|---|
| `[ANTI_PATTERNS_LIST]` | AUTO-GENERATED: describe `ANTI_PATTERNS_LIST` |
| `[CODING_STANDARDS_LIST]` | AUTO-GENERATED: describe `CODING_STANDARDS_LIST` |
| `[FRAMEWORK]` | AUTO-GENERATED: describe `FRAMEWORK` |
| `[PATTERN_DEFINITIONS]` | AUTO-GENERATED: describe `PATTERN_DEFINITIONS` |
| `[PRIMARY_LANGUAGE]` | AUTO-GENERATED: describe `PRIMARY_LANGUAGE` |
| `[PROJECT_DESCRIPTION]` | AUTO-GENERATED: describe `PROJECT_DESCRIPTION` |
| `[PROJECT_NAME]` | AUTO-GENERATED: describe `PROJECT_NAME` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````
## Variables

| Variable | Description |
|---|---|
| `[ANTI_PATTERNS_LIST]` | AUTO-GENERATED: describe `ANTI_PATTERNS_LIST` |
| `[Anthropic Claude Patterns]` | AUTO-GENERATED: describe `Anthropic Claude Patterns` |
| `[CODING_STANDARDS_LIST]` | AUTO-GENERATED: describe `CODING_STANDARDS_LIST` |
| `[FRAMEWORK]` | AUTO-GENERATED: describe `FRAMEWORK` |
| `[Fill in a realistic input for the prompt]` | AUTO-GENERATED: describe `Fill in a realistic input for the prompt` |
| `[OpenAI Integration]` | AUTO-GENERATED: describe `OpenAI Integration` |
| `[PATTERN_DEFINITIONS]` | AUTO-GENERATED: describe `PATTERN_DEFINITIONS` |
| `[PRIMARY_LANGUAGE]` | AUTO-GENERATED: describe `PRIMARY_LANGUAGE` |
| `[PROJECT_DESCRIPTION]` | AUTO-GENERATED: describe `PROJECT_DESCRIPTION` |
| `[PROJECT_NAME]` | AUTO-GENERATED: describe `PROJECT_NAME` |
| `[Project Name]` | AUTO-GENERATED: describe `Project Name` |
| `[Representative AI response]` | AUTO-GENERATED: describe `Representative AI response` |
| `[category]` | AUTO-GENERATED: describe `category` |
| `[file]` | AUTO-GENERATED: describe `file` |
| `[framework-name]` | AUTO-GENERATED: describe `framework-name` |
| `[markdown]` | AUTO-GENERATED: describe `markdown` |
| `[notebooks|case-studies]` | AUTO-GENERATED: describe `notebooks|case-studies` |
| `[pattern]` | AUTO-GENERATED: describe `pattern` |
| `[pattern-name]` | AUTO-GENERATED: describe `pattern-name` |
| `[python]` | AUTO-GENERATED: describe `python` |
| `[validators|generators|benchmarks]` | AUTO-GENERATED: describe `validators|generators|benchmarks` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````

