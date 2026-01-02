# Evaluation Result Schema Specification

> **Version:** 1.0.0  
> **Created:** 2026-01-01  
> **Status:** Active

This document defines the canonical result schema, output formats, and acceptance criteria for the prompt evaluation framework.

---

## Table of Contents

- [Result JSON Schema](#result-json-schema)
- [Error Codes](#error-codes)
- [Output Formats](#output-formats)
- [Input Types](#input-types)
- [Acceptance Criteria](#acceptance-criteria)

---

## Result JSON Schema

The evaluation framework produces a **single canonical result schema** for all evaluation runs. This schema is used by all reporters (JSON, Markdown, CSV) and must be produced regardless of input type or model provider.

### Required Fields (Minimum)

```json
{
  "schema_version": "1.0.0",
  "eval_id": "uuid-v4",
  "timestamp": "2026-01-01T12:00:00.000Z",
  
  "input": {
    "path": "prompts/advanced/chain-of-thought-guide.md",
    "type": "markdown",
    "title": "Chain of Thought Guide",
    "category": "advanced"
  },
  
  "model": {
    "name": "openai/gpt-4o-mini",
    "provider": "github",
    "version": null
  },
  
  "execution": {
    "tier": 2,
    "run_index": 1,
    "total_runs": 1,
    "duration_seconds": 2.69,
    "status": "success"
  },
  
  "scores": {
    "overall": 8.0,
    "rubric": {
      "clarity": 7,
      "specificity": 8,
      "actionability": 8,
      "structure": 9,
      "completeness": 8,
      "safety": 10
    },
    "structural": 75.0,
    "geval": 80.0
  },
  
  "summary": "Brief LLM-generated summary of evaluation",
  "passed": true,
  "threshold": 70.0,
  "grade": "Proficient"
}
```

### Extended Fields (Full Schema)

```json
{
  "schema_version": "1.0.0",
  "eval_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-01-01T12:00:00.000Z",
  
  "input": {
    "path": "prompts/advanced/chain-of-thought-guide.md",
    "absolute_path": "d:/source/prompts/prompts/advanced/chain-of-thought-guide.md",
    "type": "markdown",
    "title": "Chain of Thought Guide",
    "category": "advanced",
    "frontmatter": {
      "title": "Chain of Thought Guide",
      "intro": "Guide for implementing CoT reasoning",
      "category": "advanced",
      "type": "guide"
    }
  },
  
  "model": {
    "name": "openai/gpt-4o-mini",
    "provider": "github",
    "version": null,
    "parameters": {
      "temperature": 0.3,
      "max_tokens": 2000
    }
  },
  
  "execution": {
    "tier": 2,
    "tier_name": "Local G-Eval",
    "run_index": 1,
    "total_runs": 1,
    "duration_seconds": 2.69,
    "status": "success",
    "error": null,
    "error_code": null,
    "retries": 0
  },
  
  "scores": {
    "overall": 8.0,
    "overall_normalized": 80.0,
    "rubric": {
      "clarity": {"score": 7, "weight": 0.25, "reasoning": "..."},
      "specificity": {"score": 8, "weight": 0.20, "reasoning": "..."},
      "actionability": {"score": 8, "weight": 0.20, "reasoning": "..."},
      "structure": {"score": 9, "weight": 0.15, "reasoning": "..."},
      "completeness": {"score": 8, "weight": 0.10, "reasoning": "..."},
      "safety": {"score": 10, "weight": 0.10, "reasoning": "..."}
    },
    "structural": 75.0,
    "geval": 80.0
  },
  
  "summary": "The prompt is clear and well-structured...",
  "passed": true,
  "threshold": 70.0,
  "grade": "Proficient",
  
  "recommendations": [
    "Improve clarity: currently 70% (Competent)"
  ],
  "issues": [
    "Missing governance tags"
  ],
  
  "complexity": {
    "tier": "reasoning",
    "score": 20.0
  },
  
  "metadata": {
    "evaluator_version": "1.0.0",
    "rubric_version": "1.0.0",
    "hostname": "workstation",
    "platform": "win32"
  }
}
```

### Error Result Schema

When evaluation fails, the result uses this structure:

```json
{
  "schema_version": "1.0.0",
  "eval_id": "...",
  "timestamp": "...",
  
  "input": { "path": "...", "type": "..." },
  "model": { "name": "openai/o1", "provider": "github" },
  
  "execution": {
    "tier": 4,
    "run_index": 1,
    "total_runs": 1,
    "duration_seconds": 0.85,
    "status": "error",
    "error": "403 Forbidden",
    "error_code": "permission_denied",
    "retries": 0
  },
  
  "scores": null,
  "summary": null,
  "passed": false,
  "threshold": 70.0,
  "grade": null
}
```

---

## Error Codes

Standardized error codes for evaluation failures:

| Code | Description | Retry? |
|------|-------------|--------|
| `success` | Evaluation completed | N/A |
| `unavailable_model` | Model exists but not runnable | No |
| `permission_denied` | 403 Forbidden (entitlement) | No |
| `rate_limited` | 429 Too Many Requests | Yes |
| `timeout` | Request timed out | Yes |
| `parse_error` | Could not parse LLM response | Yes |
| `file_not_found` | Input file missing | No |
| `invalid_input` | Input format unsupported | No |
| `internal_error` | Unexpected evaluator error | No |

---

## Output Formats

### Markdown Report Format

```markdown
# Prompt Evaluation Report

**Generated:** 2026-01-01T12:00:00Z  
**Tier:** 2 (Local G-Eval)  
**Threshold:** 70%

## Summary

| Metric | Value |
|--------|-------|
| Files Evaluated | 15 |
| Passed | 12 (80%) |
| Failed | 3 (20%) |
| Average Score | 78.5% |
| Models Used | phi4, mistral |

## Results by File

### ✅ chain-of-thought-guide.md — 85% (Proficient)

| Criterion | Score | Grade |
|-----------|-------|-------|
| Clarity | 90% | Exceptional |
| Specificity | 85% | Proficient |
| Actionability | 80% | Proficient |
| Structure | 85% | Proficient |
| Completeness | 80% | Proficient |

**Summary:** Well-structured prompt with clear instructions...

### ❌ basic-template.md — 55% (Developing)

| Criterion | Score | Grade |
|-----------|-------|-------|
| Clarity | 60% | Developing |
| Specificity | 50% | Inadequate |
| ... | ... | ... |

**Issues:**
- Missing frontmatter: intro, type
- No code examples found

**Recommendations:**
- Improve specificity: currently 50% (Inadequate)

## Model Comparison (if multi-model)

| Model | Avg Score | Evals | Failures |
|-------|-----------|-------|----------|
| phi4 | 82% | 15 | 0 |
| gpt-4o-mini | 78% | 15 | 1 |
```

### CSV Format

```csv
eval_id,timestamp,path,type,model,provider,tier,run,status,overall,clarity,specificity,actionability,structure,completeness,safety,passed,grade
abc123,2026-01-01T12:00:00Z,prompts/advanced/cot.md,markdown,phi4,local,2,1,success,85,90,85,80,85,80,100,true,Proficient
def456,2026-01-01T12:00:01Z,prompts/basic/template.md,markdown,phi4,local,2,1,success,55,60,50,55,60,50,80,false,Developing
```

---

## Input Types

### Supported Input Types

| Type | Location | Extension | Description |
|------|----------|-----------|-------------|
| **Markdown Prompts** | `prompts/**` | `.md` | Standard prompt files with YAML frontmatter |
| **Prompt YAML** | `testing/evals/**` | `.prompt.yml` | GitHub Models evaluation format |

### Excluded Files (Discovery Rules)

The following patterns are **always excluded** from evaluation:

- `README.md` — Documentation files
- `index.md` — Index/navigation files
- `*.agent.md` — Agent definition files
- `*.instructions.md` — Instruction files
- Files in `archive/` directories
- Files in `_archive/` directories
- Files in `templates/` that are scaffolds, not prompts

### Input Type Detection

```python
def detect_input_type(path: Path) -> str:
    if path.suffix == ".md":
        return "markdown"
    elif path.suffix in (".yml", ".yaml") and "prompt" in path.stem:
        return "prompt_yaml"
    else:
        raise ValueError(f"Unsupported input type: {path}")
```

---

## Acceptance Criteria

### Validation Test Cases

The following must pass for schema compliance:

1. **Schema compliance**: Every result from `prompteval` must validate against the schema
2. **Input flexibility**: `python -m prompteval prompts/advanced/cot.md` and `python -m prompteval testing/evals/advanced/` both produce valid results
3. **Error handling**: Known-failing models produce error results (not crashes) with correct `error_code`
4. **Report generation**: `-o report.md` produces valid Markdown matching the format above
5. **JSON export**: `-o results.json` produces valid JSON matching the schema

### Grade Thresholds

| Score Range | Grade | Description |
|-------------|-------|-------------|
| 90-100% | Exceptional | Exceeds all criteria |
| 80-89% | Proficient | Meets all criteria well |
| 70-79% | Competent | Meets minimum requirements |
| 60-69% | Developing | Below threshold, needs improvement |
| 0-59% | Inadequate | Fails most criteria |

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-01-01 | 1.0.0 | Initial schema specification (Phase 0 complete) |
