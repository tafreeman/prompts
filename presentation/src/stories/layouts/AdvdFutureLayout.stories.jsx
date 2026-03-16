import React from "react";
import { AdvdFutureLayout } from "../../layouts/advocacy-dense/AdvdFutureLayout.tsx";

export default {
  title: "Layouts/Advocacy Dense/AdvdFutureLayout",
  component: AdvdFutureLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "advd-future",
  title: "The Next Generation of Onboarding",
  subtitle:
    "Five capabilities that will define how high-performing teams ramp new engineers in the next two years.",
  color: "#0891B2",
  colorLight: "#22D3EE",
  colorGlow: "rgba(8,145,178,0.3)",
  icon: "🎯",
  pullQuote:
    "The best onboarding experience feels less like a program and more like having a senior engineer available at any moment.",
  cards: [
    {
      eyebrow: "AI Assistance",
      title: "Context-Aware AI Buddy",
      body: "An AI assistant pre-loaded with team ADRs, codebase structure, and coding standards answers 'why' questions instantly — without interrupting senior engineers.",
    },
    {
      eyebrow: "Adaptive Planning",
      title: "Dynamic 90-Day Plans",
      body: "Milestone timelines adjust in real time based on actual progress. Hires who move fast are accelerated; those who are blocked get support triggered automatically.",
    },
    {
      eyebrow: "Knowledge Graph",
      title: "Team Expertise Map",
      body: "A lightweight graph surfaces who owns what across the codebase. New hires find the right person to ask without navigating org charts or Slack history.",
    },
    {
      eyebrow: "Analytics",
      title: "Cohort-Level Insights",
      body: "Aggregated, anonymized metrics surface systemic friction before it appears in attrition data. Program gaps are fixed within the same cohort they are discovered.",
    },
    {
      eyebrow: "Integration",
      title: "Embedded in the Workflow",
      body: "Onboarding tasks appear directly in the sprint board. There is no separate system to check — progress is tracked where the work happens.",
    },
  ],
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
