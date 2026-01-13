# Validators

> **Prompt validation tools** - YAML frontmatter, content structure, and link integrity checking.

---

## ⚡ Quick Start

```powershell
# Validate all prompts (frontmatter)
python tools/validators/frontmatter_validator.py --all

# Quick validation
python tools/validate_prompts.py prompts/

# Check links
python tools/check_links.py docs/
```

---

## Available Validators

| Tool | Purpose | Output |
|------|---------|--------|
| `frontmatter_validator.py` | YAML metadata schema | Pass/Fail + errors |
| `prompt_validator.py` | Content structure | Score + issues |
| `score_validator.py` | Score validation | Numeric validation |
| `validate_prompts.py` | Quick validation | Summary |
| `check_links.py` | Link integrity | Broken links list |

---

## Frontmatter Validator

Validates YAML frontmatter against the metadata schema (`metadata_schema.yaml`).

### CLI Usage

```powershell
# Validate all prompts in repository
python tools/validators/frontmatter_validator.py --all

# Validate specific folder
python tools/validators/frontmatter_validator.py prompts/developers/

# Validate single file
python tools/validators/frontmatter_validator.py prompts/example.md

# Output JSON report
python tools/validators/frontmatter_validator.py --all -o validation_report.json

# Strict mode (exit non-zero on any error)
python tools/validators/frontmatter_validator.py --all --strict
```

### Python API

```python
from tools.validators.frontmatter_validator import FrontmatterValidator

validator = FrontmatterValidator()

# Validate single file
result = validator.validate_file("prompts/example.md")
print(f"Valid: {result.is_valid}")
print(f"Errors: {result.errors}")

# Validate folder
results = validator.validate_folder("prompts/developers/")
for r in results:
    if not r.is_valid:
        print(f"{r.file}: {r.errors}")
```

---

## Prompt Validator

Comprehensive content validation including structure, metadata, security, and accessibility.

### Python API

```python
from tools.validators.prompt_validator import PromptValidator

validator = PromptValidator()
report = validator.validate_file("prompts/example.md")

print(f"Overall Score: {report.overall_score}")
print(f"Error Count: {report.get_severity_counts()['error']}")
print(f"Warning Count: {report.get_severity_counts()['warning']}")

# List all issues
for issue in report.issues:
    print(f"[{issue.level}] {issue.category}: {issue.message}")
```

### Issue Categories

| Category | Description |
|----------|-------------|
| `frontmatter` | YAML metadata issues |
| `structure` | Document structure |
| `content` | Content quality |
| `security` | Security concerns |
| `accessibility` | Accessibility issues |

---

## Quick Validation Script

Fast validation for CI/CD pipelines.

```powershell
# Validate folder
python tools/validate_prompts.py prompts/

# Strict mode (exit code for CI)
python tools/validate_prompts.py prompts/ --strict

# Specific folder
python tools/validate_prompts.py prompts/advanced/
```

---

## Link Checker

Validates internal documentation links.

```powershell
# Check links in docs folder
python tools/check_links.py docs/

# Check all links
python tools/check_links.py --all

# Output to file
python tools/check_links.py docs/ -o broken_links.txt
```

---

## CI/CD Integration

```yaml
# GitHub Actions example
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python tools/validators/frontmatter_validator.py --all --strict
      - run: python tools/check_links.py --all
```

---

## Metadata Schema

The frontmatter validator uses `validators/metadata_schema.yaml` which defines:

- Required fields: `title`, `intro`, `type`
- Optional fields: `shortTitle`, `platforms`, `audience`, etc.
- Field types and valid values
- Governance tags

---

## See Also

- [analyzers.md](./analyzers.md) - Analysis tools
- [../prompteval/README.md](../prompteval/README.md) - Prompt evaluation
