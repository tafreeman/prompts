import React from "react";
import { StatCardsLayout } from "../../layouts/base/StatCardsLayout.tsx";

export default {
  title: "Layouts/Base/StatCardsLayout",
  component: StatCardsLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "stat-cards-onboarding",
  title: "Onboarding by the Numbers",
  subtitle: "Real metrics from our new-hire program over the last four cohorts.",
  color: "#0891B2",
  colorLight: "#22D3EE",
  colorGlow: "rgba(8,145,178,0.3)",
  icon: "🎯",
  cards: [
    {
      stat: "94%",
      statLabel: "Retention Rate",
      title: "Engineers Who Stay",
      body: "New hires who complete the full 90-day plan are 94% more likely to remain with the team through their first year compared to those who do not.",
    },
    {
      stat: "18 days",
      statLabel: "Avg. First Commit",
      title: "Time to First Contribution",
      body: "The median new hire makes their first merged pull request within 18 days of their start date, down from 32 days two years ago.",
    },
    {
      stat: "4.8 / 5",
      statLabel: "Satisfaction Score",
      title: "New Hire Experience Rating",
      body: "Post-onboarding surveys consistently rate the program above 4.7 across all dimensions: clarity, support, tooling, and team integration.",
    },
    {
      stat: "3×",
      statLabel: "Velocity Multiplier",
      title: "Buddy Program Impact",
      body: "New hires paired with a dedicated senior buddy reach full sprint velocity three times faster than those relying on documentation alone.",
    },
  ],
  callout: "A well-run onboarding program is the highest-ROI investment in your people.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
