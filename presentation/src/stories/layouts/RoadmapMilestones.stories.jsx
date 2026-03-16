import React from "react";
import RoadmapMilestones from "../../layouts/engineering/RoadmapMilestones.tsx";

export default {
  title: "Layouts/Engineering/RoadmapMilestones",
  component: RoadmapMilestones,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "demo",
  title: "Onboarding Platform Roadmap",
  subtitle: "Phased delivery plan from MVP to enterprise-grade deployment",
  color: "#0891B2",
  colorLight: "#22D3EE",
  colorGlow: "rgba(8,145,178,0.3)",
  icon: "\uD83C\uDFD7\uFE0F",
  cards: [
    {
      title: "Phase 1: Core Runtime",
      body: "Protocols, adapter registry, native DAG executor, and basic agent dispatch. Test harness and CI pipeline established.",
      stat: "Q1",
      icon: "\uD83D\uDEE0\uFE0F",
    },
    {
      title: "Phase 2: RAG & Memory",
      body: "Full retrieval pipeline, hybrid search, memory abstraction, and domain-adaptive scoring. 92% module coverage achieved.",
      stat: "Q2",
      icon: "\uD83E\uDDE0",
    },
    {
      title: "Phase 3: Integration",
      body: "CLI tooling, server routing, WebSocket streaming, and React dashboard. End-to-end workflow execution validated.",
      stat: "Q3",
      icon: "\uD83D\uDD17",
    },
    {
      title: "Phase 4: Hardening",
      body: "Security audit, path traversal protection, prompt injection framing, and antagonistic review gates. Production deployment.",
      stat: "Q4",
      icon: "\uD83D\uDD12",
    },
    {
      title: "Phase 5: Scale",
      body: "Multi-tenant isolation, horizontal agent scaling, persistent checkpointing, and observability dashboards for operations teams.",
      stat: "Q5",
      icon: "\uD83D\uDE80",
    },
  ],
  talkingPoints: [
    "Each phase gated by checkpoint review with antagonistic audit -- no phase ships without sign-off",
    "Additive-only contract evolution ensures downstream consumers never break on upgrade",
    "Parallel sprint execution used when phases touch non-overlapping file sets",
    "Security reviewer agent runs before every merge to production branch",
  ],
  callout: "Roadmap milestones are commitments, not aspirations -- each one backed by test evidence and checkpoint sign-off.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
