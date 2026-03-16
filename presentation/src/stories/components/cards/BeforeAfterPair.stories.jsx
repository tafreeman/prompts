import React from "react";
import BeforeAfterPair from "../../../components/cards/BeforeAfterPair.tsx";

export default {
  title: "Cards/BeforeAfterPair",
  component: BeforeAfterPair,
  parameters: {
    layout: "padded",
  },
  argTypes: {
    color: { control: "color" },
    layout: { control: { type: "radio" }, options: ["horizontal", "vertical"] },
  },
};

export const Default = {
  args: {
    beforeTitle: "Challenge",
    beforeBody:
      "Developers used ad-hoc, inconsistent prompts. Each engineer had their own style, producing wildly different AI output quality with no shared baseline.",
    afterTitle: "Solution",
    afterBody:
      "Established versioned prompt templates with embedded architecture context. All engineers now start from the same high-quality foundation.",
    color: "#F59E0B",
    layout: "horizontal",
  },
  render: (args) => (
    <div style={{ maxWidth: 680 }}>
      <BeforeAfterPair {...args} />
    </div>
  ),
};

export const Vertical = {
  args: {
    beforeTitle: "Before",
    beforeBody:
      "Code reviews were manual and inconsistent — reviewers applied personal standards rather than a shared checklist, letting subtle issues slip through.",
    afterTitle: "After",
    afterBody:
      "Structured review gates with AI-assisted diff summaries. Every PR evaluated against a documented checklist before merge is permitted.",
    color: "#22D3EE",
    layout: "vertical",
  },
  render: (args) => (
    <div style={{ maxWidth: 420 }}>
      <BeforeAfterPair {...args} />
    </div>
  ),
};

export const GovernanceExample = {
  args: {
    beforeTitle: "No Governance",
    beforeBody:
      "AI-generated code went straight to review with no context. Reviewers had no way to verify whether the model understood the system's constraints.",
    afterTitle: "Governed Process",
    afterBody:
      "Every AI task now includes an architecture brief. Reviewers verify the model worked within approved patterns and coding standards.",
    color: "#8B5CF6",
    layout: "horizontal",
  },
  render: (args) => (
    <div style={{ maxWidth: 680 }}>
      <BeforeAfterPair {...args} />
    </div>
  ),
};

export const StackedExamples = {
  render: () => {
    const pairs = [
      {
        beforeTitle: "Ad-Hoc Prompts",
        beforeBody: "No shared prompt baseline. Quality was engineer-dependent and unrepeatable.",
        afterTitle: "Versioned Templates",
        afterBody: "24 active templates pinned in source control with embedded context and review guidelines.",
        color: "#F59E0B",
      },
      {
        beforeTitle: "Manual Testing",
        beforeBody: "Tests written after the fact, coverage untracked, and flaky tests left unresolved.",
        afterTitle: "Test-Driven Delivery",
        afterBody: "1,400+ tests written test-first. CI gate enforces 80% coverage on every PR.",
        color: "#10B981",
      },
      {
        beforeTitle: "Undocumented Decisions",
        beforeBody: "Architectural choices made verbally in standups with no written rationale.",
        afterTitle: "ADR Discipline",
        afterBody: "47 decisions logged with evidence, trade-offs, and reviewers. Fully auditable.",
        color: "#22D3EE",
      },
    ];

    return (
      <div style={{ display: "flex", flexDirection: "column", gap: 24, maxWidth: 680 }}>
        {pairs.map((p, i) => (
          <BeforeAfterPair key={i} layout="horizontal" {...p} />
        ))}
      </div>
    );
  },
};
