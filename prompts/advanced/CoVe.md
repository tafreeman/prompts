---
name: Chain-of-Verification (CoVe)
description: Reduce hallucinations through structured fact-checking using the Generate→Verify→Revise cycle - claude-3 - llama-3 - gemini
type: how_to
pattern: cove
difficulty: advanced
model: openai/gpt-4o
response_format: text
---

# Chain-of-Verification (CoVe) Prompting Pattern

## Description

Use the **Generate → Verify → Revise** loop to reduce hallucinations by decomposing an answer into verifiable claims, independently checking each claim, and then producing a corrected final response.

## Prompt

You are a factual accuracy assistant that reduces hallucinations through systematic verification. You will answer questions using a 4-step Chain-of-Verification process.

### Step 1: Baseline Generation
Answer the following question with verified accuracy:
**Question:** {{user_question}}
**Domain:** {{domain}}

### Step 2: Verification Planning

Analyze your baseline response and generate verification questions for each factual claim.
**Guidelines for verification questions:**

- One question per distinct factual claim
- Use the 5W framework: Who, What, When, Where, Why
- Make each question independently answerable
- Target verifiable facts, not opinions
- Be specific, not generic

  <verification_questions>

1. [Question for claim 1]
2. [Question for claim 2]
3. [Continue for all factual claims in your response]

   </verification_questions>

### Step 3: Verification Execution

Answer each verification question independently.

### Step 4: Final Revision

Produce a final, corrected response based on the verification results.

## Variables

- `{{user_question}}`: The question to answer.
- `{{domain}}`: The domain of the question (e.g. History, Science).

## Example

**Question**: Who is the CEO of Twitter?
**Domain**: Logic

### Step 1: Baseline Generation
Elon Musk is the CEO of Twitter.

### Step 2: Verification Planning
1. Is Elon Musk the current CEO of Twitter?

### Step 3: Verification Execution
1. No, Linda Yaccarino is the current CEO of Twitter.

### Step 4: Final Revision
Linda Yaccarino is the CEO of Twitter.
| Claim from Baseline | Verification Result      | Correction (if needed) |
| ------------------- | ------------------------ | ---------------------- |
| [Claim 1]           | ✓ Verified / ✗ Incorrect | [Correct information]  |
| [Claim 2]           | ✓ Verified / ✗ Incorrect | [Correct information]  |

**Confidence Level:** [High/Medium/Low based on verification results]

### STEP 2: VERIFICATION PLANNING

<verification_questions>

1. Does `api-documentation-generator.md` actually use the ReAct pattern?
2. Does it have exactly 4 reasoning steps as claimed?
3. Are there exactly 5 use cases documented?
4. Is the YAML frontmatter complete?
5. Was the prompt last updated in October 2024?
6. Does the prompt lack few-shot examples?
7. Based on the scoring rubric, would 72/100 be correct?

   </verification_questions>

### STEP 4: FINAL VERIFIED RESPONSE

<final_response>

The evaluation contains **5 factual errors**:

| Original Claim | Verified Fact | Status |
| ---------------- | --------------- | -------- |
| Uses ReAct pattern | Uses Chain-of-Thought | ✗ |
| Has 4 reasoning steps | Has 6 steps | ✗ |
| Includes 5 use cases | Has 4 use cases | ✗ |
| Updated October 2024 | Updated September 2024 | ✗ |
| Score: 72/100 (Tier 2) | Should be ~68/100 (Tier 3) | ✗ |
| Complete YAML frontmatter | Complete | ✓ |
| Lacks few-shot examples | No real examples | ✓ |

**Corrected:**The prompt scores **68/100 (Tier 3)**, uses CoT (not ReAct) with 6 steps, has 4 use cases, and was updated September 2024

</final_response>

---

### Why This Example Matters for Prompt Library Work

CoVe is valuable when:

1. **Evaluating prompts** - Verify scoring claims before prioritizing improvements
2. **Auditing the repository** - Fact-check batch evaluation reports
3. **Reviewing PRs** - Verify claims about new or modified prompts
4. **Comparing techniques** - Ensure descriptions are accurate ("uses ToT" - does it?)
5. **Documentation accuracy** - Verify descriptions match actual behavior
