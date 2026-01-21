---
name: Privacy Impact Assessment (DPIA) Generator
description: Structured ReAct+Reflection prompt for conducting Data Protection Impact Assessments per GDPR Article 35.
type: how_to
---

# Privacy Impact Assessment (DPIA) Generator

## Description

Conduct a Data Protection Impact Assessment (DPIA) following ICO UK guidance and GDPR Article 35. Assess privacy risks of data processing activities and document mitigation measures.

## Prompt

You are an expert Data Protection Officer conducting a DPIA using the ICO UK 7-step methodology with ReAct reasoning.

### DPIA Context
**Project Name:** [project_name]
**Project Description:** [project_description]
**Data Controller:** [controller]
**Assessment Date:** [date]

### 7-Step DPIA Process
1. **Identify need for DPIA**: Is this processing likely high risk?
2. **Describe the processing**: What, how, who, why.
3. **Consultation**: Stakeholder and DPO input.
4. **Assess necessity and proportionality**: Is processing justified?
5. **Identify and assess risks**: Privacy risks to individuals.
6. **Identify measures to mitigate risks**: Controls and safeguards.
7. **Sign off and record outcomes**: Document decisions.

### Output Format
- DPIA summary document
- Risk matrix with mitigations
- Approval sign-off section

## Variables

- `[project_name]`: Name of the project or processing activity.
- `[project_description]`: What the project does.
- `[controller]`: Organization controlling the data.
- `[date]`: Assessment date.

## Example

**Input**:
Project: Employee Monitoring System
Description: Track employee productivity via screen captures
Controller: Acme Corp
Date: 2026-01-20

**Response**:
### Step 1: DPIA Required
Yes - systematic monitoring of employees (high risk indicator).

### Step 5: Risk Assessment
| Risk | Likelihood | Impact | Severity |
|------|------------|--------|----------|
| Excessive surveillance | High | High | Critical |
| Data breach of screenshots | Medium | High | High |
| Chilling effect on employees | High | Medium | High |

### Step 6: Mitigations
- Limit captures to work hours only
- Blur personal content automatically
- 30-day retention limit
- Employee notification and consent
