---

title: "Legal: Contract Review Assistant"
category: "governance-compliance"
tags: ["legal", "contract-review", "risk-assessment", "compliance", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-17"
difficulty: "advanced"
governance_tags: ["requires-human-review", "audit-required", "attorney-approval-required"]
data_classification: "Confidential"
risk_level: "High"
regulatory_scope: ["general-commercial-law", "contract-law"]
approval_required: "Legal Counsel"
retention_period: "7 years"
platform: "Claude Sonnet 4.5"
---

# Legal: Contract Review Assistant

## Description

An AI-powered contract review assistant for legal teams to identify risks, unusual clauses, and compliance issues in commercial agreements. This prompt systematically analyzes contracts, highlights areas of concern, and provides structured risk assessments. **IMPORTANT: Output must be reviewed by licensed attorney before use.**

## Use Cases

- Initial contract review and risk triage
- Vendor agreement analysis
- NDA and partnership agreement review
- SaaS/software license agreement analysis
- Employment agreement review
- Identifying unusual or high-risk clauses
- Compliance gap analysis

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
```

## Variables

- `[CONTRACT_TYPE]`: Type of agreement (NDA, MSA, SaaS Agreement, Employment Contract, etc.)
- `[PARTY_NAMES_AND_ROLES]`: Who is signing (Company A as Provider, Company B as Customer, etc.)
- `[FULL_CONTRACT_TEXT_OR_KEY_SECTIONS]`: Complete contract or specific sections to review
- `[SPECIFIC_CONCERNS_OR_GENERAL_REVIEW]`: Particular concerns (liability, IP, data privacy) or comprehensive review

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
```

**Output:**

```text
**1. Contract Summary**
- **Type**: Software-as-a-Service (SaaS) Agreement
- **Parties**: CloudTech Solutions (Provider) / Acme Corporation (Customer)
- **Purpose**: Cloud-based software services provision
- **Term**: Not provided in excerpt (needs clarification)
- **Financial**: Based on prior 12 months' payments (amount not specified)

**2. Risk Assessment**

**Risk #1: Unlimited Data License Grant**
- **Risk Category**: Intellectual Property / Data Privacy
- **Severity**: **CRITICAL**
- **Clause Reference**: Section 7.1 - "perpetual, worldwide, royalty-free license to use Customer Data"
- **Description**: Customer grants Provider unrestricted, perpetual rights to Customer Data, including for training ML models. This is extremely broad and likely violates GDPR Article 5(1)(b) (purpose limitation) and Article 6 (lawful basis).
- **Potential Impact**: 
  - GDPR violation risk: Fines up to €20M or 4% of global revenue
  - Loss of control over proprietary/sensitive data
  - Competitive risk if data used to benefit competitors
  - Cannot comply with data subject deletion requests (GDPR Article 17)
- **Recommendation**: **REJECT this clause as written. Negotiate:**
  - Remove "perpetual" - limit to term of agreement
  - Remove ML training rights entirely, or limit to non-PII aggregate data
  - Add GDPR Data Processing Addendum (DPA)
  - Require explicit consent for any secondary use

**Risk #2: Irreversible Data Deletion**
- **Risk Category**: Operational / Compliance
- **Severity**: **HIGH**
- **Clause Reference**: Section 9.1 - "all Customer Data will be deleted within 30 days, with no option for retrieval"
- **Description**: Automatic deletion with no retrieval option creates business continuity risk and potential compliance issues (data retention requirements).
- **Potential Impact**:
  - Loss of business-critical data
  - Inability to comply with legal hold/discovery requests
  - No time to verify complete migration before deletion
- **Recommendation**: **NEGOTIATE:**
  - 90-day retention window instead of 30 days
  - Option to export all data before deletion
  - Secure deletion certification provided
  - Exception for legal hold requirements

**Risk #3: Cayman Islands Arbitration**
- **Risk Category**: Legal / Operational
- **Severity**: **HIGH**
- **Clause Reference**: Section 11.3 - Cayman Islands law and arbitration
- **Description**: Unusual jurisdiction choice (not where either party is located) significantly increases dispute resolution costs and complexity. Cayman Islands law may not have well-developed case law for SaaS disputes.
- **Potential Impact**:
  - $100K+ travel costs for arbitration
  - Unfamiliar legal framework
  - Difficulty enforcing judgment
  - Delay in dispute resolution
- **Recommendation**: **NEGOTIATE:**
  - Change to jurisdiction where Customer is headquartered
  - If overseas arbitration required, use established venue (e.g., ICC Paris, AAA)
  - Add mediation step before arbitration
  - Specify English as arbitration language

**Risk #4: Liability Cap Too Low**
- **Risk Category**: Financial
- **Severity**: **MEDIUM**
- **Clause Reference**: Section 5.2 - Liability capped at "twelve (12) months preceding the claim"
- **Description**: Liability cap of 12 months' fees may be insufficient if Service failure causes significant business harm. Standard for SaaS is 12-24 months, but should align with potential damages.
- **Potential Impact**:
  - Unrecoverable damages if Service causes >12 months fees in harm
  - Example: If fees are $100K/year, cap is $100K - but data breach could cost millions
- **Recommendation**: **NEGOTIATE based on risk:**
  - For critical systems: Increase to 24 months or $X million minimum
  - Carve out unlimited liability for: data breaches, IP infringement, gross negligence
  - Add insurance requirement ($X million cyber liability coverage)

**3. Unusual or Non-Standard Clauses**

**Clause: Perpetual Data License (Section 7.1)**
- **Why Unusual**: Market standard is "during Term + limited post-Term for wind-down"
- **Favorability**: **Extremely unfavorable to Customer**
- **Market Standard**: Provider may use aggregated, anonymized data for analytics; no perpetual license; no ML training on customer data without explicit consent

**Clause: Cayman Islands Jurisdiction (Section 11.3)**
- **Why Unusual**: Neither party located there; unusual for SaaS contracts
- **Favorability**: **Unfavorable to both parties** (adds cost/complexity)
- **Market Standard**: Jurisdiction of defendant's location or mutual third-party (e.g., Delaware for US contracts)

**4. Missing Clauses**

**Missing: Data Processing Addendum (DPA)**
- **Why Important**: Required for GDPR compliance when Provider processes Customer personal data
- **Risk of Omission**: GDPR violation, cannot legally transfer data to Provider under Chapter V

**Missing: Data Breach Notification**
- **Why Important**: Customer needs to know about breaches to comply with GDPR Article 33 (72-hour notification)
- **Risk of Omission**: Cannot meet Customer's own regulatory obligations

**Missing: Service Level Agreement (SLA)**
- **Why Important**: No uptime guarantee means no recourse if Service is unavailable
- **Risk of Omission**: No credits/refunds for outages, business continuity risk

**Missing: Data Residency / International Transfers**
- **Why Important**: GDPR requires knowing where data is processed and transferred
- **Risk of Omission**: Cannot ensure data stays in EU/adequate jurisdiction

**Missing: Audit Rights**
- **Why Important**: Common for enterprise SaaS, especially for compliance audits
- **Risk of Omission**: Cannot verify Provider's security/compliance claims

**5. Compliance Check**

**Applicable Regulations**:
- **GDPR** (General Data Protection Regulation) - If processing EU personal data
- **CCPA** (California Consumer Privacy Act) - If processing California residents' data
- **Industry-specific**: Depending on Customer's industry (HIPAA, PCI-DSS, etc.)

**Compliance Risks**:

⚠️ **GDPR Violation - Section 7.1 (Data License)**
- **Issue**: Perpetual, unlimited license to Customer Data violates:
  - Article 5(1)(b): Purpose limitation
  - Article 5(1)(e): Storage limitation
  - Article 6: Lacks lawful basis for ML training
  - Article 17: Cannot honor deletion requests
- **Consequence**: €20M fine or 4% global revenue + regulatory action
- **Action Required**: Must add comprehensive DPA and limit data use

⚠️ **GDPR Violation - Missing Data Transfer Mechanism**
- **Issue**: No mention of Standard Contractual Clauses (SCCs) or adequacy decision
- **Consequence**: Unlawful data transfer under Chapter V
- **Action Required**: Add SCCs if Provider not in EU/adequate country

⚠️ **GDPR Violation - Missing Breach Notification**
- **Issue**: Customer needs breach notification to comply with Article 33
- **Consequence**: Customer cannot meet 72-hour notification requirement
- **Action Required**: Add breach notification clause (24-48 hours to Customer)

**6. Key Business Terms Analysis**

[Note: Full contract not provided, analyzing available terms]

**Data Rights**:
- ❌ **Problematic**: Provider gets perpetual license to Customer Data
- **Market Standard**: Customer retains all rights; Provider license limited to Service provision

**Liability Protection**:
- ⚠️ **Moderate**: 12-month cap may be insufficient
- **Assessment**: Review against risk (if critical system, negotiate higher cap)

**Data Deletion**:
- ❌ **Problematic**: Irreversible 30-day deletion
- **Market Standard**: 60-90 days with export option before deletion

**Termination**:
- ✓ **Acceptable**: 30-day termination for convenience
- **Note**: Ensure sufficient time to migrate data (may need longer notice for critical systems)

**Dispute Resolution**:
- ❌ **Problematic**: Cayman Islands arbitration
- **Market Standard**: Arbitration in neutral, established venue or courts of Customer's jurisdiction

**7. Red Flags - IMMEDIATE CONCERNS**

🚨 **RED FLAG #1**: Perpetual Data License (Section 7.1)
- **Why Critical**: Allows unlimited data use forever, including ML training
- **GDPR Violation**: Multiple articles violated
- **Action**: Must be removed or heavily modified before signing

🚨 **RED FLAG #2**: No Data Processing Addendum
- **Why Critical**: Cannot legally process EU personal data without DPA
- **GDPR Violation**: Chapter V (international transfers)
- **Action**: Must add GDPR-compliant DPA (can use EU Standard Contractual Clauses)

🚨 **RED FLAG #3**: Irreversible Data Deletion
- **Why Critical**: Business continuity risk + legal hold issue
- **Action**: Negotiate data export option and longer retention

⚠️ **CONCERN #4**: Cayman Islands Arbitration
- **Why Concerning**: High cost, unfamiliar law, enforcement risk
- **Action**: Change to established arbitration venue

**8. Overall Risk Rating**

- **Overall Risk**: **CRITICAL**
- **Recommendation**: **DO NOT SIGN WITHOUT MAJOR REVISIONS**
- **Priority Action Items**:
  1. **MUST FIX**: Remove or heavily restrict Section 7.1 (data license) + add DPA
  2. **MUST FIX**: Add GDPR Data Processing Addendum (DPA) with SCCs
  3. **MUST FIX**: Add data breach notification clause (24-48 hours)
  4. **SHOULD FIX**: Change jurisdiction to US/EU (not Cayman Islands)
  5. **SHOULD FIX**: Add data export option before deletion

**Without these changes, this contract:**
- Violates GDPR (potential €20M fine)
- Creates unacceptable IP/data risk
- Provides inadequate liability protection
- Presents operational continuity risk

**9. Questions for Business Team**

1. **Data Sensitivity**: What type of data will be processed? (PII, financial, health, proprietary?)
2. **User Location**: Are any users in EU/California? (Determines GDPR/CCPA applicability)
3. **Business Criticality**: How critical is this Service to operations? (Determines acceptable liability cap)
4. **Budget**: What is annual contract value? (Validates if liability cap is reasonable)
5. **Alternatives**: Are there alternative providers with better terms?
6. **Timeline**: What's urgency to sign? (Determines negotiation leverage)

**DISCLAIMER**: This is an AI-assisted contract review tool. This analysis must be reviewed and validated by a licensed attorney before making any legal decisions. This does not constitute legal advice. No attorney-client relationship is created.
```

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
```

## Related Prompts

- [Legal: Compliance Check](legal-compliance-check.md) - Regulatory compliance verification
- [Compliance: Risk Assessment](compliance-risk-assessment.md) - General risk evaluation
- [Security: Vendor Assessment](security-vendor-assessment.md) - Security review of vendors

## Changelog

### Version 1.0 (2025-11-17)

- Initial release
- Comprehensive contract review framework
- GDPR and privacy compliance focus
- Risk categorization and severity assessment
- Attorney review requirement emphasized
- Audit and governance controls included
