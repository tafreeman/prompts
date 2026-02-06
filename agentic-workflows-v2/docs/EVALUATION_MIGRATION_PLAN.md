# Evaluation Migration & Consolidation Plan (Enhanced)

## Objective

Consolidate all evaluation logic into `agentic-v2-eval`, merging the best of:

1. **Execution-Based Eval**: SWE-bench style sandbox execution (from `multiagent-workflows`).
2. **LLM-Based Eval**: "Judge" patterns for quality, coherence, relevance (from `tools/prompteval`).
3. **Pattern Eval**: Structural compliance for ReAct/CoVe/etc. (from `unified_scorer.py`).
4. **Code Static Analysis**: AST-based metrics (already in `agentic-v2-eval`).

## Phase 1: Core Framework Extensions

### 1.1 Foundation & Registry

* [x] **Enhance `agentic_v2_eval/evaluators/base.py`**:
  * Define `Evaluator` abstract base class.
  * Implement `EvaluatorRegistry` for loading by name.
* [x] **Create `agentic_v2_eval/evaluators/llm.py`**:
  * Port `LLMEvaluator` class from `tools/prompteval/builtin_evaluators.py`.
  * Implement "Choice-based" scoring logic (robust parsing of 1-5 ratings).
  * **Note:** initial choice-matching implementation exists; expand robustness as part of Phase 3 tests.
* [ ] **Create `agentic_v2_eval/evaluators/string.py`**:
  * Port `StringEvaluator` (contains, starts_with, etc.).

### 1.2 Execution Sandbox (The "Runner")

* [x] **Create `agentic_v2_eval/runners/sandbox.py`**:
  * ~~Port `ExecutionScorer` logic from `multiagent_workflows`.~~
  * ~~Implement `DockerSandbox`.~~
  * **Done**: `LocalSubprocessSandbox` implemented in `sandbox/local.py` (cross-platform, safe-mode, timeout support).
  * DockerSandbox deferred to later phase (optional for production isolation).

**Status note:** Sandbox interface at `agentic_v2_eval/sandbox/base.py` (ExecutionResult + Sandbox ABC). `LocalSubprocessSandbox` fully implemented and tested (22 tests).

## Phase 2: Logic Migration

### 2.1 Prompt Pattern Scoring (The "Unified Scorer")

**Source**: `tools/prompteval/unified_scorer.py`
**Destination**: `agentic_v2_eval/scorers/prompt.py`

* [ ] Port `score_prompt` (Standard 5-dim rubric: Clarity, Effectiveness, etc.).
* [ ] Port `score_pattern` (Complex Pattern Eval: ReAct, CoVe, RAG).
* [ ] **Refactor**: Decouple from specific `llm_client`. Use `agentic-v2`'s standard model interface.
* [ ] **Refactor**: Move judget prompts to `agentic_v2_eval/prompts/judges.py`.

### 2.2 Built-in LLM Evaluators

**Source**: `tools/prompteval/builtin_evaluators.py`
**Destination**: `agentic_v2_eval/evaluators/library.py`

* [ ] Register standard evaluators:
  * `Coherence`
  * `Fluency`
  * `Relevance`
  * `Groundedness` (RAG context check)
  * `Similarity` (Equivalence)

### 2.3 SWE-Bench Evaluation Logic

* [ ] **Create `agentic_v2_eval/evaluators/swe.py`**:
  * Logic to parse SWE-bench task instances.
  * Logic to prepare git repos and apply patches.
  * Integration with `sandbox.py` runner to execute verification.

## Phase 3: Validation & Testing

* [ ] **Unit Tests**:
  * `test_llm_evaluator.py`: Mock model responses, verify choice parsing.
  * `test_pattern_scorer.py`: Verify ReAct state machine logic.
  * `test_sandbox.py`: Verify Docker command construction.
* [ ] **Integration Proof**:
  * Run a mock "Agent" generating a simple Python script.
  * Evaluate it using `swe.py` (execution correctness).
  * Evaluate the agent's thought process using `prompt.py` (ReAct pattern compliance).

## Phase 4: Cleanup & Switchover

* [ ] **Delete Old Code**:
  * `d:\source\prompts\multiagent-workflows\src\multiagent_workflows\evaluation\`
  * `d:\source\prompts\tools\prompteval\`
* [ ] **Update Consumers**:
  * Update `agentic-workflows-v2` to import from new locations.
  * Update `scripts/` to use new `agentic-v2-eval` CLI.

## Key Enhancements

* **Unified Registry**: All evaluators (Code, LLM, String) accessible via one interface.
* **Separation of Concerns**: Runners (Execution) vs Evaluators (Scoring) vs Reporters (formatting).
* **robustness**: Porting the "Choice Matching" logic from `builtin_evaluators.py` is critical for reliable LLM scoring.

---

## Appendix A: Benchmark / Dataset Infrastructure (Already Complete)

> **Location:** `tools/agents/benchmarks/`
>
> Datasets are already defined with loaders and an interactive runner. The migration plan targets consolidating them into `agentic-v2-eval` or adding a dependency bridge.

| File | Purpose | Status |
|------|---------|--------|
| `datasets.py` | `BenchmarkDefinition` + `BENCHMARK_DEFINITIONS` for SWE-bench (full/verified/lite), HumanEval (+plus), MBPP (sanitized), CodeClash, Custom Local | ✅ Complete |
| `loader.py` | `BenchmarkTask` struct, loaders from HuggingFace, GitHub, local JSON; on-demand caching | ✅ Complete |
| `registry.py` | `BenchmarkConfig`, `BenchmarkRegistry`, preset configs (`quick-test`, `swe-bench-eval`) | ✅ Complete |
| `runner.py` | Interactive CLI; auto-discovers models; runs multi-agent workflows against tasks | ✅ Complete |
| `llm_evaluator.py` | LLM-based judge for workflow output quality | ✅ Complete |

### Remaining Work

* [x] **Import/bridge into `agentic-v2-eval`**: `agentic_v2_eval.datasets` module re-exports all benchmark types and functions (list_benchmarks, load_benchmark, BenchmarkTask, etc.).
* [x] **Add tests in `agentic-v2-eval/tests/test_benchmarks.py`** for benchmark loading (32 tests covering definitions, loader, cache, registry, presets).
* [x] **Add tests in `agentic-v2-eval/tests/test_datasets_bridge.py`** for datasets bridge module (16 tests).

---

## Appendix B: LLMClientAdapter (P1 Complete)

> **Location:** `agentic-v2-eval/src/agentic_v2_eval/adapters/`
>
> Bridges `tools.llm.LLMClient` to the `LLMClientProtocol` expected by `LLMEvaluator` and other LLM-based components.

| File | Purpose | Status |
|------|---------|--------|
| `__init__.py` | Exports `LLMClientAdapter`, `create_llm_client` | ✅ Complete |
| `llm_client.py` | Adapter wrapping `tools.llm.llm_client.LLMClient` static methods | ✅ Complete |

### Usage Example

```python
from agentic_v2_eval.adapters import LLMClientAdapter, create_llm_client
from agentic_v2_eval.evaluators.llm import LLMEvaluator, STANDARD_CHOICES

# Create adapter for tools.llm.LLMClient
client = create_llm_client(model="gh:gpt-4o-mini")

# Use with LLMEvaluator
evaluator = LLMEvaluator(
    model_id="gh:gpt-4o-mini",
    system_prompt="Rate the quality on a scale of 1-5.",
    prompt_template="Rate this output:\n\n{output}",
    choices=STANDARD_CHOICES,
    llm_client=client,
)

result = evaluator.evaluate("Agent generated this response...")
```

### Tests

* `agentic-v2-eval/tests/test_adapters.py` — 13 tests covering adapter creation, protocol compliance, and delegation.
