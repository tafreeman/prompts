import React from "react";
import { TwoColLayout } from "../../layouts/base/TwoColLayout.tsx";

export default {
  title: "Layouts/Base/TwoColLayout",
  component: TwoColLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "two-col-onboarding",
  eyebrow: "New Hire Onboarding",
  title: "Welcome to the Team",
  subtitle:
    "Everything you need to become productive, trusted, and effective in your first 90 days.",
  color: "#0891B2",
  colorLight: "#22D3EE",
  colorGlow: "rgba(8,145,178,0.3)",
  icon: "🎯",
  summary:
    "Our onboarding program is structured around three phases: orientation, ramp-up, and contribution. Each phase has clear goals, milestones, and support resources to ensure you succeed from day one.",
  heroPoints: [
    "90-Day Ramp Plan",
    "Dedicated Buddy",
    "Clear Milestones",
    "Team Integration",
  ],
  cards: [
    {
      title: "Week 1 — Orientation",
      body: "Meet your team, complete required compliance training, and get your development environment fully configured. Your buddy will guide you through tooling and answer early questions.",
    },
    {
      title: "Weeks 2–4 — Ramp-Up",
      body: "Tackle your first assigned tickets, attend sprint ceremonies, and shadow senior engineers on design sessions. Begin contributing small pull requests by end of week three.",
    },
    {
      title: "Days 30–90 — Contribution",
      body: "Take ownership of a module, lead a feature from design to deploy, and complete your first code review as a reviewer. Present a retrospective to your manager at day 90.",
    },
  ],
  talkingPoints: [
    "Every new hire is paired with a senior buddy for the first 30 days — direct access, no bureaucracy.",
    "All onboarding tasks live in the shared tracker so progress is visible to you and your manager.",
    "The 90-day plan is adaptive — milestones adjust if you hit blockers early in the ramp.",
    "Completion of the plan is a formal checkpoint before your first performance cycle.",
  ],
  callout: "Day one is just the beginning — your ramp is our shared responsibility.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
