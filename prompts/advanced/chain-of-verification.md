---
name: Chain-of-Verification (CoVe)
description: Reduce hallucinations by generating a response, planning verification questions, answering them independently, and revising.
title: Chain-of-Verification (CoVe)
shortTitle: CoVe Hallucination Reducer
intro: Reduce hallucinations by generating a response, planning verification questions, answering them independently, and revising.
type: template
difficulty: advanced
audience: [ai-engineers, prompt-engineers, researchers]
platforms: [chatgpt, claude, gemini, llama-3]
topics: [hallucination-reduction, fact-checking, verification, chain-of-verification]
author: Based on Dhuliawala et al. (Meta AI, 2023)
version: 1.0
date: 2026-02-03
reviewStatus: approved
governance_tags: [research-validated, hallucination-prevention]
dataClassification: public
effectivenessScore: 9.0
---

# Chain-of-Verification (CoVe)

## Description

Chain-of-Verification (CoVe) is a prompting pattern designed to reduce hallucinations in Large Language Models. It breaks the generation process into four distinct steps: (1) Generate a baseline response, (2) Plan verification questions to check facts, (3) Execute verifications independently, and (4) Generate a final revised response. Research shows this structured approach significantly improves factual accuracy compared to standard generation or simple self-correction.

## Use Cases

- **Factual Q&A:** Answering questions about historical events, bios, or technical facts.
- **Long-form Generation:** Writing reports or articles where accuracy is critical.
- **Entity Retrieval:** extracting or listing entities with specific properties (e.g., "List politicians born in NY").
- **Reduce Hallucinations:** Any task where the model is prone to making up facts.

## The Prompt Template

(Note: CoVe is best implemented as a multi-step workflow, but can be prompted in a single complex chain for capable models.)

### Step 1: Generate Baseline (User Prompt)

```
Q: {{USER_QUERY}}
Optionally: Please generate a concise initial answer.
```

### Step 2: Plan Verifications (System/Chain Prompt)

```
Based on the initial response, identify specific facts that need verification. Generate 3-5 verification questions that would check the accuracy of these facts.

Format:
- Verification Question 1: [Question]
- Verification Question 2: [Question]
...
```

### Step 3: Execute Verifications (System/Chain Prompt)

```
Please answer the verification questions above independently. Do not rely on the initial response; answer based on your internal knowledge.

Format:
- Answer 1: [Answer]
- Answer 2: [Answer]
...
```

### Step 4: Final Verification (System/Chain Prompt)

```
Using the verified answers above, please generate a final, revised response to the original query: "{{USER_QUERY}}". Ensure all facts are consistent with the verification answers. If the initial response contained errors, correct them.
```

---

## Single-Turn Prompt Implementation (Compressed)

For environments allowing only one system prompt, use this structure:

```markdown
# System Instructions
You are a precise and factual assistant. To answer the user's query, you will follow a strict "Chain of Verification" process:

1. **Draft:** Generate a preliminary answer.
2. **Verify:** Identify specific factual claims in your draft and generate "Verification Questions" to check them.
3. **Check:** Answer these verification questions independently and strictly.
4. **Final:** Write the final, corrected answer based *only* on your verified checks.

# Output Format to Follow

## Draft
[Your initial attempt]

## Verification
- Q: [Verification Question]
- A: [Precise Answer]
- Q: [Verification Question]
- A: [Precise Answer]

## Final Answer
[Your revised, accurate response]
```

## Example Input/Output

### Input

```
Tell me about the "Mexican-American War" of 1998.
```

### Output

```markdown
## Draft
The Mexican-American War of 1998 was a brief conflict over trade disputes following the implementation of NAFTA. It resulted in the Treaty of San Antonio.

## Verification
- Q: Did a Mexican-American War occur in 1998?
- A: No, the Mexican-American War occurred from 1846 to 1848. There was no war between Mexico and the US in 1998.
- Q: What notable event happened between Mexico and US in 1998?
- A: Not a war. The US and Mexico were engaging in trade under NAFTA (signed 1992, effective 1994).
- Q: Is there a Treaty of San Antonio related to a 1998 war?
- A: No.

## Final Answer
There was no "Mexican-American War" in 1998. The actual Mexican-American War took place from 1846 to 1848. You might be confusing this with trade discussions or other diplomatic events following NAFTA, but no military conflict occurred between the two nations in 1998.
```

## Implementation Parameters

| Phase | Description | Key setting |
| ----- | ----------- | ----------- |
| Baseline | Draft generation | `temperature=1.0` (creative) |
| Verification | Fact checking | `temperature=0.0` (precise) |
| Final | Synthesis | `temperature=0.2-0.5` |

## Tips for Success

1. **Separation is Key:** Ideally, run the verification answers in a separate context or ensure the model attends to them over the draft.
2. **Short Questions:** Verification questions should be factual and "Google-able" (short, precise).
3. **Independent Answering:** The model must not just confirm its own bias ("Yes, I was right"). Prompt it to be skeptical.

## References

- Dhuliawala et al. (2023). "Chain-of-Verification Reduces Hallucination in Large Language Models." arXiv:2309.11495.
