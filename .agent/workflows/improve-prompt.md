---
description: Improve a prompt using the quality evaluator and validator tools
---

1. Ask the user which prompt file they want to improve.
2. **Compliance Check**: Run the validator tool to get a baseline structural score:
   `python tools/validators/prompt_validator.py [file_path]`
3. **Quality Check**: Read the `prompts/system/prompt-quality-evaluator.md` system prompt and `tools/rubrics/quality_standards.json` to understand the qualitative criteria.
4. Read the target prompt file content.
5. **Hybrid Evaluation**: Evaluate the prompt by combining:
   - The validator's structural report (missing sections, metadata).
   - Your qualitative assessment against the rubric (clarity, tone, realism of examples).
6. Present a comprehensive evaluation report and prioritized improvement plan to the user.
7. Ask the user for approval to apply the fixes.
8. Apply the fixes (using `replace_file_content` or `multi_replace_file_content`).
9. **Verification**: Re-run the validator tool to verify the score improvement.
   `python tools/validators/prompt_validator.py [file_path]`
