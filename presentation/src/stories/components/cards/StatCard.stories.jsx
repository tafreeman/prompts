import React from "react";
import StatCard from "../../../components/cards/StatCard.tsx";

export default {
  title: "Cards/StatCard",
  component: StatCard,
  parameters: {
    layout: "padded",
  },
  argTypes: {
    color: { control: "color" },
    size: { control: { type: "select" }, options: ["sm", "md", "lg"] },
    expandable: { control: "boolean" },
  },
};

export const Default = {
  args: {
    title: "Prompt Templates",
    stat: "24",
    statLabel: "active",
    body: "Versioned prompt templates with embedded architecture context reduce AI hallucination and standardize code review output.",
    size: "md",
  },
  render: (args) => (
    <div style={{ maxWidth: 480 }}>
      <StatCard {...args} />
    </div>
  ),
};

export const WithAccentColor = {
  args: {
    title: "Human Review Gates",
    stat: "100%",
    statLabel: "coverage",
    body: "Every AI-assisted pull request passes through a structured human review checklist before merge.",
    size: "md",
    color: "#22D3EE",
  },
  render: (args) => (
    <div style={{ maxWidth: 480 }}>
      <StatCard {...args} />
    </div>
  ),
};

export const Small = {
  args: {
    title: "Critical Defects",
    stat: "0",
    statLabel: "post-launch",
    size: "sm",
    color: "#10B981",
  },
  render: (args) => (
    <div style={{ maxWidth: 480 }}>
      <StatCard {...args} />
    </div>
  ),
};

export const Large = {
  args: {
    title: "ADR Decisions Logged",
    stat: "47",
    statLabel: "documented",
    body: "Every architectural decision recorded with evidence, rationale, and trade-offs so the full team can audit choices months later.",
    size: "lg",
    color: "#8B5CF6",
  },
  render: (args) => (
    <div style={{ maxWidth: 480 }}>
      <StatCard {...args} />
    </div>
  ),
};

export const DashboardRow = {
  render: () => (
    <div style={{ display: "flex", flexDirection: "column", gap: 16, maxWidth: 520 }}>
      <StatCard
        title="Test Suite Coverage"
        stat="92%"
        statLabel="branch coverage"
        body="RAG module coverage tracked via pytest-cov; gate set at 80% with CI enforcement."
        color="#22D3EE"
        size="md"
      />
      <StatCard
        title="Governance Reviews Passed"
        stat="12"
        statLabel="checkpoints"
        body="Four antagonistic checkpoint reviews caught critical issues before they reached production."
        color="#F59E0B"
        size="md"
      />
      <StatCard
        title="AI Models Integrated"
        stat="8+"
        statLabel="providers"
        body="Smart router dispatches across OpenAI, Anthropic, Gemini, Azure, GitHub Models, and Ollama."
        color="#8B5CF6"
        size="md"
      />
    </div>
  ),
};
