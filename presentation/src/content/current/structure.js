/**
 * Current (Advocacy) Deck — Structure (layout skeleton).
 * Text content lives in the companion `content.json`.
 *
 * This is the original advocacy deck that was previously inline in App.v14.jsx.
 */

export const structure = {
  themeId: "midnight-teal",

  introStatColors: ["#22D3EE", "#34D399", "#10B981", "#A78BFA"],

  sprintNodes: [
    { abbr: "RQ", label: "Requirements",   type: "human" },
    { abbr: "UI", label: "UI Mockup",      type: "human" },
    { abbr: "AD", label: "AI Converts AC", type: "ai"    },
    { abbr: "RF", label: "AC Refinement",  type: "human" },
    { abbr: "RV", label: "Human Review",   type: "human" },
    { abbr: "AC", label: "AI Gen Code",    type: "ai"    },
    { abbr: "CO", label: "Code Output",    type: "ai"    },
    { abbr: "PR", label: "Code Review",    type: "human" },
    { abbr: "QA", label: "Testing",        type: "human" },
    { abbr: "FX", label: "Defect Fix",     type: "human" },
    { abbr: "DP", label: "Deploy",         type: "human" },
    { abbr: "RO", label: "Client Review",  type: "human" },
  ],

  shellSlides: [],

  contentSlides: [
    {
      id: "human", order: 4, role: "evidence", layout: "stat-cards",
      num: "01", icon: "\u25C9",
      color: "#0891B2", colorLight: "#22D3EE", colorGlow: "rgba(8,145,178,0.3)",
    },
    {
      id: "hurdles", order: 5, role: "challenges", layout: "before-after",
      num: "02", icon: "\u2B21",
      color: "#F59E0B", colorLight: "#FBBF24", colorGlow: "rgba(245,158,11,0.3)",
    },
    {
      id: "sprint", order: 6, role: "process", layout: "process-cycle",
      num: "04", icon: "\u27F3",
      color: "#8B5CF6", colorLight: "#A78BFA", colorGlow: "rgba(139,92,246,0.3)",
    },
    {
      id: "future", order: 7, role: "vision", layout: "h-strip",
      num: "03", icon: "\u25B3",
      color: "#10B981", colorLight: "#34D399", colorGlow: "rgba(16,185,129,0.3)",
    },
  ],
};
