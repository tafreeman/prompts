# Tools Directory Reference

**Generated**: 2025-12-19  
**Files Analyzed**: 23 Python files  
**Recommendation Summary**: 18 KEEP, 3 CONSOLIDATE, 2 ARCHIVE

---

## Summary

The `tools/` directory contains Python scripts for:

- **LLM Integration** (multi-provider client, local ONNX, Windows AI)
- **Prompt Evaluation** (tiered evaluation, CoVe, batch processing)
- **Prompt Improvement** (assessment, recommendations)
- **Validation** (frontmatter, links, structure)
- **Multi-modal** (image generation, speech-to-text)

---

## Core Infrastructure

### `llm_client.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `tools/llm_client.py` |
| **Type** | Library |
| **Lines** | 425 |

#### Function

Unified LLM dispatcher supporting 8+ providers with single `LLMClient.generate_text()` interface. Routes requests to local ONNX, GitHub Models, Azure Foundry, OpenAI, Claude, Gemini, Ollama, and Windows AI.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model_name` | str | Required | Provider:model (e.g., `gh:gpt-4o`, `local:phi4`) |
| `prompt` | str | Required | User prompt text |
| `system_instruction` | str | None | Optional system prompt |
| `temperature` | float | 0.7 | Sampling temperature |
| `max_tokens` | int | 4096 | Max output tokens |

#### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_TOKEN` | For `gh:*` | GitHub Models API |
| `AZURE_FOUNDRY_API_KEY` | For `azure-foundry:*` | Azure Foundry |
| `OPENAI_API_KEY` | For `gpt-*` | OpenAI API |
| `ANTHROPIC_API_KEY` | For `claude-*` | Anthropic Claude |
| `GOOGLE_API_KEY` | For `gemini-*` | Google Gemini |

#### Workflow Usage

- **Used by**: `prompt.py`, `tiered_eval.py`, `cove_runner.py`, `improve_prompts.py`
- **Calls**: Provider-specific APIs
- **Example**: `LLMClient.generate_text("gh:gpt-4o", "Hello world")`

#### Value Assessment

- **Unique Value**: Central abstraction for all LLM providers
- **Overlap**: None - core infrastructure
- **Recommendation**: **KEEP** (Critical)

---

### `local_model.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `tools/local_model.py` |
| **Type** | Library + CLI |
| **Lines** | 460 |

#### Function

Local ONNX model runner using `onnxruntime-genai`. Runs Phi-4, Phi-3.5, Mistral-7B locally on CPU/GPU. Provides both text generation and prompt evaluation.

#### Parameters (CLI)

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `-p, --prompt` | str | Required | Prompt text or file path |
| `-m, --model` | str | auto | Model key (phi4, mistral-7b, etc.) |
| `--evaluate` | flag | - | Run evaluation mode |
| `--temperature` | float | 0.7 | Sampling temperature |
| `--max-tokens` | int | 1024 | Max output tokens |

#### Workflow Usage

- **Used by**: `llm_client.py`, `tiered_eval.py` (Tier 0)
- **Example**: `python local_model.py -p "Explain AI" -m phi4`

#### Value Assessment

- **Unique Value**: Free local inference with no API keys
- **Recommendation**: **KEEP** (Core for $0 evaluation)

---

### `windows_ai.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `tools/windows_ai.py` |
| **Type** | Library + CLI |
| **Lines** | 240 |

#### Function

Windows Copilot Runtime integration for Phi Silica SLM on NPU. Uses C# bridge to access Windows App SDK 1.7+ APIs.

#### Requirements

- Windows 11 with NPU (Copilot+ PC)
- Windows App SDK 1.7+
- `dotnet build tools/windows_ai_bridge/`

#### Workflow Usage

- **Used by**: `llm_client.py`, `tiered_eval.py` (Tier 7)
- **Example**: `python windows_ai.py -p "Hello AI" --verbose`

#### Value Assessment

- **Unique Value**: NPU-accelerated local inference
- **Recommendation**: **KEEP** (Unique capability)

---

## Evaluation Tools

### `tiered_eval.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `tools/tiered_eval.py` |
| **Type** | CLI |
| **Lines** | 1502 |

#### Function

Multi-tier evaluation system with 8 cost/depth levels (Tier 0-7). Orchestrates evaluations from free local models to premium cloud services.

#### Tiers

| Tier | Name | Cost | Method |
|------|------|------|--------|
| 0 | Local ONNX | $0 | Phi/Mistral local |
| 1 | Quick Triage | $0 | Structure only |
| 2 | Single Model | ~$0.01 | 1 cloud model |
| 3 | Cross-Validate | ~$0.05 | 3 models × 2 |
| 4 | Full Pipeline | ~$0.15 | 5 models × 3 |
| 5 | Premium | ~$0.25 | 5 models × 4 |
| 6 | Azure Foundry | Varies | Your deployment |
| 7 | Windows AI | $0 | NPU Phi Silica |

#### Parameters (CLI)

| Flag | Type | Description |
|------|------|-------------|
| `path` | str | Prompt file or directory |
| `-t, --tier` | int | Tier level (0-7) |
| `-o, --output` | str | Output directory |
| `--verbose` | flag | Detailed output |

#### Example

```bash
python tools/tiered_eval.py prompts/advanced/ -t 3 -o results/
```

#### Value Assessment

- **Unique Value**: Unified multi-tier evaluation framework
- **Recommendation**: **KEEP** (Core evaluation system)

---

### `cove_runner.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `tools/cove_runner.py` |
| **Type** | Library + CLI |
| **Lines** | 792 |

#### Function

Chain-of-Verification (CoVe) implementation. Reduces hallucinations through 4-step process: Draft → Verification Questions → Independent Answers → Final Synthesis.

#### Parameters (CLI)

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `question` | str | - | Question to answer |
| `-p, --provider` | str | local | Provider (local/gh/azure/openai) |
| `-m, --model` | str | auto | Model to use |
| `-n, --questions` | int | 5 | Number of verification questions |
| `--domain` | str | None | Domain hint |
| `-i, --interactive` | flag | - | Interactive mode |

#### Example

```bash
python tools/cove_runner.py "What is machine learning?" -p gh -m gpt-4o
```

#### Value Assessment

- **Unique Value**: Fact-checking via CoVe methodology
- **Recommendation**: **KEEP** (Unique hallucination reduction)

---

### `cove_batch_analyzer.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `tools/cove_batch_analyzer.py` |
| **Type** | CLI |
| **Lines** | 670 |

#### Function

Batch prompt analysis using CoVe methodology. Scores prompts on clarity, effectiveness, reusability, simplicity, and example quality.

#### Parameters (CLI)

| Flag | Type | Description |
|------|------|-------------|
| `folder` | str | Folder to analyze |
| `-p, --provider` | str | LLM provider |
| `-m, --model` | str | Model to use |
| `--limit` | int | Max prompts to analyze |
| `-o, --output` | str | Output JSON file |

#### Example

```bash
python tools/cove_batch_analyzer.py prompts/ -p gh -m gpt-4o --limit 10
```

#### Value Assessment

- **Unique Value**: Batch CoVe analysis
- **Overlap**: Some overlap with `batch_evaluate.py`
- **Recommendation**: **CONSOLIDATE** with batch_evaluate.py

---

### `batch_evaluate.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `tools/batch_evaluate.py` |
| **Type** | CLI |
| **Lines** | 718 |

#### Function

Batch evaluation of prompts with `effectivenessScore: pending`. Discovers prompts, runs evaluations, updates frontmatter scores.

#### Parameters (CLI)

| Flag | Type | Description |
|------|------|-------------|
| `--folder` | str | Specific folder to evaluate |
| `--runs` | int | Runs per model |
| `--skip-scored` | flag | Skip already-scored prompts |
| `--update` | flag | Update frontmatter with scores |
| `--dry-run` | flag | Don't modify files |

#### Value Assessment

- **Unique Value**: Frontmatter score updating
- **Overlap**: With `cove_batch_analyzer.py`
- **Recommendation**: **CONSOLIDATE** - merge CoVe batch into this

---

### `evaluate_library.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `tools/evaluate_library.py` |
| **Type** | CLI |
| **Lines** | 1181 |

#### Function

Unified evaluator using both rubrics: Quality Standards (0-100) and Effectiveness (1.0-5.0). Generates comprehensive reports.

#### Scoring Dimensions

| Rubric | Dimensions |
|--------|------------|
| Quality Standards | Completeness, Example Quality, Specificity, Format, Enterprise |
| Effectiveness | Clarity, Effectiveness, Reusability, Simplicity, Examples |

#### Example

```bash
python tools/evaluate_library.py prompts/ -o docs/eval-report.md
```

#### Value Assessment

- **Unique Value**: Dual-rubric evaluation
- **Recommendation**: **KEEP** (Best standalone evaluator)

---

### `evaluation_agent.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `tools/evaluation_agent.py` |
| **Type** | CLI |
| **Lines** | 1118 |

#### Function

Autonomous evaluation agent that runs complete pipeline without human intervention. Handles eval file generation, execution, result parsing, and improvement recommendations.

#### Features

- Checkpoint/resume capability
- Parallel evaluation
- Automatic retries
- Improvement plan generation

#### Parameters (CLI)

| Flag | Type | Description |
|------|------|-------------|
| `--dry-run` | flag | Preview without executing |
| `--resume` | flag | Resume from checkpoint |
| `--category` | str | Specific category to evaluate |
| `-v, --verbose` | flag | Detailed output |

#### Value Assessment

- **Unique Value**: Fully autonomous evaluation
- **Recommendation**: **KEEP** (Automation target)

---

## Improvement Tools

### `improve_prompts.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `tools/improve_prompts.py` |
| **Type** | CLI |
| **Lines** | 948 |

#### Function

Assessment engine that scores prompts against rubrics and generates improvement recommendations. Creates prioritized improvement tasks.

#### Outputs

- `IMPROVEMENT_REPORT.md` - Full assessment
- `IMPROVEMENT_PROMPTS.md` - Ready-to-use improvement prompts

#### Parameters (CLI)

| Flag | Type | Description |
|------|------|-------------|
| `--limit` | int | Max prompts to assess |
| `--worst` | int | Show N worst prompts |
| `--generate-prompts` | flag | Generate improvement prompts |
| `-o, --output` | str | Output directory |

#### Example

```bash
python tools/improve_prompts.py --worst 10 --generate-prompts
```

#### Value Assessment

- **Unique Value**: Improvement recommendations
- **Recommendation**: **KEEP** (Improvement workflow)

---

## Validation Tools

### `validate_prompts.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `tools/validate_prompts.py` |
| **Type** | CLI |
| **Lines** | 108 |

#### Function

Validates prompt files for required sections (Description, Prompt, Variables, Example) and frontmatter fields.

#### Example

```bash
python tools/validate_prompts.py
```

#### Value Assessment

- **Unique Value**: Structural validation
- **Recommendation**: **KEEP** (CI integration)

---

### `check_links.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `tools/check_links.py` |
| **Type** | CLI |
| **Lines** | ~50 |

#### Function

Checks for broken internal links in markdown files.

#### Value Assessment

- **Recommendation**: **KEEP** (Maintenance utility)

---

### `normalize_frontmatter.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `tools/normalize_frontmatter.py` |
| **Type** | CLI |
| **Lines** | ~400 |

#### Function

Normalizes and fixes frontmatter across all prompts. Ensures consistent field naming and values.

#### Value Assessment

- **Recommendation**: **KEEP** (Migration utility)

---

### `audit_prompts.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `tools/audit_prompts.py` |
| **Type** | CLI |
| **Lines** | ~200 |

#### Function

Audits prompts for migration readiness and compliance.

#### Value Assessment

- **Recommendation**: **ARCHIVE** (One-time migration)

---

## Multi-Modal Tools

### `local_media.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `tools/local_media.py` |
| **Type** | CLI |
| **Lines** | 438 |

#### Function

Local media processing: image generation (Stable Diffusion), speech-to-text (Whisper), image upscaling (ESRGAN).

#### Commands

| Command | Description |
|---------|-------------|
| `image "prompt"` | Generate image |
| `transcribe file.wav` | Audio to text |
| `upscale image.png` | 4x upscale |

#### Example

```bash
python tools/local_media.py image "sunset over mountains" -o sunset.png
```

#### Value Assessment

- **Unique Value**: Local multi-modal processing
- **Recommendation**: **KEEP** (Unique capability)

---

## Subdirectories

### `validators/`

- `frontmatter_validator.py` - Schema validation for YAML frontmatter
- Contains JSON schemas for validation

### `rubrics/`

- Scoring rubric definitions

### `models/`

- Model configuration files

### `archive/`

- Deprecated tools (4 files)

---

## Workflow Map

```
Evaluation Workflow:
  prompt.py eval → tiered_eval.py → [llm_client.py ↔ providers]
                                  ↓
                          [local_model.py | windows_ai.py]

CoVe Workflow:
  prompt.py cove → cove_runner.py → llm_client.py

Improvement Workflow:
  evaluate_library.py → improve_prompts.py → [manual edits]

Validation Workflow:
  validate_prompts.py → normalize_frontmatter.py
```

---

## Consolidation Recommendations

| Action | Files | Reason |
|--------|-------|--------|
| **CONSOLIDATE** | `cove_batch_analyzer.py` + `batch_evaluate.py` | Overlapping batch functionality |
| **ARCHIVE** | `audit_prompts.py` | One-time migration tool |
| **ARCHIVE** | `generate_eval_files.py` | Superseded by evaluation_agent |

---

## Key Environment Variables

| Variable | Tools | Purpose |
|----------|-------|---------|
| `GITHUB_TOKEN` | llm_client, tiered_eval, cove_runner | GitHub Models API |
| `AZURE_FOUNDRY_API_KEY` | llm_client, tiered_eval | Azure Foundry |
| `AZURE_FOUNDRY_ENDPOINT_1` | llm_client | Phi-4 endpoint |
| `AZURE_FOUNDRY_ENDPOINT_2` | llm_client | Mistral endpoint |
| `OPENAI_API_KEY` | llm_client | OpenAI API |
| `ANTHROPIC_API_KEY` | llm_client | Claude API |
| `GOOGLE_API_KEY` | llm_client | Gemini API |
