import React from "react";
import { BeforeAfterLayout } from "../../layouts/base/BeforeAfterLayout.tsx";

export default {
  title: "Layouts/Base/BeforeAfterLayout",
  component: BeforeAfterLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "before-after-onboarding",
  title: "Onboarding Hurdles — Solved",
  subtitle:
    "The four friction points that slow down new hires, and exactly how we addressed each one.",
  color: "#0891B2",
  colorLight: "#22D3EE",
  colorGlow: "rgba(8,145,178,0.3)",
  icon: "🎯",
  cards: [
    {
      title: "Environment Setup",
      challenge:
        "New hires spent an average of three days configuring local tooling, chasing down credentials, and resolving version conflicts before writing a single line of code.",
      fix: "Automated setup script provisions the full dev environment in under 20 minutes. A one-page quickstart covers the three manual steps that cannot be automated.",
    },
    {
      title: "Codebase Orientation",
      challenge:
        "The monorepo had grown to over 40,000 lines across five packages with no consistent entry-point documentation, leaving new engineers unsure where to start reading.",
      fix: "CLAUDE.md and ARCHITECTURE.md now provide a structured tour of every package, key patterns, and where to find canonical examples for each concern.",
    },
    {
      title: "First Ticket Paralysis",
      challenge:
        "Without explicit guidance on scope, new hires either under-reached (trivial typo fixes) or over-reached (refactoring existing modules) on their first assigned tasks.",
      fix: "A curated 'first-ticket' backlog is maintained for each sprint. Each ticket is scoped to one file, has acceptance criteria, and links to the relevant architecture section.",
    },
    {
      title: "Review Feedback Whiplash",
      challenge:
        "Inconsistent code review standards across the team meant new hires received contradictory feedback, eroding confidence and slowing their ability to internalize norms.",
      fix: "Coding standards are codified in CODING_STANDARDS.md and enforced by pre-commit hooks. Reviewers focus on logic and correctness, not style — the linter handles style.",
    },
  ],
  callout: "Every hurdle we document is a hurdle the next hire does not face alone.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
