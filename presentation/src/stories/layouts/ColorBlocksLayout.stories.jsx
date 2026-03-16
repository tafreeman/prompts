import React from "react";
import { ColorBlocksLayout } from "../../layouts/verge-pop/ColorBlocksLayout.tsx";

export default {
  title: "Layouts/Verge Pop/ColorBlocksLayout",
  component: ColorBlocksLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "demo",
  title: "Onboarding Task Ownership",
  subtitle:
    "Who handles each phase of onboarding \u2014 people alone, AI-assisted, or fully automated.",
  color: "#8B5CF6",
  colorLight: "#A78BFA",
  colorGlow: "rgba(139,92,246,0.3)",
  icon: "\u25CE",
  blocks: [
    {
      area: "left",
      bgColor: "#A78BFA",
      stat: {
        val: "62%",
        label:
          "of onboarding tasks can be partially or fully automated with AI tooling",
      },
    },
    {
      area: "top-right",
      bgColor: "#F59E0B",
      text: "Mentorship, culture fit, and security interviews remain human-led. AI handles environment provisioning, documentation walkthroughs, and compliance checklists.",
    },
    {
      area: "bottom-right",
      bgColor: "#F0FDF4",
      chartBars: [
        { label: "Env Setup", peopleOnly: 10, mixed: 30, aiOnly: 60 },
        { label: "Security", peopleOnly: 80, mixed: 15, aiOnly: 5 },
        { label: "Code Review", peopleOnly: 40, mixed: 50, aiOnly: 10 },
        { label: "Compliance", peopleOnly: 20, mixed: 35, aiOnly: 45 },
        { label: "Mentoring", peopleOnly: 85, mixed: 15, aiOnly: 0 },
        { label: "Doc Review", peopleOnly: 15, mixed: 25, aiOnly: 60 },
      ],
    },
  ],
  callout:
    "Automate the repeatable. Invest human time where judgment and relationships matter most.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
