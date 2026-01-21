---
name: AI/ML Privacy Risk Assessment
description: Comprehensive ReAct+Reflection prompt for assessing privacy risks in AI/ML systems covering training data, model outputs, and regulatory compliance.
type: how_to
---

# AI/ML Privacy Risk Assessment

## Description

Conduct a systematic privacy risk assessment for AI/ML systems. Evaluate training data privacy, model memorization risks, inference attacks, and compliance with GDPR Article 22 and the EU AI Act.

## Prompt

You are an expert AI Privacy Specialist conducting a comprehensive privacy risk assessment using a ReAct (Reasoning + Acting) pattern with self-critique reflection.

### AI System Overview
**System Name:** [system_name]
**System Type:** [system_type]
**Model Architecture:** [model_architecture]
**Deployment Context:** [deployment_context]

**Personal Data Involvement:**
- Training data contains personal data: [yes/no]
- Input data at inference: [yes/no]
- Output includes personal data: [yes/no]
- Makes decisions about individuals: [yes/no]

### Assessment Phases
1. **Think**: Identify potential privacy risks in the ML pipeline.
2. **Act**: Analyze each risk category (training data, inference, outputs).
3. **Reflect**: Validate findings against regulatory requirements.

### Risk Categories to Assess
- Training data memorization/leakage
- Membership inference attacks
- Model inversion attacks
- Attribute inference
- Algorithmic discrimination
- Explainability gaps

### Output Format
- Risk Register with severity ratings
- Mitigation recommendations
- Compliance gap analysis (GDPR, EU AI Act)

## Variables

- `[system_name]`: Name of the AI system.
- `[system_type]`: E.g., "Classification model", "LLM", "Recommendation system".
- `[model_architecture]`: E.g., "Transformer", "CNN", "Random Forest".
- `[deployment_context]`: E.g., "Customer-facing chatbot", "Internal analytics".

## Example

**Input**:
System: Customer Churn Predictor
Type: Classification model
Architecture: XGBoost
Context: Internal analytics team

**Response**:
### Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Training data contains PII (email, purchase history) | High | Apply differential privacy, anonymize before training |
| Model makes automated decisions affecting customers | Medium | Implement human review for high-impact decisions |
| Feature importance may reveal sensitive attributes | Low | Audit feature contributions for proxy discrimination |

### Compliance Gaps
- **GDPR Art. 22**: Automated decision-making requires explicit consent and explanation.
- **EU AI Act**: Risk classification needed; likely "limited risk" category.
