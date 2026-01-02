# YAML Evaluation Support

## Overview

As of Phase 4 (2026-01-01), `prompteval` supports evaluating `.prompt.yml` files alongside traditional Markdown prompts. This enables testing prompts in the same format used by GitHub Models and provides a structured approach to multi-case evaluation.

## File Format

YAML evaluation files follow this structure:

```yaml
name: Evaluation Suite Name
description: Brief description
testData:
  - promptTitle: "Test Case 1"
    promptContent: "The actual prompt text"
    # Additional variables as needed
messages:
  - role: system
    content: "System instruction with {{variable}} substitution"
  - role: user
    content: "User message referencing {{promptContent}}"
```

### Required Fields

- **`testData`**: Array of test cases, each containing variables for substitution
- **`messages`**: Array of message templates with roles (system, user, assistant)

### Variable Substitution

Variables in messages use `{{variableName}}` syntax and are replaced with values from each test case:

```yaml
testData:
  - topic: "quantum computing"
    audience: "beginners"
messages:
  - role: user
    content: "Explain {{topic}} for {{audience}}"
```

## How It Works

### 1. Discovery

The `find_prompts()` function automatically discovers both:
- **Markdown**: `prompts/**/*.md`
- **YAML**: `testing/evals/**/*.prompt.yml`

```bash
# Evaluate all prompts (Markdown + YAML)
python -m prompteval prompts/

# Evaluate only YAML files
python -m prompteval testing/evals/
```

### 2. Structural Analysis (Tier 0)

YAML files are scored on structure:

| Component | Weight | Criteria |
|-----------|--------|----------|
| Structure | 40% | Presence of `testData` and `messages` |
| Test Data | 30% | At least one test case |
| Messages | 30% | At least one message template |

```bash
# Fast structural check
python -m prompteval testing/evals/ --tier 0
```

### 3. Model Evaluation (Tiers 1-7)

For each test case:
1. **Render messages**: Replace `{{variables}}` with values from testData
2. **Call model**: Execute via LLMClient (local, cloud, or hybrid)
3. **Parse response**: Extract JSON scores from model output
4. **Aggregate**: Average scores across all test cases

```bash
# Evaluate with local model (free)
python -m prompteval testing/evals/ --tier 1

# Cross-validate with multiple models
python -m prompteval testing/evals/ --tier 3
```

### 4. Output Schema

YAML evaluations produce **identical schema** to Markdown evaluations:

```json
{
  "model": "local:phi4",
  "run": 1,
  "score": 85.5,
  "criteria": {
    "clarity": 90,
    "effectiveness": 85,
    "reusability": 82
  },
  "duration": 1.2,
  "error": null
}
```

## Example: Multi-Case Evaluation

```yaml
name: Code Review Prompts
description: Test code review prompt quality
testData:
  - language: "Python"
    complexity: "simple"
    code: "def add(a, b): return a + b"
  - language: "JavaScript"
    complexity: "complex"
    code: "const memoize = fn => { const cache = {}; return (...args) => { ... }}"
messages:
  - role: system
    content: "You are a code reviewer. Evaluate this {{language}} code ({{complexity}}): {{code}}"
  - role: user
    content: "Provide a quality score (1-10) for: clarity, maintainability, correctness"
```

This will:
- Execute 2 test cases (Python simple, JavaScript complex)
- Average the scores across both cases
- Report aggregated criteria (clarity, maintainability, correctness)

## Comparison: Markdown vs YAML

| Aspect | Markdown | YAML |
|--------|----------|------|
| **Use Case** | Single-prompt library | Multi-case testing |
| **Structure** | Frontmatter + body | testData + messages |
| **Variables** | Manual | Automatic substitution |
| **Test Cases** | One per file | Multiple per file |
| **Rubric** | Structural (frontmatter, sections) | Structural (testData, messages) |
| **Output** | ModelResult | ModelResult (identical) |

## CLI Examples

### Discover All Prompts
```bash
# Find all Markdown and YAML prompts
python -m prompteval prompts/ --tier 0 --verbose
```

### Evaluate YAML with Local Model
```bash
# Fast, free evaluation
python -m prompteval testing/evals/advanced/ --tier 1
```

### Cross-Validate YAML
```bash
# Multiple models, multiple runs
python -m prompteval testing/evals/ --tier 3 --runs 2
```

### JSON Output
```bash
# Machine-readable results
python -m prompteval testing/evals/ --tier 2 -o results.json
```

### CI Mode
```bash
# Exit non-zero if any prompt fails threshold
python -m prompteval testing/evals/ --tier 2 --ci --threshold 70
```

## Implementation Details

### Core Functions

**`evaluate_yaml_prompt(file_path, model_full, run_num, start_time)`**
- Parses YAML file
- Iterates through testData
- Renders messages with variable substitution
- Calls model for each test case
- Aggregates scores
- Returns `ModelResult`

**`evaluate_structural(file_path)`**
- Detects file type (MD vs YAML)
- Applies appropriate rubric
- Returns consistent schema

**`find_prompts(path, exclude)`**
- Discovers both `.md` and `.prompt.yml` files
- Applies exclusion rules
- Returns sorted list

### Error Handling

- **YAML Parse Error**: Returns ModelResult with error="YAML Error: ..."
- **Missing Fields**: Returns error="Missing testData or messages in YAML"
- **Model Failure**: Continues to next test case, reports if all fail
- **No Valid Responses**: Returns score=0 with error message

## Best Practices

### 1. Organize by Category
```
testing/evals/
├── advanced/           # Complex reasoning prompts
├── developers/         # Code-related prompts
├── security/          # Security-focused prompts
└── test-simple.prompt.yml
```

### 2. Keep Test Cases Focused
```yaml
# Good: Related test cases
testData:
  - scenario: "authentication"
  - scenario: "authorization"
  - scenario: "rate limiting"

# Avoid: Unrelated test cases
testData:
  - scenario: "authentication"
  - scenario: "data visualization"  # Different domain
```

### 3. Use Descriptive Variables
```yaml
# Good
testData:
  - userRole: "admin"
    resourceType: "database"

# Avoid
testData:
  - var1: "admin"
    var2: "database"
```

### 4. Start with Tier 0
```bash
# Always validate structure first (free, instant)
python -m prompteval new-eval.prompt.yml --tier 0
```

## Migration Guide

### Converting Markdown to YAML

**Before (Markdown):**
```markdown
---
title: Code Review Prompt
category: developers
---

Review this code and provide feedback:
- Clarity
- Maintainability
```

**After (YAML):**
```yaml
name: Code Review Prompt
description: Multi-language code review
testData:
  - language: "Python"
    code: "..."
  - language: "JavaScript"
    code: "..."
messages:
  - role: user
    content: "Review this {{language}} code: {{code}}"
```

## Troubleshooting

### Issue: "No prompts found"
**Cause:** YAML file not in `evals/` directory or doesn't end with `.prompt.yml`  
**Fix:** Ensure file is in `testing/evals/` and named `*.prompt.yml`

### Issue: "Missing testData or messages in YAML"
**Cause:** Required fields not present  
**Fix:** Add both `testData` and `messages` arrays

### Issue: Scores are 0
**Cause:** Model response not parseable as JSON  
**Fix:** Improve message templates to explicitly request JSON output

### Issue: Variable not substituted
**Cause:** Variable name mismatch  
**Fix:** Ensure `{{variableName}}` matches key in testData exactly

## Future Enhancements

Potential improvements for Phase 5+:
- [ ] Support for `expectedOutput` (automated correctness checking)
- [ ] Custom rubrics per YAML file
- [ ] Parallel execution of test cases
- [ ] Integration with `gh models eval` for native GitHub Models support
- [ ] Support for multi-turn conversations (message history)
