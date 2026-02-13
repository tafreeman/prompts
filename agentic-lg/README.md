# agentic-lg

**LangGraph-Native Agentic Workflows** — YAML-driven agents and workflows with loops, HITL, evaluation gates, and a modern React UI.

## Architecture

```
agentic-lg/
├── packages/
│   ├── core/        # Python: YAML compiler, agents, server
│   └── ui/          # React: DAG visualization, analytics
└── definitions/     # User-facing YAML workflows + agents
```

## Quick Start

```bash
# Backend
cd packages/core
pip install -e ".[dev]"
python -m agentic_lg.server

# Frontend
cd packages/ui
npm install && npm run dev
```

## Key Features

- **YAML-Driven**: Define workflows and agents entirely in YAML
- **LangGraph Runtime**: Battle-tested graph execution with automatic checkpointing
- **Loops & Iteration**: Conditional back-edges for retry/refinement cycles
- **HITL**: Pause workflows for human approval, resume from checkpoint
- **Evaluation Gates**: In-graph quality gates with LLM judge scoring
- **Modern UI**: React Flow graph + D3.js analytics + real-time SSE streaming
