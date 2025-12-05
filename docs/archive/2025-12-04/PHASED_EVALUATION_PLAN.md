# Phased Prompt Library Evaluation Plan

## Executive Summary

This document outlines a comprehensive, phased approach to evaluating all prompts in the `tafreeman/prompts` library using `gh models eval` and industry best practices. The plan covers:

- **Total Prompts to Evaluate**: ~150 prompts across 8 categories
- **Evaluation Methodology**: Multi-run statistical validation with model rotation
- **Timeline**: 4-6 weeks (phased rollout)
- **Success Criteria**: 90%+ prompts achieving passing scores (≥7.0/10)

---

## Table of Contents

1. [Prompt Inventory](#1-prompt-inventory)
2. [Evaluation Methodology](#2-evaluation-methodology)
3. [Model Selection Strategy](#3-model-selection-strategy)
4. [Phased Execution Plan](#4-phased-execution-plan)
5. [Statistical Best Practices](#5-statistical-best-practices)
6. [Improvement Prompts Reference](#6-improvement-prompts-reference)
7. [Automation Scripts](#7-automation-scripts)
8. [Success Metrics](#8-success-metrics)

---

## 1. Prompt Inventory

### Category Breakdown

| Category | Prompt Count | Priority | Complexity | Est. Eval Time |
| :--- |-------------| :--- |------------| :--- |
| `developers/` | 24 | P1 ✅ | High | Completed |
| `analysis/` | 21 | P1 | High | Week 1 |
| `business/` | 38 | P1 | Medium | Week 2 |
| `m365/` | 20 | P2 | Medium | Week 2 |
| `system/` | 24 | P2 | High | Week 3 |
| `advanced/` | 18 | P3 | Very High | Week 3-4 |
| `creative/` | 9 | P3 | Low | Week 4 |
| `governance/` | 3 | P4 | Medium | Week 4 |
| **Total** | **~157** | | | **4-6 weeks** |

### Priority Rationale

- **P1 (Critical)**: High-usage categories affecting core workflows (developers, analysis, business)
- **P2 (Important)**: Platform-specific or infrastructure prompts (m365, system)
- **P3 (Standard)**: Advanced patterns and creative content (advanced, creative)
- **P4 (Low)**: Governance/compliance (smaller scope, specialized use)

---

## 2. Evaluation Methodology

### Dual Rubric System

We use two complementary evaluation frameworks:

#### Quality Standards Rubric (0-100 scale)

| Dimension | Weight | Description |
| :--- |--------| :--- |
| Completeness | 25% | All required sections present |
| Example Quality | 30% | Realistic, complete examples |
| Specificity | 20% | Clear instructions, no ambiguity |
| Format | 15% | Proper structure and metadata |
| Enterprise | 10% | Governance, compliance tags |

#### Effectiveness Rubric (1.0-5.0 scale)

| Dimension | Weight | Description |
| :--- |--------| :--- |
| Clarity | 25% | Understandable in <30 seconds |
| Effectiveness | 30% | Achieves stated goal |
| Reusability | 20% | Parameterized, adaptable |
| Simplicity | 15% | Not overly complex |
| Examples | 10% | Quality of demonstrations |

### Pass/Fail Criteria

```yaml
passing_criteria:
  overall_score: ">= 7.0/10"
  no_criterion_below: "5.0"
  required_metadata:
    - title
    - description
    - use_cases (min 3)
    - variables
    - example_usage

failing_indicators:
  - word_count: "< 30 words in prompt body"
  - missing_yaml_frontmatter: true
  - no_example_usage: true
  - placeholder_only_examples: true
```sql
---

## 3. Model Selection Strategy

### Evaluation Models (Graders)

Based on research from OpenAI, Anthropic, and Microsoft best practices:

| Model | Role | Strengths | Use Case |
| :--- |------| :--- |----------|
| **GPT-4o-mini** | Primary Grader | Fast, cost-effective, consistent | Standard evaluations |
| **Claude 3.5 Sonnet** | Secondary Grader | Strong reasoning, catches nuance | Cross-validation |
| **GPT-4o** | Tie-breaker | High accuracy | Disputed scores |
| **o1-mini** | Advanced Patterns | Deep reasoning | CoT/ToT/ReAct prompts |

### Model Rotation Strategy

For statistical reliability, rotate models across runs:

```text
Run 1: GPT-4o-mini (baseline)
Run 2: Claude 3.5 Sonnet (cross-validation)
Run 3: GPT-4o-mini (confirmation)
Run 4: GPT-4o (if variance > 1.5 points)
Run 5: o1-mini (for advanced/* prompts only)
```text
### Generator Models (for Improvement)

When improving prompts, use different models for different tasks:

| Task | Recommended Model | Reason |
| :--- |------------------| :--- |
| **Content Generation** | Claude Sonnet 4 | Strong writing, follows instructions |
| **Technical Prompts** | GPT-4o | Good code examples |
| **Refactoring** | Claude Sonnet 4 | Maintains structure |
| **Adding CoT/ToT** | o1-mini | Native reasoning patterns |

---

## 4. Phased Execution Plan

### Phase 1: Analysis Prompts (Week 1)

**Scope**: 21 prompts in `prompts/analysis/`

```bash
# Generate eval files
python testing/evals/generate_eval_files.py prompts/analysis --output testing/evals/analysis

# Run evaluations (3 runs per prompt)
python testing/evals/run_gh_eval.py testing/evals/analysis --runs 3 --model gpt-4o-mini
python testing/evals/run_gh_eval.py testing/evals/analysis --runs 1 --model claude-3.5-sonnet

# Generate report
python tools/evaluate_library.py --category analysis --output docs/reports/ANALYSIS_EVAL_REPORT.md
```text
**Batch Strategy**:
- Batch 1: Market Research prompts (6 prompts)
- Batch 2: Data Analysis prompts (8 prompts)
- Batch 3: Strategic Analysis prompts (7 prompts)

### Phase 2: Business + M365 Prompts (Week 2)

**Scope**: 58 prompts (38 business + 20 m365)

```bash
# Business prompts
python testing/evals/generate_eval_files.py prompts/business --output testing/evals/business
python testing/evals/run_gh_eval.py testing/evals/business --runs 3 --model gpt-4o-mini

# M365 prompts
python testing/evals/generate_eval_files.py prompts/m365 --output testing/evals/m365
python testing/evals/run_gh_eval.py testing/evals/m365 --runs 3 --model gpt-4o-mini
```text
**Batch Strategy**:
- Business Batch 1: Project Management (10 prompts)
- Business Batch 2: Communication (12 prompts)
- Business Batch 3: Strategy (16 prompts)
- M365 Batch 1: Productivity (10 prompts)
- M365 Batch 2: Designer/Creative (10 prompts)

### Phase 3: System + Advanced Prompts (Week 3-4)

**Scope**: 42 prompts (24 system + 18 advanced)

```bash
# System prompts (use stronger model for architecture prompts)
python testing/evals/generate_eval_files.py prompts/system --output testing/evals/system
python testing/evals/run_gh_eval.py testing/evals/system --runs 3 --model gpt-4o

# Advanced prompts (require specialized evaluation)
python testing/evals/generate_eval_files.py prompts/advanced --output testing/evals/advanced
python testing/evals/run_gh_eval.py testing/evals/advanced --runs 5 --model o1-mini
```text
**Special Handling for Advanced Prompts**:
- CoT prompts: Verify reasoning chain quality
- ToT prompts: Check multi-branch structure
- ReAct prompts: Validate tool-use patterns
- RAG prompts: Assess context management

### Phase 4: Creative + Governance (Week 4)

**Scope**: 12 prompts (9 creative + 3 governance)

```bash
# Creative prompts
python testing/evals/generate_eval_files.py prompts/creative --output testing/evals/creative
python testing/evals/run_gh_eval.py testing/evals/creative --runs 3 --model gpt-4o-mini

# Governance prompts
python testing/evals/generate_eval_files.py prompts/governance --output testing/evals/governance
python testing/evals/run_gh_eval.py testing/evals/governance --runs 3 --model gpt-4o
```text
---

## 5. Statistical Best Practices

### Number of Runs per Prompt

Based on LLM evaluation research:

| Prompt Complexity | Minimum Runs | Recommended | Rationale |
| :--- |--------------| :--- |-----------|
| Simple (creative) | 3 | 3 | Low variance expected |
| Standard (business) | 3 | 5 | Moderate variance |
| Complex (developers) | 3 | 5 | Higher variance |
| Advanced (CoT/ToT) | 5 | 7 | High variance in reasoning |

### Variance Handling

```python
def determine_score(runs: list[float]) -> tuple[float, str]:
    """
    Determine final score from multiple runs.
    
    Returns: (final_score, confidence_level)
    """
    mean = statistics.mean(runs)
    stdev = statistics.stdev(runs) if len(runs) > 1 else 0
    
    if stdev <= 0.5:
        return mean, "high"  # Consistent scoring
    elif stdev <= 1.0:
        return mean, "medium"  # Acceptable variance
    else:
        # High variance - need additional runs or manual review
        return statistics.median(runs), "low"
```text
### Inter-Rater Reliability

When using multiple models as graders:

```python
def cross_validate_scores(model_a_scores: dict, model_b_scores: dict) -> dict:
    """
    Compare scores between two grader models.
    Flag significant disagreements (>1.5 point difference).
    """
    disagreements = {}
    
    for prompt_id, score_a in model_a_scores.items():
        score_b = model_b_scores.get(prompt_id)
        if score_b and abs(score_a - score_b) > 1.5:
            disagreements[prompt_id] = {
                "model_a": score_a,
                "model_b": score_b,
                "delta": abs(score_a - score_b),
                "action": "manual_review"
            }
    
    return disagreements
```text
### Confidence Intervals

Report scores with confidence intervals:

```yaml
Prompt: code-review-expert.md
Score: 8.2 ± 0.4 (95% CI)
Runs: [8.0, 8.5, 8.1, 8.0, 8.4]
Confidence: High
```text
---

## 6. Improvement Prompts Reference

### Primary Improvement Prompts

The following prompts in this library are specifically designed to improve other prompts:

#### 1. Prompt Quality Evaluator
**Location**: `prompts/system/prompt-quality-evaluator.md`
**Use For**: Comprehensive meta-evaluation with 5-dimensional scoring

```text
Key Features:
- 5-dimensional scoring framework (Clarity, Structure, Usefulness, Technical, Ease of Use)
- Phase 1: Initial Evaluation
- Phase 2: Self-Critique and Reflection
- Prioritized recommendations (P0-P3)
- Before/after improvement examples
```text
**Best For**: Individual prompt deep-dive assessment

#### 2. Tree-of-Thoughts Repository Evaluator
**Location**: `prompts/system/tree-of-thoughts-repository-evaluator.md`
**Use For**: Repository-wide or category-wide assessment

```text
Key Features:
- Multi-branch reasoning (ToT pattern)
- 3 evaluation branches:
  - Branch A: Structural & Foundational Integrity (35%)
  - Branch B: Advanced Technique Depth (30%)
  - Branch C: Enterprise Applicability (35%)
- Cross-branch synthesis
- Executive summary generation
```text
**Best For**: Batch evaluation of prompt categories

#### 3. Reflection: Self-Critique Pattern
**Location**: `prompts/advanced/reflection-self-critique.md`
**Use For**: Improving individual prompt answers

```text
Key Features:
- Two-phase pattern (Initial Answer → Self-Critique)
- 5 critique dimensions (Accuracy, Completeness, Quality, Bias, Risk)
- Confidence level assessment
- Actionable revision generation
```text
**Best For**: Iterative prompt refinement

### Improvement Workflow

```mermaid
flowchart TD
    A[Run gh models eval] --> B{Score >= 7.0?}
    B -->|Yes| C[Document in Report]
    B -->|No| D[Identify Issues]
    
    D --> E{Issue Type?}
    
    E -->|Structure/Completeness| F[Use Prompt Quality Evaluator]
    E -->|Reasoning Depth| G[Use ToT Repository Evaluator]
    E -->|Specific Answer Quality| H[Use Reflection Pattern]
    
    F --> I[Generate Improvement Recommendations]
    G --> I
    H --> I
    
    I --> J[Apply Improvements]
    J --> K[Re-run Evaluation]
    K --> B
```text
### Model Selection for Improvements

| Improvement Task | Recommended Model | Improvement Prompt |
| :--- |------------------| :--- |
| Add missing sections | Claude Sonnet 4 | Prompt Quality Evaluator |
| Add examples | GPT-4o | Prompt Quality Evaluator |
| Add CoT reasoning | o1-mini | Native reasoning |
| Restructure prompt | Claude Sonnet 4 | ToT Repository Evaluator |
| Fix ambiguity | GPT-4o | Reflection Pattern |
| Add enterprise metadata | Claude Sonnet 4 | Prompt Quality Evaluator |

---

## 7. Automation Scripts

### Master Evaluation Script

Create `tools/run_full_evaluation.py`:

```python
#!/usr/bin/env python3
"""
Master evaluation script for phased prompt library evaluation.
"""

import argparse
import subprocess
from pathlib import Path
from dataclasses import dataclass

@dataclass
class EvaluationPhase:
    name: str
    categories: list[str]
    model: str
    runs: int
    priority: int

PHASES = [
    EvaluationPhase("Phase 1", ["analysis"], "gpt-4o-mini", 3, 1),
    EvaluationPhase("Phase 2a", ["business"], "gpt-4o-mini", 3, 1),
    EvaluationPhase("Phase 2b", ["m365"], "gpt-4o-mini", 3, 2),
    EvaluationPhase("Phase 3a", ["system"], "gpt-4o", 3, 2),
    EvaluationPhase("Phase 3b", ["advanced"], "o1-mini", 5, 3),
    EvaluationPhase("Phase 4", ["creative", "governance"], "gpt-4o-mini", 3, 4),
]

def run_phase(phase: EvaluationPhase, base_dir: Path):
    """Execute evaluation for a single phase."""
    for category in phase.categories:
        # Generate eval files
        subprocess.run([
            "python", "testing/evals/generate_eval_files.py",
            f"prompts/{category}",
            "--output", f"testing/evals/{category}"
        ], check=True)
        
        # Run evaluations
        for run in range(phase.runs):
            subprocess.run([
                "python", "testing/evals/run_gh_eval.py",
                f"testing/evals/{category}",
                "--model", phase.model,
                "--run", str(run + 1)
            ], check=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", type=int, help="Run specific phase (1-4)")
    parser.add_argument("--all", action="store_true", help="Run all phases")
    args = parser.parse_args()
    
    base_dir = Path(__file__).parent.parent
    
    if args.all:
        for phase in PHASES:
            print(f"\n{'='*60}")
            print(f"Running {phase.name}: {phase.categories}")
            print(f"{'='*60}\n")
            run_phase(phase, base_dir)
    elif args.phase:
        matching = [p for p in PHASES if p.priority == args.phase]
        for phase in matching:
            run_phase(phase, base_dir)

if __name__ == "__main__":
    main()
```text
### Cross-Validation Script

Create `tools/cross_validate_evals.py`:

```python
#!/usr/bin/env python3
"""
Cross-validate evaluation results between multiple grader models.
"""

import json
from pathlib import Path
from collections import defaultdict

def load_results(results_dir: Path) -> dict:
    """Load evaluation results from JSON files."""
    results = defaultdict(list)
    for file in results_dir.glob("*.json"):
        with open(file) as f:
            data = json.load(f)
            for prompt_id, scores in data.items():
                results[prompt_id].extend(scores)
    return results

def calculate_agreement(model_a: dict, model_b: dict) -> dict:
    """Calculate inter-rater agreement statistics."""
    agreements = []
    disagreements = []
    
    for prompt_id in model_a:
        if prompt_id in model_b:
            score_a = sum(model_a[prompt_id]) / len(model_a[prompt_id])
            score_b = sum(model_b[prompt_id]) / len(model_b[prompt_id])
            delta = abs(score_a - score_b)
            
            if delta <= 1.0:
                agreements.append(prompt_id)
            else:
                disagreements.append({
                    "prompt": prompt_id,
                    "model_a_score": round(score_a, 2),
                    "model_b_score": round(score_b, 2),
                    "delta": round(delta, 2)
                })
    
    total = len(agreements) + len(disagreements)
    return {
        "agreement_rate": round(len(agreements) / total * 100, 1) if total > 0 else 0,
        "total_prompts": total,
        "agreements": len(agreements),
        "disagreements": disagreements
    }

def main():
    # Load results from different models
    results_dir = Path("testing/evals/results")
    
    gpt4o_results = load_results(results_dir / "gpt-4o-mini")
    claude_results = load_results(results_dir / "claude-3.5-sonnet")
    
    # Calculate agreement
    agreement = calculate_agreement(gpt4o_results, claude_results)
    
    print(f"\n{'='*60}")
    print("Cross-Validation Report")
    print(f"{'='*60}\n")
    print(f"Agreement Rate: {agreement['agreement_rate']}%")
    print(f"Total Prompts: {agreement['total_prompts']}")
    print(f"Agreements: {agreement['agreements']}")
    print(f"Disagreements: {len(agreement['disagreements'])}")
    
    if agreement['disagreements']:
        print("\nDisagreements requiring manual review:")
        for d in agreement['disagreements']:
            print(f"  - {d['prompt']}: GPT-4o={d['model_a_score']}, Claude={d['model_b_score']} (Δ={d['delta']})")

if __name__ == "__main__":
    main()
```text
---

## 8. Success Metrics

### Phase Completion Criteria

| Metric | Target | Measurement |
| :--- |--------| :--- |
| Pass Rate | ≥ 90% | Prompts scoring ≥ 7.0/10 |
| Average Score | ≥ 7.5/10 | Mean across all evaluations |
| Score Variance | ≤ 0.5 | Standard deviation per prompt |
| Inter-Rater Agreement | ≥ 85% | Agreement between grader models |
| Improvement Cycle Time | ≤ 2 hours | Time to improve a failing prompt |

### Dashboard Metrics

Track these metrics weekly:

```markdown
## Weekly Evaluation Dashboard

### Phase Progress
- [ ] Phase 1: Analysis (0/21 complete)
- [ ] Phase 2a: Business (0/38 complete)
- [ ] Phase 2b: M365 (0/20 complete)
- [ ] Phase 3a: System (0/24 complete)
- [ ] Phase 3b: Advanced (0/18 complete)
- [ ] Phase 4: Creative+Governance (0/12 complete)

### Quality Metrics
| Category | Evaluated | Passing | Pass Rate | Avg Score |
| :--- |-----------| :--- |-----------| :--- |
| developers | 24 | 23 | 96% | 7.9 |
| analysis | :--- | - | :--- | - |
| business | :--- | - | :--- | - |
| m365 | :--- | - | :--- | - |
| system | :--- | - | :--- | - |
| advanced | :--- | - | :--- | - |
| creative | :--- | - | :--- | - |
| governance | :--- | - | :--- | - |

### Improvement Backlog
| Priority | Count | Avg Score | Primary Issue |
| :--- |-------| :--- |---------------|
| P0 (Critical) | 0 | :--- | - |
| P1 (High) | 1 | 6.75 | Missing structure |
| P2 (Medium) | 0 | :--- | - |
```

### Final Success Criteria

The evaluation plan is complete when:

1. **Coverage**: All 157 prompts evaluated at least 3 times
2. **Quality**: 90%+ pass rate across all categories
3. **Consistency**: Inter-rater agreement ≥ 85%
4. **Documentation**: All evaluation results documented in `docs/reports/`
5. **Improvements**: All P0/P1 issues resolved
6. **Automation**: Scripts validated and documented

---

## Appendix: Quick Reference

### 🤖 Autonomous Agent (Recommended)

Run the entire evaluation pipeline without intervention:

```bash
# Full autonomous evaluation - runs everything end-to-end
python tools/evaluation_agent.py --full

# Dry run - see what would happen without executing
python tools/evaluation_agent.py --full --dry-run

# Resume from last checkpoint if interrupted
python tools/evaluation_agent.py --resume

# Run specific phase only
python tools/evaluation_agent.py --phase 1

# Verbose logging
python tools/evaluation_agent.py --full --verbose
```text
**What the agent does automatically:**
1. ✅ Checks prerequisites (Python, gh CLI, gh-models extension)
2. ✅ Generates eval files for each category
3. ✅ Runs evaluations with appropriate models per category
4. ✅ Parses results and calculates pass/fail metrics
5. ✅ Generates improvement plan for failing prompts
6. ✅ Creates comprehensive reports
7. ✅ Saves checkpoints for resume capability

**Output files:**
- `docs/reports/EVALUATION_REPORT.md` - Full library assessment
- `docs/reports/AGENT_EXECUTION_SUMMARY.md` - Agent run summary
- `docs/reports/IMPROVEMENT_PLAN.md` - Failing prompts action items
- `logs/eval_agent_*.log` - Detailed execution log

---

### Manual Command Cheat Sheet

For manual step-by-step execution:

```bash
# Generate eval files for a category
python testing/evals/generate_eval_files.py prompts/[CATEGORY] --output testing/evals/[CATEGORY]

# Run single evaluation
gh models eval testing/evals/[CATEGORY]/[PROMPT].prompt.yml

# Run batch evaluation with multiple runs
python testing/evals/run_gh_eval.py testing/evals/[CATEGORY] --runs 3 --model gpt-4o-mini

# Generate improvement recommendations
python tools/improve_prompts.py --input prompts/[CATEGORY]/[PROMPT].md --output improvements/

# Full library evaluation
python tools/evaluate_library.py --all --output docs/EVALUATION_REPORT.md

# Cross-validate between models
python tools/cross_validate_evals.py --model-a gpt-4o-mini --model-b claude-3.5-sonnet
```text
### Evaluation File Structure

```text
testing/
├── evals/
│   ├── developers/
│   │   ├── code-review-expert.prompt.yml
│   │   └── ...
│   ├── analysis/
│   ├── business/
│   ├── m365/
│   ├── system/
│   ├── advanced/
│   ├── creative/
│   └── governance/
│   └── results/
│       ├── gpt-4o-mini/
│       └── claude-3.5-sonnet/
```text
### Priority Issue Definitions

| Priority | Definition | Response Time | Example |
| :--- |------------| :--- |---------|
| P0 | Prompt is broken/unusable | Immediate | <30 words, missing metadata |
| P1 | Major quality issues | Within phase | No examples, unclear goal |
| P2 | Moderate improvements needed | Next cycle | Generic examples, missing tips |
| P3 | Minor enhancements | Backlog | Formatting, additional links |

---

*Last Updated: 2025-01-07*
*Version: 1.0*
*Author: GitHub Copilot*
