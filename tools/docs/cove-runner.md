# CoVe Runner (`cove_runner.py`)

> **Chain-of-Verification** - Fact-checking and hallucination reduction through multi-step verification.

---

## ⚡ Quick Start

```powershell
# Verify a single question
python tools/cove_runner.py "What year was Python created?"

# Interactive mode
python tools/cove_runner.py --interactive

# With specific model
python tools/cove_runner.py "Who invented electricity?" --provider local --model phi4
```

---

## What is Chain-of-Verification?

CoVe is a multi-step approach to reduce hallucinations:

1. **Initial Response** - Get first answer from LLM
2. **Verification Questions** - Generate fact-checking questions  
3. **Independent Verification** - Answer each question independently
4. **Final Response** - Synthesize verified answer

---

## CLI Usage

```powershell
# Basic question
python tools/cove_runner.py "What year was Python created?"

# Interactive mode (continuous questioning)
python tools/cove_runner.py --interactive

# Specify provider and model
python tools/cove_runner.py "What is CRISPR?" --provider local --model phi4
python tools/cove_runner.py "Is water wet?" --provider gh --model gpt-4o-mini

# With domain context
python tools/cove_runner.py "What is CRISPR?" --domain biology
python tools/cove_runner.py "Explain quantum entanglement" --domain physics

# Verbose output (show verification steps)
python tools/cove_runner.py "When was the moon landing?" -v
```

---

## Python API

```python
from tools.cove_runner import CoVeRunner

# Initialize runner
runner = CoVeRunner(
    provider="local",
    model="phi4",
    verbose=True
)

# Run verification
result = runner.verify("What year was Python first released?")

print(f"Question: {result.question}")
print(f"Initial Answer: {result.initial_response}")
print(f"Verification Steps: {result.verification_steps}")
print(f"Final Answer: {result.final_response}")
print(f"Confidence: {result.confidence}")
```

---

## Verification Output

```
Question: What year was Python created?

Initial Response: Python was created in 1991 by Guido van Rossum.

Verification Questions:
1. Who created Python?
2. When did Guido van Rossum start working on Python?
3. What year was Python 1.0 released?

Verification Answers:
1. Guido van Rossum created Python.
2. Guido van Rossum started Python in 1989 during Christmas.
3. Python 1.0 was released in January 1994.

Final Verified Response:
Python was begun in December 1989 by Guido van Rossum, 
with version 1.0 released in January 1994. The language
was first conceived and developed starting in 1989.

Confidence: 0.92
```

---

## Best Models for CoVe

| Model | Quality | Speed | Cost |
|-------|---------|-------|------|
| `local:phi4` | Good | Fast | FREE |
| `local:mistral` | Better | Medium | FREE |
| `gh:gpt-4o-mini` | Best | Medium | FREE tier |
| `gh:gpt-4o` | Excellent | Slow | Paid |

---

## Through prompt.py CLI

```powershell
python prompt.py cove "Is Python faster than Java?"
python prompt.py cove "What causes earthquakes?" --domain geology
```

---

## See Also

- [llm-client.md](./llm-client.md) - LLM dispatcher
- [../prompteval/README.md](../prompteval/README.md) - Prompt evaluation
