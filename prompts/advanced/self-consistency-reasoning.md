---
title: Self-Consistency Chain-of-Thought Reasoning
shortTitle: Self-Consistency CoT
intro: Improve reasoning accuracy by sampling multiple diverse reasoning paths and selecting the most consistent answer.
type: template
difficulty: intermediate
audience: [ai-engineers, prompt-engineers, developers]
platforms: [github-copilot, chatgpt, claude, gemini]
topics: [reasoning, chain-of-thought, accuracy-improvement]
author: Based on Wang et al. (ICLR 2023)
version: 1.0
date: 2025-12-06
reviewStatus: approved
governance_tags: [research-validated, benchmark-proven]
dataClassification: public
effectivenessScore: 8.5
---

# Self-Consistency Chain-of-Thought Reasoning

## Description

Self-Consistency is an advanced prompting technique that significantly improves the accuracy of Chain-of-Thought (CoT) reasoning by generating multiple diverse reasoning paths and selecting the most consistent answer. Instead of relying on a single reasoning chain, this approach samples k different paths using temperature-controlled generation, then aggregates the final answers through majority voting.

## Use Cases

- **Arithmetic reasoning:** Math word problems (GSM8K, SVAMP, AQuA)
- **Commonsense reasoning:** Multi-step logical inference (StrategyQA)
- **Science QA:** Complex questions requiring step-by-step reasoning (ARC)
- **Any task where:** Multiple valid reasoning approaches can reach the same correct answer

**Not recommended for:** Creative writing, open-ended generation, simple classification, tasks requiring diverse outputs.

## The Prompt Template

### System Message

```

You are an expert problem solver. When given a problem, you will:

1. Read the problem carefully
2. Break it down step-by-step
3. Show your reasoning process clearly
4. State your final answer explicitly

Format your answer as: "The answer is [X]."

```

### Few-Shot Exemplars (provide 3-8 examples)

```

Q: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?
A: We start with 15 trees. Later we have 21 trees. The difference must be the number of trees they planted. So, they must have planted 21 - 15 = 6 trees. The answer is 6.

Q: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?
A: There are 3 cars in the parking lot already. 2 more arrive. Now there are 3 + 2 = 5 cars. The answer is 5.

Q: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?
A: Leah had 32 chocolates and Leah's sister had 42. That means there were originally 32 + 42 = 74 chocolates. 35 have been eaten. So in total they still have 74 - 35 = 39 chocolates. The answer is 39.

[Add 3-5 more exemplars relevant to your domain]

```

### User Query

```

Q: {{PROBLEM_STATEMENT}}
A:

```

## Implementation Parameters

| Variable | Description | Recommended Value |
| ---------- | ------------- | ------------------- |
| `k` | Number of reasoning paths to generate | 5-10 (higher for critical tasks) |
| `temperature` | Sampling temperature for diversity | 0.7-1.0 |
| `top_p` | Nucleus sampling parameter | 1.0 |
| `max_tokens` | Maximum length per reasoning path | 256-512 |
| `stop` | Stop sequence | ["The answer is", "\n\n", "Q:"] |

## Aggregation Strategy

1. **Generate k samples** using the same prompt with temperature > 0
2. **Extract final answers** from each sample (look for "The answer is X" pattern)
3. **Count answer frequencies** across all k samples
4. **Select majority answer** (most frequent)
5. **Handle ties:** Increase k or use first-generated answer as tiebreaker

## Example Input/Output

### Input

```

Q: When I was 6 my sister was half my age. Now I'm 70 how old is my sister?
A:

```

### Sample Reasoning Paths (k=5, temperature=0.7)

**Path 1:**

```

When I was 6 my sister was half my age, so she was 3. Now I am 70, so she is 70 - 3 = 67. The answer is 67.

```

**Path 2:**

```

When the narrator was 6, his sister was half his age, which is 3. Now that the narrator is 70, his sister would be 70 - 3 = 67 years old. The answer is 67.

```

**Path 3:**

```

When I was 6 my sister was half my age, so she was 3. Now I am 70, so she is 70/2 = 35. The answer is 35.

```

**Path 4:**

```

The age difference is constant. When I was 6, sister was 3, so difference = 3 years. At age 70, sister is 70 - 3 = 67. The answer is 67.

```

**Path 5:**

```

Half of 6 is 3, so sister was 3 when I was 6. The gap is 3 years and never changes. Now at 70, sister is 67. The answer is 67.

```

### Aggregation

- Answer "67" appears: 4 times
- Answer "35" appears: 1 time

### Final Output

```

The answer is 67.

```

## Performance Benchmarks

- GSM8K (math): +17.9% improvement over standard CoT
- SVAMP (math): +11.0% improvement
- AQuA (algebra): +12.2% improvement
- StrategyQA (commonsense): +6.4% improvement

## Tips for Success

1. **Quality exemplars matter:** Provide diverse reasoning styles in your few-shot examples
2. **Start with k=5:** Good balance of accuracy and cost
3. **Use consistent format:** "The answer is [X]" makes extraction easier
4. **Monitor costs:** k=10 means 10x inference calls
5. **Task selection:** Works best for problems with deterministic answers

## References

- Wang et al. (2023). "Self-Consistency Improves Chain of Thought Reasoning in Language Models." ICLR 2023.
- Prompt Engineering Guide: <https://www.promptingguide.ai/techniques/consistency>
