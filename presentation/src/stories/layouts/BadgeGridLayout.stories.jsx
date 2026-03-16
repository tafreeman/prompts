import React from "react";
import { BadgeGridLayout } from "../../layouts/verge-pop/BadgeGridLayout.tsx";

export default {
  title: "Layouts/Verge Pop/BadgeGridLayout",
  component: BadgeGridLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "demo",
  title: "Onboarding Skill Badges",
  subtitle:
    "Track your progress through each competency area as you earn badges during your first 90 days.",
  color: "#8B5CF6",
  colorLight: "#A78BFA",
  colorGlow: "rgba(139,92,246,0.3)",
  icon: "\u25CE",
  question: "Which skills should every new engineer demonstrate by week 12?",
  badges: [
    { icon: "\uD83D\uDD12", name: "Security Cleared", value: "Wk 1", bgColor: "#A78BFA" },
    { icon: "\uD83D\uDEE0\uFE0F", name: "Dev Env Ready", value: "Wk 1", bgColor: "#34D399" },
    { icon: "\uD83D\uDCDD", name: "First Commit", value: "Wk 1", bgColor: "#60A5FA" },
    { icon: "\u2705", name: "Code Review", value: "Wk 2", bgColor: "#F59E0B" },
    { icon: "\uD83E\uDDEA", name: "TDD Certified", value: "Wk 3", bgColor: "#FB923C" },
    { icon: "\uD83D\uDE80", name: "Feature Shipped", value: "Wk 4", bgColor: "#F472B6" },
    { icon: "\uD83D\uDCCA", name: "Sprint Demo", value: "Wk 6", bgColor: "#10B981" },
    { icon: "\uD83E\uDD1D", name: "Peer Mentor", value: "Wk 8", bgColor: "#8B5CF6" },
    { icon: "\uD83C\uDFAF", name: "Full Velocity", value: "Wk 12", bgColor: "#000000" },
    { icon: "\u2B50", name: "Onboarded", value: "Done", bgColor: "#EAB308" },
  ],
  callout:
    "Badge-based progression gives new hires clear milestones and managers measurable checkpoints.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
