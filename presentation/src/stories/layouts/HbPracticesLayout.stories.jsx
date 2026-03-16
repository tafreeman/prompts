import React from "react";
import { HbPracticesLayout } from "../../layouts/handbook/HbPracticesLayout.tsx";

export default {
  title: "Layouts/Handbook/HbPracticesLayout",
  component: HbPracticesLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "demo",
  color: "#0891B2",
  colorLight: "#22D3EE",
  colorGlow: "rgba(8,145,178,0.3)",
  icon: "\uD83D\uDCD8",
  eyebrow: "Engineering Practices",
  num: "03",
  title: "How We Build Software",
  subtitle: "Core practices that keep quality high and velocity sustainable",
  summary:
    "These six practices form the foundation of our engineering culture. They are not aspirational guidelines \u2014 they are daily habits enforced through tooling, CI gates, and peer review. Every new team member is expected to internalize them within their first two sprints.",
  practices: [
    {
      title: "Test-Driven Development",
      body: "Write the test first. Watch it fail. Write the minimal code to pass. Refactor. This is not optional \u2014 it is how we catch regressions before they reach production.",
    },
    {
      title: "Immutable Data Patterns",
      body: "Never mutate state in place. Create new objects with changes applied. This eliminates an entire class of concurrency and debugging issues.",
      dark: true,
    },
    {
      title: "Structured Error Handling",
      body: "No bare except clauses. Custom exception hierarchies. Every error boundary maps to an HTTP status code at the API layer.",
    },
    {
      title: "Pydantic Contracts",
      body: "All API inputs, configs, and pipeline interfaces use Pydantic v2 models. Additive-only schema evolution \u2014 never break downstream consumers.",
      highlight: true,
    },
    {
      title: "Automated Code Quality",
      body: "Black, isort, Ruff, and mypy run on every commit via pre-commit hooks. A single lint failure blocks the merge. Humans review logic, machines review style.",
    },
    {
      title: "Security by Default",
      body: "No hardcoded secrets. Input validation at every boundary. Rate limiting on all endpoints. Treat AI-generated code as untrusted input.",
      dark: true,
    },
  ],
  callout: "Practices without enforcement are just wishes. We enforce with tooling.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
