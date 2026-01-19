---
title: Generate Prompt
shortTitle: Generate Prompt
intro: Generate a high-quality prompt using the Agent (no API keys required).
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
description: Generate a high-quality prompt using the Agent (no API keys required)
---

1. **Ask User for Inputs**:
   - Ask the user for the **Category** (e.g., "developers", "business").
   - Ask for the **Use Case** (e.g., "Python API Client", "Meeting Minutes").
   - Ask for key **Variables** (e.g., "language", "tone").

2. **Generate Draft (Agent)**:
   - Act as the **Generator**.
   - Create a comprehensive draft prompt based on the inputs.
   - Follow the structure: Title, Metadata, Purpose, Prompt, Variables, Example.

3. **Review Draft (Agent)**:
   - Act as the **Reviewer**.
   - Read `tools/rubrics/quality_standards.json` (if available) or use standard criteria.
   - Critique the draft:
     - Is it specific?
     - Are examples realistic?
     - Is metadata complete?
   - Output a brief critique.

4. **Refine Draft (Agent)**:
   - Act as the **Refiner**.
   - Apply the improvements from the review.
   - Ensure the final output is a high-quality markdown file.

5. **Save and Verify**:
   - Ask the user for the filename/path to save it to.
   - Save the file.
   - Run the validator: `python tools/validators/prompt_validator.py [file_path]`
