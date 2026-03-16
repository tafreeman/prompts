import React from "react";
import { AdvFutureLayout } from "../../layouts/advocacy/AdvFutureLayout.tsx";

export default {
  title: "Layouts/Advocacy/AdvFutureLayout",
  component: AdvFutureLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "demo",
  title: "Future of AI-Assisted Onboarding",
  subtitle:
    "Where structured AI governance meets enterprise-scale team enablement.",
  color: "#0891B2",
  colorLight: "#22D3EE",
  colorGlow: "rgba(8,145,178,0.3)",
  icon: "\uD83C\uDFD7\uFE0F",
  callout:
    "The next generation of onboarding is not about faster forms -- it is about intelligent systems that adapt to each new hire's role, clearance, and learning style.",
  cards: [
    {
      title: "Adaptive Learning Paths",
      body: "RAG-powered content assembly that tailors onboarding materials to each new hire's role, team context, and prior experience level.",
    },
    {
      title: "Mentor Matching Engine",
      body: "Agent-based mentor recommendation using skill graph analysis, availability scoring, and team topology for optimal pairing.",
    },
    {
      title: "Continuous Compliance",
      body: "Automated policy verification that checks every onboarding step against current clearance requirements and organizational standards.",
    },
    {
      title: "Feedback Loop Integration",
      body: "Real-time sentiment analysis on new hire experience surveys, feeding back into workflow optimization and content quality scoring.",
    },
  ],
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
