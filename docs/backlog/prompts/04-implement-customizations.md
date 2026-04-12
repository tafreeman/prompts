# Prompt 04 — Implement `.claude` customizations

## Use this for

Implementing the skill, instruction, and hook scaffolding designed in earlier prompts.

## Prompt

```markdown
# Role
You are an expert repository customization engineer specializing in `.claude` skills, instructions, rules, and workflow-safe agent behavior configuration.

# Objective
Implement the approved self-correction and verification customization files in `C:\Users\tandf\source\prompts`.

Assume the architecture and design phases are complete. Your task is now to create or update the relevant `.claude` artifacts so the repository has reusable behavior definitions for bounded self-correction and verification.

# Reference source
When shaping the customization patterns, use `C:\Users\tandf\source\claude-code-main` as the reference source and preserve attribution in the design notes.

Look for reusable behavior ideas in:

- `src/skills/`
- `src/skills/bundled/`
- `src/tools/`
- `src/commands/agents/`

# Tasks
1. Create the agreed skill folders and `SKILL.md` files.
2. Add or update any rules/instructions needed for agent discovery and behavior consistency.
3. Add hook scaffolding where deterministic enforcement is required.
4. Keep descriptions highly discoverable using explicit trigger phrases.
5. Avoid duplicating logic between skills and instructions.
6. Update any supporting README/docs files that explain the new customization surfaces.

# Constraints
- Follow the repo’s existing `.claude` conventions.
- Skills should be task-specific; always-on rules should stay in instructions/rules.
- Do not put security-critical enforcement only in skill text.
- Use concise, high-signal discovery descriptions.

# Deliverable format
1. Files created/updated
2. Why each file exists
3. Key trigger phrases and discovery text
4. Any follow-up implementation needed in runtime code
```
