import React from "react";
import { HbChapterLayout } from "../../layouts/handbook/HbChapterLayout.tsx";

export default {
  title: "Layouts/Handbook/HbChapterLayout",
  component: HbChapterLayout,
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
  eyebrow: "Onboarding Handbook",
  num: "01",
  title: "Welcome to the Team",
  subtitle: "Everything you need to hit the ground running on day one",
  summary:
    "This handbook covers the essential knowledge, tools, and workflows you will use daily. Each chapter builds on the last, guiding you from environment setup through your first production contribution.",
  heroPoints: [
    "Set up your local development environment in under 30 minutes",
    "Understand the monorepo structure and package boundaries",
    "Learn the review and merge workflow before your first commit",
    "Know where to find help when you get stuck",
  ],
  chapters: [
    { num: "01", title: "Environment Setup", sub: "Toolchain, IDE, and local dev configuration" },
    { num: "02", title: "Repo Architecture", sub: "Monorepo layout, packages, and dependency graph" },
    { num: "03", title: "Coding Standards", sub: "Style guides, linting, and type checking" },
    { num: "04", title: "Git Workflow", sub: "Branching model, PR templates, and CI gates" },
    { num: "05", title: "Testing Strategy", sub: "Unit, integration, and E2E test expectations" },
    { num: "06", title: "Deployment Pipeline", sub: "Build, stage, and release process overview" },
  ],
  callout: "A well-onboarded engineer ships confidently within their first sprint.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
