# Prompt Validation Remediation Plan

**Goal**: Fix all 137 prompt files failing `python tools/validate_prompts.py --all`

**Generated**: 2026-01-21

---

## Executive Summary

| Issue Type | Count | Effort |
|------------|-------|--------|
| Missing `## Prompt` section | 110 | Medium (add section + move/format prompt text) |
| Missing `## Description` section | 107 | Low (write 2-3 sentences) |
| Missing `## Example` section | 91 | Medium (create realistic input/output) |
| Missing `## Variables` section | 60 | Low (extract placeholders → table) |
| **Total files affected** | **137** | — |

---

## Breakdown by Category

| Category | Files | Priority | Notes |
|----------|-------|----------|-------|
| `business/` | 36 | High | Largest set; high user visibility |
| `analysis/` | 19 | High | Frequently used prompts |
| `system/` | 16 | Medium | System prompts may need special handling |
| `advanced/` | 13 | Medium | Complex prompts; examples matter |
| `agents/` | 10 | Medium | Agent definitions |
| `developers/` | 10 | Medium | Developer tooling prompts |
| `techniques/` | 10 | Medium | Technique references |
| `creative/` | 8 | Low | Creative writing prompts |
| `frameworks/` | 5 | Low | Framework integration guides |
| `governance/` | 3 | Low | Policy/compliance prompts |
| `m365/` | 3 | Low | Microsoft 365 specific |
| `templates/` | 2 | Low | Meta-templates |
| `socmint/` | 1 | Low | OSINT prompt |
| Root file | 1 | Low | `self-consistency-reasoning.md` |

---

## Remediation Strategy

### Phase 1: Automated Pre-Processing

1. **Generate a manifest** of all affected files with their specific issues.
2. **Classify each file** by its `type` frontmatter (reference vs. template vs. how_to) to determine required sections.
3. **Extract existing content** that can be repurposed:
   - Look for inline descriptions in frontmatter or first paragraph → `## Description`
   - Look for code blocks that are the actual prompt → `## Prompt`
   - Look for `[PLACEHOLDER]` patterns → `## Variables` table

### Phase 2: Section-by-Section Fixes

#### 2a. Add `## Description` (107 files)

**Pattern**:
```markdown
## Description

[2-3 sentences explaining what this prompt does and when to use it.]
```

**Source**: Derive from `name` + `description` frontmatter if present, or summarize the prompt's purpose from its content.

#### 2b. Add `## Prompt` (110 files)

**Pattern**:
```markdown
## Prompt

### System Prompt (if applicable)

```text
[system instructions]
```

### User Prompt

```text
[user-facing prompt with [VARIABLES]]
```
```

**Source**: Many files already have the prompt text inline but not under a `## Prompt` heading. Identify and wrap it.

#### 2c. Add `## Variables` (60 files)

**Pattern**:
```markdown
## Variables

| Variable | Description |
|----------|-------------|
| `[VAR_NAME]` | What to replace this with |
```

**Source**: Scan prompt text for `[BRACKETED_PLACEHOLDERS]` and generate table entries.

#### 2d. Add `## Example` (91 files)

**Pattern**:
```markdown
## Example

### Input

```text
[Concrete example with variables filled in]
```

### Expected Output

```text
[Representative AI response]
```
```

**Source**: Create realistic examples based on the prompt's purpose. This is the most manual step.

### Phase 3: Validation Loop

After each batch of fixes:
1. Run `python tools/validate_prompts.py --all`
2. Capture remaining issues
3. Repeat until clean

---

## Execution Approach

### Option A: Subagent Batch Processing (Recommended)

Use a subagent to process files in batches by category:

```
For each category folder:
  1. Read all failing files in that folder
  2. For each file:
     a. Parse existing content
     b. Add missing sections using template patterns
     c. Extract variables from prompt text
     d. Generate a plausible example
  3. Validate the batch
  4. Report results
```

**Batch order** (by priority):
1. `business/` (36 files)
2. `analysis/` (19 files)
3. `system/` (16 files)
4. `advanced/` (13 files)
5. `agents/` + `developers/` + `techniques/` (30 files)
6. Remaining folders (23 files)

### Option B: Manual Triage

If automated fixing is unreliable:
1. Fix `templates/` first (2 files) to establish patterns
2. Fix high-visibility categories manually
3. Use validation output to track progress

---

## Acceptance Criteria

- [ ] `python tools/validate_prompts.py --all` exits with code 0
- [ ] All prompt files have: `## Description`, `## Prompt` (if not reference type), `## Variables` (if not reference type), `## Example`
- [ ] No regressions in `pytest testing/ -v`
- [ ] Changes are reviewable (small diffs per file)

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Generated examples are unrealistic | Flag files for human review post-fix |
| Breaking existing content | Preserve original content; add sections only |
| Type misclassification | Check `type` frontmatter before adding Prompt/Variables |
| Large PR is hard to review | Split by category folder; one PR per batch |

---

## Subagent Prompt Template

```text
You are fixing prompt validation issues in a prompt library repository.

For the file at [FILE_PATH]:
1. Read the current content
2. Check which sections are missing: Description, Prompt, Variables, Example
3. Add ONLY the missing sections following the template at prompts/templates/prompt-template.md
4. For ## Description: Write 2-3 sentences based on the prompt's purpose
5. For ## Prompt: Wrap existing prompt text in proper ### System Prompt / ### User Prompt subsections
6. For ## Variables: Scan for [BRACKETED_PLACEHOLDERS] and create a markdown table
7. For ## Example: Create a realistic input/output pair

Rules:
- Do NOT modify existing content except to restructure into proper sections
- Keep frontmatter unchanged unless fixing obvious issues
- If type is 'reference', 'guide', or 'tutorial', skip Prompt and Variables sections
- Preserve all existing sections and their content

Output the complete fixed file content.
```

---

## Next Steps

1. ✅ Plan created
2. ⏳ Launch subagent to process first batch (`business/` folder)
3. ⏳ Validate results
4. ⏳ Iterate through remaining categories
