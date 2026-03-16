import React from "react";
import { AdvdStatsLayout } from "../../layouts/advocacy-dense/AdvdStatsLayout.tsx";

export default {
  title: "Layouts/Advocacy Dense/AdvdStatsLayout",
  component: AdvdStatsLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "advd-stats",
  title: "Onboarding Metrics That Matter",
  subtitle: "Hard numbers from four cohorts and 32 new hires over 18 months.",
  color: "#0891B2",
  colorLight: "#22D3EE",
  colorGlow: "rgba(8,145,178,0.3)",
  icon: "🎯",
  thesis:
    "A structured onboarding program is not overhead — it is the fastest path to a productive, retained engineer. These numbers make the case.",
  cards: [
    {
      icon: "📅",
      stat: "18 days",
      statLabel: "Avg. First Merged PR",
      title: "Time to First Contribution",
      body: "Down from 32 days before the structured program was introduced.",
    },
    {
      icon: "📈",
      stat: "94%",
      statLabel: "Year-1 Retention",
      title: "Engineers Who Stay",
      body: "New hires completing the 90-day plan retain at nearly double the baseline rate.",
    },
    {
      icon: "⭐",
      stat: "4.8 / 5",
      statLabel: "Satisfaction Score",
      title: "New Hire Experience",
      body: "Post-program survey across clarity, tooling, support, and team integration.",
    },
    {
      icon: "⚡",
      stat: "3×",
      statLabel: "Velocity Multiplier",
      title: "Buddy Program Impact",
      body: "Buddy-paired hires reach full sprint velocity three times faster.",
    },
    {
      icon: "🛠️",
      stat: "< 20 min",
      statLabel: "Setup Time",
      title: "Automated Provisioning",
      body: "Full dev environment, credentials, and IDE config via a single setup script.",
    },
    {
      icon: "✅",
      stat: "0",
      statLabel: "Missed Day-90 Reviews",
      title: "Program Completion Rate",
      body: "Every hire in the last three cohorts completed the formal day-90 retrospective.",
    },
  ],
  leadershipPoints: [
    "A 14-day reduction in time-to-first-PR translates directly to sprint capacity recovered per hire.",
    "94% year-1 retention means each structured onboarding cycle pays for itself many times over.",
    "The buddy program is the single highest-leverage intervention — it costs hours and saves months.",
  ],
  callout: "The numbers are not goals — they are the outcome of a system that actually runs.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
