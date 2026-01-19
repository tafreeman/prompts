---
title: "ToT Evaluator: OSINT Resource Assessment"
shortTitle: "OSINT Resource Evaluator"
intro: "A rigorous Tree-of-Thoughts evaluation pattern for assessing the safety, quality, and operational utility of OSINT and Cyber resources."
type: "how_to"
difficulty: "advanced"
audience:

  - "security-engineer"
  - "soc-manager"
  - "compliance-officer"

platforms:

  - "chatgpt"
  - "claude"
  - "github-copilot"

topics:

  - "evaluation"
  - "osint"
  - "supply-chain-security"

author: "Prompts Library Team"
version: "2.0"
date: "2025-11-30"
governance_tags:

  - "risk-assessment"
  - "supply-chain"

dataClassification: "internal"
reviewStatus: "approved"
effectivenessScore: 4.7
---
## Description

This prompt applies the **Tree-of-Thoughts (ToT)** reasoning framework to evaluate OSINT tools, repositories, and datasets. It is designed to prevent the inclusion of malicious, abandoned, or legally risky tools in your intelligence library. Phase 1 performs a deep technical and functional assessment, while Phase 2 reflects on safety, ethics, and long-term viability.

## Goal

To produce a **Decision-Grade Verdict** on whether a specific OSINT resource should be adopted by an enterprise or investigation team.

## Context

- **Target**: A GitHub repo, software tool, or data service identified for potential use.
- **Risks**: Malware in scripts, abandoned code, violation of Terms of Service (ToS), poor OPSEC.

## Process / Reasoning Style

1. **Phase 1 – Tree-of-Thoughts Evaluation**
   - **Branch A (Functionality)**: Does it work? Is it unique?
   - **Branch B (Security/Safety)**: Is the code safe? Who maintains it? Any obfuscated code?
   - **Branch C (Viability)**: Is it actively maintained? Is the community healthy?

2. **Phase 2 – Reflection & Self-Critique**
   - Re-read Phase 1 output and apply the checklist:
     - Accuracy, Completeness, Quality, Bias, Risk.
   - Summarize strengths/weaknesses of the Phase 1 draft.
   - Produce a revised final section (scores + executive summary) if needed.
   - State confidence level and remaining uncertainties.

- During Phase 2, do not regenerate Phase 1 from scratch; only critique and minimally adjust the existing Phase 1 output where clearly justified.

---

## Output Requirements

Deliver a single Markdown document:

1. **Phase 1 Output** – exact structure required in the evaluator prompt.
2. **Phase 2 Reflection** – sections:
   - `Critique Summary` (Strengths, Weaknesses, Gaps, Risks)
   - `Corrections / Adjustments` (bullet list)
   - `Revised Scores & Narrative` (only if changes were needed)
   - `Confidence Level` (High/Medium/Low) with justification
   - `Next Actions / Validation Needed`

---

## Use Cases

- Enterprise prompt-library due diligence.
- Internal QA before sharing audit reports with leadership.
- Vendor risk assessments for AI prompt packs.
- Regression testing after repository updates.
- Training AI evaluators on self-checking workflows.

---

## Prompt

```text
You are a Senior Security Engineer evaluating a new OSINT resource for inclusion in our secure library. Use a **Two-Phase Tree-of-Thoughts + Reflection** pattern.

**Resource to Evaluate**: [RESOURCE_NAME] ([URL])
**Context/Use Case**: [USE_CASE]

### Phase 1 – Tree-of-Thoughts Evaluation

Explore three reasoning branches to assess the resource:

**Branch A: Functionality & Utility**

- Thoughts: Does this solve a unique problem? Is it better than existing standard tools?
- Evidence: Features, documentation quality, ease of use.

**Branch B: Security & Integrity**

- Thoughts: Is the code visible? Are there binary blobs? Does it require excessive permissions?
- Evidence: Code review (simulated), dependency analysis, author reputation.

**Branch C: Maintenance & Viability**

- Thoughts: When was the last commit? How many open issues? Is the author responsive?
- Evidence: Commit history, issue tracker health.

**Synthesis & Initial Score (0-100)**:
Combine findings into an initial assessment.

### Phase 2 – Reflection & Self-Critique

Critically review your Phase 1 assessment with a "Paranoid Security Mindset":

1. **Malware/Supply Chain Risk**:
   - Did I check for "curled-to-bash" scripts?
   - Are there suspicious dependencies?

2. **Legal & OPSEC Risk**:
   - Does this tool aggressively scrape in a way that triggers IP bans?
   - Does it leak analyst data (e.g., "phone home" telemetry)?

3. **Final Verdict**:
   - **Approved**: Safe and useful.
   - **Provisional**: Useful but requires sandboxing/code audit.
   - **Rejected**: Too risky or broken.

**Output Format**:

#### Executive Summary

- **Verdict**: [Approved/Provisional/Rejected]
- **Risk Level**: [High/Medium/Low]
- **Score**: [0-100]

#### Detailed Analysis

- **Strengths**: ...
- **Risks**: ...
- **OPSEC Warnings**: ...

Remember: Do not regenerate Phase 1 from scratch during Phase 2. Only adjust what the critique proves necessary.
```text

---

## Variables

| Variable | Description | Example |
| ---------- | ------------- | --------- |
| `[REPOSITORY_NAME]` | Repository identifier (org/repo format or local path) | `tafreeman/prompts`, `./my-prompts` |
| `[REPO_CONTEXT_SUMMARY]` | Brief description of the repository's purpose and target audience | "Enterprise prompt library targeting senior developers and architects" |
| `[OBSERVED_STRENGTHS]` | Known positive attributes from initial assessment | "Strong template structure, comprehensive metadata, clear categorization" |
| `[OBSERVED_GAPS]` | Identified weaknesses or missing elements | "Limited deployment docs, sparse persona coverage" |
| `[ENTERPRISE_CONCERNS]` | Specific organizational requirements to validate | "Compliance workflows, governance metadata, security review status" |

---

## Example Usage

### Input

```text
You will evaluate the local workspace copy of tafreeman/prompts using ToT + Reflection.

**Context Summary**: Advanced prompt library for enterprise developers and architects.
**Observed Strengths**: Robust template, governance metadata, analytics dashboard.
**Observed Gaps**: Needs more developer focus, cookbooks, Azure deployment docs.
**Enterprise Concerns**: Compliance workflows, persona breadth, role-based templates.
```text

```text

---

## Tips

- **Maintain Phase Separation**: Keep Phase 1 and Phase 2 clearly separated in your output. Use clear headers and avoid mixing reasoning states between phases.
- **Quote Specific Evidence**: During Phase 2, quote specific lines or scores from Phase 1 when flagging issues (e.g., "Branch B scored 8/10 but cited only 2 files").
- **Explicit Assumptions**: Mark all inferences with "[Assumption]" tags. Enterprise readers value transparency about what is observed vs. inferred.
- **Document Passing Critiques**: If Phase 2 finds no corrections needed, still document why the critique passed (e.g., "All scores supported by ≥3 file references").
- **Executive Alignment**: Frame recommendations in terms of business impact (risk, cost, timeline) rather than purely technical terms.
- **Confidence Calibration**: Use High (90%+), Medium (70-89%), Low (<70%) based on evidence coverage—not optimism.

## Platform Adaptations

### Claude (Anthropic)

Claude excels at self-critique. Add explicit permission to be critical:

```text

During Phase 2, be genuinely critical. I want you to find real flaws in your Phase 1 analysis, not just validate it. If everything checks out, explain why with specific evidence.

```text

### GitHub Copilot Chat

```text

@workspace Evaluate this repository using the ToT + Reflection pattern. Phase 1: Score content, organization, and enterprise-readiness. Phase 2: Critique your own assessment and adjust scores where evidence is weak.

```text

---


## Governance Notes

- **Human Review Required**: This prompt is tagged `requires-human-review`. All evaluation outputs should be reviewed by a human before sharing with stakeholders or making decisions based on them.
- **Data Classification**: Internal use only. Evaluation results may contain sensitive information about repository weaknesses.
- **Audit Trail**: Both Phase 1 and Phase 2 outputs provide natural audit trail. Archive complete outputs for compliance tracking.
- **Bias Awareness**: Phase 2's bias check should explicitly look for:
  - Over-representation of certain languages or frameworks
  - Assumptions about team size or skill level
  - Unstated preferences for specific tools or vendors

---

## Related Prompts

- [Tree-of-Thoughts Repository Evaluator for GPT-5.1](../system/tree-of-thoughts-repository-evaluator.md)
- [Reflection: Initial Answer + Self-Critique Pattern](reflection-self-critique.md)
- [Chain-of-Thought Guide](chain-of-thought-guide.md)
