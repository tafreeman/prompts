---
title: "Privacy Impact Assessment (DPIA) Generator"
shortTitle: "DPIA Generator"
intro: "A structured ReAct+Reflection prompt for conducting Data Protection Impact Assessments following ICO UK guidance and GDPR Article 35 requirements."
type: "how_to"
difficulty: "advanced"
audience:
  - "solution-architect"
  - "security-engineer"
platforms:
  - "claude"
  - "chatgpt"
  - "github-copilot"
topics:
  - "governance"
  - "compliance"
  - "privacy"
  - "dpia"
author: "Prompts Library Team"
version: "1.0"
date: "2025-12-05"
governance_tags:
  - "requires-human-review"
  - "compliance-critical"
  - "audit-required"
dataClassification: "internal"
reviewStatus: "draft"
regulatory_scope:
  - "GDPR"
  - "UK-GDPR"
  - "ISO-27701"
---
# Privacy Impact Assessment (DPIA) Generator

---

## Description

A comprehensive prompt for conducting Data Protection Impact Assessments (DPIAs) as required by GDPR Article 35. Uses a 7-step methodology aligned with ICO UK guidance to systematically assess privacy risks, evaluate necessity and proportionality, and identify mitigating measures. Essential for processing involving new technologies, profiling, large-scale processing, or sensitive data.

---

## Research Foundation

**Regulatory Basis:**
- GDPR Article 35: Data Protection Impact Assessment
- ICO UK DPIA Guidance (2023)
- European Data Protection Board Guidelines on DPIAs

**Methodology:**
- 7-step DPIA process from ICO UK
- ReAct reasoning pattern (Yao et al., ICLR 2023) for systematic assessment
- Self-Refine reflection (Madaan et al., NeurIPS 2023) for quality assurance

**When DPIA is Mandatory:**
- Systematic and extensive profiling with significant effects
- Large-scale processing of special category data
- Systematic monitoring of publicly accessible areas
- Use of innovative technologies (including AI/ML)
- Processing that could prevent individuals exercising rights

---

## Use Cases

- New product/feature launches involving personal data
- AI/ML system deployments
- Biometric data processing systems
- Employee monitoring implementations
- Customer profiling and scoring systems
- Cross-border data sharing initiatives
- Third-party data integration projects

---

## Prompt

```text
You are an expert Data Protection Officer conducting a Data Protection Impact Assessment (DPIA) using the ICO UK 7-step methodology with ReAct reasoning and self-critique reflection.

## DPIA Context

**Project/Processing Name:** [PROJECT_NAME]
**Project Description:** [PROJECT_DESCRIPTION]
**Data Controller:** [CONTROLLER_NAME]
**DPO Contact:** [DPO_CONTACT]
**Assessment Date:** [DATE]
**Assessment Author:** [AUTHOR]

---

## Step 1: Screening - Do We Need a DPIA?

**Think:** Does this processing require a mandatory DPIA under GDPR Article 35(3)?

**Act:** Check against ICO screening criteria:

### Automatic DPIA Triggers
- [ ] Systematic and extensive profiling with significant effects
- [ ] Large-scale processing of special category data (Art. 9) or criminal data (Art. 10)
- [ ] Systematic monitoring of publicly accessible areas

### High-Risk Indicators (2+ = DPIA likely required)
- [ ] Evaluation/scoring (profiling, predicting)
- [ ] Automated decision-making with legal/significant effects
- [ ] Systematic monitoring
- [ ] Sensitive data or data of highly personal nature
- [ ] Large-scale processing
- [ ] Matching/combining datasets
- [ ] Data concerning vulnerable individuals
- [ ] Innovative use of technology (AI, biometrics, IoT)
- [ ] Processing preventing individuals from exercising rights
- [ ] Data transfers outside EEA

**Observe:** Count indicators triggered: [X/10]

**Reflect:** Based on the screening, is a DPIA:
- [ ] **Mandatory** (automatic trigger or 2+ high-risk indicators)
- [ ] **Recommended** (1 indicator but novel processing)
- [ ] **Not required** (but document reasoning)

**Screening Decision:** [DPIA Required / Not Required / Voluntary]
**Rationale:** [Document why]

---

## Step 2: Describe the Processing

**Think:** What exactly is being done with personal data, by whom, and why?

**Act:** Document the processing systematically:

### 2.1 Nature of Processing
- What will you do with the data?
- How is data collected?
- How is data stored?
- Who has access?
- What is the data flow?

### 2.2 Scope of Processing
- What data is being processed?
- How much data is involved?
- How often is processing performed?
- How long is data retained?
- What is the geographical area covered?

### 2.3 Context of Processing
- What is the relationship with data subjects?
- How much control do individuals have?
- Would individuals expect this processing?
- Do you use any new technologies?
- What is the current state of technology in this area?

### 2.4 Purposes of Processing
- What are you trying to achieve?
- What is the intended effect on individuals?
- What are the benefits (to you and to individuals)?

**Observe:** Create a data flow diagram showing:
```
[Data Source] → [Collection Point] → [Processing System] → [Storage] → [Output/Sharing]
```

**Reflect:** Is the description complete enough for risk assessment?

---

## Step 3: Consultation Requirements

**Think:** Who needs to be consulted, and when?

**Act:** Plan consultations:

### 3.1 Internal Consultation
| Stakeholder | Role | Input Needed | Status |
|-------------|------|--------------|--------|
| DPO | Privacy expert | Risk assessment, compliance | [ ] |
| IT Security | Technical controls | Security measures | [ ] |
| Legal | Legal basis, contracts | Lawfulness | [ ] |
| Business Owner | Requirements | Necessity | [ ] |

### 3.2 Data Subject Consultation
- Is consultation with data subjects feasible?
- If not, why not? (Document justification)
- What form will consultation take?
- How will feedback be incorporated?

### 3.3 External Consultation
- Are third-party processors involved?
- Is supervisory authority consultation required (Art. 36)?

**Observe:** Document consultation plan and outcomes.

**Reflect:** Have all relevant perspectives been captured?

---

## Step 4: Assess Necessity and Proportionality

**Think:** Is this processing actually necessary and proportionate to the purpose?

**Act:** Evaluate against GDPR principles:

### 4.1 Lawful Basis Assessment
| Purpose | Lawful Basis | Justification |
|---------|--------------|---------------|
| [Purpose 1] | [Basis] | [Why appropriate] |
| [Purpose 2] | [Basis] | [Why appropriate] |

### 4.2 Necessity Test
- Could the same result be achieved with less data?
- Could the same result be achieved differently?
- Is the processing proportionate to the aim?

### 4.3 Data Minimization Check
- Is all data collected actually needed?
- Can any data fields be removed?
- Can data be anonymized/pseudonymized?

### 4.4 Storage Limitation Check
- What is the retention period?
- Is this the minimum necessary?
- How is data deleted?

### 4.5 Data Subject Rights
| Right | How Fulfilled | Evidence |
|-------|---------------|----------|
| Information | [Mechanism] | [Link] |
| Access | [Mechanism] | [Process] |
| Rectification | [Mechanism] | [Process] |
| Erasure | [Mechanism] | [Process] |
| Portability | [Mechanism] | [Process] |
| Object | [Mechanism] | [Process] |

**Observe:** Document necessity and proportionality assessment.

**Reflect:** Is processing genuinely necessary, or is it "nice to have"?

---

## Step 5: Identify and Assess Risks

**Think:** What could go wrong for individuals, and how likely is it?

**Act:** Conduct risk assessment:

### Risk Assessment Matrix

| Risk | Likelihood | Severity | Risk Level | Affected Rights |
|------|------------|----------|------------|-----------------|
| Unauthorized access | H/M/L | H/M/L | [Score] | Confidentiality |
| Data breach | H/M/L | H/M/L | [Score] | Security |
| Inaccurate decisions | H/M/L | H/M/L | [Score] | Accuracy |
| Discrimination | H/M/L | H/M/L | [Score] | Fairness |
| Loss of control | H/M/L | H/M/L | [Score] | Autonomy |
| Re-identification | H/M/L | H/M/L | [Score] | Anonymity |
| Function creep | H/M/L | H/M/L | [Score] | Purpose limitation |

### Risk Scoring Guide
- **Likelihood:** High (probable), Medium (possible), Low (unlikely)
- **Severity:** High (significant harm), Medium (moderate harm), Low (minimal harm)
- **Risk Level:** H×H=Critical, H×M or M×H=High, M×M=Medium, Others=Low

**Observe:** Prioritize risks by level: Critical → High → Medium → Low

**Reflect:** Have I considered risks from the individual's perspective, not just organizational risks?

---

## Step 6: Identify Mitigating Measures

**Think:** How can identified risks be reduced or eliminated?

**Act:** Define controls for each risk:

### Mitigation Plan

| Risk | Measure | Effect on Risk | Residual Risk | Owner |
|------|---------|----------------|---------------|-------|
| [Risk 1] | [Control] | Eliminates/Reduces | H/M/L | [Role] |
| [Risk 2] | [Control] | Eliminates/Reduces | H/M/L | [Role] |

### Categories of Measures

**Technical Measures:**
- [ ] Encryption (at rest, in transit)
- [ ] Pseudonymization/anonymization
- [ ] Access controls
- [ ] Audit logging
- [ ] Automated deletion
- [ ] Data loss prevention

**Organizational Measures:**
- [ ] Staff training
- [ ] Policies and procedures
- [ ] Contractual safeguards
- [ ] Regular audits
- [ ] Incident response plan

**Privacy-Enhancing Measures:**
- [ ] Privacy by design architecture
- [ ] Consent management
- [ ] Transparency mechanisms
- [ ] User controls

**Observe:** Confirm each measure is:
- Practical to implement
- Effective at reducing risk
- Proportionate to the risk level

**Reflect:** Are residual risks acceptable? If not, reconsider the processing.

---

## Step 7: Sign Off and Record Outcomes

**Think:** Can this processing proceed? What needs to be documented?

**Act:** Complete the DPIA conclusion:

### 7.1 Risk Assessment Summary

| Risk Level | Count Before | Count After | Acceptable? |
|------------|--------------|-------------|-------------|
| Critical | [X] | [Y] | Y/N |
| High | [X] | [Y] | Y/N |
| Medium | [X] | [Y] | Y/N |
| Low | [X] | [Y] | Y/N |

### 7.2 DPIA Decision

- [ ] **Approved** - Processing can proceed as designed
- [ ] **Approved with Conditions** - Processing can proceed once measures implemented
- [ ] **Deferred** - Additional measures/consultation required before decision
- [ ] **Rejected** - Residual risks too high; processing cannot proceed
- [ ] **Refer to Supervisory Authority** - Art. 36 prior consultation required

### 7.3 Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| DPO | [Name] | [Date] | [Sig] |
| Project Owner | [Name] | [Date] | [Sig] |
| Senior Management | [Name] | [Date] | [Sig] |

**Observe:** Document the DPIA decision and maintain records per Art. 30.

**Reflect:** Is this DPIA defensible to a regulator?

---

## Phase 2: Self-Critique Reflection

### Quality Assurance Checklist

**Accuracy:**
- [ ] All facts are verified
- [ ] Risk assessments are evidence-based
- [ ] Mitigation effectiveness is realistic

**Completeness:**
- [ ] All 7 steps fully addressed
- [ ] All relevant risks identified
- [ ] All data flows documented

**Compliance:**
- [ ] Aligns with ICO DPIA guidance
- [ ] Meets GDPR Art. 35 requirements
- [ ] Consultation requirements met

**Confidence Level:** [High/Medium/Low]
**Key Uncertainties:** [List any areas needing clarification]
**Recommended Review Date:** [When to revisit this DPIA]
```

---

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `[PROJECT_NAME]` | Name of project or processing activity | "AI-Powered Customer Churn Prediction" |
| `[PROJECT_DESCRIPTION]` | Brief description of what the project does | "ML model to predict customer churn using behavioral data" |
| `[CONTROLLER_NAME]` | Organization responsible for processing | "Contoso Ltd" |
| `[DPO_CONTACT]` | DPO email/contact | "dpo@contoso.com" |
| `[DATE]` | Assessment date | "2025-12-05" |
| `[AUTHOR]` | Person conducting DPIA | "Jane Smith, Privacy Analyst" |

---

## Example Usage

**Input:**

```text
## DPIA Context

**Project/Processing Name:** Employee Wellness AI Assistant
**Project Description:** AI chatbot that monitors employee communications to detect burnout and suggest wellness resources
**Data Controller:** TechCorp Inc.
**DPO Contact:** privacy@techcorp.com
**Assessment Date:** 2025-12-05
**Assessment Author:** Privacy Team
```

**Output (Excerpt - Step 1):**

```markdown
## Step 1: Screening - Do We Need a DPIA?

### Automatic DPIA Triggers
- [x] Systematic and extensive profiling with significant effects
  → **TRIGGERED**: Continuous monitoring of employee communications constitutes systematic profiling

### High-Risk Indicators
- [x] Evaluation/scoring - Detecting "burnout" involves employee evaluation
- [x] Systematic monitoring - Ongoing communication analysis
- [x] Sensitive data - Health-related inferences (mental wellbeing)
- [x] Vulnerable individuals - Employees in subordinate position
- [x] Innovative technology - AI/ML-based analysis
- [ ] Large-scale processing - Internal employees only
- [ ] Automated decision-making - Human review before intervention
- [ ] Matching datasets - Single source
- [ ] Preventing rights exercise - N/A
- [ ] International transfers - To be confirmed

**Observe:** 5/10 high-risk indicators triggered + 1 automatic trigger

**Reflect:** This processing has MULTIPLE automatic triggers and high-risk indicators.

**Screening Decision:** DPIA MANDATORY
**Rationale:** 
1. Automatic trigger: Systematic profiling of employees with significant effects on their employment
2. High-risk indicators: 5 of 10 triggered including sensitive health inferences and vulnerable individuals
3. Novel AI technology processing employee communications requires careful assessment
```

---

## Tips

- **Start early** - Conduct DPIA during design phase, not after implementation
- **Be thorough on risks** - Think from the individual's perspective, not just organizational liability
- **Document everything** - DPIAs may be requested by regulators
- **Involve the DPO early** - Required by GDPR Art. 35(2)
- **Revisit regularly** - Review when processing changes or new risks emerge
- **Consider consultation** - When feasible, seek data subject input
- **Be honest about residual risk** - Don't minimize risks to get approval

---

## Related Prompts

- [GDPR Compliance Assessment](gdpr-compliance-assessment.md) - For broader compliance checks
- [AI Risk Assessment](ai-risk-assessment.md) - For AI-specific evaluations
- [Cross-Border Transfer Assessment](cross-border-transfer-assessment.md) - For international transfers
