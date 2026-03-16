import React from "react";
import { AdvStatsLayout } from "../../layouts/advocacy/AdvStatsLayout.tsx";

export default {
  title: "Layouts/AdvStatsLayout",
  component: AdvStatsLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "adv-stats",
  title: "Sprint Velocity & Metrics",
  subtitle: "Hard numbers from 12 sprints of AI-assisted delivery.",
  color: "#10B981",
  colorLight: "#34D399",
  colorGlow: "rgba(16,185,129,0.3)",
  thesis:
    "AI-assisted development is not about replacing engineers. It is about removing friction so senior engineers can focus on architecture, governance, and quality.",
  cards: [
    {
      stat: "1,400+",
      statLabel: "Tests Passing",
      title: "Comprehensive Coverage",
      body: "Unit, integration, and E2E tests across all modules with 80%+ coverage on business logic.",
      marker: "\u2713",
    },
    {
      stat: "92%",
      statLabel: "RAG Coverage",
      title: "Pipeline Quality",
      body: "Full RAG pipeline coverage exceeding the 80% gate across ingest, chunk, embed, retrieve, and assemble.",
      marker: "\u2713",
    },
    {
      stat: "12",
      statLabel: "Sprints",
      title: "Delivery Cadence",
      body: "Consistent two-week sprints with clear checkpoint reviews and antagonistic audits at each gate.",
      marker: "\u25CB",
    },
    {
      stat: "0",
      statLabel: "Critical Defects",
      title: "Quality Gate",
      body: "Zero critical defects across all sprints. Every FATAL and CRITICAL finding resolved before merge.",
      marker: "\u2605",
    },
    {
      stat: "24",
      statLabel: "Agent Personas",
      title: "Specialized Workflows",
      body: "Each persona has domain-specific reasoning steps, boundaries, and output formats.",
    },
    {
      stat: "8+",
      statLabel: "LLM Providers",
      title: "Multi-Backend Routing",
      body: "OpenAI, Anthropic, Gemini, Azure, GitHub Models, Ollama, and local ONNX with smart tier dispatch.",
    },
  ],
  leadershipPoints: [
    "AI accelerated delivery by 3-5x while maintaining federal compliance standards.",
    "Structured governance (antagonistic reviews, checkpoint gates) prevented quality regression.",
    "The platform is production-ready, not a prototype \u2014 it runs in cleared environments today.",
  ],
  callout: "Velocity without governance is just technical debt at speed.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};

export const Expanded = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
  play: async ({ canvasElement }) => {
    // Click the first two cards to show the expanded state
    const buttons = canvasElement.querySelectorAll("button");
    if (buttons[0]) buttons[0].click();
    if (buttons[1]) buttons[1].click();
  },
};
