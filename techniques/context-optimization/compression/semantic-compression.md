---
title: "Semantic Compression"
category: "techniques"
subcategory: "context-optimization"
technique_type: "compression"
framework_compatibility:
  openai: ">=1.0.0"
  anthropic: ">=0.8.0"
difficulty: "intermediate"
use_cases:
  - long-document-summarization
  - chat-history-management
  - token-optimization
  - cost-reduction
performance_metrics:
  compression_ratio: "40-60%"
  information_retention: "high"
  cost_reduction: "50%"
testing:
  framework: "pytest"
  coverage: "90%"
  validation_status: "passed"
governance:
  data_classification: "internal"
  risk_level: "low"
  compliance_standards: ["GDPR"]
version: "1.0.0"
author: "AI Research Team"
last_updated: "2025-11-23"
tags:
  - compression
  - summarization
  - token-optimization
  - python
---

# Semantic Compression

## Purpose

Reduce token usage while retaining essential meaning by using a smaller, faster model to summarize or "compress" text segments before passing them to a more capable (and expensive) model.

## Overview

Semantic compression replaces raw text with dense, information-rich summaries. It is particularly effective for:

1. **Chat History**: Summarizing older turns of a conversation.
2. **Reference Documents**: Distilling long articles into key facts.
3. **Logs**: Extracting relevant error patterns from verbose logs.

## Prompt

Use this prompt with a cheaper model (e.g., GPT-3.5-Turbo, Claude 3 Haiku) to compress text.

```markdown
Compress the following text to retain all key information, facts, and entities, but remove redundancy and filler words. The output should be roughly {{target_ratio}}% of the original length.

**Original Text**:
{{text}}

**Compressed Version**:
```

## Example

### Python Implementation

This example uses the `ContextOptimizer` class (see `../context_optimizer.py`) to apply semantic compression.

```python
from techniques.context_optimization.context_optimizer import ContextOptimizer

# Initialize optimizer
optimizer = ContextOptimizer()

# Long text to compress
long_text = """
The project kickoff meeting was held on Tuesday, November 23rd. 
All stakeholders were present, including the engineering lead, product manager, and design lead. 
We discussed the timeline for Q4 and agreed that the MVP must be shipped by December 15th. 
There were some concerns raised about the database schema, specifically regarding the user profile table. 
The engineering team agreed to review the schema and propose a solution by Friday.
"""

# Apply semantic compression
compressed_text = optimizer.compress_context(
    text=long_text,
    strategy="semantic",
    target_token_count=50  # Target roughly 50 tokens
)

print(f"Original Length: {len(long_text)}")
print(f"Compressed Text: {compressed_text}")
```

### Expected Output

```text
Kickoff 11/23: Stakeholders (Eng, PM, Design) present. 
Goal: MVP by 12/15. 
Issue: DB schema (user profile). 
Action: Eng to review/propose solution by Friday.
```

## Usage

### When to Use

- **Chat Applications**: Compress conversation history older than 5 turns.
- **RAG Systems**: Compress retrieved chunks that are marginally relevant.
- **Cost Sensitive Tasks**: When using GPT-4 or Claude 3 Opus, compress context first.

### When to Avoid

- **Legal/Medical Analysis**: When exact wording is critical.
- **Code Analysis**: Compression breaks syntax (use specialized code compression instead).
- **Poetry/Creative Writing**: Compression destroys style and nuance.

## Best Practices

1. **Preserve Entities**: Ensure names, dates, and IDs are never removed.
2. **Use Cheap Models**: The compressor model should be 10x cheaper than the main model to justify the extra latency.
3. **Ratio Tuning**: Aim for 50% compression. Going below 30% often results in hallucination or loss of critical context.
4. **Fallback**: If compression fails or returns empty text, fallback to the original text (truncated if necessary).
