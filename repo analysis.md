# Repository State Analysis Report

## Executive Summary

| Area | Current State | Biggest Gap | Estimated Effort |
| --- | --- | --- | --- |
| Presentation system | Functional, but monolithic and duplicated | Content and theme extraction | ~2-3 sprints for MVP |
| Non-presentation codebase | Strong overall, improving steadily | Reranking and reflection loop | ~1 sprint for next milestone |

---

## 1. Presentation System (`presentation/`)

### Current State

The `presentation/` folder contains a React + Vite single-page application that renders interactive slide decks as standalone JSX components.

#### Variant Files

| File | Lines | Purpose |
| --- | ---: | --- |
| `genai_advocacy_hub_10.jsx` | 1,575 | Primary variant (Naval Service Platform theme) |
| `genai_advocacy_hub_10_v2.0.jsx` | 2,229 | Extended variant with additional slides and sections |
| `genai_advocacy_hub_13.jsx` | 1,049 | Streamlined variant |

#### Supporting Infrastructure

- `src/main.jsx`: Vite entry point; dynamically imports one variant
- `scripts/`: 4 Node.js scripts (`build`, `export-pdf`, `export-images`, `validate-scrub`)
- `vite.config.js`, `package.json`: React 19, Vite 6, Tailwind CSS

#### Recent Changes (Last 2 Commits)

| Commit | Summary |
| --- | --- |
| `bb08a398` | Added PropTypes validation (~92 lines per file), replaced `Math.random()` with `crypto.getRandomValues()` for CSPRNG, added `validate-scrub.mjs` Playwright validator |
| `03c8000b` | Refactored terminology (`Marketplace` -> `Service Platform`), aligned component names (`SI` -> `SvgIcon`, `CI` -> `CardIcon`) |

### Technical Debt

#### Critical: Monolithic Architecture

Each variant is a single self-contained JSX file containing themes, content data, reusable components, slide layouts, navigation logic, and styling. The `THEMES` array is identically defined in all three files, creating a clear DRY violation.

Estimated duplication is roughly 55-65% of shared code across variants. A simple theme-color change currently requires updating three separate files.

#### Specific Debt Items

| Issue | Severity | Location |
| --- | --- | --- |
| `THEMES` array duplicated 3x | High | Lines 29, 4, and 4 in the variant files |
| Content strings hardcoded inline | High | Throughout all 3 files |
| Slide components defined inside each file | High | ~20 component functions per file |
| No separation of layout vs. content | Medium | Each slide is a monolithic render |
| Theme switching logic duplicated | Medium | `ThemeCtx` + provider pattern repeated 3x |
| No TypeScript (PropTypes only) | Low | Recently improved, but still lacks full type safety |
| `v10_v2.0` at 2,229 lines | Low | Exceeds 800-line file-size target |

#### Goal vs. Current Gap

| Goal | Current State | Gap |
| --- | --- | --- |
| Config-driven content swapping | Content hardcoded in JSX | Large: no config layer exists |
| Reusable template library | 3 monolithic variants | Large: templates are not extractable |
| Theme selection via config | Themes work but are duplicated | Medium: mechanism exists, needs extraction |
| Auto-adjusting themes | Basic CSS custom properties | Medium: no responsive token system |

> **Insight**  
> Config-driven presentation architecture follows a well-established pattern in the React ecosystem. Frameworks like Spectacle, Slidev, and MDX Deck use a layered model: content lives in data files, themes are token-based systems, and slide templates are composable layout primitives. The most important design idea here is a 3-tier token hierarchy: global tokens -> semantic tokens -> component tokens. Each theme should override only the semantic layer, while components consume tokens without knowing which theme is active.

### Recommended Migration Path

1. Extract shared infrastructure into `presentation/src/lib/`, including `THEMES`, `ThemeCtx`, `ThemeProvider`, navigation logic, and shared components such as `SvgIcon`, `CardIcon`, and slide chrome.
2. Move slide content into `presentation/content/*.json` files so each deck becomes content plus template selection rather than a standalone code fork.
3. Create a template registry with layout primitives like `TitleSlide`, `MetricsGrid`, `TwoColumn`, and `FullBleed`, using slot-based composition for content placement.
4. Replace the flat `THEMES` array with a CSS custom-property hierarchy using Tailwind CSS v4 `@theme`, such as `--color-primary -> --card-bg -> component styles`, to enable clean theme swapping.
5. Introduce `class-variance-authority` (`CVA`) for component variants like `<Card variant="elevated" size="lg">` to reduce conditional class-string logic and improve styling consistency.

#### Target Architecture

```text
presentation/
|-- content/
|   |-- naval-platform.json
|   `-- advocacy-hub.json
|-- src/
|   |-- lib/
|   |   |-- themes/
|   |   |-- templates/
|   |   |-- components/
|   |   `-- navigation/
|   `-- main.jsx
`-- scripts/
```

---

## 2. Non-Presentation Codebase

### Current State

**Health score:** 7.9/10

The non-presentation codebase spans roughly 49,000 lines across three packages.

#### Package Health

| Package | Approx. Lines | Health |
| --- | ---: | --- |
| `agentic-workflows-v2/agentic_v2/` | ~34,800 | Strong: protocol-first, well-tested |
| `tools/` | ~14,300 | Moderate: 30% modernized, rest needs work |
| `agentic-v2-eval/` | ~3,000 | Good: clean evaluator pattern |

Test coverage stands at 1,456 tests across 66 files. The RAG module is at roughly 92% coverage, while the overall gate remains at 70% against an 80% target.

#### Recent Changes (Last 11 Commits)

| Commit | Type | Impact |
| --- | --- | --- |
| `cf496491` | Refactor | `tools/core` modernized with PEP 604 types and structured logging across 25 files |
| `23b735ca` | Refactor | Split `model_probe.py` from ~2,000 lines into 5 files (530, 344, 651, 143, 522 lines) |
| `8304cf9a` | Refactor | Tightened protocol types (`Any` -> `WorkflowResult`), extracted server modules |
| `984d5b51` | Feature | Added 6 runnable examples with zero API key requirement |
| `eb0b3bfd` | Docs | Added onboarding guide, pattern catalog, and workflow authoring reference |
| `d4819071` | Docs | Validated ADRs and corrected fabricated citations |
| `74f547f1` | Chore | Expanded CI from 1 job to 4 jobs and added MIT license |
| `cac6582c` | Test | Added cross-package integration tests |

> **Insight**  
> The `model_probe.py` refactor in commit `23b735ca` is a strong example of extracting by concern until each file has one reason to change. The original file mixed config parsing, HTTP discovery, provider-specific logic, and output formatting. The new structure separates those concerns into focused modules and keeps `probe_providers.py` as a small facade that routes to cloud or local implementations without leaking complexity.

### Technical Debt

#### Partially Implemented Features (From 6-Week Roadmap)

| Feature | Status | What Remains |
| --- | --- | --- |
| Reranking (Week 5) | Not started | Add `CrossEncoderReranker` after hybrid retrieval, with Cohere/BGE support |
| Reflection loop (Week 5) | Designed, not wired | Architecture exists in ADR, but engine lacks an `iterate` step type |
| Iterate DSL (Week 6) | Not started | Add YAML `max_iterations` and convergence predicate support |
| Coverage gate 80% (Week 6) | Partial | CI still targets 70%; coverage gaps remain |
| RAG evaluation (Week 6) | Not started | Add precision/recall benchmark suite for retrieval quality |

#### Code-Level Debt

| Issue | Severity | Location |
| --- | --- | --- |
| `tools/` modernization only 30% done | Medium | ~70% of `tools/` still uses `List[str]`, `Optional`, or lacks proper type hints |
| 4 oversized files remain (>800 lines) | Medium | `server/datasets.py`, `server/evaluation_scoring.py`, `langchain/graph.py`, `models/smart_router.py` |
| `smart_router.py` circuit breaker is a stub | Low | Returns hardcoded fallback, no real failure tracking |
| Coverage gate still at 70% | Low | `pyproject.toml` pytest config |
| Prompt injection defense in RAG is incomplete | Low | Delimiter framing exists, but no input sanitization layer |
| 3 pre-existing test failures | Low | Known, not currently regressing |

### Strengths

- **Protocol-first design:** Core abstractions such as `ExecutionEngine`, `AgentProtocol`, and `ToolProtocol` use `@runtime_checkable` protocols, making the system genuinely pluggable.
- **RAG pipeline maturity:** 13 modules, ~92% coverage, hybrid retrieval, content-hash dedup, token-budget assembly, and OTEL tracing indicate production-grade work.
- **Adapter registry:** A thread-safe singleton provides clean native and LangChain backends, making new engine support a straightforward registration problem.
- **ADR discipline:** Validation work caught fabricated citations in ADR-010, ADR-011, and ADR-012 and corrected them, which is unusually strong process hygiene.

> **Insight**  
> The dual execution-engine pattern, native DAG plus LangChain adapter, is a strong architectural hedge. The native engine offers deterministic execution ordering, error handling, and auditability, while the LangChain path opens access to more dynamic agent patterns. Keeping both behind the `ExecutionEngine` protocol lets workflow authors stay decoupled from the runtime choice.

### Future Changes and Next Steps

#### Immediate (Next Sprint)

1. Raise the coverage gate from 70% to 80% in `pyproject.toml` and close the most important test gaps.
2. Continue modernizing `tools/` with PEP 604 typing, structured logging, and stronger error handling.
3. Split remaining oversized files, especially `datasets.py`, `evaluation_scoring.py`, `graph.py`, and `smart_router.py`.

#### Near-Term (2-4 Weeks)

4. Implement reranking by inserting `CrossEncoderReranker` after `HybridRetriever`, using the existing retrieval protocol as the integration seam.
5. Wire the reflection loop into the DAG engine by adding an `iterate` step type with `max_iterations` and convergence predicates.
6. Build a RAG evaluation benchmark using synthetic Q&A pairs and known-good retrieval results.

#### Medium-Term (1-2 Months)

7. Complete a full `tools/` package audit and bring the remaining modules up to the bar already set by `tools/core/` and `tools/llm/`.
8. Harden the smart router by replacing the circuit-breaker stub with real failure tracking, exponential backoff, and provider health scoring.
9. Add a dedicated prompt-injection defense layer at the RAG query boundary instead of relying only on system-prompt delimiter framing.

---

## Summary Comparison

| Dimension | Presentation | Non-Presentation |
| --- | --- | --- |
| Architecture | Monolithic, needs decomposition | Protocol-first, structurally strong |
| Modularity | Poor, with 55-65% duplication | Good, improving steadily |
| Config-driven support | No config layer exists | YAML workflows and env-based routing already present |
| Test coverage | 1 Playwright validator | ~92% in RAG, 70% overall |
| Biggest gap | Content and theme extraction | Reranking and reflection loop |
| Effort to next milestone | ~2-3 sprints for MVP | ~1 sprint |
