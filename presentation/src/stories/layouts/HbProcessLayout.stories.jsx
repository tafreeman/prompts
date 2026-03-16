import React from "react";
import { HbProcessLayout } from "../../layouts/handbook/HbProcessLayout.tsx";

export default {
  title: "Layouts/Handbook/HbProcessLayout",
  component: HbProcessLayout,
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
  eyebrow: "Development Process",
  title: "From Idea to Production",
  subtitle: "The eight-step pipeline every feature follows before reaching users",
  steps: [
    {
      num: "01",
      title: "Intake",
      body: "Product owner drafts a feature brief with acceptance criteria. Architect reviews for feasibility and scope.",
    },
    {
      num: "02",
      title: "Planning",
      body: "Planner agent generates an implementation plan. Team reviews dependencies, estimates effort, and assigns ownership.",
    },
    {
      num: "03",
      title: "Design",
      body: "Architect produces ADR with at least two independent Tier A sources. Security reviewer scans for threat model gaps.",
    },
    {
      num: "04",
      title: "Test First",
      body: "TDD guide agent scaffolds failing tests from acceptance criteria. No implementation code exists yet.",
    },
    {
      num: "05",
      title: "Implement",
      body: "Coder writes the minimal code to pass all tests. Immutable patterns, type hints, and structured logging enforced.",
    },
    {
      num: "06",
      title: "Review",
      body: "Code reviewer agent performs automated analysis. Human reviewer approves logic, edge cases, and security posture.",
    },
    {
      num: "07",
      title: "CI Gate",
      body: "Pre-commit hooks run Black, isort, Ruff, and mypy. Pytest suite must pass with 80%+ coverage. Single failure blocks merge.",
    },
    {
      num: "08",
      title: "Deploy",
      body: "Merged code triggers staging build. Smoke tests validate, then promotion to production with feature flag control.",
    },
  ],
  callout: "Every shortcut we skip today becomes a fire drill tomorrow.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
