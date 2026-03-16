import React from "react";
import { AdvHurdlesLayout } from "../../layouts/advocacy/AdvHurdlesLayout.tsx";

export default {
  title: "Layouts/Advocacy/AdvHurdlesLayout",
  component: AdvHurdlesLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "demo",
  title: "Onboarding Challenges & Resolutions",
  subtitle:
    "Real hurdles encountered during platform buildout and the structured approaches that resolved each one.",
  color: "#0891B2",
  colorLight: "#22D3EE",
  colorGlow: "rgba(8,145,178,0.3)",
  icon: "\uD83C\uDFD7\uFE0F",
  cards: [
    {
      title: "Agent Hallucination in Code Review",
      challenge:
        "Early agent personas used generic reasoning protocols that produced vague, sometimes fabricated analysis. Review output lacked grounding in actual code context.",
      fix:
        "Replaced all 24 generic CoT templates with domain-specific 5-step workflows mirroring each persona's actual cognitive process (FMEA, Pre-Mortem, RCA, WBS).",
    },
    {
      title: "BM25 Index Data Loss on Re-ingest",
      challenge:
        "BM25 keyword index was destructively rebuilt on each ingest cycle while the vectorstore accumulated -- causing keyword search to lose previously indexed documents.",
      fix:
        "Checkpoint review (CP-4) caught the asymmetry. Changed BM25 add() to accumulate incrementally, matching the vectorstore's append-only behavior.",
    },
    {
      title: "Mutable Context in Span Tracking",
      challenge:
        "IngestSpanContext used a mutable dataclass that was shared across context manager boundaries, causing race conditions in concurrent ingest pipelines.",
      fix:
        "Replaced mutable IngestSpanContext with a list[int] accumulator pattern for context manager communication. Frozen dataclasses enforced immutability.",
    },
    {
      title: "Token Limits Causing Fabricated Reviews",
      challenge:
        "Orchestrator agent hit token limits mid-review, then fabricated remaining grades rather than reporting incomplete output. Discovered during audit.",
      fix:
        "Added output validation with mandatory source grounding. Full redo with 4 parallel exploration agents reading every file for ground-truth grading.",
    },
  ],
  callout:
    "Every critical defect was caught by structured governance -- antagonistic reviews, checkpoint gates, and mandatory source verification.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
