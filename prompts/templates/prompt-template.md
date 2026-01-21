---
name: Prompt Title Here
description: One-sentence summary of what this prompt does.
type: template
# === Optional execution fields (uncomment as needed) ===
# pattern: react | cove | reflexion | rag    # For advanced reasoning patterns
# model: openai/gpt-4o                       # Recommended model
# model_parameters:                          # Optional model settings
#   temperature: 0.7
#   max_tokens: 2000
# response_format: text                      # text | json_object | json_schema
# difficulty: intermediate                   # beginner | intermediate | advanced
# test_data:                                 # For automated evaluation (alternative to ## Test Data section)
#   - input: { VAR1: "example" }
#     expected_contains: "success"
---

# Prompt Title Here

<!-- Score: ⭐⭐⭐ (X.X) - Update after scoring with tools/rubrics/unified-scoring.yaml -->

## Description

Provide a clear, concise description (2-3 sentences max) of what this prompt does and the problem it solves.

## Prompt

### System Prompt

```text
[Configure the AI's role, capabilities, and constraints here.
Define output format requirements and behavioral guidelines.]
```

### User Prompt

```text
[Write the user-facing prompt template here. Be specific, clear, and provide all necessary context.
Use [VARIABLE_NAME] for values users should replace.]
```

## Variables

| Variable | Description |
| ---------- | ------------- |
| `[VARIABLE_1]` | What to put here |
| `[VARIABLE_2]` | What this represents |

## Example

### Input

```text
Show a concrete example with real values filled in.
```

### Expected Output

```text
Example of what the AI would generate.
```

## Test Data (Optional)

<!-- For automated evaluation with prompteval. Use this OR test_data in frontmatter. -->
| Scenario | Input Variables | Expected Contains |
|----------|-----------------|-------------------|
| Basic case | `[VARIABLE_1]=example` | "expected phrase" |
| Edge case | `[VARIABLE_1]=edge` | "handles correctly" |

## Tips

- Tip 1: How to customize for specific needs
- Tip 2: Common pitfalls to avoid
- Tip 3: Suggestions for better results
- (Max 5 tips)

## Related Prompts

- [related-prompt-1.md](../category/related-prompt-1.md) - Brief description
- [related-prompt-2.md](../category/related-prompt-2.md) - Brief description## Related Prompts

- [Related Prompt 1](../path/to/prompt.md)
- [Related Prompt 2](../path/to/prompt.md)
- (Max 3 related prompts)

---

## Contributor Checklist

Before submitting, verify:

- [ ] `effectivenessScore` set (score with `tools/rubrics/prompt-scoring.yaml`)
- [ ] All required frontmatter fields populated
- [ ] Description is 2-3 sentences max
- [ ] Variables documented in table format
- [ ] Example has realistic input/output
- [ ] Tips are actionable (max 5)
- [ ] Related prompts are relevant (max 3)
