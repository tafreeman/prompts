import React from "react";
import { DataTableLayout } from "../../layouts/verge-pop/DataTableLayout.tsx";

export default {
  title: "Layouts/Verge Pop/DataTableLayout",
  component: DataTableLayout,
  parameters: {
    layout: "fullscreen",
  },
};

const mockTopic = {
  id: "demo",
  title: "Onboarding Program Comparison",
  subtitle:
    "How structured onboarding stacks up against ad-hoc approaches across key delivery metrics.",
  color: "#8B5CF6",
  colorLight: "#A78BFA",
  colorGlow: "rgba(139,92,246,0.3)",
  icon: "\u25CE",
  tableTitle: "Onboarding Effectiveness Matrix",
  tableHeaders: ["Metric", "Ad-Hoc", "Structured", "AI-Assisted"],
  headerColors: ["transparent", "#FB923C", "#34D399", "#A78BFA"],
  tableRows: [
    ["Time to first commit", "5 days", "2 days", "1 day"],
    ["Time to first feature", "6 weeks", "3 weeks", "2 weeks"],
    ["Full velocity (weeks)", "16", "10", "6"],
    ["90-day retention", "72%", "88%", "94%"],
    ["Security clearance gap", "3 days", "0 days", "0 days"],
    ["Mentor hours required", "40 hrs", "24 hrs", "12 hrs"],
    ["Satisfaction score", "3.2/5", "4.1/5", "4.7/5"],
  ],
  callout:
    "AI-assisted onboarding cuts ramp-up time by 60% while improving retention and satisfaction.",
};

export const Default = {
  args: {
    topic: mockTopic,
    onBack: () => window.history.back(),
  },
};
