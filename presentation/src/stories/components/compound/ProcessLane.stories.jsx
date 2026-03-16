import React from "react";
import { ProcessLane } from "../../../components/compound/ProcessLane.tsx";

export default {
  title: "Compound/ProcessLane",
  component: ProcessLane,
  parameters: {
    layout: "padded",
  },
  argTypes: {
    color: { control: "color" },
    variant: {
      control: { type: "select" },
      options: ["linear", "circular"],
    },
  },
};

const linearSteps = [
  { label: "Gather requirements from stakeholder interviews", description: "Product and engineering align on acceptance criteria.", type: "human" },
  { label: "AI generates initial code scaffold", description: "LLM produces boilerplate from architecture context and templates.", type: "ai" },
  { label: "Human review and refinement", description: "Developer validates output against coding standards and security policy.", type: "human" },
];

export const Linear = {
  args: {
    persona: "Software Engineer — AI-Assisted Delivery",
    steps: linearSteps,
    variant: "linear",
  },
  render: (args) => (
    <div style={{ maxWidth: 380 }}>
      <ProcessLane {...args} />
    </div>
  ),
};

const circularSteps = [
  { label: "Plan sprint backlog", description: "Team selects stories and sizes effort.", type: "human" },
  { label: "AI drafts implementation", description: "Code generation with embedded architecture context.", type: "ai" },
  { label: "Code review checkpoint", description: "Pull request review with project-specific checklists.", type: "human" },
  { label: "Automated testing", description: "Unit, integration, and security scans run in CI.", type: "ai" },
  { label: "Deploy to staging", description: "Validated artifacts promoted to staging environment.", type: "human" },
];

export const Circular = {
  args: {
    persona: "Sprint Cycle — Continuous Delivery",
    steps: circularSteps,
    variant: "circular",
  },
  render: (args) => (
    <div style={{ maxWidth: 380 }}>
      <ProcessLane {...args} />
    </div>
  ),
};

const manySteps = [
  { label: "Discovery & scoping", description: "Identify business problem and stakeholders.", type: "human" },
  { label: "Data collection", description: "Ingest raw data from source systems.", type: "ai" },
  { label: "Feature engineering", description: "Transform raw signals into model-ready features.", type: "ai" },
  { label: "Model training", description: "Train candidate models with hyperparameter search.", type: "ai" },
  { label: "Human evaluation", description: "Subject-matter experts validate model outputs.", type: "human" },
  { label: "Governance review", description: "Security, legal, and compliance sign-off.", type: "human" },
  { label: "Production deployment", description: "Model packaged and deployed behind API gateway.", type: "human" },
];

export const ManySteps = {
  args: {
    persona: "ML Engineer — End-to-End Pipeline",
    steps: manySteps,
    variant: "linear",
    color: "#8B5CF6",
  },
  render: (args) => (
    <div style={{ maxWidth: 420 }}>
      <ProcessLane {...args} />
    </div>
  ),
};
