import React from "react";
import { AdvOverviewLayout } from "../../layouts/advocacy/AdvOverviewLayout.tsx";

export default {
  title: "Layouts/AdvOverviewLayout",
  component: AdvOverviewLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "adv-overview",
  eyebrow: "GenAI Advocacy",
  title: "Accelerating Federal Delivery",
  subtitle:
    "How structured AI-assisted development delivered a production-grade platform in record time while maintaining zero critical defects.",
  color: "#22D3EE",
  colorLight: "#67E8F9",
  colorGlow: "rgba(34,211,238,0.3)",
  heroPoints: [
    "12-Sprint Delivery",
    "1,400+ Tests",
    "Zero Critical Defects",
    "8 LLM Providers",
  ],
  summary:
    "This deck walks through the real metrics, patterns, and governance model behind our GenAI-accelerated workflow platform. Every claim is backed by commit history and test evidence.",
  cards: [
    { title: "Multi-Agent Runtime", body: "DAG-based orchestration with Kahn's algorithm" },
    { title: "RAG Pipeline", body: "Full ingest-chunk-embed-retrieve-assemble pipeline" },
    { title: "Dual Engines", body: "Native + LangGraph execution backends" },
    { title: "Smart Routing", body: "8+ LLM providers with tier-based dispatch" },
  ],
  talkingPoints: [
    "Production code, not a prototype — runs in cleared federal environments",
    "Every architectural decision documented in ADRs with 2+ independent sources",
    "Antagonistic review pattern caught issues that unit tests missed",
  ],
  callout: "We didn't just use AI. We governed it.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
