# Prompt Library Evaluation Execution Plan

## Executive Summary

This document outlines the comprehensive strategy for evaluating the `prompts` repository using frontier AI models. The evaluation leverages the library's own evaluation prompts to ensure consistency and demonstrate the library's capabilities.

---

## Available Evaluation Prompts

The library contains **5 specialized evaluation prompts** optimized for different assessment dimensions:

| Prompt | Location | Best For | Scoring |
|--------|----------|----------|---------|
| **Prompt Quality Evaluator** | `prompts/system/prompt-quality-evaluator.md` | Individual prompt assessment | 0-100 (5 dimensions × 20 pts) |
| **Tree-of-Thoughts Repository Evaluator** | `prompts/system/tree-of-thoughts-repository-evaluator.md` | Full repository assessment | 0-100 weighted (A:35%, B:30%, C:35%) |
| **ToT Evaluator + Reflection** | `prompts/advanced/tree-of-thoughts-evaluator-reflection.md` | Enterprise-ready assessment | Two-phase with confidence |
| **Library Visual Audit** | `prompts/system/library-visual-audit.md` | UX/formatting consistency | A-F grade + prioritized fixes |
| **Reflection Self-Critique** | `prompts/advanced/reflection-self-critique.md` | Deep accuracy validation | Phase 1 + Phase 2 critique |

---

## Recommended Evaluation Strategy

### Phase 1: Repository-Level Assessment (30 min)

Use **Tree-of-Thoughts Repository Evaluator** with GPT-5.1 or Claude Opus 4.5:

```
Target: Entire repository structure
Dimensions: 
  - Branch A: Structural & Foundational Integrity (35%)
  - Branch B: Advanced Technique Depth & Accuracy (30%)  
  - Branch C: Enterprise Applicability & Breadth (35%)
Output: Comprehensive markdown report with weighted scores
```

### Phase 2: Individual Prompt Quality (2-3 hours)

Use **Prompt Quality Evaluator** against each prompt category:

| Category | File Count | Priority |
|----------|------------|----------|
| `prompts/advanced/` | 18 prompts | P0 - Critical |
| `prompts/system/` | ~10 prompts | P0 - Critical |
| `prompts/developers/` | ~25 prompts | P1 - High |
| `prompts/business/` | ~15 prompts | P1 - High |
| `prompts/creative/` | ~12 prompts | P2 - Medium |
| `prompts/analysis/` | ~10 prompts | P2 - Medium |

**Scoring Framework (0-100):**
- Clarity & Specificity: 20 pts
- Structure & Completeness: 20 pts  
- Usefulness & Reusability: 20 pts
- Technical Quality: 20 pts
- Ease of Use: 20 pts

**Quality Tiers:**
- Tier 1: 85-100 (Production Ready)
- Tier 2: 70-84 (Needs Minor Improvements)
- Tier 3: 55-69 (Needs Significant Work)
- Tier 4: <55 (Major Revision Required)

### Phase 3: Visual & Formatting Audit (1 hour)

Use **Library Visual Audit** to check:
- Heading hierarchy consistency
- Table alignment and formatting
- Code block language specifiers
- Frontmatter completeness
- Link integrity

### Phase 4: Cross-Model Validation (Optional, 2 hours)

Run the same evaluations across multiple models to identify:
- Scoring variance between models
- Model-specific blind spots
- Consensus areas for improvement

---

## Available Frontier Models

Based on user's available models:

| Model | Recommended Use | Strengths |
|-------|-----------------|-----------|
| **Claude Opus 4.5** | Repository evaluator, deep analysis | Best reasoning, comprehensive |
| **Claude Sonnet 4.5** | Individual prompt evaluation | Fast, accurate, balanced |
| **GPT-5.1-Codex-Max** | Technical prompt assessment | Code-focused, structured output |
| **GPT-5.1** | Tree-of-Thoughts evaluations | Native ToT support |
| **Gemini 3 Pro** | Cross-validation | Alternative perspective |
| **Gemini 2.5 Pro** | Batch processing | Fast throughput |

---

## Execution Commands

### Using `dual_eval.py` (Limited Model Selection)

```bash
# Basic evaluation with default models
python testing/evals/dual_eval.py prompts/advanced/ --format json --output docs/EVAL_ADVANCED.json

# With specific models (gh models supported only)
python testing/evals/dual_eval.py prompts/advanced/ \
  --models "openai/gpt-4.1" \
  --runs 3 \
  --format json \
  --output docs/EVAL_ADVANCED_GPT41.json \
  --log-file docs/EVAL_ADVANCED_GPT41.md
```

### Manual Evaluation (Frontier Models)

For models not supported by `gh models`, use direct model interaction:

1. **Copy the evaluator prompt** from the appropriate file
2. **Replace variables**:
   - `[REPOSITORY_NAME]` → `tafreeman/prompts`
   - `[PASTE_PROMPT_CONTENT_HERE]` → actual prompt content
3. **Run in model interface** (Copilot Chat, Claude, etc.)
4. **Save output** to `docs/evaluations/` directory

### Batch Processing Script

```python
# Suggested approach for batch evaluation
import os
import glob

PROMPTS_DIR = "prompts/advanced"
OUTPUT_DIR = "docs/evaluations"

for prompt_file in glob.glob(f"{PROMPTS_DIR}/*.md"):
    if "index" in prompt_file.lower() or "readme" in prompt_file.lower():
        continue
    
    with open(prompt_file, 'r') as f:
        content = f.read()
    
    # Construct evaluation prompt
    eval_prompt = EVALUATOR_TEMPLATE.replace(
        "[PASTE_PROMPT_CONTENT_HERE]", content
    )
    
    # Send to model API...
```

---

## Expected Outputs

### Per-Model Report Structure

```
docs/evaluations/
├── repository/
│   ├── REPO_EVAL_claude-opus-4.5.md
│   ├── REPO_EVAL_gpt-5.1.md
│   └── REPO_EVAL_gemini-3.md
├── prompts/
│   ├── advanced/
│   │   ├── chain-of-thought-detailed_claude.md
│   │   ├── chain-of-thought-detailed_gpt.md
│   │   └── ...
│   └── developers/
│       └── ...
└── CONSOLIDATED_REPORT.md
```

### Consolidated Report Sections

1. **Executive Summary**
   - Overall repository score (0-100)
   - Cross-model consensus areas
   - Top 5 improvement priorities

2. **Category Breakdown**
   - Average scores by prompt category
   - Model variance per category
   - Best/worst performing prompts

3. **Improvement Roadmap**
   - P0 (Critical): Prompts scoring <55
   - P1 (High): Prompts scoring 55-69
   - P2 (Medium): Prompts scoring 70-84
   - P3 (Polish): Prompts scoring 85+ with minor tweaks

4. **Model-Specific Insights**
   - Which models found which issues
   - Cross-validation confidence levels

---

## Prioritized Evaluation Targets

### Must Evaluate (P0)

These prompts represent the library's flagship capabilities:

1. `prompts/advanced/chain-of-thought-detailed.md`
2. `prompts/advanced/tree-of-thoughts-template.md`
3. `prompts/advanced/reflection-self-critique.md`
4. `prompts/system/prompt-quality-evaluator.md`
5. `prompts/system/tree-of-thoughts-repository-evaluator.md`
6. `prompts/developers/code-review-assistant.md`
7. `prompts/business/strategy-analyzer.md`

### Should Evaluate (P1)

High-value prompts for enterprise adoption:

1. All remaining `prompts/advanced/*.md`
2. All `prompts/system/*.md`
3. All `prompts/developers/*.md` core prompts

### Nice to Evaluate (P2)

Completeness evaluation:

1. `prompts/creative/` folder
2. `prompts/analysis/` folder
3. `prompts/business/` folder

---

## Success Criteria

| Metric | Target | Current |
|--------|--------|---------|
| Repository-level score | 80+ | TBD |
| Advanced prompts avg score | 85+ | TBD |
| System prompts avg score | 90+ | TBD |
| Prompts in Tier 1 (85-100) | 60%+ | TBD |
| Prompts in Tier 4 (<55) | 0% | TBD |
| Cross-model variance | <10 pts | TBD |

---

## Next Steps

1. [ ] Run Tree-of-Thoughts Repository Evaluator with Claude Opus 4.5
2. [ ] Run Prompt Quality Evaluator against `prompts/advanced/` (all models)
3. [ ] Aggregate results into `CONSOLIDATED_REPORT.md`
4. [ ] Update `CONSOLIDATED_IMPROVEMENT_PLAN.md` with findings
5. [ ] Create improvement tickets/tasks for P0 and P1 issues

---

*Generated: 2025-01-XX*
*Version: 1.0*
