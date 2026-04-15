# Backlog: Agent Behaviors & Rules Integration

Created: 2026-04-11

## Reference source

This backlog is derived from architecture and behavior patterns reviewed in:

- Reference repo: `C:\Users\tandf\source\claude-code-main`

Relevant source areas include:

- `src/skills/` and `src/skills/bundled/`
- `src/tools/`
- `src/utils/tokenBudget.ts`
- `src/utils/diff.ts`
- `src/utils/treeify.ts`
- `src/bridge/`

## Goal

Integrate two high-value behavior systems into the `prompts` repository:

1. Self-correction and verification loops
2. Prompt data sanitization and security enforcement

These capabilities should be implemented through a combination of:

- `.claude/skills/`
- repository instructions and rules
- hooks where deterministic enforcement is needed
- Python runtime middleware in the orchestration path
- workflow-aware validation and bounded retry policies

## Why this matters

- Improves output reliability by forcing post-generation verification
- Prevents agents from handing off broken code without trying to fix it
- Reduces risk of leaking secrets or sensitive content into provider-bound prompts
- Makes prompt safety enforceable in code instead of relying only on prose rules

## Source-derived high-value extraction candidates

These ranked items were identified by reviewing the reference implementation in
`C:\Users\tandf\source\claude-code-main` and are the highest-value patterns to
adapt across `prompts`, `ExecutionKit`, or standalone packages.

| Rank | Capability | Primary reference | Recommended home | Why it matters |
| --- | --- | --- | --- | --- |
| 1 | Agent orchestration runtime | `src/tools/AgentTool/AgentTool.tsx` | `ExecutionKit` or standalone runtime package | Enables delegated execution, specialist routing, and bounded multi-agent workflows |
| 2 | Skill system as executable prompt programs | `src/tools/SkillTool/SkillTool.ts`, `src/skills/loadSkillsDir.ts`, `src/skills/bundled/` | `prompts` | Turns prompt procedures into reusable, discoverable, versionable execution units |
| 3 | Deferred tool loading and tool search | `src/utils/toolSearch.ts` | `ExecutionKit` or standalone runtime package | Keeps capability discovery scalable without loading every tool eagerly |
| 4 | Agent manifest loader | `src/tools/AgentTool/loadAgentsDir.ts` | `prompts` and `ExecutionKit` | Makes agent definitions portable, file-based, and easy to customize per repo |
| 5 | Prompt safety and Unicode-aware sanitization | `src/utils/sanitization.ts` | `prompts` | Provides deterministic preflight cleanup, redaction, and policy enforcement |
| 6 | MCP tool adapter pattern | `src/tools/MCPTool/MCPTool.ts` | `ExecutionKit` or standalone integration package | Standardizes external capability exposure without hard-coding every provider/tool |
| 7 | Conditional path-based skill activation | `src/skills/loadSkillsDir.ts` | `prompts` | Activates the right behavior automatically from repo structure and scope |
| 8 | Plugin architecture | `src/plugins/builtinPlugins.ts` | standalone package or `ExecutionKit` | Creates a clean extension seam for optional behaviors and bundled integrations |
| 9 | Patch and diff primitives | `src/utils/diff.ts` | standalone package | Supports safe structured edits, review flows, and self-correction repair loops |
| 10 | Tree and context compression | `src/utils/treeify.ts` | standalone package | Compresses large repo context into model-friendly views without losing structure |

### Near-term recommendation

- Prioritize ranks 2, 5, and 7 inside `prompts`
- Prioritize ranks 1, 3, 4, and 6 for shared runtime extraction
- Follow with ranks 9 and 10 as standalone utilities consumed by both ecosystems

## Backlog items

| ID | Item | Type | Dependencies | Output |
| --- | --- | --- | --- | --- |
| ABI-001 | Design architecture for skills, instructions, hooks, and middleware split | architecture | — | Architecture plan + file map |
| ABI-002 | Design reusable self-correction loop behaviors for coding, workflow authoring, and research tasks | design | ABI-001 | Skill/instruction design |
| ABI-003 | Design prompt sanitization policy, redaction categories, and enforcement outcomes | design | ABI-001 | Sanitization spec + contracts |
| ABI-004 | Implement `.claude` skills and/or instructions for bounded self-correction loops | implementation | ABI-002 | New skill folders/files |
| ABI-005 | Implement prompt sanitization middleware and reusable result models in Python | implementation | ABI-003 | Middleware modules + tests |
| ABI-006 | Wire verification policies into relevant workflow and agent execution paths | integration | ABI-004, ABI-005 | Runtime integration |
| ABI-007 | Add tests, fixtures, and failure-mode coverage for sanitization and verification loops | testing | ABI-005, ABI-006 | Test coverage |
| ABI-008 | Document usage, rollout strategy, and operator guidance | docs | ABI-004, ABI-005, ABI-006 | Docs updates |

## Suggested execution order

1. ABI-001 — architecture split
2. ABI-002 — self-correction design
3. ABI-003 — sanitization design
4. ABI-004 — customization files
5. ABI-005 — middleware implementation
6. ABI-006 — runtime integration
7. ABI-007 — validation and test coverage
8. ABI-008 — docs and rollout notes

## Iterative prompt pack

Use the prompts in `docs/backlog/prompts/` in order:

1. `01-architecture-plan.md`
2. `02-self-correction-design.md`
3. `03-sanitization-design.md`
4. `04-implement-customizations.md`
5. `05-implement-middleware.md`
6. `06-rollout-validation.md`

## Definition of done

- New `.claude` skills/instructions exist for bounded verification behavior
- Sanitization runs before outbound provider calls in the relevant runtime path
- Secret-like payloads are classified as clean, redacted, blocked, or requires-approval
- Verification retries are bounded and policy-driven
- Tests cover happy path, retries, failures, and false-positive sanitization cases
- Documentation explains where logic is advisory vs enforced
