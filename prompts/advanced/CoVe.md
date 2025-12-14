---
title: Chain-of-Verification (CoVe)
description: "Reduce hallucinations through structured fact-checking using the Generate\u2192\
  Verify\u2192Revise cycle"
category: reasoning
tags:
- hallucination-reduction
- factual-accuracy
- self-critique
- verification
- qa
author: Research Team
version: 1.0.0
model_compatibility:
- gpt-4
- gpt-4o
- claude-3
- llama-3
- gemini
variables:
- name: user_question
  description: The user's original question requiring a factually accurate answer
  required: true
- name: domain
  description: Optional domain context for specialized verification
  required: false
  default: general knowledge
use_cases:
- Factual question answering
- Biography and profile generation
- List generation tasks
- Knowledge-intensive content creation
- Report writing requiring accuracy
- Medical/legal/technical information
complexity: medium
estimated_tokens: 800-1500
shortTitle: CoVe Verification
intro: Chain-of-Verification pattern for self-verifying LLM outputs through structured decomposition.
type: reference
difficulty: advanced
audience:
- developers
platforms:
- github-copilot
topics:
- general
date: '2025-12-13'
reviewStatus: draft
governance_tags: []
dataClassification: []
effectivenessScore: 0.0
---

# Chain-of-Verification (CoVe) Prompting Pattern
You are a factual accuracy assistant that reduces hallucinations through systematic verification. You will answer questions using a 4-step Chain-of-Verification process.

## Description

Use the **Generate → Verify → Revise** loop to reduce hallucinations by decomposing an answer into verifiable claims, independently checking each claim, and then producing a corrected final response.
## Your Task
Answer the following question with verified accuracy:
**Question:** {{user_question}}
**Domain:** {{domain}}
---
## STEP 1: BASELINE RESPONSE
Generate your initial answer to the question. Do not verify yet—provide your best complete answer.
<baseline_response>
[Your initial answer here]
</baseline_response>
---
## STEP 2: VERIFICATION PLANNING
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
---
## STEP 3: VERIFICATION EXECUTION
**CRITICAL:** Answer each question INDEPENDENTLY. Do NOT reference your baseline response. Treat each as a completely fresh query.
<verified_answers>
**Q1:** [Question]
**A1:** [Your independent answer—ignore what you said in the baseline]
**Q2:** [Question]
**A2:** [Your independent answer]
[Continue for all questions...]
</verified_answers>
---
## STEP 4: FINAL VERIFIED RESPONSE
Synthesize a final response using ONLY:
- The original question
- Your verified answers from Step 3
Do NOT copy from your baseline response. Correct any claims that were wrong. Incorporate all verified facts.
<final_response>
[Your corrected, verified answer]
</final_response>
---
## VERIFICATION SUMMARY
| Claim from Baseline | Verification Result | Correction (if needed) |
|---------------------|---------------------|------------------------|
| [Claim 1] | ✓ Verified / ✗ Incorrect | [Correct information] |
| [Claim 2] | ✓ Verified / ✗ Incorrect | [Correct information] |
**Confidence Level:** [High/Medium/Low based on verification results]
---
## Example

### Verifying Prompt Evaluation Claims
This example demonstrates CoVe applied to a real prompt library task: **verifying the accuracy of claims made during a prompt quality evaluation**.
### Scenario
You've used the `prompt-quality-evaluator.md` to assess a prompt and received this evaluation:
> "The `api-documentation-generator.md` prompt scores 72/100 (Tier 2). It uses the ReAct pattern with 4 reasoning steps, includes 5 use cases, has complete YAML frontmatter, and was last updated in October 2024. The main weakness is that it lacks few-shot examples."
Before acting on this evaluation, you want to verify its claims.
---
### STEP 1: BASELINE RESPONSE
**Question:** "Is this evaluation of `api-documentation-generator.md` accurate?"
<baseline_response>
The evaluation appears accurate. The prompt scores 72/100 (Tier 2). It uses ReAct for structured reasoning, includes 5 use cases, has complete YAML frontmatter, and was updated October 2024. The criticism about lacking few-shot examples is valid.
</baseline_response>
---
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
---
### STEP 3: VERIFICATION EXECUTION
<verified_answers>
**Q1:** Does it use the ReAct pattern?
**A1:** The prompt uses **Chain-of-Thought (CoT)**, not ReAct. ReAct requires Thought→Action→Observation cycles with tool calls. This prompt has sequential steps but no action/observation structure. **INCORRECT.**
**Q2:** Does it have 4 reasoning steps?
**A2:** The prompt has 6 steps: (1) Analyze code, (2) Extract endpoints, (3) Document parameters, (4) Generate examples, (5) Format output, (6) Validate. **INCORRECT—6 steps, not 4.**
**Q3:** Are there 5 use cases?
**A3:** Counting: (1) REST API docs, (2) GraphQL docs, (3) SDK docs, (4) Internal API reference. **INCORRECT—4 use cases, not 5.**
**Q4:** Is YAML frontmatter complete?
**A4:** Checking: title ✓, category ✓, tags ✓, author ✓, version ✓, date ✓, difficulty ✓, platform ✓. **CORRECT.**
**Q5:** Was it last updated October 2024?
**A5:** The `date` field shows `2024-09-15`. **INCORRECT—September 2024, not October.**
**Q6:** Does it lack few-shot examples?
**A6:** The "Example Usage" section has placeholder text only. **CORRECT—lacks real examples.**
**Q7:** Would 72/100 be accurate?
**A7:** Recalculating: Clarity 16/20, Structure 14/20, Usefulness 14/20, Technical 12/20, Ease of Use 12/20. **Revised: 68/100 (Tier 3), not 72 (Tier 2).**
</verified_answers>
---
### STEP 4: FINAL VERIFIED RESPONSE
<final_response>
The evaluation contains **5 factual errors**:
| Original Claim | Verified Fact | Status |
|----------------|---------------|--------|
| Uses ReAct pattern | Uses Chain-of-Thought | ✗ |
| Has 4 reasoning steps | Has 6 steps | ✗ |
| Includes 5 use cases | Has 4 use cases | ✗ |
| Updated October 2024 | Updated September 2024 | ✗ |
| Score: 72/100 (Tier 2) | Should be ~68/100 (Tier 3) | ✗ |
| Complete YAML frontmatter | Complete | ✓ |
| Lacks few-shot examples | No real examples | ✓ |
**Corrected:** The prompt scores **68/100 (Tier 3)**, uses CoT (not ReAct) with 6 steps, has 4 use cases, and was updated September 2024.
</final_response>
---
### Why This Example Matters for Prompt Library Work
CoVe is valuable when:
1. **Evaluating prompts** - Verify scoring claims before prioritizing improvements
2. **Auditing the repository** - Fact-check batch evaluation reports
3. **Reviewing PRs** - Verify claims about new or modified prompts
4. **Comparing techniques** - Ensure descriptions are accurate ("uses ToT" - does it?)
5. **Documentation accuracy** - Verify descriptions match actual behavior
