import React from "react";
import { HbIndexLayout } from "../../layouts/handbook/HbIndexLayout.tsx";

export default {
  title: "Layouts/Handbook/HbIndexLayout",
  component: HbIndexLayout,
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
  eyebrow: "Quick Reference",
  num: "IX",
  title: "Handbook Index",
  subtitle: "Jump to any section of the onboarding handbook",
  categories: [
    {
      label: "Environment & Tooling",
      body: "Local dev setup, IDE configuration, shell environment, and required CLI tools for day-one productivity.",
    },
    {
      label: "Architecture & Patterns",
      body: "Monorepo structure, adapter registry, dual execution engines, and the protocol-first design philosophy.",
    },
    {
      label: "Coding Standards",
      body: "Naming conventions, immutability rules, error handling hierarchy, and automated formatting enforcement.",
    },
    {
      label: "Testing & Quality",
      body: "TDD workflow, coverage gates, pytest-asyncio patterns, and the antagonistic review process.",
    },
    {
      label: "Security & Compliance",
      body: "Secret management, input validation, rate limiting, and audit logging for cleared federal environments.",
    },
    {
      label: "Deployment & Operations",
      body: "CI pipeline stages, Docker containerization, feature flags, and production monitoring dashboards.",
    },
  ],
  callout: "If you can't find it in the index, it probably needs to be written. Open a PR.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
