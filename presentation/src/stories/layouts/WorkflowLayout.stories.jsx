import React from "react";
import { WorkflowLayout } from "../../layouts/onboarding/WorkflowLayout.tsx";

export default {
  title: "Layouts/Onboarding/WorkflowLayout",
  component: WorkflowLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "ai-code-review-workflow",
  title: "AI-Assisted Code Review",
  subtitle: "How Every Pull Request Moves from Draft to Merge",
  color: "#7C3AED",
  colorLight: "#A78BFA",
  colorGlow: "rgba(124,58,237,0.3)",
  icon: "🔍",
  order: "04",
  steps: [
    {
      num: "01",
      type: "ai",
      title: "Context-Enriched Prompt Assembly",
      body: "Architecture docs, coding standards, and the relevant module's existing patterns are injected into the prompt before any generation request is made.",
      tip: "Always include the CLAUDE.md and the target module's __init__.py in the context window for best results.",
    },
    {
      num: "02",
      type: "ai",
      title: "AI Draft Generation",
      body: "The model produces an initial implementation — functions, tests, and docstrings — based on the enriched context and the developer's intent statement.",
      tip: "Keep intent statements under 3 sentences. Specificity outperforms length.",
    },
    {
      num: "03",
      type: "human",
      title: "Developer Review Pass",
      body: "The developer reads every line of AI output for correctness, security implications, and alignment with the architecture. No blind acceptance.",
      tip: "Use the diff view. Read it the same way you would a junior engineer's first PR.",
    },
    {
      num: "04",
      type: "ai",
      title: "Automated Lint, Type Check & Tests",
      body: "Pre-commit hooks run black, isort, ruff, mypy --strict, and the full pytest suite. All checks must pass before the PR is opened.",
      tip: "If mypy fails, fix the types — do not add type: ignore comments unless there is a documented reason.",
    },
    {
      num: "05",
      type: "human",
      title: "Peer Code Review",
      body: "A second engineer reviews the PR for logic correctness, edge cases, error handling, and security. At least one approval is required to merge.",
      tip: "Focus on the why, not the what. Black and Ruff own formatting — you own correctness.",
    },
    {
      num: "06",
      type: "human",
      title: "Merge Gate & CI Validation",
      body: "The merge button is gated on all CI checks passing: lint, type check, full test suite, and coverage threshold of 80%+.",
      tip: "A single failing check blocks the merge. No exceptions, no manual overrides.",
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
