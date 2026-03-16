import React from "react";
import { AdvPlatformLayout } from "../../layouts/advocacy/AdvPlatformLayout.tsx";

export default {
  title: "Layouts/Advocacy/AdvPlatformLayout",
  component: AdvPlatformLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "demo",
  title: "Onboarding Workflow Platform",
  subtitle:
    "A unified platform for automated team onboarding with multi-agent orchestration, smart routing, and governed AI assistance.",
  color: "#0891B2",
  colorLight: "#22D3EE",
  colorGlow: "rgba(8,145,178,0.3)",
  icon: "\uD83C\uDFD7\uFE0F",
  eyebrow: "Platform Overview",
  heroPoints: [
    "DAG-Based Orchestration",
    "24 Agent Personas",
    "Hybrid RAG Retrieval",
    "8+ LLM Backends",
    "Zero Critical Defects",
  ],
  focusPanels: [
    {
      label: "Orchestration",
      title: "Workflow Engine",
      body: "DAG executor with Kahn's algorithm manages step dependencies, parallel dispatch, and hierarchical context propagation across all onboarding tasks.",
    },
    {
      label: "Intelligence",
      title: "RAG Pipeline",
      body: "Hybrid retrieval combining BM25 keyword search and cosine similarity with RRF fusion. Token-budget assembly ensures context stays within model limits.",
    },
    {
      label: "Governance",
      title: "Quality Gates",
      body: "Antagonistic review pattern with checkpoint gates at every phase. Security reviewer, code reviewer, and TDD guide agents enforce standards before merge.",
    },
  ],
  capabilities: [
    {
      icon: "\uD83E\uDD16",
      title: "Multi-Agent Dispatch",
      body: "Specialized personas for architecture, code review, security analysis, TDD guidance, and documentation.",
    },
    {
      icon: "\uD83D\uDD00",
      title: "Smart LLM Routing",
      body: "Tier-based dispatch across OpenAI, Anthropic, Gemini, Azure, GitHub Models, Ollama, and local ONNX.",
    },
    {
      icon: "\uD83D\uDEE1\uFE0F",
      title: "Security First",
      body: "Path traversal protection, input validation, prompt injection framing, and tool allowlisting per workflow step.",
    },
    {
      icon: "\uD83D\uDCCA",
      title: "Observability",
      body: "OTEL tracing across the full RAG pipeline, structured logging with loguru, and real-time WebSocket status streaming.",
    },
  ],
  lanes: [
    {
      title: "New Hire Onboarding Flow",
      persona: "Onboarding Manager",
      steps: [
        "Receive intake form with role, clearance level, and team assignment",
        "Validate inputs against access policy using Pydantic models",
        "Build dependency graph of onboarding steps via DAG planner",
        "Dispatch provisioning agents for accounts, equipment, and training",
        "Assemble welcome packet using RAG retrieval of team norms and role guides",
        "Stream completed package to manager dashboard via WebSocket",
      ],
    },
    {
      title: "Mentor Assignment Pipeline",
      persona: "Team Lead",
      steps: [
        "Analyze new hire's skill profile and learning preferences",
        "Query skill graph for compatible mentors with matching domain expertise",
        "Score candidates by availability, workload balance, and team proximity",
        "Present top three recommendations with rationale to team lead",
        "Confirm assignment and notify both parties with kickoff agenda",
      ],
    },
    {
      title: "Compliance Verification",
      persona: "Security Officer",
      steps: [
        "Check clearance tier against role requirements and facility access",
        "Verify training completion records for mandatory security modules",
        "Validate NDA and acceptable use policy acknowledgments",
        "Generate compliance attestation report for audit trail",
      ],
    },
  ],
  callout:
    "Production-grade governance means every workflow step is auditable, every agent output is validated, and every decision has a paper trail.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
