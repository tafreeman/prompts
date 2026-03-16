import React from "react";
import { AdvdHurdlesLayout } from "../../layouts/advocacy-dense/AdvdHurdlesLayout.tsx";

export default {
  title: "Layouts/Advocacy Dense/AdvdHurdlesLayout",
  component: AdvdHurdlesLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "advd-hurdles",
  title: "Onboarding Friction — Identified and Fixed",
  subtitle:
    "The six most common blockers new hires reported, each with a documented resolution.",
  color: "#0891B2",
  colorLight: "#22D3EE",
  colorGlow: "rgba(8,145,178,0.3)",
  icon: "🎯",
  cards: [
    {
      title: "Environment Setup Takes Days",
      labels: ["Tooling", "Credentials", "Week 1"],
      challenge:
        "Manual credential provisioning and undocumented version dependencies consumed an average of 2.8 days before a hire could run the test suite.",
      fix: "Automated setup script with idempotent steps. Single-command bootstrap covers all dependencies, credentials, and IDE config in under 20 minutes.",
    },
    {
      title: "No Clear Starting Point in the Codebase",
      labels: ["Documentation", "Architecture"],
      challenge:
        "A 40,000-line monorepo with five packages and no canonical entry-point guide left new engineers unsure where to begin reading.",
      fix: "CLAUDE.md and ARCHITECTURE.md provide a structured tour. Each package has a one-paragraph purpose statement and a pointer to the canonical example for its core concern.",
    },
    {
      title: "Ambiguous First-Ticket Scope",
      labels: ["Backlog", "Ramp-Up"],
      challenge:
        "Without explicit scope guidance, first tickets were either trivially small (no learning) or dangerously large (blocked, frustrated, discouraged).",
      fix: "Curated first-ticket backlog maintained by the tech lead each sprint. Every ticket is scoped to one file, has acceptance criteria, and links to the relevant docs section.",
    },
    {
      title: "Contradictory Code Review Feedback",
      labels: ["Standards", "Culture"],
      challenge:
        "Inconsistent reviewer expectations caused new hires to receive conflicting style feedback, eroding confidence and slowing internalization of team norms.",
      fix: "CODING_STANDARDS.md codifies all style rules. Pre-commit hooks enforce formatting automatically. Reviewers are explicitly chartered to focus on logic and correctness only.",
    },
    {
      title: "Invisible Progress",
      labels: ["Visibility", "Manager"],
      challenge:
        "Neither the hire nor the manager had a shared view of where the new engineer stood in the onboarding plan, making check-ins unstructured and unproductive.",
      fix: "Shared progress tracker updated by the hire daily. Manager dashboard surfaces blockers and milestone status in real time without requiring status emails.",
    },
    {
      title: "Buddy Commitment Not Enforced",
      labels: ["Buddy Program", "Culture"],
      challenge:
        "Buddy assignments existed on paper but were not tracked, resulting in some new hires receiving no meaningful support during their first two weeks.",
      fix: "Buddy availability and responsiveness is tracked in the onboarding dashboard. Buddy commitment is included in quarterly goal-setting as a named responsibility.",
    },
  ],
  callout:
    "Every friction point we document is one fewer obstacle for the next hire who joins the team.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
