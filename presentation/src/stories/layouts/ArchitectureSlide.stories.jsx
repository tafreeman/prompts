import React from "react";
import ArchitectureSlide from "../../layouts/engineering/ArchitectureSlide.tsx";

export default {
  title: "Layouts/Engineering/ArchitectureSlide",
  component: ArchitectureSlide,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "demo",
  title: "Platform Architecture",
  subtitle: "Layered system topology for the onboarding workflow engine",
  color: "#0891B2",
  colorLight: "#22D3EE",
  colorGlow: "rgba(8,145,178,0.3)",
  icon: "\uD83C\uDFD7\uFE0F",
  cards: [
    {
      title: "Presentation Layer",
      body: "React 19 dashboard with real-time workflow visualization, WebSocket streaming, and role-based access controls for new team members.",
      stat: "UI",
      statLabel: "React 19 + Vite 6",
    },
    {
      title: "API Gateway",
      body: "FastAPI server with SSE and WebSocket endpoints. Handles authentication, rate limiting, and request validation for all onboarding flows.",
      stat: "API",
      statLabel: "FastAPI + Uvicorn",
    },
    {
      title: "Orchestration Engine",
      body: "DAG-based workflow executor using Kahn's algorithm. Manages agent dispatch, step dependencies, and parallel execution across onboarding tasks.",
      stat: "DAG",
      statLabel: "Dual Engine (Native + LangGraph)",
    },
    {
      title: "Agent Runtime",
      body: "24 specialized agent personas with domain-specific reasoning steps. Each agent has defined expertise boundaries, output formats, and tool allowlists.",
      stat: "24",
      statLabel: "Agent Personas",
    },
    {
      title: "RAG Pipeline",
      body: "Full ingest-chunk-embed-retrieve-assemble pipeline with hybrid retrieval (BM25 + cosine similarity), RRF fusion, and token-budget assembly.",
      stat: "RAG",
      statLabel: "Hybrid Retrieval",
    },
    {
      title: "Infrastructure",
      body: "8+ LLM providers with smart tier-based routing, content-hash dedup embedding, and OTEL tracing. Designed for cleared federal environments.",
      stat: "8+",
      statLabel: "LLM Providers",
    },
  ],
  callout: "Each layer is independently testable and deployable -- no monolithic coupling between concerns.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
