# PromptEval: Comprehensive Prompt Evaluation Tool

## Implementation Plan & Design Document

**Version**: 1.0  
**Date**: December 2025  
**Status**: Design Phase

---

## Executive Summary

This document outlines the design for **PromptEval**, a comprehensive, standalone prompt evaluation tool that:

1. **Consolidates** existing tools (`tiered_eval.py`, `evaluate_library.py`, `cove_batch_analyzer.py`, `run_eval_geval.py`)
2. **Incorporates** industry best practices from Promptfoo, DeepEval, RAGAS, and G-Eval
3. **Leverages** your existing infrastructure (`llm_client.py`, `local_model.py`, rubrics)
4. **Adds** Promptfoo-style YAML configuration for easy test case definition
5. **Provides** both an intuitive CLI and a Python API

---

## 1. Design Goals

### Primary Goals

| Goal | Description | Priority |
|------|-------------|----------|
| **Ease of Use** | Single CLI command for common operations, sensible defaults | P0 |
| **Extensive Capabilities** | Support 6 evaluation dimensions, 3 scoring methodologies, 8+ model providers | P0 |
| **Research-Backed Scoring** | Implement G-Eval, BERTScore-style, RAGAS metrics per research doc | P0 |
| **Local-First** | Free evaluation using local ONNX models as default | P0 |
| **Promptfoo Compatibility** | Optional YAML test case format for CI/CD integration | P1 |
| **Extensibility** | Plugin architecture for custom metrics and evaluators | P1 |

### Non-Goals (v1.0)

- Full observability/tracing platform (use LangSmith/Phoenix for that)
- Real-time production monitoring
- Multi-user collaboration features

---

## 2. Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PromptEval                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────┐    ┌──────────────────────┐    ┌───────────────┐  │
│  │      CLI Layer       │    │     Python API       │    │  YAML Config  │  │
│  │   prompteval [cmd]   │    │   from prompteval    │    │ prompteval.yml│  │
│  └──────────┬───────────┘    └──────────┬───────────┘    └───────┬───────┘  │
│             │                           │                         │          │
│             └───────────────────────────┼─────────────────────────┘          │
│                                         ▼                                    │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                        Evaluation Engine                              │   │
│  ├──────────────────────────────────────────────────────────────────────┤   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │   │
│  │  │  Structural │  │   G-Eval    │  │  LLM-Judge  │  │  Semantic   │  │   │
│  │  │   Analyzer  │  │   Scorer    │  │   Scorer    │  │  Similarity │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                         │                                    │
│                                         ▼                                    │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                        Model Layer (llm_client.py)                    │   │
│  ├──────────┬──────────┬──────────┬──────────┬──────────┬───────────────┤   │
│  │  Local   │ Windows  │  GitHub  │  Azure   │  OpenAI  │   Anthropic   │   │
│  │  ONNX    │    AI    │  Models  │ Foundry  │   API    │     API       │   │
│  └──────────┴──────────┴──────────┴──────────┴──────────┴───────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component Breakdown

```
tools/prompteval/
├── __init__.py              # Package exports
├── __main__.py              # CLI entry point
│
├── # ═══ Core Engine ═══
├── engine/
│   ├── __init__.py
│   ├── evaluator.py         # Main evaluation orchestrator
│   ├── structural.py        # Structural/static analysis
│   ├── geval.py             # G-Eval implementation per research
│   ├── llm_judge.py         # LLM-as-judge scorer
│   ├── semantic.py          # BERTScore / embedding similarity
│   └── reproducibility.py   # Multi-run consistency testing
│
├── # ═══ Metrics ═══
├── metrics/
│   ├── __init__.py
│   ├── base.py              # Abstract metric class
│   ├── clarity.py           # Clarity dimension
│   ├── effectiveness.py     # Effectiveness dimension
│   ├── reusability.py       # Reusability dimension
│   ├── simplicity.py        # Simplicity dimension
│   ├── examples.py          # Example quality dimension
│   ├── security.py          # Security & compliance
│   ├── custom.py            # Custom metric loader
│   └── ragas.py             # RAGAS-style RAG metrics
│
├── # ═══ Configuration ═══
├── config/
│   ├── __init__.py
│   ├── loader.py            # YAML/JSON config loader
│   ├── defaults.py          # Default settings
│   └── schema.py            # Config validation schema
│
├── # ═══ Reporters ═══
├── reporters/
│   ├── __init__.py
│   ├── console.py           # Terminal output
│   ├── markdown.py          # Markdown report
│   ├── json_reporter.py     # JSON output
│   ├── html.py              # HTML dashboard
│   └── ci.py                # CI/CD exit codes
│
├── # ═══ CLI ═══
├── cli/
│   ├── __init__.py
│   ├── main.py              # CLI dispatcher
│   ├── evaluate.py          # eval command
│   ├── test.py              # test command (promptfoo-style)
│   ├── compare.py           # compare command
│   ├── init.py              # init config command
│   └── interactive.py       # interactive mode
│
└── # ═══ Utilities ═══
├── utils/
│   ├── __init__.py
│   ├── prompt_parser.py     # Parse prompt files
│   ├── text_similarity.py   # Similarity calculations
│   ├── cache.py             # Result caching
│   └── parallel.py          # Parallel execution
```

---

## 3. Feature Specification

### 3.1 CLI Commands

```bash
# ═══════════════════════════════════════════════════════════════════════════
#                           PROMPTEVAL CLI
# ═══════════════════════════════════════════════════════════════════════════

# ─── EVALUATE: Score prompts against rubric ───
prompteval evaluate prompts/advanced/            # Evaluate directory
prompteval evaluate prompts/example.md           # Single prompt
prompteval evaluate . --tier 3                   # Use evaluation tier
prompteval evaluate . -m local:phi4mini          # Specific model
prompteval evaluate . --rubric custom.yaml       # Custom rubric
prompteval evaluate . -o report.json             # JSON output
prompteval evaluate . --threshold 80             # Fail if <80%

# ─── TEST: Run assertion-based tests (Promptfoo-style) ───
prompteval test                                  # Run prompteval.yaml
prompteval test tests/api-prompts.yaml           # Custom test file
prompteval test --filter "category=advanced"     # Filter tests
prompteval test --parallel 4                     # Parallel execution

# ─── COMPARE: A/B prompt comparison ───
prompteval compare v1.md v2.md                   # Compare two versions
prompteval compare old/ new/ -o diff.html        # Directory comparison

# ─── REPRODUCIBILITY: Consistency testing ───
prompteval repro prompts/cot.md -n 10            # 10 runs
prompteval repro prompts/ --threshold 85         # Require 85% similarity

# ─── INIT: Create configuration ───
prompteval init                                  # Interactive setup
prompteval init --template enterprise           # Enterprise template

# ─── CONFIG: Manage settings ───
prompteval config set model local:phi4mini       # Default model
prompteval config set threshold 75               # Default threshold
prompteval config show                           # Show current config

# ─── Interactive Mode ───
prompteval interactive                           # REPL for exploration
```

### 3.2 Evaluation Tiers (Ported + Enhanced)

| Tier | Name | Description | Cost | Time |
|------|------|-------------|------|------|
| 0 | **Structural** | Static analysis only (no LLM) | $0 | <1s |
| 1 | **Local Quick** | Single local model, 1 run | $0 | ~30s |
| 2 | **Local Deep** | Local model with G-Eval reasoning | $0 | ~60s |
| 3 | **Cross-Model** | 3 models × 2 runs (local mix) | $0 | ~5min |
| 4 | **Cloud Quick** | Single cloud model (gh:gpt-4o-mini) | ~$0.01 | ~5s |
| 5 | **Cloud Cross** | 3 cloud models × 2 runs | ~$0.10 | ~30s |
| 6 | **Premium** | 5 models × 3 runs + reproducibility | ~$0.30 | ~2min |
| 7 | **Enterprise** | Full pipeline + human-in-loop prep | ~$0.50 | ~5min |

### 3.3 Scoring Methodologies

**Three complementary approaches per our research document:**

#### 3.3.1 Structural Scoring (No LLM)

```python
structural_score = {
    "frontmatter_complete": True,       # Has all required fields
    "sections_present": 0.90,           # % of expected sections
    "example_count": 2,                 # Number of examples
    "variable_definitions": True,       # Variables defined
    "research_citation": True,          # Has research foundation
    "word_count": 1500,                 # Total word count
    "governance_tags": ["PII-safe"],    # Governance tags
    "overall": 0.85                     # Structural completeness
}
```

#### 3.3.2 G-Eval Scoring (Per Research)

Implementation based on G-Eval paper with our enterprise criteria:

```python
geval_config = {
    "criteria": [
        {
            "name": "clarity",
            "weight": 0.25,
            "description": "Is the prompt unambiguous and easy to understand?",
            "cot_prompt": """
            Evaluate the clarity of this prompt. Consider:
            1. Can a user understand the purpose within 10 seconds?
            2. Are variable names self-explanatory?
            3. Is the instruction structure logical?
            4. Are there ambiguous phrases or jargon?
            
            Think step-by-step, then provide a score 1-5.
            """
        },
        # ... effectiveness, reusability, simplicity, examples
    ],
    "scale": "1-5",
    "normalization": "0-100",
    "model": "local:phi4mini"
}
```

#### 3.3.3 Semantic Similarity (For Reproducibility)

```python
similarity_config = {
    "method": "sentence-transformers",  # or "openai-embeddings"
    "model": "all-MiniLM-L6-v2",        # Local embedding model
    "threshold": 0.85,                   # 85% similarity = reproducible
    "runs": 10                           # Number of test runs
}
```

### 3.4 YAML Test Configuration (Promptfoo-Compatible)

```yaml
# prompteval.yaml - Main configuration file

description: "Prompt Library Evaluation Suite"

# Default settings
defaults:
  provider: local:phi4mini
  threshold: 0.75
  max_tokens: 2048
  temperature: 0.3

# Prompts to evaluate
prompts:
  - prompts/advanced/*.md
  - prompts/developers/*.md
  
# Exclude patterns
exclude:
  - "**/README.md"
  - "**/index.md"
  - "**/archive/**"

# Evaluation criteria (overrides defaults)
criteria:
  clarity:
    weight: 0.25
    threshold: 0.70
    
  effectiveness:
    weight: 0.30
    threshold: 0.75
    
  reusability:
    weight: 0.20
    threshold: 0.65
    
  simplicity:
    weight: 0.15
    threshold: 0.60
    
  examples:
    weight: 0.10
    threshold: 0.50

# Test cases (Promptfoo-style assertions)
tests:
  - name: "CoT prompts should have step-based output"
    prompts:
      - prompts/advanced/chain-of-thought*.md
    assertions:
      - type: contains
        value: "Step 1"
      - type: llm-rubric
        value: "The prompt should guide step-by-step reasoning"
        threshold: 0.8
        
  - name: "All prompts should have research foundation"
    prompts:
      - prompts/advanced/*.md
    assertions:
      - type: contains
        value: "Research Foundation"
      - type: frontmatter
        field: "governance_tags"
        
  - name: "Reflection prompts should include self-critique"
    prompts:
      - prompts/advanced/reflection*.md
    assertions:
      - type: contains
        value: "critique"
        case_insensitive: true
      - type: section-exists
        value: "Phase 2"

# Output configuration
output:
  format: markdown
  path: reports/evaluation-{date}.md
  include_details: true
  
# CI/CD integration
ci:
  fail_on_score_below: 70
  fail_on_test_failure: true
  badge_endpoint: /api/badge
```

### 3.5 Python API

```python
from prompteval import PromptEval, GEvalScorer, StructuralAnalyzer
from prompteval.metrics import ClarityMetric, EffectivenessMetric
from prompteval.reporters import MarkdownReporter

# ═══════════════════════════════════════════════════════════════════════════
#                           SIMPLE USAGE
# ═══════════════════════════════════════════════════════════════════════════

# Single prompt evaluation
evaluator = PromptEval()
result = evaluator.evaluate("prompts/advanced/chain-of-thought-concise.md")
print(f"Score: {result.overall_score}%")
print(f"Grade: {result.grade}")  # "Exceptional", "Proficient", etc.

# Directory evaluation
results = evaluator.evaluate_directory("prompts/advanced/")
print(f"Average: {results.average_score}%")
print(f"Passed: {results.passed_count}/{results.total_count}")

# ═══════════════════════════════════════════════════════════════════════════
#                           ADVANCED USAGE
# ═══════════════════════════════════════════════════════════════════════════

# Custom configuration
evaluator = PromptEval(
    model="local:phi4mini",
    tier=3,
    threshold=80,
    rubric="rubrics/enterprise.yaml"
)

# Specific methodologies
result = evaluator.evaluate(
    "prompt.md",
    methods=["structural", "geval", "reproducibility"],
    geval_criteria=["clarity", "effectiveness"],
    reproducibility_runs=10
)

# Access detailed results
print(f"Structural: {result.structural_score}")
print(f"G-Eval: {result.geval_score}")
print(f"Reproducibility: {result.reproducibility_score}%")
print(f"Combined: {result.combined_score}")

# Individual criteria
for criterion, score in result.criteria_scores.items():
    print(f"  {criterion}: {score.value} ({score.grade})")
    print(f"    Reasoning: {score.reasoning}")

# ═══════════════════════════════════════════════════════════════════════════
#                           CUSTOM METRICS
# ═══════════════════════════════════════════════════════════════════════════

from prompteval.metrics import BaseMetric

class SecurityMetric(BaseMetric):
    """Check for security best practices."""
    
    name = "security"
    weight = 0.20
    
    def evaluate(self, prompt_content: str, metadata: dict) -> MetricResult:
        score = 100
        issues = []
        
        # Check for PII handling
        if "PII" not in str(metadata.get("governance_tags", [])):
            score -= 20
            issues.append("Missing PII governance tag")
            
        # Check for injection warnings
        if "injection" not in prompt_content.lower():
            score -= 10
            issues.append("No injection prevention guidance")
            
        return MetricResult(
            value=score,
            issues=issues,
            grade=self._grade(score)
        )

# Register custom metric
evaluator.register_metric(SecurityMetric())

# ═══════════════════════════════════════════════════════════════════════════
#                           COMPARISON & DIFFING
# ═══════════════════════════════════════════════════════════════════════════

from prompteval import compare_prompts

diff = compare_prompts(
    "prompts/v1/cot.md",
    "prompts/v2/cot.md",
    model="local:phi4mini"
)

print(f"Score change: {diff.score_delta:+.1f}%")
print(f"Improved: {diff.improvements}")
print(f"Degraded: {diff.degradations}")

# ═══════════════════════════════════════════════════════════════════════════
#                           BATCH & PARALLEL
# ═══════════════════════════════════════════════════════════════════════════

from prompteval import batch_evaluate

results = batch_evaluate(
    paths=["prompts/advanced/", "prompts/developers/"],
    model="local:phi4mini",
    parallel=4,
    progress=True  # Show progress bar
)

# Export results
results.to_json("results.json")
results.to_markdown("report.md")
results.to_html("dashboard.html")
```

---

## 4. Integration Points

### 4.1 Existing Tools Integration

| Existing Tool | Integration Strategy |
|--------------|---------------------|
| `llm_client.py` | Use directly for model dispatch |
| `local_model.py` | Import for ONNX model evaluation |
| `rubrics/prompt-scoring.yaml` | Load as default rubric |
| `tiered_eval.py` | Port tier logic to new engine |
| `cove_batch_analyzer.py` | Port CoVe scoring to metrics module |
| `evaluate_library.py` | Port unified evaluation logic |

### 4.2 External Tool Inspiration

| Tool | Features to Incorporate |
|------|------------------------|
| **Promptfoo** | YAML test config, assertions, matrix output |
| **DeepEval** | G-Eval implementation, pytest-style testing |
| **RAGAS** | Faithfulness/relevance metrics (for RAG prompts) |
| **LangSmith** | LLM-as-judge patterns, prompt versioning |
| **BERTScore** | Semantic similarity for reproducibility |

### 4.3 CI/CD Integration

```yaml
# .github/workflows/prompt-eval.yml
name: Prompt Evaluation

on:
  push:
    paths:
      - 'prompts/**/*.md'
  pull_request:
    paths:
      - 'prompts/**/*.md'

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
        run: pip install -e ./tools/prompteval
        
      - name: Run evaluation
        run: prompteval test --ci
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          
      - name: Upload report
        uses: actions/upload-artifact@v4
        with:
          name: evaluation-report
          path: reports/
```

---

## 5. Scoring Algorithm

### 5.1 Combined Score Calculation

Based on our research document, the final score combines multiple methodologies:

```python
def calculate_final_score(
    structural: float,       # 0-100
    geval: float,           # 0-100 (normalized from 1-5)
    reproducibility: float  # 0-100 (% similarity)
) -> float:
    """
    Calculate final score using methodology weights.
    
    Weights based on industry research:
    - Structural: 15% (fast, deterministic, catches basics)
    - G-Eval: 70% (main quality assessment)
    - Reproducibility: 15% (consistency matters)
    """
    weights = {
        "structural": 0.15,
        "geval": 0.70,
        "reproducibility": 0.15
    }
    
    final = (
        structural * weights["structural"] +
        geval * weights["geval"] +
        reproducibility * weights["reproducibility"]
    )
    
    return round(final, 1)
```

### 5.2 G-Eval Score Normalization

Per research, normalize 1-5 scale to 0-100%:

```python
def normalize_geval_score(raw_score: float) -> float:
    """
    Normalize G-Eval 1-5 score to 0-100%.
    
    Formula: (score - 1) / 4 * 100
    
    1 → 0%
    2 → 25%
    3 → 50%
    4 → 75%
    5 → 100%
    """
    return (raw_score - 1) / 4 * 100
```

### 5.3 Grade Assignment

```python
def assign_grade(score: float) -> tuple[str, str]:
    """
    Assign grade based on score thresholds.
    
    Returns: (grade_name, emoji_label)
    """
    if score >= 90:
        return ("Exceptional", "⭐⭐⭐⭐⭐")
    elif score >= 80:
        return ("Proficient", "⭐⭐⭐⭐")
    elif score >= 70:
        return ("Competent", "⭐⭐⭐")
    elif score >= 60:
        return ("Developing", "⭐⭐")
    else:
        return ("Inadequate", "⭐")
```

---

## 6. Implementation Phases

### Phase 1: Core Foundation (Week 1-2)

- [ ] Create package structure (`tools/prompteval/`)
- [ ] Implement evaluation engine core
- [ ] Port structural analyzer
- [ ] Implement G-Eval scorer using `local_model.py`
- [ ] Create CLI skeleton with `evaluate` command
- [ ] Basic JSON/console reporter

**Deliverable**: `prompteval evaluate prompts/example.md` works

### Phase 2: Full Evaluation (Week 3-4)

- [ ] Implement all 5 quality metrics per rubric
- [ ] Add reproducibility testing with embedding similarity
- [ ] Implement all evaluation tiers (0-7)
- [ ] Add YAML configuration loader
- [ ] Markdown report generation

**Deliverable**: Multi-tier evaluation with detailed reports

### Phase 3: Testing & Assertions (Week 5-6)

- [ ] Implement Promptfoo-style test runner
- [ ] Add assertion types (contains, llm-rubric, etc.)
- [ ] Parallel test execution
- [ ] CI/CD integration helpers
- [ ] Compare/diff feature

**Deliverable**: `prompteval test prompteval.yaml` works

### Phase 4: Polish & Documentation (Week 7-8)

- [ ] Interactive mode
- [ ] HTML dashboard reporter
- [ ] Custom metric plugin system
- [ ] Comprehensive documentation
- [ ] Migration guide from existing tools

**Deliverable**: Production-ready v1.0

---

## 7. Configuration Schema

### Default Config (`prompteval.defaults.yaml`)

```yaml
# PromptEval Default Configuration
version: "1.0"

# Model settings
model:
  default: "local:phi4mini"
  fallback: "gh:gpt-4o-mini"
  temperature: 0.3
  max_tokens: 2048

# Evaluation settings
evaluation:
  default_tier: 2
  threshold: 70
  
  methods:
    - structural
    - geval
    
  geval:
    model: "local:phi4mini"
    criteria:
      - clarity
      - effectiveness
      - reusability
      - simplicity
      - examples
      
  reproducibility:
    enabled: false
    runs: 5
    threshold: 0.85

# Scoring weights (per enterprise framework)
weights:
  clarity: 0.25
  effectiveness: 0.30
  reusability: 0.20
  simplicity: 0.15
  examples: 0.10

# Rubric source
rubric: "rubrics/prompt-scoring.yaml"

# Output settings
output:
  format: "console"
  verbose: false
  show_reasoning: true
  
# Caching
cache:
  enabled: true
  path: ".prompteval/cache"
  ttl_hours: 24
```

---

## 8. Expected Output Examples

### Console Output

```
$ prompteval evaluate prompts/advanced/chain-of-thought-concise.md

╔══════════════════════════════════════════════════════════════════════════╗
║                         PromptEval Results                                ║
╠══════════════════════════════════════════════════════════════════════════╣
║  File: chain-of-thought-concise.md                                        ║
║  Model: local:phi4mini                                                    ║
║  Tier: 2 (Local Deep)                                                     ║
╚══════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────┐
│ CRITERIA SCORES                                                          │
├───────────────────┬─────────┬────────┬──────────────────────────────────┤
│ Criterion         │ Score   │ Grade  │ Summary                          │
├───────────────────┼─────────┼────────┼──────────────────────────────────┤
│ Clarity           │ 95%     │ ⭐⭐⭐⭐⭐ │ Excellent step-by-step format    │
│ Effectiveness     │ 88%     │ ⭐⭐⭐⭐  │ Works well, could add verify step│
│ Reusability       │ 92%     │ ⭐⭐⭐⭐⭐ │ Highly generic template          │
│ Simplicity        │ 85%     │ ⭐⭐⭐⭐  │ Concise with minor redundancy    │
│ Examples          │ 90%     │ ⭐⭐⭐⭐⭐ │ Excellent debugging example      │
└───────────────────┴─────────┴────────┴──────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ FINAL SCORE                                                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ████████████████████████████████████████░░░░░░░░   90%                │
│                                                                          │
│   Grade: ⭐⭐⭐⭐⭐ EXCEPTIONAL                                              │
│   Status: ✓ PASSED (threshold: 70%)                                     │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

📋 Recommendations:
  1. Consider adding a self-verification step (e.g., "Review your reasoning")
  2. Could include a non-technical use case example

Time: 45.3s | Tokens: 1,234 | Cost: $0.00 (local model)
```

### JSON Output

```json
{
  "file": "prompts/advanced/chain-of-thought-concise.md",
  "timestamp": "2025-12-22T00:15:00Z",
  "model": "local:phi4mini",
  "tier": 2,
  
  "scores": {
    "structural": 88,
    "geval": 90,
    "reproducibility": null,
    "combined": 90
  },
  
  "criteria": {
    "clarity": {"score": 95, "grade": "Exceptional", "reasoning": "..."},
    "effectiveness": {"score": 88, "grade": "Proficient", "reasoning": "..."},
    "reusability": {"score": 92, "grade": "Exceptional", "reasoning": "..."},
    "simplicity": {"score": 85, "grade": "Proficient", "reasoning": "..."},
    "examples": {"score": 90, "grade": "Exceptional", "reasoning": "..."}
  },
  
  "result": {
    "passed": true,
    "threshold": 70,
    "grade": "Exceptional",
    "grade_emoji": "⭐⭐⭐⭐⭐"
  },
  
  "recommendations": [
    "Consider adding a self-verification step",
    "Could include a non-technical use case example"
  ],
  
  "metadata": {
    "duration_seconds": 45.3,
    "tokens_used": 1234,
    "cost_usd": 0.00
  }
}
```

---

## 9. Migration Path

### From Existing Tools

```bash
# Old way (multiple tools)
python tools/evaluate_library.py prompts/
python tools/tiered_eval.py prompts/ -t 3
python tools/cove_batch_analyzer.py prompts/

# New way (unified)
prompteval evaluate prompts/
prompteval evaluate prompts/ --tier 3
prompteval evaluate prompts/ --methods geval,cove
```

### Backward Compatibility

- Keep existing tools functional during transition
- Add deprecation warnings pointing to `prompteval`
- Provide migration script to convert old configs

---

## 10. Success Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| CLI response time (single prompt) | <60s | Benchmark on tier 2 |
| Accuracy vs. expert review | >80% correlation | Compare to manual scoring |
| User adoption | 100% team usage in 30 days | Track CLI invocations |
| CI/CD integration | All PRs evaluated | GitHub Actions metrics |
| Documentation coverage | 100% | All public APIs documented |

---

## Appendix A: Existing Tool Mapping

| Old Tool | New Equivalent |
|----------|---------------|
| `tiered_eval.py` | `prompteval evaluate --tier N` |
| `evaluate_library.py` | `prompteval evaluate DIR` |
| `cove_batch_analyzer.py` | `prompteval evaluate --methods cove` |
| `run_eval_geval.py` | `prompteval evaluate --methods geval` |
| `batch_evaluate.py` | `prompteval evaluate DIR --parallel` |
| `improve_prompts.py` | `prompteval improve FILE` (v1.1) |

---

## Appendix B: Research References

- [G-Eval Paper (NeurIPS 2023)](https://arxiv.org/abs/2303.16634)
- [RubricEval (Stanford)](https://crfm.stanford.edu/papers/rubriceval.pdf)
- [MT-Bench (LMSYS)](https://arxiv.org/abs/2306.05685)
- [RAGAS Framework](https://docs.ragas.io/)
- [DeepEval Documentation](https://docs.deepeval.com/)
- [Promptfoo Documentation](https://www.promptfoo.dev/)
- [BERTScore Paper](https://arxiv.org/abs/1904.09675)
- [Local Research Doc](../docs/prompt-evaluation-research.md)
- [Enterprise Framework](../frameworks/enterprise-prompt-evaluation-framework.md)

---

*Document Version: 1.0 | Last Updated: December 2025*
