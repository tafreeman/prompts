---
name: Compliance Policy Generator
description: Prompt for drafting formal corporate policies aligned with industry standards (SOC 2, ISO 27001, NIST).
type: how_to
---

# Compliance Policy Generator

## Description

Draft formal corporate policies for security, privacy, and HR topics. Align policies with industry frameworks (SOC 2, ISO 27001, NIST) and organizational requirements.

## Prompt

You are a Senior Compliance Officer drafting a corporate policy.

### Policy Requirements
**Topic:** [topic]
**Framework:** [framework]
**Specific Requirements:** [requirements]

### Deliverables
Generate a formal policy document with these sections:
1. **Policy Statement**: Purpose and scope.
2. **Definitions**: Key terms.
3. **Roles and Responsibilities**: Who does what.
4. **Policy Requirements**: Specific rules and standards.
5. **Enforcement**: Consequences for non-compliance.
6. **Exceptions**: Process for requesting exceptions.
7. **Review Schedule**: Next review date.

### Format
- Use formal, authoritative tone.
- Reference specific framework controls where applicable.
- Include version number and effective date.

## Variables

- `[topic]`: E.g., "Acceptable Use Policy", "Password Management".
- `[framework]`: E.g., "SOC 2 CC6.1", "ISO 27001 A.9".
- `[requirements]`: Specific rules to include.

## Example

**Input**:
Topic: Password Management Policy
Framework: SOC 2 CC6.1
Requirements: 12-char minimum, MFA required, 90-day rotation

**Response**:
# Password Management Policy

**Version:** 1.0
**Effective Date:** 2026-01-20
**Next Review:** 2027-01-20

## 1. Policy Statement
This policy establishes password requirements to protect organizational systems.

## 2. Requirements
- Minimum length: 12 characters
- Complexity: Upper, lower, number, symbol
- MFA: Required for all privileged access
- Rotation: Every 90 days for service accounts

## 3. Enforcement
Violations may result in disciplinary action up to termination.
