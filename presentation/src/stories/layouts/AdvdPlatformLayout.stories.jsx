import React from "react";
import { AdvdPlatformLayout } from "../../layouts/advocacy-dense/AdvdPlatformLayout.tsx";

export default {
  title: "Layouts/Advocacy Dense/AdvdPlatformLayout",
  component: AdvdPlatformLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "advd-platform",
  eyebrow: "Onboarding Platform",
  title: "The Platform Behind the Program",
  subtitle:
    "How automation, structured content, and real-time tracking come together to deliver a repeatable onboarding experience at any team size.",
  color: "#0891B2",
  colorLight: "#22D3EE",
  colorGlow: "rgba(8,145,178,0.3)",
  icon: "🎯",
  heroPoints: [
    "Single Source of Truth",
    "Automated Provisioning",
    "Real-Time Progress",
    "Manager Dashboard",
    "Feedback Loops",
  ],
  focusPanels: [
    {
      label: "Phase 1 — Orientation",
      title: "Days 1–5: Get Running",
      body: "Setup script provisions the environment in under 20 minutes. Compliance training is self-paced with automated completion tracking. Buddy is available same-day via shared channel.",
    },
    {
      label: "Phase 2 — Ramp-Up",
      title: "Days 6–30: First Contributions",
      body: "Curated first-ticket backlog surfaces in the hire's sprint board on day 6. Progress tracker updates automatically on PR merge. Manager 2-week check-in is pre-scheduled.",
    },
    {
      label: "Phase 3 — Ownership",
      title: "Days 31–90: Full Contribution",
      body: "Independent feature ownership with structured code-review responsibility introduced in week 4. Day-90 retrospective is a formal milestone with written sign-off from both sides.",
    },
  ],
  capabilities: [
    {
      icon: "⚙️",
      title: "Setup Script",
      body: "Idempotent bootstrap for env, credentials, and IDE.",
    },
    {
      icon: "📋",
      title: "First-Ticket Backlog",
      body: "Curated per sprint by the tech lead.",
    },
    {
      icon: "📊",
      title: "Progress Dashboard",
      body: "Shared real-time view for hire, buddy, and manager.",
    },
    {
      icon: "🤝",
      title: "Buddy Tracker",
      body: "Availability and responsiveness tracked automatically.",
    },
    {
      icon: "🔁",
      title: "Survey Engine",
      body: "Post-week-1, post-week-4, and post-day-90 feedback.",
    },
    {
      icon: "📚",
      title: "Knowledge Base",
      body: "CLAUDE.md, ARCHITECTURE.md, and CODING_STANDARDS.md kept current.",
    },
    {
      icon: "🔔",
      title: "Blocker Alerts",
      body: "Manager notified automatically when a milestone slips.",
    },
    {
      icon: "✅",
      title: "Sign-Off Workflow",
      body: "Formal day-90 completion with structured written retrospective.",
    },
  ],
  lanes: [
    {
      title: "Engineer Lane",
      persona: "New Hire",
      steps: [
        "Run setup script",
        "Complete compliance training",
        "Read CLAUDE.md",
        "Pick first ticket",
        "Submit first PR",
        "Take first review",
        "Day-90 retro",
      ],
    },
    {
      title: "Manager Lane",
      persona: "Engineering Manager",
      steps: [
        "Day-1 welcome session",
        "Assign buddy",
        "2-week check-in",
        "Review first PR",
        "Day-90 sign-off",
      ],
    },
    {
      title: "Team Lane",
      persona: "Full Team",
      steps: [
        "Buddy: week-1 daily unblocking",
        "Invite to architecture review",
        "Include in retrospective from day 7",
        "Assign first reviewer role (week 4)",
      ],
    },
  ],
  callout:
    "The platform does not replace human mentorship — it removes every obstacle that gets in its way.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
