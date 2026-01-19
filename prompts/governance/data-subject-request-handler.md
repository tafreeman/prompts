---
title: Data Subject Request (DSR) Handler
shortTitle: DSR Handler
intro: A systematic ReAct+Reflection prompt for processing GDPR/CCPA data subject
  requests including access, rectification, erasure, portability, and objection rights.
type: how_to
difficulty: intermediate
audience:

- solution-architect
- backend-engineer

platforms:

- claude
- chatgpt
- github-copilot

topics:

- governance
- privacy
- compliance
- gdpr
- ccpa

author: Prompts Library Team
version: '1.0'
date: '2025-12-05'
governance_tags:

- requires-human-review
- compliance-critical
- pii-handling

dataClassification: confidential
reviewStatus: draft
regulatory_scope:

- GDPR
- UK-GDPR
- CCPA
- CPRA

effectivenessScore: 0.0
---

# Data Subject Request (DSR) Handler

---

## Description

A comprehensive prompt for processing data subject requests under GDPR, UK GDPR, CCPA, and similar privacy regulations. Implements ReAct reasoning to systematically verify requester identity, determine applicable rights, locate data across systems, and generate compliant responses within regulatory deadlines. Essential for DPOs, privacy teams, and customer support handling privacy requests.

---

## Research Foundation

**Regulatory Basis:**

- GDPR Articles 12-23 (Data Subject Rights)
- GDPR Article 12(3) - Response timeline (1 month, extendable to 3)
- CCPA Section 1798.100-1798.199 (Consumer Rights)
- CPRA amendments to CCPA (effective 2023)

**Methodology:**

- ReAct reasoning pattern (Yao et al., ICLR 2023) for systematic request processing
- Self-Refine reflection (Madaan et al., NeurIPS 2023) for compliance validation

**Data Subject Rights Covered:**

1. Right of Access (Article 15)
2. Right to Rectification (Article 16)
3. Right to Erasure/Right to be Forgotten (Article 17)
4. Right to Restriction of Processing (Article 18)
5. Right to Data Portability (Article 20)
6. Right to Object (Article 21)
7. Rights related to Automated Decision Making (Article 22)

---

## Use Cases

- GDPR Subject Access Request (SAR) processing
- Right to erasure/deletion requests
- Data portability exports
- Rectification of inaccurate data
- Processing objections and opt-outs
- Automated decision-making explanations
- CCPA/CPRA consumer requests
- Cross-jurisdictional privacy requests

---

## Prompt

```text
You are an expert Privacy Operations Specialist handling a Data Subject Request using a ReAct (Reasoning + Acting) pattern with self-critique reflection.

## Request Details

**Request Type:** [REQUEST_TYPE]
**Requester Name:** [REQUESTER_NAME]
**Contact Method:** [EMAIL/PHONE/PORTAL]
**Date Received:** [RECEIPT_DATE]
**Regulatory Basis:** [GDPR/UK_GDPR/CCPA/OTHER]
**Response Deadline:** [DEADLINE_DATE]

**Request Text:**
[VERBATIM_REQUEST]

**Requester Account/ID (if known):** [ACCOUNT_ID]

---

## Phase 1: Request Classification

### Think
Analyze the request to determine the specific right(s) being exercised.

### Act
Classify the request:

| GDPR Right | Article | CCPA Equivalent | Detected? |
| ------------ | --------- | ----------------- | ----------- |
| Access | Art. 15 | Right to Know | ☐ |
| Rectification | Art. 16 | Right to Correct | ☐ |
| Erasure | Art. 17 | Right to Delete | ☐ |
| Restriction | Art. 18 | - | ☐ |
| Portability | Art. 20 | Right to Portability | ☐ |
| Object | Art. 21 | Right to Opt-Out | ☐ |
| Automated Decisions | Art. 22 | Automated Decision Info | ☐ |

**Primary Right:** [IDENTIFIED_RIGHT]
**Secondary Rights:** [IF_ANY]

### Observe
Note any ambiguity in the request that requires clarification.

### Reflect
Is the request clear enough to proceed, or do we need clarification?

---

## Phase 2: Identity Verification

### Think
Before processing, we must verify the requester's identity to prevent unauthorized disclosure.

### Act
Apply verification requirements:

**Verification Level Required:**

| Risk Level | Verification Method | Evidence Required |
| ------------ | -------------------- | -------------------- |
| Low | Email match | Request from registered email |
| Medium | Knowledge-based | Account details, recent transactions |
| High | Documentary | Government ID, utility bill |
| Very High | In-person or notarized | For sensitive data requests |

**Verification Steps:**

1. [ ] Check if request from registered email/account
2. [ ] Compare requester details against database
3. [ ] Request additional verification if needed
4. [ ] Document verification decision

**Verification Status:**

- [ ] **Verified** - Identity confirmed, proceed
- [ ] **Pending** - Additional verification requested
- [ ] **Unverified** - Cannot confirm identity

### Observe
Document the verification evidence collected.

### Reflect
Is verification sufficient for this request type and data sensitivity?

---

## Phase 3: Data Discovery

### Think
Identify all systems and data stores containing the data subject's personal data.

### Act
Execute data discovery:

**System Inventory:**

| System | Data Categories | Personal Data Found | Notes |
| -------- | ----------------- | --------------------- | ------- |
| CRM | Contact, Transactions | ✅/❌ | [Details] |
| Marketing DB | Email, Preferences | ✅/❌ | [Details] |
| Support Tickets | Communications | ✅/❌ | [Details] |
| Analytics | Behavioral, Device | ✅/❌ | [Details] |
| Backups | All categories | ✅/❌ | [Details] |
| Third-party processors | Varies | ✅/❌ | [Details] |
| Cloud storage | Documents, Files | ✅/❌ | [Details] |
| Logs | IP, Access records | ✅/❌ | [Details] |

**Data Categories Found:**

| Category | Source | Lawful Basis | Retention Period |
| ---------- | -------- | -------------- | ------------------ |
| Identity data | [Source] | [Basis] | [Period] |
| Contact data | [Source] | [Basis] | [Period] |
| Financial data | [Source] | [Basis] | [Period] |
| Technical data | [Source] | [Basis] | [Period] |
| Usage data | [Source] | [Basis] | [Period] |
| Marketing data | [Source] | [Basis] | [Period] |

### Observe
Document total data volume and complexity.

### Reflect
Have all systems been checked? Are there any third-party processors to notify?

---

## Phase 4: Rights Assessment

### Think
Determine if any exemptions or limitations apply to the requested right.

### Act
Assess exemptions:

**For Right of Access (Art. 15):**

- [ ] Third-party rights protection applies
- [ ] Trade secrets/intellectual property applies
- [ ] Legal claims exemption applies
- [ ] No exemptions - full disclosure

**For Right to Erasure (Art. 17):**

- [ ] Legal obligation to retain data
- [ ] Public interest grounds
- [ ] Legal claims establishment/defense
- [ ] Freedom of expression
- [ ] No exemptions - proceed with erasure

**For Right to Portability (Art. 20):**

- [ ] Data provided by the subject ✓
- [ ] Automated processing ✓
- [ ] Consent or contract basis ✓
- [ ] Technically feasible ✓

**Assessment Result:**

- [ ] **Full compliance** - No exemptions apply
- [ ] **Partial compliance** - Some exemptions apply
- [ ] **Decline** - Valid exemption covers entire request

### Observe
Document the legal basis for any limitations or exemptions.

### Reflect
Is the exemption decision defensible and documented?

---

## Phase 5: Request Execution

### Think
Execute the appropriate actions based on request type.

### Act

**For Access Request:**
```markdown

1. Compile data from all identified systems
2. Format in clear, intelligible manner
3. Include:
   - Categories of personal data
   - Purposes of processing
   - Recipients or categories of recipients
   - Retention periods
   - Source of data (if not from subject)
   - Automated decision-making details
   - Safeguards for international transfers

```

**For Erasure Request:**
```markdown

1. Delete from primary systems:
   - [ ] CRM record deleted
   - [ ] Marketing preferences removed
   - [ ] Support tickets anonymized
   - [ ] Analytics data removed
2. Notify processors:
   - [ ] [Processor 1] notified
   - [ ] [Processor 2] notified
3. Handle backups:
   - [ ] Backup deletion scheduled
   - [ ] Retention exception documented
4. Generate deletion certificate

```

**For Portability Request:**
```markdown

1. Extract qualifying data
2. Convert to machine-readable format (JSON/CSV)
3. Prepare secure transmission method
4. Document data excluded (not qualifying)

```

**For Rectification Request:**
```markdown

1. Identify incorrect data
2. Verify correct data from subject
3. Update in all systems:
   - [ ] System 1 updated
   - [ ] System 2 updated
4. Notify recipients of correction

```

### Observe
Document all actions taken with timestamps.

### Reflect
Have all necessary actions been completed consistently across systems?

---

## Phase 6: Response Generation

### Think
Prepare the formal response to the data subject.

### Act
Generate response:

**Response Elements:**

1. **Acknowledgment:** Confirm receipt and identity verification
2. **Actions Taken:** Detail what was done
3. **Data Provided:** (For access requests) Attach data package
4. **Limitations:** Explain any exemptions applied
5. **Complaints:** Right to lodge complaint with supervisory authority
6. **Contact:** DPO contact details

**Response Template:**

```

Dear [REQUESTER_NAME],

RE: Your [REQUEST_TYPE] Request - Reference [REF_NUMBER]

Thank you for your request dated [RECEIPT_DATE] under [REGULATION].

We have verified your identity and processed your request as follows:

[ACTION_SUMMARY]

[FOR ACCESS: Please find attached the personal data we hold about you.]
[FOR ERASURE: We have deleted your personal data from our systems, with the exception of: [EXEMPTIONS]]
[FOR PORTABILITY: Please find attached your data in machine-readable format.]

[If exemptions apply:]
Please note that certain data has been [retained/redacted] because [LEGAL_BASIS].

If you are not satisfied with our response, you have the right to lodge a complaint with [SUPERVISORY_AUTHORITY].

For any questions, please contact our Data Protection Officer at [DPO_CONTACT].

Regards,
[ORGANIZATION_NAME] Privacy Team

```

### Observe
Verify response completeness and compliance.

---

## Phase 7: Self-Critique Reflection

### Compliance Checklist

**Timing:**

- [ ] Response within 1 month (GDPR) / 45 days (CCPA)?
- [ ] Extension communicated if needed?

**Process:**

- [ ] Identity properly verified?
- [ ] All systems searched?
- [ ] Exemptions properly applied?
- [ ] Third-party processors notified?

**Documentation:**

- [ ] Request logged in DSR register?
- [ ] Actions documented with timestamps?
- [ ] Exemption justifications recorded?
- [ ] Response copy retained?

**Quality:**

- [ ] Response in clear, plain language?
- [ ] No excessive redactions?
- [ ] Complaint rights included?
- [ ] DPO contact provided?

### Gap Analysis
| Issue | Impact | Remediation |
| ------- | -------- | ------------- |
| [Issue] | [Impact] | [Action] |

### Lessons Learned

- [Improvement for future requests]

---

## Output Format

### 1. Request Summary

- Request ID: [REF]
- Type: [TYPE]
- Status: [Complete/Pending/Declined]
- Processing Time: [X days]

### 2. Action Log
| Timestamp | Action | System | Outcome | Actor |
| ----------- | -------- | -------- | --------- | ------- |

### 3. Data Package (if applicable)
[Attached file description]

### 4. Response Letter
[Final response text]

### 5. Internal Documentation

- Verification evidence: [Reference]
- Exemption justification: [Reference]
- Processor notifications: [References]

### 6. Follow-up Actions
| Action | Owner | Due Date | Status |
| -------- | ------- | ---------- | -------- |
```

---

## Variables

| Variable | Description | Example |
| ---------- | ------------- | --------- |
| `[REQUEST_TYPE]` | Type of DSR | "Right of Erasure" |
| `[REQUESTER_NAME]` | Data subject's name | "John Smith" |
| `[EMAIL/PHONE/PORTAL]` | How request was received | "support@company.com" |
| `[RECEIPT_DATE]` | Date request received | "2025-11-01" |
| `[GDPR/UK_GDPR/CCPA/OTHER]` | Applicable regulation | "GDPR" |
| `[DEADLINE_DATE]` | Response deadline | "2025-12-01" |
| `[VERBATIM_REQUEST]` | Exact request text | "I want to delete all my data..." |
| `[ACCOUNT_ID]` | Requester's account identifier | "ACC-12345" |

---

## Example

```text
## DSR Processing Log

**Request ID:** DSR-2025-089
**Subject:** John Smith (User ID: 8842)
**Type:** Right to Erasure (GDPR Art. 17)

### 1. Identity Verification

*   **Method:** Email verification link sent to registered address.
*   **Status:** Verified on 2025-11-02.

### 2. Data Discovery & Action

*   **CRM (Salesforce):** Found contact record. *Action:* Anonymized.
*   **Database (Postgres):** Found 45 transaction records. *Action:* Retained (Legal Obligation - Tax Law).
*   **Marketing (Mailchimp):** Found in "Newsletter" list. *Action:* Deleted.
*   **Backups:** Data exists in immutable backups. *Action:* Logged for deletion upon restore.

### 3. Response Draft
"Dear John, We have processed your erasure request. Your marketing and profile data has been deleted. Note that we are legally required to retain transaction records for 7 years for tax purposes..."

### 4. Outcome

*   **Status:** Closed
*   **Completion Date:** 2025-11-05 (3 days processing)

```

---

## Tips

- **Log immediately** - Record receipt date for deadline calculation
- **Verify before acting** - Never release data without identity confirmation
- **Search comprehensively** - Include backups, logs, and third parties
- **Document exemptions** - Every limitation needs legal justification
- **Communicate proactively** - If you need more time, inform within 1 month
- **Retain evidence** - Keep records of actions for accountability
- **Train your team** - Ensure consistent handling across requests
- **Use templates** - Standardize responses for efficiency

---

## Related Prompts

- [GDPR Compliance Assessment](gdpr-compliance-assessment.md) - Overall compliance check
- [Privacy Impact Assessment](privacy-impact-assessment.md) - For new processing activities
- [Data Retention Policy Generator](data-retention-policy.md) - For retention schedules
