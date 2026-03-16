import React from "react";
import { SprintLayout } from "../../layouts/sprint/SprintLayout.tsx";

export default {
  title: "Layouts/Sprint/SprintLayout",
  component: SprintLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "demo",
  color: "#0891B2",
  colorLight: "#22D3EE",
  colorGlow: "rgba(8,145,178,0.3)",
  icon: "\uD83D\uDCD8",
  title: "AI Sprint Cycle",
  subtitle: "Continuous Build-Validate loop powering iterative delivery",
  callout:
    "Each sprint cycle feeds validated output back into the next iteration, compounding quality with every pass.",
};

const mockNodes = [
  { icon: "\uD83D\uDCCB", label: "Requirements", type: "human" },
  { icon: "\uD83E\uDDE0", label: "Architecture", type: "ai" },
  { icon: "\uD83D\uDCDD", label: "Spec Draft", type: "ai" },
  { icon: "\u2705", label: "Spec Review", type: "human" },
  { icon: "\uD83D\uDEE0\uFE0F", label: "Implementation", type: "ai" },
  { icon: "\uD83E\uDDEA", label: "Test Suite", type: "ai" },
  { icon: "\uD83D\uDD0D", label: "Code Review", type: "human" },
  { icon: "\uD83D\uDE80", label: "Deploy", type: "human" },
  { icon: "\uD83D\uDCCA", label: "Metrics", type: "ai" },
  { icon: "\uD83D\uDD04", label: "Retrospective", type: "human" },
];

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
    nodes: mockNodes,
  },
};
