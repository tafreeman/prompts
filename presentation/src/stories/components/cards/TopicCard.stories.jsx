import React from "react";
import TopicCard from "../../../components/cards/TopicCard.tsx";

export default {
  title: "Cards/TopicCard",
  component: TopicCard,
  parameters: {
    layout: "padded",
  },
  argTypes: {
    color: { control: "color" },
    onClick: { action: "clicked" },
  },
};

export const Default = {
  args: {
    title: "Prompt Standardization",
    body: "Established versioned prompt templates with embedded architecture context, reducing hallucination and inconsistent output across the team.",
    icon: "📋",
    color: "#22D3EE",
  },
  render: (args) => (
    <div style={{ maxWidth: 360 }}>
      <TopicCard {...args} />
    </div>
  ),
};

export const WithoutIcon = {
  args: {
    title: "AI Governance Model",
    body: "Every AI-generated code change is gated behind a structured human review checklist. Accountability is built into the workflow, not added after the fact.",
    color: "#F59E0B",
  },
  render: (args) => (
    <div style={{ maxWidth: 360 }}>
      <TopicCard {...args} />
    </div>
  ),
};

export const Clickable = {
  args: {
    title: "Code Review Workflow",
    body: "Pull requests include AI-generated diffs alongside human annotations. Reviewers verify correctness, security posture, and coding standards compliance.",
    icon: "🔍",
    color: "#8B5CF6",
    onClick: () => {},
  },
  render: (args) => (
    <div style={{ maxWidth: 360 }}>
      <p style={{ fontSize: 13, marginBottom: 12, opacity: 0.6 }}>
        This card is interactive — click to trigger the handler.
      </p>
      <TopicCard {...args} />
    </div>
  ),
};

export const TopicGrid = {
  render: () => {
    const topics = [
      {
        title: "Prompt Standardization",
        body: "Versioned templates with architecture context embedded at the system-prompt level.",
        icon: "📋",
        color: "#22D3EE",
      },
      {
        title: "Human Review Gates",
        body: "Structured PR checklists ensure every AI-assisted change passes security and quality bars.",
        icon: "🔍",
        color: "#F59E0B",
      },
      {
        title: "ADR Discipline",
        body: "Architectural decisions logged with rationale and trade-offs so the full team can audit choices.",
        icon: "📐",
        color: "#8B5CF6",
      },
      {
        title: "Test-Driven Delivery",
        body: "1,400+ tests written test-first. Coverage gate enforced in CI — no merge below 80%.",
        icon: "✅",
        color: "#10B981",
      },
    ];

    return (
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(2, 1fr)",
          gap: 16,
          maxWidth: 740,
        }}
      >
        {topics.map((t, i) => (
          <TopicCard key={i} {...t} />
        ))}
      </div>
    );
  },
};
