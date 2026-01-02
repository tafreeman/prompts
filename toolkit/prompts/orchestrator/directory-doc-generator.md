---
title: Directory Documentation Generator
shortTitle: Doc Generator
type: template
model: gpt-4o
temperature: 0.3
---

# Directory Documentation Generator

Use this prompt in GitHub Copilot Chat to document any directory in the repository.

---

## How to Use

1. Open GitHub Copilot Chat
2. Paste the prompt below
3. Replace `[DIRECTORY]` with the folder to document (e.g., `agents/`, `toolkit/`, `testing/`)

---

## Prompt

```
Document all files in the [DIRECTORY] folder following this format:

## Output Format

Create a comprehensive markdown reference document with:

1. **Header Section**:
   - Title: "[DIRECTORY] Reference"
   - Generated date
   - Files analyzed count
   - Recommendation summary (X KEEP, Y CONSOLIDATE, Z ARCHIVE)

2. **Summary**: 2-3 sentences describing what this directory contains and its role

3. **For each file, document**:

### For Python Files:
```markdown
### `filename.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `path/to/file.py` |
| **Type** | CLI / Library / Script |
| **Lines** | ~XXX |

#### Function
[2-3 sentences describing what this file does]

#### Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|

#### Environment Variables (if any)
| Variable | Required | Description |
|----------|----------|-------------|

#### Workflow Usage
- **Used by**: [other tools/files that call this]
- **Calls**: [dependencies it uses]
- **Example**: `command example`

#### Value Assessment
- **Unique Value**: [what this provides]
- **Overlap**: [similar functionality elsewhere]
- **Recommendation**: KEEP / CONSOLIDATE / ARCHIVE
```

### For Markdown Prompt Files

```markdown
### `filename.md`

| Attribute | Value |
|-----------|-------|
| **Location** | `path/to/file.md` |
| **Type** | How-To / Template / Reference / Agent |
| **Frontmatter** | Complete / Partial / Missing |

#### Function
[2-3 sentences describing purpose]

#### Variables
| Variable | Required | Description |
|----------|----------|-------------|

#### Use Cases
1. [Use case 1]
2. [Use case 2]

#### Value Assessment
- **Recommendation**: KEEP / IMPROVE / MERGE / ARCHIVE
```

4. **Workflow Map**: Show how files connect in common workflows

5. **Consolidation Recommendations**: Table of suggested merges/archives

---

Now read all files in [DIRECTORY] and generate this documentation. Save to `docs/[directory-name]-reference.md`.

```

---

## Example Usage

**For agents/**:
```

Document all files in the agents/ folder following this format...

```

**For toolkit/**:
```

Document all files in the toolkit/ folder following this format...

```

**For testing/**:
```

Document all files in the testing/ folder following this format...

```

---

## Directories to Document

| Directory | Expected Output |
|-----------|-----------------|
| `agents/` | `docs/agents-reference.md` |
| `toolkit/` | `docs/toolkit-reference.md` |
| `testing/` | `docs/testing-reference.md` |
| `frameworks/` | `docs/frameworks-reference.md` |
| `app.prompts.library/` | `docs/app-reference.md` |
| `_archive/` | `docs/archive-reference.md` |
