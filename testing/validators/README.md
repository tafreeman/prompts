# Testing Validators

This directory contains validation tests for the prompt library schema and frontmatter.

## Test Files

| File | Description | Tests |
|------|-------------|-------|
| `test_frontmatter.py` | Frontmatter parsing and required field validation | ~20 |
| `test_schema.py` | Schema structure and field type validation | ~25 |

## Running Tests

```bash
# Run all validator tests
python -m pytest testing/validators/ -v

# Run specific test file
python -m pytest testing/validators/test_frontmatter.py -v

# Run specific test class
python -m pytest testing/validators/test_schema.py::TestValidationFunctions -v
```text
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

errors = validate_frontmatter(my_frontmatter_dict)
if errors:
    print("Validation failed:", errors)
```text