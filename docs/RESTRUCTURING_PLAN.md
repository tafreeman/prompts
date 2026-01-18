# Repository Streamlining & Improvement Plan

This plan outlines the steps to clean up the repository, remove redundant code, and reorganize folders into a more intuitive and professional structure.

## 🏗️ Phase 1: Infrastructure Consolidation

### 1.1 Consolidate Archives

* Move all contents of `_archive/` into `archive/`.
* Remove the `_archive/` directory.

### 1.2 Unified Documentation

Move root-level documentation folders into the `docs/` directory to reduce root clutter:

* `get-started/` -> `docs/get-started/`
* `tutorials/` -> `docs/tutorials/`
* `concepts/` -> `docs/concepts/`
* `reference/` -> `docs/reference/`
* `troubleshooting/` -> `docs/troubleshooting/`
* `instructions/` -> `docs/instructions/`

### 1.3 Cleanup Root Scripts

Move utility scripts from the root to the `scripts/` directory:

* `Run-Tools-Ecosystem-Eval.cmd` -> `bin/` or `scripts/`
* `run-advanced-eval-local.ps1` -> `scripts/`
* `test-eval-setup.ps1` -> `scripts/`
* `test_llm_json.py` -> `testing/` or `scripts/`

## 📚 Phase 2: Content Library Reorganization

### 2.1 Group Content Resources

Move library-related folders into a more structured hierarchy. Currently, these are scattered at the root:

* `agents/` -> `prompts/agents/` (or keep at root but document as library)
* `templates/` -> `prompts/templates/`
* `techniques/` -> `prompts/techniques/`
* `frameworks/` -> `prompts/frameworks/`

### 2.2 Resolve Prompt Folder Confusion

Currently, there is a `prompts/` folder at root, which contains another `prompts/` folder conceptually (though it's actually just subfolders like `business/`).

* Ensure root `prompts/` is the clear entry point for all "Library" content.

## 🔧 Phase 3: Tooling & Code Cleanup

### 3.1 Remove Redundant Entry Points

* **DELETE** `scripts/prompt.py` (Duplicate of root `prompt.py`).
* Verify that `prompt.py` at the root is the unique entry point for all CLI operations.

### 3.2 Archive Superseded Tools

Move older/redundant tools from `tools/` to `tools/archive/`:

* `tools/enterprise_evaluator/` (Deprecated in favor of `prompteval`)
* `tools/batch_free_eval.py` (Superseded by `prompt.py batch`)
* `tools/run_eval_geval_2.py` (Superseded by `prompteval`)
* `tools/tiered_eval.py` (Superseded by `prompteval`)

### 3.3 Internal Utility Organization

Move standalone utility scripts within `tools/` to a `tools/utils/` subdirectory:

* `tools/audit_prompts.py`
* `tools/check_links.py`
* `tools/normalize_frontmatter.py`
* `tools/generate_eval_files.py`
* `tools/scan_prompts_dual.py`

## 📝 Phase 4: Path & Documentation Updates

### 4.1 Update `prompt.py` and `tools/`

* Adjust imports in internal tools to reflect new locations.
* Update `prompt.py` defaults if any content paths changed.

### 4.2 Update `README.md`

* Refresh the **Repository Structure** section to reflect the clean state.
* Update all broken links resulting from folder moves.

## 🚀 Execution Strategy

1. **Draft Implementation**: Perform moves and deletions in chunks.
2. **Verify Integrity**: Run `python prompt.py help` and basic evaluations to ensure nothing broke.
3. **Final Polish**: Update documentation links.
