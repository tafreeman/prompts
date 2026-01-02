# Prompt Evaluation Scoring Research: Industry Standards & Best Practices

**Research Document** | **Version 1.0** | **December 2025**

---

## Executive Summary

This document compiles research findings on how leading organizations and academic institutions implement prompt evaluation scoring. The goal is to answer: **"How do we determine what makes a 60% score vs. a 90% score?"**

Key findings:

- **Industry standard scales**: 1-5 (G-Eval), 1-4 (Stanford RubricEval), 1-10 (MT-Bench), 0-1 normalized (RAGAS, DeepEval)
- **Default threshold**: 0.5 (50%) is the common pass/fail threshold; production-ready typically ≥0.80 (80%)
- **Reproducibility**: Measured via 10+ executions with semantic similarity scoring (BERTScore ≥0.86 = highly similar)
- **Inter-rater reliability**: Target κ > 0.6 for production use; MT-Bench achieves 80%+ human agreement

---

## 1. Industry Frameworks Analyzed

### 1.1 G-Eval (Microsoft Research / DeepEval)

**Source**: "G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment" (Liu et al., 2023)

**Methodology**:

1. Define evaluation criteria in natural language
2. LLM generates Chain-of-Thought evaluation steps
3. LLM judges output on 1-5 scale
4. Normalize to 0-1 for final score
5. Use probability weighting for fine-grained scores

**Scoring Scale**:

| Score | Meaning | Normalized |
|-------|---------|------------|
| 5 | Excellent | 1.00 |
| 4 | Good | 0.75 |
| 3 | Acceptable | 0.50 |
| 2 | Poor | 0.25 |
| 1 | Bad | 0.00 |

**Default Threshold**: 0.5 (equivalent to "Acceptable")

**Production Threshold**: 0.8+ (equivalent to "Good" or better)

#### Prompt Library Example: Evaluating Chain-of-Thought Prompts

Using G-Eval to score `chain-of-thought-concise.md`:

```yaml
# G-Eval configuration for CoT prompt evaluation
criteria:
  - name: "reasoning_clarity"
    description: "Are reasoning steps clear, logical, and easy to follow?"
    weight: 0.3
    
  - name: "step_completeness"
    description: "Does the prompt guide toward complete step-by-step reasoning?"
    weight: 0.25
    
  - name: "output_structure"
    description: "Is the expected output format clearly specified?"
    weight: 0.2
    
  - name: "variable_clarity"
    description: "Are placeholder variables well-defined and unambiguous?"
    weight: 0.15
    
  - name: "reusability"
    description: "Can this prompt be easily adapted for different use cases?"
    weight: 0.1

evaluation_steps:
  1. Read the prompt and identify the core instruction pattern
  2. Assess if reasoning steps are explicit or implicit
  3. Check if output format is precisely specified
  4. Verify all placeholders have clear definitions
  5. Rate each criterion on 1-5 scale
  6. Calculate weighted average
  
threshold: 0.8  # Production-ready
```

**Example Evaluation**:

```
Prompt: chain-of-thought-concise.md

Reasoning Clarity: 5 (explicit step format with "Step 1, Step 2...")
Step Completeness: 4 (good but could include verification step)
Output Structure: 5 (clear format specification)
Variable Clarity: 4 (variables defined, but examples could be richer)
Reusability: 5 (generic template pattern)

Raw Score: (5×0.3) + (4×0.25) + (5×0.2) + (4×0.15) + (5×0.1) = 4.6/5
Normalized: 0.90 (Exceptional - exceeds production threshold)
```

---

### 1.2 RubricEval (Stanford)

**Source**: "RubricEval: A Scalable Human-LLM Evaluation Framework" (Stanford, 2024)

**Methodology**:

1. Human-generated, instruction-specific rubrics
2. 1-4 scoring scale
3. GPT-4o as evaluator
4. Average across all criteria for instruction score
5. Validated against Chatbot Arena (ρ = 0.98 correlation)

**Scoring Scale**:

| Score | Level | Description |
|-------|-------|-------------|
| 4 | Excellent | Exceeds expectations; exemplary quality |
| 3 | Good | Meets expectations; solid quality |
| 2 | Fair | Partially meets expectations; needs improvement |
| 1 | Poor | Does not meet expectations; significant issues |

**Inter-Rater Reliability**: κ = 0.37 (moderate agreement between human and LLM)

#### Prompt Library Example: Reflection Pattern Evaluation

Applying RubricEval to `reflection-self-critique.md`:

```
RUBRIC: Reflection Pattern Prompt Quality

Criterion 1: Phase Structure (Weight: 25%)
- 4: Clear two-phase structure with explicit phase labels
- 3: Two phases present but boundaries unclear
- 2: Phases exist but poorly defined
- 1: No clear phase structure

Score: 4 (Explicit "Phase 1: Initial Answer" and "Phase 2: Self-Critique")

Criterion 2: Critique Framework Completeness (Weight: 25%)
- 4: 5+ critique dimensions with specific questions
- 3: 3-4 critique dimensions
- 2: 1-2 critique dimensions
- 1: No structured critique

Score: 4 (5 dimensions: Accuracy, Completeness, Quality, Bias, Risk)

Criterion 3: Output Specification (Weight: 20%)
- 4: JSON schema + formatted text + examples
- 3: Clear format + examples
- 2: Basic format guidance
- 1: No format specification

Score: 4 (JSON schema provided, formatted example included)

Criterion 4: Use Case Clarity (Weight: 15%)
- 4: Clear when to use AND when NOT to use
- 3: Clear when to use only
- 2: Vague guidance
- 1: No guidance

Score: 4 (Both "Use When" and "Don't Use When" sections)

Criterion 5: Research Foundation (Weight: 15%)
- 4: Academic citation + explanation of mechanism
- 3: Citation only
- 2: General reference
- 1: No research basis

Score: 4 (Madaan et al. citation with findings summary)

Final Score: (4×0.25) + (4×0.25) + (4×0.20) + (4×0.15) + (4×0.15) = 4.0/4
Percentage: 100% (Exceptional)
```

---

### 1.3 MT-Bench (LMSYS / UC Berkeley)

**Source**: "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (Zheng et al., 2023)

**Methodology**:

1. 80 multi-turn questions across 8 categories
2. GPT-4 as judge
3. 1-10 scoring scale
4. Separate scores for turn 1 and turn 2
5. Average for overall score

**Categories**: Writing, Roleplay, Extraction, Reasoning, Math, Coding, STEM, Humanities

**Human Agreement**: 80%+ between GPT-4 judge and human preferences

**Bias Mitigation**:

- Random order presentation
- Few-shot examples for consistency
- Reference solutions for math/coding

#### Prompt Library Example: Multi-Turn Capability

Evaluating prompt library prompts for multi-turn support:

```
MT-BENCH STYLE EVALUATION

Prompt: react-tool-augmented.md

Turn 1 Evaluation (Initial Task):
- Does prompt support initial task definition? ✓
- Is reasoning structure clear? ✓
- Score: 8/10

Turn 2 Evaluation (Follow-up/Refinement):
- Does prompt handle iteration? ✓ (ReAct loop)
- Is context maintained? ✓ (Observation → Thought cycle)
- Score: 9/10

Average: 8.5/10 (85% - Proficient)

Category Breakdown:
- Reasoning: 9/10 (explicit Thought-Action-Observation)
- Coding: 8/10 (tool integration examples)
- Extraction: 7/10 (could be more specific)
```

---

### 1.4 RAGAS (Retrieval-Augmented Generation Assessment)

**Source**: RAGAS Open Source Framework

**Core Metrics**:

| Metric | What it Measures | Production Threshold |
|--------|-----------------|---------------------|
| Faithfulness | Is answer grounded in context? | ≥0.85 |
| Answer Relevancy | Does answer address the question? | ≥0.70 |
| Context Precision | Is retrieved context relevant? | ≥0.70 |
| Context Recall | Was necessary info retrieved? | ≥0.75 |
| Answer Correctness | Factual accuracy | ≥0.80 |

**Important Note**: "LLM-based metrics can be somewhat non-deterministic as the LLM might not always return the same result for the same input."

#### Prompt Library Example: RAG Prompt Evaluation

Evaluating `rag-document-retrieval.md`:

```python
# RAGAS-style evaluation for RAG prompt
from ragas.metrics import faithfulness, answer_relevancy

evaluation_data = {
    "prompt": "rag-document-retrieval.md",
    "test_queries": [
        {
            "question": "How do I implement document chunking?",
            "context": "[Retrieved documents...]",
            "answer": "[Model response...]",
            "ground_truth": "[Expected answer...]"
        }
    ]
}

results = {
    "faithfulness": 0.92,      # Answer grounded in retrieved docs
    "answer_relevancy": 0.88,  # Addresses the question well
    "context_precision": 0.85, # Retrieved context was relevant
    "context_recall": 0.78,    # Some docs missed but acceptable
}

# Overall assessment
all_pass = all(
    results["faithfulness"] >= 0.85,
    results["answer_relevancy"] >= 0.70,
    results["context_precision"] >= 0.70,
    results["context_recall"] >= 0.75
)
# Result: PASS (all thresholds met)
```

---

### 1.5 Promptfoo

**Source**: Promptfoo Open Source

**Approach**: Assertion-based testing with YAML configuration

**Assertion Types**:

| Type | Description | Example Threshold |
|------|-------------|-------------------|
| `contains` | Output contains string | N/A (boolean) |
| `similar` | Semantic similarity | 0.8 (cosine) |
| `llm-rubric` | LLM judges against criteria | 0.7 |
| `cost` | Token cost limit | $0.01 |
| `latency` | Response time | 2000ms |

**Default Pass Threshold**: 0.5

#### Prompt Library Example: Promptfoo Test Configuration

Testing `chain-of-thought-concise.md`:

```yaml
# promptfoo.yaml for chain-of-thought-concise.md testing
description: "CoT Concise Mode Evaluation"

prompts:
  - file://prompts/advanced/chain-of-thought-concise.md

providers:
  - openai:gpt-4
  - anthropic:claude-3-sonnet

tests:
  # Test 1: Debugging scenario
  - vars:
      DESCRIBE_YOUR_TASK: "Debug API returning 500 errors"
      PROVIDE_RELEVANT_CONTEXT: "PostgreSQL, 50 req/min, connection pool 20"
      LIST_ANY_CONSTRAINTS: "Need quick diagnosis"
    assert:
      # Must contain step-by-step format
      - type: contains
        value: "Step 1"
      - type: contains
        value: "Final Answer"
      
      # Reasoning quality (LLM judge)
      - type: llm-rubric
        value: |
          The response should:
          1. Identify root cause hypotheses
          2. Show logical progression between steps
          3. Provide actionable conclusion
        threshold: 0.8
      
      # Should be concise (under 500 words)
      - type: javascript
        value: output.split(' ').length < 500
      
      # Semantic similarity to expected pattern
      - type: similar
        value: |
          Step 1: Analyze the problem
          Step 2: Consider likely causes
          Step 3: Narrow down possibilities
          Final Answer: Root cause and recommendation
        threshold: 0.7

  # Test 2: Architecture decision
  - vars:
      DESCRIBE_YOUR_TASK: "Choose between microservices or monolith"
      PROVIDE_RELEVANT_CONTEXT: "10 developers, 100k users, new startup"
      LIST_ANY_CONSTRAINTS: "Limited budget, need fast iteration"
    assert:
      - type: llm-rubric
        value: "Response considers trade-offs and provides clear recommendation"
        threshold: 0.75

# Thresholds for overall evaluation
defaultTest:
  threshold: 0.7  # 70% pass rate required
```

---

### 1.6 BERTScore (Semantic Similarity)

**Source**: "BERTScore: Evaluating Text Generation with BERT" (Zhang et al., 2020)

**Methodology**:

1. Tokenize candidate and reference text
2. Generate BERT embeddings for each token
3. Compute pairwise cosine similarity matrix
4. Calculate precision, recall, F1 based on max similarities

**Interpretation**:

| Score Range | Interpretation | What It Means |
|-------------|---------------|---------------|
| 0.90-1.00 | Almost identical | Minor word variations only |
| 0.86-0.89 | Highly similar | Same meaning, different phrasing |
| 0.70-0.85 | Similar | Core message aligned |
| 0.50-0.69 | Partially similar | Some overlap, key differences |
| <0.50 | Dissimilar | Substantially different meaning |

#### Prompt Library Example: Reproducibility Testing

Testing reproducibility of `reflection-self-critique.md`:

```python
import bert_score
from transformers import AutoTokenizer, AutoModel

def test_reproducibility(prompt_path, test_input, n_runs=10):
    """
    Run prompt n times and measure output similarity.
    """
    outputs = []
    for i in range(n_runs):
        response = run_prompt(prompt_path, test_input)
        outputs.append(response)
    
    # Calculate pairwise BERTScore
    similarities = []
    for i in range(len(outputs)):
        for j in range(i+1, len(outputs)):
            P, R, F1 = bert_score.score(
                [outputs[i]], 
                [outputs[j]], 
                lang="en"
            )
            similarities.append(F1.item())
    
    avg_similarity = sum(similarities) / len(similarities)
    return avg_similarity

# Test reflection-self-critique.md
result = test_reproducibility(
    "prompts/advanced/reflection-self-critique.md",
    test_input={
        "USER_QUESTION": "Should we migrate to microservices?",
        "BACKGROUND_AND_CONSTRAINTS": "300K LOC monolith, 30 developers"
    }
)

# Results interpretation
print(f"Reproducibility Score: {result:.2f}")
# 0.92 → Exceptional (>95% equivalent)
# 0.87 → Proficient (85-94% equivalent)  
# 0.78 → Competent (75-84% equivalent)
# 0.65 → Developing (60-74% equivalent)
# <0.60 → Inadequate
```

---

## 2. Threshold Determination Methodology

### 2.1 The Empirical Calibration Process

Based on research, here's how organizations determine valid thresholds:

```
┌─────────────────────────────────────────────────────────────────┐
│         THRESHOLD CALIBRATION PROCESS                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: CREATE GOLD STANDARD DATASET                             │
│                                                                   │
│ • Select 50-100 representative prompts from library               │
│ • Include intentionally good, bad, and borderline examples        │
│ • Have 3+ human experts score each prompt                        │
│ • Calculate inter-rater reliability (target: κ > 0.6)            │
│ • Create consensus scores through discussion                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: RUN AUTOMATED EVALUATION                                 │
│                                                                   │
│ • Apply your evaluation framework to gold standard                │
│ • Record scores for each prompt                                   │
│ • Note any edge cases or failures                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: CALCULATE CORRELATION                                    │
│                                                                   │
│ • Compare automated scores to human consensus                     │
│ • Target Pearson r > 0.7 or Spearman ρ > 0.7                     │
│ • If correlation low, refine criteria and re-evaluate            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: SET THRESHOLDS BASED ON RISK TOLERANCE                   │
│                                                                   │
│ • Examine score distribution vs. human labels                     │
│ • Find cutoff that minimizes false positives/negatives           │
│ • Adjust based on business risk:                                 │
│   - Critical: err toward false negatives (reject good prompts)   │
│   - Low-risk: err toward false positives (accept more broadly)   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: VALIDATE ON HELD-OUT SET                                 │
│                                                                   │
│ • Split data 70/30 (calibration/validation)                      │
│ • Apply thresholds to validation set                             │
│ • Measure precision, recall, F1                                   │
│ • Iterate if necessary                                           │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Risk-Based Threshold Guidelines

| Domain | Pass Threshold | Exceptional | Rationale |
|--------|---------------|-------------|-----------|
| **Healthcare/Finance** | ≥90% | ≥98% | Errors have high cost |
| **Customer-Facing** | ≥80% | ≥92% | User experience matters |
| **Internal Tools** | ≥70% | ≥85% | More tolerance for iteration |
| **Development/Testing** | ≥60% | ≥80% | Focus on rapid improvement |

### 2.3 Prompt Library-Specific Calibration

For your prompt library, suggested approach:

```yaml
# Calibration configuration for tafreeman/prompts
calibration:
  gold_standard_size: 50  # Prompts to manually score
  evaluators: 3           # Number of human raters
  min_kappa: 0.6          # Minimum inter-rater reliability
  
  prompt_categories:
    advanced:
      weight: 1.0         # Full evaluation rigor
      min_score: 80       # Production-ready threshold
      
    developers:
      weight: 0.9
      min_score: 75       # Slightly more permissive
      
    business:
      weight: 0.8
      min_score: 70       # Focus on usability over perfection
      
  dimensions:
    technical_quality:
      weight: 0.25
      criteria:
        - clarity
        - structure
        - advanced_techniques
        
    business_alignment:
      weight: 0.20
      criteria:
        - use_case_fit
        - documentation
        - reusability
        
    security_compliance:
      weight: 0.20
      criteria:
        - pii_safety
        - governance_tags
        - risk_classification
        
    performance:
      weight: 0.15
      criteria:
        - reproducibility
        - token_efficiency
        
    maintainability:
      weight: 0.10
      criteria:
        - version_control
        - related_prompts
        
    innovation:
      weight: 0.10
      criteria:
        - research_foundation
        - technique_adoption
```

---

## 3. Reproducibility: How to Measure "60% vs 90%"

### 3.1 Measurement Protocol

Based on industry standards, reproducibility is measured as follows:

```
REPRODUCIBILITY TEST PROTOCOL
═══════════════════════════════════════════════════════════════════

SETUP
─────
• Fixed inputs: Same test case for all runs
• Fixed parameters: temperature=0.3, top_p=0.9 (or 0 for deterministic)
• Fixed model: Same model version throughout
• Number of runs: 10 minimum, 30 for high-confidence

EXECUTION
─────────
For i in 1..10:
    output[i] = run_prompt(prompt, test_input, params)

COMPARISON METHOD 1: Semantic Similarity (Preferred)
────────────────────────────────────────────────────
For each pair (output[i], output[j]) where i < j:
    similarity[i,j] = BERTScore_F1(output[i], output[j])

average_similarity = mean(all similarity scores)
variance = std(all similarity scores)

COMPARISON METHOD 2: Key Element Matching
─────────────────────────────────────────
Define key elements expected in output:
  - Contains "Step 1"
  - Contains "Final Answer"
  - Includes recommendation
  - Lists 3+ options

For each output:
    element_score = count(elements_present) / total_elements

average_element_score = mean(all element scores)

SCORE CALCULATION
─────────────────
reproducibility_score = (average_similarity * 0.7) + (element_consistency * 0.3)
```

### 3.2 Score Thresholds Explained

**90-100% Reproducibility (Exceptional)**:

```
Example: Chain-of-Thought Concise prompt with structured output

Run 1: "Step 1: Identify the problem. Step 2: Analyze causes..."
Run 2: "Step 1: First, identify the core issue. Step 2: Next, analyze..."
Run 3: "Step 1: Identify what's happening. Step 2: Analyze root causes..."

Analysis:
- All runs have same structure (Step 1, Step 2, Final Answer)
- Core content is equivalent (same meaning)
- Only stylistic word choice differs
- BERTScore F1: 0.93, 0.91, 0.94 (avg: 0.93)
- Result: 93% → Exceptional
```

**60-69% Reproducibility (Developing)**:

```
Example: Vague creative prompt without structure

Run 1: "Here are some ideas: First, consider X. You might also try Y."
Run 2: "I'd recommend starting with Z. Another option is W."
Run 3: "The best approach depends on your situation. Options include..."

Analysis:
- Different opening structure each time
- Core recommendations differ
- Some content overlap but significant variation
- BERTScore F1: 0.68, 0.62, 0.71 (avg: 0.67)
- Result: 67% → Developing
```

### 3.3 Factors Affecting Reproducibility

| Factor | Impact | Mitigation |
|--------|--------|------------|
| **Temperature** | High temp → more variation | Use temp ≤ 0.5 for consistency |
| **Output structure** | Unstructured → more variation | Define explicit output format |
| **Prompt specificity** | Vague → more variation | Be precise about requirements |
| **Few-shot examples** | None → more variation | Include 2-3 examples |
| **Length constraints** | None → more variation | Specify word/token limits |

---

## 4. Prompt Library Evaluation Examples

### 4.1 Comprehensive Evaluation: `chain-of-thought-concise.md`

```yaml
# Full evaluation using enterprise framework

prompt: chain-of-thought-concise.md
evaluator: gpt-4
date: 2025-12-21

dimensions:
  technical_quality:
    score: 92
    breakdown:
      clarity: 95        # Clear instructions, explicit format
      structure: 90      # Logical sections, well-organized
      syntax: 95         # No grammar issues
      advanced_techniques: 88  # Good CoT implementation, could add verification
    notes: "Excellent technical execution. Consider adding self-verification step."
    
  business_alignment:
    score: 88
    breakdown:
      strategic_value: 85    # Addresses common reasoning needs
      use_case_fit: 92       # Well-suited for debugging, decisions
      roi_potential: 85      # 40-60% token reduction claimed
      stakeholder_fit: 90    # Good for technical audiences
    notes: "Strong alignment. Could expand examples for non-technical users."
    
  security_compliance:
    score: 90
    breakdown:
      data_protection: 95    # PII-safe tag, no sensitive data handling
      regulatory: 88         # General-use classification
      risk_mitigation: 85    # Human review guidance included
      privacy: 92            # No PII collection
    notes: "Good governance documentation."
    
  performance_reliability:
    score: 85
    breakdown:
      reproducibility: 88    # Structured output helps consistency
      accuracy: 82           # Depends on model capability
      response_quality: 85   # Good output format
      efficiency: 85         # Token-efficient design
    notes: "Test with 10 runs across models to validate."
    
  maintainability:
    score: 90
    breakdown:
      documentation: 92      # Comprehensive docs, examples, tips
      version_control: 90    # Version 1.0.0, dates tracked
      sustainability: 88     # Model-agnostic design
      modification_ease: 90  # Variables clearly defined
    notes: "Well-documented, easy to modify."
    
  innovation_optimization:
    score: 85
    breakdown:
      creative_solutions: 80    # Standard CoT approach
      efficiency: 90            # Token-efficient variant
      technique_adoption: 85    # Based on arXiv research
      improvement_evidence: 85  # Claims 40-60% reduction
    notes: "Good optimization; research-backed."

final_score: 89  # Weighted average
classification: Proficient (Production-Ready)

recommendations:
  - Add self-verification Step (e.g., "Step N: Verify your reasoning")
  - Include non-technical use case example
  - Add actual token count comparison data
```

### 4.2 Comparative Evaluation: CoT Concise vs. Reflection

```
┌─────────────────────────────────────────────────────────────────┐
│         PROMPT COMPARISON: CoT Concise vs. Reflection            │
├─────────────────────┬─────────────────────┬────────────────────┤
│ Dimension           │ CoT Concise         │ Reflection         │
├─────────────────────┼─────────────────────┼────────────────────┤
│ Technical Quality   │ 92                  │ 95                 │
│ Business Alignment  │ 88                  │ 92                 │
│ Security/Compliance │ 90                  │ 88                 │
│ Performance         │ 85                  │ 78                 │
│ Maintainability     │ 90                  │ 92                 │
│ Innovation          │ 85                  │ 90                 │
├─────────────────────┼─────────────────────┼────────────────────┤
│ FINAL SCORE         │ 89                  │ 90                 │
│ CLASSIFICATION      │ Proficient          │ Exceptional        │
├─────────────────────┴─────────────────────┴────────────────────┤
│ KEY DIFFERENTIATORS:                                            │
│ • Reflection has richer critique framework (+3 Technical)       │
│ • CoT Concise has better token efficiency (+7 Performance)      │
│ • Reflection requires 2x token consumption (cost_multiplier)    │
│ • Both production-ready; choose based on use case               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Key Research Citations

### Academic Papers

1. **Wei, J., et al. (2022)**. "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." *NeurIPS 2022*. [arXiv:2201.11903](https://arxiv.org/abs/2201.11903)

2. **Liu, Y., et al. (2023)**. "G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment." [arXiv:2303.16634](https://arxiv.org/abs/2303.16634)

3. **Madaan, A., et al. (2023)**. "Self-Refine: Iterative Refinement with Self-Feedback." *NeurIPS 2023*. [arXiv:2303.17651](https://arxiv.org/abs/2303.17651)

4. **Zheng, L., et al. (2023)**. "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena." [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)

5. **Zhang, T., et al. (2020)**. "BERTScore: Evaluating Text Generation with BERT." *ICLR 2020*. [arXiv:1904.09675](https://arxiv.org/abs/1904.09675)

6. **Dubois, Y., et al. (2024)**. "RubricEval: A Scalable Human-LLM Evaluation Framework for Open-Ended Tasks." *Stanford*. [crfm.stanford.edu/papers/rubriceval](https://crfm.stanford.edu/papers/rubriceval.pdf)

### Frameworks Referenced

- **RAGAS**: [docs.ragas.io](https://docs.ragas.io/)
- **DeepEval**: [docs.deepeval.com](https://docs.deepeval.com/)
- **Promptfoo**: [promptfoo.dev](https://www.promptfoo.dev/)
- **LangSmith**: [smith.langchain.com](https://smith.langchain.com/)
- **OpenAI Evals**: [github.com/openai/evals](https://github.com/openai/evals)

---

## 6. Summary: Score Determination Formula

### The Bottom Line

**60% vs 90% is determined by**:

1. **Quantitative thresholds** from industry standards (BERTScore, Cohen's κ, pass rates)
2. **Multi-run testing** (10+ executions to measure variance)
3. **Rubric-based evaluation** with explicit criteria and levels
4. **Calibration against human judgment** (target κ > 0.6)
5. **Risk-adjusted thresholds** based on domain criticality

### Quick Reference

```
SCORE DETERMINATION CHECKLIST
═════════════════════════════════════════════════════════════════

□ Did you run the prompt 10+ times to check consistency?
  → Consistency ≥85% = Proficient baseline

□ Did you calculate semantic similarity (BERTScore)?
  → ≥0.86 = Highly similar = 90+ score contribution

□ Did you evaluate against rubric criteria?
  → All 4/4 or 5/5 ratings = Exceptional
  → Mix of 3-4 ratings = Proficient
  → Any 2 or lower = Competent or below

□ Did you compare to human gold standard?
  → Correlation ≥0.7 validates automated scoring

□ Did you weight by dimension importance?
  → Technical Quality (25%) + Business (20%) + Security (20%) + 
    Performance (15%) + Maintainability (10%) + Innovation (10%)

□ Did you apply risk-appropriate pass/fail thresholds?
  → Critical: ≥90%
  → Standard: ≥80%  
  → Development: ≥70%

FINAL SCORE = Weighted average of dimension scores
```

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-21 | Research Team | Initial research compilation |

**Review Cycle**: Quarterly  
**Next Review**: March 2025
