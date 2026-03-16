import React from "react";
import { HbManifestoLayout } from "../../layouts/handbook/HbManifestoLayout.tsx";

export default {
  title: "Layouts/Handbook/HbManifestoLayout",
  component: HbManifestoLayout,
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
  eyebrow: "Team Manifesto",
  title: "What We Stand For",
  statement:
    "We build software\nthat earns trust\nthrough evidence.",
  beliefs: [
    "Every architectural claim is backed by commit history and test results, not slides.",
    "AI accelerates our work but never replaces our judgment or accountability.",
    "Quality is not a phase \u2014 it is woven into every step from intake to deploy.",
    "We ship small, validate fast, and compound improvements across sprints.",
    "Security and compliance are first-class concerns, not afterthoughts.",
    "Onboarding is a team responsibility \u2014 the handbook is everyone's code to maintain.",
  ],
  callout:
    "This manifesto is a living document. When our practices evolve, this page evolves with them.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
