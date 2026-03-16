import React from "react";
import { StatHeroLayout } from "../../layouts/verge-pop/StatHeroLayout.tsx";

export default {
  title: "Layouts/Verge Pop/StatHeroLayout",
  component: StatHeroLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "demo",
  title: "Your First 90 Days",
  subtitle:
    "Key milestones and metrics that define a successful onboarding journey from day one through full ramp-up.",
  color: "#8B5CF6",
  colorLight: "#A78BFA",
  colorGlow: "rgba(139,92,246,0.3)",
  icon: "\u25CE",
  question:
    "What does a high-performing new hire accomplish in their first quarter?",
  statItems: [
    {
      label: "Week 1",
      val: "5",
      bgColor: "#A78BFA",
      bullets: [
        "Complete security onboarding",
        "Set up dev environment",
        "First commit to codebase",
        "Meet your team lead",
        "Review architecture docs",
      ],
    },
    {
      label: "Week 4",
      val: "80%",
      bgColor: "#F59E0B",
      bullets: [
        "Pass coding standards review",
        "Ship first feature to staging",
        "Complete compliance training",
      ],
    },
    {
      label: "Week 12",
      val: "3x",
      bgColor: "#10B981",
      bullets: [
        "Velocity matches team average",
        "Lead your first sprint demo",
        "Mentor incoming hire",
      ],
    },
  ],
  callout:
    "Structured onboarding reduces time-to-productivity by 40% compared to ad-hoc ramp-up.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
