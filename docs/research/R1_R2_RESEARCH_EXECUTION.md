# Research Execution: R1 & R2 Advanced Techniques

**Purpose:** Ready-to-execute research prompts for Self-Consistency (R1) and Chain-of-Verification (R2)  
**Created:** December 6, 2025  
**Status:** Ready to Execute

---

## How to Use This Document

### Recommended Execution Method

**Best Option: Claude (claude.ai or API)**

1. Copy the entire prompt text from the relevant section below
2. Paste into Claude's chat interface (or API call)
3. Claude will execute the full research framework and return structured findings

**Alternative: ChatGPT-4 / GPT-4o**

1. Copy the prompt text
2. Paste into ChatGPT interface
3. Results may be slightly less structured but still comprehensive

**API Execution (Python):**

```python
import anthropic

client = anthropic.Anthropic()

# Read prompt from this file or inline
prompt = """[PASTE FULL PROMPT TEXT HERE]"""

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=8000,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print(message.content[0].text)
```

---

## R1: Self-Consistency Pattern Research

### Research Objectives

- How does Self-Consistency (Wang et al., ICLR 2023) differ from simple majority voting?
- What sampling parameters are optimal?
- How to present multiple reasoning paths in a prompt template?
- When to use Self-Consistency vs single-path CoT?

### Ready-to-Execute Prompt

Copy everything between the `---START---` and `---END---` markers:

```
---START---
You are an AI research assistant conducting deep research on advanced prompt engineering techniques. You use Tree-of-Thoughts (ToT) for multi-path exploration wrapped in Reflexion for iterative quality improvement.

---

## Research Topic
Self-Consistency prompting pattern for chain-of-thought reasoning

## Research Questions

1. How does Self-Consistency (Wang et al., ICLR 2023) differ from simple majority voting? What makes the "marginalization over reasoning paths" approach more effective?
2. What sampling parameters (k samples, temperature, top-p) are optimal for different task types? What does the research say about the accuracy vs. cost tradeoff?
3. How should multiple reasoning paths be presented in a prompt template for a reusable prompt library? What structure works best?
4. When should Self-Consistency be used vs single-path Chain-of-Thought? What are the decision criteria?
5. Are there any extensions or improvements to Self-Consistency since the original 2023 paper?

## Research Depth
Deep Dive

## Time Range
2022-2025 (original paper through current implementations)

---

## Phase 1: Research Planning (ToT Branching)

Generate 3-5 distinct research paths to explore this topic comprehensively.

For each branch:

- **Branch [N]: [Research Angle]**
- **Focus:** What aspect this branch investigates
- **Key Sources to Find:** Academic papers, documentation, implementations
- **Expected Insights:** What this path should reveal
- **Priority:** High/Medium/Low based on relevance to research questions

Suggested branches to consider:

- Branch A: Original Self-Consistency paper deep dive (Wang et al. mechanism, benchmarks, theory)
- Branch B: Implementation patterns (how to structure prompts, API usage, code examples)
- Branch C: Comparison to related techniques (CoT, Self-Refine, Universal Self-Consistency)
- Branch D: Optimal parameters research (k values, temperature settings, cost analysis)
- Branch E: Recent extensions and improvements (2024-2025 papers building on Self-Consistency)

Select the top 3 branches based on priority and potential yield.

---

## Phase 2: Research Execution (ReAct Loop)

For each selected branch, execute:

### Round 1 - Initial Investigation

1. **Think:** What specific information will best answer the research questions?
2. **Act:** Describe what you're searching for or analyzing
3. **Observe:** Document findings with citations
4. **Reflect:** What's missing? Are sources authoritative and recent?

### Round 2 - Refinement (if gaps remain)

1. **Think:** Based on reflection, what angle was missed?
2. **Act:** Targeted follow-up investigation
3. **Observe:** New findings
4. **Reflect:** Is this branch now sufficiently explored?

### Capture for each branch:

- Key concepts and mechanisms discovered
- Source quality (academic paper / industry documentation / blog)
- Publication dates and citation counts where available
- Implementation examples or code repositories
- Benchmark results and performance data
- Contradictions or debates in the literature

---

## Phase 3: Cross-Branch Reflection (Reflexion)

### Self-Critique Questions:

1. Have I covered the major research directions for Self-Consistency?
2. Are my sources recent (2022-2025) and authoritative (arXiv, NeurIPS, ICLR)?
3. Did I find contradictory information requiring reconciliation?
4. What gaps remain in my understanding?
5. Am I confident enough to write a prompt template for a prompt library?

### If gaps exist:
Open 1-2 new targeted investigations to fill critical gaps.

---

## Phase 4: Synthesis & Output

Produce a structured research report with these exact sections:

### Executive Summary

- 3-4 sentence overview of Self-Consistency
- Key insight that differentiates it from simple voting
- Readiness for production use (High/Medium/Low/Experimental)

### Technique Overview Table

| Aspect | Details |
| -------- | --------- |
| **Name** | Self-Consistency |
| **Origin** | [Full citation] |
| **Core Mechanism** | [How it works in 2-3 sentences] |
| **Key Innovation** | [What makes it different from majority voting] |
| **Best Use Cases** | [When to use this] |
| **Limitations** | [Known drawbacks] |
| **Implementation Complexity** | [Low/Medium/High] |

### Detailed Findings

#### How Self-Consistency Works (Mechanism)
[Detailed explanation with citations - explain the "marginalization over reasoning paths" concept]

#### Self-Consistency vs Simple Majority Voting
[Key differences - why Self-Consistency is more than just voting]

#### Optimal Parameters
| Parameter | Recommended Value | Rationale | Source |
| ----------- | ------------------ | ----------- | -------- |
| k (samples) | | | |
| Temperature | | | |
| Top-p | | | |

#### Comparison to Related Techniques
| Technique | Similarity | Key Difference | When to Prefer |
| ----------- | ------------ | ---------------- | ---------------- |
| Single-path CoT | | | |
| Self-Refine | | | |
| Universal Self-Consistency | | | |
| Majority Voting | | | |

#### Prompt Template Structure for Library
Provide a reusable prompt template structure that can be added to a prompt library. Format as:

```text

[Provide the actual prompt template text that can be used in production]

```

Include:

- System instructions for generating diverse reasoning paths
- Format for presenting k reasoning attempts
- Instructions for answer extraction and aggregation
- Variable placeholders with descriptions

#### Benchmark Results
[Performance data from papers with proper citations - GSM8K, SVAMP, AQuA, etc.]

### Contradictions & Open Questions

- Areas where sources disagree
- Unresolved questions in the research

### Practical Recommendations

1. [When to use Self-Consistency]
2. [Optimal k and temperature for cost/accuracy balance]
3. [What to avoid]

### Full Citation List
[Academic format citations for all sources referenced]

### Artifacts for Prompt Library
Provide ready-to-use content:

1. A complete prompt template (markdown format) following this structure:
   - Title, description, use cases
   - The actual prompt text
   - Variables table
   - Example input/output

2. A Mermaid diagram showing the Self-Consistency process flow

---END---
```

---

## R2: Chain-of-Verification (CoVe) Pattern Research

### Research Objectives

- What is the Generate→Verify→Revise cycle structure?
- How does CoVe compare to Self-Refine?
- When should each technique be used?
- What are the implementation patterns?

### Ready-to-Execute Prompt

Copy everything between the `---START---` and `---END---` markers:

```
---START---
You are an AI research assistant conducting deep research on advanced prompt engineering techniques. You use Tree-of-Thoughts (ToT) for multi-path exploration wrapped in Reflexion for iterative quality improvement.

---

## Research Topic
Chain-of-Verification (CoVe) prompting pattern for reducing hallucinations and improving factual accuracy

## Research Questions

1. What is the exact structure of the Generate→Verify→Revise cycle in Chain-of-Verification? How does each phase work?
2. How does CoVe compare to Self-Refine (Madaan et al., 2023)? What are the key differences in mechanism and use cases?
3. What types of verification questions are most effective? How should they be structured?
4. When should CoVe be used vs Self-Refine vs other refinement techniques?
5. What are the benchmark results showing CoVe's effectiveness at reducing hallucinations?
6. Are there variations or extensions of CoVe (e.g., for different domains)?

## Research Depth
Deep Dive

## Time Range
2023-2025 (CoVe introduction through current implementations)

---

## Phase 1: Research Planning (ToT Branching)

Generate 3-5 distinct research paths to explore this topic comprehensively.

For each branch:

- **Branch [N]: [Research Angle]**
- **Focus:** What aspect this branch investigates
- **Key Sources to Find:** Academic papers, documentation, implementations
- **Expected Insights:** What this path should reveal
- **Priority:** High/Medium/Low based on relevance to research questions

Suggested branches to consider:

- Branch A: Original CoVe paper deep dive (Dhuliawala et al. mechanism, benchmarks, theory)
- Branch B: Generate→Verify→Revise cycle implementation (step-by-step structure, verification question design)
- Branch C: Comparison to Self-Refine and other refinement techniques
- Branch D: Hallucination reduction benchmarks and effectiveness data
- Branch E: Domain-specific applications and variations (coding, factual QA, long-form generation)

Select the top 3 branches based on priority and potential yield.

---

## Phase 2: Research Execution (ReAct Loop)

For each selected branch, execute:

### Round 1 - Initial Investigation

1. **Think:** What specific information will best answer the research questions?
2. **Act:** Describe what you're searching for or analyzing
3. **Observe:** Document findings with citations
4. **Reflect:** What's missing? Are sources authoritative and recent?

### Round 2 - Refinement (if gaps remain)

1. **Think:** Based on reflection, what angle was missed?
2. **Act:** Targeted follow-up investigation
3. **Observe:** New findings
4. **Reflect:** Is this branch now sufficiently explored?

### Capture for each branch:

- Key concepts and mechanisms discovered
- Source quality (academic paper / industry documentation / blog)
- Publication dates and citation counts where available
- Implementation examples or code repositories
- Benchmark results and performance data
- Contradictions or debates in the literature

---

## Phase 3: Cross-Branch Reflection (Reflexion)

### Self-Critique Questions:

1. Have I covered the major research directions for Chain-of-Verification?
2. Are my sources recent (2023-2025) and authoritative (arXiv, NeurIPS, EMNLP)?
3. Did I find contradictory information requiring reconciliation?
4. What gaps remain in my understanding?
5. Am I confident enough to write a prompt template for a prompt library?

### If gaps exist:
Open 1-2 new targeted investigations to fill critical gaps.

---

## Phase 4: Synthesis & Output

Produce a structured research report with these exact sections:

### Executive Summary

- 3-4 sentence overview of Chain-of-Verification
- Key insight about how verification reduces hallucinations
- Readiness for production use (High/Medium/Low/Experimental)

### Technique Overview Table

| Aspect | Details |
| -------- | --------- |
| **Name** | Chain-of-Verification (CoVe) |
| **Origin** | [Full citation - Dhuliawala et al.] |
| **Core Mechanism** | [How it works in 2-3 sentences] |
| **Key Innovation** | [What makes it effective at reducing hallucinations] |
| **Best Use Cases** | [When to use this] |
| **Limitations** | [Known drawbacks] |
| **Implementation Complexity** | [Low/Medium/High] |

### Detailed Findings

#### The Generate→Verify→Revise Cycle (Mechanism)
[Detailed explanation of each phase with citations]

**Phase 1: Generate**
[How initial response generation works]

**Phase 2: Verify**
[How verification questions are generated and answered]
[Types of verification questions]
[How to structure effective verification]

**Phase 3: Revise**
[How the final revised response is produced]
[What information from verification is used]

#### CoVe vs Self-Refine Comparison
| Aspect | Chain-of-Verification (CoVe) | Self-Refine |
| -------- | ------------------------------ | ------------- |
| **Core Approach** | | |
| **Verification Method** | | |
| **Best For** | | |
| **Limitations** | | |
| **When to Prefer** | | |

#### Comparison to Other Refinement Techniques
| Technique | Mechanism | Best Use Case | Complexity |
| ----------- | ----------- | --------------- | ------------ |
| CoVe | | | |
| Self-Refine | | | |
| Self-Consistency | | | |
| Constitutional AI | | | |

#### Verification Question Design
[How to design effective verification questions]
[Examples of good vs poor verification questions]
[Domain-specific considerations]

#### Prompt Template Structure for Library
Provide a reusable prompt template structure that can be added to a prompt library. Format as:

```text

[Provide the actual prompt template text that can be used in production]

```

Include:

- System instructions for the 3-phase process
- Format for verification question generation
- Instructions for revision based on verification
- Variable placeholders with descriptions

#### Benchmark Results
[Performance data from papers with proper citations - hallucination reduction metrics, factual accuracy improvements]

### Contradictions & Open Questions

- Areas where sources disagree
- Unresolved questions in the research
- When CoVe might not help

### Practical Recommendations

1. [When to use CoVe]
2. [How many verification questions are optimal]
3. [What types of tasks benefit most]
4. [What to avoid]

### Full Citation List
[Academic format citations for all sources referenced]

### Artifacts for Prompt Library
Provide ready-to-use content:

1. A complete prompt template (markdown format) following this structure:
   - Title, description, use cases
   - The actual prompt text (with the full Generate→Verify→Revise structure)
   - Variables table
   - Example input/output showing all three phases

2. A Mermaid diagram showing the CoVe process flow (Generate → Plan Verification → Execute Verification → Revise)

---END---
```

---

## Expected Outputs

After executing each prompt, you should receive:

### For R1 (Self-Consistency):

- [ ] Complete understanding of Self-Consistency mechanism
- [ ] Optimal parameter recommendations (k, temperature)
- [ ] Ready-to-use prompt template for the library
- [ ] Mermaid diagram of the sampling/voting process
- [ ] Clear guidance on when to use vs single-path CoT

### For R2 (Chain-of-Verification):

- [ ] Complete understanding of Generate→Verify→Revise cycle
- [ ] Comparison matrix with Self-Refine
- [ ] Ready-to-use prompt template for the library
- [ ] Mermaid diagram of the 3-phase process
- [ ] Verification question design guidance

---

## Next Steps After Research

1. **Review findings** - Validate research outputs against source papers
2. **Create library prompts** - Use the template artifacts to create:
   - `prompts/advanced/self-consistency-reasoning.md` (Task T1)
   - `prompts/advanced/chain-of-verification.md` (Future Task T11)
3. **Update improvement plan** - Mark R1 and R2 as complete in `docs/CONSOLIDATED_IMPROVEMENT_PLAN.md`
4. **Add to index** - Update `prompts/advanced/index.md` with new prompts
