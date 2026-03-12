/**
 * ui-strings.js
 * ─────────────────────────────────────────────────────────────────────────────
 * All user-facing UI label strings in one place.
 * Import { UI } wherever you need a label — never hardcode display text inline.
 *
 * Categories:
 *   SHELL     — app chrome, navigation, version picker
 *   SELECTOR  — theme selector start screen
 *   FOOTER    — landing-page footer controls
 *   LANDING   — landing tile CTA
 *   SECTION   — reusable section divider labels (used across many screens)
 *   CHECKLIST — tool-checklist screen labels
 *   WORKFLOW  — step-type badges
 *   OP        — one-pager screen micro-labels
 *   EYEBROW   — fallback eyebrow/kicker strings (used when topic.eyebrow is absent)
 *   SETTINGS  — settings panel headings + labels
 */

export const UI = {

  // ── Shell ──────────────────────────────────────────────────────────────────
  SHELL: {
    back:          "← Back",
    reset:         "↺",
    resetTitle:    "Reset to deck theme",
    editTheme:     "✎",                   // appended to theme name: "Midnight Teal ✎"
    versionLabel:  "Version",
  },

  // ── Theme selector (start screen) ─────────────────────────────────────────
  SELECTOR: {
    eyebrow:    "GenAI Transformation",
    heading:    "Choose Your Theme",
    subheading: "Select a visual style for the advocacy deck",
    fontLabel:  "Aa",                     // prefix in font preview "Aa Inter"
  },

  // ── Landing footer controls ────────────────────────────────────────────────
  FOOTER: {
    settings:        "Settings",
    settingsTitle:   "Open settings panel",
    layoutFamilies: [
      { key: "native",   label: "Native" },
      { key: "base",     label: "Base Style" },
      { key: "verge",    label: "Verge Style" },
      { key: "handbook", label: "Handbook Style" },
    ],
  },

  // ── Landing tile ──────────────────────────────────────────────────────────
  LANDING: {
    cta:    "Explore",
    ctaArrow: "→",
  },

  // ── Reusable section dividers ─────────────────────────────────────────────
  SECTION: {
    snapshot:           "Snapshot",
    overview:           "Overview",
    whatItCovers:       "What It Covers",
    corePrinciple:      "Core Principle",
    talkingPoints:      "Talking Points",
    bottomLine:         "Bottom Line",
    processFlow:        "Process Flow & Personas",
    dataClassification: "Data Classification",
    storyNotes:         "Story Notes",
  },

  // ── Checklist screen ──────────────────────────────────────────────────────
  CHECKLIST: {
    approved:      "Approved",
    awarenessOnly: "Awareness Only",
    prohibited:    "Prohibited",
  },

  // ── Workflow step-type badges ─────────────────────────────────────────────
  WORKFLOW: {
    ai:    "AI",
    human: "Human",
  },

  // ── One-pager micro-labels ────────────────────────────────────────────────
  OP: {
    moduleBadge: (order) => `Module ${order ?? "—"} · One-Pager`,
    sprintCycle: "1 wk",
    sprintCycleLabel: "Sprint Cycle",
    totalSteps: "Total Steps",
    aiSteps: "AI Steps",
    humanGates: "Human Gates",
    restricted: "Restricted",
    required: "Day 1",
    requiredLabel: "Required",
    tolerance: "Zero",
    toleranceLabel: "Tolerance",
    approved: "Approved",
    approvedLabel: "Approved",
  },

  // ── Eyebrow / kicker fallbacks (per-screen defaults) ─────────────────────
  EYEBROW: {
    overview:       "Overview",
    governance:     "Governance",
    servicePlatform:"Service Platform",
    chapter:        "Chapter",
    index:          "Index",
    practiceAreas:  "Practice Areas",
    process:        "Process",
  },

  // ── Settings panel headings & labels ──────────────────────────────────────
  SETTINGS: {
    title:        "Settings",
    close:        "✕",
    deckSection:  "Deck",
    themeSection: "Theme",
    styleSection: "Style",
    layoutSection:"Layout Family",
    layoutNote:   "Only applies to decks with non-standard layouts",
    topicsUnit:   "topics",
  },
};

export default UI;
