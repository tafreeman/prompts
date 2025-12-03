# 🔬 Prompt Evaluation with GitHub Models

This directory contains tools for evaluating prompts from the library using GitHub Models (`gh models eval`).

> **Industry Best Practices**: This evaluation system incorporates methodologies from OpenAI Evals, Promptfoo, Anthropic, and Google Gemini.

## Prerequisites

1. **GitHub CLI** - Install from [cli.github.com](https://cli.github.com/)
2. **gh-models extension** - Install with:
   ```bash
   gh extension install github/gh-models
   ```
3. **Authentication** - Login with `gh auth login`

## Quick Start

### 1. Run a pre-built evaluation

```bash
# Evaluate sample prompts
gh models eval testing/evals/prompt-quality-eval.prompt.yml

# Get JSON output
gh models eval testing/evals/prompt-quality-eval.prompt.yml --json
```

### 2. Generate evaluations from your prompts

```bash
# Generate eval file for all developer prompts
python testing/evals/generate_eval_files.py prompts/developers

# Limit to 10 prompts
python testing/evals/generate_eval_files.py prompts/developers --limit 10

# Use a different model
python testing/evals/generate_eval_files.py prompts/developers --model openai/gpt-4o
```

### 3. Run evaluations with formatted output

```bash
# Run evaluation and see formatted results
python testing/evals/run_gh_eval.py testing/evals/developers-eval.prompt.yml

# Generate a markdown report
python testing/evals/run_gh_eval.py testing/evals/*.prompt.yml --report report.md

# Save raw JSON results
python testing/evals/run_gh_eval.py testing/evals/*.prompt.yml --json-output results.json
```

## Files

| File | Description |
|------|-------------|
| `prompt-quality-eval.prompt.yml` | Sample evaluation with 2 test prompts |
| `generate_eval_files.py` | Script to generate `.prompt.yml` files from markdown prompts |
| `run_gh_eval.py` | Script to run evaluations and format results |
| `tests.json` | Structured test suite definition (Anthropic-style) |

## Evaluation Criteria

Prompts are evaluated on **8 criteria** across two categories (scored 1-10):

### Core Quality Criteria

| Criterion | Description |
|-----------|-------------|
| **Clarity** | How clear and unambiguous are the instructions? |
| **Specificity** | Does it provide enough detail for consistent outputs? |
| **Actionability** | Can the AI clearly determine what actions to take? |
| **Structure** | Is it well-organized with clear sections? |
| **Completeness** | Does it cover all necessary aspects? |

### Advanced Quality Criteria (Industry Best Practices)

| Criterion | Description | Source |
|-----------|-------------|--------|
| **Factuality** | Are any claims/examples accurate? | OpenAI Evals |
| **Consistency** | Will it produce reproducible outputs? | Promptfoo |
| **Safety** | Does it avoid harmful patterns or vulnerabilities? | Anthropic |

## Pass/Fail Thresholds (Promptfoo-style)

```
✅ PASS: Overall score >= 7.0 AND no individual criterion < 5.0
❌ FAIL: Overall score < 7.0 OR any criterion < 5.0
```

### Grading Scale

| Grade | Score Range | Meaning |
|-------|-------------|---------|
| A | 8.5-10 | Excellent - production ready |
| B | 7.0-8.4 | Good - minor improvements possible |
| C | 5.5-6.9 | Average - several areas need work |
| D | 4.0-5.4 | Below Average - significant rework needed |
| F | <4.0 | Fails - major issues, not usable |

## Chain-of-Thought Evaluation (OpenAI-style)

The evaluator uses chain-of-thought reasoning before scoring:

1. Read the entire prompt to understand its intent
2. Identify the target audience and use case
3. Assess each criterion individually with specific evidence
4. Consider industry best practices
5. Formulate actionable improvements

## Example Output

```
📊 EVALUATION RESULTS: Developers Prompts Evaluation
======================================================================

1. 🏆 API Design Consultant [✅ PASS]
   Score: 9.6/10 (Grade: A)
   Category: developers | Difficulty: advanced
   Core: clarity: 9 | specificity: 10 | actionability: 9 | structure: 10 | completeness: 10
   Advanced: factuality: 9 | consistency: 10 | safety: 10
   Reasoning: The prompt clearly defines the role, provides comprehensive context...
   Summary: Exceptional prompt with clear structure and comprehensive coverage.

2. ❌ Vague Request [❌ FAIL]
   Score: 4.2/10 (Grade: D)
   Category: developers | Difficulty: beginner
   Core: clarity: 3 | specificity: 4 | actionability: 4 | structure: 5 | completeness: 5
   Advanced: factuality: 5 | consistency: 4 | safety: 5
   Summary: Lacks clarity and specificity, needs significant improvement.

----------------------------------------------------------------------
📈 SUMMARY STATISTICS
----------------------------------------------------------------------
   Prompts Evaluated: 10
   Average Score: 8.1/10
   Highest Score: 9.6/10
   Lowest Score: 4.2/10

   Pass/Fail Results:
      ✅ Passed: 8 (80%)
      ❌ Failed: 2 (20%)
   Pass Threshold: >= 7.0/10, no criterion < 5.0

   Grade Distribution:
      A: 4 prompt(s)
      B: 4 prompt(s)
      D: 2 prompt(s)

   Criterion Averages:
      ✅ clarity: 7.8/10
      ✅ specificity: 8.1/10
      ✅ actionability: 8.0/10
      ✅ structure: 8.5/10
      ✅ completeness: 8.2/10
      ✅ factuality: 8.0/10
      ✅ consistency: 8.3/10
      ✅ safety: 9.1/10
```

## CI/CD Integration

Add to your GitHub Actions workflow:

```yaml
name: Evaluate Prompts

on:
  pull_request:
    paths:
      - 'prompts/**'

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install pyyaml
      
      - name: Install gh-models
        run: gh extension install github/gh-models
        env:
          GH_TOKEN: ${{ github.token }}
      
      - name: Generate eval files
        run: python testing/evals/generate_eval_files.py prompts/ --limit 20
      
      - name: Run evaluations
        run: |
          for f in testing/evals/*-eval.prompt.yml; do
            gh models eval "$f" --json >> results.json
          done
        env:
          GH_TOKEN: ${{ github.token }}
      
      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: evaluation-results
          path: results.json
```

## Available Models

You can use any model available on GitHub Models:

- `openai/gpt-4o` - Best quality (default for deep evaluation)
- `openai/gpt-4o-mini` - Good balance of speed/quality (default)
- `openai/o1-mini` - Reasoning-focused
- `meta-llama/Meta-Llama-3.1-70B-Instruct` - Open source alternative

List available models:
```bash
gh models list
```

## Creating Custom Evaluations

Create a `.prompt.yml` file with this structure:

```yaml
name: My Custom Evaluation
description: What this evaluation tests
model: openai/gpt-4o-mini
modelParameters:
  temperature: 0.3
  max_tokens: 2000

testData:
  - promptTitle: "My Prompt"
    promptContent: |
      Your prompt content here...
    difficulty: "intermediate"

messages:
  - role: system
    content: |
      Your evaluation instructions...
  - role: user
    content: |
      Evaluate: {{promptTitle}}
      Content: {{promptContent}}

evaluators:
  - name: check-score
    string:
      contains: '"score"'
```

## Troubleshooting

### Rate Limiting
GitHub Models has rate limits. If you hit them:
- Reduce batch size in `generate_eval_files.py` with `--batch-size 5`
- Wait a few minutes between evaluations

### Authentication Issues
```bash
# Re-authenticate
gh auth login

# Check status
gh auth status
```

### Extension Not Found
```bash
# Reinstall extension
gh extension remove models
gh extension install github/gh-models
```

## Related

- [GitHub Models Documentation](https://docs.github.com/github-models)
- [gh-models Extension](https://github.com/github/gh-models)
- [Prompt Standards](../../docs/PROMPT_STANDARDS.md)
