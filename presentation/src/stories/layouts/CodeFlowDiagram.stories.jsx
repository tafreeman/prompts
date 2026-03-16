import React from "react";
import CodeFlowDiagram from "../../layouts/engineering/CodeFlowDiagram.tsx";

export default {
  title: "Layouts/Engineering/CodeFlowDiagram",
  component: CodeFlowDiagram,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "demo",
  title: "Onboarding Request Pipeline",
  subtitle: "End-to-end data flow from new hire intake to provisioned workspace",
  color: "#0891B2",
  colorLight: "#22D3EE",
  colorGlow: "rgba(8,145,178,0.3)",
  icon: "\uD83C\uDFD7\uFE0F",
  cards: [
    {
      title: "Intake Form",
      body: "New hire submits onboarding request via React dashboard with role, clearance level, and team assignment.",
      icon: "\uD83D\uDCCB",
    },
    {
      title: "Validation",
      body: "Pydantic models validate all inputs. Clearance tier and role checked against access policy before proceeding.",
      icon: "\u2705",
    },
    {
      title: "DAG Planning",
      body: "Orchestrator builds a dependency graph of onboarding steps using Kahn's algorithm for topological ordering.",
      icon: "\uD83D\uDDD3\uFE0F",
    },
    {
      title: "Agent Dispatch",
      body: "Specialized agents execute each step: account provisioning, training assignment, mentor matching, equipment request.",
      icon: "\uD83E\uDD16",
    },
    {
      title: "RAG Enrichment",
      body: "Hybrid retriever pulls relevant policy docs, team norms, and role-specific guides for the new hire's welcome packet.",
      icon: "\uD83D\uDD0D",
    },
    {
      title: "Delivery",
      body: "Assembled onboarding package streamed to dashboard via WebSocket. Manager receives status summary and action items.",
      icon: "\uD83D\uDCE6",
    },
  ],
  callout: "Average onboarding pipeline completes in under 90 seconds -- from intake to fully provisioned workspace.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
