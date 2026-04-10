# Research Library

Curated source governance artifacts and subagent reports used for research-focused workflows.

## Structure

- `library/` — Source governance data:
  - `approved_domains.md`, `reputable_sources.md` — whitelists for trusted sources
  - `source_registry.json`, `material_manifest.json` — indexed source metadata
  - `code_references.md` — code-focused reference material
- `subagents/` — Reports and roles for research assistants:
  - `ROLE_DEFINITIONS.md` — expectations for librarian, scout, curator, and auditor roles
  - `*_REPORT.md` files — prior research runs and findings per role

## How to use

- Check `library/` before adding new sources; extend the registries/whitelists instead of scattering lists elsewhere.
- Keep subagent reports append-only for traceability. If you open a new research thread, add a dated report file rather than overwriting existing ones.
- Align any new research guidance with `.claude/rules/common/security.md` (treat AI output as untrusted input) and cite sources per `.github/copilot-instructions.md` research standards.
