# Comparison matrix — 2026-02-03

This matrix summarizes top-level patterns and folder-layout signals from 10 representative repos I fetched (README / top-level pages). Use this to inform the `prompts/` modularization.

| Repo | Primary language(s) | Notable top-level folders / files | Key patterns (templates / evals / metrics / agents) |
|---|---:|---|---|
| EleutherAI/lm-evaluation-harness | Python | `docs/`, `examples/`, `lm_eval/`, `scripts/`, `templates/`, `tests/` | CLI + YAML configs, backend adapters (hf/vllm/api), caching, results logging; eval-first harness. |
| openai/evals | Python, notebooks | `evals/`, `examples/`, `docs/`, `scripts/` | Registry of YAML evals, Git-LFS for large eval data, runner CLI, strong docs for writing evals. |
| openai/openai-cookbook | Jupyter notebooks, MDX | `articles/`, `examples/`, `images/`, `AGENTS.md` | Cookbook-style runnable examples and notebooks; good demo patterns for docs + examples. |
| bigscience-workshop/promptsource | Python | `promptsource/`, `assets/`, `test/`, `promptsource/app.py` | Prompt templates stored as standalone files (Jinja), Streamlit GUI, dataset integration; separate prompt catalog. |
| huggingface/evaluate | Python | `metrics/`, `measurements/`, `comparisons/`, `docs/` | Metrics-as-components, CLI to create/publish metrics, hub integration for community metrics. |
| huggingface/transformers | Python | `src/transformers/`, `examples/`, `docs/`, `notebooks/` | High-level pipeline abstraction, many examples and extension points; central model-definition framework. |
| langchain-ai/langchain | Python | `libs/`, `.github/`, `docs/`, `AGENTS.md` | SDK-style modular components (chains/agents/tools), heavy integration surface and observability patterns. |
| thunlp/OpenPrompt | Python | `openprompt/`, `tutorial/`, `datasets/`, `scripts/` | Prompt-learning primitives (Template/Verbalizer/PromptModel), tutorials; templates & training code separated. |
| microsoft/semantic-kernel | C#, Python, .NET | `python/`, `dotnet/`, `prompt_template_samples/`, `docs/` | SDK for agents/multi-agent orchestration, plugin/plugin samples, cross-language SDK design. |
| microsoft/autogen | Python, C# | `python/`, `dotnet/`, `docs/`, `packages/` | Multi-agent framework (layered packages), studio & bench tools, packaged subprojects and clear package boundaries. |

Observations & actionable signals

- Common signals for modularization:
  - `templates/` or `promptsource`-style stores for prompt templates (separate, editable files).
  - `evaluations/` or `evals/` registries declared as YAML configs + a small runner/CLI.
  - `metrics/` or `metrics/`-like packages that wrap compute logic and can be published or reused.
  - `agents/` or `packages/` for SDK-like wrappers and orchestration logic.
- CI practice: add a lightweight smoke-eval in PR workflows rather than run large evals.
- Data policy: use Git-LFS for eval data/artifacts and avoid committing sensitive datasets.

Files created in this step

- `docs/planning/RESEARCH_COMPARISON_MATRIX_2026-02-03.md` — this file (comparison matrix).

Next steps

- I can parse deeper (read specific README sections, `tree` outputs, or example YAML files) for 8–12 repos and add file excerpts into the expanded dump (if you want full excerpts). Estimated additional time: 30–90 minutes depending on depth.
- Or I can open a POC PR (move one YAML+runner into `evaluations/`) — confirm which you'd prefer.
