---
title: About Advanced Prompting Patterns
shortTitle: Advanced Patterns
intro: Understand advanced prompting techniques like Chain-of-Thought, few-shot learning,
  and agentic patterns, and when to use them.
type: conceptual
difficulty: intermediate
audience:

- senior-engineer
- solution-architect

platforms:

- github-copilot
- claude
- chatgpt
- azure-openai

topics:

- advanced-patterns
- chain-of-thought
- few-shot
- agentic

author: Deloitte AI & Engineering
version: '1.0'
date: '2025-11-29'
governance_tags:

- PII-safe

dataClassification: public
reviewStatus: approved
---

# About Advanced Prompting Patterns

## Introduction: When Basic Isn't Enough

Basic prompting—asking a direct question and receiving a direct answer—works well for straightforward tasks. But as your requirements grow in complexity, you'll encounter situations where simple prompts fall short:

- **Multi-step reasoning**: The model needs to work through logic, not just recall facts
- **Domain-specific tasks**: Generic responses don't meet specialized requirements
- **Consistency at scale**: You need predictable, structured outputs across many interactions
- **Complex workflows**: Tasks require planning, tool use, or iterative refinement

Advanced prompting patterns address these challenges by shaping *how* the model thinks, not just *what* it responds to. These patterns emerged from research and real-world experimentation, each solving specific categories of problems.

Understanding these patterns helps you select the right technique for your use case—and equally important, helps you avoid over-engineering simple tasks.

## Pattern Categories Overview

### Reasoning Enhancement Patterns

These patterns improve the model's ability to work through complex problems step-by-step.

#### Chain-of-Thought (CoT)

Chain-of-Thought prompting asks the model to show its reasoning process before arriving at an answer. Instead of jumping to conclusions, the model "thinks aloud," which improves accuracy on tasks requiring logic, math, or multi-step analysis.

**Why it works**: By generating intermediate steps, the model is less likely to skip crucial reasoning or make logical leaps that lead to errors.

**Best for**: Mathematical problems, logical deduction, code debugging, complex analysis

#### Tree-of-Thought (ToT)

Tree-of-Thought extends Chain-of-Thought by exploring multiple reasoning paths simultaneously. The model evaluates different approaches, backtracks from dead ends, and selects the most promising path forward.

**Why it works**: Some problems don't have a single linear solution path. ToT allows exploration and comparison of alternatives.

**Best for**: Strategic planning, creative problem-solving, optimization tasks

### Learning from Examples Patterns

These patterns leverage examples to guide model behavior without fine-tuning.

#### Zero-Shot Prompting

Zero-shot asks the model to perform a task without any examples, relying entirely on the instruction and the model's pre-trained knowledge.

**When it works**: Well-defined tasks the model has seen during training, general knowledge questions, simple classifications

#### Few-Shot Prompting

Few-shot provides 2-5 examples demonstrating the desired input-output pattern before presenting the actual task. The model learns the pattern from these examples and applies it to new inputs.

**Why it works**: Examples disambiguate intent, establish format expectations, and demonstrate edge case handling better than instructions alone.

**Best for**: Custom formats, domain-specific terminology, classification tasks, consistent styling

#### The Zero-Shot vs. Few-Shot Decision

| Factor | Favor Zero-Shot | Favor Few-Shot |
| -------- | ----------------- | ---------------- |
| Task complexity | Simple, well-defined | Nuanced, pattern-dependent |
| Output format | Flexible or standard | Specific, custom structure |
| Domain specificity | General knowledge | Specialized terminology |
| Token budget | Constrained | Available headroom |
| Consistency needs | Moderate | High |

### Role and Persona Patterns

Persona patterns assign the model a specific role, expertise level, or character that shapes its responses.

**Why it works**: Personas activate relevant knowledge domains, establish appropriate tone, and create consistent framing across interactions.

**Common personas**:

- **Expert roles**: "You are a senior security engineer..." activates security-focused reasoning
- **Audience-aware roles**: "You are explaining to a junior developer..." adjusts complexity
- **Constrained roles**: "You are a code reviewer who only comments on security issues..." focuses scope

**Best for**: Domain expertise activation, consistent voice, audience-appropriate communication

### Structured Output Patterns

These patterns ensure model outputs conform to specific formats, making them suitable for programmatic consumption.

**Techniques include**:

- **JSON/YAML specification**: Explicitly requesting structured data formats
- **Schema enforcement**: Providing a schema the output must match
- **Template filling**: Giving a template with placeholders to complete

**Why it matters**: Structured outputs enable automation, integration with other systems, and consistent downstream processing.

**Best for**: API responses, data extraction, form generation, system integration

### Agentic Patterns

Agentic patterns enable models to act autonomously, using tools and iterating toward goals.

#### ReAct (Reasoning + Acting)

ReAct interleaves reasoning traces with actions. The model thinks about what to do, takes an action (like calling a tool), observes the result, and continues reasoning based on new information.

**Pattern flow**:

1. **Thought**: Reason about the current state and what's needed
2. **Action**: Select and execute a tool or operation
3. **Observation**: Process the result
4. **Repeat**: Continue until the goal is achieved

**Why it works**: Combines the model's reasoning capabilities with external tools, grounding responses in real data and enabling complex multi-step workflows.

#### Tool-Use Patterns

Tool-use patterns define how models interact with external capabilities: APIs, databases, code execution, web search, and more.

**Key considerations**:

- **Tool selection**: When should the model use which tool?
- **Parameter formatting**: How does the model structure tool calls?
- **Error handling**: What happens when tools fail?
- **Result integration**: How are tool outputs incorporated into responses?

**Best for**: Information retrieval, calculations, code execution, system integration, real-time data access

## When to Use Advanced Patterns

Advanced patterns add value when the problem genuinely requires them. Consider these decision criteria:

### Use Advanced Patterns When

- **Accuracy matters more than speed**: CoT improves correctness but increases latency
- **Tasks require genuine reasoning**: Multi-step logic, not just information retrieval
- **Consistency is critical**: Few-shot examples enforce patterns better than instructions
- **Output must be machine-readable**: Structured output patterns ensure parseability
- **Tasks require external information**: Agentic patterns enable tool access
- **Simple prompts produce inconsistent results**: Pattern application often fixes variability

### Match Pattern to Problem Type

| Problem Type | Recommended Patterns |
| -------------- | --------------------- |
| Math/logic problems | Chain-of-Thought |
| Custom output formats | Few-shot + Structured Output |
| Domain expertise needed | Persona + Few-shot |
| Multi-step research | ReAct + Tool-use |
| Strategic decisions | Tree-of-Thought |
| Classification tasks | Few-shot |
| Code generation | Persona + CoT + Few-shot |

## When NOT to Use Advanced Patterns

The best prompt is often the simplest one that works. Avoid over-engineering:

### Keep It Simple When

- **Basic prompts work**: If zero-shot achieves your goal, don't add complexity
- **Latency is critical**: Advanced patterns increase response time
- **Token budget is tight**: Examples and reasoning steps consume tokens
- **Tasks are straightforward**: Summarization, simple Q&A, basic transformations
- **You're still exploring**: Start simple, add complexity only when needed

### The Simplicity Principle

> "Make everything as simple as possible, but not simpler."

Begin with the simplest approach:

1. **Try zero-shot first**: Clear instruction, no examples
2. **Add structure if needed**: Specify format requirements
3. **Add examples if inconsistent**: Few-shot for pattern enforcement
4. **Add reasoning if inaccurate**: CoT for complex logic
5. **Add tools if limited**: Agentic patterns for external capabilities

Each step adds power but also complexity, cost, and potential failure points.

## Pattern Combinations

Patterns often work together. Common effective combinations:

### Persona + Few-Shot + Structured Output

Combines role expertise, example-based learning, and format enforcement:

- Persona establishes domain knowledge and tone
- Examples demonstrate the specific pattern
- Structure ensures consistent, parseable output

**Use case**: Domain-specific data extraction, specialized code review

### Chain-of-Thought + Few-Shot

Shows reasoning examples, then asks for similar reasoning:

- Examples demonstrate the thinking process, not just answers
- Model learns both *what* to produce and *how* to reason

**Use case**: Complex analysis, multi-step problem solving

### ReAct + Persona + Structured Output

Agentic workflow with expertise and consistency:

- Persona shapes tool selection and interpretation
- ReAct enables iterative tool use
- Structured output ensures predictable results

**Use case**: Research agents, automated analysis pipelines

## Costs and Trade-offs

Every advanced pattern involves trade-offs:

### Token Usage

| Pattern | Token Impact |
| --------- | -------------- |
| Chain-of-Thought | +50-200% (reasoning steps) |
| Few-shot (3 examples) | +200-500 tokens per example |
| Tree-of-Thought | +300-500% (multiple paths) |
| ReAct | Variable (depends on iterations) |
| Structured Output | Minimal (+schema definition) |

### Latency

Longer prompts and longer outputs mean longer response times:

- CoT: 1.5-2x baseline latency
- ToT: 3-5x baseline latency
- Agentic: Highly variable (tool call overhead)

### Complexity

More complex prompts are harder to:

- Debug when they fail
- Maintain as requirements change
- Explain to stakeholders
- Test systematically

### When Trade-offs Are Worth It

Accept the costs when:

- Accuracy improvements justify latency increases
- Consistency requirements justify token costs
- Capability needs (tools, reasoning) justify complexity
- The alternative (manual work) is more expensive

## How It Relates to Other Concepts

Understanding advanced patterns builds on and connects to other prompting concepts:

- **[About Prompt Engineering](./about-prompt-engineering.md)**: Foundational concepts these patterns extend
- **[Prompt Effectiveness](../docs/prompt-effectiveness-scoring-methodology.md)**: How to measure pattern success
- **[Platform-Specific Templates](../docs/platform-specific-templates.md)**: How patterns adapt across models

## Next Steps

Ready to apply specific patterns? Explore detailed implementations:

### Reasoning Patterns

- [Chain-of-Thought Techniques](../techniques/README.md)
- [Tree-of-Thought Patterns](../prompts/advanced/)

### Example-Based Learning

- [Few-Shot Prompting Guide](../prompts/advanced/)
- [Zero-Shot vs. Few-Shot Selection](../guides/best-practices.md)

### Agentic Patterns

- [ReAct Pattern Implementation](../techniques/agentic/)
- [Tool-Use Patterns](../frameworks/)

### Getting Started

- [Choosing the Right Pattern](../get-started/choosing-the-right-pattern.md)
- [Platform Quickstarts](../get-started/)

---

## Summary

Advanced prompting patterns extend your capabilities beyond simple question-answer interactions. They enable complex reasoning, consistent outputs, domain expertise, and autonomous workflows.

**Key takeaways**:

- **Match pattern to problem**: Each pattern solves specific challenges
- **Start simple**: Add complexity only when simpler approaches fail
- **Understand trade-offs**: Token costs, latency, and maintenance complexity
- **Combine thoughtfully**: Patterns work together when properly integrated
- **Measure results**: Validate that advanced patterns actually improve outcomes

The goal isn't to use the most sophisticated technique—it's to use the *right* technique for each situation.
