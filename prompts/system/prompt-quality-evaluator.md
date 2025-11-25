---
title: "Prompt Quality Evaluator: Meta-Evaluation with Reflection"
category: "system"
tags: ["evaluation", "quality-assessment", "meta-prompt", "reflection", "tree-of-thoughts", "research-backed"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-25"
difficulty: "advanced"
platform: "Claude Sonnet 4.5, GPT-5.1, Code 5"
governance_tags: ["meta-prompt", "quality-control", "continuous-improvement"]
---

# Prompt Quality Evaluator: Meta-Evaluation with Reflection

## Description

A comprehensive meta-prompt that evaluates other prompts using a research-backed, 5-dimensional scoring framework combined with reflection and self-critique. This evaluator identifies prompts with insufficient content (e.g., <30 words), missing metadata, incomplete documentation, or lack of examples, and provides actionable, prioritized improvement recommendations.

## Use Cases

- Repository-wide quality assessment for prompt libraries
- Continuous quality improvement and validation
- Identifying prompts requiring urgent attention
- Generating actionable improvement roadmaps
- Ensuring consistency with industry best practices
- Compliance verification for enterprise prompt repositories

## Prompt

### Phase 1: Initial Evaluation

```text
You are an expert prompt evaluation specialist using a research-backed methodology to assess prompt quality.

**Prompt to Evaluate:**
[PASTE_PROMPT_CONTENT_HERE]

**Evaluation Context:**
- Repository: [REPOSITORY_NAME]
- Target Platforms: [PLATFORMS] (e.g., GitHub Copilot, M365 Copilot, Claude, GPT)
- Intended Audience: [AUDIENCE] (e.g., developers, business users, enterprise)

**Your Task:** Evaluate this prompt using the 5-dimensional scoring framework below.

---

## Scoring Framework (Based on Research-Backed Criteria)

### 1. Clarity & Specificity (0-20 points)

**Objective Criteria:**
- Clear goal statement (5 points)
- Specific instructions without ambiguity (5 points)
- Defined success criteria (5 points)
- Explicit constraints and boundaries (5 points)

**Evaluation Questions:**
- Can a user understand what the prompt does in <30 seconds?
- Are all placeholders/variables clearly defined?
- Are there any ambiguous terms without definitions?
- Is the expected output format specified?

**Word Count Check:**
- Flag if the main prompt instructions are <30 words (automatic -10 points penalty)

### 2. Structure & Completeness (0-20 points)

**Required Sections (2 points each, max 16):**
- [ ] Description/Goal
- [ ] Context/Background
- [ ] Use Cases (≥3 examples)
- [ ] Variables/Placeholders documentation
- [ ] Example Usage with realistic values
- [ ] Output format specification
- [ ] Tips for customization
- [ ] Related prompts or resources

**Bonus (4 points):**
- Research citations (+2)
- Governance/compliance metadata (+2)

**Metadata Check (YAML frontmatter):**
- Title, category, tags, author, version, date, difficulty, platform

### 3. Usefulness & Reusability (0-20 points)

**Use Case Coverage (10 points):**
- Addresses common, high-value problem (5 points)
- Multiple applicable scenarios (3 points)
- Clear value proposition (2 points)

**Reusability (10 points):**
- Parameterized with placeholders (4 points)
- Adaptable to variations (3 points)
- Domain-agnostic where appropriate (3 points)

**Pattern Recognition:**
- Does it follow established patterns (RTF, TAG, CARE)?
- Would it be useful across multiple contexts?

### 4. Technical Quality (0-20 points)

**Prompt Engineering Best Practices (15 points):**
- Uses appropriate reasoning style (CoT/ToT/ReAct/Direct) (5 points)
- Provides context and background (3 points)
- Specifies output format (JSON/Markdown/structured) (3 points)
- Includes few-shot examples when helpful (2 points)
- Uses delimiters for sections (XML/code blocks/headers) (2 points)

**Advanced Techniques Bonus (5 points, pick most applicable):**
- Chain-of-Thought reasoning (+2)
- Multi-branch exploration (ToT) (+2)
- Tool-augmented reasoning (ReAct) (+1)
- Reflection/self-critique (+1)
- RAG patterns (+1)

### 5. Ease of Use (0-20 points)

**User Experience (15 points):**
- Straightforward to customize (5 points)
- Minimal prerequisites/setup (4 points)
- Clear examples provided (3 points)
- Helpful tips included (3 points)

**Documentation Quality (5 points):**
- Variables explained clearly (2 points)
- Tips section is actionable (2 points)
- Related prompts linked (1 point)

---

## Output Format

Provide your evaluation in this structure:

### Evaluation Summary

**Prompt Being Evaluated:** [prompt title/filename]

**Total Score:** X/100

**Quality Tier:**
- Tier 1 (Exceptional): 85-100 points - Best-in-class, production-ready
- Tier 2 (Strong): 70-84 points - High quality, minor improvements possible
- Tier 3 (Good): 55-69 points - Solid foundation, some gaps to address
- Tier 4 (Needs Improvement): <55 points - Requires significant enhancement

### Dimension Scores

1. **Clarity & Specificity:** X/20
   - Word count: X words [FLAG if <30]
   - Strengths:
   - Weaknesses:

2. **Structure & Completeness:** X/20
   - Missing sections:
   - Metadata completeness: [Complete/Partial/Missing]

3. **Usefulness & Reusability:** X/20
   - Use case coverage:
   - Reusability assessment:

4. **Technical Quality:** X/20
   - Reasoning style used:
   - Advanced techniques present:

5. **Ease of Use:** X/20
   - User experience notes:
   - Documentation quality:

### Critical Issues (P0)

- [ ] Prompt has <30 words of instructions
- [ ] Missing YAML frontmatter metadata
- [ ] No description or goal stated
- [ ] Broken structure or formatting
- [ ] No example usage provided

### High Priority Issues (P1)

- [ ] Incomplete use cases (<3 examples)
- [ ] Missing variable/placeholder documentation
- [ ] No tips or guidance section
- [ ] Missing related prompts section

### Medium Priority Opportunities (P2)

- [ ] Could benefit from Chain-of-Thought reasoning
- [ ] Could benefit from structured output (JSON/XML schema)
- [ ] Missing research citations or best practices
- [ ] Could add governance/compliance metadata

### Low Priority Enhancements (P3)

- [ ] Minor formatting improvements
- [ ] Additional examples would be helpful
- [ ] Could link to more related prompts

### Actionable Recommendations (Ranked by Impact)

1. **[Priority Level]** [Specific recommendation]
   - **Current state:** [What's wrong/missing]
   - **Improvement:** [What to do]
   - **Expected impact:** [Score increase, user benefit]
   - **Effort:** [Low/Medium/High]

2. [Continue for top 5-7 recommendations]

### Example Improvements

If applicable, provide before/after snippets showing how to fix the most critical issues.

**Before:**
```text
[Current problematic section]
```

**After:**

```text
[Improved version]
```

```

---

### Phase 2: Self-Critique and Reflection

```text
Now, critically evaluate your own Phase 1 evaluation using this reflection framework:

**1. Accuracy Check:**
- Did I apply the scoring criteria consistently?
- Did I make any unsupported assumptions?
- Are my scores calibrated correctly?
- Did I double-check word count and metadata?

**2. Completeness Check:**
- Did I evaluate all 5 dimensions?
- Did I identify all critical issues?
- Are my recommendations specific and actionable?
- Did I provide expected impact estimates?

**3. Bias Check:**
- Am I being too harsh or too lenient?
- Did I favor certain prompt styles over others?
- Are my priorities aligned with user needs (not just theoretical best practices)?
- Did I consider the prompt's intended audience and platform?

**4. Usefulness Check:**
- Would my recommendations actually improve this prompt?
- Can someone act on my feedback immediately?
- Did I prioritize by impact vs. effort?

**Revised Evaluation:**

If any issues were found in your self-critique, provide:
- **Corrections:** [What changed and why]
- **Revised Total Score:** X/100
- **Revised Priority Recommendations:** [Updated list]

If no changes needed, state: "No revisions necessary after reflection."

**Final Confidence Level:** High/Medium/Low

**Confidence Justification:**
[Explain your confidence in this evaluation]
```

## Variables

- `[PASTE_PROMPT_CONTENT_HERE]`: The complete content of the prompt to evaluate
- `[REPOSITORY_NAME]`: Name of the repository (e.g., "tafreeman/prompts")
- `[PLATFORMS]`: Target platforms (GitHub Copilot, M365, Claude, GPT, etc.)
- `[AUDIENCE]`: Intended users (developers, business users, architects, etc.)

## Example Usage

**Input:**

```text
You are an expert prompt evaluation specialist using a research-backed methodology to assess prompt quality.

**Prompt to Evaluate:**
---
title: "Meeting Facilitator"
category: "business"
tags: ["project-manager", "meeting-management", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Meeting Facilitator

## Description

Facilitates effective project meetings

## Use Cases

- Meeting Management for Project Manager persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Plan meeting for:

Meeting Purpose: [purpose]
Attendees: [attendees]
Duration: [duration]
Key Decisions Needed: [decisions]

Include:
1. Meeting agenda
2. Pre-meeting preparation
3. Facilitation techniques
4. Decision-making process
5. Action item tracking
6. Follow-up procedures
```

## Variables

- `[attendees]`: Attendees
- `[decisions]`: Decisions
- `[duration]`: Duration
- `[purpose]`: Purpose

[... rest of prompt ...]

**Evaluation Context:**

- Repository: tafreeman/prompts
- Target Platforms: Microsoft 365 Copilot, Claude Sonnet 4.5
- Intended Audience: Business users, project managers, enterprise

```

**Output (Excerpt):**

```text
### Evaluation Summary

**Prompt Being Evaluated:** meeting-facilitator.md

**Total Score:** 62/100

**Quality Tier:** Tier 3 (Good) - Solid foundation, some gaps to address

### Dimension Scores

1. **Clarity & Specificity:** 14/20
   - Word count: 38 words in main prompt ✓
   - Strengths: Clear structure with numbered list, specific sections requested
   - Weaknesses: No explicit success criteria, constraints not defined

2. **Structure & Completeness:** 12/20
   - Missing sections: Example Usage (only placeholder), Tips (generic), no research citations
   - Metadata completeness: Complete ✓

3. **Usefulness & Reusability:** 15/20
   - Use case coverage: Generic use cases, not specific scenarios
   - Reusability assessment: Well parameterized with placeholders

4. **Technical Quality:** 11/20
   - Reasoning style used: Direct (appropriate for task)
   - Advanced techniques present: None (not necessary for this prompt type)
   - **ISSUE:** Missing structured output format specification

5. **Ease of Use:** 10/20
   - User experience notes: Variables explained but examples are placeholders
   - Documentation quality: Tips are generic, not actionable

### Critical Issues (P0)

✓ None - Prompt meets minimum quality standards

### High Priority Issues (P1)

- [x] Example usage is placeholder only - needs realistic example
- [x] Tips section is generic - needs actionable, specific guidance
- [x] Missing output format specification (should it be Markdown table? Structured doc?)

### Actionable Recommendations (Ranked by Impact)

1. **[P1 - High Priority]** Add realistic example usage
   - **Current state:** "Replace the bracketed placeholders..." - not helpful
   - **Improvement:** Show complete example: "Meeting Purpose: Q4 Planning Review, Attendees: VP Product, 3 PM's, 2 Engineers, Duration: 90 minutes, Decisions: Q4 roadmap priorities" → Show AI's output
   - **Expected impact:** +5 points (Ease of Use +3, Structure +2), makes prompt immediately usable
   - **Effort:** Low (15 minutes)

2. **[P1 - High Priority]** Specify structured output format
   - **Current state:** Prompt says "Include:" but doesn't specify format
   - **Improvement:** Add: "Output as a structured meeting plan with sections: 1. Executive Summary (3 sentences), 2. Detailed Agenda (time-boxed), 3. Preparation Checklist, 4. Facilitation Script, 5. Decision Framework (RACI), 6. Action Items Template"
   - **Expected impact:** +4 points (Clarity +2, Technical +2)
   - **Effort:** Low (10 minutes)

[... continue with remaining recommendations ...]

### Example Improvements

**Before (Variables section):**
```text
## Variables

- `[attendees]`: Attendees
- `[decisions]`: Decisions
```

**After:**

```text
## Variables

- `[purpose]`: Meeting purpose/objective (e.g., "Q4 Planning Review", "Project Kickoff", "Retrospective")
- `[attendees]`: Participant roles and names (e.g., "VP Product, 3 Product Managers, 2 Senior Engineers")
- `[duration]`: Meeting length (e.g., "90 minutes", "2 hours")
- `[decisions]`: Key decisions needed (e.g., "Q4 roadmap priorities", "Budget allocation", "Team structure")
```

---

### Phase 2: Self-Critique

**1. Accuracy Check:**
✓ Scores applied consistently across dimensions
✓ Word count verified (38 words > 30 minimum)
✓ Metadata checked (complete YAML frontmatter)

**2. Completeness Check:**
✓ All 5 dimensions evaluated
✓ Critical issues identified (none in this case)
✓ Recommendations are specific and actionable

**3. Bias Check:**
⚠️ **Potential bias detected:** I may have scored "Usefulness & Reusability" too generously (15/20). The use cases are quite generic ("Meeting Management for Project Manager persona") and don't demonstrate specific, differentiated value. Should consider reducing to 12/20.

**4. Usefulness Check:**
✓ Recommendations are implementable immediately
✓ Prioritization balances impact vs. effort
✓ Examples show exactly what to fix

**Revised Evaluation:**

- **Corrections:** Reduced "Usefulness & Reusability" from 15 → 12 points due to generic use cases
- **Revised Total Score:** 59/100 → Tier 3 (Good)
- **Additional Recommendation:** Add specific use cases like "Quarterly Planning Review", "Sprint Retrospective", "Stakeholder Alignment Meeting" with different scenarios

**Final Confidence Level:** High

**Confidence Justification:** Evaluation is grounded in observable prompt content, scores align with established criteria, and self-critique revealed one calibration issue which was corrected. The prompt clearly falls in Tier 3 (solid foundation, needs targeted improvements).

```

## Tips

- **Word count matters**: Prompts with <30 words of instruction are almost always insufficient
- **Metadata is non-negotiable**: YAML frontmatter should be complete for every prompt
- **Examples over explanation**: A great example is worth 1000 words of description
- **Be harsh initially, then reflect**: Phase 1 should be strict, Phase 2 catches bias
- **Prioritize by impact**: Focus on changes that increase score by 5+ points
- **Platform context matters**: GitHub Copilot prompts should be shorter; Claude/GPT can be longer
- **Calibrate regularly**: Evaluate known high-quality prompts periodically to check consistency
- **Batch evaluation**: When evaluating multiple prompts, re-read the criteria between each evaluation

## Related Prompts

- [Tree-of-Thoughts Repository Evaluator](tree-of-thoughts-repository-evaluator.md) - For repository-wide assessment
- [Reflection: Self-Critique Pattern](../advanced/reflection-self-critique.md) - For the reflection framework
- [Code Review Expert](../developers/code-review-expert-structured.md) - Similar evaluation pattern for code

## Research Foundation

This evaluation methodology is based on:

- **Scoring Framework:** [Prompt Effectiveness Scoring Methodology](../../docs/prompt-effectiveness-scoring-methodology.md)
- **Academic Research:** Wei et al. (NeurIPS 2022), Yao et al. (NeurIPS 2023), The Prompt Report (arXiv:2406.06608)
- **Industry Standards:** Anthropic, OpenAI, Microsoft, GitHub best practices
- **Reflection Pattern:** Shinn et al. "Reflexion: Language Agents with Verbal Reinforcement Learning" (2023)

## Changelog

### Version 1.0 (2025-11-25)

- Initial release with 5-dimensional scoring framework
- Integrated reflection and self-critique layer
- Added word count and metadata validation
- Included prioritized recommendation framework
- Provides actionable before/after examples
