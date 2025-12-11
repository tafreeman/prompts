# Testing Validators

This directory contains validation tests for the prompt library schema and frontmatter.

## Test Files

| File | Description | Tests |
|------|-------------|-------|
| `test_frontmatter.py` | Frontmatter parsing and required field validation | ~20 |
| `test_schema.py` | Schema structure and field type validation | ~25 |
| `test_frontmatter_auditor.py` | Auditor/autofix library tests | few |

## Running Tests

```bash
# Run all validator tests
python -m pytest testing/validators/ -v

# Run specific test file
python -m pytest testing/validators/test_frontmatter.py -v

# Run specific test class
python -m pytest testing/validators/test_schema.py::TestValidationFunctions -v

# Run auditor tests
python -m pytest testing/validators/test_frontmatter_auditor.py -v
```

## Schema Definition

Required frontmatter fields:

| Field | Type | Constraints |
|-------|------|-------------|
| `title` | string | 3-100 chars |
| `shortTitle` | string | 2-30 chars |
| `intro` | string | 10-500 chars |
| `type` | enum | `how_to`, `template`, `reference`, `guide` |
| `difficulty` | enum | `beginner`, `intermediate`, `advanced` |
| `audience` | list | min 1 item |
| `platforms` | list | min 1 item |
| `topics` | list | min 1 item |

## Using Validation in Other Tools

```python
from testing.validators.test_schema import validate_frontmatter, PROMPT_SCHEMA

# Auditor/autofix helpers
from testing.validators.frontmatter_auditor import validate_frontmatter_file, autofix_frontmatter_file

errors = validate_frontmatter(my_frontmatter_dict)
if errors:
    print("Validation failed:", errors)

result = validate_frontmatter_file(Path("prompts/foo.md"))
if result.status == "fail":
    print(result.errors)
```

## CLI (auditor)

```bash
# Audit without modifying files
python -m testing.validators.frontmatter_auditor check prompts/ docs/ --format text

# Audit and apply autofixes (placeholders, normalization)
python -m testing.validators.frontmatter_auditor check prompts/ --fix

# JSON report (useful for eval ingestion)
python -m testing.validators.frontmatter_auditor check prompts/ --format json > frontmatter-report.json
```
