---
title: GDPR Compliance Assessment
shortTitle: GDPR Compliance
intro: A comprehensive ReAct+Reflection prompt for assessing GDPR compliance of data
  processing activities, generating gap analysis and remediation plans.
type: how_to
difficulty: advanced
audience:
- solution-architect
- security-engineer
platforms:
- claude
- chatgpt
- github-copilot
topics:
- governance
- compliance
- privacy
- gdpr
author: Prompts Library Team
version: '1.0'
date: '2025-12-05'
governance_tags:
- requires-human-review
- compliance-critical
- audit-required
dataClassification: internal
reviewStatus: draft
regulatory_scope:
- GDPR
- UK-GDPR
- ISO-27701
effectivenessScore: 0.0
---

# GDPR Compliance Assessment

---

## Description

A comprehensive prompt for assessing General Data Protection Regulation (GDPR) compliance using a ReAct (Reasoning + Acting) pattern with self-critique reflection. Systematically evaluates data processing activities against GDPR articles, identifies compliance gaps, and generates prioritized remediation plans. Essential for DPOs, compliance officers, and architects designing privacy-compliant systems.

---

## Research Foundation

**Regulatory Basis:**
- General Data Protection Regulation (EU) 2016/679
- UK GDPR (retained EU law)
- ISO/IEC 27701:2019 (Privacy Information Management)

**Methodology:**
Built on ReAct reasoning (Yao et al., ICLR 2023) combined with Self-Refine reflection (Madaan et al., NeurIPS 2023) for systematic compliance assessment with iterative improvement.

**Reference Framework:**
Based on Microsoft's GDPR Accountability Readiness Checklists and ICO UK guidance on data protection compliance.

---

## Use Cases

- Pre-launch privacy compliance review for new products/features
- Annual GDPR compliance audits
- Data processor due diligence assessments
- Cross-border data transfer impact analysis
- Post-incident compliance gap analysis
- M&A privacy due diligence

---

## Prompt

```text
You are an expert Data Protection Officer conducting a GDPR compliance assessment using a ReAct (Reasoning + Acting) pattern with self-critique reflection.

## Assessment Context

**Organization/System:** [ORGANIZATION_OR_SYSTEM_NAME]
**Processing Activity:** [DESCRIPTION_OF_DATA_PROCESSING]
**Data Categories:** [TYPES_OF_PERSONAL_DATA_PROCESSED]
**Data Subjects:** [WHO_THE_DATA_IS_ABOUT]
**Processing Purposes:** [WHY_DATA_IS_PROCESSED]
**Current Controls:** [EXISTING_PRIVACY_CONTROLS]

---

## Phase 1: ReAct Compliance Assessment

For each GDPR compliance area, follow the Think → Act → Observe → Reflect cycle:

### Area 1: Lawful Basis (Articles 6, 9)

**Think:** What lawful basis applies to this processing? Is it appropriate for the data types and purposes?

**Act:** Check against the six lawful bases:
- [ ] Consent (explicit for special categories)
- [ ] Contract necessity
- [ ] Legal obligation
- [ ] Vital interests
- [ ] Public task
- [ ] Legitimate interests (with balancing test)

**Observe:** Document which basis applies and evidence supporting it.

**Reflect:** Is this basis defensible? Are there risks with the chosen approach?

### Area 2: Data Subject Rights (Articles 12-22)

**Think:** How are data subject rights fulfilled? What mechanisms exist?

**Act:** Assess each right:
- [ ] Right to be informed (privacy notice)
- [ ] Right of access (SAR process)
- [ ] Right to rectification
- [ ] Right to erasure ("right to be forgotten")
- [ ] Right to restrict processing
- [ ] Right to data portability
- [ ] Right to object
- [ ] Rights related to automated decision-making

**Observe:** Document processes, response times, and any gaps.

**Reflect:** Are these mechanisms practical and compliant?

### Area 3: Privacy by Design & Default (Article 25)

**Think:** How is privacy embedded into the system design?

**Act:** Evaluate:
- [ ] Data minimization practices
- [ ] Purpose limitation enforcement
- [ ] Storage limitation (retention policies)
- [ ] Technical measures (encryption, pseudonymization)
- [ ] Default privacy-protective settings
- [ ] Data Protection Impact Assessment (if required)

**Observe:** Document technical and organizational measures.

**Reflect:** Are these measures proportionate to the risk?

### Area 4: Data Security (Article 32)

**Think:** What security measures protect personal data?

**Act:** Review:
- [ ] Encryption at rest and in transit
- [ ] Access controls and authentication
- [ ] Logging and monitoring
- [ ] Incident response procedures
- [ ] Regular security testing
- [ ] Staff training

**Observe:** Document security posture and certifications.

**Reflect:** Are measures appropriate to the risk level?

### Area 5: International Transfers (Chapter V)

**Think:** Does personal data leave the EEA? What safeguards apply?

**Act:** Identify:
- [ ] Transfer destinations
- [ ] Transfer mechanisms (SCCs, BCRs, adequacy)
- [ ] Supplementary measures (if required)
- [ ] Transfer Impact Assessments (TIAs)

**Observe:** Document transfer flows and legal basis.

**Reflect:** Are transfers legally defensible post-Schrems II?

### Area 6: Accountability & Governance (Articles 5, 24, 30)

**Think:** How does the organization demonstrate compliance?

**Act:** Check:
- [ ] Records of Processing Activities (RoPA)
- [ ] DPO appointment (if required)
- [ ] Data protection policies
- [ ] Training programs
- [ ] Audit trail maintenance
- [ ] Processor agreements (Article 28)

**Observe:** Document governance structure and evidence.

**Reflect:** Is there sufficient documentation for regulatory inquiry?

---

## Phase 2: Self-Critique Reflection

After completing the ReAct assessment, critically evaluate your findings:

### Accuracy Check
- Are all compliance determinations based on specific GDPR articles?
- Have I made any assumptions without evidence?
- Are there areas where I need more information?

### Completeness Check
- Did I assess all six core areas?
- Are there processing activities I may have missed?
- Have I considered all relevant data flows?

### Risk Assessment
- What are the highest-risk compliance gaps?
- What is the likelihood of regulatory scrutiny?
- What is the potential impact of non-compliance (fines, reputational)?

### Bias Check
- Am I being overly conservative or lenient?
- Have I considered the organization's specific context?
- Are my recommendations practical and proportionate?

---

## Output Format

Provide your assessment in this structure:

### 1. Executive Summary
- Overall compliance score (1-5 scale)
- Critical findings count
- Top 3 risks requiring immediate attention

### 2. Detailed Findings

| Area | Status | Gap | Risk Level | GDPR Article | Evidence |
|------|--------|-----|------------|--------------|----------|
| Lawful Basis | ✅/⚠️/❌ | [Gap description] | High/Med/Low | Art. X | [Evidence] |
| Data Subject Rights | ✅/⚠️/❌ | [Gap description] | High/Med/Low | Art. X | [Evidence] |
| Privacy by Design | ✅/⚠️/❌ | [Gap description] | High/Med/Low | Art. X | [Evidence] |
| Data Security | ✅/⚠️/❌ | [Gap description] | High/Med/Low | Art. X | [Evidence] |
| International Transfers | ✅/⚠️/❌ | [Gap description] | High/Med/Low | Art. X | [Evidence] |
| Accountability | ✅/⚠️/❌ | [Gap description] | High/Med/Low | Art. X | [Evidence] |

### 3. Remediation Roadmap

| Priority | Finding | Recommended Action | Owner | Timeline | Effort |
|----------|---------|-------------------|-------|----------|--------|
| P0 | [Critical gap] | [Specific action] | [Role] | [Date] | [Days] |
| P1 | [High gap] | [Specific action] | [Role] | [Date] | [Days] |
| P2 | [Medium gap] | [Specific action] | [Role] | [Date] | [Days] |

### 4. Self-Critique Summary
- Confidence level: High/Medium/Low
- Key assumptions made
- Additional information needed
- Areas requiring specialist legal review

### 5. Compliance Statement
[Draft compliance statement for the assessed processing activity]
```

---

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `[ORGANIZATION_OR_SYSTEM_NAME]` | Name of org or system being assessed | "Contoso Customer Portal" |
| `[DESCRIPTION_OF_DATA_PROCESSING]` | What processing occurs | "Collection and analysis of customer behavior for personalization" |
| `[TYPES_OF_PERSONAL_DATA_PROCESSED]` | Categories of data | "Name, email, browsing history, purchase history" |
| `[WHO_THE_DATA_IS_ABOUT]` | Data subject categories | "EU customers, website visitors" |
| `[WHY_DATA_IS_PROCESSED]` | Processing purposes | "Service delivery, marketing, analytics" |
| `[EXISTING_PRIVACY_CONTROLS]` | Current measures in place | "Consent management, encryption, access controls" |

---

## Example Usage

**Input:**

```text
## Assessment Context

**Organization/System:** Contoso E-Commerce Platform
**Processing Activity:** Customer account management and order processing
**Data Categories:** Name, email, address, payment details, order history, browsing behavior
**Data Subjects:** EU/UK retail customers
**Processing Purposes:** Order fulfillment, customer service, marketing (with consent), fraud prevention
**Current Controls:** SSL encryption, consent banner, privacy policy, customer portal for data access
```

**Output (Excerpt):**

```markdown
### 1. Executive Summary
- Overall compliance score: 3.5/5 (Moderate - Improvements Required)
- Critical findings: 2
- Top 3 risks:
  1. **Incomplete Records of Processing** - RoPA missing for marketing activities
  2. **Transfer mechanism gaps** - Third-party analytics uses US servers without SCCs
  3. **Consent granularity** - Single consent for multiple purposes violates specificity

### 2. Detailed Findings

| Area | Status | Gap | Risk Level | GDPR Article | Evidence |
|------|--------|-----|------------|--------------|----------|
| Lawful Basis | ⚠️ | Marketing consent bundled with T&Cs | High | Art. 6, 7 | Consent form review |
| Data Subject Rights | ✅ | Minor - DSR response time not documented | Low | Art. 12 | Process exists but SLA unclear |
| Privacy by Design | ⚠️ | No DPIA conducted for profiling | Medium | Art. 35 | Profiling for fraud detection |
| Data Security | ✅ | Adequate controls | Low | Art. 32 | SOC 2 Type II report |
| International Transfers | ❌ | US analytics provider lacks safeguards | High | Art. 44-49 | No SCCs in contract |
| Accountability | ⚠️ | Incomplete RoPA | Medium | Art. 30 | Missing marketing activities |

### 3. Remediation Roadmap

| Priority | Finding | Recommended Action | Owner | Timeline | Effort |
|----------|---------|-------------------|-------|----------|--------|
| P0 | US transfer without SCCs | Execute SCCs with analytics vendor or migrate to EU | Legal/IT | 30 days | 5 days |
| P0 | Bundled consent | Implement granular consent with separate opt-ins | Product | 45 days | 10 days |
| P1 | Missing DPIA | Conduct DPIA for fraud profiling | DPO | 60 days | 3 days |
| P2 | Incomplete RoPA | Update RoPA with marketing activities | Compliance | 30 days | 2 days |
```

---

## Tips

- **Start with high-risk processing** - Focus on automated decision-making, special category data, and large-scale processing first
- **Document everything** - GDPR requires demonstrable compliance; ensure all assessments are recorded
- **Engage legal counsel** - For complex transfers or novel processing, involve qualified legal advice
- **Use existing frameworks** - Leverage ISO 27701 controls mapping where certifications exist
- **Consider proportionality** - Recommendations should match the risk level and organizational resources
- **Plan for ongoing compliance** - GDPR is not a one-time exercise; build monitoring into processes

---

## Related Prompts

- [Privacy Impact Assessment Generator](privacy-impact-assessment.md) - For detailed DPIAs
- [Data Subject Request Handler](data-subject-request-handler.md) - For processing DSRs
- [SOC 2 Audit Preparation](soc2-audit-preparation.md) - For security compliance
