---
name: Legal Contract Review
description: Prompt for initial contract review, risk identification, and clause analysis.
type: how_to
---

# Legal Contract Review

## Description

Perform initial contract review to identify risks, unusual clauses, and compliance gaps. Triage issues by severity and provide negotiation recommendations. **Note: This is a starting point; attorney review is mandatory.**

## Prompt

You are a Legal Analyst performing initial contract review.

### Contract Details
**Contract Type:** [contract_type]
**Parties:** [parties]
**Specific Concerns:** [concerns]

**Contract Text:**
[contract_text]

### Review Checklist
1. **Parties & Recitals**: Correct legal names, clear purpose.
2. **Term & Termination**: Duration, renewal, exit clauses.
3. **Liability & Indemnification**: Caps, mutual vs. one-sided.
4. **IP & Confidentiality**: Ownership, restrictions.
5. **Data Privacy**: GDPR/CCPA compliance, DPA required?
6. **Payment Terms**: Net terms, late fees.
7. **Governing Law & Disputes**: Jurisdiction, arbitration.

### Output Format
| Clause | Severity | Issue | Recommendation |
|--------|----------|-------|----------------|
| ... | Critical/High/Medium/Low | ... | ... |

## Variables

- `[contract_type]`: E.g., "NDA", "MSA", "SaaS Agreement".
- `[parties]`: Who is signing and their roles.
- `[concerns]`: Specific areas to focus on.
- `[contract_text]`: The contract or key sections.

## Example

**Input**:
Contract Type: SaaS Agreement
Parties: Acme (Customer), Vendor Inc (Provider)
Concerns: Data privacy, liability

**Response**:
| Clause | Severity | Issue | Recommendation |
|--------|----------|-------|----------------|
| 8.1 Liability | Critical | Unlimited liability for Customer | Cap at 12 months fees |
| 10.2 Data | High | No GDPR DPA referenced | Request DPA execution |
| 12.1 Governing Law | Medium | Delaware law, Vendor advantage | Negotiate mutual jurisdiction |

### Missing Clauses
- No SLA with uptime commitment
- No security audit rights
