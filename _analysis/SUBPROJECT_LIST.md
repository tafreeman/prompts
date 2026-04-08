# Subproject Inventory

Confirmed 2026-04-08 during documentation audit.

| Subproject | Path | Type | Has README | Has CLAUDE.md | Has docs/ |
|---|---|---|---|---|---|
| Agentic Workflows v2 | `agentic-workflows-v2/` | Python runtime (hatchling) | ✅ | ❌ | ✅ (10 files) |
| Agentic Workflows UI | `agentic-workflows-v2/ui/` | React 19 dashboard (Vite 6) | ✅ | ❌ | ❌ |
| Evaluation Framework | `agentic-v2-eval/` | Python eval (hatchling) | ✅ | ❌ | ✅ (7 files) |
| Shared Tools | `tools/` | Python utilities (hatchling) | ✅ (thin) | ❌ | ❌ |
| Presentation System | `presentation/` | React 19 (Vite 5, Storybook) | ❌ **missing** | ✅ | ❌ |
| Deck Generator | `decks-generated/` | YAML-to-PPTX builder | ✅ | ✅ | ❌ |
| Examples | `examples/` | 6 Python examples | ✅ | ❌ | ❌ |
| Research Library | `research/` | Archival research artifacts | ❌ (subdir only) | ❌ | ❌ |
| Documentation | `docs/` | Architecture, ADRs, audits | ✅ | ❌ | N/A |
| Claude Config | `.claude/` | Commands, rules, skills, agents | ✅ | ❌ | N/A |
| GitHub Config | `.github/` | CI, agents, templates | ✅ (agents/) | ❌ | N/A |

## Changes from initial inventory

- **Confirmed**: All 11 entries above verified against filesystem.
- **Added**: `examples/` — standalone runnable examples with README.
- **Clarified**: `presentation/` has CLAUDE.md but no README.md.
- **Note**: `prompts/` is not a subproject — it is the repo root itself.
- **Note**: `output/`, `reports/`, `scripts/` are utility directories, not subprojects.
