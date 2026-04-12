# Prompt 01 — Architecture plan

## Use this for

Designing the overall split between skills, instructions, hooks, and runtime middleware for agent behavior reliability and prompt safety.

## Prompt

```markdown
# Role
You are an expert AI systems architect and prompt-infrastructure engineer specializing in agent behavior design, secure prompt pipelines, and repository-level customization systems.

# Objective
Create a concrete architecture plan for integrating two capabilities into `C:\Users\tandf\source\prompts`:

1. Self-correction and verification loops
2. Prompt data sanitization and security

The solution must fit the existing Python-heavy orchestration repo and use the right mix of:
- `.claude/skills/`
- rules/instructions
- hooks
- runtime middleware
- workflow integration

# Reference source
Base your recommendations on the architecture patterns studied in the reference repository:

- `C:\Users\tandf\source\claude-code-main`

Prioritize lessons and reusable patterns from:

- `src/skills/`
- `src/skills/bundled/`
- `src/tools/`
- `src/utils/tokenBudget.ts`
- `src/bridge/`

# Tasks
1. Recommend what belongs in skills vs instructions vs hooks vs middleware.
2. Propose exact file and folder paths to add or update.
3. Define which parts are advisory and which are deterministic/enforced.
4. Explain how this integrates with workflows, agents, and tool execution.
5. Produce an ordered implementation plan with dependencies.

# Constraints
- Prefer Python for runtime enforcement unless there is a strong reason otherwise.
- Avoid duplicating the same logic in multiple personas.
- Security-critical behavior must not live only in prompt text.
- Be opinionated and specific to this repo.

# Deliverable format
Return:
1. Recommended architecture
2. Skill vs instruction vs hook vs middleware split
3. Proposed file map
4. Integration points
5. Ordered implementation plan
6. Top risks and mitigations
```
