---
title: "Tree-of-Thoughts Evaluator: Reflection & Self-Critique"
shortTitle: "ToT Evaluator Reflection"
intro: "A rigorous reflection/self-critique cycle layered on top of Tree-of-Thoughts repository evaluation for enterprise-ready assessments."
type: "how_to"
difficulty: "advanced"
audience:
  - "senior-engineer"
  - "solution-architect"
platforms:
  - "chatgpt"
  - "claude"
  - "github-copilot"
topics:
  - "evaluation"
  - "quality"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-17"
governance_tags:
  - "requires-human-review"
dataClassification: "internal"
reviewStatus: "approved"
effectivenessScore: 4.7
---
## Description

Layer a rigorous reflection/self-critique cycle on top of the Tree-of-Thoughts repository evaluation workflow described in [`Tree-of-Thoughts Repository Evaluator for GPT-5.1`](../system/tree-of-thoughts-repository-evaluator.md). Phase 1 runs the full ToT-based assessment, while Phase 2 audits that output for accuracy, completeness, bias, and enterprise-readiness gaps, then produces a refined, leadership-ready verdict.

## Goal

Enable GPT-5.1-class (or similar) evaluators to generate a structured ToT report and then critically assess and improve it before publishing enterprise-facing, decision-grade recommendations.

## Context

- Repository: `[REPOSITORY_NAME]`, positioned as an enterprise prompt library.
- Phase 1 must follow the ToT structure (Branches A/B/C, scoring, synthesis).
- Phase 2 applies the reflection checklist to the Phase 1 draft, tightening evidence, scores, and recommendations.

## Inputs

- `[REPOSITORY_NAME]`
- `[REPO_CONTEXT_SUMMARY]`
- `[OBSERVED_STRENGTHS]`
- `[OBSERVED_GAPS]`
- `[ENTERPRISE_CONCERNS]`
- Optional artifacts: links to prompt categories, analytics screenshots, governance notes.

## Assumptions

- Evaluator can browse the repo or is provided sufficient excerpts.
- Enterprise adoption is the default target unless contradicted.
- Missing data should be flagged as assumptions rather than fabricated.

## Constraints

- Maintain the mandatory Markdown structure from the ToT evaluator.
- Cite observable evidence; label inferred points as “Assumption”.
- Scores must stay within stated ranges (0–10, 0–100 weighted).
- Keep critique constructive and actionable.

## Process / Reasoning Style

1. **Phase 1 – Tree-of-Thoughts Evaluation**
   - Run full multi-branch reasoning as defined in the evaluator prompt.
   - Document candidate thoughts, selections, analyses, and scores.

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
You will evaluate the **local workspace copy** of the repository identified as `[REPOSITORY_NAME]` using a **two-phase Tree-of-Thoughts + Reflection pattern**. Do not pull from or browse any remote repository; rely only on the files and context available in the current local workspace.

### Phase 1 – Tree-of-Thoughts Evaluation
Follow the complete instructions from `Tree-of-Thoughts Repository Evaluator for GPT-5.1` (System + User message). Produce the required Markdown sections verbatim:
- Repository Overview
- ToT Setup (Branches A/B/C with candidate thoughts and selections)
- Branch Analyses (A, B, C)
- Cross-Branch Synthesis & Final Score
- Key Strengths, Key Risks, Executive Summary

### Phase 2 – Reflection & Self-Critique
Critically review your own Phase 1 output:

1. **Accuracy Check**
   - Are all factual statements grounded in repository evidence or clearly marked as assumptions?
   - Did any scores lack justification?

2. **Completeness Check**
   - Did you cover every subsection from the instructions?
   - Were enterprise concerns `[ENTERPRISE_CONCERNS]` addressed?

3. **Quality Check**
   - Is reasoning coherent, non-redundant, and senior-executive ready?
   - Are improvement recommendations actionable?

4. **Bias & Risk Check**
   - Did you overweight certain personas or categories?
   - Are there unstated assumptions about tooling, hosting, or governance?
   - What could go wrong if stakeholders rely on this report?

5. **Confidence Assessment**
   - Assign High/Medium/Low confidence.
   - List remaining uncertainties or data you would need.

Output Phase 2 as:

#### Phase 2 – Reflection & Self-Critique
- **Critique Summary**
  - Strengths:
  - Weaknesses:
  - Gaps:
  - Risks:
- **Corrections / Adjustments** (if none, state "None")
- **Revised Scores & Narrative** (only include if changes were made; otherwise state "No changes")
- **Confidence Level**: High/Medium/Low
- **Confidence Justification**:
- **Next Actions / Validation Needed**:

Remember: Do not regenerate Phase 1 from scratch during Phase 2. Only adjust what the critique proves necessary.
<<<<<<< HEAD
```sql
=======
```text

---

>>>>>>> main
## Variables

| Variable | Description | Example |
|----------|-------------|---------|
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
<<<<<<< HEAD
=======

>>>>>>> main
### Output Excerpt

```markdown
## Phase 1 – Tree-of-Thoughts Evaluation

### Repository Overview
- Name: tafreeman/prompts
- Purpose: Enterprise prompt library
- Target Audience: Senior developers, architects

### Branch A: Content Quality Analysis
**Candidate Thoughts**:
1. Evaluate prompt clarity and specificity
2. Assess template completeness

**Selected Thought**: Evaluate prompt clarity
**Score**: 8/10 - Strong template structure

## Phase 2 – Reflection & Self-Critique

- **Critique Summary**
  - Strengths: Clear scoring methodology
  - Weaknesses: Branch B scores lacked citations
  - Gaps: Azure governance not addressed
  - Risks: Persona breadth relied on sampling

- **Corrections / Adjustments**
  - Branch B score: 8 → 7

- **Confidence Level**: Medium
- **Next Actions**: Sample prompts per persona, request Azure docs
<<<<<<< HEAD
```sql
=======
```text

---

>>>>>>> main
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
<<<<<<< HEAD
=======

>>>>>>> main
### GPT-4/GPT-5 (OpenAI)

For longer evaluations, consider using system messages to establish the two-phase pattern:

```text
System: You are an enterprise repository evaluator using Tree-of-Thoughts methodology with built-in self-reflection. Always complete Phase 1 fully before beginning Phase 2.
```text
<<<<<<< HEAD
=======

>>>>>>> main
### GitHub Copilot Chat

```text
@workspace Evaluate this repository using the ToT + Reflection pattern. Phase 1: Score content, organization, and enterprise-readiness. Phase 2: Critique your own assessment and adjust scores where evidence is weak.
```text
<<<<<<< HEAD
=======

---

>>>>>>> main
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
