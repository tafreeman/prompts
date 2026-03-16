import React from "react";
import { AdvdOverviewLayout } from "../../layouts/advocacy-dense/AdvdOverviewLayout.tsx";

export default {
  title: "Layouts/Advocacy Dense/AdvdOverviewLayout",
  component: AdvdOverviewLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "advd-overview",
  eyebrow: "New Hire Onboarding",
  title: "Onboarding at Speed and Scale",
  subtitle:
    "A structured, AI-assisted 90-day program that gets engineers contributing faster without sacrificing quality or culture.",
  color: "#0891B2",
  colorLight: "#22D3EE",
  colorGlow: "rgba(8,145,178,0.3)",
  icon: "🎯",
  heroPoints: [
    "90-Day Ramp Plan",
    "Automated Setup",
    "Curated First Tickets",
    "Buddy Program",
    "Zero Guesswork",
  ],
  summary:
    "Every step is documented, every milestone is tracked, and every friction point has an owner. New hires arrive to a program that is ready for them — not the other way around.",
  cards: [
    {
      title: "Multi-Lane Process",
      body: "Engineer, Manager, and Team lanes run in parallel with clear ownership at each step.",
    },
    {
      title: "Automated Provisioning",
      body: "Dev environment and credentials fully configured in under 20 minutes via setup script.",
    },
    {
      title: "First-Ticket Backlog",
      body: "Curated per sprint — scoped, documented, and linked to the relevant architecture section.",
    },
    {
      title: "Day-90 Retrospective",
      body: "Formal sign-off milestone with structured feedback flowing back into program improvement.",
    },
  ],
  callout: "Onboarding is a system, not an event.",
  allTopics: [
    { title: "Overview", color: "#0891B2" },
    { title: "Metrics", color: "#10B981" },
    { title: "Hurdles", color: "#F59E0B" },
    { title: "Future State", color: "#8B5CF6" },
    { title: "Platform", color: "#EC4899" },
  ],
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
