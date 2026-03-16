import React from "react";
import TechStackTimeline from "../../layouts/engineering/TechStackTimeline.tsx";

export default {
  title: "Layouts/Engineering/TechStackTimeline",
  component: TechStackTimeline,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "demo",
  title: "Technology Evolution",
  subtitle: "How our onboarding platform's tech stack matured across 12 sprints",
  color: "#0891B2",
  colorLight: "#22D3EE",
  colorGlow: "rgba(8,145,178,0.3)",
  icon: "\uD83C\uDFD7\uFE0F",
  results: [
    { value: "12", label: "Sprints" },
    { value: "1,400+", label: "Tests" },
    { value: "92%", label: "RAG Coverage" },
    { value: "8+", label: "LLM Backends" },
  ],
  cards: [
    {
      title: "Foundation",
      body: "Core protocols, adapter registry, and native DAG executor. Established runtime-checkable interfaces for all extension points.",
      stat: "S1-S3",
    },
    {
      title: "RAG Pipeline",
      body: "Built full ingest-chunk-embed-retrieve-assemble pipeline. Content-hash dedup, BM25 keyword index, and hybrid retrieval with RRF fusion.",
      stat: "S4-S7",
    },
    {
      title: "Memory & Research",
      body: "MemoryStoreProtocol with async key-value and search. Domain-adaptive recency scoring and YAML anchor-based config.",
      stat: "S8-S9",
    },
    {
      title: "CLI & Server",
      body: "CLI compare command, RAG CLI tools, server adapter routing. FastAPI + WebSocket streaming for real-time dashboard updates.",
      stat: "S10",
    },
    {
      title: "Security Audit",
      body: "Path traversal protection, top_k bounds validation, query sanitization, and adapter exception narrowing. Final validation pass.",
      stat: "S11",
    },
    {
      title: "Production Ready",
      body: "All 11 sprints and 4 checkpoint reviews completed. Zero critical defects, 1,400+ tests passing, deployed to cleared federal environment.",
      stat: "S12",
    },
  ],
  callout: "Each sprint built on proven foundations -- no throwaway prototypes, no rewrites.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
