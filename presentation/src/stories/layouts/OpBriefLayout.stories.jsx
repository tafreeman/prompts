import React from "react";
import { OpBriefLayout } from "../../layouts/onboarding/OpBriefLayout.tsx";

export default {
  title: "Layouts/Onboarding/OpBriefLayout",
  component: OpBriefLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "human-in-the-loop-brief",
  title: "Human in the Loop",
  subtitle: "AI Accelerates. Humans Govern.",
  headline: "A structured governance model that pairs AI code generation with mandatory human review gates at every stage of the development lifecycle.",
  color: "#0891B2",
  colorLight: "#22D3EE",
  colorGlow: "rgba(8,145,178,0.3)",
  icon: "🧑‍✈️",
  order: "01",
  cards: [
    {
      stat: "100%",
      statLabel: "Human-Reviewed",
      title: "Gated Pull Request Review",
      body: "Every PR requires at least one peer approval plus full CI passage before merge. AI-generated code receives no special bypass.",
    },
    {
      stat: "~90%",
      statLabel: "AI-Assisted",
      title: "Context-Enriched Generation",
      body: "Architecture docs, coding standards, and module conventions are injected into prompts before generation, raising output fidelity significantly.",
    },
    {
      stat: "0",
      statLabel: "Critical Defects",
      title: "Zero Critical Defects Shipped",
      body: "Twelve sprints of AI-assisted development with mandatory review gates produced zero critical defects in the production codebase.",
    },
    {
      stat: "80%+",
      statLabel: "Coverage Gate",
      title: "Enforced Coverage Threshold",
      body: "CI blocks merge if test coverage drops below 80%. Coverage is a hard gate, not an aspirational metric.",
    },
  ],
  callout: "AI generated the code. Humans owned every decision. That distinction is what makes this model viable in a federal environment.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
