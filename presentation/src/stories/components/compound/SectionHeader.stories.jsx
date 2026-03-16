import React, { useEffect, useState } from "react";
import SectionHeader from "../../../components/compound/SectionHeader.tsx";

export default {
  title: "Compound/SectionHeader",
  component: SectionHeader,
  parameters: {
    layout: "padded",
  },
  argTypes: {
    entered: { control: "boolean" },
  },
};

const governanceTopic = {
  icon: "⚖️",
  order: "01",
  title: "AI Governance",
  subtitle: "Accountability structures that keep humans in control of every decision.",
  color: "#F59E0B",
  colorLight: "#FBBF24",
  colorGlow: "rgba(245,158,11,0.35)",
};

const codeReviewTopic = {
  icon: "🔍",
  order: "02",
  title: "Code Review Workflow",
  subtitle: "Structured gates that catch issues before they reach production.",
  color: "#22D3EE",
  colorLight: "#67E8F9",
  colorGlow: "rgba(34,211,238,0.35)",
};

const testingTopic = {
  icon: "🧪",
  order: "03",
  title: "Test-Driven Delivery",
  subtitle: "Every feature written test-first. 1,400+ tests enforced in CI.",
  color: "#10B981",
  colorLight: "#34D399",
  colorGlow: "rgba(16,185,129,0.35)",
};

const architectureTopic = {
  icon: "🏗️",
  order: "04",
  title: "Architecture Decisions",
  subtitle: "ADRs capture the rationale behind every structural choice — fully auditable.",
  color: "#8B5CF6",
  colorLight: "#A78BFA",
  colorGlow: "rgba(139,92,246,0.35)",
};

export const Default = {
  args: {
    topic: governanceTopic,
    entered: true,
  },
  render: (args) => (
    <div style={{ maxWidth: 640 }}>
      <SectionHeader {...args} />
    </div>
  ),
};

export const NotEntered = {
  args: {
    topic: codeReviewTopic,
    entered: false,
  },
  render: (args) => (
    <div style={{ maxWidth: 640 }}>
      <p style={{ fontSize: 12, opacity: 0.5, marginBottom: 16 }}>
        entered=false — header is translucent and translated down (pre-animation state).
      </p>
      <SectionHeader {...args} />
    </div>
  ),
};

export const AnimatedEntry = {
  render: () => {
    const [entered, setEntered] = useState(false);

    useEffect(() => {
      const t = setTimeout(() => setEntered(true), 300);
      return () => clearTimeout(t);
    }, []);

    return (
      <div style={{ maxWidth: 640 }}>
        <p style={{ fontSize: 12, opacity: 0.5, marginBottom: 16 }}>
          Reopen this story to replay the entrance animation.
        </p>
        <SectionHeader topic={testingTopic} entered={entered} />
      </div>
    );
  },
};

export const WithoutSubtitle = {
  args: {
    topic: {
      icon: "📐",
      order: "05",
      title: "Prompt Engineering",
      color: "#0891B2",
      colorLight: "#22D3EE",
      colorGlow: "rgba(8,145,178,0.35)",
    },
    entered: true,
  },
  render: (args) => (
    <div style={{ maxWidth: 640 }}>
      <SectionHeader {...args} />
    </div>
  ),
};

export const AllModules = {
  render: () => {
    const topics = [governanceTopic, codeReviewTopic, testingTopic, architectureTopic];

    return (
      <div style={{ maxWidth: 640, display: "flex", flexDirection: "column", gap: 8 }}>
        {topics.map((topic, i) => (
          <SectionHeader key={i} topic={topic} entered={true} />
        ))}
      </div>
    );
  },
};
