---
name: Enterprise Prompt Evaluation Framework
description: A comprehensive, multi-model compatible evaluation framework for assessing enterprise AI prompts across six dimensions - Technical Quality, Business Alignment, Security, Performance, Maintainability, and Innovation.
type: reference
---

# Enterprise GenAI Prompt Evaluation Framework

**Version 2.0** | **Multi-Model Compatible** | **Last Updated: December 2025**

## Description

This framework provides a rigorous, quantitative methodology for evaluating AI prompts in enterprise environments. It defines six weighted dimensions (Technical Quality 25%, Business Alignment 20%, Security & Compliance 20%, Performance 15%, Maintainability 10%, Innovation 10%), detailed scoring rubrics with concrete thresholds, testing protocols, and approval workflows. Designed for governance teams, prompt engineers, and AI platform administrators.

## Section 2: Evaluation Framework

### 2.1 Dimension Overview

The framework evaluates prompts across six core dimensions, each weighted according to its strategic importance to enterprise AI governance:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    EVALUATION DIMENSION WEIGHTS                          │
├─────────────────────────────────────────────────────────────────────────┤
│  Technical Quality          ████████████████████████████████  25%       │
│  Business Alignment         █████████████████████████         20%       │
│  Security & Compliance      █████████████████████████         20%       │
│  Performance & Reliability  ███████████████████               15%       │
│  Maintainability            █████████████                     10%       │
│  Innovation & Optimization  █████████████                     10%       │
└─────────────────────────────────────────────────────────────────────────┘
                                                          TOTAL: 100%
```

### 2.2 Detailed Dimension Descriptions

#### Dimension 1: Technical Quality (25%)

**Definition**: Evaluates prompt construction excellence, including clarity, syntax, structure, and utilization of advanced prompting techniques.

**Evaluation Criteria**:

- **Clarity & Precision**: Unambiguous language, specific terminology, clear instructions
- **Structural Integrity**: Logical organization, proper formatting, section coherence
- **Syntax Correctness**: Grammatical accuracy, consistent style, appropriate punctuation
- **Advanced Technique Utilization**: Implementation of CoT, Few-Shot, ToT, ReAct, and other methodologies

**Weight Rationale**: Technical quality forms the foundation of prompt effectiveness. Poor construction directly impacts output quality across all use cases, making it the highest-weighted dimension.

#### Dimension 2: Business Alignment (20%)

**Definition**: Assesses strategic value, use case appropriateness, ROI potential, and organizational goal support.

**Evaluation Criteria**:

- **Strategic Value**: Contribution to organizational objectives and priorities
- **Use Case Fit**: Appropriateness for intended application domain
- **ROI Potential**: Cost-benefit analysis and efficiency gains
- **Stakeholder Requirements**: Alignment with business user needs and expectations

**Weight Rationale**: Prompts must deliver business value to justify governance investment. Strong technical prompts that don't serve organizational needs waste resources and create governance overhead.

#### Dimension 3: Security & Compliance (20%)

**Definition**: Evaluates data protection measures, regulatory adherence, risk mitigation, and privacy safeguards.

**Evaluation Criteria**:

- **Data Protection**: Handling of sensitive information, PII safeguards, data minimization
- **Regulatory Compliance**: GDPR, CCPA, HIPAA, industry-specific requirements
- **Risk Mitigation**: Prompt injection prevention, output validation, guardrails
- **Privacy Safeguards**: User consent considerations, data retention policies

**Weight Rationale**: Equal weight to business alignment reflects the critical importance of security in enterprise AI. Compliance failures carry significant legal, financial, and reputational risks.

#### Dimension 4: Performance & Reliability (15%)

**Definition**: Measures output consistency, accuracy, response quality, and operational effectiveness.

**Evaluation Criteria**:

- **Output Consistency**: Reproducible results across multiple executions
- **Accuracy**: Factual correctness and alignment with expected outcomes
- **Response Quality**: Completeness, relevance, and usefulness of outputs
- **Operational Effectiveness**: Token efficiency, latency optimization, error handling

**Weight Rationale**: Performance directly impacts user experience and operational costs. While important, it can often be improved iteratively after deployment.

#### Dimension 5: Maintainability (10%)

**Definition**: Assesses documentation quality, version control practices, sustainability, and ease of modification.

**Evaluation Criteria**:

- **Documentation**: Clear purpose statements, usage instructions, example outputs
- **Version Control**: Change history, deprecation notices, migration guides
- **Sustainability**: Long-term viability, model-agnostic design, update ease
- **Modification Ease**: Modular structure, clear parameterization, extension points

**Weight Rationale**: Long-term governance requires maintainable prompts. Lower weight reflects that maintainability issues, while important, are typically recoverable.

#### Dimension 6: Innovation & Optimization (10%)

**Definition**: Evaluates creative problem-solving, efficiency improvements, and advanced technique adoption.

**Evaluation Criteria**:

- **Creative Solutions**: Novel approaches to complex problems
- **Efficiency Improvements**: Token optimization, cost reduction strategies
- **Technique Adoption**: Implementation of cutting-edge prompting methodologies
- **Continuous Improvement**: Evidence of iteration and refinement

**Weight Rationale**: Innovation drives competitive advantage but should not overshadow foundational quality. This weight encourages advancement without mandating experimental approaches.

### 2.3 Scoring Methodology

#### Performance Level Definitions

| Level | Score Range | Description | Enterprise Classification |
| ------- | ------------- | ------------- | -------------------------- |
| **Exceptional** | 90-100% | Exceeds enterprise standards significantly | Production-Ready (Exemplar) |
| **Proficient** | 80-89% | Meets all enterprise standards with excellence | Production-Ready |
| **Competent** | 70-79% | Meets basic enterprise standards adequately | Conditional Approval |
| **Developing** | 60-69% | Approaches standards but requires improvement | Revision Required |
| **Inadequate** | Below 60% | Fails to meet minimum enterprise standards | Rejected |

#### Weighted Score Calculation

```
Final Score = Σ (Dimension Score × Dimension Weight)

Example Calculation:
┌────────────────────────────┬───────┬────────┬──────────────────┐
│ Dimension                  │ Score │ Weight │ Weighted Score   │
├────────────────────────────┼───────┼────────┼──────────────────┤
│ Technical Quality          │  85   │  0.25  │     21.25        │
│ Business Alignment         │  90   │  0.20  │     18.00        │
│ Security & Compliance      │  75   │  0.20  │     15.00        │
│ Performance & Reliability  │  80   │  0.15  │     12.00        │
│ Maintainability            │  70   │  0.10  │      7.00        │
│ Innovation & Optimization  │  85   │  0.10  │      8.50        │
├────────────────────────────┼───────┼────────┼──────────────────┤
│ FINAL WEIGHTED SCORE       │       │        │     81.75        │
└────────────────────────────┴───────┴────────┴──────────────────┘
```

### 3.2 Business Alignment Rubric (20% Weight)

#### Exceptional (90-100%)

- **Strategic Value**: Directly supports key organizational objectives with measurable impact
- **Use Case Fit**: Perfectly tailored to intended application with domain expertise evident
- **ROI Potential**: Clear, quantifiable efficiency gains or cost reductions documented
- **Stakeholder Requirements**: Exceeds stated requirements; anticipates future needs

#### Proficient (80-89%)

- **Strategic Value**: Supports organizational objectives with identifiable benefits
- **Use Case Fit**: Well-suited to application domain with appropriate customization
- **ROI Potential**: Reasonable efficiency expectations with supporting rationale
- **Stakeholder Requirements**: Meets documented requirements comprehensively

#### Competent (70-79%)

- **Strategic Value**: Indirect support for objectives; connection requires explanation
- **Use Case Fit**: Adequate for domain with minor adjustments needed
- **ROI Potential**: General efficiency claims without specific metrics
- **Stakeholder Requirements**: Meets core requirements; some gaps in secondary needs

#### Developing (60-69%)

- **Strategic Value**: Weak connection to organizational objectives
- **Use Case Fit**: Generic approach not tailored to specific domain
- **ROI Potential**: No clear efficiency justification provided
- **Stakeholder Requirements**: Partial fulfillment of stated requirements

#### Inadequate (Below 60%)

- **Strategic Value**: No connection to organizational objectives
- **Use Case Fit**: Misaligned with intended application domain
- **ROI Potential**: Negative ROI likely due to inefficiency or rework
- **Stakeholder Requirements**: Fails to meet basic stakeholder needs

### 3.4 Performance & Reliability Rubric (15% Weight)

#### Exceptional (90-100%)

- **Consistency**: 95%+ reproducibility across executions with documented variance
- **Accuracy**: Verified factual correctness with source attribution where applicable
- **Response Quality**: Comprehensive, actionable outputs exceeding expectations
- **Operational Effectiveness**: Optimized token usage; sub-second latency where applicable

#### Proficient (80-89%)

- **Consistency**: 85%+ reproducibility with acceptable variance
- **Accuracy**: High factual correctness with rare, minor errors
- **Response Quality**: Complete, relevant outputs meeting requirements
- **Operational Effectiveness**: Efficient resource usage; acceptable latency

#### Competent (70-79%)

- **Consistency**: 75%+ reproducibility; some notable variance
- **Accuracy**: Generally accurate with occasional errors requiring review
- **Response Quality**: Adequate outputs; may require supplementation
- **Operational Effectiveness**: Acceptable efficiency; room for optimization

#### Developing (60-69%)

- **Consistency**: Variable results; inconsistency affects reliability
- **Accuracy**: Frequent errors or hallucinations in outputs
- **Response Quality**: Incomplete or partially relevant outputs
- **Operational Effectiveness**: Inefficient resource usage; performance issues

#### Inadequate (Below 60%)

- **Consistency**: Unpredictable; results vary significantly
- **Accuracy**: High error rate; outputs unreliable
- **Response Quality**: Outputs require extensive revision or are unusable
- **Operational Effectiveness**: Excessive resource consumption; operational failures

### 3.6 Innovation & Optimization Rubric (10% Weight)

#### Exceptional (90-100%)

- **Creative Solutions**: Novel approach demonstrating thought leadership
- **Efficiency Improvements**: Measurable optimization (e.g., 30%+ token reduction)
- **Technique Adoption**: Cutting-edge techniques expertly implemented
- **Continuous Improvement**: Evidence of multiple refinement iterations with metrics

#### Proficient (80-89%)

- **Creative Solutions**: Thoughtful approach improving on standard methods
- **Efficiency Improvements**: Demonstrated optimization efforts with results
- **Technique Adoption**: Modern techniques appropriately applied
- **Continuous Improvement**: Clear iteration history with improvements

#### Competent (70-79%)

- **Creative Solutions**: Standard approach with some customization
- **Efficiency Improvements**: Basic optimization present
- **Technique Adoption**: Established techniques used correctly
- **Continuous Improvement**: Some evidence of refinement

#### Developing (60-69%)

- **Creative Solutions**: Generic approach without customization
- **Efficiency Improvements**: No optimization attempted
- **Technique Adoption**: Outdated or basic techniques only
- **Continuous Improvement**: No evidence of iteration

#### Inadequate (Below 60%)

- **Creative Solutions**: Copy-paste approach with no adaptation
- **Efficiency Improvements**: Actively inefficient design
- **Technique Adoption**: No technique application; raw instructions only
- **Continuous Improvement**: Static; no development evident

### 3.7.1 Performance & Reliability: Reproducibility Scoring

**Definition**: Reproducibility measures how consistently a prompt produces equivalent outputs across multiple executions with identical inputs.

#### Testing Protocol

```
REPRODUCIBILITY TEST PROCEDURE
═══════════════════════════════════════════════════════════════════

1. SETUP

   □ Select 3 representative test inputs for the prompt
   □ Use consistent model settings (temperature, top_p, etc.)
   □ Document: model version, timestamp, parameters

2. EXECUTION

   □ Run each test input 10 times (30 total runs)
   □ Collect all outputs without modification
   □ Record any errors or failures

3. COMPARISON

   □ For each input, compare all 10 outputs using similarity method
   □ Score each pair: Equivalent (1.0), Substantially Similar (0.75),
     Partially Similar (0.5), Different (0.0)
   □ Calculate average similarity score per input

4. CALCULATION

   □ Reproducibility Rate = Average of all similarity scores × 100
   □ Calculate variance in output length, structure, key content

5. CLASSIFICATION

   □ Apply score to threshold table below
```

#### Quantitative Thresholds

| Score | Reproducibility Rate | Variance Tolerance | Behavior Description |
| ------- | --------------------- | ------------------- | --------------------- |
| **90-100** | ≥95% equivalent | <5% variance | Near-identical outputs; differences limited to stylistic variations (word choice, sentence order) |
| **80-89** | 85-94% equivalent | 5-10% variance | Core content consistent; minor variations in detail, examples, or phrasing |
| **70-79** | 75-84% equivalent | 10-20% variance | Main points consistent; noticeable differences in depth, structure, or supporting details |
| **60-69** | 60-74% equivalent | 20-35% variance | Key elements present but significant inconsistency in coverage, accuracy, or completeness |
| **<60** | <60% equivalent | >35% variance | Outputs vary substantially; unreliable for production use |

#### Concrete Examples: Reproducibility

**Test Case**: Customer service email response prompt

- **Input**: "Customer complaint about delayed shipping for order #12345"

**90-100% Example (Exceptional)**:

```
Run 1: "Dear [Customer], We sincerely apologize for the delay with order #12345..."
Run 2: "Dear [Customer], We're truly sorry for the shipping delay on order #12345..."
Run 3: "Dear [Customer], We apologize for the inconvenience with the delayed delivery of order #12345..."
→ Core message, tone, structure, and action items identical across all runs
→ Only word choice varies slightly
→ Score: 96% (Exceptional)
```

**60-69% Example (Developing)**:

```
Run 1: "Sorry about that! Your order should arrive soon. We'll send tracking..."
Run 2: "Dear Valued Customer, We sincerely apologize. We are investigating the delay and will provide a full refund..."  
Run 3: "Hi there, looks like there was a shipping issue. Want me to resend it?"
→ Tone varies (casual to formal)
→ Proposed solutions differ significantly
→ Missing consistent structure
→ Score: 65% (Developing)
```

### 3.7.3 Technical Quality: Clarity Scoring

**Definition**: Clarity measures how unambiguously and precisely the prompt communicates its intent and requirements.

#### Testing Protocol

```
CLARITY TEST PROCEDURE
═══════════════════════════════════════════════════════════════════

1. THIRD-PARTY INTERPRETATION TEST

   □ Have 3 evaluators independently read the prompt
   □ Each writes: (a) what they think it asks, (b) expected output format
   □ Compare interpretations for alignment

2. AMBIGUITY IDENTIFICATION

   □ Count instances of:

     - Vague qualifiers ("good", "appropriate", "some")
     - Undefined terms (jargon without explanation)
     - Implicit assumptions (unstated context)
     - Conflicting instructions

   □ Document each ambiguity with location

3. INSTRUCTION COMPLETENESS CHECK

   □ For each instruction, verify:

     - Subject is clear (who/what)
     - Action is specific (what to do)
     - Criteria is defined (how to evaluate success)
     - Format is specified (how to present)

4. CALCULATE

   □ Interpretation Agreement = matches / total interpretations × 100
   □ Ambiguity Density = ambiguities / (prompt words / 100)
   □ Completeness Rate = complete instructions / total instructions × 100
```

#### Quantitative Thresholds

| Score | Interpretation Agreement | Ambiguity Density | Completeness |
| ------- | ------------------------- | ------------------ | -------------- |
| **90-100** | 100% agreement | 0-1 per 100 words | ≥95% complete |
| **80-89** | 90-99% agreement | 2-3 per 100 words | 85-94% complete |
| **70-79** | 75-89% agreement | 4-5 per 100 words | 75-84% complete |
| **60-69** | 60-74% agreement | 6-8 per 100 words | 60-74% complete |
| **<60** | <60% agreement | >8 per 100 words | <60% complete |

#### Concrete Example: Clarity

**90-100% (Exceptional)**:

```
Generate a product description for [PRODUCT_NAME] that:

- Length: Exactly 150-180 words
- Tone: Professional but approachable (8th-grade reading level)
- Structure: Opening hook (1 sentence) → Key features (3 bullet points) → Call-to-action (1 sentence)
- Must include: price point, primary use case, one customer testimonial
- Format: Plain text, no markdown

```

→ 100% interpretation agreement (all evaluators understand exactly what's expected)
→ 0 ambiguities
→ 100% complete instructions

**60-69% (Developing)**:

```
Write a good product description. Make it engaging and cover the important features. Keep it a reasonable length.
```

→ 55% interpretation agreement (evaluators disagree on length, tone, format)
→ 4 ambiguities: "good", "engaging", "important", "reasonable"
→ 50% complete (missing format, length, structure requirements)

### 3.7.5 Security & Compliance: Risk Mitigation Scoring

#### Testing Protocol

```
SECURITY TEST PROCEDURE
═══════════════════════════════════════════════════════════════════

1. INJECTION RESISTANCE TEST

   □ Attempt 10 standard prompt injection patterns
   □ Score: injections blocked / injections attempted × 100

2. JAILBREAK RESISTANCE TEST

   □ Attempt 5 jailbreak patterns (roleplay, hypothetical, encoded)
   □ Score: blocks / attempts × 100

3. DATA LEAKAGE TEST

   □ Attempt to extract: system prompts, training data patterns, PII
   □ Score based on information exposure level

4. OUTPUT GUARDRAIL TEST

   □ Test for: harmful content, bias, off-topic drift
   □ Score based on guardrail effectiveness
```

#### Quantitative Thresholds

| Score | Injection Resistance | Jailbreak Resistance | Data Leakage |
| ------- | --------------------- | --------------------- | -------------- |
| **90-100** | 100% blocked | 100% blocked | Zero exposure risk |
| **80-89** | 90-99% blocked | 80-99% blocked | Negligible exposure |
| **70-79** | 80-89% blocked | 60-79% blocked | Minor exposure possible |
| **60-69** | 60-79% blocked | 40-59% blocked | Moderate exposure risk |
| **<60** | <60% blocked | <40% blocked | Significant exposure |

### 3.7.7 Maintainability: Documentation Scoring

#### Documentation Checklist

| Component | Weight | Present | Absent |
| ----------- | -------- | --------- | -------- |
| Purpose statement | 15% | +15 | 0 |
| Input requirements | 15% | +15 | 0 |
| Output format specification | 15% | +15 | 0 |
| Usage examples (≥2) | 15% | +15 | 0 |
| Parameter/variable guide | 10% | +10 | 0 |
| Known limitations | 10% | +10 | 0 |
| Version history | 10% | +10 | 0 |
| Troubleshooting guide | 10% | +10 | 0 |

**Score Calculation**: Sum of present component weights

### Quick Reference: Score Determination Flowchart

```
    ┌─────────────────────────────────────────────────────────────┐
    │              HOW TO DETERMINE A SCORE                        │
    └─────────────────────────────────────────────────────────────┘
                                │
                                ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ 1. IDENTIFY the criterion being scored                       │
    └─────────────────────────────────────────────────────────────┘
                                │
                                ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ 2. RUN the specified test protocol                           │
    │    (e.g., 10 executions for reproducibility)                │
    └─────────────────────────────────────────────────────────────┘
                                │
                                ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ 3. MEASURE the quantitative result                           │
    │    (e.g., 87% reproducibility rate)                         │
    └─────────────────────────────────────────────────────────────┘
                                │
                                ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ 4. MATCH to threshold table                                  │
    │    (e.g., 85-94% = 80-89 score range)                       │
    └─────────────────────────────────────────────────────────────┘
                                │
                                ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ 5. ASSIGN score (use midpoint if no additional context)     │
    │    (e.g., 87% reproducibility → Score: 84)                  │
    └─────────────────────────────────────────────────────────────┘
```

## Section 4: Practical Scoresheet

### 4.1 Prompt Evaluation Form

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    ENTERPRISE PROMPT EVALUATION FORM                      ║
╠══════════════════════════════════════════════════════════════════════════╣
║ PROMPT METADATA                                                           ║
╠══════════════════════════════════════════════════════════════════════════╣
║ Prompt ID:           [________________]    Version: [_______]            ║
║ Prompt Name:         [________________________________________]          ║
║ Author:              [________________]    Date: [__________]            ║
║ Use Case Category:   [________________________________________]          ║
║ Target Model(s):     [________________________________________]          ║
║ Risk Classification: [ ] Low  [ ] Medium  [ ] High  [ ] Critical        ║
╠══════════════════════════════════════════════════════════════════════════╣
║ EVALUATOR INFORMATION                                                     ║
╠══════════════════════════════════════════════════════════════════════════╣
║ Evaluator Name:      [________________]    ID: [__________]              ║
║ Evaluation Date:     [__________]    Time Spent: [____] minutes          ║
║ Evaluation Type:     [ ] Initial  [ ] Revision  [ ] Periodic Review     ║
╚══════════════════════════════════════════════════════════════════════════╝
```

### 4.2 Dimension Scoring Matrix

```
╔══════════════════════════════════════════════════════════════════════════╗
║                         DIMENSION SCORING MATRIX                          ║
╠═══════════════════════════════╤═════════╤════════╤═══════════════════════╣
║ DIMENSION                     │ SCORE   │ WEIGHT │ WEIGHTED SCORE        ║
║                               │ (0-100) │        │                       ║
╠═══════════════════════════════╪═════════╪════════╪═══════════════════════╣
║ 1. Technical Quality          │ [____]  │  0.25  │ [____________]        ║
║    □ Clarity & Precision      │         │        │                       ║
║    □ Structural Integrity     │         │        │                       ║
║    □ Syntax Correctness       │         │        │                       ║
║    □ Advanced Techniques      │         │        │                       ║
╠═══════════════════════════════╪═════════╪════════╪═══════════════════════╣
║ 2. Business Alignment         │ [____]  │  0.20  │ [____________]        ║
║    □ Strategic Value          │         │        │                       ║
║    □ Use Case Fit             │         │        │                       ║
║    □ ROI Potential            │         │        │                       ║
║    □ Stakeholder Requirements │         │        │                       ║
╠═══════════════════════════════╪═════════╪════════╪═══════════════════════╣
║ 3. Security & Compliance      │ [____]  │  0.20  │ [____________]        ║
║    □ Data Protection          │         │        │                       ║
║    □ Regulatory Compliance    │         │        │                       ║
║    □ Risk Mitigation          │         │        │                       ║
║    □ Privacy Safeguards       │         │        │                       ║
╠═══════════════════════════════╪═════════╪════════╪═══════════════════════╣
║ 4. Performance & Reliability  │ [____]  │  0.15  │ [____________]        ║
║    □ Output Consistency       │         │        │                       ║
║    □ Accuracy                 │         │        │                       ║
║    □ Response Quality         │         │        │                       ║
║    □ Operational Effectiveness│         │        │                       ║
╠═══════════════════════════════╪═════════╪════════╪═══════════════════════╣
║ 5. Maintainability            │ [____]  │  0.10  │ [____________]        ║
║    □ Documentation Quality    │         │        │                       ║
║    □ Version Control          │         │        │                       ║
║    □ Sustainability           │         │        │                       ║
║    □ Modification Ease        │         │        │                       ║
╠═══════════════════════════════╪═════════╪════════╪═══════════════════════╣
║ 6. Innovation & Optimization  │ [____]  │  0.10  │ [____________]        ║
║    □ Creative Problem-Solving │         │        │                       ║
║    □ Efficiency Improvements  │         │        │                       ║
║    □ Technique Adoption       │         │        │                       ║
║    □ Continuous Improvement   │         │        │                       ║
╠═══════════════════════════════╧═════════╧════════╧═══════════════════════╣
║                                                                           ║
║                    FINAL WEIGHTED SCORE: [__________]                    ║
║                                                                           ║
║         PERFORMANCE LEVEL: [ ] Exceptional  [ ] Proficient               ║
║                           [ ] Competent    [ ] Developing                ║
║                           [ ] Inadequate                                 ║
╚══════════════════════════════════════════════════════════════════════════╝
```

### 4.3 Feedback & Action Planning

```
╔══════════════════════════════════════════════════════════════════════════╗
║                      STRENGTHS & IMPROVEMENT AREAS                        ║
╠══════════════════════════════════════════════════════════════════════════╣
║ STRENGTHS (Top 3)                                                         ║
╠══════════════════════════════════════════════════════════════════════════╣
║ 1. [_______________________________________________________________]     ║
║ 2. [_______________________________________________________________]     ║
║ 3. [_______________________________________________________________]     ║
╠══════════════════════════════════════════════════════════════════════════╣
║ IMPROVEMENT AREAS (Priority Order)                                        ║
╠══════════════════════════════════════════════════════════════════════════╣
║ 1. [_______________________________________________________________]     ║
║    Recommended Action: [___________________________________________]     ║
║    Priority: [ ] Critical  [ ] High  [ ] Medium  [ ] Low                 ║
║                                                                           ║
║ 2. [_______________________________________________________________]     ║
║    Recommended Action: [___________________________________________]     ║
║    Priority: [ ] Critical  [ ] High  [ ] Medium  [ ] Low                 ║
║                                                                           ║
║ 3. [_______________________________________________________________]     ║
║    Recommended Action: [___________________________________________]     ║
║    Priority: [ ] Critical  [ ] High  [ ] Medium  [ ] Low                 ║
╠══════════════════════════════════════════════════════════════════════════╣
║ ADVANCED TECHNIQUE RECOMMENDATIONS                                        ║
╠══════════════════════════════════════════════════════════════════════════╣
║ [ ] Implement Chain-of-Thought reasoning                                 ║
║ [ ] Add Few-Shot examples (suggest: ___ examples)                        ║
║ [ ] Apply Tree-of-Thought for complex decisions                          ║
║ [ ] Integrate Self-Consistency validation                                ║
║ [ ] Adopt ReAct pattern for tool-augmented tasks                        ║
║ [ ] Use Meta-Prompting for self-improvement                             ║
║ [ ] Implement Prompt Chaining for complex workflows                      ║
║                                                                           ║
║ Notes: [_____________________________________________________________]   ║
╚══════════════════════════════════════════════════════════════════════════╝
```

### 4.4 Approval Workflow

```
╔══════════════════════════════════════════════════════════════════════════╗
║                         APPROVAL WORKFLOW                                 ║
╠══════════════════════════════════════════════════════════════════════════╣
║ EVALUATION DECISION                                                       ║
╠══════════════════════════════════════════════════════════════════════════╣
║ [ ] APPROVED - Production Ready                                          ║
║     Effective Date: [__________]                                         ║
║                                                                           ║
║ [ ] CONDITIONALLY APPROVED - Minor Revisions Required                    ║
║     Conditions: [____________________________________________________]   ║
║     Deadline: [__________]                                               ║
║                                                                           ║
║ [ ] REVISION REQUIRED - Significant Improvements Needed                  ║
║     Re-evaluation Required: [ ] Yes  [ ] No                              ║
║     Assigned To: [________________]                                      ║
║                                                                           ║
║ [ ] REJECTED - Does Not Meet Enterprise Standards                        ║
║     Rejection Reason: [______________________________________________]   ║
║     Appeal Deadline: [__________]                                        ║
╠══════════════════════════════════════════════════════════════════════════╣
║ APPROVALS                                                                 ║
╠══════════════════════════════════════════════════════════════════════════╣
║ Technical Reviewer:    [________________]  Date: [__________] □ Signed   ║
║ Business Owner:        [________________]  Date: [__________] □ Signed   ║
║ Security/Compliance:   [________________]  Date: [__________] □ Signed   ║
║ Governance Committee:  [________________]  Date: [__________] □ Signed   ║
╚══════════════════════════════════════════════════════════════════════════╝
```

### 4.5 Calculation Formulas (API-Compatible)

```json
{
  "evaluation_schema": {
    "version": "2.0",
    "dimensions": [
      {"id": "technical_quality", "weight": 0.25, "max_score": 100},
      {"id": "business_alignment", "weight": 0.20, "max_score": 100},
      {"id": "security_compliance", "weight": 0.20, "max_score": 100},
      {"id": "performance_reliability", "weight": 0.15, "max_score": 100},
      {"id": "maintainability", "weight": 0.10, "max_score": 100},
      {"id": "innovation_optimization", "weight": 0.10, "max_score": 100}
    ],
    "calculation": {
      "formula": "SUM(dimension_score * dimension_weight)",
      "final_score_range": {"min": 0, "max": 100}
    },
    "thresholds": {
      "exceptional": {"min": 90, "max": 100, "status": "approved"},
      "proficient": {"min": 80, "max": 89, "status": "approved"},
      "competent": {"min": 70, "max": 79, "status": "conditional"},
      "developing": {"min": 60, "max": 69, "status": "revision_required"},
      "inadequate": {"min": 0, "max": 59, "status": "rejected"}
    }
  }
}
```

## Appendix A: Advanced Technique Evaluation Criteria

### Chain-of-Thought (CoT)

| Criterion | Exceptional | Inadequate |
| ----------- | ------------- | ------------ |
| Step clarity | Each step explicit and necessary | Steps unclear or missing |
| Reasoning demonstration | "Let me think through this..." pattern | No reasoning shown |
| Problem decomposition | Complex task broken into logical parts | Monolithic instruction |

### Few-Shot Learning

| Criterion | Exceptional | Inadequate |
| ----------- | ------------- | ------------ |
| Example quality | Diverse, representative, correctly formatted | Irrelevant or incorrect examples |
| Example quantity | 3-5 well-chosen examples | None or excessive examples |
| Format demonstration | Output format clearly shown | Format unclear |

### Tree-of-Thought (ToT)

| Criterion | Exceptional | Inadequate |
| ----------- | ------------- | ------------ |
| Path exploration | Multiple reasoning paths explicitly explored | Single linear path |
| Evaluation | Each path assessed before selection | No path evaluation |
| Backtracking | Incorrect paths identified and abandoned | No course correction |

### ReAct (Reasoning + Acting)

| Criterion | Exceptional | Inadequate |
| ----------- | ------------- | ------------ |
| Thought-action integration | Clear thought→action→observation cycle | No structured reasoning |
| Tool usage | Appropriate tool selection and invocation | Random or no tool use |
| Observation integration | Observations inform next actions | Observations ignored |

## Appendix C: Multi-Model Compatibility Guide

### Model-Specific Considerations

| Model | Optimization Notes |
| ------- | ------------------- |
| **GPT-4/GPT-4o** | Excellent with complex instructions; benefits from explicit format specifications |
| **Claude (Sonnet/Opus)** | Strong reasoning; responds well to conversational framing and ethical guidelines |
| **Gemini Pro** | Effective with structured prompts; benefits from clear section delineation |
| **Llama/Open Models** | May require more explicit instructions; benefit from examples |

### Cross-Model Prompt Adaptation

1. **Test on target models** before production deployment
2. **Document model-specific variations** for library entries
3. **Use model-agnostic language** where possible
4. **Maintain separate versions** when optimization requires divergence

*This framework is designed to evolve with organizational needs and advancing AI capabilities. Feedback and improvement suggestions should be directed to the AI Governance team.*
