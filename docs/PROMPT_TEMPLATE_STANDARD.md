# Prompt File Standard Template

This document defines the canonical structure for prompt files in this repository.

> **Version**: 2.0.0 | **Updated**: 2026-01-20
>
> Aligned with unified-scoring.yaml v3.0.0 and prompt_file.py (gh-models format)

## Required Structure

All prompt files MUST have these components:

```markdown
---
name: [Prompt Name]
description: [Brief description]
type: how_to | reference | template | guide
# === Optional execution fields ===
pattern: react | cove | reflexion | rag    # For advanced reasoning patterns
model: openai/gpt-4o                       # Recommended model
model_parameters:                          # Optional model settings
  temperature: 0.7
  max_tokens: 2000
response_format: text | json_object | json_schema  # Expected output format
difficulty: beginner | intermediate | advanced     # Complexity level
---

# [Title]

## Description

[What this prompt does and when to use it]

## Prompt

### System Prompt

```text
[System-level instructions that configure the AI's role and behavior]
```

### User Prompt

```text
[User-facing template with variables]
```

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `[VARIABLE]` | What it represents | Example value |

## Example

### Input

```text
[Example filled-in values]
```

### Expected Output

```markdown
[Expected output - useful for automated evaluation]
```

## Test Data (Optional)

<!-- For automated evaluation with prompteval -->
| Scenario | Input Variables | Expected Contains |
|----------|-----------------|-------------------|
| Basic case | `[VAR]=value` | "expected phrase" |
| Edge case | `[VAR]=edge` | "handles edge" |

```

## Section Details

### YAML Frontmatter

#### Required Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✅ Yes | Human-readable title (must match filename convention) |
| `description` | ✅ Yes | 1-2 sentence description |
| `type` | ✅ Yes | One of: `how_to`, `reference`, `template`, `guide` |

#### Optional Execution Fields

| Field | Purpose | Values |
|-------|---------|--------|
| `pattern` | Enables pattern-specific scoring | `react`, `cove`, `reflexion`, `rag` |
| `model` | Recommended model for execution | e.g., `openai/gpt-4o`, `local:phi4` |
| `model_parameters` | Model settings (temp, max_tokens, top_p) | Object with numeric values |
| `response_format` | Expected output structure | `text`, `json_object`, `json_schema` |
| `difficulty` | Complexity indicator | `beginner`, `intermediate`, `advanced` |

### H2 Sections

| Section | Required | Purpose |
|---------|----------|---------|
| `## Description` | ✅ Yes | What the prompt does, use cases |
| `## Prompt` | ✅ Yes | The actual prompt content |
| `## Variables` | ✅ Yes | Variable documentation table |
| `## Example` | ✅ Yes | Input/output demonstration |
| `## Test Data` | Optional | Input/expected pairs for automated evaluation |

### Prompt Sub-Sections

The `## Prompt` section SHOULD contain:

| Sub-Section | Purpose |
|-------------|---------|
| `### System Prompt` | AI role, capabilities, constraints, output standards |
| `### User Prompt` | Task-specific template with `[VARIABLE]` placeholders |

For simple prompts (no agent execution), a single code block is acceptable:

```markdown
## Prompt

```text
[Combined prompt content]
```

```

## Validation Compliance

This structure passes:
- ✅ `prompttools validate` - Structural validation
- ✅ `prompttools evaluate` - LLM-based quality scoring (5 dimensions, 0-100)
- ✅ `list_complete_files.py` - Section completeness check
- ✅ Pattern scoring - When `pattern:` is set, enables 7 universal + pattern-specific dimensions

## Execution Compatibility

For prompts intended for agent execution frameworks:
1. The `### System Prompt` becomes the system message
2. The `### User Prompt` becomes the user message with variable substitution
3. Variables from `## Variables` map to the `[VARIABLE]` placeholders
4. `model` and `model_parameters` configure the target model
5. `response_format` sets output expectations (text/JSON)

## Pattern-Specific Scoring

When `pattern:` is set in frontmatter, the prompt is evaluated with additional dimensions:

| Pattern | Specific Dimensions |
|---------|--------------------|
| `react` | Thought/Action separation, Observation binding, Termination discipline |
| `cove` | Verification question quality, Evidence independence, Revision delta |
| `reflexion` | Critique specificity, Memory utilization, Improvement signal |
| `rag` | Retrieval trigger accuracy, Evidence grounding, Citation discipline |

Universal dimensions (all patterns): PIF, POI, PC, CA, SRC, PR, IR

See `tools/rubrics/pattern-scoring.yaml` for full rubric definitions.

## Test Data Format

The `## Test Data` section enables automated evaluation. Two formats supported:

### Markdown Table (Human-Readable)

```markdown
## Test Data

| Scenario | Input Variables | Expected Contains |
|----------|-----------------|-------------------|
| Basic | `[VAR]=test` | "success" |
```

### YAML in Frontmatter (Machine-Readable)

```yaml
test_data:
  - input: { VAR: "test" }
    expected_contains: "success"
  - input: { VAR: "edge" }
    expected_contains: "handles"
```

## Related

- `prompttools/config.py` - Defines REQUIRED_SECTIONS and PREFERRED_SECTIONS
- `tools/rubrics/unified-scoring.yaml` - Standard scoring rubric (5 dimensions)
- `tools/rubrics/pattern-scoring.yaml` - Pattern-specific scoring rubric
- `tools/rubrics/patterns/*.yaml` - Individual pattern definitions (react, cove, reflexion, rag)
- `tools/prompteval/prompt_file.py` - gh-models compatible prompt file loader
