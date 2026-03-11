import React, { useState, useEffect, useRef, useCallback, createContext, useContext } from "react";
import PropTypes from "prop-types";

const IS_SINGLE_FILE_BUILD = import.meta.env.MODE === "single-file";

// ─── HERO IMAGERY ───
const _IMGBASE = import.meta.env.BASE_URL ?? "./";
const HERO_IMGS = {
  carrierFleet:     _IMGBASE + "images/carrier-fleet.jpg",
  helicopterRappel: _IMGBASE + "images/helicopter-rappel.jpg",
  droneDeck:        _IMGBASE + "images/drone-deck.jpg",
  carrierOps:       _IMGBASE + "images/carrier-ops.jpg",
  uavSunset:        _IMGBASE + "images/uav-sunset.jpg",
};

// ─── TYPE SCALE ───
const TYPE_SCALE = {
  STAT:    { fontSize: 48, fontWeight: 800, letterSpacing: -1.5, lineHeight: 1 },
  HERO:    { fontSize: 44, fontWeight: 800, letterSpacing: -1, lineHeight: 0.96 },
  TITLE:   { fontSize: 32, fontWeight: 700, letterSpacing: -0.5, lineHeight: 1.05 },
  SECTION: { fontSize: 24, fontWeight: 700, letterSpacing: 0, lineHeight: 1.12 },
  CARD:    { fontSize: 18, fontWeight: 600, letterSpacing: 0, lineHeight: 1.2 },
  BODY:    { fontSize: 16, fontWeight: 400, letterSpacing: 0, lineHeight: 1.6 },
  CAPTION: { fontSize: 13, fontWeight: 500, letterSpacing: 0.5, lineHeight: 1.4 },
  EYEBROW: { fontSize: 11, fontWeight: 700, letterSpacing: 2.5, lineHeight: 1, textTransform: "uppercase" },
};

// ─── THEMES ───
const THEMES = [
  { id: "midnight-teal", name: "Midnight Teal", vibe: "Current Default", fontDisplay: "'Space Grotesk',sans-serif", fontBody: "'DM Sans',sans-serif", bg: "#0B1426", bgCard: "#162240", bgDeep: "#111827", text: "#F0F4F8", textMuted: "#CBD5E1", textDim: "#64748B", accent: "#22D3EE", accentGlow: "rgba(8,145,178,0.3)", gradient: ["#22D3EE", "#10B981"], success: "#10B981", danger: "#EF4444", warning: "#F59E0B", surfaceElevated: "#0A1628" },
  { id: "obsidian-ember", name: "Obsidian & Ember", vibe: "Editorial / Luxury", fontDisplay: "'Playfair Display',serif", fontBody: "'Source Sans 3',sans-serif", bg: "#1A1A1E", bgCard: "#242428", bgDeep: "#2C2C32", text: "#E8E4DF", textMuted: "#9B9590", textDim: "#6B6560", accent: "#D4A853", accentGlow: "rgba(212,168,83,0.25)", gradient: ["#D4A853", "#C75B39"], success: "#5B8A72", danger: "#C75B39", warning: "#D4A853", surfaceElevated: "#141416" },
  { id: "arctic-steel", name: "Arctic Steel", vibe: "Industrial Nordic", fontDisplay: "'JetBrains Mono',monospace", fontBody: "'Nunito Sans',sans-serif", bg: "#0F1318", bgCard: "#171D24", bgDeep: "#1E2630", text: "#D6DDE6", textMuted: "#7B8EA3", textDim: "#4E6178", accent: "#4FC3F7", accentGlow: "rgba(79,195,247,0.2)", gradient: ["#4FC3F7", "#B2EBF2"], success: "#69F0AE", danger: "#FF6B6B", warning: "#FFD54F", surfaceElevated: "#0B1018" },
  { id: "midnight-verdant", name: "Midnight Verdant", vibe: "Organic Tech", fontDisplay: "'Outfit',sans-serif", fontBody: "'Karla',sans-serif", bg: "#0A1628", bgCard: "#112240", bgDeep: "#152A4E", text: "#CCD6F6", textMuted: "#8892B0", textDim: "#5A6480", accent: "#64FFDA", accentGlow: "rgba(100,255,218,0.18)", gradient: ["#64FFDA", "#48BB78"], success: "#64FFDA", danger: "#F78166", warning: "#F1FA8C", surfaceElevated: "#071420" },
  { id: "neon-noir", name: "Neon Noir", vibe: "Cyberpunk / Bold", fontDisplay: "'Chakra Petch',sans-serif", fontBody: "'Barlow',sans-serif", bg: "#050508", bgCard: "#0D0D12", bgDeep: "#14141C", text: "#EAEAF0", textMuted: "#8585A0", textDim: "#55556E", accent: "#00E5FF", accentGlow: "rgba(0,229,255,0.2)", gradient: ["#00E5FF", "#FF2D95"], success: "#AAFF00", danger: "#FF2D95", warning: "#FFD600", surfaceElevated: "#030305" },
  { id: "paper-ink", name: "Paper & Ink", vibe: "Light Editorial", fontDisplay: "'DM Serif Display',serif", fontBody: "'Atkinson Hyperlegible',sans-serif", bg: "#FAF8F5", bgCard: "#FFFFFF", bgDeep: "#F0EDE8", text: "#1A1A2E", textMuted: "#5C5C6F", textDim: "#8E8E9F", accent: "#1E40AF", accentGlow: "rgba(30,64,175,0.12)", gradient: ["#1E40AF", "#7C3AED"], success: "#047857", danger: "#DC2626", warning: "#B45309", surfaceElevated: "#E8E5E0" },
];

const THEME_SELECTOR_FONTS_URL = "https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700&family=Space+Grotesk:wght@500;700&family=Playfair+Display:wght@700&family=JetBrains+Mono:wght@700&family=Outfit:wght@700&family=Chakra+Petch:wght@700&family=DM+Serif+Display&display=swap";

const THEME_FONT_URLS = {
  "midnight-teal": "https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700&family=Space+Grotesk:wght@500;700&display=swap",
  "obsidian-ember": "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Source+Sans+3:wght@400;500;600;700&display=swap",
  "arctic-steel": "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700;800&family=Nunito+Sans:wght@400;500;600;700&display=swap",
  "midnight-verdant": "https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&family=Karla:wght@400;500;600;700&display=swap",
  "neon-noir": "https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=Barlow:wght@400;500;600&display=swap",
  "paper-ink": "https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Atkinson+Hyperlegible:wght@400;700&display=swap",
};

const ThemeCtx = createContext(THEMES[0]);

const positionPropType = PropTypes.shape({
  x: PropTypes.number.isRequired,
  y: PropTypes.number.isRequired,
});

const themePropType = PropTypes.shape({
  id: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  vibe: PropTypes.string.isRequired,
  fontDisplay: PropTypes.string.isRequired,
  fontBody: PropTypes.string.isRequired,
  bg: PropTypes.string.isRequired,
  bgCard: PropTypes.string.isRequired,
  bgDeep: PropTypes.string.isRequired,
  text: PropTypes.string.isRequired,
  textMuted: PropTypes.string.isRequired,
  textDim: PropTypes.string.isRequired,
  accent: PropTypes.string.isRequired,
  accentGlow: PropTypes.string.isRequired,
  gradient: PropTypes.arrayOf(PropTypes.string).isRequired,
  success: PropTypes.string.isRequired,
  danger: PropTypes.string.isRequired,
  warning: PropTypes.string.isRequired,
  surfaceElevated: PropTypes.string.isRequired,
});

const topicCardPropType = PropTypes.shape({
  title: PropTypes.string.isRequired,
  body: PropTypes.string,
  challenge: PropTypes.string,
  fix: PropTypes.string,
  step: PropTypes.string,
  marker: PropTypes.string,
  eyebrow: PropTypes.string,
  highlight: PropTypes.string,
  details: PropTypes.arrayOf(PropTypes.string),
});

const topicResultPropType = PropTypes.shape({
  value: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  detail: PropTypes.string,
});

const topicFocusPanelPropType = PropTypes.shape({
  label: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  body: PropTypes.string.isRequired,
});

const topicCapabilityPropType = PropTypes.shape({
  title: PropTypes.string.isRequired,
  body: PropTypes.string.isRequired,
  marker: PropTypes.string.isRequired,
});

const topicLanePropType = PropTypes.shape({
  title: PropTypes.string.isRequired,
  subtitle: PropTypes.string.isRequired,
  persona: PropTypes.string.isRequired,
  accent: PropTypes.string.isRequired,
  steps: PropTypes.arrayOf(PropTypes.string).isRequired,
});

const topicPropType = PropTypes.shape({
  id: PropTypes.string.isRequired,
  num: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  subtitle: PropTypes.string.isRequired,
  color: PropTypes.string.isRequired,
  colorLight: PropTypes.string.isRequired,
  colorGlow: PropTypes.string,
  optional: PropTypes.bool,
  eyebrow: PropTypes.string,
  summary: PropTypes.string,
  heroPoints: PropTypes.arrayOf(PropTypes.string),
  cards: PropTypes.arrayOf(topicCardPropType),
  talkingPoints: PropTypes.arrayOf(PropTypes.string),
  callout: PropTypes.string.isRequired,
  heroTitle: PropTypes.string,
  kicker: PropTypes.string,
  subkicker: PropTypes.string,
  thesis: PropTypes.string,
  leadershipPoints: PropTypes.arrayOf(PropTypes.string),
  results: PropTypes.arrayOf(topicResultPropType),
  enablementTitle: PropTypes.string,
  enablement: PropTypes.string,
  focusPanels: PropTypes.arrayOf(topicFocusPanelPropType),
  capabilities: PropTypes.arrayOf(topicCapabilityPropType),
  lanes: PropTypes.arrayOf(topicLanePropType),
});

// ─── TOPICS DATA ───
const topics = [
  {
    id: "overview", num: "01", title: "Case Study Overview",
    subtitle: "How the AI-accelerated delivery story unfolds across governance, execution, and scale",
    color: "#67E8F9", colorLight: "#A5F3FC", colorGlow: "rgba(103,232,249,0.24)",
    eyebrow: "Deck Flow",
    summary: "This opener gives the audience the full story in one pass: the mission need, the platform model, the governance proof points, and the path to scale.",
    heroPoints: ["Mission need", "Platform model", "Delivery guardrails", "Scale path"],
    cards: [
      { title: "Mission Need", body: "The agency needed one front door for fragmented IT demand." },
      { title: "Operating Model", body: "The platform links discovery, approval, and procurement handoff." },
      { title: "Human Governance", body: "Speed stayed credible because humans still owned review and release." },
      { title: "What Follows", body: "The next pages prove governance, execution, and scale in detail." },
    ],
    talkingPoints: [
      "Lead with the mission problem before the technology.",
      "Frame the platform as an operating model, not a catalog screen.",
      "Use the rest of the deck as proof of governance and execution.",
      "Keep the throughline on readiness, speed, and controlled handoff.",
    ],
    callout: "Use this slide as the executive opener, then move into the proof pages.",
  },
  {
    id: "platform", num: "Optional", title: "Service Platform",
    subtitle: "One front door for IT demand, approvals, and procurement handoff",
    color: "#38BDF8", colorLight: "#7DD3FC", colorGlow: "rgba(56,189,248,0.28)",
    optional: true,
    eyebrow: "Issue to Impact",
    summary: "The platform creates one governed front door for IT demand, approvals, and procurement continuation, helping users get the right tools faster.",
    heroPoints: ["Unified IT catalogs", "Role-based approvals", "Procurement handoff", "Mission readiness"],
    focusPanels: [
      { label: "Overview", title: "One governed entry point", body: "Discovery, request intake, approvals, and procurement continuation all sit in one flow." },
      { label: "Capability Zoom", title: "What users can do", body: "Users can browse, research, track, and route requests without jumping tools." },
      { label: "Process Zoom", title: "How requests move", body: "Users request. Approvers review. Admins complete procurement in the right tool." },
    ],
    capabilities: [
      { title: "Browse IT Goods", body: "See hardware and software options in one place.", marker: "BG" },
      { title: "Research Solutions", body: "Explore available IT services before submitting demand.", marker: "RS" },
      { title: "Track Requests", body: "Users and admins can see request status clearly.", marker: "TR" },
      { title: "Continue Procurement", body: "Approved demand flows into the right downstream tool.", marker: "CP" },
    ],
    lanes: [
      {
        title: "Review & Request Tool",
        subtitle: "Service Platform",
        persona: "User: Any authorized personnel with agency credentials",
        accent: "#38BDF8",
        steps: [
          "Browse orderable goods and services.",
          "Submit a request form routed to the right approver.",
          "Approve or deny the queued request.",
        ],
      },
      {
        title: "Procurement Tool",
        subtitle: "e.g. Legacy Procurement",
        persona: "User: Admin with procurement permissions",
        accent: "#22D3EE",
        steps: [
          "Approved requests continue in the relevant procurement tool.",
        ],
      },
    ],
    talkingPoints: [
      "Fast-changing IT demand needs one clear front door.",
      "The platform simplifies discovery without weakening control.",
      "Role-based routing keeps the right people in the loop.",
      "The real payoff is faster access and stronger readiness.",
    ],
    callout: "This is not just a catalog. It is a governed path from need to procurement.",
  },
  {
    id: "human", num: "02", title: "Human in the Loop",
    heroTitle: "Human-in-the-Loop Focused AI Development",
    kicker: "AI-Accelerated Delivery",
    subkicker: "Governance-First Delivery",
    subtitle: "AI accelerates delivery. Human judgment governs quality.",
    thesis: "Accelerated by AI. Governed by human expertise.",
    color: "#0891B2", colorLight: "#22D3EE", colorGlow: "rgba(8,145,178,0.3)",
    cards: [
      {
        title: "Governance First", step: "01", marker: "GF",
        eyebrow: "Approvals before acceleration",
        highlight: "Approvals and legal clearance came before acceleration.",
        details: [
          "Risk, legal, and compliance teams approved AI use before production release.",
          "Contract updates included explicit AI language and operating guardrails.",
        ],
      },
      {
        title: "Quality Gates", step: "02", marker: "QG",
        eyebrow: "Human review at every gate",
        highlight: "Every AI-assisted line was reviewed before merge.",
        details: [
          "More time was invested in review discipline, not less.",
          "Unit and integration testing validated output before release.",
          "No merge moved forward until all gates passed.",
        ],
      },
      {
        title: "Context Engineering", step: "03", marker: "PC",
        eyebrow: "Manage context, lower variance",
        highlight: "Standardized prompts, process learning sessions, and developer expertise provided the system the full context.",
        details: [
          "Architecture docs, data models, and coding standards were embedded in prompts.",
          "Variance dropped because outputs stayed anchored to the real system.",
        ],
      },
    ],
    leadershipPoints: [
      "Governance sat inside the workflow, not after the fact.",
      "Humans kept release authority even when AI authored most of the implementation.",
      "Review rigor made speed credible to leadership.",
    ],
    results: [
      { value: "50%", label: "Reduction in development time", detail: "through incorporation of AI tools in development processes" },
      { value: "90%", label: "Of production code developed via AI" },
      { value: "2", label: "Months from idea to production" },
      { value: "0", label: "Critical defects discovered post deployment" },
    ],
    enablementTitle: "Enablement + Outcome",
    enablement: "An internal hackathon built team fluency and confidence, turning experimentation into a repeatable delivery habit.",
    callout: "AI generated code. Humans owned the decisions.",
  },
  {
    id: "hurdles", num: "03", title: "Hurdles We Overcame",
    subtitle: "What changed from day one to delivery",
    color: "#F59E0B", colorLight: "#FBBF24", colorGlow: "rgba(245,158,11,0.3)",
    cards: [
      { title: "Prompt Standardization", challenge: "Ad-hoc prompts created uneven quality and rework.", fix: "Versioned prompt templates added consistent architecture context." },
      { title: "Process Realignment", challenge: "Traditional reviews were not built for AI-assisted output.", fix: "AI-specific review checklists made quality gates explicit." },
      { title: "Governance Clearance", challenge: "Policy approval was required before production use.", fix: "Risk and legal teams were engaged early to set guardrails." },
      { title: "Team Enablement", challenge: "Skill levels with AI tools were uneven across the team.", fix: "A hands-on hackathon built shared confidence before delivery." },
    ],
    callout: "The early friction became the guardrails that let the team move fast later.",
  },
  {
    id: "sprint", num: "04", title: "AI Sprint Cycle",
    subtitle: "Human checkpoints at every stage of AI-assisted delivery",
    color: "#8B5CF6", colorLight: "#A78BFA", colorGlow: "rgba(139,92,246,0.3)",
    callout: "The sprint changed, but human checkpoints stayed embedded throughout delivery.",
  },
  {
    id: "future", num: "05", title: "Looking Ahead",
    subtitle: "Better steering -- not more automation -- is the next multiplier",
    color: "#10B981", colorLight: "#34D399", colorGlow: "rgba(16,185,129,0.3)",
    cards: [
      { title: "Model Steering & Planning", body: "Guardrails move upstream into prompts, tools, and workflow defaults." },
      { title: "Evolved Prompt Library", body: "Prompt assets become reusable, modular, and versioned." },
      { title: "Human-Governed Pipeline", body: "Automation helps at every step, but humans still decide to merge and deploy." },
      { title: "Team Enablement Kit", body: "New team members can learn the playbook in days, not months." },
    ],
    callout: "The playbook is proven. The next gain comes from better steering, not less governance.",
  },
];

// ─── SPRINT NODE ICONS (custom stroke-based SVGs, 24×24 viewBox) ───
const SvgIcon = ({ children }) => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
    strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" style={{ display: "block" }}>
    {children}
  </svg>
);
SvgIcon.propTypes = { children: PropTypes.node };
const SPRINT_ICONS = {
  // Requirements — spec document with bullet rows
  RQ: () => <SvgIcon><rect x="5" y="2" width="14" height="20" rx="1.5"/><line x1="9" y1="7" x2="15" y2="7"/><line x1="9" y1="11" x2="15" y2="11"/><line x1="9" y1="15" x2="13" y2="15"/><circle cx="7" cy="7" r="1" fill="currentColor" stroke="none"/><circle cx="7" cy="11" r="1" fill="currentColor" stroke="none"/><circle cx="7" cy="15" r="1" fill="currentColor" stroke="none"/></SvgIcon>,

  // UI Mockup — split-pane wireframe
  UI: () => <SvgIcon><rect x="2" y="4" width="20" height="16" rx="1.5"/><line x1="2" y1="9" x2="22" y2="9"/><line x1="9" y1="9" x2="9" y2="20"/><rect x="11" y="12" width="8" height="3" rx="0.5" opacity="0.5"/><rect x="11" y="17" width="5" height="1.5" rx="0.5" opacity="0.4"/></SvgIcon>,

  // AI Draft — 4-pointed diamond star (generative spark)
  AD: () => <SvgIcon><path d="M12 2 L14 10 L22 12 L14 14 L12 22 L10 14 L2 12 L10 10 Z"/></SvgIcon>,

  // AC Refine — pencil with underlining stroke
  RF: () => <SvgIcon><path d="M15.5 4.5 L19.5 8.5 L9 19 L5 20 L6 16 Z"/><line x1="13" y1="7" x2="17" y2="11"/><line x1="4" y1="22" x2="20" y2="22"/></SvgIcon>,

  // Human Review — eye with iris detail
  RV: () => <SvgIcon><path d="M2 12 C5 6 19 6 22 12 C19 18 5 18 2 12 Z"/><circle cx="12" cy="12" r="3.5"/><circle cx="12" cy="12" r="1.5" fill="currentColor" stroke="none"/></SvgIcon>,

  // AI Code — brackets with central circuit dot
  AC: () => <SvgIcon><polyline points="8,5 3,12 8,19"/><polyline points="16,5 21,12 16,19"/><circle cx="12" cy="12" r="1.8" fill="currentColor" stroke="none"/><line x1="12" y1="7" x2="12" y2="9.2" opacity="0.5"/><line x1="12" y1="14.8" x2="12" y2="17" opacity="0.5"/></SvgIcon>,

  // Code Output — terminal with prompt cursor
  CO: () => <SvgIcon><rect x="2" y="4" width="20" height="16" rx="2"/><line x1="2" y1="9" x2="22" y2="9"/><circle cx="5.5" cy="6.5" r="0.9" fill="currentColor" stroke="none"/><circle cx="8.5" cy="6.5" r="0.9" fill="currentColor" stroke="none"/><polyline points="6,13 9.5,16 6,19"/><line x1="12" y1="19" x2="18" y2="19"/></SvgIcon>,

  // PR Review — git Y-merge topology
  PR: () => <SvgIcon><circle cx="7" cy="5" r="2"/><circle cx="17" cy="5" r="2"/><circle cx="12" cy="19" r="2"/><path d="M7 7 C7 13 12 17 12 17"/><path d="M17 7 C17 13 12 17 12 17"/></SvgIcon>,

  // Testing — shield with interior checkmark
  QA: () => <SvgIcon><path d="M12 2 L20 5.5 L20 12 C20 16.8 16.5 21 12 22.5 C7.5 21 4 16.8 4 12 L4 5.5 Z"/><polyline points="8.5,12 11,14.5 15.5,9.5"/></SvgIcon>,

  // Fixes — adjustable wrench rotated diagonal
  FX: () => <SvgIcon><path d="M15 5 C18 5 20 7 20 10 C20 12 18.5 13.5 17 14 L7 21 L4 18 L11 10 C10.5 8.5 11 6 12.5 5.5"/><line x1="15.5" y1="8.5" x2="18.5" y2="5.5"/></SvgIcon>,

  // Deploy — rocket with twin exhaust fins
  DP: () => <SvgIcon><path d="M12 2 C12 2 18 8 18 14 L15.5 17 L8.5 17 L6 14 C6 8 12 2 12 2 Z"/><circle cx="12" cy="10" r="2"/><line x1="8.5" y1="17" x2="6" y2="22"/><line x1="15.5" y1="17" x2="18" y2="22"/></SvgIcon>,

  // Client Readout — monitor with rising bar chart
  RO: () => <SvgIcon><rect x="2" y="3" width="20" height="14" rx="1.5"/><line x1="12" y1="17" x2="12" y2="21"/><line x1="7" y1="21" x2="17" y2="21"/><line x1="7" y1="14" x2="7" y2="10"/><line x1="11" y1="14" x2="11" y2="7"/><line x1="15" y1="14" x2="15" y2="11"/><line x1="5.5" y1="14" x2="16.5" y2="14"/></SvgIcon>,
};

// ─── CARD ICONS (for screen markers, tile icons, and badges) ───
const CardIcon = ({ children, size = 20 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor"
    strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" style={{ display: "block" }}>
    {children}
  </svg>
);
CardIcon.propTypes = { children: PropTypes.node, size: PropTypes.number };

const CARD_ICONS = {
  humanInLoop: (size) => <CardIcon size={size}><circle cx="12" cy="7" r="3.5"/><path d="M5 20a7 7 0 0 1 14 0"/><path d="M19 5 A9 9 0 1 1 5 19" strokeDasharray="2.5 1.5"/><polyline points="21.5,2.5 19,5 16.5,2.5"/></CardIcon>,
  governanceScale: (size) => <CardIcon size={size}><line x1="12" y1="3" x2="12" y2="21"/><path d="M5 8h14"/><path d="M7.5 8 L4 15 h7 z"/><path d="M16.5 8 L13 15 h7 z"/><line x1="8" y1="21" x2="16" y2="21"/></CardIcon>,
  qualityGate: (size) => <CardIcon size={size}><rect x="4" y="5" width="3.5" height="14" rx="1"/><rect x="16.5" y="5" width="3.5" height="14" rx="1"/><line x1="7.5" y1="12" x2="16.5" y2="12" strokeDasharray="2 1.5"/><polyline points="12,9 15,12 12,15" /></CardIcon>,
  contextHub: (size) => <CardIcon size={size}><circle cx="12" cy="12" r="2.5"/><circle cx="4" cy="5" r="1.5"/><line x1="5.5" y1="6.5" x2="10" y2="10.5"/><circle cx="20" cy="5" r="1.5"/><line x1="18.5" y1="6.5" x2="14" y2="10.5"/><circle cx="4" cy="19" r="1.5"/><line x1="5.5" y1="17.5" x2="10" y2="13.5"/><circle cx="20" cy="19" r="1.5"/><line x1="18.5" y1="17.5" x2="14" y2="13.5"/></CardIcon>,
  resultsChart: (size) => <CardIcon size={size}><line x1="3" y1="20" x2="21" y2="20"/><rect x="4.5" y="13" width="3.5" height="7" rx="0.5"/><rect x="10.25" y="9" width="3.5" height="11" rx="0.5"/><rect x="16" y="5" width="3.5" height="15" rx="0.5"/></CardIcon>,
  browseCatalog: (size) => <CardIcon size={size}><rect x="3" y="3" width="7.5" height="7.5" rx="1.5"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="1.5"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="1.5"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="1.5"/></CardIcon>,
  researchMagnify: (size) => <CardIcon size={size}><circle cx="10" cy="10" r="6.5"/><line x1="15" y1="15" x2="21" y2="21"/><line x1="8" y1="10" x2="12" y2="10"/><line x1="10" y1="8" x2="10" y2="12"/></CardIcon>,
  trackFlow: (size) => <CardIcon size={size}><circle cx="5" cy="12" r="2" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="2" fill="currentColor" stroke="none"/><circle cx="19" cy="12" r="2" fill="currentColor" stroke="none"/><line x1="7" y1="12" x2="10" y2="12"/><line x1="14" y1="12" x2="17" y2="12"/><polyline points="6,8 12,5 18,8"/></CardIcon>,
  procureHandoff: (size) => <CardIcon size={size}><circle cx="6" cy="12" r="3.5"/><circle cx="18" cy="12" r="3.5"/><line x1="9.5" y1="12" x2="14.5" y2="12"/><polyline points="12.5,9 15,12 12.5,15"/></CardIcon>,
  compassOverview: (size) => <CardIcon size={size}><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="1.5" fill="currentColor" stroke="none"/><line x1="12" y1="3" x2="12" y2="6"/><line x1="12" y1="18" x2="12" y2="21"/><line x1="3" y1="12" x2="6" y2="12"/><line x1="18" y1="12" x2="21" y2="12"/><polyline points="12,7 14,12 12,17 10,12 Z" fill="currentColor" stroke="none" opacity="0.5"/></CardIcon>,
  stepsHurdles: (size) => <CardIcon size={size}><polyline points="3,21 3,15 9,15 9,9 15,9 15,3 21,3"/><line x1="3" y1="21" x2="21" y2="21"/></CardIcon>,
  infinitySprint: (size) => <CardIcon size={size}><path d="M12 12C12 12 9 6 6 6a4 4 0 0 0 0 8c3 0 6-6 6-6s3 6 6 6a4 4 0 0 0 0-8c-3 0-6 6-6 6z"/></CardIcon>,
  horizonFuture: (size) => <CardIcon size={size}><line x1="3" y1="16" x2="21" y2="16"/><line x1="12" y1="14" x2="12" y2="8"/><line x1="7" y1="13" x2="5" y2="8"/><line x1="17" y1="13" x2="19" y2="8"/></CardIcon>,
  marketArch: (size) => <CardIcon size={size}><path d="M5 21 V12 A7 7 0 0 1 19 12 V21"/><line x1="3" y1="21" x2="21" y2="21"/><line x1="9" y1="21" x2="9" y2="14"/><line x1="15" y1="21" x2="15" y2="14"/></CardIcon>,
};

// ─── SPRINT NODES ───
const sprintNodes = [
  { abbr: "RQ", label: "Requirements", type: "human" },
  { abbr: "UI", label: "UI Mockup", type: "human" },
  { abbr: "AD", label: "AI AC Draft", type: "ai" },
  { abbr: "RF", label: "AC Refine", type: "human" },
  { abbr: "RV", label: "Human Review", type: "human" },
  { abbr: "AC", label: "AI Code", type: "ai" },
  { abbr: "CO", label: "Code Output", type: "ai" },
  { abbr: "PR", label: "PR Review", type: "human" },
  { abbr: "QA", label: "Testing", type: "human" },
  { abbr: "FX", label: "Fixes", type: "human" },
  { abbr: "DP", label: "Deploy", type: "human" },
  { abbr: "RO", label: "Client Readout", type: "human" },
];

// ─── BACK BUTTON ───
function BackBtn({ onClick }) {
  const T = useContext(ThemeCtx);
  return (
    <button onClick={onClick} style={{ background: "none", border: "none", color: T.textMuted, ...TYPE_SCALE.CAPTION, cursor: "pointer", fontFamily: T.fontDisplay, marginBottom: 12, display: "flex", alignItems: "center", gap: 8, fontWeight: 700, padding: 0 }}>
      <span style={{ fontSize: 16 }}>&#8592;</span> Back
    </button>
  );
}
BackBtn.propTypes = { onClick: PropTypes.func.isRequired };

let fallbackEntropyCursor = 0;
const FALLBACK_ENTROPY_DIVISOR = 997;

function getRandomUnit() {
  const cryptoApi = globalThis.crypto;

  if (cryptoApi && typeof cryptoApi.getRandomValues === "function") {
    return cryptoApi.getRandomValues(new Uint32Array(1))[0] / 0x100000000;
  }

  fallbackEntropyCursor = (fallbackEntropyCursor + 619) % FALLBACK_ENTROPY_DIVISOR;
  return fallbackEntropyCursor / FALLBACK_ENTROPY_DIVISOR;
}

// ─── PARTICLES (reduced to 20) ───
function Particles({ color, active }) {
  const canvasRef = useRef(null);
  const pRef = useRef([]);
  const animRef = useRef(null);
  useEffect(() => {
    const c = canvasRef.current;
    if (!c) return;
    const ctx = c.getContext("2d");
    c.width = c.offsetWidth * 2;
    c.height = c.offsetHeight * 2;
    ctx.scale(2, 2);
    const W = c.offsetWidth, H = c.offsetHeight;
    pRef.current = [];
    for (let i = 0; i < 20; i++) {
      pRef.current.push({
        x: getRandomUnit() * W, y: getRandomUnit() * H,
        vx: (getRandomUnit() - 0.5) * 0.4, vy: (getRandomUnit() - 0.5) * 0.4,
        r: getRandomUnit() * 2 + 0.8, o: getRandomUnit() * 0.4 + 0.1, life: getRandomUnit() * 100,
      });
    }
    function draw() {
      ctx.clearRect(0, 0, W, H);
      pRef.current.forEach(p => {
        p.life++;
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > W) p.vx *= -1;
        if (p.y < 0 || p.y > H) p.vy *= -1;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = color + Math.round(p.o * 255).toString(16).padStart(2, "0");
        ctx.fill();
      });
      animRef.current = requestAnimationFrame(draw);
    }
    if (active) draw();
    return () => cancelAnimationFrame(animRef.current);
  }, [color, active]);
  return <canvas ref={canvasRef} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", pointerEvents: "none", opacity: active ? 1 : 0, transition: "opacity 0.8s" }} />;
}
Particles.propTypes = {
  color: PropTypes.string.isRequired,
  active: PropTypes.bool.isRequired,
};

// ─── COMET TRANSITION ───
function CometTransition({ from, color, active, onDone }) {
  const onDoneRef = useRef(onDone);
  onDoneRef.current = onDone;
  const [phase, setPhase] = useState("idle");
  useEffect(() => {
    if (!active || !from) return;
    setPhase("idle");
    const t1 = requestAnimationFrame(() => { requestAnimationFrame(() => setPhase("launch")); });
    const t2 = setTimeout(() => { setPhase("done"); onDoneRef.current(); }, 700);
    return () => { cancelAnimationFrame(t1); clearTimeout(t2); };
  }, [active, from]);
  if (!active || !from) return null;
  const tx = (typeof globalThis.window !== "undefined" ? globalThis.window.innerWidth / 2 : 500) - from.x;
  const ty = (typeof globalThis.window !== "undefined" ? globalThis.window.innerHeight / 2 : 400) - from.y;
  return (
    <div style={{ position: "fixed", inset: 0, zIndex: 100, pointerEvents: "none", overflow: "hidden" }}>
      <div style={{ position: "absolute", left: from.x - 10, top: from.y - 10, width: 20, height: 20, borderRadius: "50%", background: color, boxShadow: `0 0 30px 10px ${color}, 0 0 60px 20px ${color}80, 0 0 4px 2px #FFFFFF`, transform: phase === "launch" ? `translate(${tx}px, ${ty}px) scale(0.3)` : "translate(0,0) scale(1)", opacity: phase === "launch" ? 0.2 : 1, transition: "transform 0.6s cubic-bezier(0.16,1,0.3,1), opacity 0.6s ease" }} />
      {[...new Array(8)].map((_, i) => (
        <div key={i} style={{ position: "absolute", left: from.x - (6 - i * 0.5), top: from.y - (6 - i * 0.5), width: (12 - i), height: (12 - i), borderRadius: "50%", background: color, opacity: phase === "launch" ? 0 : (0.5 - i * 0.06), transform: phase === "launch" ? `translate(${tx * (1 - i * 0.08)}px, ${ty * (1 - i * 0.08)}px)` : "translate(0,0)", transition: `transform ${0.6 + i * 0.03}s cubic-bezier(0.16,1,0.3,1) ${i * 0.02}s, opacity 0.5s ease ${i * 0.02}s` }} />
      ))}
      <div style={{ position: "absolute", left: "50%", top: "50%", width: phase === "launch" ? 200 : 0, height: phase === "launch" ? 200 : 0, marginLeft: phase === "launch" ? -100 : 0, marginTop: phase === "launch" ? -100 : 0, borderRadius: "50%", border: `2px solid ${color}60`, background: `${color}08`, transition: "all 0.4s 0.4s ease-out", opacity: phase === "launch" ? 0 : 1 }} />
    </div>
  );
}
CometTransition.propTypes = {
  from: positionPropType,
  color: PropTypes.string,
  active: PropTypes.bool.isRequired,
  onDone: PropTypes.func.isRequired,
};

// ─── TITLE REVEAL (replaces ThematicIntro) ───
function TitleReveal({ onComplete }) {
  const T = useContext(ThemeCtx);
  const [entered, setEntered] = useState(false);
  const [fading, setFading] = useState(false);
  const onCompleteRef = useRef(onComplete);
  onCompleteRef.current = onComplete;

  const stats = [
    { val: "~40%", lbl: "Productivity Uplift", color: T.gradient ? T.gradient[0] : T.accent },
    { val: "2 mo", lbl: "To Production", color: T.gradient ? T.gradient[1] : T.success },
    { val: "0", lbl: "Critical Defects", color: T.success },
    { val: "~90%", lbl: "AI-Assisted Code", color: T.accent },
  ];

  const proceed = useCallback(() => {
    if (fading) return;
    setFading(true);
    setTimeout(() => onCompleteRef.current(), 600);
  }, [fading]);

  useEffect(() => {
    const t1 = setTimeout(() => setEntered(true), 100);
    const t2 = setTimeout(() => proceed(), 2500);
    return () => { clearTimeout(t1); clearTimeout(t2); };
  }, [proceed]);

  useEffect(() => {
    const onKey = (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); proceed(); } };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [proceed]);

  return (
    <div onClick={proceed} style={{
      position: "fixed", inset: 0, zIndex: 200, cursor: "pointer",
      backgroundImage: `url(${HERO_IMGS.carrierFleet})`,
      backgroundSize: "cover", backgroundPosition: "center",
      display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
      opacity: fading ? 0 : 1, transition: "opacity 0.6s ease",
    }}>
      <div style={{ position: "absolute", inset: 0, background: `linear-gradient(160deg, ${T.surfaceElevated}F0, ${T.bg}E0, ${T.bgDeep}D8)`, pointerEvents: "none" }} />
      {/* Gradient sweep decoration */}
      <div style={{ position: "absolute", inset: 0, background: `radial-gradient(ellipse at 30% 40%, ${T.accent}12, transparent 60%), radial-gradient(ellipse at 70% 60%, ${T.gradient ? T.gradient[1] + "10" : "transparent"}, transparent 50%)`, pointerEvents: "none" }} />

      <div style={{ position: "relative", zIndex: 2, display: "flex", flexDirection: "column", alignItems: "center", padding: "0 32px" }}>
        {/* Eyebrow */}
        <div style={{
          ...TYPE_SCALE.EYEBROW, fontFamily: T.fontDisplay, color: T.textDim, marginBottom: 16,
          opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(12px)",
          transition: "all 0.5s 0.2s ease",
        }}>AI-Assisted Delivery</div>

        {/* Title */}
        <h1 style={{
          fontFamily: T.fontDisplay, ...TYPE_SCALE.HERO, fontSize: 52, color: T.text,
          textAlign: "center", margin: "0 0 8px",
          opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(20px)",
          transition: "all 0.6s 0.4s ease",
        }}>GenAI Transformation</h1>

        {/* Subtitle */}
        <p style={{
          ...TYPE_SCALE.CARD, fontStyle: "italic", textAlign: "center", margin: "0 0 32px",
          opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(12px)",
          transition: "all 0.5s 0.6s ease",
        }}>
          <span style={{ background: `linear-gradient(90deg, ${T.gradient ? T.gradient[0] : T.accent}, ${T.gradient ? T.gradient[1] : T.accent})`, WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
            From prototype to production in 2 months
          </span>
        </p>

        {/* Stats */}
        <div style={{
          display: "flex", gap: 32,
          opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(12px)",
          transition: "all 0.5s 0.8s ease",
        }}>
          {stats.map((s, i) => (
            <div key={i} style={{ textAlign: "center" }}>
              <div style={{ fontFamily: T.fontDisplay, fontSize: 28, fontWeight: 700, color: s.color }}>{s.val}</div>
              <div style={{ ...TYPE_SCALE.EYEBROW, fontSize: 10, color: T.textMuted, marginTop: 2 }}>{s.lbl}</div>
            </div>
          ))}
        </div>

        <div style={{ ...TYPE_SCALE.EYEBROW, fontSize: 10, color: T.textDim, marginTop: 28, opacity: entered ? 0.6 : 0, transition: "opacity 0.5s 1s ease" }}>
          Press Enter or click to continue
        </div>
      </div>
    </div>
  );
}
TitleReveal.propTypes = { onComplete: PropTypes.func.isRequired };

// ─── THEME SELECTOR ───
function ThemeSelector({ onSelect }) {
  const [hovered, setHovered] = useState(null);
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 50); return () => clearTimeout(t); }, []);

  return (
    <div style={{ minHeight: "100vh", background: "#08101C", display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", padding: "40px 48px" }}>
      {!IS_SINGLE_FILE_BUILD && <link href={THEME_SELECTOR_FONTS_URL} rel="stylesheet" />}
      <div style={{ textAlign: "center", marginBottom: 40, opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(20px)", transition: "all 0.6s ease" }}>
        <div style={{ ...TYPE_SCALE.EYEBROW, fontFamily: "'Space Grotesk',sans-serif", color: "#64748B", marginBottom: 12 }}>GenAI Transformation</div>
        <h1 style={{ fontFamily: "'Space Grotesk',sans-serif", ...TYPE_SCALE.HERO, fontSize: 40, color: "#F0F4F8", margin: "0 0 10px" }}>Choose Your Theme</h1>
        <p style={{ ...TYPE_SCALE.CAPTION, color: "#94A3B8", margin: 0 }}>Select a visual style for the advocacy deck</p>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 16, maxWidth: 900, width: "100%" }}>
        {THEMES.map((t, i) => {
          const isH = hovered === t.id;
          return (
            <button key={t.id} onClick={() => onSelect(t)} onMouseEnter={() => setHovered(t.id)} onMouseLeave={() => setHovered(null)}
              style={{
                cursor: "pointer", borderRadius: 14, overflow: "hidden",
                border: `1px solid ${isH ? t.accent + "60" : "rgba(255,255,255,0.06)"}`,
                boxShadow: isH ? `0 0 30px ${t.accentGlow}` : "0 2px 12px rgba(0,0,0,0.3)",
                transition: "all 0.3s ease", opacity: entered ? 1 : 0, transitionDelay: `${0.1 + i * 0.06}s`,
                background: "none", padding: 0, textAlign: "left", width: "100%",
              }}>
              <div style={{ background: t.bg, padding: "20px 18px 14px", position: "relative" }}>
                <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: 3, background: `linear-gradient(90deg, ${t.gradient[0]}, ${t.gradient[1]})` }} />
                <div style={{ fontFamily: t.fontDisplay, ...TYPE_SCALE.CARD, color: t.text, marginBottom: 4 }}>{t.name}</div>
                <div style={{ fontSize: 10, color: t.textDim, textTransform: "uppercase", letterSpacing: 1 }}>{t.vibe}</div>
              </div>
              <div style={{ background: t.bgCard, padding: "14px 18px 16px" }}>
                <div style={{ display: "flex", gap: 6, marginBottom: 10 }}>
                  {[t.accent, t.gradient[1], t.textDim].map((c, j) => <div key={j} style={{ flex: 1, height: 6, borderRadius: 3, background: c, opacity: 0.6 }} />)}
                </div>
                <div style={{ fontSize: 11, color: t.textMuted, lineHeight: 1.4 }}>
                  <span style={{ color: t.accent, fontWeight: 600 }}>Aa</span> {t.fontDisplay.split(",")[0].replace(/'/g, "")}
                </div>
                <div style={{ display: "flex", gap: 5, marginTop: 8 }}>
                  {[t.bg, t.bgCard, t.accent, t.gradient[1]].map((c, j) => <div key={j} style={{ width: 14, height: 14, borderRadius: "50%", background: c, border: "1px solid rgba(255,255,255,0.1)" }} />)}
                </div>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
ThemeSelector.propTypes = { onSelect: PropTypes.func.isRequired };

// ─── LANDING TILE ───
function LandingTile({ topic, onClick, hovered, onHover, borderVariant }) {
  const T = useContext(ThemeCtx);
  const h = hovered === topic.id;
  const dimmed = hovered !== null && !h;
  const borderStyle = borderVariant === "left"
    ? { borderLeft: `3px solid ${h ? topic.color : topic.color + "40"}`, borderTop: "none" }
    : { borderTop: `3px solid ${h ? topic.color : topic.color + "40"}`, borderLeft: "none" };

  const TILE_ICONS = {
    overview: CARD_ICONS.compassOverview,
    human: CARD_ICONS.humanInLoop,
    hurdles: CARD_ICONS.stepsHurdles,
    sprint: CARD_ICONS.infinitySprint,
    future: CARD_ICONS.horizonFuture,
    platform: CARD_ICONS.marketArch,
  };
  const TileIcon = TILE_ICONS[topic.id];

  return (
    <div
      onClick={(e) => { const r = e.currentTarget.getBoundingClientRect(); onClick(topic.id, { x: r.left + r.width / 2, y: r.top + r.height / 2 }); }}
      onMouseEnter={() => onHover(topic.id)}
      onMouseLeave={() => onHover(null)}
      style={{
        flex: 1, position: "relative", cursor: "pointer", overflow: "hidden", borderRadius: 12,
        padding: "20px 24px", display: "flex", flexDirection: "column", justifyContent: "space-between",
        minHeight: 180, background: T.bgDeep,
        border: `1px solid ${h ? topic.color + "50" : "rgba(255,255,255,0.05)"}`,
        ...borderStyle,
        opacity: dimmed ? 0.7 : 1,
        transition: "all 0.2s ease",
      }}>
      <div>
        {TileIcon && (
          <div style={{ color: topic.color, marginBottom: 8 }}>
            {TileIcon(22)}
          </div>
        )}
        <div style={{ ...TYPE_SCALE.EYEBROW, fontFamily: T.fontDisplay, color: topic.color, marginBottom: 6 }}>{topic.num}</div>
        <h2 style={{ fontFamily: T.fontDisplay, ...TYPE_SCALE.SECTION, color: T.text, margin: "0 0 6px" }}>{topic.title}</h2>
        <p style={{ ...TYPE_SCALE.CAPTION, color: T.textMuted, lineHeight: 1.5, margin: 0 }}>{topic.subtitle}</p>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 8, marginTop: 16, color: topic.color, ...TYPE_SCALE.CAPTION, fontWeight: 700, fontFamily: T.fontDisplay }}>
        <span>Explore</span><span style={{ fontSize: 14 }}>&#8594;</span>
      </div>
    </div>
  );
}
LandingTile.propTypes = {
  topic: topicPropType.isRequired,
  onClick: PropTypes.func.isRequired,
  hovered: PropTypes.string,
  onHover: PropTypes.func.isRequired,
  borderVariant: PropTypes.oneOf(["left", "top"]).isRequired,
};

// ─── STORY ARC DIAGRAM ───
function StoryArcDiagram({ topic, T }) {
  const steps = [
    { num: "01", label: "Mission Need", sub: "One front door for IT demand" },
    { num: "02", label: "Platform Model", sub: "Discovery to procurement" },
    { num: "03", label: "Human Governance", sub: "Speed with oversight" },
    { num: "04", label: "Scale Path", sub: "Repeatable delivery" },
  ];
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 0 }}>
      {steps.map((s, i) => (
        <div key={i} style={{ display: "flex", gap: 12, alignItems: "stretch" }}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", width: 28 }}>
            <div style={{ width: 28, height: 28, borderRadius: "50%", background: topic.color + "20", border: `1px solid ${topic.color}50`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 10, fontWeight: 800, color: topic.colorLight, flexShrink: 0 }}>{s.num}</div>
            {i < steps.length - 1 && <div style={{ width: 1, flex: 1, minHeight: 20, background: topic.color + "30", margin: "4px 0" }}/>}
          </div>
          <div style={{ paddingBottom: i < steps.length - 1 ? 16 : 0, paddingTop: 4 }}>
            <div style={{ fontFamily: T.fontDisplay, fontSize: 14, fontWeight: 700, color: T.text, lineHeight: 1.2 }}>{s.label}</div>
            <div style={{ fontSize: 12, color: T.textMuted, marginTop: 2 }}>{s.sub}</div>
          </div>
        </div>
      ))}
    </div>
  );
}
StoryArcDiagram.propTypes = {
  topic: topicPropType.isRequired,
  T: themePropType.isRequired,
};

// ─── OVERVIEW SCREEN ───
function OverviewScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const [entered, setEntered] = useState(false);
  const [showTalking, setShowTalking] = useState(false);
  const platformTopic = topics.find((item) => item.id === "platform") || topic;

  useEffect(() => { const t = setTimeout(() => setEntered(true), 50); return () => clearTimeout(t); }, []);

  return (
    <div style={{ position: "relative", height: "100vh", background: T.bg, overflow: "hidden", display: "flex", flexDirection: "column" }}>
      <Particles color={topic.color} active={entered} />
      <div style={{ position: "absolute", inset: 0, background: `radial-gradient(circle at 10% 0%, ${topic.color}18, transparent 26%)`, pointerEvents: "none" }} />
      <div style={{ position: "relative", zIndex: 2, flex: 1, maxWidth: 1320, margin: "0 auto", padding: "20px 32px", display: "flex", flexDirection: "column", overflow: "auto" }}>
        <BackBtn onClick={onBack} />
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 32, flex: 1 }}>
          {/* Left: text content */}
          <div style={{ opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(20px)", transition: "all 0.6s ease" }}>
            <div style={{ ...TYPE_SCALE.EYEBROW, fontFamily: T.fontDisplay, color: topic.colorLight, marginBottom: 8 }}>{topic.eyebrow}</div>
            <h1 style={{ fontFamily: T.fontDisplay, ...TYPE_SCALE.HERO, color: T.text, margin: "0 0 10px" }}>{topic.title}</h1>
            <p style={{ ...TYPE_SCALE.CARD, color: topic.colorLight, fontStyle: "italic", lineHeight: 1.4, margin: "0 0 12px" }}>{topic.subtitle}</p>
            <p style={{ ...TYPE_SCALE.BODY, color: T.textMuted, margin: "0 0 16px", maxWidth: 560 }}>{topic.summary}</p>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 16 }}>
              {topic.heroPoints.map((point, i) => (
                <span key={i} style={{ padding: "6px 10px", borderRadius: 6, background: topic.color + "12", border: `1px solid ${topic.color}24`, ...TYPE_SCALE.CAPTION, fontWeight: 700, color: T.text }}>{point}</span>
              ))}
            </div>
            <div style={{ display: "grid", gap: 6 }}>
              {topic.cards.map((card, i) => (
                <div key={i} style={{ padding: "12px 16px", borderRadius: 8, background: T.bgDeep, borderLeft: `2px solid ${topic.color}`, opacity: entered ? 1 : 0, transition: `opacity 0.4s ${0.2 + i * 0.08}s ease` }}>
                  <p style={{ ...TYPE_SCALE.CAPTION, color: T.textMuted, margin: 0 }}>{card.body}</p>
                </div>
              ))}
            </div>
            {/* Expandable talking points */}
            <button onClick={() => setShowTalking(!showTalking)} style={{ marginTop: 12, background: "none", border: `1px solid ${topic.color}30`, borderRadius: 6, padding: "8px 14px", cursor: "pointer", color: topic.colorLight, fontFamily: T.fontDisplay, ...TYPE_SCALE.CAPTION, fontWeight: 700 }}>
              {showTalking ? "Hide" : "Show"} Talking Points {showTalking ? "−" : "+"}
            </button>
            {showTalking && (
              <div style={{ marginTop: 8, display: "grid", gap: 6 }}>
                {topic.talkingPoints.map((pt, i) => (
                  <div key={i} style={{ padding: "8px 12px", borderRadius: 6, background: "rgba(255,255,255,0.03)", border: `1px solid ${topic.color}14`, ...TYPE_SCALE.CAPTION, color: T.textMuted }}>{pt}</div>
                ))}
              </div>
            )}
          </div>
          {/* Right: story arc + platform snapshot */}
          <div style={{ opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(20px)", transition: "all 0.6s 0.1s ease" }}>
            <div style={{ ...TYPE_SCALE.EYEBROW, fontFamily: T.fontDisplay, color: platformTopic.colorLight, marginBottom: 8 }}>Operating Model Snapshot</div>
            <div style={{ fontFamily: T.fontDisplay, ...TYPE_SCALE.SECTION, color: T.text, marginBottom: 16 }}>How the story unfolds</div>
            <StoryArcDiagram topic={topic} T={T} />
            <div style={{ marginTop: 16, padding: "12px 16px", borderRadius: 8, borderLeft: `3px solid ${topic.color}`, background: T.bgCard }}>
              <p style={{ ...TYPE_SCALE.CAPTION, color: T.textMuted, margin: 0 }}><strong style={{ color: topic.colorLight }}>{topic.callout}</strong></p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
OverviewScreen.propTypes = {
  topic: topicPropType.isRequired,
  onBack: PropTypes.func.isRequired,
};

// ─── HUMAN SCREEN ───
function HumanScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const [e, setE] = useState(false);
  const [expandedCard, setExpandedCard] = useState(null);
  useEffect(() => { const t = setTimeout(() => setE(true), 50); return () => clearTimeout(t); }, []);
  const processCards = topic.cards || [];
  const results = topic.results || [];
  const leadershipPoints = topic.leadershipPoints || [];

  return (
    <div style={{ position: "relative", height: "100vh", background: T.bg, overflow: "auto" }}>
      <Particles color={topic.color} active={e} />
      <div style={{ position: "absolute", inset: 0, pointerEvents: "none", background: `radial-gradient(circle at 14% 0%, ${topic.color}24, transparent 28%)` }} />
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1380, margin: "0 auto", padding: "18px 22px 20px", opacity: e ? 1 : 0, transform: e ? "translateY(0)" : "translateY(30px)", transition: "all 0.8s cubic-bezier(0.22,1,0.36,1)" }}>
        <BackBtn onClick={onBack} />
        <div style={{ background: `linear-gradient(180deg, ${T.bgCard}F2, ${T.bgDeep}F0)`, borderRadius: 16, padding: "12px 16px 16px", border: `1px solid ${topic.color}22`, marginBottom: 14 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 14, flexWrap: "wrap", marginBottom: 10, paddingBottom: 10, borderBottom: `1px solid ${topic.color}18` }}>
            <div style={{ width: 44, height: 44, borderRadius: 12, background: topic.color + "14", border: `1px solid ${topic.color}2E`, display: "flex", alignItems: "center", justifyContent: "center", color: topic.colorLight }}>{CARD_ICONS.humanInLoop(26)}</div>
            <div>
              <div style={{ ...TYPE_SCALE.EYEBROW, fontFamily: T.fontDisplay, color: topic.colorLight, marginBottom: 4 }}>{topic.kicker}</div>
              <div style={{ fontFamily: T.fontDisplay, ...TYPE_SCALE.TITLE, fontSize: 28, color: T.text }}>{topic.subkicker}</div>
            </div>
          </div>
          {/* Governance approval chain */}
          <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 12, flexWrap: "wrap" }}>
            {["Risk Mgmt", "Legal", "Compliance"].map((org, i) => (
              <React.Fragment key={org}>
                <div style={{ borderRadius: 6, padding: "4px 10px", background: topic.color + "12", border: `1px solid ${topic.color}30`, fontSize: 11, fontWeight: 700, color: topic.colorLight, fontFamily: T.fontDisplay }}>{org}</div>
                {i < 2 && <div style={{ fontSize: 14, color: topic.color, opacity: 0.5 }}>→</div>}
              </React.Fragment>
            ))}
            <div style={{ fontSize: 14, color: topic.color, opacity: 0.5 }}>→</div>
            <div style={{ borderRadius: 6, padding: "4px 10px", background: topic.color + "20", border: `1px solid ${topic.color}50`, fontSize: 11, fontWeight: 800, color: topic.colorLight, fontFamily: T.fontDisplay }}>AI Clearance ✓</div>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "minmax(0,1.2fr) minmax(320px,0.8fr)", gap: 16, alignItems: "stretch" }}>
            <div>
              <h1 style={{ fontFamily: T.fontDisplay, ...TYPE_SCALE.HERO, color: T.text, margin: "0 0 8px" }}>{topic.heroTitle || topic.title}</h1>
              <p style={{ ...TYPE_SCALE.CARD, color: topic.colorLight, fontStyle: "italic", lineHeight: 1.38, margin: "0 0 10px" }}>{topic.subtitle}</p>
              <p style={{ ...TYPE_SCALE.BODY, color: T.textMuted, margin: 0 }}>AI increased throughput, but approvals, review authority, and release confidence stayed in human hands.</p>
            </div>
            <div style={{ background: `linear-gradient(160deg, ${T.bgDeep}, ${T.bgCard})`, borderRadius: 12, padding: "14px 16px 16px", border: `1px solid ${topic.color}24`, overflow: "hidden" }}>
              <div style={{ ...TYPE_SCALE.EYEBROW, fontFamily: T.fontDisplay, color: topic.colorLight, marginBottom: 8 }}>Leadership Thesis</div>
              <div style={{ fontFamily: T.fontDisplay, ...TYPE_SCALE.SECTION, color: T.text, marginBottom: 10 }}>{topic.thesis}</div>
              <div style={{ display: "grid", gap: 6 }}>
                {leadershipPoints.map((point, i) => (
                  <div key={i} style={{ display: "grid", gridTemplateColumns: "22px minmax(0,1fr)", gap: 8, alignItems: "start", padding: "6px 0", borderTop: i === 0 ? "none" : `1px solid ${topic.color}14` }}>
                    <div style={{ width: 22, height: 22, borderRadius: "50%", background: topic.color + "16", border: `1px solid ${topic.color}28`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 10, fontWeight: 800, color: topic.colorLight }}>{i + 1}</div>
                    <p style={{ ...TYPE_SCALE.CAPTION, color: T.textMuted, margin: 0 }}>{point}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
          <div style={{ marginTop: 12, background: `linear-gradient(135deg, ${T.bgDeep}, ${T.bgCard})`, borderRadius: 12, border: `1px solid ${topic.color}1E`, overflow: "hidden" }}>
            <div style={{ display: "grid", gridTemplateColumns: "320px minmax(0,1fr) 280px", alignItems: "stretch" }}>
              <div style={{ padding: "14px 16px", background: `linear-gradient(180deg, ${topic.color}14, transparent)`, borderRight: `1px solid ${topic.color}18` }}>
                <div style={{ ...TYPE_SCALE.EYEBROW, fontFamily: T.fontDisplay, color: topic.colorLight, marginBottom: 8 }}>{topic.enablementTitle}</div>
                <div style={{ fontFamily: T.fontDisplay, ...TYPE_SCALE.SECTION, color: T.text }}>Team readiness made scale sustainable.</div>
              </div>
              <div style={{ padding: "14px 16px", display: "flex", alignItems: "center", borderRight: `1px solid ${topic.color}18` }}>
                <p style={{ ...TYPE_SCALE.BODY, color: T.textMuted, margin: 0 }}>{topic.enablement}</p>
              </div>
              <div style={{ padding: "14px 16px", display: "flex", alignItems: "center", justifyContent: "center", background: "rgba(255,255,255,0.02)" }}>
                <p style={{ ...TYPE_SCALE.BODY, color: T.textMuted, margin: 0 }}>
                  <strong style={{ color: topic.colorLight }}>{topic.callout}</strong>
                </p>
              </div>
            </div>
          </div>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, minmax(0,1fr))", gap: 12, alignItems: "stretch" }}>
          {processCards.map((card, i) => (
            <div key={i} onClick={() => setExpandedCard(expandedCard === i ? null : i)} style={{
              position: "relative", display: "flex", flexDirection: "column", height: "100%",
              minHeight: expandedCard === i ? 320 : 200,
              background: `linear-gradient(180deg, ${T.bgCard}ED, ${T.bgDeep})`, borderRadius: 12,
              padding: "20px 24px", border: `1px solid ${expandedCard === i ? topic.color + "50" : topic.color + "34"}`,
              opacity: e ? 1 : 0, transform: e ? "translateY(0)" : "translateY(26px)",
              transition: `all 0.55s ${0.18 + i * 0.1}s cubic-bezier(0.22,1,0.36,1)`,
              overflow: "hidden", cursor: "pointer",
            }}>
              <div style={{ position: "relative", zIndex: 1 }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12, marginBottom: 10 }}>
                  <div style={{ ...TYPE_SCALE.EYEBROW, fontFamily: T.fontDisplay, color: topic.colorLight }}>{card.step}</div>
                  <div style={{ minWidth: 40, height: 40, borderRadius: 10, background: topic.color + "12", border: `1px solid ${topic.color}28`, display: "flex", alignItems: "center", justifyContent: "center", color: topic.colorLight }}>
                    {card.marker === "GF" && CARD_ICONS.governanceScale(22)}
                    {card.marker === "QG" && CARD_ICONS.qualityGate(22)}
                    {card.marker === "PC" && CARD_ICONS.contextHub(22)}
                  </div>
                </div>
                <h3 style={{ fontFamily: T.fontDisplay, ...TYPE_SCALE.SECTION, color: T.text, margin: "0 0 6px" }}>{card.title}</h3>
                <div style={{ ...TYPE_SCALE.EYEBROW, fontSize: 10, color: T.textDim, marginBottom: 10 }}>{card.eyebrow}</div>
                <p style={{ ...TYPE_SCALE.BODY, color: T.text, fontWeight: 600, margin: 0 }}>{card.highlight}</p>
                {expandedCard === i && card.details.map((point, idx) => (
                  <div key={idx} style={{ paddingTop: 8, borderTop: `1px solid ${topic.color}14`, marginTop: 8 }}>
                    <p style={{ ...TYPE_SCALE.CAPTION, fontSize: 14, color: T.textMuted, margin: 0 }}>{point}</p>
                  </div>
                ))}
                <div style={{ marginTop: 12 }}>
                  <div style={{ width: 28, height: 28, borderRadius: "50%", background: topic.color + "10", border: `1px solid ${topic.color}20`, display: "flex", alignItems: "center", justifyContent: "center", color: expandedCard === i ? topic.colorLight : T.textDim, fontSize: 16, fontWeight: 700 }}>
                    {expandedCard === i ? "\u2212" : "+"}
                  </div>
                </div>
              </div>
            </div>
          ))}

          {/* Results card */}
          <div onClick={() => setExpandedCard(expandedCard === "results" ? null : "results")} style={{
            position: "relative", display: "flex", flexDirection: "column", height: "100%",
            minHeight: expandedCard === "results" ? 320 : 200,
            background: `linear-gradient(180deg, ${T.bgCard}, ${T.bgDeep})`, borderRadius: 12,
            padding: "20px 24px", border: `1px solid ${expandedCard === "results" ? topic.color + "50" : topic.color + "34"}`,
            opacity: e ? 1 : 0, transform: e ? "translateY(0)" : "translateY(26px)",
            transition: `all 0.6s 0.48s cubic-bezier(0.22,1,0.36,1)`, cursor: "pointer", overflow: "hidden",
          }}>
            <div style={{ position: "relative", zIndex: 1, display: "flex", flexDirection: "column", height: "100%" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12, marginBottom: 10 }}>
                <div style={{ ...TYPE_SCALE.EYEBROW, fontFamily: T.fontDisplay, color: topic.colorLight }}>04</div>
                <div style={{ minWidth: 40, height: 40, borderRadius: 10, background: topic.color + "12", border: `1px solid ${topic.color}28`, display: "flex", alignItems: "center", justifyContent: "center", color: topic.colorLight }}>{CARD_ICONS.resultsChart(22)}</div>
              </div>
              <h3 style={{ fontFamily: T.fontDisplay, ...TYPE_SCALE.SECTION, color: T.text, margin: "0 0 6px" }}>Results</h3>
              <div style={{ ...TYPE_SCALE.EYEBROW, fontSize: 10, color: T.textDim, marginBottom: 10 }}>Measured impact with governance intact</div>
              <div style={{ display: "grid", gap: 8, flex: 1, alignContent: "start" }}>
                {results[0] && (
                  <div>
                    <div style={{ display: "flex", alignItems: "baseline", gap: 10, flexWrap: "wrap", marginBottom: 4 }}>
                      <div style={{ fontFamily: T.fontDisplay, fontSize: 36, fontWeight: 800, color: topic.colorLight, letterSpacing: -1.3, lineHeight: 0.95 }}>{results[0].value}</div>
                      <div style={{ ...TYPE_SCALE.EYEBROW, fontSize: 12, color: T.textDim }}>{results[0].label}</div>
                    </div>
                    {results[0].detail && <p style={{ ...TYPE_SCALE.CAPTION, color: T.textMuted, margin: 0 }}>{results[0].detail}</p>}
                  </div>
                )}
                {expandedCard === "results" && results.slice(1, 3).map((item, idx) => (
                  <div key={idx} style={{ paddingTop: 8, borderTop: `1px solid ${topic.color}14` }}>
                    <div style={{ display: "flex", alignItems: "baseline", gap: 10, flexWrap: "wrap" }}>
                      <div style={{ fontFamily: T.fontDisplay, fontSize: 30, fontWeight: 800, color: topic.colorLight, letterSpacing: -1, lineHeight: 0.95 }}>{item.value}</div>
                      <div style={{ ...TYPE_SCALE.EYEBROW, fontSize: 12, color: T.textDim }}>{item.label}</div>
                    </div>
                  </div>
                ))}
                <div style={{ marginTop: "auto", paddingTop: 8 }}>
                  <div style={{ width: 28, height: 28, borderRadius: "50%", background: topic.color + "10", border: `1px solid ${topic.color}20`, display: "flex", alignItems: "center", justifyContent: "center", color: expandedCard === "results" ? topic.colorLight : T.textDim, fontSize: 16, fontWeight: 700 }}>
                    {expandedCard === "results" ? "\u2212" : "+"}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
HumanScreen.propTypes = {
  topic: topicPropType.isRequired,
  onBack: PropTypes.func.isRequired,
};

// ─── HURDLES SCREEN (horizontal timeline rows) ───
function HurdlesScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const [e, setE] = useState(false);
  useEffect(() => { const t = setTimeout(() => setE(true), 50); return () => clearTimeout(t); }, []);

  return (
    <div style={{ position: "relative", height: "100vh", background: T.bg, overflow: "hidden", display: "flex", flexDirection: "column" }}>
      <Particles color={topic.color} active={e} />
      {/* Diagonal line decoration */}
      <div style={{ position: "absolute", inset: 0, pointerEvents: "none", overflow: "hidden" }}>
        <div style={{ position: "absolute", top: 0, left: 0, width: "141%", height: 1, background: `${topic.color}1A`, transform: "rotate(35deg)", transformOrigin: "top left" }} />
      </div>
      <div style={{ position: "relative", zIndex: 2, flex: 1, padding: "20px 32px 20px 40px", display: "flex", flexDirection: "column", maxWidth: 1200, margin: "0 auto", width: "100%" }}>
        <BackBtn onClick={onBack} />
        <div style={{ marginBottom: 32, opacity: e ? 1 : 0, transform: e ? "translateX(0)" : "translateX(-60px)", transition: "all 0.5s cubic-bezier(0.16,1,0.3,1)" }}>
          <h1 style={{ fontFamily: T.fontDisplay, ...TYPE_SCALE.TITLE, color: T.text, margin: "0 0 6px" }}>{topic.title}</h1>
          <p style={{ ...TYPE_SCALE.CARD, color: topic.colorLight, fontStyle: "italic", margin: 0, lineHeight: 1.45 }}>{topic.subtitle}</p>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "60% 40%", gap: 32, flex: 1, alignItems: "start" }}>
          {/* Left: timeline rows */}
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            {topic.cards.map((c, i) => (
              <div key={i} style={{
                display: "grid", gridTemplateColumns: "180px 1fr 1fr", gap: 16, alignItems: "start",
                borderLeft: `3px solid ${topic.color}`, padding: "12px 16px", borderRadius: 6,
                background: "transparent",
                opacity: e ? 1 : 0, transform: e ? "translateX(0)" : "translateX(-40px)",
                transition: `all 0.45s ${0.2 + i * 0.12}s cubic-bezier(0.16,1,0.3,1)`,
              }}>
                <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  <div style={{ width: 30, height: 30, borderRadius: 6, background: topic.color + "20", display: "flex", alignItems: "center", justifyContent: "center", fontFamily: T.fontDisplay, fontWeight: 700, ...TYPE_SCALE.CAPTION, color: topic.color }}>{i + 1}</div>
                  <h3 style={{ fontFamily: T.fontDisplay, ...TYPE_SCALE.CARD, color: T.text, margin: 0 }}>{c.title}</h3>
                </div>
                <div>
                  <div style={{ ...TYPE_SCALE.EYEBROW, fontSize: 10, color: T.danger, marginBottom: 4 }}>Challenge</div>
                  <p style={{ ...TYPE_SCALE.BODY, color: T.textDim, margin: 0 }}>{c.challenge}</p>
                </div>
                <div>
                  <div style={{ ...TYPE_SCALE.EYEBROW, fontSize: 10, color: T.success, marginBottom: 4 }}>Solution</div>
                  <p style={{ ...TYPE_SCALE.BODY, color: T.text, margin: 0 }}>{c.fix}</p>
                </div>
              </div>
            ))}
          </div>

          {/* Right: photo placeholder + callout */}
          <div style={{ display: "flex", flexDirection: "column", gap: 16, opacity: e ? 1 : 0, transition: "opacity 0.6s 0.5s" }}>
            <div style={{ borderRadius: 10, overflow: "hidden", minHeight: 200, position: "relative" }}>
              <img src={HERO_IMGS.helicopterRappel} alt="Field operations" style={{ width: "100%", height: "100%", objectFit: "cover", display: "block", minHeight: 200, filter: "brightness(0.72) saturate(0.85)" }} />
              <div style={{ position: "absolute", inset: 0, background: `linear-gradient(to top, ${T.bg}CC 0%, transparent 55%)` }} />
              <div style={{ position: "absolute", bottom: 10, left: 12, ...TYPE_SCALE.EYEBROW, fontSize: 10, color: topic.colorLight }}>Operations</div>
            </div>
            <div style={{ borderLeft: `3px solid ${topic.color}`, paddingLeft: 16 }}>
              <p style={{ ...TYPE_SCALE.BODY, color: T.text, fontStyle: "italic", lineHeight: 1.6, margin: 0 }}>
                <strong style={{ color: topic.colorLight }}>{topic.callout}</strong>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
HurdlesScreen.propTypes = {
  topic: topicPropType.isRequired,
  onBack: PropTypes.func.isRequired,
};

// ─── FIGURE-8 SPRINT CYCLE ───
function Figure8Cycle({ entered }) {
  const T = useContext(ThemeCtx);
  const canvasRef = useRef(null);
  const progressRef = useRef(0);

  const W = 860, H = 420;
  const lcx = 280, rcx = 580, cy = 210, lrx = 210, rrx = 210, ry = 155;

  function fig8Pos(t) {
    if (t < 0.5) {
      const a = -Math.PI + t * 2 * Math.PI * 2;
      return { x: lcx + lrx * Math.cos(a), y: cy + ry * Math.sin(a) };
    } else {
      const a = Math.PI - (t - 0.5) * 2 * Math.PI * 2;
      return { x: rcx + rrx * Math.cos(a), y: cy + ry * Math.sin(a) };
    }
  }

  const nodePositions = sprintNodes.map((n, i) => {
    const t = i / 12;
    return { ...n, ...fig8Pos(t), t, i };
  });

  useEffect(() => {
    const c = canvasRef.current;
    if (!c) return;
    const ctx = c.getContext("2d");
    c.width = W * 2; c.height = H * 2; ctx.scale(2, 2);
    const accentColor = T.accent;
    let raf;
    function draw() {
      progressRef.current = (progressRef.current + 0.0008) % 1;
      const prog = progressRef.current;
      ctx.clearRect(0, 0, W, H);

      ctx.beginPath();
      for (let i = 0; i <= 300; i++) { const p = fig8Pos(i / 300); i === 0 ? ctx.moveTo(p.x, p.y) : ctx.lineTo(p.x, p.y); }
      ctx.closePath(); ctx.strokeStyle = accentColor + "1A"; ctx.lineWidth = 2.5; ctx.stroke();

      // Comet trail (20 particles)
      for (let i = 0; i < 20; i++) {
        const tt = ((prog - (i / 20) * 0.06) + 1) % 1;
        const p = fig8Pos(tt);
        const alpha = (1 - i / 20) * 0.55;
        const r = parseInt(accentColor.slice(1, 3), 16);
        const g = parseInt(accentColor.slice(3, 5), 16);
        const b = parseInt(accentColor.slice(5, 7), 16);
        ctx.beginPath(); ctx.arc(p.x, p.y, 4 - i * 0.15, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${r},${g},${b},${alpha})`; ctx.fill();
      }
      const lead = fig8Pos(prog);
      ctx.beginPath(); ctx.arc(lead.x, lead.y, 6, 0, Math.PI * 2);
      ctx.fillStyle = accentColor; ctx.shadowColor = accentColor; ctx.shadowBlur = 18; ctx.fill(); ctx.shadowBlur = 0;

      raf = requestAnimationFrame(draw);
    }
    if (entered) draw();
    return () => cancelAnimationFrame(raf);
  }, [entered, T.accent]);

  return (
    <div style={{ position: "relative", width: W, height: H, margin: "0 auto" }}>
      <canvas ref={canvasRef} style={{ position: "absolute", inset: 0, width: W, height: H }} />

      <div style={{ position: "absolute", left: lcx - 62, top: 12, ...TYPE_SCALE.EYEBROW, fontSize: 12, color: T.accent, fontFamily: T.fontDisplay }}>Phase 1 -- Build</div>
      <div style={{ position: "absolute", left: rcx - 68, top: 12, ...TYPE_SCALE.EYEBROW, fontSize: 12, color: T.gradient ? T.gradient[1] : T.textMuted, fontFamily: T.fontDisplay }}>Phase 2 -- Validate</div>
      <div style={{ position: "absolute", left: (lcx + rcx) / 2 - 38, top: cy - 14, background: T.surfaceElevated, border: `1px solid ${T.accent}4D`, borderRadius: 6, padding: "5px 12px", ...TYPE_SCALE.EYEBROW, fontSize: 10, color: T.accent, fontFamily: T.fontDisplay, zIndex: 6 }}>Handoff</div>

      {nodePositions.map((n, i) => {
        const isAI = n.type === "ai";
        const size = 34;
        const humanBorderColor = T.gradient ? T.gradient[1] : "#0891B2";
        const humanIconColor = T.gradient ? T.gradient[1] : "#22D3EE";
        const borderColor = isAI ? `${T.accent}99` : `${humanBorderColor}60`;
        const iconColor = isAI ? T.accent : humanIconColor;
        const nodeIcon = SPRINT_ICONS[n.abbr] ? React.createElement(SPRINT_ICONS[n.abbr]) : n.abbr;
        return (
          <div key={i} style={{
            position: "absolute", left: n.x - size, top: n.y - size, width: size * 2, height: size * 2,
            borderRadius: "50%", background: isAI ? T.accent + "18" : T.bgCard,
            border: `2px solid ${borderColor}`,
            boxShadow: isAI ? `0 0 12px ${T.accent}2E` : "none",
            display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
            zIndex: 5,
            opacity: entered ? 1 : 0, transform: entered ? "scale(1)" : "scale(0.7)",
            transition: `all 0.4s ${0.15 + i * 0.06}s cubic-bezier(0.34,1.56,0.64,1)`,
          }}>
            <span style={{ color: iconColor }}>{nodeIcon}</span>
            <div style={{ position: "absolute", top: -6, right: -6, width: 16, height: 16, borderRadius: "50%", background: isAI ? "#7C3AED" : "#0891B2", display: "flex", alignItems: "center", justifyContent: "center" }}>
              {isAI ? (
                <svg width="9" height="9" viewBox="0 0 24 24" fill="currentColor" stroke="none" style={{ color: "#fff" }}>
                  <path d="M13 2L4 14h7l-1 8 10-12h-7z"/>
                </svg>
              ) : (
                <svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.5" strokeLinecap="round">
                  <circle cx="12" cy="7" r="3"/>
                  <path d="M5 20a7 7 0 0 1 14 0"/>
                </svg>
              )}
            </div>
            <div style={{ position: "absolute", top: size * 2 + 8, left: -18, width: 104, ...TYPE_SCALE.CAPTION, color: T.text, textAlign: "center", fontWeight: 600, fontFamily: T.fontDisplay, lineHeight: 1.2 }}>{n.label}</div>
          </div>
        );
      })}
    </div>
  );
}
Figure8Cycle.propTypes = { entered: PropTypes.bool.isRequired };

// ─── SPRINT SCREEN (Figure-8 only) ───
function SprintScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 50); return () => clearTimeout(t); }, []);

  return (
    <div style={{ position: "relative", height: "100vh", background: T.bg, overflow: "hidden", display: "flex", flexDirection: "column" }}>
      <Particles color={topic.color} active={entered} />
      <div style={{ position: "relative", zIndex: 2, flex: 1, padding: "20px 32px", display: "flex", flexDirection: "column" }}>
        <BackBtn onClick={onBack} />
        <div style={{ textAlign: "center", marginBottom: 16, opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(-20px)", transition: "all 0.6s cubic-bezier(0.22,1,0.36,1)" }}>
          <h1 style={{ fontFamily: T.fontDisplay, ...TYPE_SCALE.TITLE, fontSize: 28, color: T.text, margin: "0 0 6px" }}>AI Sprint Cycle</h1>
          <p style={{ ...TYPE_SCALE.BODY, color: topic.colorLight, fontStyle: "italic", margin: 0, lineHeight: 1.45 }}>{topic.subtitle}</p>
        </div>

        <div style={{ background: T.surfaceElevated, borderRadius: 12, padding: "20px 24px", border: `1px solid ${topic.color}18`, maxWidth: 920, margin: "0 auto", flex: 1, display: "flex", alignItems: "center", justifyContent: "center", width: "100%" }}>
          <Figure8Cycle entered={entered} />
        </div>

        <div style={{ marginTop: 12, padding: "12px 16px", borderRadius: 6, borderLeft: `4px solid ${topic.color}`, maxWidth: 920, marginLeft: "auto", marginRight: "auto", opacity: entered ? 1 : 0, transition: "opacity 0.6s 1s" }}>
          <p style={{ ...TYPE_SCALE.BODY, color: T.text, margin: 0 }}>
            <strong style={{ color: topic.colorLight }}>{topic.callout}</strong>
          </p>
        </div>
        {/* Sprint legend */}
        <div style={{ display: "flex", justifyContent: "center", gap: 24, marginTop: 12, opacity: entered ? 1 : 0, transition: "opacity 0.6s 2s" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 7 }}>
            <div style={{ width: 14, height: 14, borderRadius: "50%", background: "#0891B2", display: "flex", alignItems: "center", justifyContent: "center" }}>
              <svg width="8" height="8" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.5" strokeLinecap="round"><circle cx="12" cy="7" r="3"/><path d="M5 20a7 7 0 0 1 14 0"/></svg>
            </div>
            <span style={{ ...TYPE_SCALE.EYEBROW, fontSize: 10, color: T.textMuted }}>Human-governed</span>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: 7 }}>
            <div style={{ width: 14, height: 14, borderRadius: "50%", background: "#7C3AED", display: "flex", alignItems: "center", justifyContent: "center" }}>
              <svg width="8" height="8" viewBox="0 0 24 24" fill="#fff" stroke="none"><path d="M13 2L4 14h7l-1 8 10-12h-7z"/></svg>
            </div>
            <span style={{ ...TYPE_SCALE.EYEBROW, fontSize: 10, color: T.textMuted }}>AI-assisted</span>
          </div>
        </div>
      </div>
    </div>
  );
}
SprintScreen.propTypes = {
  topic: topicPropType.isRequired,
  onBack: PropTypes.func.isRequired,
};

// ─── FUTURE SCREEN (1x4 horizontal strip) ───
function FutureScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const [e, setE] = useState(false);
  useEffect(() => { const t = setTimeout(() => setE(true), 50); return () => clearTimeout(t); }, []);

  return (
    <div style={{ position: "relative", height: "100vh", background: T.bg, overflow: "hidden", display: "flex", flexDirection: "column" }}>
      <Particles color={topic.color} active={e} />
      {/* UAV photo — right-edge accent */}
      <div style={{ position: "absolute", right: 0, bottom: 0, width: 340, height: 260, overflow: "hidden", pointerEvents: "none", zIndex: 0 }}>
        <img src={HERO_IMGS.uavSunset} alt="" style={{ width: "100%", height: "100%", objectFit: "cover", opacity: 0.18, filter: "saturate(0.7)" }} />
        <div style={{ position: "absolute", inset: 0, background: `linear-gradient(to bottom-right, ${T.bg} 0%, transparent 60%)` }} />
      </div>
      {/* Concentric arc decoration */}
      <div style={{ position: "absolute", top: "50%", left: "50%", width: 600, height: 600, borderRadius: "50%", border: `1px solid ${topic.color}08`, transform: "translate(-50%, -50%)", pointerEvents: "none" }} />
      <div style={{ position: "absolute", top: "50%", left: "50%", width: 400, height: 400, borderRadius: "50%", border: `1px solid ${topic.color}06`, transform: "translate(-50%, -50%)", pointerEvents: "none" }} />

      {/* Horizon accent — bottom left */}
      <div style={{ position: "absolute", bottom: 24, left: 24, opacity: 0.08, pointerEvents: "none" }}>
        <svg width="120" height="60" viewBox="0 0 120 60" fill="none" stroke={topic.color} strokeWidth="1.5" strokeLinecap="round">
          <line x1="0" y1="50" x2="120" y2="50"/>
          <line x1="60" y1="48" x2="60" y2="20"/>
          <line x1="35" y1="46" x2="25" y2="18"/>
          <line x1="85" y1="46" x2="95" y2="18"/>
        </svg>
      </div>

      <div style={{ position: "relative", zIndex: 2, flex: 1, padding: "20px 32px", display: "flex", flexDirection: "column", maxWidth: 1200, margin: "0 auto", width: "100%" }}>
        <BackBtn onClick={onBack} />
        <div style={{ marginBottom: 24, opacity: e ? 1 : 0, transform: e ? "translateY(0)" : "translateY(20px)", transition: "all 0.6s ease" }}>
          <h1 style={{ fontFamily: T.fontDisplay, ...TYPE_SCALE.TITLE, color: T.text, margin: "0 0 6px" }}>{topic.title}</h1>
          <p style={{ ...TYPE_SCALE.CARD, color: topic.colorLight, fontStyle: "italic", margin: 0 }}>{topic.subtitle}</p>
        </div>

        {/* Pull-quote */}
        <div style={{ marginBottom: 24, padding: "16px 20px", borderLeft: `3px solid ${topic.color}`, opacity: e ? 1 : 0, transition: "opacity 0.6s 0.3s ease" }}>
          <div style={{ fontFamily: "Georgia, serif", fontSize: 80, lineHeight: 0.7, color: topic.color, opacity: 0.12, marginBottom: -8, userSelect: "none" }}>&ldquo;</div>
          <p style={{ fontFamily: T.fontDisplay, fontSize: 22, fontStyle: "italic", fontWeight: 500, color: T.text, margin: 0, lineHeight: 1.45 }}>{topic.callout}</p>
        </div>

        {/* 1x4 horizontal strip */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12, flex: 1 }}>
          {topic.cards.map((c, i) => {
            const borders = [
              { borderLeft: `3px solid ${topic.color}` },
              { borderTop: `3px solid ${topic.color}` },
              { borderBottom: `3px solid ${topic.color}` },
              { borderLeft: `3px solid ${topic.color}` },
            ];
            return (
              <div key={i} style={{
                background: T.bgCard, borderRadius: 8, padding: "20px 24px",
                ...borders[i],
                opacity: e ? 1 : 0, transform: e ? "translateY(0)" : "translateY(16px)",
                transition: `all 0.5s ${0.3 + i * 0.12}s ease`,
                display: "flex", flexDirection: "column",
              }}>
                <div style={{ ...TYPE_SCALE.EYEBROW, fontFamily: T.fontDisplay, color: topic.colorLight, marginBottom: 8 }}>
                  {String(i + 1).padStart(2, "0")}
                </div>
                <h3 style={{ fontFamily: T.fontDisplay, ...TYPE_SCALE.CARD, color: T.text, margin: "0 0 8px" }}>{c.title}</h3>
                <p style={{ ...TYPE_SCALE.BODY, color: T.textMuted, margin: 0 }}>{c.body}</p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
FutureScreen.propTypes = {
  topic: topicPropType.isRequired,
  onBack: PropTypes.func.isRequired,
};

// ─── PLATFORM MOCK FRAME ───
function PlatformMockFrame({ topic, entered, theme }) {
  return (
    <div style={{ position: "relative", minHeight: 280, borderRadius: 12, overflow: "hidden", background: `linear-gradient(145deg, ${theme.bgDeep}, ${theme.bgCard})`, border: `1px solid ${topic.color}26` }}>
      <div style={{ position: "relative", zIndex: 1, padding: "16px 18px 0", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div style={{ display: "flex", gap: 5 }}>{["#F97316", "#FBBF24", "#22C55E"].map((c, i) => <div key={i} style={{ width: 8, height: 8, borderRadius: "50%", background: c, opacity: 0.9 }} />)}</div>
      </div>
      <div style={{ position: "relative", zIndex: 1, padding: "16px 18px", display: "flex", flexWrap: "wrap", gap: 16, alignItems: "stretch" }}>
        <div style={{ flex: "1 1 240px", display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
          <div>
            <div style={{ ...TYPE_SCALE.EYEBROW, fontFamily: theme.fontDisplay, color: topic.colorLight, marginBottom: 8 }}>Unified Service Catalog</div>
            <div style={{ fontFamily: theme.fontDisplay, ...TYPE_SCALE.SECTION, color: theme.text, marginBottom: 8 }}>Request. Review. Route.</div>
            <p style={{ ...TYPE_SCALE.CAPTION, color: theme.textMuted, lineHeight: 1.5, margin: 0 }}>A single front door for discovery, intake, approvals, and downstream procurement handoff.</p>
          </div>
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginTop: 12 }}>
            <button style={{ border: "none", borderRadius: 6, padding: "8px 12px", background: `linear-gradient(90deg, ${topic.color}, ${topic.colorLight})`, color: theme.surfaceElevated, fontWeight: 800, ...TYPE_SCALE.CAPTION, cursor: "default", fontFamily: theme.fontDisplay }}>Browse Catalog</button>
            <div style={{ display: "flex", alignItems: "center", gap: 6, padding: "7px 10px", borderRadius: 6, background: "rgba(255,255,255,0.04)", border: `1px solid ${topic.color}18`, color: theme.textMuted, ...TYPE_SCALE.CAPTION }}>
              <span style={{ width: 7, height: 7, borderRadius: "50%", background: theme.success }} />
              CAC-enabled
            </div>
          </div>
        </div>
        <div style={{ flex: "1 1 200px", display: "grid", gap: 8 }}>
          {[
            { label: "Discovery", value: "Catalogs + services" },
            { label: "Governance", value: "Approval queue" },
            { label: "Tracking", value: "User visibility" },
            { label: "Handoff", value: "Procurement flow" },
          ].map((item, i) => (
            <div key={i} style={{ background: "rgba(255,255,255,0.04)", border: `1px solid ${topic.color}18`, borderRadius: 8, padding: "10px 12px", opacity: entered ? 1 : 0, transform: entered ? "translateX(0)" : "translateX(16px)", transition: `all 0.4s ${0.2 + i * 0.08}s ease` }}>
              <div style={{ ...TYPE_SCALE.EYEBROW, fontSize: 10, color: theme.textDim, marginBottom: 3 }}>{item.label}</div>
              <div style={{ fontFamily: theme.fontDisplay, ...TYPE_SCALE.CAPTION, fontWeight: 700, color: theme.text }}>{item.value}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
PlatformMockFrame.propTypes = {
  topic: topicPropType.isRequired,
  entered: PropTypes.bool.isRequired,
  theme: themePropType.isRequired,
};

// ─── PLATFORM SCREEN ───
function PlatformScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const [entered, setEntered] = useState(false);
  const [showCaps, setShowCaps] = useState(false);
  const [showProcess, setShowProcess] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 50); return () => clearTimeout(t); }, []);

  return (
    <div style={{ position: "relative", height: "100vh", background: T.bg, overflow: "auto" }}>
      <Particles color={topic.color} active={entered} />
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1320, margin: "0 auto", padding: "20px 32px" }}>
        <BackBtn onClick={onBack} />

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 32, marginBottom: 16 }}>
          {/* Left: text content */}
          <div style={{ opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(20px)", transition: "all 0.6s ease" }}>
            <div style={{ ...TYPE_SCALE.EYEBROW, fontFamily: T.fontDisplay, color: topic.colorLight, marginBottom: 8 }}>{topic.eyebrow}</div>
            <h1 style={{ fontFamily: T.fontDisplay, ...TYPE_SCALE.HERO, color: T.text, margin: "0 0 10px" }}>{topic.title}</h1>
            <p style={{ ...TYPE_SCALE.CARD, color: topic.colorLight, fontStyle: "italic", lineHeight: 1.4, margin: "0 0 12px" }}>{topic.subtitle}</p>
            <p style={{ ...TYPE_SCALE.BODY, color: T.textMuted, margin: "0 0 16px" }}>{topic.summary}</p>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 16 }}>
              {topic.heroPoints.map((point, i) => (
                <span key={i} style={{ padding: "6px 10px", borderRadius: 6, background: topic.color + "12", border: `1px solid ${topic.color}24`, ...TYPE_SCALE.CAPTION, fontWeight: 700, color: T.text }}>{point}</span>
              ))}
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 8 }}>
              {topic.focusPanels.map((panel, i) => (
                <div key={i} style={{ background: T.bgDeep, borderRadius: 8, padding: "12px 14px", borderTop: `2px solid ${topic.color}`, opacity: entered ? 1 : 0, transition: `opacity 0.4s ${0.18 + i * 0.08}s ease` }}>
                  <div style={{ ...TYPE_SCALE.EYEBROW, fontSize: 10, fontFamily: T.fontDisplay, color: topic.colorLight, marginBottom: 6 }}>{panel.label}</div>
                  <div style={{ fontFamily: T.fontDisplay, ...TYPE_SCALE.CAPTION, fontWeight: 700, color: T.text, marginBottom: 4 }}>{panel.title}</div>
                  <p style={{ ...TYPE_SCALE.CAPTION, color: T.textMuted, margin: 0 }}>{panel.body}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Right: mock frame */}
          <div style={{ opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(20px)", transition: "all 0.6s 0.1s ease" }}>
            {/* Photo strip */}
            <div style={{ borderRadius: 10, overflow: "hidden", height: 100, marginBottom: 12, position: "relative" }}>
              <img src={HERO_IMGS.droneDeck} alt="Operations deck" style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: "center 40%", filter: "brightness(0.65) saturate(0.8)" }} />
              <div style={{ position: "absolute", inset: 0, background: `linear-gradient(to right, ${T.bg}AA, transparent 40%, ${T.bg}AA)` }} />
              <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center" }}>
                <span style={{ ...TYPE_SCALE.EYEBROW, fontSize: 10, color: topic.colorLight, letterSpacing: 3 }}>SERVICE PLATFORM — MISSION READY</span>
              </div>
            </div>
            {/* Issue-to-Impact flow */}
            <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 16, flexWrap: "wrap" }}>
              {[
                { label: "IT Need", sub: "User Request" },
                { label: "Platform", sub: "Review & Route" },
                { label: "Procurement", sub: "Handoff to downstream tool" },
              ].map((node, i) => (
                <React.Fragment key={i}>
                  <div style={{ borderRadius: 8, padding: "8px 14px", background: topic.color + (i === 1 ? "22" : "10"), border: `1px solid ${topic.color}${i === 1 ? "50" : "28"}`, textAlign: "center" }}>
                    <div style={{ fontFamily: T.fontDisplay, fontSize: 13, fontWeight: 700, color: topic.colorLight }}>{node.label}</div>
                    <div style={{ fontSize: 10, color: T.textMuted, marginTop: 2 }}>{node.sub}</div>
                  </div>
                  {i < 2 && <div style={{ fontSize: 18, color: topic.color, opacity: 0.5, flexShrink: 0 }}>→</div>}
                </React.Fragment>
              ))}
            </div>
            <div style={{ ...TYPE_SCALE.EYEBROW, fontFamily: T.fontDisplay, color: topic.colorLight, marginBottom: 8 }}>One-Pager Snapshot</div>
            <PlatformMockFrame topic={topic} entered={entered} theme={T} />
          </div>
        </div>

        {/* Expandable: Capabilities */}
        <button onClick={() => setShowCaps(!showCaps)} style={{ width: "100%", background: T.bgCard, border: `1px solid ${topic.color}20`, borderRadius: 8, padding: "12px 16px", cursor: "pointer", display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: showCaps ? 0 : 8 }}>
          <span style={{ fontFamily: T.fontDisplay, ...TYPE_SCALE.CARD, color: T.text }}>Capability View</span>
          <span style={{ color: topic.colorLight, fontWeight: 700 }}>{showCaps ? "\u2212" : "+"}</span>
        </button>
        {showCaps && (
          <div style={{ background: T.bgCard, borderRadius: "0 0 8px 8px", padding: "12px 16px", border: `1px solid ${topic.color}20`, borderTop: "none", marginBottom: 8 }}>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(2,1fr)", gap: 8 }}>
              {topic.capabilities.map((cap, i) => (
                <div key={i} style={{ background: T.bgDeep, borderRadius: 8, padding: "12px 16px", borderLeft: `2px solid ${topic.color}` }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6 }}>
                    <div style={{ width: 28, height: 28, borderRadius: 6, background: topic.color + "14", border: `1px solid ${topic.color}28`, display: "flex", alignItems: "center", justifyContent: "center", color: topic.colorLight }}>
                      {cap.marker === "BG" && CARD_ICONS.browseCatalog(16)}
                      {cap.marker === "RS" && CARD_ICONS.researchMagnify(16)}
                      {cap.marker === "TR" && CARD_ICONS.trackFlow(16)}
                      {cap.marker === "CP" && CARD_ICONS.procureHandoff(16)}
                    </div>
                    <h3 style={{ fontFamily: T.fontDisplay, ...TYPE_SCALE.CARD, color: T.text, margin: 0 }}>{cap.title}</h3>
                  </div>
                  <p style={{ ...TYPE_SCALE.BODY, color: T.textMuted, margin: 0 }}>{cap.body}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Expandable: Process Flow */}
        <button onClick={() => setShowProcess(!showProcess)} style={{ width: "100%", background: T.bgCard, border: `1px solid ${topic.color}20`, borderRadius: 8, padding: "12px 16px", cursor: "pointer", display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: showProcess ? 0 : 8 }}>
          <span style={{ fontFamily: T.fontDisplay, ...TYPE_SCALE.CARD, color: T.text }}>Process Flow & Personas</span>
          <span style={{ color: topic.colorLight, fontWeight: 700 }}>{showProcess ? "\u2212" : "+"}</span>
        </button>
        {showProcess && (
          <div style={{ background: T.bgCard, borderRadius: "0 0 8px 8px", padding: "12px 16px", border: `1px solid ${topic.color}20`, borderTop: "none", marginBottom: 8 }}>
            <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
              {topic.lanes.map((lane, index) => (
                <div key={index} style={{ flex: index === 0 ? "1.3 1 480px" : "0.9 1 300px", background: T.bgDeep, borderRadius: 12, border: `1px solid ${lane.accent}2a`, overflow: "hidden" }}>
                  <div style={{ padding: "14px 16px 10px", borderBottom: `1px solid ${lane.accent}1c`, background: `linear-gradient(180deg, ${lane.accent}12, transparent)` }}>
                    <div style={{ ...TYPE_SCALE.EYEBROW, fontFamily: T.fontDisplay, color: lane.accent, marginBottom: 4 }}>{lane.title}</div>
                    <div style={{ fontFamily: T.fontDisplay, ...TYPE_SCALE.SECTION, color: T.text, marginBottom: 6 }}>{lane.subtitle}</div>
                    <div style={{ display: "inline-flex", alignItems: "center", gap: 6, padding: "6px 10px", borderRadius: 6, background: lane.accent + "12", border: `1px solid ${lane.accent}24`, ...TYPE_SCALE.CAPTION, color: T.textMuted }}>
                      <span style={{ width: 7, height: 7, borderRadius: "50%", background: lane.accent }} />
                      {lane.persona}
                    </div>
                  </div>
                  <div style={{ padding: "12px 14px", display: "grid", gap: 8 }}>
                    {lane.steps.map((step, i) => (
                      <div key={i} style={{ padding: "12px 14px", borderRadius: 8, background: T.bgCard, borderTop: `2px solid ${lane.accent}` }}>
                        <div style={{ width: 24, height: 24, borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", background: lane.accent + "18", color: lane.accent, fontWeight: 800, fontFamily: T.fontDisplay, fontSize: 12, marginBottom: 8 }}>{i + 1}</div>
                        <p style={{ ...TYPE_SCALE.BODY, color: T.textMuted, margin: 0 }}>{step}</p>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Callout line */}
        <div style={{ padding: "12px 16px", borderLeft: `3px solid ${topic.color}`, marginTop: 4 }}>
          <p style={{ ...TYPE_SCALE.BODY, color: T.text, margin: 0 }}><strong style={{ color: topic.colorLight }}>{topic.callout}</strong></p>
        </div>
      </div>
    </div>
  );
}
PlatformScreen.propTypes = {
  topic: topicPropType.isRequired,
  onBack: PropTypes.func.isRequired,
};

// ─── MAIN APP ───
export default function App() {
  const [theme, setTheme] = useState(null);
  const [introDone, setIntroDone] = useState(false);
  const [active, setActive] = useState(null);
  const [transitioning, setTransitioning] = useState(false);
  const [hovered, setHovered] = useState(null);
  const [comet, setComet] = useState({ active: false, from: null, color: null, targetId: null });

  const handleSelect = (id, pos) => {
    const topic = topics.find(t => t.id === id);
    setTransitioning(true);
    setComet({ active: true, from: pos, color: topic.color, targetId: id });
  };
  const cometRef = useRef(comet);
  cometRef.current = comet;
  const handleCometDone = useCallback(() => {
    setActive(cometRef.current.targetId);
    setComet({ active: false, from: null, color: null, targetId: null });
    setTransitioning(false);
  }, []);
  const handleBack = () => { setTransitioning(true); setTimeout(() => { setActive(null); setTransitioning(false); }, 350); };
  const activeTopic = topics.find(t => t.id === active);
  const primaryTopics = topics.filter((t) => !t.optional);
  const optionalPlatform = topics.find((t) => t.id === "platform");

  const landingStats = [
    { val: "~40%", lbl: "Productivity Uplift" },
    { val: "2 mo", lbl: "Prototype to Production" },
    { val: "~90%", lbl: "AI-Assisted Code" },
    { val: "~95%", lbl: "Sprint Predictability" },
  ];

  if (!theme) return <ThemeSelector onSelect={(t) => setTheme(t)} />;

  const T = theme;

  return (
    <ThemeCtx.Provider value={T}>
    <div style={{ fontFamily: T.fontBody, minHeight: "100vh", background: T.bg, opacity: (transitioning && !comet.active) ? 0 : 1, transition: "opacity 0.35s ease" }}>
      {!IS_SINGLE_FILE_BUILD && <link href={THEME_FONT_URLS[T.id]} rel="stylesheet" />}
      <CometTransition from={comet.from} color={comet.color} active={comet.active} onDone={handleCometDone} />
      {!introDone && <TitleReveal onComplete={() => setIntroDone(true)} />}
      {!active && introDone && (
        <div style={{ height: "100vh", display: "flex", padding: "32px 40px", gap: 32, opacity: comet.active ? 0 : 1, transition: "opacity 0.4s ease", overflow: "hidden" }}>
          {/* Large quarter-circle decoration */}
          <div style={{ position: "fixed", bottom: -200, right: -200, width: 500, height: 500, borderRadius: "50%", background: T.accent + "08", pointerEvents: "none" }} />
          {/* Background silhouette — very subtle, 4% opacity */}
          <div style={{ position: "fixed", bottom: 0, right: 0, width: 480, height: 160, pointerEvents: "none", opacity: 0.04 }}>
            <svg viewBox="0 0 480 160" fill={T.text} xmlns="http://www.w3.org/2000/svg" style={{ width: "100%", height: "100%" }}>
              <path d="M20 90 L440 90 L460 80 L460 95 L20 110 Z"/>
              <rect x="340" y="55" width="60" height="35" rx="2"/>
              <rect x="355" y="35" width="8" height="20"/>
              <rect x="370" y="40" width="5" height="15"/>
              <rect x="380" y="45" width="4" height="10"/>
              <line x1="359" y1="35" x2="359" y2="20" strokeWidth="2" stroke={T.text}/>
              <line x1="349" y1="25" x2="369" y2="25" strokeWidth="1.5" stroke={T.text}/>
              <path d="M15 110 C10 120 10 130 30 135 L450 135 C465 132 468 122 460 110 Z"/>
              <path d="M15 115 C5 125 0 155 0 160 L0 160" fill="none" strokeWidth="1" stroke={T.text} opacity="0.3"/>
            </svg>
          </div>

          {/* Left text column (35%) */}
          <div style={{ flex: "0 0 35%", display: "flex", flexDirection: "column", justifyContent: "center" }}>
            <div style={{ ...TYPE_SCALE.EYEBROW, fontFamily: T.fontDisplay, color: T.textDim, marginBottom: 10 }}>AI-Assisted Delivery</div>
            <h1 style={{ fontFamily: T.fontDisplay, ...TYPE_SCALE.HERO, color: T.text, margin: "0 0 10px" }}>
              GenAI Transformation<br />
              <span style={{ background: `linear-gradient(90deg, ${T.gradient[0]}, ${T.gradient[1]})`, WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>Advocacy Deck</span>
            </h1>
            <p style={{ ...TYPE_SCALE.BODY, color: T.textMuted, margin: "0 0 20px", maxWidth: 420 }}>Five core pages. One clean storyline. Open the optional Service Platform one-pager below.</p>

            {/* Inline stats 2x2 */}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, marginBottom: 20 }}>
              {landingStats.map((s, i) => {
                const accentColor = [T.accent, T.gradient[1], T.gradient[0], T.accent][i];
                return (
                  <div key={i} style={{ borderRadius: 8, padding: "12px 16px", background: T.bgDeep, borderLeft: `2px solid ${accentColor}` }}>
                    <div style={{ fontFamily: T.fontDisplay, fontSize: 28, fontWeight: 800, color: accentColor, lineHeight: 1, marginBottom: 4 }}>{s.val}</div>
                    <div style={{ ...TYPE_SCALE.EYEBROW, fontSize: 10, color: T.textMuted }}>{s.lbl}</div>
                  </div>
                );
              })}
            </div>

            {/* Optional platform link */}
            {optionalPlatform && (
              <div
                onClick={(e) => { const r = e.currentTarget.getBoundingClientRect(); handleSelect("platform", { x: r.left + r.width / 2, y: r.top + r.height / 2 }); }}
                onMouseEnter={() => setHovered("platform")}
                onMouseLeave={() => setHovered(null)}
                style={{
                  cursor: "pointer", borderRadius: 8, padding: "12px 16px",
                  background: T.bgCard,
                  borderLeft: `3px solid ${hovered === "platform" ? optionalPlatform.color : optionalPlatform.color + "40"}`,
                  transition: "border-color 0.2s ease",
                }}>
                <div style={{ ...TYPE_SCALE.EYEBROW, fontSize: 10, fontFamily: T.fontDisplay, color: optionalPlatform.colorLight, marginBottom: 4 }}>Optional One-Pager</div>
                <div style={{ fontFamily: T.fontDisplay, ...TYPE_SCALE.CARD, color: T.text, marginBottom: 4 }}>{optionalPlatform.title}</div>
                <p style={{ ...TYPE_SCALE.CAPTION, color: T.textMuted, margin: "0 0 6px" }}>{optionalPlatform.subtitle}</p>
                <div style={{ display: "flex", alignItems: "center", gap: 6, color: optionalPlatform.color, ...TYPE_SCALE.CAPTION, fontWeight: 700, fontFamily: T.fontDisplay }}>
                  <span>Open</span><span>&#8594;</span>
                </div>
              </div>
            )}

            <div style={{ marginTop: 12, display: "flex", gap: 8, alignSelf: "flex-start" }}>
              <button onClick={() => setTheme(null)} style={{ background: "none", border: `1px solid ${T.textDim}30`, borderRadius: 6, padding: "6px 12px", ...TYPE_SCALE.CAPTION, color: T.textDim, cursor: "pointer", fontFamily: T.fontBody }}>{T.name} &#9998;</button>
              <div style={{ padding: "6px 14px", borderRadius: 6, background: T.accent + "10", border: `1px solid ${T.accent}22`, ...TYPE_SCALE.CAPTION, color: T.textMuted }}>
                Use <strong style={{ color: T.accent }}>npm run export:pdf</strong> or <strong style={{ color: T.accent }}>npm run export:images</strong>
              </div>
            </div>
          </div>

          {/* Right tile grid (65%) */}
          <div style={{ flex: "0 0 65%", display: "grid", gridTemplateColumns: "1fr 1fr", gridTemplateRows: "1fr 1fr 1fr", gap: 12, alignContent: "center" }}>
            {primaryTopics.map((t, i) => (
              <LandingTile
                key={t.id}
                topic={t}
                onClick={handleSelect}
                hovered={hovered}
                onHover={setHovered}
                borderVariant={i % 2 === 0 ? "left" : "top"}
              />
            ))}
          </div>
        </div>
      )}
      {active === "overview" && <OverviewScreen topic={activeTopic} onBack={handleBack} />}
      {active === "human" && <HumanScreen topic={activeTopic} onBack={handleBack} />}
      {active === "hurdles" && <HurdlesScreen topic={activeTopic} onBack={handleBack} />}
      {active === "future" && <FutureScreen topic={activeTopic} onBack={handleBack} />}
      {active === "platform" && <PlatformScreen topic={activeTopic} onBack={handleBack} />}
      {active === "sprint" && <SprintScreen topic={activeTopic} onBack={handleBack} />}
    </div>
    </ThemeCtx.Provider>
  );
}
