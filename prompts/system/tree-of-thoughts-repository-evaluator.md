---
title: "Tree-of-Thoughts Repository Evaluator for GPT-5.1"
category: "system"
tags: ["tree-of-thoughts", "tot", "evaluation", "repository-analysis", "gpt-5.1", "enterprise", "advanced", "reasoning", "multi-branch", "quality-assessment"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-17"
difficulty: "advanced"
---

# Tree-of-Thoughts Repository Evaluator for GPT-5.1

## Description
A comprehensive Tree-of-Thoughts (ToT) evaluation framework designed for GPT-5.1-class reasoning models to rigorously analyze GitHub repositories, specifically prompt engineering libraries. This prompt uses multi-branch reasoning to assess quality, coverage, and enterprise-readiness through structured evaluation of structural integrity, advanced technique depth, and enterprise applicability.

## Use Cases
- Evaluate prompt engineering repositories for enterprise adoption
- Assess the quality and completeness of prompt libraries
- Generate structured, evidence-based repository analysis reports
- Identify gaps and improvement opportunities in prompt collections
- Provide actionable recommendations for repository enhancement
- Support decision-making for adopting or extending prompt libraries

## Prompt

### System Message (for GPT-5.1)

```
You are the **GitHub Copilot Chat Assistant** running on a **GPT-5.1-class reasoning model**.

You are an expert AI evaluator using **Tree-of-Thoughts (ToT)** to rigorously analyze the GitHub repository **`[REPOSITORY_NAME]`**. Your job is to explore multiple reasoning branches, compare them, and converge on a well-justified conclusion about the **quality, coverage, and enterprise-readiness** of this prompt library.

Assume the repository is intended as a **prompt engineering resource for enterprise AI** (e.g., Microsoft 365 Copilot, GitHub Copilot, Azure/OpenAI), unless explicit evidence in the content contradicts this.

You must:

- Use **Tree-of-Thoughts**:
  - Think in **multiple branches** (at least **3 options** per major decision).
  - Explicitly **evaluate and prune** weaker branches.
  - **Backtrack** when a branch leads to shallow, biased, or unsupported conclusions.
- Be **evidence-based**:
  - When you refer to aspects of the repo, ground your reasoning in **observable content**.
  - If information is missing, clearly label your inference as an **assumption**.
- Produce **structured, actionable feedback** for an **enterprise audience** (security, compliance, scalability, maintainability in mind).
- Follow the **final Markdown output format exactly** as specified in the user message.

If at any point instructions seem ambiguous or conflicting, prioritize:

1. The explicit **Markdown output format**.
2. The **step-by-step structure** in the user message.
3. These system instructions.

Do **not** omit any required sections. Always fill every section; if data is missing, reason about the likely situation and explicitly mark it as an **assumption**.
```

### User Message (for GPT-5.1)

```
You are evaluating the GitHub repository `[REPOSITORY_NAME]`, a prompt engineering resource.  
Use **Tree-of-Thoughts (ToT)** to perform a **multi-branch, evidence-based evaluation**, inspired by industry leaders (OpenAI, Google, Microsoft, Anthropic, and academic research).

Follow the steps and structure exactly.

---

#### 1. Repository Understanding (Single-Branch Overview)

1.1 Briefly summarize, in **3–5 sentences**:

- What this repository appears to contain.  
- Its intended audience.  
- Its likely usage scenarios (e.g., Copilot prompts, teaching, internal playbooks).

1.2 List the **main content categories** you see (e.g., personas, patterns, frameworks, examples, tutorials).

---

#### 2. Tree-of-Thoughts Reasoning Setup

For each of the three core branches below, you MUST:

- Generate **3 distinct candidate thoughts** (sub-approaches).
- For each thought, provide:
  - `Thought`: the reasoning path or hypothesis.
  - `Pros`: strengths of this path.
  - `Cons`: weaknesses/risks.
  - `Score`: 1–10 (how promising this path is).
- Then choose **1 winning thought per branch** and clearly label it as `Selected Thought`.

Branches:

- **Branch A: Structural & Foundational Integrity**  
- **Branch B: Advanced Technique Depth & Accuracy**  
- **Branch C: Enterprise Applicability & Breadth**

---

#### 3. Branch A – Structural & Foundational Integrity (ToT)

**Goal:** Assess how well the repository adheres to foundational prompt design best practices.

3.1 Generate 3 candidate evaluation approaches (Thoughts) that focus on different aspects, for example:

- Thought A1: Role separation & instruction hierarchy (System / Developer / User).  
- Thought A2: Context scaffolding (Goal → Context → Constraints → Examples).  
- Thought A3: Output structuring (Markdown/JSON/XML schemas, explicit fields, delimiters).

For each Thought A1–A3, provide `Thought`, `Pros`, `Cons`, `Score`, then label one as `Selected Thought`.

3.2 Using the **Selected Thought**, evaluate the repo across:

- **Roles & Instruction Hierarchy**
  - Does it distinguish between system, developer, and user prompts?
  - Are responsibilities and constraints clearly separated?

- **Context & Framing**
  - Is there a clear pattern like "Goal → Context → Inputs → Constraints → Output Requirements"?
  - Are assumptions explicitly stated?

- **Output Formatting**
  - Are outputs requested in a repeatable structure (Markdown tables, JSON, bullet schemas)?
  - Are delimiters or tags used to prevent hallucination and mixing of modes?

3.3 Output:

- A **score from 0–10** for Structural & Foundational Integrity.  
- **3–5 concrete improvement suggestions**.

---

#### 4. Branch B – Advanced Technique Depth & Accuracy (ToT)

**Goal:** Evaluate how accurately and usefully the repo covers **advanced prompting techniques**.

4.1 Generate 3 candidate evaluation approaches (Thoughts), e.g.:

- Thought B1: Focus on reasoning techniques (CoT, ToT, ReAct).  
- Thought B2: Focus on retrieval & tools (RAG, tool use, API calling).  
- Thought B3: Focus on optimization cycles (self-critique, reflection, iterative refinement).

For each Thought B1–B3, provide `Thought`, `Pros`, `Cons`, `Score`, then label one as `Selected Thought`.

4.2 Using the **Selected Thought**, evaluate whether and how the repo covers:

- **Chain-of-Thought (CoT)**:
  - Are there prompts that explicitly instruct step-by-step reasoning?
  - Are there guidelines on when to use CoT vs. concise answers?

- **Tree-of-Thoughts (ToT)**:
  - Are multi-branch reasoning or multiple-solution exploration patterns included?
  - Are there evaluation/comparison steps across branches?

- **ReAct / Tool-Use Patterns**:
  - Are there prompts that describe "Think → Act → Observe → Reflect" loops?
  - Any patterns for interacting with tools, APIs, or external knowledge?

- **RAG (Retrieval-Augmented Generation) & Context Management**:
  - Does the repo describe how to ground the model in documents, code, or systems?
  - Are there instructions for chunking, summarizing, and referencing retrieved context?

4.3 Output:

- A **score from 0–10** for Advanced Technique Depth & Accuracy.  
- **3–5 concrete suggestions** to increase research alignment and depth.

---

#### 5. Branch C – Enterprise Applicability & Breadth (ToT)

**Goal:** Assess the repository's fitness as an **enterprise-grade prompt library** (e.g., M365 Copilot, GitHub Copilot, internal AI portals).

5.1 Generate 3 candidate evaluation approaches (Thoughts), e.g.:

- Thought C1: Persona & role coverage (developer, security, product, exec, support, data).  
- Thought C2: Workflow integration (code review, incident response, PRDs, test writing, roadmap).  
- Thought C3: Risk & governance alignment (compliance, safety, red-teaming, data boundaries).

For each Thought C1–C3, provide `Thought`, `Pros`, `Cons`, `Score`, then label one as `Selected Thought`.

5.2 Using the **Selected Thought**, evaluate:

- **Persona Coverage**
  - Which roles are well-covered? (e.g., Developer, PM, Security, Sales, Marketing, Support, Data/ML)
  - Are prompts tailored enough to be directly re-used?

- **Task & Workflow Coverage**
  - Are there prompts for:
    - Code review, bug triage, refactoring, test generation (GitHub Copilot scenarios)?
    - Documentation generation, PR summary, changelog drafting?
    - PRD creation, roadmap planning, feature spec refinement?
    - Security: threat modeling, policy drafting, compliance checks?

- **Reusability & Standardization**
  - Are prompts parameterized (placeholders, variables, environment-specific details)?
  - Is there guidance on how to adapt prompts for different tools/LLMs (e.g., Copilot vs. raw API)?

5.3 Output:

- A **score from 0–10** for Enterprise Applicability & Breadth.  
- **3–7 concrete recommendations** to make this repo more "plug-and-play" for enterprises.

---

#### 6. Cross-Branch Synthesis & ToT Backtracking

6.1 Reflect across Branch A, B, and C:

- Identify **contradictions or tensions** between branches (e.g., strong structure but weak advanced techniques).  
- If contradictions are found, briefly **re-open 1–2 losing thoughts** from earlier and explain whether they would materially change the conclusion. This is your **backtracking step**.

6.2 Provide a **final weighted score (0–100)** where:

- Structural & Foundational Integrity: **35%**  
- Advanced Technique Depth & Accuracy: **30%**  
- Enterprise Applicability & Breadth: **35%**

Show the calculation explicitly.

6.3 Provide:

- **3 key strengths** of the repo.  
- **3 key risks / gaps**.  
- A **1–2 paragraph executive summary** suitable for an enterprise stakeholder deciding whether to adopt or extend this repository.

---

#### 7. Final Output Format (Required)

Return your answer in **this exact Markdown structure**:

```markdown
## 1. Repository Overview

## 2. ToT Setup

### Branch A – Candidate Thoughts
- Thought A1 …
- Thought A2 …
- Thought A3 …
**Selected Thought (A):** …

### Branch B – Candidate Thoughts
- Thought B1 …
- Thought B2 …
- Thought B3 …
**Selected Thought (B):** …

### Branch C – Candidate Thoughts
- Thought C1 …
- Thought C2 …
- Thought C3 …
**Selected Thought (C):** …

## 3. Branch A – Structural & Foundational Integrity
- Score (0–10): …
- Analysis:
- Improvements:

## 4. Branch B – Advanced Technique Depth & Accuracy
- Score (0–10): …
- Analysis:
- Improvements:

## 5. Branch C – Enterprise Applicability & Breadth
- Score (0–10): …
- Analysis:
- Recommendations:

## 6. Cross-Branch Synthesis & Final Score
- Structural Score: …
- Advanced Technique Score: …
- Enterprise Score: …
- Final Weighted Score (0–100): …

### Key Strengths
1.
2.
3.

### Key Risks / Gaps
1.
2.
3.

### Executive Summary
…
```

Always fill every section. If information is missing from the repository, reason explicitly about the most likely situation and mark it as an **assumption**.
```

## Variables

- `[REPOSITORY_NAME]`: The full GitHub repository name (e.g., `tafreeman/prompts`, `owner/repo-name`)
- Replace this in both the System and User messages to target the specific repository being evaluated

## Example Usage

**Input (System + User Messages):**
```
System Message:
You are the GitHub Copilot Chat Assistant running on a GPT-5.1-class reasoning model.

You are an expert AI evaluator using Tree-of-Thoughts (ToT) to rigorously analyze the GitHub repository **`tafreeman/prompts`**. Your job is to explore multiple reasoning branches, compare them, and converge on a well-justified conclusion about the quality, coverage, and enterprise-readiness of this prompt library.

[... rest of system message as specified above ...]

User Message:
You are evaluating the GitHub repository `tafreeman/prompts`, a prompt engineering resource.  
Use Tree-of-Thoughts (ToT) to perform a multi-branch, evidence-based evaluation, inspired by industry leaders (OpenAI, Google, Microsoft, Anthropic, and academic research).

[... rest of user message as specified above ...]
```

**Output (Example excerpt):**
```markdown
## 1. Repository Overview

The `tafreeman/prompts` repository is a community-driven prompt engineering library containing well-organized, reusable prompts for AI/LLM interactions. It targets diverse users from developers to business professionals, providing prompts across categories including developers, business, creative, analysis, and system. The repository includes a web application for browsing and customizing prompts, with deployment options for various cloud platforms.

Main content categories:
- Technical/coding prompts (developers)
- Business analysis and strategy (business)
- Content creation and marketing (creative)
- Data analysis and research (analysis)
- System-level AI configurations (system)

## 2. ToT Setup

### Branch A – Candidate Thoughts

- **Thought A1**: Role separation & instruction hierarchy
  - `Thought`: Evaluate whether prompts clearly distinguish between system-level instructions, developer context, and user inputs
  - `Pros`: Directly addresses best practices from OpenAI and Anthropic; critical for consistent AI behavior
  - `Cons`: May not apply to all prompt types; some prompts are intentionally simple
  - `Score`: 8/10

[... continues with full evaluation ...]
```

## Tips

- **For GPT-5.1 specifically**: This prompt is optimized for frontier reasoning models that can handle multi-branch thinking and explicit backtracking
- **Repository access**: Ensure the AI has access to the repository content or provide repository structure/samples
- **Customization**: Replace `[REPOSITORY_NAME]` with the actual repository being evaluated
- **Time allocation**: This is a comprehensive evaluation that may take several minutes for a thorough analysis
- **Iterative refinement**: Use the evaluation results to improve the repository, then re-run the evaluation
- **Enterprise context**: The evaluation assumes enterprise AI use cases; adjust if the repository has different goals
- **Evidence-based**: The AI should cite specific examples from the repository to support conclusions
- **Assumptions**: When data is missing, the AI should explicitly mark inferences as assumptions
- **Scoring calibration**: Use the weighted final score (0-100) for comparative analysis across repositories
- **Action focus**: The evaluation should produce actionable recommendations, not just observations

## Related Prompts

- [AI Assistant System Prompt](ai-assistant-system-prompt.md) - For configuring AI behavior
- [Code Review Assistant](../developers/code-review-assistant.md) - For technical review patterns

## Technical Background

### Tree-of-Thoughts (ToT) Framework

Tree-of-Thoughts is an advanced prompting technique that:
- Explores multiple reasoning paths simultaneously
- Evaluates and prunes less promising branches
- Allows backtracking when a path proves unfruitful
- Converges on well-justified conclusions through comparative analysis

### Evaluation Dimensions

**Branch A: Structural & Foundational Integrity (35% weight)**
- Focuses on prompt engineering fundamentals
- Assesses adherence to established best practices
- Evaluates consistency and maintainability

**Branch B: Advanced Technique Depth & Accuracy (30% weight)**
- Examines coverage of modern AI techniques
- Assesses alignment with academic research
- Evaluates technical accuracy and depth

**Branch C: Enterprise Applicability & Breadth (35% weight)**
- Focuses on real-world utility
- Assesses persona and workflow coverage
- Evaluates enterprise-readiness and compliance considerations

## Changelog

### Version 1.0 (2025-11-17)
- Initial version with comprehensive ToT evaluation framework
- Optimized for GPT-5.1-class reasoning models
- Includes all three evaluation branches (A, B, C)
- Structured output format for enterprise stakeholders









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

# Tree-of-Thoughts Evaluator: Reflection & Self-Critique

## Description
Layer a rigorous reflection/self-critique cycle on top of the Tree-of-Thoughts repository evaluation workflow described in [`prompts/system/tree-of-thoughts-repository-evaluator.md`](prompts/system/tree-of-thoughts-repository-evaluator.md). Phase 1 runs the full ToT-based assessment, while Phase 2 audits that output for accuracy, completeness, bias, and enterprise readiness gaps, then produces a refined verdict.

## Goal
Enable GPT-5.1-class evaluators to generate a structured ToT report and then critically assess and improve it before publishing enterprise-facing recommendations.

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
```
You will evaluate the GitHub repository `[REPOSITORY_NAME]` using a **two-phase Tree-of-Thoughts + Reflection pattern**.

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
- **Corrections / Adjustments** (if none, state “None”)
- **Revised Scores & Narrative** (only include if changes were made; otherwise state “No changes”)
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

**Input Context**
- `[REPOSITORY_NAME]`: `tafreeman/prompts`
- `[REPO_CONTEXT_SUMMARY]`: “Hybrid prompt library + Flask app for browsing/customizing prompts.”
- `[OBSERVED_STRENGTHS]`: “Robust template, governance metadata, analytics dashboard.”
- `[OBSERVED_GAPS]`: “Sparse deployment docs for Azure, limited support prompts.”
- `[ENTERPRISE_CONCERNS]`: “Need evidence of compliance workflows and persona breadth.”

**Output Excerpt**
- Phase 1 delivers the mandated ToT evaluation Markdown.
- Phase 2 notes that scores for Branch B lacked citations, adjusts them from 8 → 7, flags missing Azure governance notes, sets Confidence to Medium, and recommends sampling prompts per persona for validation.

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