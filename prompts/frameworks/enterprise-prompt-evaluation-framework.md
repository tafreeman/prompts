# Enterprise GenAI Prompt Evaluation Framework

**Version 2.0** | **Multi-Model Compatible** | **Last Updated: December 2025**

---

## Section 1: Executive Summary

### Framework Overview

This Enterprise GenAI Prompt Evaluation Framework provides a comprehensive, research-backed methodology for assessing generative AI prompts against enterprise library standards. Built on a weighted percentage scoring system (0-100 scale), the framework enables organizations to systematically evaluate, improve, and govern their prompt assets.

### Key Benefits

| Benefit | Description |
| --------- | ------------- |
| **Consistency** | Standardized evaluation criteria ensure 90%+ inter-evaluator agreement |
| **Quality Assurance** | Measurable improvement in prompt effectiveness over time |
| **Risk Mitigation** | Reduced security and compliance incidents from prompt usage |
| **Operational Efficiency** | Streamlined prompt approval and deployment processes |
| **Strategic Alignment** | Improved connection between prompts and business objectives |

### Target Audience

- **Prompt Engineers & Developers**: Primary evaluators and prompt creators
- **QA Teams**: Quality assurance and testing specialists
- **Governance Committees**: Risk and compliance oversight personnel
- **Business Stakeholders**: Domain experts validating use case alignment

### Implementation Approach

1. **Configure** evaluation parameters for your organizational context
2. **Train** evaluators on rubric application and scoring methodology
3. **Pilot** with representative prompt sample before full deployment
4. **Deploy** across enterprise prompt library with batch evaluation support
5. **Iterate** based on feedback and quality metrics analysis

---

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

---

## Section 3: Comprehensive Rubric

### 3.1 Technical Quality Rubric (25% Weight)

#### Exceptional (90-100%)

- **Clarity**: Instructions are crystal clear with zero ambiguity; terminology precisely defined
- **Structure**: Perfect logical flow with clear sections, headers, and formatting conventions
- **Syntax**: Flawless grammar and punctuation; consistent professional style throughout
- **Advanced Techniques**: Masterful integration of multiple techniques (CoT, Few-Shot, ToT, ReAct) with clear reasoning
- **Example**: Prompt includes explicit step-by-step reasoning, 3+ diverse examples, and built-in self-verification

#### Proficient (80-89%)

- **Clarity**: Clear instructions with minimal ambiguity; terms well-defined
- **Structure**: Strong logical organization; consistent formatting
- **Syntax**: Minor grammatical variations that don't impact comprehension
- **Advanced Techniques**: Effective use of at least two advanced techniques with appropriate application
- **Example**: Prompt uses Chain-of-Thought with relevant examples; structure supports intended use case

#### Competent (70-79%)

- **Clarity**: Generally clear with some areas requiring interpretation
- **Structure**: Adequate organization; some formatting inconsistencies
- **Syntax**: Occasional grammar issues; style variations present
- **Advanced Techniques**: Basic implementation of one advanced technique
- **Example**: Prompt includes step-by-step instructions but lacks examples or verification

#### Developing (60-69%)

- **Clarity**: Significant ambiguity in key instructions
- **Structure**: Weak organization affecting comprehension
- **Syntax**: Multiple grammar/style issues impacting readability
- **Advanced Techniques**: Attempted but incorrectly implemented techniques
- **Example**: Prompt attempts Chain-of-Thought but reasoning steps are unclear or illogical

#### Inadequate (Below 60%)

- **Clarity**: Instructions are confusing or contradictory
- **Structure**: No discernible organization; formatting absent
- **Syntax**: Pervasive errors affecting comprehension
- **Advanced Techniques**: No advanced techniques or complete misapplication
- **Example**: Prompt is a single run-on instruction with no structure or technique application

---

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

---

### 3.3 Security & Compliance Rubric (20% Weight)

#### Exceptional (90-100%)

- **Data Protection**: Comprehensive safeguards; no sensitive data exposure possible
- **Regulatory Compliance**: Full adherence to all applicable regulations with documentation
- **Risk Mitigation**: Multi-layer defenses against injection, jailbreaking, and misuse
- **Privacy Safeguards**: Privacy-by-design principles fully implemented

#### Proficient (80-89%)

- **Data Protection**: Strong safeguards with clear data handling instructions
- **Regulatory Compliance**: Meets all required regulations with evidence of consideration
- **Risk Mitigation**: Effective guardrails and output validation implemented
- **Privacy Safeguards**: Privacy considerations addressed in design

#### Competent (70-79%)

- **Data Protection**: Basic safeguards present; some edge cases unaddressed
- **Regulatory Compliance**: Compliant with major regulations; minor gaps may exist
- **Risk Mitigation**: Basic guardrails implemented; some vulnerabilities possible
- **Privacy Safeguards**: Privacy mentioned but not comprehensively addressed

#### Developing (60-69%)

- **Data Protection**: Minimal safeguards; potential exposure risks identified
- **Regulatory Compliance**: Partial compliance; remediation required
- **Risk Mitigation**: Limited guardrails; known vulnerabilities present
- **Privacy Safeguards**: Privacy not systematically considered

#### Inadequate (Below 60%)

- **Data Protection**: No safeguards; sensitive data exposure likely
- **Regulatory Compliance**: Non-compliant with critical regulations
- **Risk Mitigation**: No protections against known attack vectors
- **Privacy Safeguards**: Privacy violations possible or likely

---

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

---

### 3.5 Maintainability Rubric (10% Weight)

#### Exceptional (90-100%)

- **Documentation**: Comprehensive docs including purpose, usage, examples, troubleshooting
- **Version Control**: Full change history; clear versioning scheme; migration guides
- **Sustainability**: Model-agnostic design; future-proofed for evolving capabilities
- **Modification Ease**: Modular, parameterized structure; clear extension points

#### Proficient (80-89%)

- **Documentation**: Clear documentation covering purpose, usage, and examples
- **Version Control**: Maintained version history with change notes
- **Sustainability**: Considers model differences; reasonable longevity
- **Modification Ease**: Well-structured; modifications straightforward

#### Competent (70-79%)

- **Documentation**: Basic documentation; purpose and usage described
- **Version Control**: Version tracked; limited change documentation
- **Sustainability**: May require updates for different models
- **Modification Ease**: Structure allows modification with some effort

#### Developing (60-69%)

- **Documentation**: Minimal documentation; gaps in critical information
- **Version Control**: Ad-hoc versioning; poor change tracking
- **Sustainability**: Model-specific; limited longevity
- **Modification Ease**: Modifications difficult; structure unclear

#### Inadequate (Below 60%)

- **Documentation**: No documentation or severely incomplete
- **Version Control**: No versioning; changes untracked
- **Sustainability**: Unlikely to remain functional; obsolescence imminent
- **Modification Ease**: Modifications require complete rewrite

---

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

---

## Section 3.7: Operationalized Scoring Criteria

This section provides **quantitative thresholds** and **testing methodologies** to eliminate subjectivity in scoring. For each criterion, you'll find specific tests to run and exact measurements that determine each performance level.

### How Scoring Works

Each dimension score is calculated by:

1. **Testing** the prompt using the specified methodology
2. **Measuring** results against quantitative thresholds
3. **Calculating** the sub-criterion score based on thresholds
4. **Averaging** sub-criteria scores to get the dimension score

---

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

---

### 3.7.2 Performance & Reliability: Accuracy Scoring

**Definition**: Accuracy measures the factual correctness and alignment of outputs with expected/verifiable outcomes.

#### Testing Protocol

```
ACCURACY TEST PROCEDURE
═══════════════════════════════════════════════════════════════════

1. ESTABLISH GROUND TRUTH

   □ For factual prompts: identify verifiable claims expected in output
   □ For analytical prompts: define expected conclusions/recommendations
   □ For creative prompts: define quality criteria and constraints
   □ Document 10-20 checkpoints per test case

2. EXECUTE PROMPT

   □ Run prompt 5 times with identical inputs
   □ Collect outputs for evaluation

3. VERIFY EACH CHECKPOINT

   □ Correct (1.0): Claim is accurate and properly contextualized
   □ Partially Correct (0.5): Claim has minor errors or lacks context
   □ Incorrect (0.0): Claim is factually wrong or a hallucination
   □ Missing (0.0): Expected claim is absent

4. CALCULATE

   □ Accuracy Rate = (Total Points / Total Checkpoints) × 100
   □ Hallucination Rate = (False Claims / Total Claims) × 100

5. APPLY PENALTIES

   □ Critical Error Penalty: -10 points per hallucination that could cause harm
   □ Omission Penalty: -5 points for missing critical information
```

#### Quantitative Thresholds

| Score | Accuracy Rate | Hallucination Rate | Error Severity |
| ------- | -------------- | ------------------- | ---------------- |
| **90-100** | ≥95% | <1% | No critical errors; trivial omissions only |
| **80-89** | 85-94% | 1-3% | No critical errors; minor factual gaps acceptable |
| **70-79** | 75-84% | 3-7% | Some errors present but self-correctable with review |
| **60-69** | 60-74% | 7-15% | Errors require significant manual correction |
| **<60** | <60% | >15% | Unreliable; outputs require full verification |

---

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

---

### 3.7.4 Technical Quality: Advanced Technique Implementation

**Definition**: Measures the correct and effective implementation of advanced prompting techniques.

#### Technique Scoring Matrix

| Technique | Exceptional (90-100%) | Proficient (80-89%) | Competent (70-79%) | Developing (60-69%) |
| ----------- | ---------------------- | -------------------- | -------------------- | --------------------- |
| **Chain-of-Thought** | ≥5 explicit reasoning steps; self-verification; handles edge cases | 3-4 reasoning steps; clear logic flow | 2-3 steps; some implicit reasoning | Steps present but unclear or illogical |
| **Few-Shot** | 4+ diverse, edge-case-covering examples; format perfectly demonstrated | 3 relevant examples; format shown | 2 examples; basic format guidance | 1 example or examples don't match use case |
| **Tree-of-Thought** | ≥3 paths explored; evaluation criteria explicit; backtracking shown | 2 paths with evaluation | 2 paths without clear evaluation | Single path labeled as "exploration" |
| **ReAct** | Clear thought→action→observation loop; ≥3 iterations modeled | 2 complete iterations | 1 complete iteration | Pattern mentioned but not demonstrated |
| **Self-Consistency** | ≥3 reasoning paths with aggregation method specified | 2 paths with comparison | 1 alternative path | Mentions "double-check" without structure |

#### Counting Rules

- **No advanced techniques**: Maximum score of 65
- **One technique, partial implementation**: Maximum score of 75
- **One technique, full implementation**: Maximum score of 85
- **Two+ techniques, properly integrated**: Eligible for 90-100

---

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

---

### 3.7.6 Business Alignment: ROI Potential Scoring

#### Quantification Method

```
ROI CALCULATION
═══════════════════════════════════════════════════════════════════

1. TIME SAVINGS

   □ Measure: time to complete task manually vs. with prompt
   □ Calculate: (manual_time - prompt_time) / manual_time × 100

2. QUALITY IMPROVEMENT

   □ Measure: error rate manual vs. prompt-assisted
   □ Calculate quality delta

3. COST IMPACT

   □ Token cost per use × expected monthly volume
   □ Compare to labor cost for equivalent output

4. DOCUMENTATION

   □ Must include: baseline metrics, expected improvement, measurement method
```

#### Quantitative Thresholds

| Score | Time Savings | Quality Delta | Documentation |
| ------- | ------------- | --------------- | --------------- |
| **90-100** | ≥70% | ≥30% improvement | Full ROI analysis with metrics |
| **80-89** | 50-69% | 15-29% improvement | Clear justification with estimates |
| **70-79** | 30-49% | 5-14% improvement | General efficiency claims |
| **60-69** | 10-29% | Minimal improvement | No quantification |
| **<60** | <10% or negative | No improvement | Potential negative ROI |

---

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

---

### 3.7.8 Innovation: Efficiency Optimization Scoring

#### Measurement Method

```
EFFICIENCY TEST
═══════════════════════════════════════════════════════════════════

1. TOKEN ANALYSIS

   □ Count prompt tokens (input)
   □ Measure average response tokens (output)
   □ Compare to baseline/standard approach

2. LATENCY MEASUREMENT

   □ Measure time-to-first-token
   □ Measure total response time
   □ Calculate across 10 runs

3. OPTIMIZATION IDENTIFICATION

   □ Document specific optimizations applied
   □ Measure impact of each optimization
```

#### Quantitative Thresholds

| Score | Token Efficiency | Latency | Optimization Evidence |
| ------- | ----------------- | --------- | ---------------------- |
| **90-100** | ≥30% reduction vs. baseline | ≥20% faster | Multiple documented optimizations with metrics |
| **80-89** | 15-29% reduction | 10-19% faster | Clear optimizations with evidence |
| **70-79** | 5-14% reduction | 5-9% faster | Some optimization present |
| **60-69** | No reduction | No improvement | No optimization attempted |
| **<60** | Bloated (>baseline) | Slower than baseline | Anti-patterns present |

---

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

---

## Section 3.8: Research-Backed Industry Standards

This section documents how **real-world implementations** determine scoring thresholds, based on academic research and production systems from leading organizations.

### Industry Scoring Scale Comparison

| Framework | Organization | Scale | Threshold Methodology |
| ----------- | ------------- | ------- | ---------------------- |
| **G-Eval** | Microsoft/DeepEval | 1-5 → 0-1 normalized | LLM judges rate 1-5, normalize to 0-1; default threshold: 0.5 |
| **RubricEval** | Stanford | 1-4 | 4=Excellent, 3=Good, 2=Fair, 1=Poor; avg across criteria |
| **MT-Bench** | LMSYS/UC Berkeley | 1-10 | GPT-4 as judge; 80%+ agreement with human preferences |
| **Chatbot Arena** | LMSYS | Pairwise + Elo | User preference voting → Bradley-Terry Elo calculation |
| **RAGAS** | Open Source | 0-1 | Per-metric; faithfulness ≥0.85, precision ≥0.70 |
| **Promptfoo** | Open Source | 0-1 + assertions | Weighted assertions; default pass threshold: 0.5 |
| **LangSmith** | LangChain | Custom | LLM-as-judge with configurable criteria |
| **BERTScore** | Research | 0-1 | Cosine similarity; ~0.86 indicates high similarity |

### Production Thresholds in Use

Based on industry research and documentation, these are **actual thresholds used in production systems**:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PRODUCTION THRESHOLDS BY METRIC                       │
├─────────────────────────────────────────────────────────────────────────┤
│ FAITHFULNESS / FACTUALITY                                                │
│   ≥ 0.85 (85%)    Answers grounded in provided context (RAGAS)          │
│   ≥ 0.95 (95%)    Critical/regulated domains (healthcare, finance)      │
│                                                                          │
│ CONTEXT PRECISION / RELEVANCE                                            │
│   ≥ 0.70 (70%)    Retrieved context is relevant to query                │
│   ≥ 0.80 (80%)    High-precision applications                           │
│                                                                          │
│ SEMANTIC SIMILARITY (BERTScore)                                          │
│   ≥ 0.86         "Highly similar" semantic match                         │
│   ≥ 0.70         "Similar" - acceptable for paraphrase                   │
│   < 0.50         "Dissimilar" - significant meaning difference           │
│                                                                          │
│ REPRODUCIBILITY / CONSISTENCY                                            │
│   ≥ 95%          Enterprise-grade consistency requirement                │
│   ≥ 85%          Standard production threshold                           │
│   ≥ 75%          Minimum acceptable for deployment                       │
│                                                                          │
│ OVERALL QUALITY (G-Eval / LLM-as-Judge)                                  │
│   ≥ 0.80         Production-ready (normalized 0-1 scale)                 │
│   ≥ 0.50         Default pass/fail threshold (DeepEval)                  │
│                                                                          │
│ OPERATIONAL METRICS                                                       │
│   Pass Rate:     ≥ 95%    Overall test suite passing                     │
│   Latency:       < 2s     Response time SLA                              │
│   Accuracy:      ≥ 98%    Critical task accuracy                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Inter-Rater Reliability Standards

Academic research establishes these standards for evaluator agreement:

| Cohen's Kappa (κ) | Interpretation | Use Case |
| ------------------- | ---------------- | ---------- |
| **κ > 0.80** | Almost perfect agreement | Gold standard; production confidence |
| **κ = 0.60-0.80** | Substantial agreement | Acceptable for production deployment |
| **κ = 0.40-0.60** | Moderate agreement | Requires calibration; use with caution |
| **κ < 0.40** | Fair/Poor agreement | Not reliable; requires rubric revision |

**Research Findings:**

- **RubricEval (Stanford)**: Achieved κ = 0.37 between human and LLM criteria scores (moderate)
- **Optimized LLM-as-Judge**: After prompt/hyperparameter tuning, achieved κ > 0.6 (substantial)
- **MT-Bench**: 80%+ agreement between GPT-4 judge and human preferences
- **Implication**: LLM-based evaluation is viable but requires calibration against human judgment

### How to Determine Your Thresholds

Based on industry best practices, follow this methodology:

#### Step 1: Establish Ground Truth (Human Baseline)

```

1. Select 50-100 representative prompts
2. Have 3+ human evaluators score each using your rubric
3. Calculate inter-rater reliability (target: κ > 0.6)
4. Create "gold standard" dataset with consensus scores

```

#### Step 2: Calibrate Automated Scoring

```

1. Run automated evaluation (LLM-as-judge or heuristic) on gold standard
2. Compare automated scores to human consensus
3. Calculate correlation (target: Pearson r > 0.7 or Spearman ρ > 0.7)
4. Adjust thresholds until agreement improves

```

#### Step 3: Set Risk-Appropriate Thresholds

| Risk Level | Threshold Approach | Example |
| ------------ | ------------------- | --------- |
| **Critical** (healthcare, finance) | Conservative; high thresholds | Accuracy ≥98%, Faithfulness ≥95% |
| **High** (customer-facing) | Standard production | Accuracy ≥90%, Consistency ≥85% |
| **Medium** (internal tools) | Balanced | Accuracy ≥80%, Consistency ≥75% |
| **Low** (exploration/testing) | Permissive | Accuracy ≥70%, iterate frequently |

#### Step 4: Validate Empirically

```
THRESHOLD VALIDATION PROCEDURE
═══════════════════════════════════════════════════════════════════

1. SPLIT gold standard into train (70%) and test (30%) sets
2. SET initial thresholds based on train set performance
3. VALIDATE on held-out test set
4. MEASURE:
   - False positive rate (poor prompts passing)
   - False negative rate (good prompts failing)
5. ADJUST thresholds to minimize business-critical errors
6. MONITOR in production; refine quarterly

```

### Mapping Our 0-100 Scale to Industry Standards

Our framework uses a 0-100 percentage scale. Here's how it maps to common industry scales:

| Our Score | 0-1 Scale | 1-5 Scale | 1-4 Scale | Interpretation |
| ----------- | ----------- | ----------- | ----------- | ---------------- |
| **90-100** | 0.90-1.00 | 4.5-5.0 | 4 (Excellent) | Exceptional; exemplar |
| **80-89** | 0.80-0.89 | 4.0-4.4 | 3-4 (Good-Excellent) | Production-ready |
| **70-79** | 0.70-0.79 | 3.5-3.9 | 3 (Good) | Acceptable with conditions |
| **60-69** | 0.60-0.69 | 3.0-3.4 | 2-3 (Fair-Good) | Needs improvement |
| **<60** | <0.60 | <3.0 | 1-2 (Poor-Fair) | Below minimum standard |

### Automated Scoring Implementation

For programmatic evaluation, use this approach aligned with G-Eval:

```python
# Example: G-Eval style scoring implementation
def calculate_dimension_score(
    prompt: str,
    output: str,
    criteria: list[str],
    model: str = "gpt-4"
) -> float:
    """
    Uses LLM-as-judge with Chain-of-Thought to score.
    Returns normalized score 0-1 (multiply by 100 for percentage).
    """
    scores = []
    for criterion in criteria:
        # Step 1: Generate evaluation steps (CoT)
        eval_steps = generate_eval_steps(criterion)

        # Step 2: LLM judges on 1-5 scale
        raw_score = llm_judge(prompt, output, eval_steps, scale="1-5")

        # Step 3: Normalize to 0-1
        normalized = (raw_score - 1) / 4  # Maps 1-5 to 0-1
        scores.append(normalized)

    # Average across criteria
    return sum(scores) / len(scores)

# Thresholds aligned with industry standards
THRESHOLDS = {
    "exceptional": 0.90,  # ≥90% normalized
    "proficient": 0.80,   # ≥80%
    "competent": 0.70,    # ≥70%
    "developing": 0.60,   # ≥60%
    "inadequate": 0.00    # <60%
}
```

### Key Research Citations

This section is based on findings from:

1. **G-Eval Paper**: "G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment" - Chain-of-Thought scoring methodology
2. **RubricEval (Stanford)**: 1-4 scoring with instruction-specific rubrics; ρ = 0.98 correlation with Chatbot Arena
3. **MT-Bench (LMSYS)**: Multi-turn benchmark with GPT-4 judge; 80%+ human agreement
4. **RAGAS**: RAG evaluation suite with faithfulness, relevance, precision metrics
5. **DeepEval**: Open-source framework; 0-1 normalized scores with 0.5 default threshold
6. **Promptfoo**: Assertion-based testing with configurable thresholds
7. **LLM-RUBRIC (ACL Anthology)**: Calibration networks to align LLM scores with human judgment
8. **BERTScore**: Semantic similarity using contextual embeddings

---

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

---

## Section 5: Implementation Guide

### 5.1 Deployment Best Practices

#### Phase 1: Preparation (Weeks 1-2)

1. **Stakeholder Alignment**
   - Present framework to governance committee for approval
   - Identify pilot team and evaluation candidates
   - Establish success metrics and baseline measurements

2. **Tool Configuration**
   - Deploy scoresheet templates in document management system
   - Configure API integration for automated scoring (if applicable)
   - Set up version control for evaluated prompts

3. **Sample Selection**
   - Choose 20-30 representative prompts across use cases
   - Include prompts of varying quality for calibration
   - Document selection rationale

#### Phase 2: Pilot Evaluation (Weeks 3-4)

1. **Calibration Sessions**
   - Conduct group evaluation of 5 prompts
   - Discuss scoring rationale and resolve discrepancies
   - Refine criteria interpretation for organizational context

2. **Independent Evaluation**
   - Each evaluator scores remaining pilot prompts
   - Calculate inter-rater reliability (target: 90%+ agreement)
   - Identify and address systematic disagreements

3. **Feedback Integration**
   - Collect evaluator feedback on rubric usability
   - Adjust weightings if organizational priorities differ
   - Update documentation based on pilot learnings

#### Phase 3: Full Deployment (Weeks 5+)

1. **Rollout**
   - Communicate framework to all prompt creators
   - Integrate evaluation into prompt approval workflow
   - Establish evaluation cadence (new prompts + periodic reviews)

2. **Monitoring**
   - Track key metrics: evaluation time, score distributions, approval rates
   - Monitor for evaluator drift through periodic calibration
   - Report aggregate quality metrics to governance committee

### 5.2 Training Recommendations

#### Evaluator Training Program

| Module | Duration | Content |
| -------- | ---------- | --------- |
| **Framework Overview** | 1 hour | Dimension definitions, scoring methodology, business context |
| **Rubric Deep-Dive** | 2 hours | Detailed criteria review, example scoring, edge cases |
| **Hands-On Calibration** | 3 hours | Group evaluation exercises, discussion, alignment |
| **Tool Training** | 1 hour | Scoresheet usage, system integration, workflow procedures |
| **Certification** | 1 hour | Assessment evaluation, feedback, certification |

#### Prompt Creator Training

| Module | Duration | Content |
| -------- | ---------- | --------- |
| **Quality Standards** | 1 hour | Enterprise requirements, common failure modes |
| **Self-Assessment** | 1 hour | Pre-submission evaluation, improvement strategies |
| **Advanced Techniques** | 2 hours | CoT, Few-Shot, ToT, ReAct implementation |
| **Submission Process** | 30 min | Workflow, documentation requirements, timeline |

### 5.3 Quality Assurance Measures

#### Inter-Rater Reliability

- Minimum 2 evaluators per prompt for high-risk classifications
- Regular calibration exercises (monthly for active evaluators)
- Automatic flagging when evaluator scores differ by >15 points

#### Audit Procedures

- Quarterly review of evaluation consistency
- Random sampling of approved prompts for validation
- Annual framework review and update

#### Escalation Paths

- Evaluator disagreement → Senior evaluator arbitration
- Author dispute → Governance committee review
- Systematic issues → Framework revision process

### 5.4 Continuous Improvement Processes

#### Metrics Dashboard

Track and report monthly:

- Average prompt scores by dimension
- Score distribution changes over time
- Approval/rejection rates
- Evaluation cycle time
- Inter-rater agreement rates

#### Feedback Loops

- Post-deployment performance tracking for approved prompts
- Correlation analysis: evaluation scores vs. production outcomes
- Annual stakeholder survey on framework effectiveness

#### Framework Evolution

- Quarterly review of emerging prompting techniques for rubric updates
- Annual weight distribution review based on organizational priorities
- Continuous alignment with regulatory changes (GDPR, AI Act, etc.)

---

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

---

## Appendix B: Industry-Specific Adaptations

### Financial Services (SOX Focus)

- Add audit trail requirements
- Increase Maintainability weight to 15%
- Include regulatory disclosure criteria

### Legal (Privilege Focus)

- Include citation accuracy validation
- Require jurisdiction-specific compliance

---

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

---

## Document Control

| Version | Date | Author | Changes |
| --------- | ------ | -------- | --------- |
| 2.0 | December 2025 | Enterprise AI Governance Team | Initial framework release |

**Compatibility**: GPT-4, Claude (Sonnet/Opus), Gemini Pro, and compatible LLMs  
**Review Cycle**: Annual with quarterly technique updates  
**Owner**: AI Governance Committee

---

*This framework is designed to evolve with organizational needs and advancing AI capabilities. Feedback and improvement suggestions should be directed to the AI Governance team.*
