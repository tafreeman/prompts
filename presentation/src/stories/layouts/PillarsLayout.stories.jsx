import React from "react";
import { PillarsLayout } from "../../layouts/onboarding/PillarsLayout.tsx";

export default {
  title: "Layouts/Onboarding/PillarsLayout",
  component: PillarsLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "ai-governance-pillars",
  title: "Five Pillars of AI Governance",
  subtitle: "The Framework Behind Every Engineering Decision",
  color: "#059669",
  colorLight: "#34D399",
  colorGlow: "rgba(5,150,105,0.3)",
  icon: "🏗️",
  order: "03",
  pillars: [
    {
      icon: "🔒",
      title: "Security First",
      items: [
        "All AI-generated code treated as untrusted input",
        "Security reviewer sign-off on auth and crypto changes",
        "No CUI or PII in public model endpoints",
        "Rate limiting on every API boundary",
      ],
    },
    {
      icon: "👁️",
      title: "Human Oversight",
      items: [
        "Every AI output reviewed before commit",
        "Peer review required for all PRs",
        "Architectural decisions require human sign-off",
        "AI cannot override documented ADRs",
      ],
    },
    {
      icon: "📐",
      title: "Standards Adherence",
      items: [
        "Black + Ruff + mypy --strict on every save",
        "80%+ test coverage gate enforced in CI",
        "Pydantic v2 for all boundary validation",
        "No magic numbers — all config externalized",
      ],
    },
    {
      icon: "🔁",
      title: "Reproducibility",
      items: [
        "Every decision backed by ADR with 2+ Tier A sources",
        "Full experiment config committed alongside code",
        "Pinned dependencies, no latest tags",
        "Commit hash + config sufficient to reproduce any run",
      ],
    },
    {
      icon: "📊",
      title: "Measurable Outcomes",
      items: [
        "Coverage thresholds enforced, not aspirational",
        "Zero critical defects across 12 sprints",
        "Antagonistic review at every checkpoint",
        "All claims tied to observable evidence",
      ],
    },
  ],
  results: [
    { val: "1,400+", label: "Tests passing across the platform" },
    { val: "0", label: "Critical defects shipped to production" },
    { val: "~92%", label: "RAG module coverage (gate: 80%)" },
    { val: "12", label: "Sprints completed with governance intact" },
  ],
  callout: "Governance is not overhead — it is the mechanism that makes velocity sustainable in a federal environment.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
