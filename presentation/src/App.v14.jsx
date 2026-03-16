/**
 * App.v14 — Registry-based presenter app (Phase 5, Strangler Fig).
 *
 * Key changes from v13 monolith:
 *   - Imports ThemeContext + ChromeContext from extracted context modules
 *   - Imports register-all.js as a side-effect (populates layout registry)
 *   - Replaces 25-case renderActiveTopic() switch with <LayoutRenderer>
 *   - Imports CometTransition, ThematicIntro, LandingTile from extracted components
 *
 * All DECKS, createDeckPreset, and transcription functions are preserved
 * verbatim from the monolith — they are data/logic, not renderers.
 */

import React, { useState, useEffect, useMemo, useCallback, useRef } from "react";
import PropTypes from "prop-types";

// ── Content imports ────────────────────────────────────────────────────────
import { themeId as genaiThemeId, contentSlides as genaiContentSlides, sprintNodes as genaiSprintNodes } from "./content/genai-advocacy/deck.js";
import { atelierSage, signalCobalt } from "./content/reference-decks/index.js";
import * as vergePop from "./content/verge-pop/deck.js";
import * as onboarding from "./content/onboarding/deck.js";
import * as onboardingOp from "./content/onboarding-op/deck.js";
import * as studio from "./content/studio/deck.js";
import * as engineering from "./content/engineering/deck.js";

// ── Token imports ─────────────────────────────────────────────────────────
import { THEMES, THEMES_BY_ID } from "./tokens/themes.ts";
import { resolveTopicColors, resolveIntroStatColors } from "./tokens/palette.ts";
import { STYLE_MODES, STYLE_MODES_BY_ID } from "./tokens/style-modes.ts";

// ── Design-system context (extracted) ─────────────────────────────────────
import { ThemeContext, ChromeContext } from "./components/context/index.js";
import { usePresentationViewport } from "./components/hooks/index.js";

// ── Extracted components ──────────────────────────────────────────────────
import { CometTransition, ThematicIntro } from "./components/animations/index.js";
import { LandingTile } from "./components/cards/index.js";
import { ControlPanel, OptionalDeckLink } from "./components/navigation/index.js";

// ── Layout registry: side-effect import registers all 34 layouts ───────────
import "./layouts/register-all.js";
import { layoutRegistry } from "./layouts/registry.ts";
import { LayoutRenderer } from "./layouts/LayoutRenderer.tsx";

// ── Transcription (cross-family layout normalisation) ─────────────────────
import { transcribeTopic } from "./transcription.ts";

// ═════════════════════════════════════════════════════════════════════
// STATIC DATA
// ═════════════════════════════════════════════════════════════════════

const topics = [
  {
    id: "hurdles", order: 5, layout: "before-after",
    num: "02", title: "Hurdles We Overcame",
    subtitle: "What changed from day one to delivery",
    color: "#F59E0B", colorLight: "#FBBF24", colorGlow: "rgba(245,158,11,0.3)", icon: "⬡",
    cards: [
      { title: "Prompt Standardization", challenge: "Developers used ad-hoc, inconsistent prompts — variable quality and constant refactoring.", fix: "Established versioned prompt templates with embedded architecture context and coding standards." },
      { title: "Process Realignment", challenge: "Traditional review workflows didn't account for AI-generated code patterns and volume.", fix: "Introduced AI-specific gated review checklists — convention adherence, test validation on every PR." },
      { title: "Governance Clearance", challenge: "Federal context required legal and policy approval before any AI-assisted code could reach production.", fix: "Proactively engaged internal risk, internal legal, and client legal to establish approval frameworks." },
      { title: "Team Enablement", challenge: "Team had varying levels of comfort and fluency with AI-assisted development tooling.", fix: "Internal hackathon built hands-on proficiency with tools and guardrails before delivery began." },
    ],
    callout: "Every hurdle became a guardrail. The friction we overcame early is the governance that keeps us fast now.",
  },
  {
    id: "human", order: 4, layout: "stat-cards",
    num: "01", title: "Human in the Loop",
    subtitle: "AI Accelerates. Humans Govern.",
    color: "#0891B2", colorLight: "#22D3EE", colorGlow: "rgba(8,145,178,0.3)", icon: "◉",
    cards: [
      { title: "Gated Review Process", body: "Every line of AI-assisted code passed through structured pull request reviews with project-specific checklists before reaching production.", stat: "100%", statLabel: "Human-Reviewed" },
      { title: "Context-Rich Prompts", body: "Standardized prompt templates embedded with architecture documentation, data models, and coding standards kept AI output anchored to the actual system.", stat: "~90%", statLabel: "AI-Assisted Code" },
      { title: "Zero Critical Defects", body: "Disciplined human governance produced zero critical defects at production release — proving speed doesn't sacrifice quality.", stat: "0", statLabel: "Critical Defects" },
    ],
    callout: "AI generated the code. Humans owned every decision. That's not a limitation — it's the model.",
  },
  {
    id: "sprint", order: 6, layout: "process-cycle",
    num: "04", title: "AI Sprint Cycle",
    subtitle: "Human checkpoints at every stage of AI-assisted delivery",
    color: "#8B5CF6", colorLight: "#A78BFA", colorGlow: "rgba(139,92,246,0.3)", icon: "⟳",
    callout: "The AI modified sprint cycle includes numerous human-in-the-loop checkpoints. Development included rapid iterations and adherence to Agile best practices.",
  },
  {
    id: "future", order: 7, layout: "h-strip",
    num: "03", title: "Looking Ahead",
    subtitle: "Better steering — not more automation — is the next multiplier",
    color: "#10B981", colorLight: "#34D399", colorGlow: "rgba(16,185,129,0.3)", icon: "△",
    cards: [
      { title: "Model Steering & Planning", body: "System prompts, prefills, and tool configs encode architecture standards and compliance guardrails before developers write a single prompt." },
      { title: "Evolved Prompt Library", body: "Templates evolve from standalone instructions to modular components operating within a steered context — version-controlled, regression-tested." },
      { title: "Human-Governed Pipeline", body: "Automated static analysis and security scanning assist at every commit, but humans make the merge and deploy decisions." },
      { title: "Team Enablement Kit", body: "Onboarding now covers model steering techniques alongside prompt writing — adoption in days, not months." },
    ],
    callout: "The playbook is proven. The automated pipeline turns one project win into a practice-wide competitive advantage.",
  },
];

const sprintNodes = [
  { icon: "📋", label: "Requirements", type: "human" },
  { icon: "🖥️", label: "UI Mockup", type: "human" },
  { icon: "🤖", label: "AI Converts AC", type: "ai" },
  { icon: "✅", label: "AC Refinement", type: "human" },
  { icon: "👥", label: "Human Review", type: "human" },
  { icon: "⚙️", label: "AI Gen Code", type: "ai" },
  { icon: "💻", label: "Code Output", type: "ai" },
  { icon: "👥", label: "Code Review", type: "human" },
  { icon: "🧪", label: "Testing", type: "human" },
  { icon: "🐛", label: "Defect Fix", type: "human" },
  { icon: "🚀", label: "Deploy", type: "human" },
  { icon: "📊", label: "Client Review", type: "human" },
];

const DEFAULT_LANDING_STATS = [
  { val: "~40%", lbl: "Productivity Uplift" },
  { val: "2 mo", lbl: "Prototype → Production" },
  { val: "0", lbl: "Critical Defects" },
  { val: "~90%", lbl: "AI-Assisted Code" },
  { val: "~95%", lbl: "Sprint Predictability" },
  { val: "1 wk", lbl: "Sprint Cadence" },
];

const LAYOUT_ICONS = {
  "two-col": "◌",
  "stat-cards": "◉",
  "before-after": "⬡",
  "process-cycle": "⟳",
  "h-strip": "△",
  "process-lanes": "▤",
  "stat-hero": "📊",
  "quote-collage": "💬",
  "badge-grid": "🏷️",
  "data-table": "📋",
  "bar-chart": "📈",
  "color-blocks": "🎨",
  "info-cards": "📋",
  "checklist": "🛡️",
  "workflow": "⚙️",
  "pillars": "🔬",
  "catalog": "🔐",
  "op-brief": "📑",
  "op-flow": "🔀",
  "hb-chapter": "📖",
  "hb-practices": "📝",
  "hb-process": "🔄",
  "hb-manifesto": "📜",
  "hb-index": "📇",
  "eng-architecture": "🏗️",
  "eng-code-flow": "🔗",
  "eng-tech-stack": "⚙️",
  "eng-roadmap": "🗺️",
};

const SPRINT_NODE_ICONS = {
  RQ: "📋",
  UI: "🖥️",
  AD: "🤖",
  RF: "✅",
  RV: "👥",
  AC: "⚙️",
  CO: "💻",
  PR: "👥",
  QA: "🧪",
  FX: "🐛",
  DP: "🚀",
  RO: "📊",
  BR: "📝",
  IN: "💡",
  FR: "🧩",
  ED: "✍️",
  ST: "🧠",
  CR: "🔎",
  AP: "✅",
  CL: "🗂️",
  TG: "🏷️",
  PL: "📈",
  PX: "📤",
};

// ═════════════════════════════════════════════════════════════════════
// DECK FACTORY
// ═════════════════════════════════════════════════════════════════════

function getInitialDeckKey() {
  const param = new URLSearchParams(globalThis.window?.location?.search ?? "").get("deck");
  return param || "onboarding";
}

function padTopicNumber(index) {
  return String(index + 1).padStart(2, "0");
}

function normalizeSprintNodes(nodes) {
  return (nodes || []).map((node) => ({
    ...node,
    icon: node.icon || SPRINT_NODE_ICONS[node.abbr] || "•",
  }));
}

function normalizeDeckTopics(slides) {
  return (slides || []).map((slide, index) => ({
    ...slide,
    num: slide.num || padTopicNumber(index),
    icon: slide.icon || LAYOUT_ICONS[slide.layout] || "•",
    colorLight: slide.colorLight || slide.color,
    colorGlow: slide.colorGlow || `${slide.color}33`,
    cards: slide.cards || [],
    heroPoints: slide.heroPoints || [],
    talkingPoints: slide.talkingPoints || [],
    focusPanels: slide.focusPanels || [],
    capabilities: slide.capabilities || [],
    lanes: slide.lanes || [],
  }));
}

function createDeckPreset(config) {
  return {
    ...config,
    topics: normalizeDeckTopics(config.topics),
    sprintNodes: normalizeSprintNodes(config.sprintNodes),
  };
}

const CURRENT_DECK = createDeckPreset({
  id: "current",
  themeId: "midnight-teal",
  brandLine: "AI-Assisted Delivery",
  title: "GenAI",
  titleAccent: "Advocacy Deck",
  tagline: "Four narratives. One story. Select a topic to explore.",
  introBrandLine: "AI-Assisted Delivery",
  introTitle: "GenAI Transformation",
  introSubtitle: "From prototype to production in 2 months",
  introStats: [
    { val: "~40%", lbl: "Uplift", color: "#22D3EE" },
    { val: "2 mo", lbl: "Delivery", color: "#34D399" },
    { val: "0", lbl: "Defects", color: "#10B981" },
    { val: "~90%", lbl: "AI Code", color: "#A78BFA" },
  ],
  stats: DEFAULT_LANDING_STATS,
  topics,
  sprintNodes,
});

const GENAI_MANIFEST_DECK = createDeckPreset({
  id: "genai",
  themeId: genaiThemeId,
  brandLine: "AI-Assisted Delivery",
  title: "GenAI",
  titleAccent: "Case Study",
  tagline: "Governance, execution, and scale — rendered from the shared deck manifest.",
  introBrandLine: "AI-Assisted Delivery",
  introTitle: "GenAI Transformation",
  introSubtitle: "Manifest-driven deck rendering for the full case-study story",
  introStats: [
    { val: "6", lbl: "Content Slides", color: "#67E8F9" },
    { val: "1", lbl: "Optional Path", color: "#38BDF8" },
    { val: "0", lbl: "Hardcoded Lists", color: "#10B981" },
    { val: "1", lbl: "Shared Manifest", color: "#A78BFA" },
  ],
  stats: [
    { val: "6", lbl: "Core Slides" },
    { val: "1", lbl: "Optional Platform" },
    { val: "1", lbl: "Shared Theme" },
    { val: "100%", lbl: "Manifest Driven" },
  ],
  topics: genaiContentSlides,
  sprintNodes: genaiSprintNodes,
});

const ATELIER_SAGE_DECK = createDeckPreset({
  id: "atelier-sage",
  themeId: atelierSage.themeId,
  brandLine: "Reference Study",
  title: "Atelier",
  titleAccent: "Sage",
  tagline: "Editorial pacing, paper surfaces, and restrained process language.",
  introBrandLine: "Reference Study",
  introTitle: "Atelier Sage",
  introSubtitle: "Editorial process deck inspired by deck.gallery",
  introStats: [
    { val: "Soft", lbl: "Palette", color: "#557868" },
    { val: "4", lbl: "Sample Slides", color: "#D7AA58" },
    { val: "1", lbl: "Theme", color: "#C87052" },
    { val: "Calm", lbl: "Tone", color: "#7F9A8C" },
  ],
  stats: [
    { val: "Sage", lbl: "Primary Accent" },
    { val: "Warm", lbl: "Paper Surface" },
    { val: "Serif", lbl: "Display Tone" },
    { val: "4", lbl: "Sample Slides" },
  ],
  topics: atelierSage.contentSlides,
  sprintNodes: atelierSage.sprintNodes,
});

const SIGNAL_COBALT_DECK = createDeckPreset({
  id: "signal-cobalt",
  themeId: signalCobalt.themeId,
  brandLine: "Reference Study",
  title: "Signal",
  titleAccent: "Cobalt",
  tagline: "Swiss-modern rhythm with cobalt interruption slides and orange utility accents.",
  introBrandLine: "Reference Study",
  introTitle: "Signal Cobalt",
  introSubtitle: "Systems deck inspired by deck.gallery",
  introStats: [
    { val: "Grid", lbl: "Discipline", color: "#1328FF" },
    { val: "5", lbl: "Sample Slides", color: "#FF6A13" },
    { val: "B/W", lbl: "Foundation", color: "#121212" },
    { val: "Sharp", lbl: "Tone", color: "#5063FF" },
  ],
  stats: [
    { val: "Cobalt", lbl: "Primary Accent" },
    { val: "Orange", lbl: "Utility Signal" },
    { val: "Swiss", lbl: "Composition" },
    { val: "5", lbl: "Sample Slides" },
  ],
  topics: signalCobalt.contentSlides,
  sprintNodes: signalCobalt.sprintNodes,
});

const VERGE_POP_DECK = createDeckPreset({
  id: "verge-pop",
  themeId: vergePop.themeId,
  brandLine: "Community Trends",
  title: "Verge",
  titleAccent: "Pop",
  tagline: "Bold data stories about digital communities, platforms, and AI.",
  introBrandLine: "Community Trends",
  introTitle: "Community & Connection",
  introSubtitle: "How people find meaning in digital spaces",
  introStats: [
    { val: "91%", lbl: "Prefer Small", color: "#00CC99" },
    { val: "78%", lbl: "Content Led", color: "#3399FF" },
    { val: "55%", lbl: "AI Creative", color: "#FF3366" },
    { val: "90%", lbl: "Belonging", color: "#FFD600" },
  ],
  stats: [
    { val: "8", lbl: "Data Stories" },
    { val: "6", lbl: "New Layouts" },
    { val: "Pop", lbl: "Art Style" },
    { val: "4", lbl: "Color Themes" },
  ],
  topics: vergePop.contentSlides,
  sprintNodes: vergePop.sprintNodes,
});

const STUDIO_DECK = createDeckPreset({
  id: "studio",
  themeId: studio.themeId,
  brandLine: "AI Studio",
  title: "Studio",
  titleAccent: "Handbook",
  tagline: "Six chapters. From who we are to your first day. Select a chapter to begin.",
  introBrandLine: "AI Studio · Handbook",
  introTitle: "The Studio Handbook",
  introSubtitle: "How we work, what we build, what we believe.",
  introStats: [
    { val: "5",  lbl: "Practices",  color: "#F4E04D" },
    { val: "8",  lbl: "Process Steps", color: "#F2A614" },
    { val: "6+", lbl: "Client Archetypes", color: "#C53B2F" },
    { val: "1",  lbl: "Manifesto",   color: "#0E0E0B" },
  ],
  stats: [
    { val: "6",  lbl: "Chapters" },
    { val: "5",  lbl: "Practice Areas" },
    { val: "8",  lbl: "Process Steps" },
    { val: "Yellow", lbl: "Accent" },
  ],
  topics: studio.contentSlides,
  sprintNodes: studio.sprintNodes,
});

const ONBOARDING_OP_DECK = createDeckPreset({
  id: "onboarding-op",
  themeId: onboardingOp.themeId,
  brandLine: "GenAI Delivery",
  title: "Onboarding",
  titleAccent: "One-Pagers",
  tagline: "Seven modules as dense one-pager briefs. Select a topic.",
  introBrandLine: "GenAI Delivery · One-Pagers",
  introTitle: "AI-Assisted Development",
  introSubtitle: "One-pager format — all key info on a single screen",
  introStats: [
    { val: "7", lbl: "Modules", color: "#F97316" },
    { val: "Op", lbl: "One-Pager", color: "#FBBF24" },
    { val: "Dense", lbl: "Format", color: "#A855F7" },
    { val: "Fast", lbl: "Scan", color: "#22C55E" },
  ],
  stats: [
    { val: "7", lbl: "Modules" },
    { val: "2", lbl: "Layout Types" },
    { val: "Dense", lbl: "One-Pager Format" },
    { val: "Fast", lbl: "At-a-Glance" },
  ],
  topics: onboardingOp.contentSlides,
  sprintNodes: onboardingOp.sprintNodes,
});

const ONBOARDING_DECK = createDeckPreset({
  id: "onboarding",
  themeId: onboarding.themeId,
  brandLine: "GenAI Delivery",
  title: "Onboarding",
  titleAccent: "Guidebook",
  tagline: "Seven modules. From expectations to execution. Select a topic to begin.",
  introBrandLine: "GenAI Delivery · Onboarding",
  introTitle: "AI-Assisted Development",
  introSubtitle: "Team guidebook for AI-assisted delivery workflows",
  introStats: [
    { val: "7", lbl: "Modules", color: "#F97316" },
    { val: "~99%", lbl: "AI-Assisted", color: "#FBBF24" },
    { val: "0", lbl: "Critical Defects", color: "#22C55E" },
    { val: "~95%", lbl: "Predictability", color: "#A855F7" },
  ],
  stats: [
    { val: "7", lbl: "Modules" },
    { val: "~99%", lbl: "AI-Assisted Code" },
    { val: "0", lbl: "Critical Defects" },
    { val: "~95%", lbl: "Sprint Predictability" },
  ],
  topics: onboarding.contentSlides,
  sprintNodes: onboarding.sprintNodes,
});

const ENGINEERING_DECK = createDeckPreset({
  id: "engineering",
  themeId: engineering.themeId,
  brandLine: "Design System",
  title: "Engineering",
  titleAccent: "Deep Dive",
  tagline: "Four modules. Architecture to roadmap. Select a topic to explore.",
  introBrandLine: "Design System · Engineering",
  introTitle: "Platform Architecture",
  introSubtitle: "From monolith to modular design system",
  introStats: [
    { val: "26", lbl: "Layouts", color: "#60A5FA" },
    { val: "6", lbl: "Families", color: "#34D399" },
    { val: "768", lbl: "Lines", color: "#A78BFA" },
    { val: "~1s", lbl: "Build", color: "#F59E0B" },
  ],
  stats: [
    { val: "26", lbl: "Registered Layouts" },
    { val: "6", lbl: "Layout Families" },
    { val: "4", lbl: "Architecture Layers" },
    { val: "7", lbl: "Migration Phases" },
  ],
  topics: engineering.contentSlides,
  sprintNodes: engineering.sprintNodes,
});

const DECKS = {
  current: CURRENT_DECK,
  genai: GENAI_MANIFEST_DECK,
  "atelier-sage": ATELIER_SAGE_DECK,
  "signal-cobalt": SIGNAL_COBALT_DECK,
  "verge-pop": VERGE_POP_DECK,
  onboarding: ONBOARDING_DECK,
  "onboarding-op": ONBOARDING_OP_DECK,
  studio: STUDIO_DECK,
  engineering: ENGINEERING_DECK,
};

// ═════════════════════════════════════════════════════════════════════
// TRANSCRIPTION FUNCTIONS  (cross-family layout normalisation)
// ═════════════════════════════════════════════════════════════════════
// Extracted to ./transcription.ts — imported above.

const HERO_IMAGE_DEFAULT = new URL(
  "./content/img/capabilities-deck-from-studio-freight (Large).png",
  import.meta.url,
).href;

// ═════════════════════════════════════════════════════════════════════
// APP
// ═════════════════════════════════════════════════════════════════════

export default function App() {
  const viewport = usePresentationViewport();
  const [deckKey, setDeckKey] = useState(getInitialDeckKey);
  const deck = DECKS[deckKey] || CURRENT_DECK;
  const [theme, setTheme] = useState(() => THEMES_BY_ID[deck.themeId] || THEMES[0]);
  const [themeManual, setThemeManual] = useState(false);
  const [renderFamily, setRenderFamily] = useState("native");
  const [styleModeId, setStyleModeId] = useState("default");
  const chrome = STYLE_MODES_BY_ID[styleModeId];
  const [animOptions, setAnimOptions] = useState({ intro: false, comet: false });
  const [heroImage, setHeroImage] = useState(HERO_IMAGE_DEFAULT);
  const [heroImageEnabled, setHeroImageEnabled] = useState(true);
  const [slideViewMode, setSlideViewMode] = useState("native");
  const [introDone, setIntroDone] = useState(true);
  const [active, setActive] = useState(null);
  const [transitioning, setTransitioning] = useState(false);
  const [hovered, setHovered] = useState(null);
  const [comet, setComet] = useState({ active: false, from: null, color: null, targetId: null });

  // Gate intro animation — skip when disabled, re-queue when enabled
  useEffect(() => {
    if (!animOptions.intro) setIntroDone(true);
    else setIntroDone(false);
  }, [animOptions.intro]);

  // ── Theme-adaptive color resolution + optional layout transcription ──
  const deckTopics = useMemo(() => {
    const colorResolved = theme ? resolveTopicColors(deck.topics, theme) : deck.topics;
    if (renderFamily === "native") return colorResolved;
    return colorResolved.map(t => transcribeTopic(t, renderFamily));
  }, [deck.topics, theme, renderFamily]);

  const introStats = useMemo(() =>
    theme ? resolveIntroStatColors(deck.introStats, theme) : deck.introStats,
    [deck.introStats, theme],
  );

  // Reset state when switching decks
  const switchDeck = (key) => {
    setDeckKey(key);
    setActive(null);
    setSlideViewMode("native");
    setIntroDone(!animOptions.intro);
    if (!themeManual) {
      const nextDeck = DECKS[key] || CURRENT_DECK;
      const suggested = THEMES_BY_ID[nextDeck.themeId];
      if (suggested) setTheme(suggested);
    }
  };

  const resetToDeckTheme = () => {
    setThemeManual(false);
    const suggested = THEMES_BY_ID[deck.themeId];
    if (suggested) setTheme(suggested);
  };

  const handleSelect = (id, pos) => {
    const topic = deckTopics.find((t) => t.id === id);
    setSlideViewMode("native");
    if (!animOptions.comet) {
      setActive(id);
      return;
    }
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
  const handleBack = () => { setSlideViewMode("native"); setTransitioning(true); setTimeout(() => { setActive(null); setTransitioning(false); }, 350); };
  const activeTopic = deckTopics.find((t) => t.id === active);

  // Per-slide one-pager toggle: transcribe active topic when in onepager mode
  const effectiveTopic = useMemo(() => {
    if (!activeTopic || slideViewMode === "native") return activeTopic;
    return transcribeTopic(activeTopic, "onboarding");
  }, [activeTopic, slideViewMode]);

  const hasOnepagerView = activeTopic && !["op-brief", "op-flow"].includes(activeTopic.layout);

  // Resolve ControlPanel feature manifest from the active slide's layout
  const activeLayoutFeatures = useMemo(() => {
    if (!activeTopic) return undefined; // landing grid — show deck-level defaults
    return layoutRegistry.getFeatures(activeTopic.layout);
  }, [activeTopic]);

  const T = theme;
  const introDeck = { ...deck, introStats };

  return (
    <ThemeContext.Provider value={T}>
    <ChromeContext.Provider value={chrome}>
    <div style={{ fontFamily: T.fontBody, minHeight: "100dvh", background: T.bg, opacity: (transitioning && !comet.active) ? 0 : 1, transition: "opacity 0.35s ease", overflowY: viewport.overlayScroll }}>
      <link href={T.fontsUrl} rel="stylesheet" />
      <CometTransition from={comet.from} color={comet.color} active={comet.active} onDone={handleCometDone} />
      {!introDone && animOptions.intro && <ThematicIntro deck={introDeck} onComplete={() => setIntroDone(true)} />}
      {!active && introDone && (
        <div style={{ position: "relative", minHeight: "100dvh", display: "flex", flexDirection: "column", justifyContent: "center", padding: `${viewport.pagePaddingTop}px ${viewport.pagePaddingX}px ${viewport.pagePaddingBottom}px`, opacity: comet.active ? 0 : 1, transition: "opacity 0.4s ease" }}>
          {/* Hero background image layer */}
          {heroImageEnabled && heroImage && (
            <div style={{ position: "absolute", inset: 0, zIndex: 0, pointerEvents: "none", backgroundImage: `url("${heroImage}")`, backgroundSize: "cover", backgroundPosition: "center", backgroundAttachment: "fixed", opacity: 0.22, borderRadius: "inherit" }} />
          )}
          <div style={{ position: "relative", zIndex: 1 }}>
            <div style={{ marginBottom: viewport.isPhone ? 24 : 32 }}>
              <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: 3, color: T.textDim, fontFamily: T.fontDisplay, fontWeight: 500, marginBottom: 10 }}>{deck.brandLine}</div>
              <h1 style={{ fontFamily: T.fontDisplay, fontSize: viewport.heroTitleSize, fontWeight: chrome.headingWeight, color: T.text, margin: "0 0 10px", letterSpacing: -1, lineHeight: 1.05, textTransform: chrome.headingTransform }}>
                {deck.title}<br /><span style={{ background: `linear-gradient(90deg,${T.gradient[0]},${T.gradient[1]})`, WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>{deck.titleAccent}</span>
              </h1>
              <p style={{ fontSize: viewport.bodySize, color: T.textDim, margin: 0, maxWidth: viewport.isPhone ? "100%" : 600 }}>{deck.tagline}</p>
            </div>
            <div style={{ display: "grid", gridTemplateColumns: viewport.isPhone ? "1fr" : viewport.isCompact ? "1fr 1fr" : "repeat(4, minmax(0, 1fr))", gap: viewport.cardGap }}>
              {deckTopics.map((t) => (
                <LandingTile
                  key={t.id}
                  title={t.title}
                  subtitle={t.subtitle}
                  icon={t.icon}
                  num={t.num}
                  color={t.color}
                  colorLight={t.colorLight}
                  colorGlow={t.colorGlow}
                  onClick={(pos) => handleSelect(t.id, pos)}
                  hovered={hovered === t.id}
                  onHover={(isHovered) => setHovered(isHovered ? t.id : null)}
                />
              ))}
            </div>
            {/* Optional one-pager links */}
            {deckTopics.filter(t => t.optional).map(t => (
              <OptionalDeckLink
                key={`opt-${t.id}`}
                topic={t}
                theme={T}
                chrome={chrome}
                onNavigate={(id, pos) => handleSelect(id, pos)}
              />
            ))}
            {/* ── Footer: stats ── */}
            <div style={{ marginTop: viewport.isPhone ? 24 : 32, paddingTop: 20, borderTop: `1px solid ${T.border || "rgba(255,255,255,0.06)"}` }}>
              <div style={{ display: "grid", gridTemplateColumns: viewport.isPhone ? "1fr 1fr" : "repeat(3, minmax(0, max-content))", gap: viewport.isPhone ? 12 : 36 }}>
                {deck.stats.map((s) => (
                  <div key={`${s.lbl}-${s.val}`}><div style={{ fontFamily: T.fontDisplay, fontSize: 22, fontWeight: 700, color: T.accent }}>{s.val}</div><div style={{ fontSize: 10, color: T.textDim, textTransform: "uppercase", letterSpacing: 0.8 }}>{s.lbl}</div></div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
      {/* Per-slide one-pager toggle */}
      {activeTopic && hasOnepagerView && (
        <button
          onClick={() => setSlideViewMode(v => v === "native" ? "onepager" : "native")}
          style={{
            position: "fixed", top: 16, right: 60, zIndex: 200,
            background: slideViewMode === "onepager" ? `${T.accent}20` : T.bgCard,
            border: `1px solid ${slideViewMode === "onepager" ? T.accent + "60" : T.textDim + "30"}`,
            borderRadius: 999, padding: "5px 14px", fontSize: 10,
            color: slideViewMode === "onepager" ? T.accent : T.textDim,
            cursor: "pointer", fontFamily: T.fontBody, letterSpacing: 0.8,
            textTransform: "uppercase",
          }}
        >
          {slideViewMode === "onepager" ? "◉ One-Pager" : "◎ Slide"}
        </button>
      )}
      {/* Active slide — registry-dispatched (replaces 25-case switch) */}
      {effectiveTopic && (
        <LayoutRenderer
          layout={effectiveTopic.layout}
          slide={effectiveTopic}
          themeId={deck.themeId}
          onBack={handleBack}
          nodes={deck.sprintNodes}
        />
      )}
      {/* Floating design control panel */}
      <ControlPanel
        decks={DECKS}
        deckKey={deckKey}
        onDeckChange={switchDeck}
        themes={THEMES}
        theme={T}
        onThemeChange={(t) => { setThemeManual(true); setTheme(t); }}
        onThemeReset={resetToDeckTheme}
        themeManual={themeManual}
        deckThemeId={deck.themeId}
        styleModes={STYLE_MODES}
        styleModeId={styleModeId}
        onStyleModeChange={setStyleModeId}
        renderFamily={renderFamily}
        onRenderFamilyChange={setRenderFamily}
        layoutFeatures={activeLayoutFeatures}
        animOptions={animOptions}
        onAnimOptionsChange={setAnimOptions}
        heroImage={heroImage}
        heroImageEnabled={heroImageEnabled}
        onHeroImageToggle={setHeroImageEnabled}
        onHeroImageChange={setHeroImage}
      />
    </div>
    </ChromeContext.Provider>
    </ThemeContext.Provider>
  );
}

App.displayName = "AppV14";
