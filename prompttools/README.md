# Prompttools

A lightweight, practical toolkit for evaluating, validating, and managing prompts in the Enterprise AI Prompt Library. This package provides CLI utilities and Python APIs for prompt quality assessment, structural validation, and LLM interactions.

## 📁 Directory Structure

```text
prompttools/
├── __init__.py           # Package initialization
├── __main__.py           # CLI entry point
├── cache.py              # Response caching utilities
├── cli.py                # Command-line interface
├── config.py             # Configuration management
├── evaluate.py           # Prompt evaluation engine
├── llm.py                # LLM provider integrations
├── parse.py              # Prompt file parsing
├── validate.py           # Structural validation
└── rubrics/              # Evaluation rubrics
    └── prompt-scoring.yaml
```

## ✨ Features

- ✅ **Multi-tier evaluation**: Local, cloud, and structural validation
- ✅ **Provider agnostic**: Supports OpenAI, Anthropic, GitHub Models, local ONNX
- ✅ **Smart caching**: Avoid redundant API calls
- ✅ **Batch processing**: Evaluate entire directories
- ✅ **YAML rubrics**: Configurable scoring criteria
- ✅ **Frontmatter parsing**: Extract metadata from Markdown files
- ✅ **Validation**: Check prompt structure and metadata

## 🚀 Quick Start

### Installation

```bash
# From repository root
pip install -e .

# Or install dependencies directly
pip install -r requirements.txt
```

### Basic Usage

```bash
# Evaluate a single prompt (local tier)
prompttools evaluate prompts/developers/code-generation.md

# Evaluate entire directory with cloud model
prompttools evaluate prompts/ --tier 2

# Validate structure only (no LLM calls)
prompttools validate prompts/

# Generate LLM response directly
prompttools generate "Write a Python function to sort a list"
```

### Python API

```python
from prompttools import evaluate_prompt, validate_prompt

# Evaluate a prompt
result = evaluate_prompt(
    prompt_path="prompts/developers/test.md",
    tier=1,  # Local model
    model="onnx:phi-3"
)
print(f"Score: {result['total_score']}/100")

# Validate structure
issues = validate_prompt("prompts/new-prompt.md")
if issues:
    print("Validation issues:", issues)
else:
    print("Valid prompt!")
```

## 🔧 Core Components

### cli.py - Command-Line Interface

**Purpose**: User-facing commands for common operations

**Commands**:

- `evaluate` (alias: `eval`, `e`): Score prompt quality
- `validate` (alias: `val`, `v`): Check structure and metadata
- `generate` (alias: `gen`, `g`): Direct LLM interaction
- `parse` (alias: `p`): Extract frontmatter and content

**Example**:

```bash
prompttools evaluate prompts/business/ --tier 2 --model gh:gpt-4o-mini
```

**Options**:

- `--tier`: Evaluation tier (0=structural, 1=local, 2=cloud, 3=premium)
- `--model`: Specific model (format: `provider:model-name`)
- `--output`: Save results to file
- `--verbose`: Detailed output

### evaluate.py - Evaluation Engine

**Purpose**: Score prompts against quality rubrics

**Tiers**:

- **Tier 0 (Structural)**: Metadata and format checks (no LLM)
- **Tier 1 (Local)**: ONNX/NPU models (phi-3, llama)
- **Tier 2 (Cloud)**: GitHub Models, OpenAI GPT-4o-mini
- **Tier 3 (Premium)**: GPT-4, Claude Opus

**Scoring Dimensions**:

1. **Clarity** (25%): How clear and understandable
2. **Structure** (25%): Organization and formatting
3. **Usefulness** (20%): Practical applicability
4. **Technical Quality** (20%): Correctness and best practices
5. **Ease of Use** (10%): User-friendliness

**Example**:

```python
from prompttools.evaluate import evaluate_prompt

result = evaluate_prompt(
    prompt_path="prompts/test.md",
    tier=2,
    rubric_path="prompttools/rubrics/prompt-scoring.yaml"
)

print(f"Clarity: {result['scores']['clarity']}/100")
print(f"Total: {result['total_score']}/100")
```

### llm.py - LLM Provider Integrations

**Purpose**: Abstract interface to multiple LLM providers

**Supported Providers**:

- **OpenAI**: GPT-4, GPT-4o, GPT-4o-mini
- **Anthropic**: Claude 3 Opus, Sonnet, Haiku
- **GitHub Models**: Via GitHub token
- **Local ONNX**: Phi-3, Llama (CPU/NPU)

**Usage**:

```python
from prompttools.llm import LLMClient

client = LLMClient(provider="openai", model="gpt-4o-mini")
response = client.generate("Explain Chain-of-Thought prompting")
print(response.text)
```

**Environment Variables**:

```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GITHUB_TOKEN=ghp_...
```

### parse.py - Prompt File Parsing

**Purpose**: Extract frontmatter and content from Markdown files

**Features**:

- YAML frontmatter extraction
- Content body parsing
- Metadata validation
- Variable extraction

**Example**:

```python
from prompttools.parse import parse_prompt_file

prompt = parse_prompt_file("prompts/test.md")
print(f"Title: {prompt['metadata']['title']}")
print(f"Category: {prompt['metadata']['category']}")
print(f"Content length: {len(prompt['content'])} chars")
```

### validate.py - Structural Validation

**Purpose**: Ensure prompts meet quality standards

**Checks**:

- ✅ Required frontmatter fields present
- ✅ Valid metadata values (against `data/` schemas)
- ✅ Proper Markdown structure
- ✅ Example sections included
- ✅ Variable placeholders documented
- ✅ File naming conventions

**Example**:

```python
from prompttools.validate import validate_prompt

issues = validate_prompt("prompts/new-prompt.md")
if issues:
    for issue in issues:
        print(f"❌ {issue['field']}: {issue['message']}")
else:
    print("✅ Prompt is valid!")
```

**Validation Rules**:

```yaml
required_fields:

  - title
  - category
  - tags
  - author
  - version

valid_categories:

  - developers
  - business
  - creative
  - analysis
  - system
  - governance

```

### cache.py - Response Caching

**Purpose**: Cache LLM responses to reduce API costs and latency

**Features**:

- File-based caching (`.cache/` directory)
- Configurable TTL (time-to-live)
- Automatic cache invalidation
- Cache hit/miss metrics

**Usage**:

```python
from prompttools.cache import cached_generate

# First call hits API
response = cached_generate("Explain CoVe", model="gpt-4o-mini")

# Second call returns cached response (instant)
response = cached_generate("Explain CoVe", model="gpt-4o-mini")
```

**Cache Key**: Hash of (prompt + model + parameters)

### config.py - Configuration Management

**Purpose**: Manage settings and environment configuration

**Configuration Sources**:

1. Environment variables
2. `.env` file
3. `config.yaml` file
4. Command-line arguments
5. Defaults

**Example**:

```python
from prompttools.config import Config

config = Config.load()
print(f"Default tier: {config.eval_tier}")
print(f"Default model: {config.default_model}")
```

**Configuration File** (`config.yaml`):

```yaml
evaluation:
  default_tier: 1
  default_model: "onnx:phi-3"
  cache_enabled: true
  cache_ttl: 86400  # 24 hours

models:
  openai_default: "gpt-4o-mini"
  anthropic_default: "claude-3-sonnet"
  github_default: "gpt-4o-mini"

validation:
  strict_mode: false
  allow_missing_examples: false
```

## 📊 Evaluation Rubrics

### Rubric Schema

Located in `rubrics/prompt-scoring.yaml`:

```yaml
dimensions:
  clarity:
    weight: 0.25
    description: "How clear and understandable is the prompt?"
    criteria:

      - "Unambiguous language"
      - "Clear objectives"
      - "Minimal jargon"
      - "Consistent terminology"

  structure:
    weight: 0.25
    description: "How well-organized is the prompt?"
    criteria:

      - "Logical flow"
      - "Proper sections"
      - "Consistent formatting"
      - "Complete metadata"

  usefulness:
    weight: 0.20
    description: "How practical and applicable is the prompt?"
    criteria:

      - "Solves real problems"
      - "Includes examples"
      - "Actionable guidance"
      - "Appropriate scope"

  technical_quality:
    weight: 0.20
    description: "Technical correctness and best practices"
    criteria:

      - "Follows best practices"
      - "Accurate information"
      - "Appropriate complexity"
      - "Error-free"

  ease_of_use:
    weight: 0.10
    description: "How easy is the prompt to use?"
    criteria:

      - "Clear instructions"
      - "Documented variables"
      - "Copy-paste ready"
      - "Minimal customization needed"

```

### Scoring System

Each dimension is scored 0-100:

- **90-100**: Exceptional quality
- **75-89**: High quality
- **60-74**: Good quality
- **50-59**: Acceptable
- **0-49**: Needs improvement

**Total Score**: Weighted average of all dimensions

## 🎯 Evaluation Tiers

### Tier 0: Structural (Free, Instant)

**What**: Metadata and format validation only  
**Cost**: Free  
**Speed**: Instant  
**Use Case**: Quick checks, CI/CD pipelines

**Example**:

```bash
prompttools validate prompts/ --tier 0
```

### Tier 1: Local (Free, Fast)

**What**: Local ONNX models on CPU/NPU  
**Cost**: Free (hardware cost)  
**Speed**: 1-3 seconds per prompt  
**Use Case**: Development, batch evaluation

**Models**: Phi-3-mini, Llama-3-8B

**Example**:

```bash
prompttools evaluate prompts/ --tier 1 --model onnx:phi-3
```

### Tier 2: Cloud (Low Cost)

**What**: GitHub Models, GPT-4o-mini  
**Cost**: $0.15-$0.60 per 1M tokens  
**Speed**: 2-5 seconds per prompt  
**Use Case**: Production evaluation, CI/CD

**Models**: gpt-4o-mini, claude-3-haiku

**Example**:

```bash
prompttools evaluate prompts/ --tier 2 --model gh:gpt-4o-mini
```

### Tier 3: Premium (High Cost)

**What**: GPT-4, Claude Opus  
**Cost**: $15-$60 per 1M tokens  
**Speed**: 3-8 seconds per prompt  
**Use Case**: High-stakes evaluation, research

**Models**: gpt-4, claude-3-opus

**Example**:

```bash
prompttools evaluate prompts/ --tier 3 --model openai:gpt-4
```

## 📖 Usage Examples

### Evaluate Single Prompt

```bash
# Local model (free)
prompttools evaluate prompts/developers/code-review.md

# Cloud model
prompttools evaluate prompts/business/analysis.md --tier 2

# Premium model for critical prompts
prompttools evaluate prompts/governance/compliance.md --tier 3 --model openai:gpt-4
```

### Batch Evaluation

```bash
# Evaluate entire category
prompttools evaluate prompts/developers/ --tier 1

# Evaluate all prompts
prompttools evaluate prompts/ --tier 2 --output results.json

# Filter by category during evaluation
prompttools evaluate prompts/ --tier 1 --category developers
```

### Validation Only

```bash
# Check all prompts
prompttools validate prompts/

# Strict mode (fail on warnings)
prompttools validate prompts/ --strict

# Validate specific file
prompttools validate prompts/new-prompt.md
```

### Direct LLM Generation

```bash
# Quick query
prompttools generate "Explain Chain-of-Thought prompting"

# With specific model
prompttools generate "Write a Python decorator" --model openai:gpt-4o-mini

# Save output
prompttools generate "Generate test cases for login" --output test-cases.txt
```

### Parse Prompt Metadata

```bash
# Extract frontmatter
prompttools parse prompts/developers/code-review.md

# JSON output
prompttools parse prompts/business/analysis.md --format json

# Extract variables
prompttools parse prompts/templates/template.md --extract-variables
```

## 🔌 Integration Examples

### CI/CD Pipeline

```yaml
# .github/workflows/validate-prompts.yml
name: Validate Prompts

on: [pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:

      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2

        with:
          python-version: '3.11'

      - run: pip install -r requirements.txt
      - run: prompttools validate prompts/ --strict
      - run: prompttools evaluate prompts/ --tier 2 --output results.json

        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - uses: actions/upload-artifact@v2

        with:
          name: evaluation-results
          path: results.json
```

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash
prompttools validate prompts/ --strict || exit 1
echo "✅ All prompts validated successfully"
```

### Python Script

```python
#!/usr/bin/env python3
"""Evaluate all prompts and generate report."""

from pathlib import Path
from prompttools import evaluate_prompt, validate_prompt

def evaluate_library(prompts_dir: str, tier: int = 1):
    """Evaluate all prompts in library."""
    results = []

    for prompt_file in Path(prompts_dir).rglob("*.md"):
        # Validate structure
        issues = validate_prompt(str(prompt_file))
        if issues:
            print(f"⚠️  {prompt_file}: {len(issues)} validation issues")
            continue

        # Evaluate quality
        result = evaluate_prompt(str(prompt_file), tier=tier)
        results.append({
            "file": str(prompt_file),
            "score": result["total_score"],
            "tier": result.get("tier", "passed")
        })
        print(f"✅ {prompt_file}: {result['total_score']}/100")

    # Generate report
    avg_score = sum(r["score"] for r in results) / len(results)
    print(f"\n📊 Average Score: {avg_score:.1f}/100")
    print(f"📈 Prompts Evaluated: {len(results)}")

    # Find top performers
    top_prompts = sorted(results, key=lambda x: x["score"], reverse=True)[:5]
    print("\n🏆 Top 5 Prompts:")
    for prompt in top_prompts:
        print(f"  - {prompt['file']}: {prompt['score']}/100")

if __name__ == "__main__":
    evaluate_library("prompts/", tier=1)
```

## 🛠️ Development

### Running Tests

```bash
# Run all tests
pytest testing/

# Run with coverage
pytest --cov=prompttools testing/

# Run specific test
pytest testing/test_evaluate.py::test_tier_1_evaluation
```

### Adding New Features

1. **Create module**: Add new `.py` file in `prompttools/`
2. **Add tests**: Create corresponding test file in `testing/`
3. **Update CLI**: Add command in `cli.py` if needed
4. **Document**: Update this README

### Code Style

```bash
# Format code
black prompttools/
isort prompttools/

# Lint
flake8 prompttools/
pylint prompttools/

# Type checking
mypy prompttools/
```

## 📚 Related Resources

- **[Main README](../README.md)**: Repository overview
- **[Tools](../tools/)**: Additional utilities and scripts
- **[Data](../data/)**: Schemas and taxonomy
- **[Docs](../docs/)**: Conceptual documentation

## 🤝 Contributing

We welcome contributions! To add features:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This package is licensed under [MIT License](../LICENSE).

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'prompttools'`  
**Solution**: Install package with `pip install -e .`

**Issue**: `API key not found`  
**Solution**: Set environment variables (see `.env.example`)

**Issue**: Local models not working  
**Solution**: Install ONNX Runtime: `pip install onnxruntime`

**Issue**: Evaluation hanging  
**Solution**: Check API connectivity and rate limits

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/tafreeman/prompts/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tafreeman/prompts/discussions)
- **Documentation**: [Full Docs](../docs/)

---

**Made with ❤️ for the prompt engineering community.**
