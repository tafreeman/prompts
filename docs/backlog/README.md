# Backlog

This folder stores forward-looking implementation backlogs and prompt packs for iterative repo improvements.

## Reference source

The work in this folder is based on patterns analyzed from the reference repository:

- `C:\Users\tandf\source\claude-code-main`

Primary reference areas for this backlog:

- `src/utils/diff.ts`
- `src/utils/treeify.ts`
- `src/utils/tokenBudget.ts`
- `src/tools/`
- `src/skills/`
- `src/bridge/`

## Contents

| Path | Purpose |
| --- | --- |
| `agent-behaviors-rules-integration.md` | Backlog and delivery plan for self-correction loops and prompt sanitization/security |
| `prompts/01-architecture-plan.md` | Prompt to design the overall architecture and file layout |
| `prompts/02-self-correction-design.md` | Prompt to design skills, instructions, and bounded verification loops |
| `prompts/03-sanitization-design.md` | Prompt to design prompt sanitization middleware and policy |
| `prompts/04-implement-customizations.md` | Prompt to implement `.claude` skills/instructions and hook scaffolding |
| `prompts/05-implement-middleware.md` | Prompt to implement runtime sanitization and verification contracts |
| `prompts/06-rollout-validation.md` | Prompt to integrate, validate, document, and harden the work |

## Usage

Work through the prompts in numeric order unless you intentionally want to parallelize architecture and implementation planning.

Each prompt is written to produce an artifact or code change that feeds the next stage.
