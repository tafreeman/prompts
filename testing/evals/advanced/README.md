# 🎓 Advanced Prompts Evaluation

Evaluation test files for advanced prompt engineering techniques and patterns.

## 📋 Overview

This directory contains evaluation prompt files for testing advanced prompting techniques including Chain-of-Thought (CoT), Tree-of-Thoughts (ToT), ReAct, Chain-of-Verification (CoVe), and other sophisticated patterns.

## 📁 Contents

```
advanced/
├── README.md                    # This file
├── advanced-eval-1.prompt.yml   # Batch 1: CoT and reasoning patterns (10 prompts)
├── advanced-eval-2.prompt.yml   # Batch 2: Additional advanced patterns
└── advanced-eval-3.prompt.yml   # Batch 3: Expert-level techniques
```

## 🎯 Purpose

These evaluation files test prompts that implement:

- **Chain-of-Thought (CoT)** - Step-by-step reasoning prompts
- **Tree-of-Thoughts (ToT)** - Multi-path exploration patterns
- **ReAct** - Reasoning + Acting loops
- **Chain-of-Verification (CoVe)** - Self-verifying prompts
- **Reflexion** - Self-critique and improvement
- **Research patterns** - Systematic investigation prompts
- **Debugging patterns** - Root cause analysis prompts
- **Performance analysis** - Profiling and optimization prompts

## 🚀 Quick Start

### Run Evaluations

```bash
# Evaluate with GitHub Models (recommended)
gh models eval testing/evals/advanced/advanced-eval-1.prompt.yml

# Using PromptEval (canonical tool)
python -m prompteval testing/evals/advanced/ --tier 2 --verbose

# Evaluate specific batch
python -m prompteval testing/evals/advanced/advanced-eval-1.prompt.yml --tier 2
```

### Run All Advanced Evaluations

```bash
# Evaluate all advanced prompt batches
for file in testing/evals/advanced/*.prompt.yml; do
    gh models eval "$file"
done

# Or use PromptEval for batch processing
python -m prompteval testing/evals/advanced/ --tier 2 -o results.json
```

## 📊 Evaluation Criteria

Advanced prompts are evaluated on:

| Criterion | Weight | Focus for Advanced |
| ----------- | -------- | ------------------- |
| **Clarity** | 1.0x | Complex instructions must still be clear |
| **Specificity** | 1.2x | Precise steps and expectations |
| **Actionability** | 1.2x | Clear reasoning/action steps |
| **Structure** | 1.3x | Well-organized multi-phase patterns |
| **Completeness** | 1.2x | All reasoning steps covered |
| **Factuality** | 1.0x | Accurate technique descriptions |
| **Consistency** | 1.3x | Reproducible reasoning paths |
| **Safety** | 1.0x | No harmful reasoning patterns |

**Higher standards for advanced prompts:**

- Overall score ≥ 8.0 (vs. 7.0 for basic prompts)
- No dimension < 6.0 (vs. 5.0 for basic prompts)
- Variance ≤ 1.0 (vs. 1.5 for basic prompts)

## 📦 Evaluation Batches

### Batch 1: advanced-eval-1.prompt.yml

**Prompts Evaluated:** 10

**Techniques Covered:**

- Chain-of-Thought (Concise, Detailed, Decision Guide)
- CoT for Debugging & Root Cause Analysis
- CoT for Performance Analysis & Profiling
- Chain-of-Verification (CoVe)
- ReAct for Library Analysis
- ReAct for Large-Scale Redesign
- Advanced Research Patterns

**Key Prompts:**

| Prompt | Technique | Difficulty | Type |
| -------- | ----------- | ------------ | ------ |
| Chain-of-Thought: Concise Mode | CoT | Intermediate | How-to |
| Chain-of-Thought: Detailed Mode | CoT | Intermediate | How-to |
| Chain-of-Thought: Decision Guide | CoT | Beginner | Reference |
| CoT: Debugging & Root Cause Analysis | CoT + Debugging | Intermediate | How-to |
| CoT: Performance Analysis | CoT + Profiling | Intermediate | How-to |
| CoVe | Verification | Advanced | Reference |
| ReAct: Library Structure Analysis | ReAct | Advanced | How-to |
| ReAct: Large-Scale Redesign | ReAct | Advanced | How-to |
| Advanced Prompt Engineering Researcher | ToT + Reflexion | Advanced | How-to |

**Usage:**

```bash
# Evaluate batch 1
gh models eval testing/evals/advanced/advanced-eval-1.prompt.yml

# Or with PromptEval
python -m prompteval testing/evals/advanced/advanced-eval-1.prompt.yml --tier 2
```

### Batch 2: advanced-eval-2.prompt.yml

**Prompts Evaluated:** TBD

**Techniques Covered:**

- Self-Consistency
- Least-to-Most Prompting
- Automatic Reasoning and Tool-use (ART)
- Program-Aided Language Models (PAL)
- Additional advanced patterns

**Status:** 🚧 In Development

### Batch 3: advanced-eval-3.prompt.yml

**Prompts Evaluated:** TBD

**Techniques Covered:**

- Expert-level prompt combinations
- Novel research patterns
- Production optimization techniques

**Status:** 📋 Planned

## 🎯 Expected Results

### Good Advanced Prompt Example

```yaml
Score: 8.7/10 (Grade: A)
Pass: ✅

Dimensions:

- clarity: 9        # Clear step-by-step instructions
- specificity: 9    # Precise reasoning format
- actionability: 9  # Well-defined actions
- structure: 9      # Multi-phase organization
- completeness: 8   # All steps covered
- factuality: 9     # Accurate technique description
- consistency: 9    # Reproducible reasoning
- safety: 9         # No harmful patterns

Strengths:

- Clear reasoning structure with labeled phases
- Comprehensive coverage of technique mechanics
- Well-defined output format
- Practical examples and use cases

Improvements:

- Could add more example outputs
- Consider edge case handling

```

### Common Issues with Advanced Prompts

| Issue | Description | Fix |
| ------- | ------------- | ----- |
| **Overly Complex** | Too many nested steps | Simplify or break into sub-prompts |
| **Unclear Reasoning Format** | Vague step structure | Define explicit step format |
| **Missing Examples** | Theory without practice | Add concrete examples |
| **Incomplete Phases** | Missing key reasoning steps | Add all necessary phases |
| **No Success Criteria** | Unclear completion | Define clear exit conditions |

## 📈 Performance Metrics

### Evaluation Speed

| Batch | Prompts | Avg Time/Prompt | Total Time |
| ------- | --------- | ----------------- | ------------ |
| Batch 1 | 10 | ~45s | ~7.5 min |
| Batch 2 | TBD | ~45s | TBD |
| Batch 3 | TBD | ~45s | TBD |

**Note:** Advanced prompts take longer to evaluate due to complexity and length.

### Historical Scores

| Batch | Avg Score | Pass Rate | Common Grade |
| ------- | ----------- | ----------- | -------------- |
| Batch 1 | 8.3/10 | 90% | B+ |
| Batch 2 | TBD | TBD | TBD |
| Batch 3 | TBD | TBD | TBD |

## 🔧 Evaluation Configuration

### Evaluator Configuration

```yaml
model: openai/gpt-4o-mini
modelParameters:
  temperature: 0.3      # Lower for consistent scoring
  max_tokens: 2000      # Higher for detailed analysis

evaluators:

  - name: valid-json

    description: Response must be valid JSON

  - name: has-overall-score

    description: Includes overall score

  - name: has-grade

    description: Includes letter grade

  - name: has-reasoning

    description: Chain-of-thought reasoning

  - name: has-safety-score

    description: Safety evaluation
```

### Custom Evaluators for Advanced Prompts

```yaml
evaluators:
  # Standard evaluators

  - name: valid-json
  - name: has-overall-score

  # Advanced-specific evaluators

  - name: has-reasoning-structure

    description: Evaluates reasoning step structure
    string:
      contains: '"reasoning_quality"'

  - name: has-phase-evaluation

    description: Evaluates multi-phase organization
    string:
      contains: '"phase_clarity"'

  - name: has-technique-accuracy

    description: Validates technique implementation
    string:
      contains: '"technique_accuracy"'
```

## 🐛 Troubleshooting

### Evaluation Takes Too Long

Advanced prompts are longer and take more time:

```bash
# Use faster model for initial testing
gh models eval file.prompt.yml --model openai/gpt-4o-mini

# Reduce number of runs
python -m prompteval file.prompt.yml --runs 1 --tier 2
```

### Low Scores

Common reasons for low scores in advanced prompts:

1. **Unclear Reasoning Format**
   - Fix: Define explicit step format with examples

2. **Too Complex**
   - Fix: Break into smaller sub-prompts

3. **Missing Context**
   - Fix: Add more background and examples

4. **Inconsistent Terminology**
   - Fix: Use standard technique names and definitions

### JSON Parsing Errors

```bash
# Validate YAML syntax
yamllint testing/evals/advanced/advanced-eval-1.prompt.yml

# Check for special characters in prompt content
# Escape curly braces: {{ becomes {{{ }}} becomes }}}
```

## 📖 See Also

- [../README.md](../README.md) - Evals directory overview
- [../analysis/README.md](../analysis/README.md) - Analysis prompts evaluation
- [../business/README.md](../business/README.md) - Business prompts evaluation
- [../system/README.md](../system/README.md) - System prompts evaluation
- [../results/README.md](../results/README.md) - Evaluation results
- [../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md](../../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md) - Scoring methodology

---

**Built with ❤️ for advanced prompt engineering excellence**
