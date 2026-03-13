import React, { useState, useEffect, useRef, useCallback, useMemo, createContext, useContext } from "react";
import PropTypes from "prop-types";

import { themeId as genaiThemeId, contentSlides as genaiContentSlides, sprintNodes as genaiSprintNodes } from "./src/content/genai-advocacy/deck.js";
import { atelierSage, signalCobalt } from "./src/content/reference-decks/index.js";
import * as vergePop from "./src/content/verge-pop/deck.js";
import { THEMES, THEMES_BY_ID, THEME_SELECTOR_FONTS_URL } from "./src/tokens/themes.js";
import { resolveTopicColors, resolveIntroStatColors } from "./src/tokens/palette.js";
import { STYLE_MODES, STYLE_MODES_BY_ID } from "./src/tokens/style-modes.js";

const ThemeCtx = createContext(THEMES[0]);
const ChromeCtx = createContext(STYLE_MODES_BY_ID["default"]);
const useChrome = () => useContext(ChromeCtx);

const positionPropType = PropTypes.shape({
  x: PropTypes.number.isRequired,
  y: PropTypes.number.isRequired,
});

const topicCardPropType = PropTypes.shape({
  title: PropTypes.string.isRequired,
  body: PropTypes.string,
  challenge: PropTypes.string,
  fix: PropTypes.string,
  icon: PropTypes.string,
  stat: PropTypes.string,
  statLabel: PropTypes.string,
});

const topicFocusPanelPropType = PropTypes.shape({
  label: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  body: PropTypes.string.isRequired,
});

const topicCapabilityPropType = PropTypes.shape({
  title: PropTypes.string.isRequired,
  body: PropTypes.string.isRequired,
  icon: PropTypes.string.isRequired,
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
  order: PropTypes.number.isRequired,
  layout: PropTypes.string.isRequired,
  num: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  subtitle: PropTypes.string.isRequired,
  color: PropTypes.string.isRequired,
  colorLight: PropTypes.string.isRequired,
  colorGlow: PropTypes.string.isRequired,
  icon: PropTypes.string.isRequired,
  optional: PropTypes.bool,
  eyebrow: PropTypes.string,
  summary: PropTypes.string,
  heroPoints: PropTypes.arrayOf(PropTypes.string),
  cards: PropTypes.arrayOf(topicCardPropType),
  talkingPoints: PropTypes.arrayOf(PropTypes.string),
  callout: PropTypes.string.isRequired,
  focusPanels: PropTypes.arrayOf(topicFocusPanelPropType),
  capabilities: PropTypes.arrayOf(topicCapabilityPropType),
  lanes: PropTypes.arrayOf(topicLanePropType),
});

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

function getInitialDeckKey() {
  const param = new URLSearchParams(globalThis.window?.location?.search ?? "").get("deck");
  return param || "current";
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

const DECKS = {
  current: CURRENT_DECK,
  genai: GENAI_MANIFEST_DECK,
  "atelier-sage": ATELIER_SAGE_DECK,
  "signal-cobalt": SIGNAL_COBALT_DECK,
  "verge-pop": VERGE_POP_DECK,
};

// ─── PARTICLES ───
function Particles({ color, type, active }) {
  const canvasRef = useRef(null);
  const pRef = useRef([]);
  const animRef = useRef(null);
  useEffect(() => {
    const c = canvasRef.current; if (!c) return;
    const ctx = c.getContext("2d");
    c.width = c.offsetWidth * 2; c.height = c.offsetHeight * 2; ctx.scale(2, 2);
    const W = c.offsetWidth, H = c.offsetHeight;
    pRef.current = [];
    let n;
    if (type === "hurdles") {
      n = 60;
    } else if (type === "sprint") {
      n = 40;
    } else {
      n = 30;
    }
    for (let i = 0; i < n; i++) {
      const hurdleParticle = type === "hurdles";
      pRef.current.push({
        x: getRandomUnit() * W,
        y: getRandomUnit() * H,
        vx: hurdleParticle ? (getRandomUnit() - 0.3) * 3 : (getRandomUnit() - 0.5) * 0.5,
        vy: hurdleParticle ? -getRandomUnit() * 4 - 1 : (getRandomUnit() - 0.5) * 0.5,
        r: hurdleParticle ? getRandomUnit() * 3 + 1 : getRandomUnit() * 2 + 1,
        o: getRandomUnit() * 0.5 + 0.15,
        life: getRandomUnit() * 100,
      });
    }
    function draw() {
      ctx.clearRect(0,0,W,H);
      pRef.current.forEach(p => {
        p.life++;
        if(type==="hurdles"){p.x+=p.vx;p.y+=p.vy;p.vy-=0.02;if(p.y<-10||p.x<-10||p.x>W+10){p.x=getRandomUnit()*W;p.y=H+10;p.vy=-getRandomUnit()*4-1;p.vx=(getRandomUnit()-0.3)*3;}}
        else if(type==="human"){p.x+=Math.sin(p.life*0.015)*0.3;p.y+=Math.cos(p.life*0.012)*0.3;}
        else if (type === "sprint") {
          const cx = W / 2;
          const cy = H / 2;
          const a = Math.atan2(p.y - cy, p.x - cx);
          p.x += Math.cos(a + Math.PI / 2) * 0.35;
          p.y += Math.sin(a + Math.PI / 2) * 0.35;
          const d = Math.sqrt((p.x - cx) ** 2 + (p.y - cy) ** 2);
          if (d > Math.max(W, H) * 0.55) {
            p.x = cx + (getRandomUnit() - 0.5) * W * 0.4;
            p.y = cy + (getRandomUnit() - 0.5) * H * 0.4;
          }
        }
        else {
          p.x += p.vx;
          p.y += p.vy;
          if (p.x < 0 || p.x > W) {
            p.vx *= -1;
          }
          if (p.y < 0 || p.y > H) {
            p.vy *= -1;
          }
        }
        ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fillStyle=color+Math.round(p.o*255).toString(16).padStart(2,"0");ctx.fill();
      });
      if (type === "human") {
        const pts = pRef.current;
        for (let i = 0; i < pts.length; i++) {
          for (let j = i + 1; j < pts.length; j++) {
            const dx = pts[i].x - pts[j].x;
            const dy = pts[i].y - pts[j].y;
            const d = Math.sqrt(dx * dx + dy * dy);
            if (d < 120) {
              ctx.beginPath();
              ctx.moveTo(pts[i].x, pts[i].y);
              ctx.lineTo(pts[j].x, pts[j].y);
              ctx.strokeStyle = color + Math.round((1 - d / 120) * 40).toString(16).padStart(2, "0");
              ctx.lineWidth = 0.5;
              ctx.stroke();
            }
          }
        }
      }
      animRef.current=requestAnimationFrame(draw);
    }
    if(active) draw();
    return () => cancelAnimationFrame(animRef.current);
  }, [color, type, active]);
  return <canvas ref={canvasRef} style={{ position:"absolute",inset:0,width:"100%",height:"100%",pointerEvents:"none",opacity:active?1:0,transition:"opacity 0.8s" }}/>;
}
Particles.propTypes = {
  color: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired,
  active: PropTypes.bool.isRequired,
};

// ─── COMET TRANSITION ───
function CometTransition({ from, color, active, onDone }) {
  const onDoneRef = useRef(onDone);
  onDoneRef.current = onDone;
  const [phase, setPhase] = useState("idle"); // idle → launch → done

  useEffect(() => {
    if (!active || !from) return;
    setPhase("idle");
    // Force reflow then launch
    const t1 = requestAnimationFrame(() => {
      requestAnimationFrame(() => setPhase("launch"));
    });
    const t2 = setTimeout(() => {
      setPhase("done");
      onDoneRef.current();
    }, 700);
    return () => { cancelAnimationFrame(t1); clearTimeout(t2); };
  }, [active, from]);

  if (!active || !from) return null;

  const tx = (typeof window !== "undefined" ? window.innerWidth / 2 : 500) - from.x;
  const ty = (typeof window !== "undefined" ? window.innerHeight / 2 : 400) - from.y;

  return (
    <div style={{ position: "fixed", inset: 0, zIndex: 100, pointerEvents: "none", overflow: "hidden" }}>
      {/* Comet head */}
      <div style={{
        position: "absolute",
        left: from.x - 10,
        top: from.y - 10,
        width: 20, height: 20,
        borderRadius: "50%",
        background: color,
        boxShadow: `0 0 30px 10px ${color}, 0 0 60px 20px ${color}80, 0 0 4px 2px #FFFFFF`,
        transform: phase === "launch" ? `translate(${tx}px, ${ty}px) scale(0.3)` : "translate(0,0) scale(1)",
        opacity: phase === "launch" ? 0.2 : 1,
        transition: "transform 0.6s cubic-bezier(0.16,1,0.3,1), opacity 0.6s ease",
      }} />
      {/* Trail */}
      {[...Array(8)].map((_, i) => (
        <div key={i} style={{
          position: "absolute",
          left: from.x - (6 - i * 0.5),
          top: from.y - (6 - i * 0.5),
          width: (12 - i), height: (12 - i),
          borderRadius: "50%",
          background: color,
          opacity: phase === "launch" ? 0 : (0.5 - i * 0.06),
          transform: phase === "launch" ? `translate(${tx * (1 - i * 0.08)}px, ${ty * (1 - i * 0.08)}px)` : "translate(0,0)",
          transition: `transform ${0.6 + i * 0.03}s cubic-bezier(0.16,1,0.3,1) ${i * 0.02}s, opacity ${0.5}s ease ${i * 0.02}s`,
        }} />
      ))}
      {/* Impact ring */}
      <div style={{
        position: "absolute",
        left: "50%", top: "50%",
        width: phase === "launch" ? 200 : 0,
        height: phase === "launch" ? 200 : 0,
        marginLeft: phase === "launch" ? -100 : 0,
        marginTop: phase === "launch" ? -100 : 0,
        borderRadius: "50%",
        border: `2px solid ${color}60`,
        background: `${color}08`,
        transition: "all 0.4s 0.4s ease-out",
        opacity: phase === "launch" ? 0 : 1,
      }} />
    </div>
  );
}
CometTransition.propTypes = {
  from: positionPropType,
  color: PropTypes.string,
  active: PropTypes.bool.isRequired,
  onDone: PropTypes.func.isRequired,
};

// ─── LANDING TILE ───
function LandingTile({ topic, onClick, hovered, onHover }) {
  const T = useContext(ThemeCtx);
  const C = useChrome();
  const h = hovered === topic.id;
  const glowShadow = C.useGlow ? `0 0 40px ${topic.colorGlow}, 0 8px 32px rgba(0,0,0,0.4)` : `0 8px 32px rgba(0,0,0,0.5)`;
  const restShadow = C.useSoftShadow ? "0 4px 20px rgba(0,0,0,0.3)" : "none";
  return (
    <div onClick={(e) => { const r = e.currentTarget.getBoundingClientRect(); onClick(topic.id, { x: r.left + r.width / 2, y: r.top + r.height / 2 }); }} onMouseEnter={() => onHover(topic.id)} onMouseLeave={() => onHover(null)}
      style={{ flex:1,position:"relative",cursor:"pointer",overflow:"hidden",borderRadius:C.tileRadius,padding:"32px 28px",display:"flex",flexDirection:"column",justifyContent:"space-between",minHeight:300,background:T.bgDeep,
        border:`${C.cardBorderWidth}px solid ${h?topic.color+"60":"rgba(255,255,255,0.06)"}`,boxShadow:h?glowShadow:restShadow,
        transform:h?"translateY(-8px) scale(1.02)":"translateY(0) scale(1)",transition:"all 0.4s cubic-bezier(0.34,1.56,0.64,1)" }}>
      <div>
        <div style={{ fontFamily:T.fontDisplay,fontSize:12,fontWeight:500,color:topic.color,letterSpacing:C.labelTracking,textTransform:"uppercase",marginBottom:6,opacity:0.8 }}>{topic.num}</div>
        <div style={{ fontSize:36,marginBottom:10,lineHeight:1,filter:h&&C.useGlow?`drop-shadow(0 0 12px ${topic.colorGlow})`:"none",transition:"filter 0.4s" }}>{topic.icon}</div>
        <h2 style={{ fontFamily:T.fontDisplay,fontSize:22,fontWeight:C.headingWeight,color:T.text,lineHeight:1.15,margin:"0 0 6px",textTransform:C.headingTransform }}>{topic.title}</h2>
        <p style={{ fontSize:13,color:T.textDim,lineHeight:1.5,margin:0 }}>{topic.subtitle}</p>
      </div>
      <div style={{ display:"flex",alignItems:"center",gap:8,marginTop:20,color:topic.color,fontSize:12,fontWeight:600,fontFamily:T.fontDisplay,transform:h?"translateX(6px)":"translateX(0)",transition:"transform 0.3s" }}>
        <span>Explore</span><span style={{ fontSize:16,lineHeight:1 }}>→</span>
      </div>
      <div style={{ position:"absolute",bottom:0,left:0,right:0,height:C.accentBarHeight,background:topic.color,opacity:h?1:0.4,transition:"opacity 0.3s" }}/>
    </div>
  );
}
LandingTile.propTypes = {
  topic: topicPropType.isRequired,
  onClick: PropTypes.func.isRequired,
  hovered: PropTypes.string,
  onHover: PropTypes.func.isRequired,
};

// ─── THEMATIC INTRO ───
function ThematicIntro({ deck, onComplete }) {
  const [phase, setPhase] = useState(0);
  const onCompleteRef = useRef(onComplete);
  onCompleteRef.current = onComplete;
  const introStats = deck?.introStats || CURRENT_DECK.introStats;

  useEffect(() => {
    const timers = [
      setTimeout(() => setPhase(1), 100),   // stars appear + warp
      setTimeout(() => setPhase(2), 1200),  // comet launches
      setTimeout(() => setPhase(3), 2200),  // title appears
      setTimeout(() => setPhase(4), 3400),  // impact burst
      setTimeout(() => { setPhase(5); onCompleteRef.current(); }, 4200),
    ];
    return () => timers.forEach(clearTimeout);
  }, []);

  // Generate static star positions once
  const starsRef = useRef(Array.from({ length: 50 }, () => ({
    x: 50 + (getRandomUnit() - 0.5) * 80,
    y: 50 + (getRandomUnit() - 0.5) * 80,
    s: getRandomUnit() * 2 + 1,
    d: getRandomUnit() * 0.8,
    hue: 190 + getRandomUnit() * 40,
    lightness: 70 + getRandomUnit() * 20,
  })));
  const streaksRef = useRef(Array.from({ length: 12 }, () => ({
    left: 15 + getRandomUnit() * 70,
    alpha: 0.1 + getRandomUnit() * 0.15,
    duration: 0.8 + getRandomUnit() * 0.6,
  })));

  return (
    <div style={{
      position: "fixed", inset: 0, zIndex: 200, background: "#020810",
      overflow: "hidden",
      opacity: phase >= 5 ? 0 : 1, transition: "opacity 0.6s ease",
    }}>
      <style>{`
        @keyframes warpStar {
          0% { transform: translate(-50%,-50%) scale(1); opacity: 0.6; }
          100% { transform: translate(-50%,-50%) scale(3) translateZ(0); opacity: 0; }
        }
        @keyframes cometFly {
          0% { transform: translate(0, -120vh) scale(0.3); opacity: 0; }
          15% { opacity: 1; }
          70% { transform: translate(0, 0) scale(1); opacity: 1; }
          100% { transform: translate(0, 0) scale(0); opacity: 0; }
        }
        @keyframes impactRing {
          0% { transform: translate(-50%,-50%) scale(0); opacity: 0.8; }
          60% { opacity: 0.4; }
          100% { transform: translate(-50%,-50%) scale(4); opacity: 0; }
        }
        @keyframes fadeUp {
          0% { opacity: 0; transform: translateY(20px); }
          100% { opacity: 1; transform: translateY(0); }
        }
        @keyframes streakLine {
          0% { transform: scaleY(0); opacity: 0; }
          20% { opacity: 0.4; }
          100% { transform: scaleY(1); opacity: 0; }
        }
      `}</style>

      {/* Warp stars */}
      {starsRef.current.map((star, i) => (
        <div key={i} style={{
          position: "absolute",
          left: `${star.x}%`, top: `${star.y}%`,
          width: star.s, height: star.s,
          borderRadius: "50%",
          background: `hsl(${star.hue}, 80%, ${star.lightness}%)`,
          animation: phase >= 1 ? `warpStar ${1.5 + star.d}s ${star.d * 0.5}s ease-out forwards` : "none",
          opacity: 0,
        }} />
      ))}

      {/* Speed streaks */}
      {phase >= 1 && streaksRef.current.map((streak, i) => (
        <div key={`s${i}`} style={{
          position: "absolute",
          left: `${streak.left}%`,
          top: "0%",
          width: 1,
          height: "100%",
          background: `linear-gradient(180deg, transparent, rgba(34,211,238,${streak.alpha}), transparent)`,
          transformOrigin: "top center",
          animation: `streakLine ${streak.duration}s ${i * 0.08}s ease-out forwards`,
        }} />
      ))}

      {/* Comet */}
      {phase >= 2 && (
        <div style={{
          position: "absolute", left: "50%", top: "50%",
          marginLeft: -10, marginTop: -10,
          width: 20, height: 20,
          borderRadius: "50%",
          background: "radial-gradient(circle, #FFFFFF 20%, #22D3EE 60%, transparent 100%)",
          boxShadow: "0 0 40px 15px rgba(34,211,238,0.5), 0 0 80px 30px rgba(34,211,238,0.2)",
          animation: "cometFly 1.2s cubic-bezier(0.16,1,0.3,1) forwards",
        }}>
          {/* Comet tail */}
          <div style={{
            position: "absolute", left: "50%", bottom: "100%",
            marginLeft: -3, width: 6, height: 120,
            background: "linear-gradient(180deg, transparent, rgba(34,211,238,0.4), rgba(255,255,255,0.6))",
            borderRadius: 3, filter: "blur(2px)",
          }} />
        </div>
      )}

      {/* Impact burst */}
      {phase >= 4 && (
        <>
          <div style={{
            position: "absolute", left: "50%", top: "50%",
            width: 200, height: 200,
            borderRadius: "50%",
            border: "2px solid rgba(34,211,238,0.5)",
            animation: "impactRing 0.8s ease-out forwards",
          }} />
          <div style={{
            position: "absolute", left: "50%", top: "50%",
            width: 100, height: 100,
            borderRadius: "50%",
            background: "radial-gradient(circle, rgba(255,255,255,0.3), transparent 70%)",
            animation: "impactRing 0.6s 0.1s ease-out forwards",
          }} />
        </>
      )}

      {/* Title text — appears after comet lands */}
      {phase >= 3 && (
        <div style={{
          position: "absolute", inset: 0,
          display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
          zIndex: 10,
        }}>
          <div style={{
            fontSize: 11, textTransform: "uppercase", letterSpacing: 4, color: "#64748B",
            fontFamily: "'Space Grotesk',sans-serif", marginBottom: 12,
            animation: "fadeUp 0.6s 0.1s ease both",
          }}>{deck?.introBrandLine || CURRENT_DECK.introBrandLine}</div>
          <h1 style={{
            fontFamily: "'Space Grotesk',sans-serif", fontSize: 48, fontWeight: 700,
            color: "#F0F4F8", textAlign: "center", margin: "0 0 8px", letterSpacing: -1,
            animation: "fadeUp 0.6s 0.2s ease both",
          }}>{deck?.introTitle || CURRENT_DECK.introTitle}</h1>
          <p style={{
            fontSize: 16, margin: "0 0 28px", textAlign: "center",
            animation: "fadeUp 0.5s 0.4s ease both",
          }}>
            <span style={{ background: "linear-gradient(90deg, #22D3EE, #10B981)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
              {deck?.introSubtitle || CURRENT_DECK.introSubtitle}
            </span>
          </p>
          <div style={{ display: "flex", gap: 32, animation: "fadeUp 0.5s 0.6s ease both" }}>
            {introStats.map((s) => (
              <div key={`${s.lbl}-${s.val}`} style={{ textAlign: "center" }}>
                <div style={{ fontFamily: "'Space Grotesk',sans-serif", fontSize: 24, fontWeight: 700, color: s.color }}>{s.val}</div>
                <div style={{ fontSize: 9, color: "#64748B", textTransform: "uppercase", letterSpacing: 1 }}>{s.lbl}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
ThematicIntro.propTypes = {
  deck: PropTypes.shape({
    introBrandLine: PropTypes.string,
    introTitle: PropTypes.string,
    introSubtitle: PropTypes.string,
    introStats: PropTypes.arrayOf(PropTypes.shape({
      val: PropTypes.string.isRequired,
      lbl: PropTypes.string.isRequired,
      color: PropTypes.string.isRequired,
    })),
  }),
  onComplete: PropTypes.func.isRequired,
};

// ─── THEME SELECTOR (Start Page) ───
function ThemeSelector({ onSelect }) {
  const [hovered, setHovered] = useState(null);
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 50); return () => clearTimeout(t); }, []);

  return (
    <div style={{ minHeight: "100vh", background: "#08101C", display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", padding: "40px 48px" }}>
      <link href={THEME_SELECTOR_FONTS_URL} rel="stylesheet" />

      <div style={{ textAlign: "center", marginBottom: 40, opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(20px)", transition: "all 0.6s ease" }}>
        <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: 4, color: "#64748B", fontFamily: "'Space Grotesk',sans-serif", fontWeight: 500, marginBottom: 12 }}>GenAI Transformation</div>
        <h1 style={{ fontFamily: "'Space Grotesk',sans-serif", fontSize: 40, fontWeight: 700, color: "#F0F4F8", margin: "0 0 10px", letterSpacing: -1 }}>Choose Your Theme</h1>
        <p style={{ fontSize: 14, color: "#94A3B8", margin: 0 }}>Select a visual style for the advocacy deck</p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 16, maxWidth: 900, width: "100%" }}>
        {THEMES.map((t, i) => {
          const isH = hovered === t.id;
          return (
            <div key={t.id}
              onClick={() => onSelect(t)}
              onMouseEnter={() => setHovered(t.id)}
              onMouseLeave={() => setHovered(null)}
              style={{
                cursor: "pointer", borderRadius: 14, overflow: "hidden",
                border: `1px solid ${isH ? t.accent + "60" : "rgba(255,255,255,0.06)"}`,
                boxShadow: isH ? `0 0 30px ${t.accentGlow}` : "0 2px 12px rgba(0,0,0,0.3)",
                transform: isH ? "translateY(-4px) scale(1.02)" : "translateY(0) scale(1)",
                transition: "all 0.3s cubic-bezier(0.34,1.56,0.64,1)",
                opacity: entered ? 1 : 0,
                transitionDelay: `${0.1 + i * 0.06}s`,
              }}>
              {/* Preview header */}
              <div style={{ background: t.bg, padding: "20px 18px 14px", position: "relative" }}>
                {/* Accent bar */}
                <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: 3, background: `linear-gradient(90deg, ${t.gradient[0]}, ${t.gradient[1]})` }} />
                <div style={{ fontFamily: t.fontDisplay, fontSize: 18, fontWeight: 700, color: t.text, marginBottom: 4 }}>{t.name}</div>
                <div style={{ fontSize: 10, color: t.textDim, textTransform: "uppercase", letterSpacing: 1 }}>{t.vibe}</div>
              </div>
              {/* Preview body */}
              <div style={{ background: t.bgCard, padding: "14px 18px 16px" }}>
                {/* Mini card previews */}
                <div style={{ display: "flex", gap: 6, marginBottom: 10 }}>
                  {[t.accent, t.gradient[1], t.textDim].map((c, j) => (
                    <div key={j} style={{ flex: 1, height: 6, borderRadius: 3, background: c, opacity: 0.6 }} />
                  ))}
                </div>
                <div style={{ fontSize: 11, color: t.textMuted, lineHeight: 1.4 }}>
                  <span style={{ color: t.accent, fontWeight: 600 }}>Aa</span> {t.fontDisplay.split(",")[0].replace(/'/g, "")}
                </div>
                {/* Color dots */}
                <div style={{ display: "flex", gap: 5, marginTop: 8 }}>
                  {[t.bg, t.bgCard, t.accent, t.gradient[1]].map((c, j) => (
                    <div key={j} style={{ width: 14, height: 14, borderRadius: "50%", background: c, border: "1px solid rgba(255,255,255,0.1)" }} />
                  ))}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
ThemeSelector.propTypes = { onSelect: PropTypes.func.isRequired };

// ─── BACK BUTTON ───
function BackBtn({ onClick }) {
  const T = useContext(ThemeCtx);
  return <button onClick={onClick} style={{ background:"none",border:"none",color:T.textDim,fontSize:13,cursor:"pointer",fontFamily:T.fontDisplay,marginBottom:20,display:"flex",alignItems:"center",gap:6 }}><span>←</span> Back</button>;
}
BackBtn.propTypes = { onClick: PropTypes.func.isRequired };

function OverviewScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const C = useChrome();
  const [entered, setEntered] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setEntered(true), 50);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <Particles color={topic.color} type="future" active={entered} />
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1180, margin: "0 auto", padding: "36px 48px 48px" }}>
        <BackBtn onClick={onBack} />
        <div style={{ display: "grid", gridTemplateColumns: "1.1fr 0.9fr", gap: 28, alignItems: "start" }}>
          <div style={{ opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(20px)", transition: "all 0.6s ease" }}>
            <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: 3, color: topic.colorLight, fontFamily: T.fontDisplay, marginBottom: 10 }}>{topic.eyebrow || "Overview"}</div>
            <h1 style={{ fontFamily: T.fontDisplay, fontSize: 42, color: T.text, margin: "0 0 10px", lineHeight: 1.05 }}>{topic.title}</h1>
            <p style={{ fontSize: 16, color: topic.colorLight, fontStyle: "italic", lineHeight: 1.5, margin: "0 0 14px" }}>{topic.subtitle}</p>
            {topic.summary && <p style={{ fontSize: 15, color: T.textMuted, lineHeight: 1.7, margin: "0 0 18px", maxWidth: 620 }}>{topic.summary}</p>}
            {topic.heroPoints?.length > 0 && (
              <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 18 }}>
                {topic.heroPoints.map((point) => (
                  <span key={point} style={{ padding: "7px 12px", borderRadius: C.pillRadius, background: `${topic.color}12`, border: `1px solid ${topic.color}26`, fontSize: 12, color: T.text }}>{point}</span>
                ))}
              </div>
            )}
            <div style={{ display: "grid", gap: 12 }}>
              {topic.cards.map((card, index) => (
                <div key={`${card.title}-${index}`} style={{ background: T.bgCard, borderRadius: C.innerRadius, padding: "16px 18px", borderLeft: `${C.accentBarHeight}px solid ${topic.color}`, opacity: entered ? 1 : 0, transform: entered ? "translateX(0)" : "translateX(-14px)", transition: `all 0.45s ${0.18 + index * 0.08}s ease` }}>
                  <div style={{ fontFamily: T.fontDisplay, fontSize: 17, color: T.text, marginBottom: 6 }}>{card.title}</div>
                  <p style={{ fontSize: 13.5, color: T.textMuted, lineHeight: 1.6, margin: 0 }}>{card.body}</p>
                </div>
              ))}
            </div>
          </div>
          <div style={{ opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(20px)", transition: "all 0.6s 0.12s ease" }}>
            <div style={{ background: `linear-gradient(180deg, ${T.bgCard}, ${T.bgDeep})`, borderRadius: C.cardRadius, padding: "22px 22px 18px", border: `${C.cardBorderWidth}px solid ${topic.color}24`, marginBottom: 16 }}>
              <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: 2.2, color: topic.colorLight, fontFamily: T.fontDisplay, marginBottom: 10 }}>Story Notes</div>
              <div style={{ display: "grid", gap: 10 }}>
                {(topic.talkingPoints || []).map((point, index) => (
                  <div key={`${point}-${index}`} style={{ display: "grid", gridTemplateColumns: "26px 1fr", gap: 10, alignItems: "start", paddingTop: index === 0 ? 0 : 10, borderTop: index === 0 ? "none" : `1px solid ${topic.color}14` }}>
                    <div style={{ width: 22, height: 22, borderRadius: "50%", background: `${topic.color}16`, color: topic.colorLight, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 11, fontWeight: 700 }}>{index + 1}</div>
                    <p style={{ fontSize: 13, color: T.textMuted, lineHeight: 1.6, margin: 0 }}>{point}</p>
                  </div>
                ))}
              </div>
            </div>
            <div style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "20px 22px", borderTop: `${C.accentBarHeight}px solid ${topic.color}` }}>
              <div style={{ fontFamily: T.fontDisplay, fontSize: 24, color: T.text, marginBottom: 10 }}>{topic.callout}</div>
              <div style={{ width: 96, height: 3, borderRadius: 999, background: `linear-gradient(90deg, ${topic.color}, ${topic.colorLight})` }} />
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

function ManifestStatCardsScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const C = useChrome();
  const [entered, setEntered] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setEntered(true), 50);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <Particles color={topic.color} type="human" active={entered} />
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1260, margin: "0 auto", padding: "36px 48px 48px" }}>
        <BackBtn onClick={onBack} />
        <div style={{ display: "grid", gridTemplateColumns: "1.15fr 0.85fr", gap: 24, marginBottom: 18 }}>
          <div style={{ opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(22px)", transition: "all 0.6s ease" }}>
            <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: 3, color: topic.colorLight, fontFamily: T.fontDisplay, marginBottom: 8 }}>{topic.kicker || topic.eyebrow || "Governance"}</div>
            <h1 style={{ fontFamily: T.fontDisplay, fontSize: 42, color: T.text, margin: "0 0 10px", lineHeight: 1.06 }}>{topic.heroTitle || topic.title}</h1>
            <p style={{ fontSize: 16, color: topic.colorLight, fontStyle: "italic", margin: "0 0 12px", lineHeight: 1.5 }}>{topic.subtitle}</p>
            {topic.thesis && <p style={{ fontSize: 15, color: T.textMuted, lineHeight: 1.7, margin: 0 }}>{topic.thesis}</p>}
          </div>
          <div style={{ background: `linear-gradient(180deg, ${T.bgCard}, ${T.bgDeep})`, borderRadius: C.cardRadius, padding: "18px 20px", border: `${C.cardBorderWidth}px solid ${topic.color}24`, opacity: entered ? 1 : 0, transition: "opacity 0.6s 0.1s ease" }}>
            <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: 2.5, color: topic.colorLight, fontFamily: T.fontDisplay, marginBottom: 8 }}>Leadership Points</div>
            <div style={{ display: "grid", gap: 10 }}>
              {(topic.leadershipPoints || []).map((point, index) => (
                <div key={`${point}-${index}`} style={{ display: "grid", gridTemplateColumns: "24px 1fr", gap: 10, alignItems: "start" }}>
                  <div style={{ width: 22, height: 22, borderRadius: "50%", background: `${topic.color}18`, color: topic.colorLight, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 11, fontWeight: 700 }}>{index + 1}</div>
                  <p style={{ fontSize: 13, color: T.textMuted, lineHeight: 1.55, margin: 0 }}>{point}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, minmax(0, 1fr))", gap: 14, marginBottom: 18 }}>
          {topic.cards.map((card, index) => (
            <div key={`${card.title}-${index}`} style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "18px 20px", borderTop: `${C.accentBarHeight}px solid ${topic.color}`, opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(18px)", transition: `all 0.45s ${0.12 + index * 0.08}s ease` }}>
              <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: 2.2, color: topic.colorLight, fontFamily: T.fontDisplay, marginBottom: 8 }}>{card.step || card.marker || `0${index + 1}`}</div>
              <h3 style={{ fontFamily: T.fontDisplay, fontSize: 21, color: T.text, margin: "0 0 8px", lineHeight: 1.15 }}>{card.title}</h3>
              {(card.eyebrow || card.statLabel) && <div style={{ fontSize: 11, color: T.textDim, textTransform: "uppercase", letterSpacing: 1.6, marginBottom: 8 }}>{card.eyebrow || card.statLabel}</div>}
              {card.highlight && <p style={{ fontSize: 14, color: T.text, lineHeight: 1.6, margin: "0 0 10px", fontWeight: 600 }}>{card.highlight}</p>}
              {card.body && <p style={{ fontSize: 13.5, color: T.textMuted, lineHeight: 1.6, margin: card.highlight ? "0" : "0 0 10px" }}>{card.body}</p>}
              {Array.isArray(card.details) && card.details.length > 0 && (
                <div style={{ display: "grid", gap: 8, marginTop: 10 }}>
                  {card.details.map((detail, detailIndex) => (
                    <div key={`${detail}-${detailIndex}`} style={{ paddingTop: 8, borderTop: `1px solid ${topic.color}14`, fontSize: 13, color: T.textMuted, lineHeight: 1.55 }}>{detail}</div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>

        {topic.results?.length > 0 && (
          <div style={{ display: "grid", gridTemplateColumns: `repeat(${topic.results.length}, minmax(0, 1fr))`, gap: 12, marginBottom: 18 }}>
            {topic.results.map((result, index) => (
              <div key={`${result.label}-${index}`} style={{ background: `linear-gradient(180deg, ${T.bgCard}, ${T.bgDeep})`, borderRadius: C.innerRadius, padding: "16px 18px", border: `${C.cardBorderWidth}px solid ${topic.color}18` }}>
                <div style={{ fontFamily: T.fontDisplay, fontSize: 30, color: topic.colorLight, marginBottom: 4 }}>{result.value}</div>
                <div style={{ fontSize: 11, color: T.textDim, textTransform: "uppercase", letterSpacing: 1.5, marginBottom: result.detail ? 8 : 0 }}>{result.label}</div>
                {result.detail && <p style={{ fontSize: 12.5, color: T.textMuted, lineHeight: 1.5, margin: 0 }}>{result.detail}</p>}
              </div>
            ))}
          </div>
        )}

        <div style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "18px 20px", borderLeft: `${C.accentBarHeight + 1}px solid ${topic.color}` }}>
          {topic.enablement && <p style={{ fontSize: 14, color: T.textMuted, lineHeight: 1.65, margin: "0 0 10px" }}>{topic.enablementTitle ? <strong style={{ color: topic.colorLight }}>{topic.enablementTitle}: </strong> : null}{topic.enablement}</p>}
          <p style={{ fontFamily: T.fontDisplay, fontSize: 24, color: T.text, margin: 0 }}>{topic.callout}</p>
        </div>
      </div>
    </div>
  );
}
ManifestStatCardsScreen.propTypes = {
  topic: topicPropType.isRequired,
  onBack: PropTypes.func.isRequired,
};

function PlatformScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const C = useChrome();
  const [entered, setEntered] = useState(false);
  const [activePanel, setActivePanel] = useState(0);

  useEffect(() => {
    const timer = setTimeout(() => setEntered(true), 50);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <Particles color={topic.color} type="future" active={entered} />
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1240, margin: "0 auto", padding: "36px 48px 48px" }}>
        <BackBtn onClick={onBack} />
        <div style={{ display: "grid", gridTemplateColumns: "1.05fr 0.95fr", gap: 24, marginBottom: 18 }}>
          <div style={{ opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(20px)", transition: "all 0.6s ease" }}>
            <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: 3, color: topic.colorLight, fontFamily: T.fontDisplay, marginBottom: 8 }}>{topic.eyebrow || "Service Platform"}</div>
            <h1 style={{ fontFamily: T.fontDisplay, fontSize: 42, color: T.text, margin: "0 0 10px", lineHeight: 1.06 }}>{topic.title}</h1>
            <p style={{ fontSize: 16, color: topic.colorLight, fontStyle: "italic", lineHeight: 1.5, margin: "0 0 14px" }}>{topic.subtitle}</p>
            {topic.summary && <p style={{ fontSize: 15, color: T.textMuted, lineHeight: 1.7, margin: "0 0 18px" }}>{topic.summary}</p>}
            <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 18 }}>
              {topic.heroPoints.map((point) => (
                <span key={point} style={{ padding: "7px 12px", borderRadius: C.pillRadius, background: `${topic.color}12`, border: `1px solid ${topic.color}24`, fontSize: 12, color: T.text }}>{point}</span>
              ))}
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(2, minmax(0, 1fr))", gap: 12 }}>
              {topic.capabilities.map((capability, index) => (
                <div key={`${capability.title}-${index}`} style={{ background: T.bgCard, borderRadius: C.innerRadius, padding: "14px 16px", borderLeft: `${C.accentBarHeight}px solid ${topic.color}`, opacity: entered ? 1 : 0, transform: entered ? "translateX(0)" : "translateX(-14px)", transition: `all 0.45s ${0.18 + index * 0.08}s ease` }}>
                  <div style={{ fontFamily: T.fontDisplay, fontSize: 17, color: T.text, marginBottom: 6 }}>{capability.title}</div>
                  <p style={{ fontSize: 13.5, color: T.textMuted, lineHeight: 1.6, margin: 0 }}>{capability.body}</p>
                </div>
              ))}
            </div>
          </div>
          <div style={{ opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(20px)", transition: "all 0.6s 0.12s ease" }}>
            <div style={{ display: "flex", gap: 8, marginBottom: 12, flexWrap: "wrap" }}>
              {topic.focusPanels.map((panel, index) => (
                <button key={`${panel.label}-${index}`} onClick={() => setActivePanel(index)} style={{ border: `1px solid ${index === activePanel ? topic.color : `${topic.color}20`}`, background: index === activePanel ? `${topic.color}18` : T.bgCard, color: index === activePanel ? topic.colorLight : T.textDim, borderRadius: C.pillRadius, padding: "7px 12px", fontSize: 12, cursor: "pointer", fontFamily: T.fontBody }}>{panel.label}</button>
              ))}
            </div>
            <div style={{ background: `linear-gradient(180deg, ${T.bgCard}, ${T.bgDeep})`, borderRadius: C.cardRadius, padding: "18px 20px", border: `${C.cardBorderWidth}px solid ${topic.color}24`, marginBottom: 14 }}>
              <div style={{ fontFamily: T.fontDisplay, fontSize: 24, color: T.text, marginBottom: 8 }}>{topic.focusPanels[activePanel]?.title}</div>
              <p style={{ fontSize: 14, color: T.textMuted, lineHeight: 1.65, margin: 0 }}>{topic.focusPanels[activePanel]?.body}</p>
            </div>
            <div style={{ display: "grid", gap: 12 }}>
              {topic.lanes.map((lane, index) => (
                <div key={`${lane.title}-${index}`} style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "16px 18px", borderTop: `${C.accentBarHeight}px solid ${lane.accent || topic.color}` }}>
                  <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: 2.5, color: lane.accent || topic.colorLight, fontFamily: T.fontDisplay, marginBottom: 6 }}>{lane.title}</div>
                  <div style={{ fontFamily: T.fontDisplay, fontSize: 20, color: T.text, marginBottom: 6 }}>{lane.subtitle}</div>
                  <p style={{ fontSize: 12.5, color: T.textDim, margin: "0 0 12px" }}>{lane.persona}</p>
                  <div style={{ display: "grid", gap: 8 }}>
                    {lane.steps.map((step, stepIndex) => (
                      <div key={`${step}-${stepIndex}`} style={{ display: "grid", gridTemplateColumns: "24px 1fr", gap: 10, alignItems: "start" }}>
                        <div style={{ width: 22, height: 22, borderRadius: "50%", background: `${lane.accent || topic.color}18`, color: lane.accent || topic.colorLight, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 11, fontWeight: 700 }}>{stepIndex + 1}</div>
                        <p style={{ fontSize: 13, color: T.textMuted, lineHeight: 1.55, margin: 0 }}>{step}</p>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
        {topic.talkingPoints?.length > 0 && (
          <div style={{ background: T.bgCard, borderRadius: 14, padding: "16px 18px", borderLeft: `4px solid ${topic.color}`, marginBottom: 14 }}>
            <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: 2.5, color: topic.colorLight, fontFamily: T.fontDisplay, marginBottom: 8 }}>Talking Points</div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(2, minmax(0, 1fr))", gap: 10 }}>
              {topic.talkingPoints.map((point, index) => (
                <div key={`${point}-${index}`} style={{ fontSize: 13, color: T.textMuted, lineHeight: 1.6 }}>{point}</div>
              ))}
            </div>
          </div>
        )}
        <div style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "18px 20px", borderLeft: `${C.accentBarHeight + 1}px solid ${topic.color}` }}>
          <p style={{ fontFamily: T.fontDisplay, fontSize: 24, color: T.text, margin: 0 }}>{topic.callout}</p>
        </div>
      </div>
    </div>
  );
}
PlatformScreen.propTypes = {
  topic: topicPropType.isRequired,
  onBack: PropTypes.func.isRequired,
};

// ─── HUMAN SCREEN ───
function HumanScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const C = useChrome();
  const [e,setE]=useState(false); useEffect(()=>{const t=setTimeout(()=>setE(true),50);return()=>clearTimeout(t)},[]);
  return (
    <div style={{ position:"relative",minHeight:"100vh",background:T.bg,overflow:"hidden" }}>
      <Particles color={topic.color} type="human" active={e}/>
      <div style={{ position:"relative",zIndex:2,maxWidth:900,margin:"0 auto",padding:"48px 32px",opacity:e?1:0,transform:e?"translateY(0)":"translateY(30px)",transition:"all 0.8s cubic-bezier(0.22,1,0.36,1)" }}>
        <BackBtn onClick={onBack}/>
        <div style={{ textAlign:"center",marginBottom:48 }}>
          <div style={{ width:64,height:64,borderRadius:"50%",background:topic.color+"18",border:`2px solid ${topic.color}40`,display:"flex",alignItems:"center",justifyContent:"center",fontSize:28,margin:"0 auto 20px",boxShadow:`0 0 40px ${topic.colorGlow}` }}>{topic.icon}</div>
          <h1 style={{ fontFamily:T.fontDisplay,fontSize:44,fontWeight:C.headingWeight,color:T.text,margin:"0 0 8px",textTransform:C.headingTransform }}>{topic.title}</h1>
          <p style={{ fontSize:16,color:topic.colorLight,fontStyle:"italic",margin:0 }}>{topic.subtitle}</p>
          <div style={{ width:80,height:C.accentBarHeight,background:topic.color,margin:"20px auto 0",borderRadius:2 }}/>
        </div>
        {topic.cards.map((c,i)=>(<div key={i} style={{ background:T.bgCard,borderRadius:C.innerRadius,padding:"28px 32px",marginBottom:20,display:"flex",alignItems:"flex-start",gap:24,borderLeft:`${C.accentBarHeight+1}px solid ${topic.color}`,opacity:e?1:0,transform:e?"translateY(0)":"translateY(20px)",transition:`all 0.6s ${0.3+i*0.15}s cubic-bezier(0.22,1,0.36,1)` }}>
          <div style={{ flexShrink:0,textAlign:"center",minWidth:72 }}><div style={{ fontFamily:T.fontDisplay,fontSize:32,fontWeight:C.headingWeight,color:topic.colorLight }}>{c.stat}</div><div style={{ fontSize:10,color:T.textDim,textTransform:"uppercase",letterSpacing:1,marginTop:2 }}>{c.statLabel}</div></div>
          <div><h3 style={{ fontFamily:T.fontDisplay,fontSize:18,fontWeight:C.headingWeight,color:topic.colorLight,margin:"0 0 8px" }}>{c.title}</h3><p style={{ fontSize:14,color:T.textMuted,lineHeight:1.6,margin:0 }}>{c.body}</p></div>
        </div>))}
        <div style={{ textAlign:"center",marginTop:32,padding:"24px",borderTop:`1px solid ${topic.color}20`,borderBottom:`1px solid ${topic.color}20`,opacity:e?1:0,transition:"opacity 1s 0.9s" }}>
          <p style={{ fontSize:16,color:T.textMuted,lineHeight:1.6,margin:0,maxWidth:600,marginLeft:"auto",marginRight:"auto" }}><span style={{ color:topic.colorLight,fontWeight:700 }}>&ldquo;{topic.callout}&rdquo;</span></p>
        </div>
      </div>
    </div>
  );
}
HumanScreen.propTypes = {
  topic: topicPropType.isRequired,
  onBack: PropTypes.func.isRequired,
};

// ─── HURDLES SCREEN ───
function HurdlesScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const C = useChrome();
  const [e,setE]=useState(false);const [vc,setVc]=useState(0);
  useEffect(()=>{const t=setTimeout(()=>setE(true),50);return()=>clearTimeout(t)},[]);
  useEffect(() => {
    if (!e) {
      return undefined;
    }

    const iv = topic.cards.map((_, i) => setTimeout(() => setVc(i + 1), 400 + i * 250));
    return () => iv.forEach(clearTimeout);
  }, [e, topic.cards]);
  return (
    <div style={{ position:"relative",minHeight:"100vh",background:T.bg,overflow:"hidden" }}>
      <Particles color={topic.color} type="hurdles" active={e}/>
      <div style={{ position:"absolute",inset:0,pointerEvents:"none",overflow:"hidden" }}>{[...Array(8)].map((_,i)=>(<div key={i} style={{ position:"absolute",left:"-10%",top:`${10+i*11}%`,width:e?"120%":"0%",height:1,background:`linear-gradient(90deg,transparent,${topic.color}15,transparent)`,transition:`width ${0.6+i*0.1}s ${0.2+i*0.05}s cubic-bezier(0.16,1,0.3,1)` }}/>))}</div>
      <div style={{ position:"relative",zIndex:2,padding:"36px 48px" }}>
        <BackBtn onClick={onBack}/>
        <div style={{ marginBottom:32,transform:e?"translateX(0)":"translateX(-100px)",opacity:e?1:0,transition:"all 0.5s cubic-bezier(0.16,1,0.3,1)" }}>
          <div style={{ display:"flex",alignItems:"center",gap:16,marginBottom:6 }}><div style={{ fontSize:36,transform:e?"rotate(0deg)":"rotate(-90deg)",transition:"transform 0.6s 0.2s cubic-bezier(0.34,1.56,0.64,1)" }}>{topic.icon}</div><h1 style={{ fontFamily:T.fontDisplay,fontSize:42,fontWeight:C.headingWeight,color:T.text,margin:0,letterSpacing:-1,textTransform:C.headingTransform }}>{topic.title}</h1></div>
          <p style={{ fontSize:15,color:topic.colorLight,fontStyle:"italic",margin:0,paddingLeft:52 }}>{topic.subtitle}</p>
        </div>
        <div style={{ display:"grid",gridTemplateColumns:"1fr 1fr",gap:20,maxWidth:1100 }}>
          {topic.cards.map((c,i)=>{const v=i<vc,fl=i%2===0;const hiddenTransform=`translateX(${fl ? "-60px" : "60px"}) scale(0.92)`;return(
            <div key={i} style={{ background:T.bgCard,borderRadius:C.innerRadius,padding:"24px 28px",borderTop:`${C.accentBarHeight}px solid ${topic.color}`,position:"relative",overflow:"hidden",opacity:v?1:0,transform:v?"translateX(0) scale(1)":hiddenTransform,transition:"all 0.45s cubic-bezier(0.34,1.56,0.64,1)" }}>
              <div style={{ position:"absolute",inset:0,background:`radial-gradient(circle at ${fl?"left":"right"} center,${topic.color}15,transparent 60%)`,opacity:v?1:0,transition:"opacity 0.3s" }}/>
              <div style={{ position:"relative",zIndex:1 }}>
                <div style={{ display:"flex",alignItems:"center",gap:10,marginBottom:14 }}><div style={{ width:28,height:28,borderRadius:C.tagRadius,background:topic.color+"20",display:"flex",alignItems:"center",justifyContent:"center",fontFamily:T.fontDisplay,fontWeight:700,fontSize:13,color:topic.color }}>{i+1}</div><h3 style={{ fontFamily:T.fontDisplay,fontSize:17,fontWeight:C.headingWeight,color:T.text,margin:0 }}>{c.title}</h3></div>
                <div style={{ marginBottom:12 }}><div style={{ fontSize:10,textTransform:"uppercase",letterSpacing:1.2,fontWeight:700,color:T.danger,marginBottom:4 }}>Challenge</div><p style={{ fontSize:13,color:T.textDim,lineHeight:1.5,margin:0 }}>{c.challenge}</p></div>
                <div><div style={{ fontSize:10,textTransform:"uppercase",letterSpacing:1.2,fontWeight:700,color:T.success,marginBottom:4 }}>Solution</div><p style={{ fontSize:13,color:T.textMuted,lineHeight:1.5,margin:0 }}>{c.fix}</p></div>
              </div>
            </div>);})}
        </div>
        <div style={{ marginTop:28,background:T.bgCard,borderRadius:C.innerRadius,padding:"16px 28px",borderLeft:`${C.accentBarHeight+1}px solid ${topic.color}`,display:"flex",alignItems:"center",gap:16,transform:e?"translateX(0)":"translateX(200px)",opacity:e?1:0,transition:"all 0.6s 1.3s cubic-bezier(0.16,1,0.3,1)" }}>
          <div style={{ fontSize:24,color:topic.color }}>⚡</div><p style={{ fontSize:14,color:T.textMuted,lineHeight:1.6,margin:0 }}><strong style={{ color:topic.colorLight }}>{topic.callout}</strong></p>
        </div>
      </div>
    </div>
  );
}
HurdlesScreen.propTypes = {
  topic: topicPropType.isRequired,
  onBack: PropTypes.func.isRequired,
};

// ─── FUTURE SCREEN ───
function FutureScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const C = useChrome();
  const [e,setE]=useState(false); useEffect(()=>{const t=setTimeout(()=>setE(true),50);return()=>clearTimeout(t)},[]);
  return (
    <div style={{ position:"relative",minHeight:"100vh",background:T.bg,overflow:"hidden" }}>
      <Particles color={topic.color} type="future" active={e}/>
      <div style={{ position:"absolute",top:"42%",left:"50%",width:e?"140%":"0%",height:1,background:`linear-gradient(90deg,transparent,${topic.color}30,transparent)`,transform:"translateX(-50%)",transition:"width 1.2s cubic-bezier(0.22,1,0.36,1)" }}/>
      <div style={{ position:"relative",zIndex:2,padding:"36px 48px" }}>
        <BackBtn onClick={onBack}/>
        <div style={{ textAlign:"center",marginBottom:40,opacity:e?1:0,transform:e?"translateY(0) scale(1)":"translateY(40px) scale(0.95)",transition:"all 0.7s cubic-bezier(0.22,1,0.36,1)" }}>
          <div style={{ fontSize:36,marginBottom:12,filter:`drop-shadow(0 0 16px ${topic.colorGlow})` }}>{topic.icon}</div>
          <h1 style={{ fontFamily:T.fontDisplay,fontSize:44,fontWeight:C.headingWeight,color:T.text,margin:"0 0 8px",textTransform:C.headingTransform }}>{topic.title}</h1>
          <p style={{ fontSize:16,color:topic.colorLight,fontStyle:"italic",margin:0 }}>{topic.subtitle}</p>
        </div>
        <div style={{ display:"grid",gridTemplateColumns:"1fr 1fr",gap:20,maxWidth:1000,margin:"0 auto" }}>
          {topic.cards.map((c,i)=>(<div key={i} style={{ background:T.bgCard,borderRadius:C.innerRadius,padding:"28px 28px 22px",borderLeft:`${C.accentBarHeight+1}px solid ${topic.color}`,opacity:e?1:0,transform:e?"scale(1)":"scale(0.8)",transition:`all 0.5s ${0.3+i*0.12}s cubic-bezier(0.22,1,0.36,1)` }}><h3 style={{ fontFamily:T.fontDisplay,fontSize:17,fontWeight:C.headingWeight,color:topic.colorLight,margin:"0 0 10px" }}>{c.title}</h3><p style={{ fontSize:13.5,color:T.textMuted,lineHeight:1.6,margin:0 }}>{c.body}</p></div>))}
        </div>
        <div style={{ textAlign:"center",marginTop:36,maxWidth:700,marginLeft:"auto",marginRight:"auto",opacity:e?1:0,transition:"opacity 0.8s 1s" }}><p style={{ fontSize:15,color:T.textMuted,lineHeight:1.6,margin:0 }}><strong style={{ color:topic.colorLight }}>{topic.callout}</strong></p></div>
      </div>
    </div>
  );
}
FutureScreen.propTypes = {
  topic: topicPropType.isRequired,
  onBack: PropTypes.func.isRequired,
};

// ═══════════════════════════════════════════
// VERGE-STYLE LAYOUTS
// ═══════════════════════════════════════════

// ─── STAT HERO SCREEN ───
function StatHeroScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const C = useChrome();
  const [e, setE] = useState(false);
  useEffect(() => { const t = setTimeout(() => setE(true), 50); return () => clearTimeout(t); }, []);

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1180, margin: "0 auto", padding: "48px" }}>
        <BackBtn onClick={onBack} />
        {topic.question && (
          <div style={{ float: "right", maxWidth: 320, background: T.text, borderRadius: C.cardRadius, padding: "14px 18px", marginLeft: 24, marginBottom: 16 }}>
            <span style={{ fontFamily: T.fontDisplay, fontSize: 20, fontWeight: 700, color: T.bg }}>Q: </span>
            <span style={{ fontFamily: T.fontBody, fontSize: 13, color: T.bg, lineHeight: 1.5 }}>{topic.question}</span>
          </div>
        )}
        <h1 style={{ fontFamily: T.fontDisplay, fontSize: 48, fontWeight: C.headingWeight, color: T.text, margin: "0 0 16px", lineHeight: 1.1, maxWidth: 680, opacity: e ? 1 : 0, transform: e ? "translateY(0)" : "translateY(20px)", transition: "all 0.6s ease" }}>
          {topic.title}
        </h1>
        {topic.subtitle && <p style={{ fontSize: 15, color: T.textMuted, margin: "0 0 32px", maxWidth: 600, lineHeight: 1.6 }}>{topic.subtitle}</p>}
        <div style={{ display: "flex", gap: 20, flexWrap: "wrap", marginBottom: 32, clear: "both" }}>
          {(topic.statItems || []).map((item, idx) => (
            <div key={idx} style={{
              background: item.bgColor || topic.color,
              borderRadius: C.cardRadius, padding: "24px 28px",
              flex: 1, minWidth: 200, maxWidth: 340,
              border: `${C.cardBorderWidth}px solid rgba(0,0,0,0.15)`,
              opacity: e ? 1 : 0, transform: e ? "translateY(0)" : "translateY(24px)",
              transition: `all 0.5s ${0.15 + idx * 0.1}s ease`,
            }}>
              <div style={{ fontFamily: T.fontDisplay, fontSize: 11, fontWeight: 700, letterSpacing: 3, textTransform: "uppercase", color: "#000", marginBottom: 6 }}>{item.label}</div>
              <div style={{ fontFamily: T.fontDisplay, fontSize: 56, fontWeight: 700, color: "#000", lineHeight: 1, marginBottom: 12 }}>{item.val}</div>
              {item.bullets && (
                <ul style={{ margin: 0, padding: "0 0 0 16px", fontSize: 12, color: "#000", lineHeight: 1.7 }}>
                  {item.bullets.map((b, bi) => <li key={bi} style={{ marginBottom: 2 }}>{b}</li>)}
                </ul>
              )}
            </div>
          ))}
        </div>
        <div style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "20px 24px", borderLeft: `${C.accentBarHeight}px solid ${topic.color}`, maxWidth: 700 }}>
          <p style={{ fontFamily: T.fontDisplay, fontSize: 18, color: T.text, margin: 0, fontWeight: 600 }}>{topic.callout}</p>
        </div>
      </div>
    </div>
  );
}
StatHeroScreen.propTypes = { topic: topicPropType.isRequired, onBack: PropTypes.func.isRequired };

// ─── QUOTE COLLAGE SCREEN ───
function QuoteCollageScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const C = useChrome();
  const [e, setE] = useState(false);
  useEffect(() => { const t = setTimeout(() => setE(true), 50); return () => clearTimeout(t); }, []);

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1180, margin: "0 auto", padding: "48px" }}>
        <BackBtn onClick={onBack} />
        <h1 style={{ fontFamily: T.fontDisplay, fontSize: 48, fontWeight: C.headingWeight, color: T.text, margin: "0 0 12px", lineHeight: 1.1 }}>
          {topic.title}
        </h1>
        {topic.subtitle && <p style={{ fontSize: 14, color: T.textMuted, margin: "0 0 28px", maxWidth: 600, lineHeight: 1.6 }}>{topic.subtitle}</p>}
        <div style={{ display: "flex", flexWrap: "wrap", gap: 14, marginBottom: 20, justifyContent: "center" }}>
          {(topic.quotes || []).map((q, idx) => (
            <div key={idx} style={{
              position: "relative", background: q.bgColor || topic.color,
              borderRadius: C.cardRadius + 4, padding: "14px 18px",
              maxWidth: 260, minWidth: 160, flex: "0 1 auto",
              border: `${C.cardBorderWidth}px solid rgba(0,0,0,0.12)`,
              opacity: e ? 1 : 0, transform: e ? "scale(1)" : "scale(0.85)",
              transition: `all 0.4s ${0.05 + idx * 0.05}s cubic-bezier(0.34,1.56,0.64,1)`,
            }}>
              <p style={{ fontFamily: T.fontBody, fontSize: 13, color: "#000", lineHeight: 1.5, margin: 0, fontWeight: 500 }}>
                &ldquo;{q.text}&rdquo;
              </p>
              <div style={{
                position: "absolute", bottom: -8, left: 20 + (idx % 3) * 20,
                width: 0, height: 0,
                borderLeft: "8px solid transparent", borderRight: "8px solid transparent",
                borderTop: `8px solid ${q.bgColor || topic.color}`,
              }} />
            </div>
          ))}
        </div>
        {topic.centerLabel && (
          <div style={{ textAlign: "center", margin: "20px 0 24px" }}>
            <span style={{ fontFamily: T.fontDisplay, fontSize: 13, fontWeight: 700, color: T.text, letterSpacing: 3, textTransform: "uppercase", background: T.bgCard, padding: "10px 20px", borderRadius: C.cardRadius, border: `${C.cardBorderWidth}px solid ${T.text}` }}>
              {topic.centerLabel}
            </span>
          </div>
        )}
        <div style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "18px 22px", borderLeft: `${C.accentBarHeight}px solid ${topic.color}`, maxWidth: 700 }}>
          <p style={{ fontFamily: T.fontDisplay, fontSize: 18, color: T.text, margin: 0, fontWeight: 600 }}>{topic.callout}</p>
        </div>
      </div>
    </div>
  );
}
QuoteCollageScreen.propTypes = { topic: topicPropType.isRequired, onBack: PropTypes.func.isRequired };

// ─── BADGE GRID SCREEN ───
function BadgeGridScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const C = useChrome();
  const [e, setE] = useState(false);
  useEffect(() => { const t = setTimeout(() => setE(true), 50); return () => clearTimeout(t); }, []);

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1180, margin: "0 auto", padding: "48px" }}>
        <BackBtn onClick={onBack} />
        <h1 style={{ fontFamily: T.fontDisplay, fontSize: 42, fontWeight: C.headingWeight, color: T.text, margin: "0 0 16px", lineHeight: 1.1 }}>
          {topic.title}
        </h1>
        {topic.question && (
          <div style={{ display: "inline-flex", alignItems: "center", gap: 8, background: T.text, borderRadius: C.cardRadius, padding: "10px 16px", marginBottom: 24 }}>
            <span style={{ fontFamily: T.fontDisplay, fontSize: 16, fontWeight: 700, color: T.bg }}>Q:</span>
            <span style={{ fontFamily: T.fontBody, fontSize: 13, color: T.bg }}>{topic.question}</span>
          </div>
        )}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: 10, marginBottom: 24 }}>
          {(topic.badges || []).map((badge, idx) => {
            const dark = badge.bgColor === "#000000";
            return (
              <div key={idx} style={{
                display: "flex", alignItems: "center", gap: 8,
                background: badge.bgColor || topic.color,
                borderRadius: C.pillRadius > 20 ? 12 : C.pillRadius, padding: "10px 14px",
                border: `${C.cardBorderWidth}px solid rgba(0,0,0,0.1)`,
                opacity: e ? 1 : 0, transform: e ? "translateY(0)" : "translateY(12px)",
                transition: `all 0.35s ${0.02 + idx * 0.025}s ease`,
              }}>
                <span style={{ fontSize: 18 }}>{badge.icon}</span>
                <span style={{ fontFamily: T.fontDisplay, fontSize: 10, fontWeight: 700, color: dark ? "#FFF" : "#000", letterSpacing: 1, textTransform: "uppercase", flex: 1 }}>{badge.name}</span>
                <span style={{ fontFamily: T.fontDisplay, fontSize: 14, fontWeight: 700, color: dark ? "#FFF" : "#000" }}>{badge.value}</span>
              </div>
            );
          })}
        </div>
        <div style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "18px 22px", borderLeft: `${C.accentBarHeight}px solid ${topic.color}`, maxWidth: 700 }}>
          <p style={{ fontFamily: T.fontDisplay, fontSize: 18, color: T.text, margin: 0, fontWeight: 600 }}>{topic.callout}</p>
        </div>
      </div>
    </div>
  );
}
BadgeGridScreen.propTypes = { topic: topicPropType.isRequired, onBack: PropTypes.func.isRequired };

// ─── DATA TABLE SCREEN ───
function DataTableScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const C = useChrome();
  const [e, setE] = useState(false);
  useEffect(() => { const t = setTimeout(() => setE(true), 50); return () => clearTimeout(t); }, []);

  const headers = topic.tableHeaders || [];
  const colors = topic.headerColors || [];
  const rows = topic.tableRows || [];

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1080, margin: "0 auto", padding: "48px" }}>
        <BackBtn onClick={onBack} />
        <h1 style={{ fontFamily: T.fontDisplay, fontSize: 42, fontWeight: C.headingWeight, color: T.text, margin: "0 0 28px", lineHeight: 1.1 }}>
          {topic.title}
        </h1>
        <div style={{ background: T.bgCard, borderRadius: C.cardRadius, overflow: "hidden", border: `${C.cardBorderWidth}px solid rgba(0,0,0,0.1)`, marginBottom: 24, opacity: e ? 1 : 0, transition: "opacity 0.6s 0.1s ease" }}>
          {topic.tableTitle && (
            <div style={{ background: T.success || "#00CC66", padding: "12px 20px" }}>
              <span style={{ fontFamily: T.fontDisplay, fontSize: 15, fontWeight: 700, color: "#000", textTransform: "uppercase", letterSpacing: 2 }}>{topic.tableTitle}</span>
            </div>
          )}
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                {headers.map((h, i) => (
                  <th key={i} style={{
                    fontFamily: T.fontDisplay, fontSize: 12, fontWeight: 700,
                    padding: "12px 14px", textAlign: i === 0 ? "left" : "center",
                    color: colors[i] === "transparent" || !colors[i] ? "#000" : "#000",
                    background: colors[i] || "transparent",
                    letterSpacing: 1, textTransform: "uppercase",
                  }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((row, ri) => (
                <tr key={ri} style={{ borderTop: "1px solid rgba(0,0,0,0.08)" }}>
                  {row.map((cell, ci) => (
                    <td key={ci} style={{
                      fontFamily: ci === 0 ? T.fontBody : T.fontDisplay,
                      fontSize: ci === 0 ? 13 : 15, padding: "12px 14px",
                      textAlign: ci === 0 ? "left" : "center",
                      color: "#000", fontWeight: ci === 0 ? 400 : 700,
                    }}>{cell}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "18px 22px", borderLeft: `${C.accentBarHeight}px solid ${topic.color}`, maxWidth: 700 }}>
          <p style={{ fontFamily: T.fontDisplay, fontSize: 18, color: T.text, margin: 0, fontWeight: 600 }}>{topic.callout}</p>
        </div>
      </div>
    </div>
  );
}
DataTableScreen.propTypes = { topic: topicPropType.isRequired, onBack: PropTypes.func.isRequired };

// ─── BAR CHART SCREEN ───
function BarChartScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const C = useChrome();
  const [e, setE] = useState(false);
  useEffect(() => { const t = setTimeout(() => setE(true), 50); return () => clearTimeout(t); }, []);

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1180, margin: "0 auto", padding: "48px" }}>
        <BackBtn onClick={onBack} />
        <h1 style={{ fontFamily: T.fontDisplay, fontSize: 42, fontWeight: C.headingWeight, color: T.text, margin: "0 0 28px", lineHeight: 1.1 }}>
          {topic.title}
        </h1>
        <div style={{ display: "grid", gridTemplateColumns: `repeat(${Math.min((topic.barGroups || []).length, 2)}, 1fr)`, gap: 24, marginBottom: 24 }}>
          {(topic.barGroups || []).map((group, gi) => (
            <div key={gi} style={{
              background: T.bgCard, borderRadius: C.cardRadius, padding: "20px 24px",
              border: `${C.cardBorderWidth}px solid rgba(0,0,0,0.1)`,
              opacity: e ? 1 : 0, transform: e ? "translateX(0)" : "translateX(-20px)",
              transition: `all 0.5s ${0.1 + gi * 0.15}s ease`,
            }}>
              <div style={{ fontFamily: T.fontDisplay, fontSize: 13, fontWeight: 700, letterSpacing: 3, textTransform: "uppercase", color: group.color || topic.color, marginBottom: 16, borderBottom: `${C.accentBarHeight}px solid ${group.color || topic.color}`, paddingBottom: 10 }}>
                {group.groupLabel}
              </div>
              <div style={{ display: "grid", gap: 10 }}>
                {(group.bars || []).map((bar, bi) => (
                  <div key={bi}>
                    <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                      <span style={{ fontFamily: T.fontBody, fontSize: 12, color: T.text }}>{bar.label}</span>
                      <span style={{ fontFamily: T.fontDisplay, fontSize: 12, fontWeight: 700, color: T.text }}>{bar.value}%</span>
                    </div>
                    <div style={{ height: 20, background: "rgba(0,0,0,0.06)", borderRadius: C.innerRadius, overflow: "hidden" }}>
                      <div style={{
                        height: "100%", width: e ? `${bar.value}%` : "0%",
                        background: group.color || topic.color,
                        borderRadius: C.innerRadius,
                        transition: `width 0.8s ${0.3 + bi * 0.06}s ease`,
                      }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
        <div style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "18px 22px", borderLeft: `${C.accentBarHeight}px solid ${topic.color}` }}>
          <p style={{ fontFamily: T.fontDisplay, fontSize: 18, color: T.text, margin: 0, fontWeight: 600 }}>{topic.callout}</p>
        </div>
      </div>
    </div>
  );
}
BarChartScreen.propTypes = { topic: topicPropType.isRequired, onBack: PropTypes.func.isRequired };

// ─── COLOR BLOCKS SCREEN ───
function ColorBlocksScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const C = useChrome();
  const [e, setE] = useState(false);
  useEffect(() => { const t = setTimeout(() => setE(true), 50); return () => clearTimeout(t); }, []);

  const blocks = topic.blocks || [];
  const left = blocks.find((b) => b.area === "left");
  const topRight = blocks.find((b) => b.area === "top-right");
  const bottomRight = blocks.find((b) => b.area === "bottom-right");

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1180, margin: "0 auto", padding: "48px" }}>
        <BackBtn onClick={onBack} />
        <h1 style={{ fontFamily: T.fontDisplay, fontSize: 42, fontWeight: C.headingWeight, color: T.text, margin: "0 0 24px", lineHeight: 1.1 }}>
          {topic.title}
        </h1>
        <div style={{
          display: "grid", gridTemplateColumns: "1fr 1.2fr", gridTemplateRows: "auto 1fr",
          gap: 0, marginBottom: 24, borderRadius: C.cardRadius, overflow: "hidden",
          border: `${C.cardBorderWidth}px solid rgba(0,0,0,0.1)`, minHeight: 420,
        }}>
          {left && (
            <div style={{
              gridRow: "1 / -1", background: left.bgColor || topic.color,
              padding: "40px 32px", display: "flex", flexDirection: "column",
              justifyContent: "center", alignItems: "center",
              opacity: e ? 1 : 0, transition: "opacity 0.6s 0.1s ease",
            }}>
              {left.stat && (
                <>
                  <div style={{ fontFamily: T.fontDisplay, fontSize: 80, fontWeight: 900, color: "#000", lineHeight: 1, marginBottom: 16 }}>{left.stat.val}</div>
                  <p style={{ fontFamily: T.fontBody, fontSize: 14, color: "#000", textAlign: "center", lineHeight: 1.5, maxWidth: 220 }}>{left.stat.label}</p>
                </>
              )}
            </div>
          )}
          {topRight && (
            <div style={{
              background: topRight.bgColor || T.bgCard, padding: "28px 24px",
              display: "flex", alignItems: "center",
              borderBottom: `${C.cardBorderWidth}px solid rgba(0,0,0,0.1)`,
              opacity: e ? 1 : 0, transition: "opacity 0.6s 0.2s ease",
            }}>
              <p style={{ fontFamily: T.fontDisplay, fontSize: 18, color: "#000", lineHeight: 1.5, margin: 0 }}>{topRight.text}</p>
            </div>
          )}
          {bottomRight && (
            <div style={{
              background: bottomRight.bgColor || T.bgCard, padding: "20px 20px",
              overflow: "auto", opacity: e ? 1 : 0, transition: "opacity 0.6s 0.3s ease",
            }}>
              {bottomRight.chartBars && (
                <div style={{ display: "grid", gap: 5 }}>
                  <div style={{ display: "flex", justifyContent: "flex-end", gap: 16, marginBottom: 4, fontSize: 9, fontFamily: T.fontDisplay, fontWeight: 700, color: "#000" }}>
                    <span>PEOPLE ONLY</span><span>AI + PEOPLE</span><span>AI ONLY</span>
                  </div>
                  {bottomRight.chartBars.map((bar, idx) => (
                    <div key={idx} style={{ display: "flex", alignItems: "center", gap: 6 }}>
                      <span style={{ fontFamily: T.fontDisplay, fontSize: 10, fontWeight: 700, color: "#000", minWidth: 100, textTransform: "uppercase", textAlign: "right" }}>{bar.label}</span>
                      <div style={{ flex: 1, display: "flex", height: 14, borderRadius: 2, overflow: "hidden" }}>
                        <div style={{ width: `${bar.peopleOnly}%`, background: "#3399FF", transition: `width 0.8s ${0.3 + idx * 0.04}s ease` }} />
                        <div style={{ width: `${bar.mixed}%`, background: "#FFD600", transition: `width 0.8s ${0.3 + idx * 0.04}s ease` }} />
                        <div style={{ width: `${bar.aiOnly}%`, background: "#00CC66", transition: `width 0.8s ${0.3 + idx * 0.04}s ease` }} />
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
        <div style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "18px 22px", borderLeft: `${C.accentBarHeight}px solid ${topic.color}` }}>
          <p style={{ fontFamily: T.fontDisplay, fontSize: 18, color: T.text, margin: 0, fontWeight: 600 }}>{topic.callout}</p>
        </div>
      </div>
    </div>
  );
}
ColorBlocksScreen.propTypes = { topic: topicPropType.isRequired, onBack: PropTypes.func.isRequired };

// ═══════════════════════════════════════════
// SPRINT CYCLE: FIGURE-8 (OPTION B)
// ═══════════════════════════════════════════
function Figure8Cycle({ entered, nodes }) {
  const canvasRef = useRef(null);
  const progressRef = useRef(0);

  // Node positions on figure-8 — Requirements (index 0) on far left, emphasized
  const W = 860, H = 420;
  const lcx = 280, rcx = 580, cy = 210, lrx = 210, rrx = 210, ry = 155;

  function fig8Pos(t) {
    // t: 0-1, first half = left loop CW, second half = right loop CW
    if (t < 0.5) {
      const a = -Math.PI + t * 2 * Math.PI * 2;
      return { x: lcx + lrx * Math.cos(a), y: cy + ry * Math.sin(a) };
    } else {
      const a = Math.PI - (t - 0.5) * 2 * Math.PI * 2;
      return { x: rcx + rrx * Math.cos(a), y: cy + ry * Math.sin(a) };
    }
  }

  const nodePositions = nodes.map((n, i) => {
    const t = i / Math.max(nodes.length, 1);
    return { ...n, ...fig8Pos(t), t, i };
  });

  useEffect(() => {
    const c = canvasRef.current; if (!c) return;
    const ctx = c.getContext("2d");
    c.width = W * 2; c.height = H * 2; ctx.scale(2, 2);
    let raf;
    function draw() {
      progressRef.current = (progressRef.current + 0.0008) % 1;
      const prog = progressRef.current;
      ctx.clearRect(0, 0, W, H);

      // Draw figure-8 path
      ctx.beginPath();
      for (let i = 0; i <= 300; i++) { const p = fig8Pos(i / 300); i === 0 ? ctx.moveTo(p.x, p.y) : ctx.lineTo(p.x, p.y); }
      ctx.closePath(); ctx.strokeStyle = "rgba(139,92,246,0.1)"; ctx.lineWidth = 2.5; ctx.stroke();

      // Animated comet
      const trailLen = 0.06;
      for (let i = 0; i < 50; i++) {
        const tt = ((prog - (i / 50) * trailLen) + 1) % 1;
        const p = fig8Pos(tt);
        const alpha = (1 - i / 50) * 0.55;
        ctx.beginPath(); ctx.arc(p.x, p.y, 4 - i * 0.06, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(139,92,246,${alpha})`; ctx.fill();
      }
      const lead = fig8Pos(prog);
      ctx.beginPath(); ctx.arc(lead.x, lead.y, 6, 0, Math.PI * 2);
      ctx.fillStyle = "#A78BFA"; ctx.shadowColor = "#8B5CF6"; ctx.shadowBlur = 18; ctx.fill(); ctx.shadowBlur = 0;

      raf = requestAnimationFrame(draw);
    }
    if (entered) draw();
    return () => cancelAnimationFrame(raf);
  }, [entered]);

  return (
    <div style={{ position: "relative", width: W, height: H, margin: "0 auto" }}>
      <canvas ref={canvasRef} style={{ position: "absolute", inset: 0, width: W, height: H }} />

      {/* Phase labels */}
      <div style={{ position: "absolute", left: lcx - 50, top: 12, fontSize: 10, textTransform: "uppercase", letterSpacing: 1.5, fontWeight: 700, color: "#8B5CF6", fontFamily: "'Space Grotesk',sans-serif" }}>Phase 1 — Build</div>
      <div style={{ position: "absolute", left: rcx - 55, top: 12, fontSize: 10, textTransform: "uppercase", letterSpacing: 1.5, fontWeight: 700, color: "#0891B2", fontFamily: "'Space Grotesk',sans-serif" }}>Phase 2 — Validate</div>

      {/* Handoff label */}
      <div style={{ position: "absolute", left: (lcx + rcx) / 2 - 30, top: cy - 12, background: "#111827", border: "1px solid rgba(139,92,246,0.3)", borderRadius: 8, padding: "3px 10px", fontSize: 9, color: "#A78BFA", fontWeight: 700, textTransform: "uppercase", letterSpacing: 1, fontFamily: "'Space Grotesk',sans-serif", zIndex: 6 }}>Handoff</div>

      {/* Nodes */}
      {nodePositions.map((n, i) => {
        const isAI = n.type === "ai";
        const size = 30;
        return (
          <div key={i} style={{
            position: "absolute", left: n.x - size, top: n.y - size, width: size * 2, height: size * 2,
            borderRadius: "50%", background: isAI ? AI_BG : "#162240",
            border: `2px solid ${isAI ? "#7C3AED" : "#0891B2"}60`,
            display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
            fontSize: 22, zIndex: 5,
            boxShadow: `0 0 16px ${isAI ? "rgba(139,92,246,0.18)" : "rgba(8,145,178,0.14)"}`,
            opacity: entered ? 1 : 0,
            transform: entered ? "scale(1)" : "scale(0.7)",
            transition: `all 0.4s ${0.15 + i * 0.06}s cubic-bezier(0.34,1.56,0.64,1)`,
          }}>
            {n.icon}
            {/* Badge */}
            <div style={{ position: "absolute", top: -6, right: -6, fontSize: 8, fontWeight: 700, background: isAI ? "#7C3AED" : "#0891B2", color: "#FFF", borderRadius: 6, padding: "1px 5px", fontFamily: "'Space Grotesk',sans-serif" }}>
              {isAI ? "AI" : "👤"}
            </div>
            {/* Label */}
            <div style={{ position: "absolute", top: size * 2 + 5, fontSize: 11, color: "#E2E8F0", textAlign: "center", whiteSpace: "nowrap", fontWeight: 600, fontFamily: "'Space Grotesk',sans-serif" }}>{n.label}</div>
          </div>
        );
      })}
    </div>
  );
}
Figure8Cycle.propTypes = {
  entered: PropTypes.bool.isRequired,
  nodes: PropTypes.arrayOf(PropTypes.shape({
    icon: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
    type: PropTypes.string.isRequired,
  })).isRequired,
};

// ═══════════════════════════════════════════
// SPRINT CYCLE: CIRCULAR RING (OPTION C)
// ═══════════════════════════════════════════
function CircularRingCycle({ entered, nodes }) {
  const canvasRef = useRef(null);
  const progressRef = useRef(0);
  const SIZE = 480;
  const cx = SIZE / 2, cy = SIZE / 2, R = 185;

  // Requirements (index 0) at 9 o'clock (left)
  const nodePositions = nodes.map((n, i) => {
    const angle = Math.PI + (i / Math.max(nodes.length, 1)) * Math.PI * 2; // start at left (π), go CW
    return { ...n, x: cx + R * Math.cos(angle), y: cy + R * Math.sin(angle), angle, i };
  });

  useEffect(() => {
    const c = canvasRef.current; if (!c) return;
    const ctx = c.getContext("2d");
    c.width = SIZE * 2; c.height = SIZE * 2; ctx.scale(2, 2);
    let raf;
    function draw() {
      progressRef.current = (progressRef.current + 0.0007) % 1;
      const prog = progressRef.current;
      ctx.clearRect(0, 0, SIZE, SIZE);

      // Ring
      ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2);
      ctx.strokeStyle = "rgba(139,92,246,0.08)"; ctx.lineWidth = 3; ctx.stroke();

      // Direction chevrons
      for (let i = 0; i < 12; i++) {
        const a = Math.PI + ((i + 0.5) / 12) * Math.PI * 2;
        const px = cx + R * Math.cos(a), py = cy + R * Math.sin(a);
        const dir = a + Math.PI / 2;
        ctx.save(); ctx.translate(px, py); ctx.rotate(dir);
        ctx.beginPath(); ctx.moveTo(-4, -3); ctx.lineTo(0, 3); ctx.lineTo(4, -3);
        ctx.strokeStyle = "rgba(148,163,184,0.2)"; ctx.lineWidth = 1; ctx.stroke(); ctx.restore();
      }

      // Radar sweep
      const sweepA = Math.PI + prog * Math.PI * 2;
      ctx.beginPath(); ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, R + 15, sweepA - 0.5, sweepA); ctx.closePath();
      const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, R + 15);
      g.addColorStop(0, "rgba(139,92,246,0)"); g.addColorStop(1, "rgba(139,92,246,0.12)");
      ctx.fillStyle = g; ctx.fill();

      // Lead dot
      const da = Math.PI + prog * Math.PI * 2;
      const dx = cx + R * Math.cos(da), dy = cy + R * Math.sin(da);
      ctx.beginPath(); ctx.arc(dx, dy, 5, 0, Math.PI * 2);
      ctx.fillStyle = "#A78BFA"; ctx.shadowColor = "#8B5CF6"; ctx.shadowBlur = 16; ctx.fill(); ctx.shadowBlur = 0;

      // Trail
      for (let i = 1; i < 30; i++) {
        const tp = ((prog - i * 0.003) + 1) % 1;
        const ta = Math.PI + tp * Math.PI * 2;
        ctx.beginPath(); ctx.arc(cx + R * Math.cos(ta), cy + R * Math.sin(ta), 3 - i * 0.08, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(139,92,246,${(1 - i / 30) * 0.35})`; ctx.fill();
      }

      raf = requestAnimationFrame(draw);
    }
    if (entered) draw();
    return () => cancelAnimationFrame(raf);
  }, [entered]);

  return (
    <div style={{ position: "relative", width: SIZE, height: SIZE, margin: "0 auto" }}>
      <canvas ref={canvasRef} style={{ position: "absolute", inset: 0, width: SIZE, height: SIZE }} />

      {/* Center hub */}
      <div style={{ position: "absolute", left: cx - 70, top: cy - 55, width: 140, textAlign: "center", zIndex: 4, opacity: entered ? 1 : 0, transition: "opacity 0.6s 0.5s" }}>
        <div style={{ fontSize: 13, fontWeight: 700, color: "#F0F4F8", fontFamily: "'Space Grotesk',sans-serif", marginBottom: 6 }}>AI Sprint Cycle</div>
        <div style={{ fontSize: 10, color: "#94A3B8", lineHeight: 1.4, marginBottom: 8 }}>1-week cadence</div>
        <div style={{ display: "flex", justifyContent: "center", gap: 14 }}>
          <div><div style={{ fontFamily: "'Space Grotesk',sans-serif", fontSize: 18, fontWeight: 700, color: "#22D3EE" }}>~90%</div><div style={{ fontSize: 7, color: "#64748B", textTransform: "uppercase" }}>AI Code</div></div>
          <div><div style={{ fontFamily: "'Space Grotesk',sans-serif", fontSize: 18, fontWeight: 700, color: "#10B981" }}>0</div><div style={{ fontSize: 7, color: "#64748B", textTransform: "uppercase" }}>Defects</div></div>
        </div>
        <div style={{ display: "flex", justifyContent: "center", gap: 10, marginTop: 8 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 4 }}><div style={{ width: 7, height: 7, borderRadius: "50%", background: "#0891B2" }} /><span style={{ fontSize: 8, color: "#94A3B8" }}>Human</span></div>
          <div style={{ display: "flex", alignItems: "center", gap: 4 }}><div style={{ width: 7, height: 7, borderRadius: "50%", background: "#7C3AED" }} /><span style={{ fontSize: 8, color: "#94A3B8" }}>AI</span></div>
        </div>
      </div>

      {/* Nodes */}
      {nodePositions.map((n, i) => {
        const isAI = n.type === "ai";
        const sz = 26;
        const labelR = R + 46;
        const lx = cx + labelR * Math.cos(n.angle);
        const ly = cy + labelR * Math.sin(n.angle);
        return (
          <React.Fragment key={i}>
            <div style={{
              position: "absolute", left: n.x - sz, top: n.y - sz, width: sz * 2, height: sz * 2,
              borderRadius: "50%", background: isAI ? AI_BG : "#162240",
              border: `2px solid ${isAI ? "#7C3AED" : "#0891B2"}60`,
              display: "flex", alignItems: "center", justifyContent: "center",
              fontSize: 20, zIndex: 5,
              boxShadow: `0 0 14px ${isAI ? "rgba(139,92,246,0.16)" : "rgba(8,145,178,0.12)"}`,
              opacity: entered ? 1 : 0, transform: entered ? "scale(1)" : "scale(0.6)",
              transition: `all 0.4s ${0.2 + i * 0.06}s cubic-bezier(0.34,1.56,0.64,1)`,
            }}>
              {n.icon}
              <div style={{ position: "absolute", top: -5, right: -5, fontSize: 7, fontWeight: 700, background: isAI ? "#7C3AED" : "#0891B2", color: "#FFF", borderRadius: 5, padding: "1px 4px", fontFamily: "'Space Grotesk',sans-serif" }}>
                {isAI ? "AI" : "👤"}
              </div>
            </div>
            <div style={{ position: "absolute", left: lx - 40, top: ly - 7, width: 80, fontSize: 10, color: "#E2E8F0", textAlign: "center", fontWeight: 600, zIndex: 3, fontFamily: "'Space Grotesk',sans-serif", opacity: entered ? 1 : 0, transition: `opacity 0.4s ${0.3 + i * 0.06}s` }}>{n.label}</div>
          </React.Fragment>
        );
      })}
    </div>
  );
}
CircularRingCycle.propTypes = {
  entered: PropTypes.bool.isRequired,
  nodes: PropTypes.arrayOf(PropTypes.shape({
    icon: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
    type: PropTypes.string.isRequired,
  })).isRequired,
};

// ═══════════════════════════════════════════
// SPRINT SCREEN (with B/C toggle)
// ═══════════════════════════════════════════
function SprintScreen({ topic, onBack, nodes }) {
  const T = useContext(ThemeCtx);
  const [entered, setEntered] = useState(false);
  const [layout, setLayout] = useState("fig8");
  useEffect(() => { const t = setTimeout(() => setEntered(true), 50); return () => clearTimeout(t); }, []);

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <Particles color={topic.color} type="sprint" active={entered} />
      <div style={{ position: "relative", zIndex: 2, padding: "36px 48px" }}>
        <BackBtn onClick={onBack} />

        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: 24, opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(-20px)", transition: "all 0.6s cubic-bezier(0.22,1,0.36,1)" }}>
          <div style={{ fontSize: 38, marginBottom: 6, display: "inline-block" }}>
            <span style={{ display: "inline-block", animation: entered ? "spinI 8s linear infinite" : "none" }}>⟳</span>
          </div>
          <style>{`@keyframes spinI { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}</style>
          <h1 style={{ fontFamily: "'Space Grotesk',sans-serif", fontSize: 36, fontWeight: 700, color: "#F0F4F8", margin: "0 0 6px" }}>AI Sprint Cycle</h1>
          <p style={{ fontSize: 14, color: topic.colorLight, fontStyle: "italic", margin: "0 0 16px" }}>{topic.subtitle}</p>

          {/* Layout toggle */}
          <div style={{ display: "flex", justifyContent: "center", gap: 8 }}>
            {[["fig8", "Figure-8 Infinity"], ["ring", "Circular Ring"]].map(([k, l]) => (
              <button key={k} onClick={() => setLayout(k)} style={{
                padding: "6px 16px", borderRadius: 20, cursor: "pointer", fontFamily: "'Space Grotesk',sans-serif", fontSize: 12, fontWeight: 600,
                background: layout === k ? "rgba(139,92,246,0.15)" : "rgba(255,255,255,0.05)",
                border: `1px solid ${layout === k ? "#8B5CF6" : "rgba(255,255,255,0.08)"}`,
                color: layout === k ? "#A78BFA" : "#64748B",
              }}>{l}</button>
            ))}
          </div>
        </div>

        {/* Diagram container */}
        <div style={{ background: "#111827", borderRadius: 16, padding: "28px 20px", border: "1px solid rgba(139,92,246,0.12)", maxWidth: layout === "fig8" ? 920 : 540, margin: "0 auto", boxShadow: "0 4px 40px rgba(0,0,0,0.3)", overflow: "hidden" }}>
          {layout === "fig8" && <Figure8Cycle entered={entered} nodes={nodes} />}
          {layout === "ring" && <CircularRingCycle entered={entered} nodes={nodes} />}
        </div>

        {/* Callout */}
        <div style={{ marginTop: 24, background: "#162240", borderRadius: 10, padding: "16px 28px", borderLeft: "4px solid #8B5CF6", display: "flex", alignItems: "center", gap: 16, maxWidth: 920, marginLeft: "auto", marginRight: "auto", opacity: entered ? 1 : 0, transition: "opacity 0.6s 1.5s" }}>
          <div style={{ fontSize: 22, color: "#8B5CF6" }}>⟳</div>
          <p style={{ fontSize: 13, color: "#CBD5E1", lineHeight: 1.6, margin: 0 }}>
            <strong style={{ color: "#A78BFA" }}>{topic.callout}</strong>
          </p>
        </div>
      </div>
    </div>
  );
}
SprintScreen.propTypes = {
  topic: topicPropType.isRequired,
  onBack: PropTypes.func.isRequired,
  nodes: PropTypes.arrayOf(PropTypes.shape({
    icon: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
    type: PropTypes.string.isRequired,
  })).isRequired,
};

// ═══════════════════════════════════════════
// MAIN APP
// ═══════════════════════════════════════════

const AI_BG = "#1E1B4B";

export default function App() {
  const [deckKey, setDeckKey] = useState(getInitialDeckKey);
  const deck = DECKS[deckKey] || CURRENT_DECK;
  const [theme, setTheme] = useState(() => deck.id === "current" ? null : (THEMES_BY_ID[deck.themeId] || null));
  const [styleModeId, setStyleModeId] = useState("default");
  const chrome = STYLE_MODES_BY_ID[styleModeId];
  const [introDone, setIntroDone] = useState(false);
  const [active, setActive] = useState(null);
  const [transitioning, setTransitioning] = useState(false);
  const [hovered, setHovered] = useState(null);
  const [comet, setComet] = useState({ active: false, from: null, color: null, targetId: null });

  // ── Theme-adaptive color resolution ──
  const deckTopics = useMemo(() =>
    theme ? resolveTopicColors(deck.topics, theme) : deck.topics,
    [deck.topics, theme],
  );
  const introStats = useMemo(() =>
    theme ? resolveIntroStatColors(deck.introStats, theme) : deck.introStats,
    [deck.introStats, theme],
  );

  // Reset state when switching decks
  const switchDeck = (key) => {
    setDeckKey(key);
    setActive(null);
    setIntroDone(false);
    const nextDeck = DECKS[key] || CURRENT_DECK;
    const suggested = THEMES_BY_ID[nextDeck.themeId];
    if (suggested) setTheme(suggested);
  };

  const handleSelect = (id, pos) => {
    const topic = deckTopics.find((t) => t.id === id);
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
  const activeTopic = deckTopics.find((t) => t.id === active);

  const renderActiveTopic = () => {
    if (!activeTopic) {
      return null;
    }

    switch (activeTopic.layout) {
      case "two-col":
        return <OverviewScreen topic={activeTopic} onBack={handleBack} />;
      case "stat-cards":
        if (activeTopic.results || activeTopic.leadershipPoints || activeTopic.enablement || activeTopic.thesis) {
          return <ManifestStatCardsScreen topic={activeTopic} onBack={handleBack} />;
        }
        return <HumanScreen topic={activeTopic} onBack={handleBack} />;
      case "before-after":
        return <HurdlesScreen topic={activeTopic} onBack={handleBack} />;
      case "process-cycle":
        return <SprintScreen topic={activeTopic} onBack={handleBack} nodes={deck.sprintNodes} />;
      case "h-strip":
        return <FutureScreen topic={activeTopic} onBack={handleBack} />;
      case "process-lanes":
        return <PlatformScreen topic={activeTopic} onBack={handleBack} />;
      case "stat-hero":
        return <StatHeroScreen topic={activeTopic} onBack={handleBack} />;
      case "quote-collage":
        return <QuoteCollageScreen topic={activeTopic} onBack={handleBack} />;
      case "badge-grid":
        return <BadgeGridScreen topic={activeTopic} onBack={handleBack} />;
      case "data-table":
        return <DataTableScreen topic={activeTopic} onBack={handleBack} />;
      case "bar-chart":
        return <BarChartScreen topic={activeTopic} onBack={handleBack} />;
      case "color-blocks":
        return <ColorBlocksScreen topic={activeTopic} onBack={handleBack} />;
      default:
        return <OverviewScreen topic={activeTopic} onBack={handleBack} />;
    }
  };

  // Theme selector gate
  if (!theme) return <ThemeSelector onSelect={(t) => setTheme(t)} />;

  const T = theme;
  const introDeck = { ...deck, introStats };

  return (
    <ThemeCtx.Provider value={T}>
    <ChromeCtx.Provider value={chrome}>
    <div style={{ fontFamily: T.fontBody, minHeight: "100vh", background: T.bg, opacity: (transitioning && !comet.active) ? 0 : 1, transition: "opacity 0.35s ease" }}>
      <link href={T.fontsUrl} rel="stylesheet" />
      <CometTransition from={comet.from} color={comet.color} active={comet.active} onDone={handleCometDone} />
      {!introDone && <ThematicIntro deck={introDeck} onComplete={() => setIntroDone(true)} />}
      {!active && introDone && (
        <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column", justifyContent: "center", padding: "40px 48px", opacity: comet.active ? 0 : 1, transition: "opacity 0.4s ease" }}>
          <div style={{ marginBottom: 32 }}>
            <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: 3, color: T.textDim, fontFamily: T.fontDisplay, fontWeight: 500, marginBottom: 10 }}>{deck.brandLine}</div>
            <h1 style={{ fontFamily: T.fontDisplay, fontSize: 44, fontWeight: chrome.headingWeight, color: T.text, margin: "0 0 10px", letterSpacing: -1, lineHeight: 1.05, textTransform: chrome.headingTransform }}>
              {deck.title}<br /><span style={{ background: `linear-gradient(90deg,${T.gradient[0]},${T.gradient[1]})`, WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>{deck.titleAccent}</span>
            </h1>
            <p style={{ fontSize: 15, color: T.textDim, margin: 0, maxWidth: 600 }}>{deck.tagline}</p>
          </div>
          <div style={{ display: "flex", gap: 18, flexWrap: "wrap" }}>
            {deckTopics.map((t) => <LandingTile key={t.id} topic={t} onClick={handleSelect} hovered={hovered} onHover={setHovered} />)}
          </div>

          {/* ── Footer: stats + pickers ── */}
          <div style={{ display: "flex", gap: 24, marginTop: 32, paddingTop: 20, borderTop: `1px solid ${T.border || "rgba(255,255,255,0.06)"}`, flexWrap: "wrap", justifyContent: "space-between", alignItems: "center" }}>
            <div style={{ display: "flex", gap: 36, flexWrap: "wrap" }}>
              {deck.stats.map((s) => (
                <div key={`${s.lbl}-${s.val}`}><div style={{ fontFamily: T.fontDisplay, fontSize: 22, fontWeight: 700, color: T.accent }}>{s.val}</div><div style={{ fontSize: 10, color: T.textDim, textTransform: "uppercase", letterSpacing: 0.8 }}>{s.lbl}</div></div>
              ))}
            </div>
            <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap" }}>
              {/* Deck picker */}
              {Object.keys(DECKS).length > 1 && (
                <div style={{ display: "flex", gap: 4 }}>
                  {Object.entries(DECKS).map(([key, d]) => (
                    <button key={key} onClick={() => switchDeck(key)} style={{
                      background: key === deckKey ? `${T.accent}20` : T.bgCard,
                      border: `1px solid ${key === deckKey ? T.accent : T.textDim + "30"}`,
                      borderRadius: chrome.pillRadius, padding: "5px 12px", fontSize: 10,
                      color: key === deckKey ? T.accent : T.textDim, cursor: "pointer",
                      fontFamily: T.fontBody, textTransform: "uppercase", letterSpacing: 0.8,
                    }}>{d.title} {d.titleAccent}</button>
                  ))}
                </div>
              )}
              {/* Style mode picker */}
              <div style={{ display: "flex", gap: 4 }}>
                {STYLE_MODES.map((m) => (
                  <button key={m.id} onClick={() => setStyleModeId(m.id)} style={{
                    background: m.id === styleModeId ? `${T.accent}20` : T.bgCard,
                    border: `1px solid ${m.id === styleModeId ? T.accent : T.textDim + "30"}`,
                    borderRadius: chrome.pillRadius, padding: "5px 10px", fontSize: 10,
                    color: m.id === styleModeId ? T.accent : T.textDim, cursor: "pointer",
                    fontFamily: T.fontBody, textTransform: "uppercase", letterSpacing: 1,
                  }}>{m.name}</button>
                ))}
              </div>
              {/* Theme switch */}
              <button onClick={() => setTheme(null)} style={{ background: T.bgCard, border: `1px solid ${T.textDim}30`, borderRadius: chrome.pillRadius, padding: "5px 14px", fontSize: 11, color: T.textDim, cursor: "pointer", fontFamily: T.fontBody }}>{T.name} ✎</button>
            </div>
          </div>
        </div>
      )}
      {renderActiveTopic()}
    </div>
    </ChromeCtx.Provider>
    </ThemeCtx.Provider>
  );
}
