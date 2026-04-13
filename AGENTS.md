# Agent Guidance

Repo-level map of agent surfaces and how they relate to the machine-loaded configuration under `.claude/`. Use this as the human-readable entrypoint before touching any agent files.

## Surfaces

- **`.claude/`** — Canonical, machine-loaded config. See `.claude/README.md` for layout (rules, commands, skills, agents) and loading precedence. Keep behavioral standards here.
- **`CLAUDE.md`** — Environment expectations (PowerShell-first), repo overview, and developer workflows for humans and agents.
- **`.github/copilot-instructions.md`** — Copilot-facing summary; keep aligned with `.claude/rules/` when content overlaps.
- **Subproject notes** — Some folders ship their own Claude guidance:
  - `decks-generated/CLAUDE.md` for the deck generator
  - Presentation system was extracted to `c:\Users\tandf\source\present` (April 2026)
- **Optional GitHub agents** — `.github/agents/` exists for Copilot agent surfaces; when updating, mirror canonical rules from `.claude/` instead of inventing new ones.

## Usage

1. Start with `.claude/rules/` for behavioral constraints, then consult `.claude/commands/` and `.claude/skills/` for orchestrated flows.
2. Use this `AGENTS.md` and `CLAUDE.md` to understand repo-wide expectations (platforms, tooling, coding standards).
3. Keep subproject-specific guidance close to the code (e.g., `decks-generated/CLAUDE.md`) and link back to `.claude/rules/` rather than duplicating content.
4. When adding a new agent surface, document it here and inside its directory with a short README describing how it is loaded and what rules it honors.
