# Reasoning

This directory contains advanced reasoning patterns and methodologies that enhance AI model capabilities through structured thinking frameworks. These patterns help models tackle complex problems requiring multi-step reasoning, verification, and iterative refinement.

## 📁 Directory Contents

```text
reasoning/
└── chain-of-verification.md    # CoVe: Reduce hallucinations through systematic fact-checking
```

## 🧠 What is Reasoning
Reasoning patterns are structured prompt frameworks that guide AI models through complex cognitive processes. Unlike simple question-answer prompts, reasoning patterns:

- **Break down complexity**: Decompose problems into manageable steps
- **Enable verification**: Add self-checking and validation mechanisms
- **Improve accuracy**: Reduce hallucinations and errors through systematic approaches
- **Show thinking**: Make the model's reasoning process transparent
- **Support iteration**: Allow refinement and correction of initial responses

## 🔬 Chain-of-Verification (CoVe)

The primary reasoning pattern in this directory is **Chain-of-Verification**, a powerful technique for improving factual accuracy.

### Overview

**File**: [chain-of-verification.md](chain-of-verification.md)

**Purpose**: Reduce hallucinations and improve factual accuracy through a structured 4-step process:

1. **Baseline Response**: Generate initial answer
2. **Verification Planning**: Create specific verification questions
3. **Independent Verification**: Answer questions without baseline influence
4. **Final Verified Response**: Synthesize verified, accurate answer

### Use Cases

CoVe is particularly effective for:

- ✅ **Factual question answering**: Historical events, scientific facts, biographical information
- ✅ **List generation**: Ensuring completeness and accuracy
- ✅ **Knowledge-intensive content**: Reports, summaries, technical documentation
- ✅ **High-stakes information**: Medical, legal, or financial content requiring accuracy
- ✅ **Research synthesis**: Combining multiple sources accurately

### When to Use CoVe

**Use CoVe when**:

- Factual accuracy is critical
- Risk of hallucination is high
- Information needs verification
- Stakes are high (legal, medical, financial)
- Working with knowledge-intensive domains

**Don't use CoVe when**:

- Creative/subjective tasks (brainstorming, creative writing)
- Simple queries with obvious answers
- Real-time conversational responses needed
- Token efficiency is paramount

### Example Usage

```markdown
**Question:** What are the key provisions of the GDPR that apply to AI systems?
**Domain:** EU data protection law

# Model follows 4-step CoVe process:

1. Generates initial answer
2. Creates verification questions
3. Independently verifies each claim
4. Produces final verified response with corrections

```

### Model Compatibility

CoVe works well with:

- ✅ GPT-4, GPT-4o (OpenAI)
- ✅ Claude 3 Opus, Sonnet (Anthropic)
- ✅ Llama 3 70B+ (Meta)
- ✅ Gemini Pro (Google)

**Recommended**: Models with strong reasoning capabilities (70B+ parameters or frontier models).

### Variables

| Variable | Description | Required | Default |
| ---------- | ------------- | ---------- | --------- |
| `user_question` | The question requiring factual accuracy | Yes | - |
| `domain` | Optional domain context for specialized verification | No | general knowledge |

## 🔮 Future Reasoning Patterns

This directory will expand to include additional reasoning patterns:

### Planned Additions

- **Chain-of-Thought (CoT)**: Step-by-step reasoning for complex problems
- **ReAct (Reasoning + Acting)**: Combining reasoning with tool use
- **Tree-of-Thoughts (ToT)**: Multi-branch exploration with backtracking
- **Reflexion**: Self-critique and iterative improvement
- **Self-Consistency**: Multiple reasoning paths with consensus
- **Least-to-Most Prompting**: Progressive problem decomposition

### Research-Backed Techniques

All reasoning patterns are based on peer-reviewed research:

- **CoVe**: [Chain-of-Verification Reduces Hallucination](https://arxiv.org/abs/2309.11495) (Meta AI Research)
- **CoT**: [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903) (Google Research)
- **ReAct**: [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629) (Princeton/Google)
- **ToT**: [Tree of Thoughts](https://arxiv.org/abs/2305.10601) (Princeton)

## 🎯 Choosing the Right Pattern

| Task Type | Recommended Pattern | Why |
| ----------- | ------------------- | ----- |
| Factual Q&A | CoVe | Verification reduces hallucinations |
| Math/Logic | Chain-of-Thought | Step-by-step reasoning |
| Tool Use | ReAct | Combines reasoning with actions |
| Complex Problems | Tree-of-Thoughts | Explores multiple solution paths |
| Code Generation | Chain-of-Thought | Shows reasoning for better code |
| Creative Writing | None | Reasoning patterns constrain creativity |

## 📊 Performance Characteristics

### Accuracy Improvements

Based on research benchmarks:

- **CoVe**: 20-30% reduction in hallucinations on factual tasks
- **CoT**: 15-40% improvement on reasoning benchmarks
- **ReAct**: 25-50% improvement on tool-augmented tasks
- **ToT**: 30-60% improvement on complex planning problems

### Token Usage

Reasoning patterns increase token consumption:

- **CoVe**: 2-3x baseline (4-step process)
- **CoT**: 1.5-2x baseline (explicit reasoning steps)
- **ReAct**: 2-4x baseline (reasoning + tool calls)
- **ToT**: 5-10x baseline (multiple branches)

**Recommendation**: Use reasoning patterns when accuracy justifies the cost.

## 🔧 Implementation Tips

### Best Practices

1. **Clear instructions**: Specify each reasoning step explicitly
2. **Structured output**: Use XML tags or markdown sections for clarity
3. **Independent verification**: Prevent circular reasoning by isolating steps
4. **Show your work**: Make reasoning transparent for debugging
5. **Iterate carefully**: Balance thoroughness with token efficiency

### Common Pitfalls

❌ **Skipping verification**: Model may shortcut the process  
✅ **Solution**: Use explicit step markers and output validation

❌ **Circular reasoning**: Verification based on baseline  
✅ **Solution**: Isolate verification step, provide fresh context

❌ **Over-engineering**: Using complex patterns for simple tasks  
✅ **Solution**: Match pattern complexity to task difficulty

## 🧪 Testing and Validation

### Evaluating Reasoning Quality

Test reasoning patterns with:

1. **Fact-checking**: Verify claims against authoritative sources
2. **Consistency checks**: Run same query multiple times
3. **Edge cases**: Test with ambiguous or controversial topics
4. **Ablation studies**: Compare with/without reasoning pattern

### Metrics

- **Factual accuracy**: % of claims that are verifiable and correct
- **Hallucination rate**: % of claims that are fabricated
- **Reasoning coherence**: Logical consistency across steps
- **Token efficiency**: Accuracy improvement per additional token

## 🤝 Contributing

### Adding New Reasoning Patterns

1. **Research basis**: Include citations to peer-reviewed papers
2. **Clear structure**: Define each step explicitly
3. **Examples**: Provide real-world use cases
4. **Metadata**: Include YAML frontmatter with:
   - Model compatibility
   - Complexity level
   - Token estimates
   - Use cases

### Template

```markdown
---
title: Pattern Name
description: Brief description
category: reasoning
tags: [relevant, tags]
model_compatibility: [gpt-4, claude-3]
complexity: low|medium|high
estimated_tokens: range
---

# Pattern Name

[Clear explanation of the reasoning pattern]

## Steps

1. Step 1
2. Step 2

...

## Example

[Concrete example]
```

## 📚 Related Resources

- **[Advanced Prompts](../prompts/advanced/)**: Implementation of reasoning patterns
- **[Research](../docs/research/)**: Academic papers and analysis
- **[Tutorials](../docs/tutorials/)**: Step-by-step guides
- **[Tools](../tools/)**: Evaluation and testing utilities

## 📖 Further Reading

### Academic Papers

- [Chain-of-Verification Paper](https://arxiv.org/abs/2309.11495)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [LLM Reasoning Survey](https://arxiv.org/abs/2212.10403)

### Industry Resources

- [Anthropic: Claude Reasoning](https://www.anthropic.com/index/chain-of-thought-reasoning)
- [OpenAI: GPT-4 Technical Report](https://arxiv.org/abs/2303.08774)
- [Google: PaLM 2 and Reasoning](https://ai.google/discover/palm2/)

## 📄 License

All reasoning patterns are licensed under [MIT License](../LICENSE).

---

**Questions or suggestions for new patterns?** Open an issue in the [main repository](https://github.com/tafreeman/prompts).
