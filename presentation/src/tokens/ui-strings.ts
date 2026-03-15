/**
 * ui-strings.ts
 * ─────────────────────────────────────────────────────────────────────────────
 * All user-facing UI label strings in one place.
 * Import { UI } wherever you need a label — never hardcode display text inline.
 */

export interface LayoutFamilyOption {
  readonly key: string;
  readonly label: string;
}

export interface UIStrings {
  readonly SHELL: {
    readonly back: string;
    readonly reset: string;
    readonly resetTitle: string;
    readonly editTheme: string;
    readonly versionLabel: string;
  };
  readonly SELECTOR: {
    readonly eyebrow: string;
    readonly heading: string;
    readonly subheading: string;
    readonly fontLabel: string;
  };
  readonly FOOTER: {
    readonly settings: string;
    readonly settingsTitle: string;
    readonly layoutFamilies: readonly LayoutFamilyOption[];
  };
  readonly LANDING: {
    readonly cta: string;
    readonly ctaArrow: string;
  };
  readonly SECTION: {
    readonly snapshot: string;
    readonly overview: string;
    readonly whatItCovers: string;
    readonly corePrinciple: string;
    readonly talkingPoints: string;
    readonly bottomLine: string;
    readonly processFlow: string;
    readonly dataClassification: string;
    readonly storyNotes: string;
  };
  readonly CHECKLIST: {
    readonly approved: string;
    readonly awarenessOnly: string;
    readonly prohibited: string;
  };
  readonly WORKFLOW: {
    readonly ai: string;
    readonly human: string;
  };
  readonly OP: {
    readonly moduleBadge: (order?: number | null) => string;
    readonly sprintCycle: string;
    readonly sprintCycleLabel: string;
    readonly totalSteps: string;
    readonly aiSteps: string;
    readonly humanGates: string;
    readonly restricted: string;
    readonly required: string;
    readonly requiredLabel: string;
    readonly tolerance: string;
    readonly toleranceLabel: string;
    readonly approved: string;
    readonly approvedLabel: string;
  };
  readonly EYEBROW: {
    readonly overview: string;
    readonly governance: string;
    readonly servicePlatform: string;
    readonly chapter: string;
    readonly index: string;
    readonly practiceAreas: string;
    readonly process: string;
  };
  readonly SETTINGS: {
    readonly title: string;
    readonly close: string;
    readonly deckSection: string;
    readonly themeSection: string;
    readonly styleSection: string;
    readonly layoutSection: string;
    readonly layoutNote: string;
    readonly topicsUnit: string;
  };
}

export const UI: UIStrings = {

  // ── Shell ──────────────────────────────────────────────────────────────────
  SHELL: {
    back:          "← Back",
    reset:         "↺",
    resetTitle:    "Reset to deck theme",
    editTheme:     "✎",
    versionLabel:  "Version",
  },

  // ── Theme selector (start screen) ─────────────────────────────────────────
  SELECTOR: {
    eyebrow:    "GenAI Transformation",
    heading:    "Choose Your Theme",
    subheading: "Select a visual style for the advocacy deck",
    fontLabel:  "Aa",
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
