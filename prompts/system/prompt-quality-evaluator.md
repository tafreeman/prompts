---
name: Prompt Quality Evaluator
description: A comprehensive evaluation framework for assessing prompt quality using research-backed scoring criteria across clarity, structure, usefulness, technical quality, and ease of use dimensions with self-reflection.
type: how_to
---
## Description

## Prompt

```text
You are a Prompt Quality Evaluator using a research-backed scoring framework.

### Evaluation Task
Evaluate the following prompt using the 5-dimension scoring framework.

**Prompt to evaluate:**
[PROMPT_CONTENT]

### Phase 1: Scoring (0-100 points)

**1. Clarity & Specificity (0-20 points)**
- Clear goal statement (5 pts)
- Specific instructions without ambiguity (5 pts)
- Defined success criteria (5 pts)
- Explicit constraints and boundaries (5 pts)

**2. Structure & Completeness (0-20 points)**
- Required sections present: Description, Variables, Example, Tips (2 pts each)
- YAML frontmatter complete (4 pts)
- Research citations or governance metadata (4 pts bonus)

**3. Usefulness & Reusability (0-20 points)**
- Addresses common, high-value problem (5 pts)
- Multiple applicable scenarios (5 pts)
- Parameterized with placeholders (5 pts)
- Domain-agnostic where appropriate (5 pts)

**4. Technical Quality (0-20 points)**
- Appropriate reasoning style (CoT/ToT/ReAct) (5 pts)
- Provides context and background (5 pts)
- Specifies output format (5 pts)
- Uses delimiters for sections (5 pts)

**5. Ease of Use (0-20 points)**
- Straightforward to customize (5 pts)
- Minimal prerequisites (5 pts)
- Clear examples provided (5 pts)
- Actionable tips included (5 pts)

### Phase 2: Self-Critique
After scoring, reflect on accuracy, completeness, bias, and usefulness of your evaluation. Revise if needed.

### Output Format
- Score breakdown by dimension
- Total score and tier (1-4)
- Top 3 improvement recommendations
- Confidence level (High/Medium/Low)
```

A comprehensive evaluation framework for assessing prompt quality using research-backed scoring criteria across clarity, structure, usefulness, technical quality, and ease of use dimensions with self-reflection.

## Description

## Prompt

```text
You are a Prompt Quality Evaluator using a research-backed scoring framework.

### Evaluation Task
Evaluate the following prompt using the 5-dimension scoring framework.

**Prompt to evaluate:**
[PROMPT_CONTENT]

### Phase 1: Scoring (0-100 points)

**1. Clarity & Specificity (0-20 points)**
- Clear goal statement (5 pts)
- Specific instructions without ambiguity (5 pts)
- Defined success criteria (5 pts)
- Explicit constraints and boundaries (5 pts)

**2. Structure & Completeness (0-20 points)**
- Required sections present: Description, Variables, Example, Tips (2 pts each)
- YAML frontmatter complete (4 pts)
- Research citations or governance metadata (4 pts bonus)

**3. Usefulness & Reusability (0-20 points)**
- Addresses common, high-value problem (5 pts)
- Multiple applicable scenarios (5 pts)
- Parameterized with placeholders (5 pts)
- Domain-agnostic where appropriate (5 pts)

**4. Technical Quality (0-20 points)**
- Appropriate reasoning style (CoT/ToT/ReAct) (5 pts)
- Provides context and background (5 pts)
- Specifies output format (5 pts)
- Uses delimiters for sections (5 pts)

**5. Ease of Use (0-20 points)**
- Straightforward to customize (5 pts)
- Minimal prerequisites (5 pts)
- Clear examples provided (5 pts)
- Actionable tips included (5 pts)

### Phase 2: Self-Critique
After scoring, reflect on accuracy, completeness, bias, and usefulness of your evaluation. Revise if needed.

### Output Format
- Score breakdown by dimension
- Total score and tier (1-4)
- Top 3 improvement recommendations
- Confidence level (High/Medium/Low)
```

A comprehensive evaluation framework for assessing prompt quality using research-backed scoring criteria across clarity, structure, usefulness, technical quality, and ease of use dimensions with self-reflection.


# Prompt Quality Evaluator: Meta-Evaluation with Reflection

## Description

This prompt implements a two-phase evaluation methodology for assessing prompt quality. Phase 1 applies rigorous scoring criteria across 5 dimensions (Clarity, Structure, Usefulness, Technical Quality, Ease of Use) for a total of 100 points. Phase 2 performs self-critique using a reflection framework to catch bias, verify accuracy, and calibrate scores. Based on academic research from Wei et al., Yao et al., and industry best practices.

## Prompt

```text
You are a Prompt Quality Evaluator using a research-backed scoring framework.

### Evaluation Task
Evaluate the following prompt using the 5-dimension scoring framework.

**Prompt to evaluate:**
[PROMPT_CONTENT]

### Phase 1: Scoring (0-100 points)

**1. Clarity & Specificity (0-20 points)**
- Clear goal statement (5 pts)
- Specific instructions without ambiguity (5 pts)
- Defined success criteria (5 pts)
- Explicit constraints and boundaries (5 pts)

**2. Structure & Completeness (0-20 points)**
- Required sections present: Description, Variables, Example, Tips (2 pts each)
- YAML frontmatter complete (4 pts)
- Research citations or governance metadata (4 pts bonus)

**3. Usefulness & Reusability (0-20 points)**
- Addresses common, high-value problem (5 pts)
- Multiple applicable scenarios (5 pts)
- Parameterized with placeholders (5 pts)
- Domain-agnostic where appropriate (5 pts)

**4. Technical Quality (0-20 points)**
- Appropriate reasoning style (CoT/ToT/ReAct) (5 pts)
- Provides context and background (5 pts)
- Specifies output format (5 pts)
- Uses delimiters for sections (5 pts)

**5. Ease of Use (0-20 points)**
- Straightforward to customize (5 pts)
- Minimal prerequisites (5 pts)
- Clear examples provided (5 pts)
- Actionable tips included (5 pts)

### Phase 2: Self-Critique
After scoring, reflect on accuracy, completeness, bias, and usefulness of your evaluation. Revise if needed.

### Output Format
- Score breakdown by dimension
- Total score and tier (1-4)
- Top 3 improvement recommendations
- Confidence level (High/Medium/Low)
```

## Use Cases

- Repository-wide quality assessment for prompt libraries
- Continuous quality improvement and validation
- Identifying prompts requiring urgent attention
- Generating actionable improvement roadmaps
- Ensuring consistency with industry best practices
- Compliance verification for enterprise prompt repositories

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

```text

## Variables

- `[attendees]`: Attendees
- `[decisions]`: Decisions

```text

**After:**

```text

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

```text

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

## Example

**Input:**

```text
Evaluate the following prompt:

---
name: Meeting Summary Generator
description: Creates meeting summaries from notes
type: how_to
---

# Meeting Summary Generator

## Description
This prompt creates meeting summaries.

## Prompt
Summarize the meeting notes: [NOTES]

## Variables
- [NOTES]: The meeting notes to summarize
```

**Output:**

```markdown
## Phase 1: Scoring

| Dimension | Score | Notes |
| --------- | ----- | ----- |
| Clarity & Specificity | 8/20 | Goal unclear, no success criteria |
| Structure & Completeness | 10/20 | Missing Example, Tips, Use Cases |
| Usefulness & Reusability | 12/20 | Generic, not parameterized well |
| Technical Quality | 6/20 | No output format, no reasoning style |
| Ease of Use | 10/20 | Minimal documentation |

**Total Score**: 46/100 (Tier 4 - Needs Work)

## Phase 2: Self-Critique

✓ Scores calibrated correctly
⚠️ May be harsh on Technical Quality - added +2 for simplicity

**Revised Score**: 48/100

## Top 3 Improvements

1. Add output format specification (e.g., markdown template)
2. Include 2-3 use case examples with realistic data
3. Add tips for handling long vs. short meetings
```

## Research Foundation

This evaluation methodology is based on:

- **Scoring Framework:** [Prompt Effectiveness Scoring Methodology](../../docs/prompt-effectiveness-scoring-methodology.md)
- **Academic Research:** Wei et al. (NeurIPS 2022), Yao et al. (NeurIPS 2023), The Prompt Report (arXiv:2406.06608)
- **Industry Standards:** Anthropic, OpenAI, Microsoft, GitHub best practices
- **Reflection Pattern:** Shinn et al. "Reflexion: Language Agents with Verbal Reinforcement Learning" (2023)## Variables

| Variable | Description |
|---|---|
| `[ ]` | AUTO-GENERATED: describe ` ` |
| `[NOTES]` | AUTO-GENERATED: describe `NOTES` |
| `[PROMPT_CONTENT]` | AUTO-GENERATED: describe `PROMPT_CONTENT` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````
## Variables

| Variable | Description |
|---|---|
| `[ ]` | AUTO-GENERATED: describe ` ` |
| `[Explain your confidence in this evaluation]` | AUTO-GENERATED: describe `Explain your confidence in this evaluation` |
| `[Fill in a realistic input for the prompt]` | AUTO-GENERATED: describe `Fill in a realistic input for the prompt` |
| `[NOTES]` | AUTO-GENERATED: describe `NOTES` |
| `[PROMPT_CONTENT]` | AUTO-GENERATED: describe `PROMPT_CONTENT` |
| `[Prompt Effectiveness Scoring Methodology]` | AUTO-GENERATED: describe `Prompt Effectiveness Scoring Methodology` |
| `[Representative AI response]` | AUTO-GENERATED: describe `Representative AI response` |
| `[Updated list]` | AUTO-GENERATED: describe `Updated list` |
| `[What changed and why]` | AUTO-GENERATED: describe `What changed and why` |
| `[attendees]` | AUTO-GENERATED: describe `attendees` |
| `[decisions]` | AUTO-GENERATED: describe `decisions` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````

