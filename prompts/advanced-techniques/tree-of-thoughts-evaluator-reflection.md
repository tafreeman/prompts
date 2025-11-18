---
title: "Tree-of-Thoughts Evaluator: Reflection & Self-Critique"
category: "advanced-techniques"
tags: ["tree-of-thoughts", "reflection", "self-critique", "repository-evaluation", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-17"
difficulty: "advanced"
platform: "GPT-5.1-class models"
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

## Output Requirements

Deliver a single Markdown document:

1. **Phase 1 Output** – exact structure required in the evaluator prompt.
2. **Phase 2 Reflection** – sections:
   - `Critique Summary` (Strengths, Weaknesses, Gaps, Risks)
   - `Corrections / Adjustments` (bullet list)
   - `Revised Scores & Narrative` (only if changes were needed)
   - `Confidence Level` (High/Medium/Low) with justification
   - `Next Actions / Validation Needed`

## Use Cases

- Enterprise prompt-library due diligence.
- Internal QA before sharing audit reports with leadership.
- Vendor risk assessments for AI prompt packs.
- Regression testing after repository updates.
- Training AI evaluators on self-checking workflows.

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
```

## Variables

- `[REPOSITORY_NAME]`
- `[REPO_CONTEXT_SUMMARY]`
- `[OBSERVED_STRENGTHS]`
- `[OBSERVED_GAPS]`
- `[ENTERPRISE_CONCERNS]`

## Example Usage

### Input Context

- `[REPOSITORY_NAME]`: `tafreeman/prompts`
- `[REPO_CONTEXT_SUMMARY]`: "Advanced prompt library targeting enterprise developers and architects, featuring categorized prompts, with templates and additional resources."
- `[OBSERVED_STRENGTHS]`: “Robust template, governance metadata, analytics dashboard.”
- `[OBSERVED_GAPS]`: “Need to be developer and architect focused. Most of the prompts should be in that area. needs cookbooks or similar section with easy to explan examples and prompts. sparse deployment docs for Azure, limited support prompts.”
- `[ENTERPRISE_CONCERNS]`: “Need evidence of compliance workflows and persona breadth. Need adoptoption eased by sample prompts per role and simple to use templates.”

### Output Excerpt

- Phase 1 delivers the mandated ToT evaluation Markdown.
- Phase 2 notes that scores for Branch B lacked citations, adjusts them from 8 → 7, flags missing Azure governance notes, sets Confidence to Medium, and recommends sampling prompts per persona for validation.
- Phase 1 remains as initially generated; Phase 2 only annotates and minimally adjusts scores/narratives where explicitly justified.

## Tips

- Keep Phase 1 and Phase 2 clearly separated to avoid mixing reasoning states.
- During Phase 2, quote specific lines from Phase 1 when flagging issues.
- Treat assumptions explicitly—enterprise readers value transparency.
- If no corrections are needed, still document why the critique passed.
- Use the reflection step to align recommendations with executive decision needs.

## Related Prompts

- [Tree-of-Thoughts Repository Evaluator for GPT-5.1](../system/tree-of-thoughts-repository-evaluator.md)
- [Reflection: Initial Answer + Self-Critique Pattern](reflection-self-critique.md)
- [Chain-of-Thought Guide](chain-of-thought-guide.md)

## Changelog

### Version 1.0 (2025-11-17)

- Initial release combining ToT evaluation with mandatory reflection cycle.
- Adds enterprise-focused critique criteria and confidence calibration.
