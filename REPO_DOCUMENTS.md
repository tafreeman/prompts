# Repository Document Catalog

This document provides a comprehensive map of the repository structure, key files, and functional domains. It is designed for both human contributors and AI agents (like LangChain) to navigate the codebase effectively.

---

## 🏗️ Core Domains

### 1. Multi-Agent Workflows (`multiagent-workflows/`)

The primary engine for executing complex, multi-stage software engineering tasks.

- **`config/`**: YAML/JSON definitions for agents, workflows, and routing.
- **`src/multiagent_workflows/`**: Implementation of the engine, agents, and evaluators.
- **`langchain/`**: Specialized integration with LangChain and LangGraph.
- **`examples/`**: Run scripts for common workflows (Fullstack, Bug Fixing, etc.).

### 2. Prompt Library (`prompts/`)

A vast collection of industry-standard and advanced prompt patterns.

- **`advanced/`**: Complex patterns like Tree-of-Thoughts, LATS, and CoVE.
- **`agents/`**: Role-based agent definitions.
- **`techniques/`**: Reusable techniques like Reflexion and Chain-of-Thought.
- **`registry.yaml`**: The central index for all metadata-enriched prompts.

### 3. Developer Tools & Evaluation (`tools/`)

Supporting infrastructure for the entire ecosystem.

- **`llm/`**: Unified client for OpenAI, Anthropic, Google, and Local models.
- **`prompteval/`**: Framework for scoring and grading LLM outputs.
- **`benchmarks/`**: Integration with HumanEval, MBPP, and SWE-Bench.

### 4. Knowledge Base (`docs/`)

Conceptual documentation and standards.

- **`concepts/`**: Explanations of prompt anatomy and model capabilities.
- **`instructions/`**: Development standards for different engineering levels.
- **`reference/`**: Glossary and metadata schemas.

---

## 🚦 Key Entry Points

| Purpose | File Path |
|---------|-----------|
| **LangChain Orchestrator** | `multiagent-workflows/src/multiagent_workflows/langchain/orchestrator.py` |
| **Workflow Engine** | `multiagent-workflows/src/multiagent_workflows/core/workflow_engine.py` |
| **Model Manager** | `multiagent-workflows/src/multiagent_workflows/core/model_manager.py` |
| **Workflow Definitions** | `multiagent-workflows/config/workflows.yaml` |
| **Agent Definitions** | `multiagent-workflows/config/agents.yaml` |
| **Unified LLM Client** | `tools/llm/llm_client.py` |

---

## 📝 Document Catalog (Curated)

### Configuration & Orchestration

- `multiagent-workflows/config/models.yaml`: Model routing and fallback logic.
- `multiagent-workflows/config/rubrics.yaml`: Scoring criteria for evaluations.
- `multiagent-workflows/src/multiagent_workflows/langchain/state.py`: State management for LangGraph.

### Agent Prompts

- `multiagent-workflows/config/prompts/architect.md`: System prompt for the Architect role.
- `multiagent-workflows/config/prompts/coder.md`: System prompt for the Developer role.
- `multiagent-workflows/config/prompts/reviewer.md`: System prompt for the Security expert.

### Advanced Research

- `prompts/advanced/tree-of-thoughts-evaluator-reflection.md`: ToT pattern for architecture review.
- `prompts/advanced/lats-full.prompt.txt`: Language Agent Tree Search implementation.

---

## 🤖 For LangChain Agents

The file `REPO_MANIFEST.json` in the root is machine-parseable and provides a full dependency map. You can use this to dynamically load tools or identify the correct system prompts for a given task.
