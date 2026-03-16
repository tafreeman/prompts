---
name: build-all
description: Build and verify all packages in the monorepo (3 Python + 2 JS apps)
disable-model-invocation: true
---

# Build All Packages

Build every package in the monorepo to verify nothing is broken.

## Steps

1. **Sync dependencies**: `uv sync --all-packages --all-extras`
2. **Build Python packages** (in dependency order):
   - `uv build --package prompts-tools`
   - `uv build --package agentic-v2-eval`
   - `uv build --package agentic-workflows-v2`
3. **Build frontend apps**:
   - `cd agentic-workflows-v2/ui && npm install && npm run build`
   - `cd presentation && npm install && npm run build`
4. **Report results**: Show pass/fail for each package

## Error Handling

- Continue building remaining packages even if one fails
- Report ALL failures at the end, not just the first
- Exit with non-zero if any package failed
