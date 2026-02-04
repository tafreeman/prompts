---
description: Automatically map and document the entire repository structure and key files.
---

# Repository Documentation Workflow

This workflow systematically explores the repository, identifies key functional areas, and generates a comprehensive catalog of documents and source files.

// turbo-all

## Instructions

1. **Phase 1: Inventory & Discovery**
   - Run a recursive file listing excluding `.git`, `__pycache__`, `.venv`, and other build artifacts.
   - Save the raw list to `_discovery/raw_file_list.txt`.

2. **Phase 2: Functional Mapping**
   - Categorize the file list into high-level domains:
     - `Core Logic`: `multiagent-workflows/src`, `tools/core`
     - `Workflows`: `multiagent-workflows/config`, `workflows/`
     - `Prompts`: `prompts/`
     - `Tools & Utils`: `tools/`, `scripts/`
     - `Documentation`: `docs/`, `README.md`
     - `Tests`: `tests/`, `multiagent-workflows/tests`

3. **Phase 3: Deep Analysis (Agentic)**
   - For each domain, identify the "entry point" or "overview" files (e.g., `README.md`, `__init__.py`, `config.yaml`).
   - Use an agent to read these files and summarize the purpose of the domain and its key components.

4. **Phase 4: Synthesis & Reporting**
   - Combine all summaries into a premium `REPO_DOCUMENTS.md` file.
   - Include a "Document Catalog" section with a nested list of all significant files and a 1-sentence description for each major folder.

## Tools Required

- `list_dir` / `find_by_name` (via MCP or command line)
- `view_file` (for analysis)
- `write_to_file` (for report generation)

## Expected Output

- `REPO_DOCUMENTS.md`: The definitive guide to the repository's contents.
