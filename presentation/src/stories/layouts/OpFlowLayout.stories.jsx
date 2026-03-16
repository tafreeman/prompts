import React from "react";
import { OpFlowLayout } from "../../layouts/onboarding/OpFlowLayout.tsx";

export default {
  title: "Layouts/Onboarding/OpFlowLayout",
  component: OpFlowLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "ai-review-op-flow",
  title: "AI-Assisted Review Workflow",
  subtitle: "One-Pager: From Prompt to Merged PR",
  subheadline: "A repeatable six-step process that integrates AI code generation with structured human review gates, automated quality checks, and peer approval before any change reaches the main branch.",
  color: "#7C3AED",
  colorLight: "#A78BFA",
  colorGlow: "rgba(124,58,237,0.3)",
  icon: "🔁",
  order: "04",
  steps: [
    {
      num: "01",
      type: "ai",
      title: "Context Assembly",
      body: "Architecture docs, coding standards, and the target module's existing patterns are bundled into the prompt context before any generation request is issued.",
      tip: "Include CLAUDE.md and the module's __init__.py for highest-fidelity output.",
    },
    {
      num: "02",
      type: "ai",
      title: "AI Draft Generation",
      body: "The model produces implementation code, unit tests, and docstrings based on the enriched context and the developer's intent statement.",
      tip: "Keep intent statements under 3 sentences — specificity beats length.",
    },
    {
      num: "03",
      type: "human",
      title: "Developer Review Pass",
      body: "The developer reads every line of AI output for correctness, security implications, and architectural alignment. No blind acceptance permitted.",
      tip: "Read the diff as you would a junior engineer's first PR.",
    },
    {
      num: "04",
      type: "ai",
      title: "Automated Quality Gates",
      body: "Pre-commit hooks execute black, isort, ruff, mypy --strict, and the full pytest suite. Every check must pass before the PR is opened.",
      tip: "Fix the types — do not add type: ignore without a documented reason.",
    },
    {
      num: "05",
      type: "human",
      title: "Peer Code Review",
      body: "A second engineer reviews for logic correctness, edge cases, error handling, and security. At least one approval is required to merge.",
      tip: "Black and Ruff own formatting — you own correctness and security.",
    },
    {
      num: "06",
      type: "human",
      title: "CI Gate & Merge",
      body: "The merge button is gated on all CI checks passing: lint, type check, full test suite, and 80%+ coverage. No manual overrides.",
      tip: "A single failing check blocks the merge. No exceptions.",
    },
  ],
  callout: "Every AI-generated line is reviewed by a human before it ships. The model accelerates — the engineer is accountable.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
