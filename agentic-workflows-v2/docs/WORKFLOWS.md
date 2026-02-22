# Workflows

This document describes built-in workflow definitions in `agentic_v2/workflows/definitions` and how to add new ones.

## Built-In Definitions

| Workflow | Purpose | Typical inputs |
| --- | --- | --- |
| `code_review` | Automated multi-step code review | `code_file`, `review_depth` |
| `bug_resolution` | Triage, root-cause, fix, and verification | `bug_report`, `code_file`, `resolution_depth` |
| `deep_research` | Iterative research with confidence gating | `topic`, `goal`, `max_rounds`, `min_ci` |
| `fullstack_generation` | Parallel feature generation across backend/frontend | `feature_spec`, `tech_stack` |
| `fullstack_generation_bounded_rereview` | Fullstack generation with bounded re-review loop | `feature_spec`, `tech_stack` |
| `multi_agent_codegen_e2e` | End-to-end multi-agent generation with quality gates | `feature_spec`, `repo_context`, `constraints` |
| `multi_agent_codegen_e2e_single_loop` | Single bounded QA loop variant | `feature_spec`, `repo_context`, `constraints` |
| `tdd_codegen_e2e` | Test-first generation and gated implementation | `feature_spec`, `repo_context`, `constraints` |
| `test_deterministic` | Deterministic no-LLM smoke workflow | `input_text` |
| `plan_implementation` | Legacy experimental iterative orchestration spec | plan and architecture docs |

## Workflow Structure

Each workflow is YAML with:
- Metadata (`name`, `description`, `version`)
- Capabilities (`inputs`, `outputs`)
- Input schema
- Step DAG (`steps` with `depends_on`, `when`, `inputs`, `outputs`)
- Optional evaluation rubric/profile metadata

## Run a Workflow

```bash
agentic validate code_review
agentic run code_review --dry-run
agentic run code_review --input input.json --output output.json
```

## Authoring Guidelines

- Keep step names explicit and stable.
- Use `depends_on` for deterministic execution order.
- Keep expressions (`${...}`) readable and minimal.
- Prefer explicit step outputs over large implicit context.
- Add evaluation criteria for production-facing workflows.

## Adding a New Workflow

1. Add a YAML file in `agentic_v2/workflows/definitions/`.
2. Define clear `inputs` and `outputs`.
3. Ensure graph validity with `agentic validate <workflow>`.
4. Add tests in `tests/test_workflow_loader.py` and relevant integration tests.
5. Document the new workflow in this file and `README.md`.
