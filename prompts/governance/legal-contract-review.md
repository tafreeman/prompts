---
title: "Legal: Contract Review Assistant"
shortTitle: "Legal: Contract Review"
intro: "An AI-powered contract review assistant for legal teams to identify risks, unusual clauses, and compliance issues in commercial agreements. This prompt systematically analyzes contracts, highlights..."
type: "how_to"
difficulty: "advanced"
audience:
  - "solution-architect"
  - "senior-engineer"
platforms:
  - "claude"
topics:
  - "governance-compliance"
  - "risk-assessment"
  - "contract-review"
  - "legal"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-17"
governance_tags:
  - "requires-human-review"
  - "audit-required"
  - "CISO-approval-required"
dataClassification: "internal"
reviewStatus: "draft"
data_classification: "Confidential"
risk_level: "High"
regulatory_scope:
  - "general-commercial-law"
  - "contract-law"
approval_required: "Legal Counsel"
retention_period: "7 years"
---
# Legal: Contract Review Assistant

---

## Description

An AI-powered contract review assistant for legal teams to identify risks, unusual clauses, and compliance issues in commercial agreements. This prompt systematically analyzes contracts, highlights areas of concern, and provides structured risk assessments. **IMPORTANT: Output must be reviewed by licensed attorney before use.**

---

## Use Cases

- Initial contract review and risk triage
- Vendor agreement analysis
- NDA and partnership agreement review
- SaaS/software license agreement analysis
- Employment agreement review
- Identifying unusual or high-risk clauses
- Compliance gap analysis

---

## Prompt

```text
You are a legal contract review assistant helping attorneys analyze commercial agreements.

**Contract Type**: [CONTRACT_TYPE]

**Parties**: [PARTY_NAMES_AND_ROLES]

**Contract Text**: [FULL_CONTRACT_TEXT_OR_KEY_SECTIONS]

**Review Focus**: [SPECIFIC_CONCERNS_OR_GENERAL_REVIEW]

**Instructions**:

Perform a systematic contract review following this structure:

**1. Contract Summary**
- Type of agreement
- Parties and their roles
- Primary purpose and scope
- Term and termination provisions
- Financial terms (if applicable)

**2. Risk Assessment**

For each identified risk, provide:
- **Risk Category**: Liability, Financial, IP, Compliance, Operational, Reputational
- **Severity**: Critical, High, Medium, Low
- **Clause Reference**: Section number and brief quote
- **Description**: What the risk is
- **Potential Impact**: Financial or business consequences
- **Recommendation**: Suggested action (negotiate, accept with mitigation, reject, seek clarification)

**3. Unusual or Non-Standard Clauses**
- Identify clauses that deviate from market standards
- Explain why they're unusual
- Assess favorability (favorable to us, unfavorable, neutral)

**4. Missing Clauses**
- Standard clauses that should be present but aren't
- Why they're important
- Risk of omission

**5. Compliance Check**
- Applicable laws and regulations
- Compliance requirements
- Potential compliance risks

**6. Key Business Terms Analysis**
- Payment terms
- Liability caps and limitations
- Indemnification obligations
- Intellectual property rights
- Confidentiality obligations
- Termination rights and consequences

**7. Red Flags**
List any immediate concerns requiring escalation:
- Unlimited liability
- Unusual indemnification
- Problematic IP assignments
- Concerning dispute resolution
- Unreasonable restrictions

**8. Overall Risk Rating**
- **Overall Risk**: Critical/High/Medium/Low
- **Recommendation**: Proceed/Negotiate/Reject/Escalate
- **Priority Action Items**: Top 3-5 items to address

**9. Questions for Business Team**
- Clarifications needed from business stakeholders
- Missing context required for full assessment

**DISCLAIMER**: This is an AI-assisted review. All findings must be reviewed and validated by a licensed attorney before taking any action. This does not constitute legal advice.
```text

---

## Variables

- `[CONTRACT_TYPE]`: Type of agreement (NDA, MSA, SaaS Agreement, Employment Contract, etc.)
- `[PARTY_NAMES_AND_ROLES]`: Who is signing (Company A as Provider, Company B as Customer, etc.)
- `[FULL_CONTRACT_TEXT_OR_KEY_SECTIONS]`: Complete contract or specific sections to review
- `[SPECIFIC_CONCERNS_OR_GENERAL_REVIEW]`: Particular concerns (liability, IP, data privacy) or comprehensive review

---

## Example Usage

**Input:**

```text
You are a legal contract review assistant helping attorneys analyze commercial agreements.

**Contract Type**: Software-as-a-Service (SaaS) Agreement

**Parties**: 
- Vendor: CloudTech Solutions Inc. (Provider)
- Customer: Acme Corporation (Customer)

**Contract Text**: [Excerpt of key clauses]

Section 5.2 Liability:
"Provider shall not be liable for any indirect, incidental, consequential, or punitive damages arising from the use of the Services, regardless of the form of action. Provider's total liability under this Agreement shall not exceed the amount paid by Customer in the twelve (12) months preceding the claim."

Section 7.1 Data Processing:
"Provider may use Customer Data to improve the Services, train machine learning models, and create aggregated analytics. Customer grants Provider a perpetual, worldwide, royalty-free license to use Customer Data for these purposes."

Section 9.1 Termination:
"Either party may terminate this Agreement for convenience upon 30 days' written notice. Upon termination, all Customer Data will be deleted within 30 days, with no option for retrieval."

Section 11.3 Governing Law:
"This Agreement shall be governed by the laws of the Cayman Islands. All disputes shall be resolved through binding arbitration in George Town, Cayman Islands."

**Review Focus**: Data privacy compliance (GDPR) and liability protection

**Instructions**: [As specified above]
```text

---

## Tips

- **Always include full context**: Contract type, parties, industry, jurisdiction
- **Prioritize risks**: Lead with Critical and High severity issues
- **Be specific**: Reference exact clause numbers and quote relevant text
- **Quantify impact**: Estimate financial exposure when possible
- **Provide alternatives**: Don't just say "problematic" - offer negotiation language
- **Check completeness**: Review for missing standard clauses
- **Escalate appropriately**: Flag truly critical issues clearly
- **Attorney review mandatory**: AI analysis is a starting point, not final legal advice

## Governance & Compliance

### Required Workflow

1. **Input Validation**: Ensure contract is redacted of unnecessary PII before analysis
2. **AI Analysis**: Use this prompt to generate initial review
3. **Attorney Review**: Licensed attorney must review and validate all findings
4. **Business Consultation**: Discuss business context with stakeholders
5. **Negotiation**: Attorney leads negotiations based on findings
6. **Final Approval**: General Counsel or authorized signatory approves
7. **Audit Logging**: Log analysis, review, approval in legal management system

### Audit Requirements

- **Log all usage**: Timestamp, user, contract ID, risk findings
- **Retain analysis**: 7 years (standard legal document retention)
- **Track outcomes**: Document which risks were negotiated, accepted, or rejected
- **Review accuracy**: Quarterly review of AI findings vs. attorney assessment

### Access Control

- **Who can use**: Legal team, compliance officers (with attorney supervision)
- **Not for use by**: Sales, general employees, external parties
- **Approval required**: Legal Counsel must review output before sharing with business

---

## Output Schema (JSON)

```json
{
  "contract_summary": {
    "type": "...",
    "parties": ["...", "..."],
    "purpose": "...",
    "term": "..."
  },
  "risks": [
    {
      "category": "IP|Financial|Compliance|Liability|Operational",
      "severity": "Critical|High|Medium|Low",
      "clause_reference": "Section X.Y",
      "description": "...",
      "impact": "...",
      "recommendation": "..."
    }
  ],
  "unusual_clauses": ["...", "..."],
  "missing_clauses": ["...", "..."],
  "compliance_issues": [
    {
      "regulation": "GDPR|CCPA|HIPAA|...",
      "violation": "...",
      "consequence": "...",
      "remediation": "..."
    }
  ],
  "overall_assessment": {
    "risk_rating": "Critical|High|Medium|Low",
    "recommendation": "Proceed|Negotiate|Reject|Escalate",
    "priority_actions": ["...", "..."]
  },
  "attorney_review_required": true,
  "audit_metadata": {
    "timestamp": "...",
    "reviewer_id": "...",
    "contract_id": "..."
  }
}
```text

---

## Related Prompts

<!-- Links removed - files don't exist yet -->
