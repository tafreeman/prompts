import React from "react";
import { HStripLayout } from "../../layouts/base/HStripLayout.tsx";

export default {
  title: "Layouts/Base/HStripLayout",
  component: HStripLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "h-strip-onboarding",
  title: "The Future of Onboarding",
  subtitle:
    "Where structured AI assistance, clear governance, and human mentorship converge.",
  color: "#0891B2",
  colorLight: "#22D3EE",
  colorGlow: "rgba(8,145,178,0.3)",
  icon: "🎯",
  cards: [
    {
      title: "AI-Assisted Ramp",
      body: "New hires interact with an AI assistant pre-loaded with team conventions, codebase context, and prior ADRs — answering the 'why' questions that documentation rarely covers.",
    },
    {
      title: "Adaptive Milestones",
      body: "The 90-day plan dynamically adjusts based on actual progress. If a hire hits week-two milestones in week one, the plan advances. If blocked, support is triggered automatically.",
    },
    {
      title: "Peer Knowledge Graph",
      body: "A lightweight graph maps who knows what across the team. New hires can identify the right person to ask for any topic without navigating org charts or Slack history.",
    },
    {
      title: "Onboarding Analytics",
      body: "Aggregated, anonymized metrics surface systemic friction early — before it shows up in attrition data. Teams can fix process gaps within the same cohort.",
    },
  ],
  callout:
    "The best onboarding programs are not documents — they are living systems that learn alongside the people they serve.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
