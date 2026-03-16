import React from "react";
import { BarChartLayout } from "../../layouts/verge-pop/BarChartLayout.tsx";

export default {
  title: "Layouts/Verge Pop/BarChartLayout",
  component: BarChartLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "demo",
  title: "Onboarding Completion Rates",
  subtitle:
    "Tracking how new hires progress through each onboarding phase across recent cohorts.",
  color: "#8B5CF6",
  colorLight: "#A78BFA",
  colorGlow: "rgba(139,92,246,0.3)",
  icon: "\u25CE",
  barGroups: [
    {
      groupLabel: "Technical Readiness",
      color: "#8B5CF6",
      bars: [
        { label: "Dev environment setup", value: 98 },
        { label: "Security clearance", value: 95 },
        { label: "First commit merged", value: 92 },
        { label: "CI/CD pipeline access", value: 88 },
        { label: "Architecture review", value: 76 },
      ],
    },
    {
      groupLabel: "Team Integration",
      color: "#10B981",
      bars: [
        { label: "Mentor pairing", value: 100 },
        { label: "Sprint participation", value: 94 },
        { label: "Code review given", value: 85 },
        { label: "Sprint demo led", value: 68 },
        { label: "Cross-team collab", value: 52 },
      ],
    },
  ],
  callout:
    "Technical readiness outpaces team integration \u2014 invest early in collaboration rituals.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
