import React from "react";
import { QuoteCollageLayout } from "../../layouts/verge-pop/QuoteCollageLayout.tsx";

export default {
  title: "Layouts/Verge Pop/QuoteCollageLayout",
  component: QuoteCollageLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "demo",
  title: "What New Hires Are Saying",
  subtitle:
    "Real feedback from engineers who completed our structured onboarding program in the last two quarters.",
  color: "#8B5CF6",
  colorLight: "#A78BFA",
  colorGlow: "rgba(139,92,246,0.3)",
  icon: "\u25CE",
  quotes: [
    {
      text: "The dev environment setup guide saved me two full days compared to my last job.",
      bgColor: "#A78BFA",
    },
    {
      text: "Pair programming in week one made me feel like part of the team immediately.",
      bgColor: "#F59E0B",
    },
    {
      text: "Having a mentor assigned on day one was the single biggest accelerator.",
      bgColor: "#34D399",
    },
    {
      text: "The architecture walkthrough gave me context I would have spent months piecing together.",
      bgColor: "#FB923C",
    },
    {
      text: "I shipped my first PR in three days. That confidence boost was huge.",
      bgColor: "#60A5FA",
    },
    {
      text: "Compliance training was baked into the flow instead of being a separate burden.",
      bgColor: "#F472B6",
    },
  ],
  centerLabel: "Voices from the team",
  callout:
    "Teams with structured onboarding see 25% higher retention in the first year.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
