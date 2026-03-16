import React from "react";
import { InfoCardsLayout } from "../../layouts/onboarding/InfoCardsLayout.tsx";

export default {
  title: "Layouts/InfoCardsLayout",
  component: InfoCardsLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "demo",
  title: "Human in the Loop",
  subtitle: "AI Accelerates. Humans Govern.",
  color: "#0891B2",
  colorLight: "#22D3EE",
  colorGlow: "rgba(8,145,178,0.3)",
  banner: "Every line of AI-assisted code passes through structured review.",
  cards: [
    {
      title: "Gated Review",
      body: "Structured PR reviews with checklists ensure every change meets quality bars before merge.",
      stat: "100%",
      statLabel: "Human-Reviewed",
    },
    {
      title: "Context Prompts",
      body: "Templates enriched with architecture docs and coding standards produce higher-quality AI output.",
      stat: "~90%",
      statLabel: "AI-Assisted",
    },
    {
      title: "Zero Defects",
      body: "Disciplined governance and review gates resulted in zero critical defects across all sprints.",
      stat: "0",
      statLabel: "Critical Defects",
    },
  ],
  callout: "AI generated the code. Humans owned every decision.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
