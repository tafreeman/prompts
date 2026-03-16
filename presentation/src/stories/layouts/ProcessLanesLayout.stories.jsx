import React from "react";
import { ProcessLanesLayout } from "../../layouts/base/ProcessLanesLayout.tsx";

export default {
  title: "Layouts/Base/ProcessLanesLayout",
  component: ProcessLanesLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "process-lanes-onboarding",
  eyebrow: "Onboarding Platform",
  title: "How the Onboarding System Works",
  subtitle:
    "Three parallel lanes — Engineer, Manager, and Team — each with their own steps, touchpoints, and owned outcomes.",
  color: "#0891B2",
  colorLight: "#22D3EE",
  colorGlow: "rgba(8,145,178,0.3)",
  icon: "🎯",
  heroPoints: [
    "Self-Service Setup",
    "Manager Checkpoints",
    "Team Integration",
    "Automated Tracking",
    "Clear Ownership",
  ],
  focusPanels: [
    {
      label: "Phase 1",
      title: "Orientation (Days 1–5)",
      body: "Tooling setup, compliance training, team introductions, and access provisioning. The engineer completes a self-service checklist; the buddy is available for same-day unblocking.",
    },
    {
      label: "Phase 2",
      title: "Ramp-Up (Days 6–30)",
      body: "First-ticket backlog, sprint ceremony participation, and pair-programming sessions. Manager conducts a 2-week check-in to surface blockers and adjust the plan if needed.",
    },
    {
      label: "Phase 3",
      title: "Contribution (Days 31–90)",
      body: "Independent feature ownership, first code review as reviewer, and a day-90 retrospective with the manager. Formal sign-off marks completion of the onboarding program.",
    },
  ],
  capabilities: [
    {
      icon: "⚙️",
      title: "Automated Setup Script",
      body: "Provisions dev environment, credentials, and IDE config in under 20 minutes.",
    },
    {
      icon: "📋",
      title: "First-Ticket Backlog",
      body: "Curated per-sprint, scoped to one file, with clear acceptance criteria.",
    },
    {
      icon: "📊",
      title: "Progress Tracker",
      body: "Shared dashboard visible to engineer, buddy, and manager throughout the 90 days.",
    },
    {
      icon: "🔍",
      title: "Feedback Loops",
      body: "Post-week-1, post-week-4, and post-day-90 surveys feed the program improvement cycle.",
    },
  ],
  lanes: [
    {
      title: "Engineer Lane",
      subtitle: "Self-directed ramp with structured support",
      persona: "New Hire",
      accent: "#0891B2",
      steps: [
        "Run automated setup script",
        "Complete compliance training",
        "Read CLAUDE.md and ARCHITECTURE.md",
        "Pick first ticket from curated backlog",
        "Submit first pull request",
        "Complete day-90 retrospective",
      ],
    },
    {
      title: "Manager Lane",
      subtitle: "Oversight, unblocking, and milestone sign-off",
      persona: "Engineering Manager",
      accent: "#0E7490",
      steps: [
        "Schedule day-1 welcome and context session",
        "Assign buddy and introduce the backlog",
        "Conduct 2-week check-in",
        "Review and merge first PR with detailed feedback",
        "Sign off on day-90 retrospective",
      ],
    },
    {
      title: "Team Lane",
      subtitle: "Integration and culture transfer",
      persona: "Full Team",
      accent: "#155E75",
      steps: [
        "Buddy provides daily unblocking support for week 1",
        "Invite new hire to architecture review in week 2",
        "Include in sprint retrospective from day 7",
        "Assign first code-review responsibility in week 4",
      ],
    },
  ],
  talkingPoints: [
    "All three lanes run in parallel — no lane waits for another to complete before starting.",
    "The progress tracker is the single source of truth; no separate status emails or check-in decks.",
    "Buddy assignment is a commitment, not a courtesy — it is tracked and reflected in quarterly goals.",
    "The curated first-ticket backlog is maintained by the tech lead and refreshed each sprint.",
  ],
  callout: "Onboarding is a system, not an event — and every lane has a named owner.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
