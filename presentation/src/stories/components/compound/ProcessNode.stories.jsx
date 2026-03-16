import React from "react";
import { ProcessNode } from "../../../components/compound/ProcessNode.tsx";

export default {
  title: "Compound/ProcessNode",
  component: ProcessNode,
  parameters: {
    layout: "padded",
  },
  argTypes: {
    color: { control: "color" },
    size: { control: { type: "select" }, options: ["sm", "md", "lg"] },
    status: { control: { type: "select" }, options: ["pending", "active", "complete"] },
    type: { control: { type: "radio" }, options: ["ai", "human"] },
  },
};

export const Default = {
  args: {
    label: "Generate Draft",
    icon: "🤖",
    size: "md",
    status: "active",
    type: "ai",
  },
  render: (args) => (
    <div style={{ display: "flex", justifyContent: "center", padding: 32 }}>
      <ProcessNode {...args} />
    </div>
  ),
};

export const HumanNode = {
  args: {
    label: "Review & Approve",
    icon: "👤",
    size: "md",
    status: "active",
    type: "human",
  },
  render: (args) => (
    <div style={{ display: "flex", justifyContent: "center", padding: 32 }}>
      <ProcessNode {...args} />
    </div>
  ),
};

export const AllSizes = {
  render: () => (
    <div style={{ display: "flex", alignItems: "flex-end", gap: 40, padding: 32 }}>
      <ProcessNode label="Small" icon="🔍" size="sm" status="active" type="ai" />
      <ProcessNode label="Medium" icon="🔍" size="md" status="active" type="ai" />
      <ProcessNode label="Large" icon="🔍" size="lg" status="active" type="ai" />
    </div>
  ),
};

export const AllStatuses = {
  render: () => (
    <div style={{ display: "flex", alignItems: "flex-end", gap: 40, padding: 32 }}>
      <ProcessNode label="Pending" icon="⏳" size="md" status="pending" type="ai" />
      <ProcessNode label="Active" icon="⚡" size="md" status="active" type="ai" />
      <ProcessNode label="Complete" icon="✅" size="md" status="complete" type="ai" />
    </div>
  ),
};

export const CodeReviewCycle = {
  render: () => {
    const nodes = [
      { label: "Write Prompt", icon: "📝", type: "human", status: "complete" },
      { label: "Generate Code", icon: "🤖", type: "ai", status: "complete" },
      { label: "Run Tests", icon: "🧪", type: "ai", status: "active" },
      { label: "Review PR", icon: "🔍", type: "human", status: "pending" },
      { label: "Merge", icon: "✅", type: "human", status: "pending" },
    ];

    return (
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 24,
          padding: 32,
          flexWrap: "wrap",
        }}
      >
        {nodes.map((n, i) => (
          <React.Fragment key={i}>
            <ProcessNode
              label={n.label}
              icon={n.icon}
              type={n.type}
              status={n.status}
              size="md"
            />
            {i < nodes.length - 1 && (
              <div style={{ color: "#4B5563", fontSize: 20, flexShrink: 0 }}>→</div>
            )}
          </React.Fragment>
        ))}
      </div>
    );
  },
};

export const AIvsHumanComparison = {
  render: () => (
    <div style={{ display: "flex", gap: 48, padding: 32, flexWrap: "wrap" }}>
      <div style={{ display: "flex", flexDirection: "column", gap: 24, alignItems: "center" }}>
        <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: 1.5, opacity: 0.5 }}>
          AI Steps
        </div>
        <ProcessNode label="Generate Draft" icon="🤖" type="ai" status="active" size="md" />
        <ProcessNode label="Run Lint" icon="🔧" type="ai" status="active" size="md" />
        <ProcessNode label="Write Tests" icon="🧪" type="ai" status="pending" size="md" />
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 24, alignItems: "center" }}>
        <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: 1.5, opacity: 0.5 }}>
          Human Steps
        </div>
        <ProcessNode label="Define Context" icon="📋" type="human" status="complete" size="md" />
        <ProcessNode label="Review PR" icon="👁️" type="human" status="active" size="md" />
        <ProcessNode label="Approve Merge" icon="✅" type="human" status="pending" size="md" />
      </div>
    </div>
  ),
};
