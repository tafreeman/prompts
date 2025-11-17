# Governance & Compliance Prompts

This directory contains prompts tailored for governance, compliance, legal, security operations, and customer support teams. These prompts include governance metadata, risk assessments, and enterprise controls.

## What's Inside

### Legal Team Prompts
- `legal-contract-review.md` - Contract analysis and risk identification
- `legal-compliance-check.md` - Regulatory compliance verification
- `legal-policy-drafting.md` - Policy and terms creation

### Compliance Officer Prompts
- `compliance-audit-trail.md` - Audit trail documentation
- `compliance-risk-assessment.md` - Risk evaluation frameworks
- `compliance-policy-enforcement.md` - Policy compliance verification

### Customer Support Prompts
- `support-ticket-triage.md` - Ticket categorization and priority
- `support-escalation.md` - Escalation decision framework
- `support-response-template.md` - Response drafting with empathy

### Security Operations Prompts
- `security-incident-response.md` - Incident handling and containment
- `security-threat-modeling.md` - Threat identification and mitigation
- `security-vulnerability-assessment.md` - Security review and recommendations

## Governance Features

All prompts in this directory include:

### Governance Tags
- **PII-handling**: Indicates if prompt processes personally identifiable information
- **requires-human-review**: Specifies when human oversight is mandatory
- **audit-required**: Whether activity must be logged for compliance
- **data-classification**: Level of data sensitivity (Public, Internal, Confidential, Restricted)
- **regulatory-scope**: Relevant regulations (GDPR, HIPAA, SOX, PCI-DSS, etc.)

### Risk Assessment Metadata
- **risk-level**: Low, Medium, High, Critical
- **business-impact**: Financial, reputational, operational, legal consequences
- **approval-required**: Who must approve use (Manager, Director, VP, Legal, CISO)
- **retention-period**: How long records must be kept (e.g., 7 years for SOX)

## Usage Guidelines

### For Legal Teams
- All legal prompts require human review before final decisions
- Output must be reviewed by licensed attorney
- Do not use for legal advice to external parties without attorney approval
- Log all usage for privilege and work product protection

### For Compliance Officers
- Document all compliance assessments
- Maintain audit trail of all decisions
- Escalate findings per company policy
- Review prompts quarterly for regulatory updates

### For Customer Support
- PII must be redacted before using prompts
- Sensitive cases (legal, security, executive) require immediate escalation
- Log all customer interactions per retention policy
- Quality assurance review required for high-risk responses

### For Security Operations
- Incident response prompts for SOC/IR teams only
- All security findings must be logged in SIEM
- Critical findings require immediate escalation to CISO
- Threat intelligence sharing per TLP (Traffic Light Protocol)

## Compliance Frameworks Supported

- **GDPR** (General Data Protection Regulation) - EU data privacy
- **CCPA** (California Consumer Privacy Act) - California data privacy
- **HIPAA** (Health Insurance Portability and Accountability Act) - Healthcare data
- **SOX** (Sarbanes-Oxley Act) - Financial controls and reporting
- **PCI-DSS** (Payment Card Industry Data Security Standard) - Payment data
- **SOC 2** (Service Organization Control 2) - Data security and availability
- **ISO 27001** - Information security management
- **NIST** (National Institute of Standards and Technology) - Cybersecurity framework

## Related Resources

- [Advanced Techniques](../advanced-techniques/) - Advanced prompting patterns
- [Business Prompts](../business/) - General business use cases
- [System Prompts](../system/) - System-level configurations
