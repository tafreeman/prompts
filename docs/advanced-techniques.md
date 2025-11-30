---
title: Advanced Prompting Techniques
shortTitle: Advanced Prompting Techn...
intro: A prompt for advanced prompting techniques tasks.
type: how_to
difficulty: intermediate
audience:
- senior-engineer
- junior-engineer
platforms:
- github-copilot
- claude
- chatgpt
author: Prompts Library Team
version: '1.0'
date: '2025-11-30'
governance_tags:
- PII-safe
dataClassification: internal
reviewStatus: draft
---
# Advanced Prompting Techniques

A comprehensive guide to Chain-of-Thought, ReAct, RAG, Reflection, and Tree-of-Thoughts prompting patterns.

---

## Table of Contents

1. [Overview](#overview)
2. [Chain-of-Thought (CoT)](#chain-of-thought-cot)
3. [ReAct (Reasoning + Acting)](#react-reasoning--acting)
4. [RAG (Retrieval-Augmented Generation)](#rag-retrieval-augmented-generation)
5. [Reflection & Self-Critique](#reflection--self-critique)
6. [Tree-of-Thoughts (ToT)](#tree-of-thoughts-tot)
7. [Choosing the Right Technique](#choosing-the-right-technique)
8. [Prompt Library Reference](#prompt-library-reference)

---

## Overview

Advanced prompting techniques improve AI reasoning accuracy and output quality for complex tasks. Based on research from NeurIPS, ICLR, and leading AI labs, these techniques are essential for production AI applications.

### When to Use Advanced Techniques

| Technique | Use When |
|-----------|----------|
| **Chain-of-Thought** | Problems need step-by-step reasoning |
| **ReAct** | Tasks require tool use or information gathering |
| **RAG** | Responses must be grounded in specific documents |
| **Reflection** | Quality and accuracy are paramount |
| **Tree-of-Thoughts** | Multiple solution paths need comparison |

---

## Chain-of-Thought (CoT)

Chain-of-Thought prompting asks the AI to show its reasoning step by step, significantly improving accuracy on complex problems.

### Research Background

Wei et al. (NeurIPS 2022) demonstrated that CoT prompting improves reasoning accuracy by 20-40% on arithmetic, symbolic, and commonsense reasoning tasks.

### Basic Pattern

```
Think through this problem step by step:

Step 1: [First consideration]
Step 2: [Second consideration]
Step 3: [Analysis and synthesis]
Step 4: [Conclusion]

Show your reasoning at each step.
```

### Concise Mode

For quick analysis when detailed reasoning isn't needed:

```
Analyze [PROBLEM] with brief step-by-step reasoning.
Keep each step to 1-2 sentences.
Conclude with a clear recommendation.
```

### Detailed Mode

For critical decisions requiring thorough documentation:

```
Analyze [PROBLEM] using detailed Chain-of-Thought reasoning.

For each step:
1. State the consideration
2. Evaluate relevant factors
3. Consider alternatives
4. Document your reasoning
5. State your intermediate conclusion

Provide a comprehensive final recommendation with confidence level.
```

### Use Cases

- Debugging complex issues
- Performance analysis
- Mathematical reasoning
- Strategic decision-making
- Root cause analysis

### Library Reference

- [chain-of-thought-concise.md](../prompts/advanced/chain-of-thought-concise.md)
- [chain-of-thought-detailed.md](../prompts/advanced/chain-of-thought-detailed.md)
- [chain-of-thought-debugging.md](../prompts/advanced/chain-of-thought-debugging.md)
- [chain-of-thought-performance-analysis.md](../prompts/advanced/chain-of-thought-performance-analysis.md)

---

## ReAct (Reasoning + Acting)

ReAct combines reasoning with action, enabling AI to use tools and gather information iteratively.

### Research Background

Yao et al. (ICLR 2023) and Shinn et al. introduced ReAct for tasks requiring interaction with external tools or environments.

### Basic Pattern

```
Use the ReAct pattern to solve [TASK].

**Think**: What information do I need? What tool should I use?
**Act**: [Use tool or take action]
**Observe**: [Result from action]
**Reflect**: Did this get me closer to the goal? What's next?

Repeat until the task is complete.

**Available Tools**:
- [TOOL_1]: [Description]
- [TOOL_2]: [Description]
```

### Example: Research Task

```
Research the current state of quantum computing adoption.

**Think**: I need recent information about quantum computing in enterprise settings.
**Act**: Search for "enterprise quantum computing 2024 adoption"
**Observe**: Found reports from IBM, Google, and industry analysts.
**Reflect**: I have general trends. Now I need specific use cases.

**Think**: What industries are using quantum computing?
**Act**: Search for "quantum computing use cases finance healthcare"
**Observe**: Found applications in drug discovery, portfolio optimization.
**Reflect**: Good coverage. Ready to synthesize findings.

[Continue until complete]
```

### Use Cases

- Research with multiple sources
- API integration workflows
- Multi-step data analysis
- Troubleshooting with diagnostic tools
- Automated investigation

### Library Reference

- [react-tool-augmented.md](../prompts/advanced/react-tool-augmented.md)
- [react-doc-search-synthesis.md](../prompts/advanced/react-doc-search-synthesis.md)

---

## RAG (Retrieval-Augmented Generation)

RAG grounds AI responses in specific documents or data, reducing hallucination and enabling citation.

### Core Components

1. **Document Retrieval**: Find relevant content
2. **Context Integration**: Include retrieved content in prompt
3. **Citation**: Reference sources in the response

### Basic Pattern

```
Answer the question using ONLY the provided documents.

**Documents**:
[Document 1: Title]
[Content...]

[Document 2: Title]
[Content...]

**Question**: [USER_QUESTION]

**Instructions**:
- Base your answer only on the provided documents
- Cite sources using [Doc N] format
- If information is not in documents, say so
- Quote directly when relevant
```

### Use Cases

- Internal documentation queries
- Legal document analysis
- Research report generation
- Compliance documentation
- Knowledge base Q&A

### Library Reference

- [rag-document-retrieval.md](../prompts/advanced/rag-document-retrieval.md)

---

## Reflection & Self-Critique

Reflection prompting asks the AI to evaluate and improve its own responses, leading to higher-quality outputs.

### Two-Phase Pattern

**Phase 1: Initial Response**
```
Provide your initial answer to: [QUESTION]
```

**Phase 2: Self-Critique**
```
Review your answer and identify:
1. Potential errors or inaccuracies
2. Missing information
3. Unclear explanations
4. Unsupported claims

Then provide an improved version addressing these issues.
```

### Iterative Improvement

```
Evaluate [CONTENT] using these criteria:
1. Accuracy: Are all claims verifiable?
2. Completeness: Is anything missing?
3. Clarity: Is the explanation clear?
4. Actionability: Can the reader act on this?

For each issue found:
- Describe the problem
- Explain why it matters
- Suggest a specific improvement

After evaluation, provide a revised version.
```

### Use Cases

- Critical business decisions
- High-stakes communications
- Technical documentation
- Customer-facing content
- Code review and improvement

### Library Reference

- [reflection-self-critique.md](../prompts/advanced/reflection-self-critique.md)

---

## Tree-of-Thoughts (ToT)

Tree-of-Thoughts explores multiple solution paths in parallel, evaluating trade-offs before selecting the best approach.

### Research Background

Yao et al. (NeurIPS 2023) introduced ToT for deliberate problem-solving, showing improvements on tasks requiring exploration and backtracking.

### Basic Pattern

```
Evaluate multiple approaches for [PROBLEM].

**Approach A: [Name]**
- Description: [How this approach works]
- Pros: [Benefits]
- Cons: [Drawbacks]
- Score: [1-10]

**Approach B: [Name]**
- Description: [How this approach works]
- Pros: [Benefits]
- Cons: [Drawbacks]
- Score: [1-10]

**Approach C: [Name]**
- Description: [How this approach works]
- Pros: [Benefits]
- Cons: [Drawbacks]
- Score: [1-10]

**Analysis**: Compare approaches across key dimensions.

**Recommendation**: Select the best approach and explain why.
```

### Architecture Evaluation Example

```
Evaluate architecture options for [SYSTEM].

**Option A: Monolith**
- Implementation: Single deployable unit
- Pros: Simple deployment, easier debugging
- Cons: Scaling limitations, larger blast radius
- Score: 7/10 for small teams

**Option B: Microservices**
- Implementation: Independent services
- Pros: Independent scaling, team autonomy
- Cons: Operational complexity, distributed tracing needed
- Score: 8/10 for large teams

**Option C: Serverless**
- Implementation: Function-based
- Pros: No server management, pay-per-use
- Cons: Cold starts, vendor lock-in
- Score: 7/10 for variable workloads

**Trade-off Matrix**:
| Dimension | Monolith | Microservices | Serverless |
|-----------|----------|---------------|------------|
| Complexity | Low | High | Medium |
| Scalability | Limited | Excellent | Excellent |
| Cost | Fixed | Variable | Pay-per-use |

**Recommendation**: For [CONTEXT], select [APPROACH] because [REASONING].
```

### Use Cases

- Architecture decisions
- Technology selection
- Strategic planning
- Complex problem-solving
- Trade-off analysis

### Library Reference

- [tree-of-thoughts-template.md](../prompts/advanced/tree-of-thoughts-template.md)
- [tree-of-thoughts-architecture-evaluator.md](../prompts/advanced/tree-of-thoughts-architecture-evaluator.md)
- [tree-of-thoughts-evaluator-reflection.md](../prompts/advanced/tree-of-thoughts-evaluator-reflection.md)

---

## Choosing the Right Technique

### Decision Guide

```
Is the problem straightforward?
├── Yes → Use Direct prompting
└── No → Continue...

Does it require step-by-step reasoning?
├── Yes → Use Chain-of-Thought
└── No → Continue...

Does it require external tools or data gathering?
├── Yes → Use ReAct
└── No → Continue...

Must the response be grounded in specific documents?
├── Yes → Use RAG
└── No → Continue...

Is quality paramount and worth extra processing?
├── Yes → Use Reflection
└── No → Continue...

Are there multiple approaches to compare?
├── Yes → Use Tree-of-Thoughts
└── No → Use Chain-of-Thought
```

### Technique Comparison

| Technique | Accuracy Improvement | Token Usage | Best For |
|-----------|---------------------|-------------|----------|
| Direct | Baseline | Low | Simple tasks |
| Chain-of-Thought | +20-40% | Medium | Reasoning tasks |
| ReAct | +25-35% | High | Tool-augmented tasks |
| RAG | +30-50%* | Medium | Document-grounded responses |
| Reflection | +10-20% | 2x base | Quality improvement |
| Tree-of-Thoughts | +15-30% | High | Multi-path problems |

*RAG accuracy depends heavily on retrieval quality.

### Combining Techniques

Techniques can be combined for complex tasks:

- **CoT + Reflection**: Reason step-by-step, then self-critique
- **ReAct + RAG**: Retrieve documents, then reason about them
- **ToT + Reflection**: Explore branches, then critique each one

---

## Prompt Library Reference

All advanced technique prompts are in the `prompts/advanced/` directory:

### Chain-of-Thought
- `chain-of-thought-concise.md` - Quick reasoning
- `chain-of-thought-detailed.md` - Thorough analysis
- `chain-of-thought-debugging.md` - Bug investigation
- `chain-of-thought-performance-analysis.md` - Performance profiling
- `chain-of-thought-guide.md` - When and how to use CoT

### ReAct
- `react-tool-augmented.md` - General tool use
- `react-doc-search-synthesis.md` - Document search
- `library-analysis-react.md` - Library evaluation

### RAG
- `rag-document-retrieval.md` - Document grounding

### Reflection
- `reflection-self-critique.md` - Self-improvement

### Tree-of-Thoughts
- `tree-of-thoughts-template.md` - Multi-branch template
- `tree-of-thoughts-architecture-evaluator.md` - Architecture decisions
- `tree-of-thoughts-evaluator-reflection.md` - Evaluation framework

---

## Additional Resources

### Research Papers

- Wei et al. (2022): "Chain-of-Thought Prompting" - NeurIPS
- Yao et al. (2023): "ReAct: Synergizing Reasoning and Acting" - ICLR
- Yao et al. (2023): "Tree of Thoughts" - NeurIPS
- Lewis et al. (2020): "Retrieval-Augmented Generation" - NeurIPS
- Shinn et al. (2023): "Reflexion: Language Agents with Verbal Reinforcement Learning"

### Repository Guides

- [Ultimate Prompting Guide](ultimate-prompting-guide.md) - Top 20% effective prompts
- [Best Practices](best-practices.md) - Prompt engineering fundamentals
- [Prompt Effectiveness Methodology](prompt-effectiveness-scoring-methodology.md) - Scoring system

---

*Last Updated: 2025-11-28*
