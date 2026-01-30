 
# GitHub Copilot instructions for the `prompts` repository

This file is a lightweight compatibility pointer and quick reference. The authoritative, repo-wide guidance is in:

- `.github/instructions/prompts-repo.instructions.md` — guardrails, checklists, and authoring conventions
- `.github/copilot-instructions.md` — comprehensive developer guidance and workflows

Quick reminders:

- Keep diffs small and reviewable; avoid bulk rewrites.
- Prompt files live under `prompts/` and must follow the frontmatter schema in `docs/reference/frontmatter-schema.md`.
- Use templates in `prompts/templates/` when creating new prompts.
- Validate prompt edits with the repo tasks or `python -m tools.validate_prompts --all` and run tests with `python -m pytest testing/` when changing tooling.

Refer to `prompts-repo.instructions.md` for full rules and examples.

  # Multi-Agent Workflow Best Practices: Copilot Enforcement Checklist

When Copilot generates, edits, or reviews code and prompts for multi-agent workflows, it MUST:

1. **Enforce Schema Validation**
	- Require all agent outputs to strictly match their defined JSON schemas.
	- Insert runtime schema validation code or checks where missing.
	- Flag or block changes that weaken schema guarantees.

2. **Require Robust Error Handling & Rollback**
	- Ensure every agent step has explicit error handling and fallback logic.
	- Add or update rollback mechanisms for partial failures or ambiguous outputs.
	- Highlight missing or incomplete error/rollback logic in reviews.

3. **Mandate Artifact Examples**
	- Include or update concrete sample outputs for each artifact type (evidence table, score report, patch, validation, synthesis decision) in code, docs, or tests.
	- Prompt for missing examples when new artifact types are introduced.

4. **Monitor Metrics & Alerts**
	- Track and document key metrics (agent pass rate, latency, error rates, test coverage) in code and documentation.
	- Add alerting logic for critical failures (e.g., security gate, model latency) where appropriate.

5. **Highlight Human-in-the-Loop Review Points**
	- Clearly annotate workflow points requiring human review or manual override in code and prompts.
	- Suggest reviewer guidance or checklists for these points.

6. **Document Branch Strategy Guidance**
	- For each branch evaluation strategy, require rationale, best use cases, and trade-offs in code comments or docs.
	- Block merges that introduce new strategies without this documentation.

7. **Promote Reproducibility**
	- Require logging of seeds, model versions, configuration snapshots, and run metadata for every execution.
	- Add or update reproducibility instructions in README or workflow docs.

8. **Ensure Comprehensive Test Coverage**
	- Check for and prompt the addition of test cases covering edge cases, adversarial inputs, and agent integration.
	- Block or flag changes that reduce test coverage or omit critical tests.

**Copilot Enforcement Policy:**
- These practices are mandatory for all code and prompt changes in multi-agent workflow projects.
- Copilot must always check for these requirements and prompt the user if any are missing or incomplete.
- When in doubt, Copilot should default to stricter enforcement and request clarification from the user.

---
# GitHub Copilot instructions (compatibility pointer)

This repo now uses a standard targeted instructions file:


And the canonical repo map + commands live in:


If you’re seeing this file referenced by older docs/config, use the two files above.
```instructions
# GitHub Copilot instructions for the `prompts` repository
