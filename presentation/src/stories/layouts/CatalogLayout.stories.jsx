import React from "react";
import { CatalogLayout } from "../../layouts/onboarding/CatalogLayout.tsx";

export default {
  title: "Layouts/Onboarding/CatalogLayout",
  component: CatalogLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "ai-tool-catalog",
  title: "Approved AI Tool Catalog",
  subtitle: "Classification by Risk Tier and Use Case",
  color: "#D97706",
  colorLight: "#FCD34D",
  colorGlow: "rgba(217,119,6,0.3)",
  icon: "🗂️",
  order: "05",
  categories: [
    {
      title: "Tier 1 — Fully Approved",
      color: "#059669",
      items: [
        {
          label: "GitHub Copilot (Enterprise)",
          desc: "Code completion and inline suggestions within the IDE. Output stays in the developer's environment. Enterprise license satisfies data residency requirements.",
        },
        {
          label: "Claude for Enterprise",
          desc: "Prompt-assisted drafting, code review support, and documentation generation via the approved enterprise API endpoint with audit logging enabled.",
        },
        {
          label: "Azure OpenAI (Approved Tenant)",
          desc: "GPT-4 class models hosted in the project's approved Azure tenant. Data does not leave the tenant boundary. Suitable for task automation and summarization.",
        },
      ],
    },
    {
      title: "Tier 2 — Conditional Use",
      color: "#D97706",
      items: [
        {
          label: "ChatGPT (Consumer)",
          desc: "Permitted for non-sensitive ideation and learning only. No project data, client names, architecture details, or code from active engagements may be entered.",
        },
        {
          label: "Gemini Advanced",
          desc: "Allowed for personal productivity on public-domain problems. Must not be used for engagement deliverables without explicit team lead approval.",
        },
        {
          label: "Local Ollama Models",
          desc: "Self-hosted open-weight models running on developer hardware. Acceptable for any sensitivity level since data never leaves the local machine.",
        },
      ],
    },
    {
      title: "Tier 3 — Prohibited",
      color: "#DC2626",
      items: [
        {
          label: "Consumer Image / Document AI",
          desc: "Uploading client documents, architecture diagrams, or engagement artifacts to consumer AI vision tools (e.g., ChatGPT vision, Google Lens) is prohibited.",
        },
        {
          label: "Unapproved Third-Party Plugins",
          desc: "IDE extensions or browser plugins that relay code to unapproved external endpoints are prohibited regardless of vendor marketing claims.",
        },
        {
          label: "AI-Generated Credentials or Keys",
          desc: "Using AI to generate, rotate, or manage secrets, API keys, or certificates outside of the approved secrets manager workflow is prohibited.",
        },
      ],
    },
    {
      title: "Tier 4 — Emerging / Review",
      color: "#6366F1",
      items: [
        {
          label: "AI Agents with Autonomous Actions",
          desc: "Tools that autonomously open PRs, deploy code, or modify infrastructure are under evaluation. Do not use in production workflows without architecture review.",
        },
        {
          label: "Multi-Modal Code Agents",
          desc: "Vision-enabled agents that read screenshots or UI designs to generate code are in sandbox review. Pilot use only with security reviewer assigned.",
        },
      ],
    },
  ],
  callout: "When in doubt about a tool's tier, default to Tier 3 and escalate to the security reviewer before use.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
