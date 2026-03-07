// ═══════════════════════════════════════════════════════════════════════════════
// PRESENTATION STARTER — Config-Driven Advocacy Deck
// ═══════════════════════════════════════════════════════════════════════════════
//
// HOW TO UPDATE THIS DECK WITH SIMPLE PROMPTS:
// ─────────────────────────────────────────────
//
// [PROMPT 1] Rebrand the deck:
//   "Update DECK_CONFIG: set title to '[Your Title]', subtitle to '[Subtitle]',
//    brand to '[Brand/Project Name]', tagline to '[One-line description]',
//    and change the primary color palette to [color theme, e.g. amber/orange]."
//
// [PROMPT 2] Replace a topic tile (landing page card):
//   "In TOPICS, replace topic id '[id]' with: title '[New Title]',
//    subtitle '[Subtitle]', icon '[emoji]', color '[hex]',
//    screen type '[stats | pillars | flow | sprint | cards]'."
//
// [PROMPT 3] Update stats bar on landing page:
//   "Update DECK_CONFIG.stats with these values: [val1/lbl1, val2/lbl2, ...]"
//
// [PROMPT 4] Update a screen's content:
//   "For topic '[id]', update the cards to: [title, body pairs].
//    Update callout to: '[callout text]'."
//
// [PROMPT 5] Add a new screen type:
//   "Add a new screen type 'timeline' that shows a vertical milestone list.
//    Use the same particle/animation patterns as existing screens."
//
// [PROMPT 6] Change the visual theme:
//   "Change the deck theme to [light/dark/navy/slate]. Keep all animations.
//    Update background, card, and text colors accordingly."
//
// [PROMPT 7] Swap the sprint diagram:
//   "Replace sprintNodes with: [list of {icon, label, type} objects].
//    Update phase labels to: Phase 1 '[label]', Phase 2 '[label]'."
//
// [PROMPT 8] Add a results/metrics screen:
//   "Add a screen type 'results' to topic '[id]' with these metrics:
//    [{ val, label, icon, color } list]. Include a headline and subtext."
//
// ═══════════════════════════════════════════════════════════════════════════════

import { useState, useEffect, useRef } from "react";

// ───────────────────────────────────────────────
// DECK CONFIG — Edit everything here
// ───────────────────────────────────────────────
const DECK_CONFIG = {
  brand: "Your Project · Division Name",
  title: "Project Name",
  titleAccent: "Advocacy Deck",
  tagline: "Four narratives. One story. Select a topic to explore.",
  accentGradient: "linear-gradient(90deg,#22D3EE,#10B981)",

  // Landing page bottom stats bar
  stats: [
    { val: "XX%", lbl: "Key Metric 1" },
    { val: "X mo", lbl: "Key Metric 2" },
    { val: "0",   lbl: "Key Metric 3" },
    { val: "~X%", lbl: "Key Metric 4" },
    { val: "~X%", lbl: "Key Metric 5" },
    { val: "X wk", lbl: "Key Metric 6" },
  ],
};

// ───────────────────────────────────────────────
// TOPICS — Each becomes a landing tile + screen
// screen types: "cards" | "pillars" | "sprint" | "flow" | "results"
// ───────────────────────────────────────────────
const TOPICS = [
  {
    id: "topic1",
    num: "01",
    title: "Topic One Title",
    subtitle: "Short supporting subtitle for this narrative.",
    icon: "◉",
    color: "#0891B2",
    colorLight: "#22D3EE",
    colorGlow: "rgba(8,145,178,0.3)",
    screen: "cards",  // renders StatCards screen

    // For screen: "cards"
    headline: "Section Headline",
    subheadline: "Optional italic subheadline text for this section.",
    banner: "Optional banner paragraph. Appears at the top of the screen as a highlighted statement about this topic.",
    cards: [
      { icon: "📊", stat: "100%", statLabel: "Stat Label", title: "Card One", body: "Describe what happened, how it was achieved, or what this metric represents in plain language." },
      { icon: "🤖", stat: "~90%", statLabel: "Stat Label", title: "Card Two", body: "Second supporting point. Keep it factual and punchy — one insight per card." },
      { icon: "✅", stat: "0",    statLabel: "Stat Label", title: "Card Three", body: "Third point. End with the impact or implication — not just the activity." },
    ],
    callout: "One bold closing line that crystallizes the 'so what' of this topic for a senior audience.",
  },

  {
    id: "topic2",
    num: "02",
    title: "Topic Two Title",
    subtitle: "Short supporting subtitle — challenge and resolution framing.",
    icon: "⬡",
    color: "#F59E0B",
    colorLight: "#FBBF24",
    colorGlow: "rgba(245,158,11,0.3)",
    screen: "pillars",  // renders Pillars screen (3 pillars + results)

    // For screen: "pillars"
    headline: "Pillar-Based Section Headline",
    pillars: [
      {
        icon: "🛡️",
        title: "Pillar One",
        items: ["First point under this pillar", "Second point", "Third point"],
      },
      {
        icon: "🔍",
        title: "Pillar Two",
        items: ["First point under this pillar", "Second point", "Third point", "Fourth point"],
      },
      {
        icon: "📝",
        title: "Pillar Three",
        items: ["First point under this pillar", "Second point", "Third point"],
      },
    ],
    results: [
      { val: "XX%", label: "Result metric one description" },
      { val: "X",   label: "Result metric two description" },
      { val: "X mo", label: "Result metric three description" },
      { val: "0",   label: "Result metric four description" },
    ],
    callout: "One bold closing statement summarizing the outcome of this pillar-based approach.",
  },

  {
    id: "topic3",
    num: "03",
    title: "Process / Sprint Cycle",
    subtitle: "Human checkpoints at every stage of delivery.",
    icon: "⟳",
    color: "#8B5CF6",
    colorLight: "#A78BFA",
    colorGlow: "rgba(139,92,246,0.3)",
    screen: "sprint",  // renders Figure-8 sprint diagram

    phase1Label: "Phase 1 — Build",
    phase2Label: "Phase 2 — Validate",
    handoffLabel: "Handoff",
    callout: "The modified process cycle includes numerous human-in-the-loop checkpoints and rapid iteration cadence aligned to Agile best practices.",
  },

  {
    id: "topic4",
    num: "04",
    title: "Topic Four Title",
    subtitle: "Flow, personas, or results framing for final narrative.",
    icon: "△",
    color: "#10B981",
    colorLight: "#34D399",
    colorGlow: "rgba(16,185,129,0.3)",
    screen: "results",  // renders Results/metrics screen

    // For screen: "results"
    headline: "Outcomes & Results",
    subheadline: "What the numbers say about the work.",
    metrics: [
      { val: "XX%", label: "Primary outcome metric", icon: "📈", color: "#10B981" },
      { val: "X mo", label: "Time-to-value metric",   icon: "⏱️", color: "#22D3EE" },
      { val: "0",   label: "Quality/defect metric",   icon: "✅", color: "#FBBF24" },
      { val: "X×",  label: "Multiplier or efficiency gain", icon: "⚡", color: "#A78BFA" },
    ],
    cards: [
      { title: "What We Proved", body: "Summarize the core proof point this project established — what wasn't believed before but is now demonstrated." },
      { title: "What Comes Next", body: "Describe the logical next step, scaled initiative, or investment case that follows from these results." },
    ],
    callout: "The playbook is proven. The question is no longer whether — it's how fast we scale.",
  },
];

// ───────────────────────────────────────────────
// SPRINT NODES — Edit for your process
// type: "human" | "ai"
// ───────────────────────────────────────────────
const SPRINT_NODES = [
  { icon: "📋", label: "Requirements",    type: "human" },
  { icon: "🖥️", label: "UI Mockup",       type: "human" },
  { icon: "🤖", label: "AI Converts AC",  type: "ai"    },
  { icon: "✅", label: "AC Refinement",   type: "human" },
  { icon: "👥", label: "Human Review",    type: "human" },
  { icon: "⚙️", label: "AI Gen Code",     type: "ai"    },
  { icon: "💻", label: "Code Output",     type: "ai"    },
  { icon: "👥", label: "Code Review",     type: "human" },
  { icon: "🧪", label: "Testing",         type: "human" },
  { icon: "🐛", label: "Defect Fix",      type: "human" },
  { icon: "🚀", label: "Deploy",          type: "human" },
  { icon: "📊", label: "Client Review",   type: "human" },
];

// ═══════════════════════════════════════════════
// THEME — Global design tokens
// ═══════════════════════════════════════════════
const T = {
  bg:         "#0B1426",
  bgCard:     "#111827",
  bgDeep:     "#162240",
  text:       "#F0F4F8",
  textMuted:  "#94A3B8",
  textDim:    "#64748B",
  border:     "rgba(255,255,255,0.06)",
  fontDisplay: "'Space Grotesk',sans-serif",
  fontBody:    "'DM Sans',sans-serif",
  aiBg:        "#1E1B4B",
};

// ═══════════════════════════════════════════════
// PARTICLES ENGINE
// ═══════════════════════════════════════════════
function Particles({ color, mode = "network", active }) {
  const canvasRef = useRef(null);
  const animRef   = useRef(null);
  const pRef      = useRef([]);

  useEffect(() => {
    const c = canvasRef.current; if (!c) return;
    const ctx = c.getContext("2d");
    c.width  = c.offsetWidth  * 2;
    c.height = c.offsetHeight * 2;
    ctx.scale(2, 2);
    const W = c.offsetWidth, H = c.offsetHeight;
    const count = mode === "orbit" ? 40 : 28;

    pRef.current = Array.from({ length: count }, () => ({
      x: Math.random() * W, y: Math.random() * H,
      vx: (Math.random() - 0.5) * 0.6, vy: (Math.random() - 0.5) * 0.6,
      r:  Math.random() * 2 + 0.8,
      o:  Math.random() * 0.45 + 0.1,
      life: Math.random() * 200,
    }));

    function tick() {
      ctx.clearRect(0, 0, W, H);
      const pts = pRef.current;

      pts.forEach(p => {
        p.life++;
        if (mode === "orbit") {
          const cx = W / 2, cy = H / 2;
          const a = Math.atan2(p.y - cy, p.x - cx);
          p.x += Math.cos(a + Math.PI / 2) * 0.32;
          p.y += Math.sin(a + Math.PI / 2) * 0.32;
          const d = Math.sqrt((p.x - cx) ** 2 + (p.y - cy) ** 2);
          if (d > Math.max(W, H) * 0.56) {
            p.x = cx + (Math.random() - 0.5) * W * 0.4;
            p.y = cy + (Math.random() - 0.5) * H * 0.4;
          }
        } else {
          p.x += Math.sin(p.life * 0.013) * 0.25;
          p.y += Math.cos(p.life * 0.011) * 0.25;
        }
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = color + Math.round(p.o * 255).toString(16).padStart(2, "0");
        ctx.fill();
      });

      if (mode === "network") {
        for (let i = 0; i < pts.length; i++) {
          for (let j = i + 1; j < pts.length; j++) {
            const dx = pts[i].x - pts[j].x, dy = pts[i].y - pts[j].y;
            const d  = Math.sqrt(dx * dx + dy * dy);
            if (d < 115) {
              ctx.beginPath();
              ctx.moveTo(pts[i].x, pts[i].y);
              ctx.lineTo(pts[j].x, pts[j].y);
              ctx.strokeStyle = color + Math.round((1 - d / 115) * 38).toString(16).padStart(2, "0");
              ctx.lineWidth   = 0.4;
              ctx.stroke();
            }
          }
        }
      }
      animRef.current = requestAnimationFrame(tick);
    }

    if (active) tick();
    return () => cancelAnimationFrame(animRef.current);
  }, [color, mode, active]);

  return (
    <canvas ref={canvasRef} style={{
      position: "absolute", inset: 0, width: "100%", height: "100%",
      pointerEvents: "none", opacity: active ? 1 : 0, transition: "opacity 0.8s",
    }} />
  );
}

// ═══════════════════════════════════════════════
// SHARED UI ATOMS
// ═══════════════════════════════════════════════
function BackBtn({ onClick }) {
  return (
    <button onClick={onClick} style={{
      background: "none", border: `1px solid ${T.border}`, color: T.textMuted,
      fontSize: 12, cursor: "pointer", fontFamily: T.fontDisplay,
      marginBottom: 24, display: "flex", alignItems: "center", gap: 6,
      padding: "6px 14px", borderRadius: 20, letterSpacing: 1,
    }}>
      ← Back
    </button>
  );
}

function SectionHeader({ topic, entered }) {
  return (
    <div style={{
      textAlign: "center", marginBottom: 40,
      opacity: entered ? 1 : 0,
      transform: entered ? "translateY(0)" : "translateY(24px)",
      transition: "all 0.7s cubic-bezier(0.22,1,0.36,1)",
    }}>
      <div style={{ width: 60, height: 60, borderRadius: "50%", background: topic.color + "16", border: `2px solid ${topic.color}40`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 26, margin: "0 auto 16px", boxShadow: `0 0 36px ${topic.colorGlow}` }}>
        {topic.icon}
      </div>
      <div style={{ fontSize: 10, fontFamily: T.fontDisplay, fontWeight: 600, color: topic.color, letterSpacing: 2.5, textTransform: "uppercase", marginBottom: 6 }}>
        {DECK_CONFIG.brand}
      </div>
      <h1 style={{ fontFamily: T.fontDisplay, fontSize: 40, fontWeight: 700, color: T.text, margin: "0 0 6px", letterSpacing: -0.5 }}>
        {topic.headline || topic.title}
      </h1>
      {topic.subheadline && (
        <p style={{ fontSize: 15, color: topic.colorLight, fontStyle: "italic", margin: 0 }}>
          {topic.subheadline}
        </p>
      )}
      <div style={{ width: 64, height: 3, background: `linear-gradient(90deg,${topic.color},${topic.colorLight})`, margin: "18px auto 0", borderRadius: 2 }} />
    </div>
  );
}

function Callout({ topic, text, entered, delay = "0.9s" }) {
  return (
    <div style={{
      textAlign: "center", marginTop: 32, padding: "22px 24px",
      borderTop: `1px solid ${topic.color}20`, borderBottom: `1px solid ${topic.color}20`,
      opacity: entered ? 1 : 0, transition: `opacity 0.8s ${delay}`,
    }}>
      <p style={{ fontSize: 15, color: T.textMuted, lineHeight: 1.65, margin: 0, maxWidth: 640, marginLeft: "auto", marginRight: "auto" }}>
        <span style={{ color: topic.colorLight, fontWeight: 700 }}>"{text}"</span>
      </p>
    </div>
  );
}

// ═══════════════════════════════════════════════
// SCREEN: CARDS (stat cards)
// ═══════════════════════════════════════════════
function CardsScreen({ topic, onBack }) {
  const [e, setE] = useState(false);
  useEffect(() => { const t = setTimeout(() => setE(true), 50); return () => clearTimeout(t); }, []);

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <Particles color={topic.color} mode="network" active={e} />
      <div style={{ position: "relative", zIndex: 2, maxWidth: 900, margin: "0 auto", padding: "48px 32px", opacity: e ? 1 : 0, transform: e ? "none" : "translateY(30px)", transition: "all 0.8s cubic-bezier(0.22,1,0.36,1)" }}>
        <BackBtn onClick={onBack} />
        <SectionHeader topic={topic} entered={e} />

        {/* Optional banner */}
        {topic.banner && (
          <div style={{ background: topic.color + "10", border: `1px solid ${topic.color}25`, borderLeft: `4px solid ${topic.color}`, borderRadius: 8, padding: "14px 22px", marginBottom: 28, opacity: e ? 1 : 0, transition: "opacity 0.6s 0.2s" }}>
            <p style={{ fontSize: 14, color: "#CBD5E1", lineHeight: 1.65, margin: 0 }}>{topic.banner}</p>
          </div>
        )}

        {/* Stat cards */}
        {topic.cards.map((c, i) => (
          <div key={i} style={{
            background: T.bgDeep, borderRadius: 12, padding: "26px 30px", marginBottom: 18,
            display: "flex", alignItems: "flex-start", gap: 22,
            borderLeft: `4px solid ${topic.color}`,
            opacity: e ? 1 : 0, transform: e ? "none" : "translateY(20px)",
            transition: `all 0.6s ${0.3 + i * 0.15}s cubic-bezier(0.22,1,0.36,1)`,
          }}>
            <div style={{ flexShrink: 0, textAlign: "center", minWidth: 68 }}>
              {c.stat && <div style={{ fontFamily: T.fontDisplay, fontSize: 30, fontWeight: 700, color: topic.colorLight, lineHeight: 1 }}>{c.stat}</div>}
              {c.statLabel && <div style={{ fontSize: 9, color: T.textDim, textTransform: "uppercase", letterSpacing: 1, marginTop: 3 }}>{c.statLabel}</div>}
              {c.icon && !c.stat && <div style={{ fontSize: 28 }}>{c.icon}</div>}
            </div>
            <div>
              <h3 style={{ fontFamily: T.fontDisplay, fontSize: 17, fontWeight: 700, color: topic.colorLight, margin: "0 0 8px" }}>{c.title}</h3>
              <p style={{ fontSize: 14, color: "#CBD5E1", lineHeight: 1.65, margin: 0 }}>{c.body}</p>
            </div>
          </div>
        ))}

        <Callout topic={topic} text={topic.callout} entered={e} />
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════
// SCREEN: PILLARS (3-column + results)
// ═══════════════════════════════════════════════
function PillarsScreen({ topic, onBack }) {
  const [e, setE] = useState(false);
  const [step, setStep] = useState(0);
  useEffect(() => { const t = setTimeout(() => setE(true), 50); return () => clearTimeout(t); }, []);
  useEffect(() => {
    if (!e) return;
    const timers = [0, 250, 500, 750].map((d, i) => setTimeout(() => setStep(i + 1), 400 + d));
    return () => timers.forEach(clearTimeout);
  }, [e]);

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <Particles color={topic.color} mode="network" active={e} />
      <div style={{ position: "absolute", inset: 0, pointerEvents: "none", overflow: "hidden" }}>
        {[...Array(6)].map((_, i) => (
          <div key={i} style={{ position: "absolute", left: "-10%", top: `${12 + i * 14}%`, width: e ? "120%" : "0%", height: 1, background: `linear-gradient(90deg,transparent,${topic.color}12,transparent)`, transition: `width ${0.5 + i * 0.08}s ${0.15 + i * 0.05}s ease` }} />
        ))}
      </div>
      <div style={{ position: "relative", zIndex: 2, padding: "40px 52px" }}>
        <BackBtn onClick={onBack} />
        <div style={{ textAlign: "center", marginBottom: 36, opacity: e ? 1 : 0, transition: "all 0.6s" }}>
          <div style={{ fontSize: 10, fontFamily: T.fontDisplay, fontWeight: 600, color: topic.color, letterSpacing: 2.5, textTransform: "uppercase", marginBottom: 6 }}>{DECK_CONFIG.brand}</div>
          <h1 style={{ fontFamily: T.fontDisplay, fontSize: 40, fontWeight: 700, color: T.text, margin: "0 0 6px" }}>{topic.headline || topic.title}</h1>
          <p style={{ fontSize: 14, color: topic.colorLight, fontStyle: "italic", margin: 0 }}>{topic.subtitle}</p>
        </div>

        {/* Pillars + Results row */}
        <div style={{ display: "flex", alignItems: "stretch", gap: 0, maxWidth: 1100, margin: "0 auto 24px", background: T.bgCard, borderRadius: 12, overflow: "hidden", border: `1px solid ${topic.color}18` }}>
          {(topic.pillars || []).map((p, i) => (
            <div key={i} style={{
              flex: 1, padding: "26px 22px", borderRight: `1px solid ${topic.color}12`,
              opacity: step > i ? 1 : 0, transform: step > i ? "none" : "translateY(14px)",
              transition: "all 0.5s cubic-bezier(0.22,1,0.36,1)",
            }}>
              <div style={{ fontSize: 26, marginBottom: 10 }}>{p.icon}</div>
              <h3 style={{ fontFamily: T.fontDisplay, fontSize: 13, fontWeight: 700, color: topic.colorLight, margin: "0 0 14px", textTransform: "uppercase", letterSpacing: 1 }}>{p.title}</h3>
              <div style={{ display: "flex", flexDirection: "column", gap: 7 }}>
                {p.items.map((item, j) => (
                  <div key={j} style={{ display: "flex", alignItems: "flex-start", gap: 8 }}>
                    <div style={{ width: 4, height: 4, borderRadius: "50%", background: topic.color, marginTop: 6, flexShrink: 0 }} />
                    <p style={{ fontSize: 12, color: "#94A3B8", lineHeight: 1.55, margin: 0 }}>{item}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
          {/* Results column */}
          {topic.results && (
            <div style={{
              flex: 1, padding: "26px 22px", background: `linear-gradient(135deg,${topic.color}12,transparent)`,
              opacity: step > (topic.pillars?.length || 0) - 1 ? 1 : 0,
              transform: step > (topic.pillars?.length || 0) - 1 ? "none" : "translateY(14px)",
              transition: "all 0.5s 0.2s cubic-bezier(0.22,1,0.36,1)",
            }}>
              <div style={{ fontSize: 26, marginBottom: 10 }}>🏆</div>
              <h3 style={{ fontFamily: T.fontDisplay, fontSize: 13, fontWeight: 700, color: topic.colorLight, margin: "0 0 14px", textTransform: "uppercase", letterSpacing: 1 }}>Results</h3>
              <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                {topic.results.map((r, i) => (
                  <div key={i} style={{ display: "flex", alignItems: "baseline", gap: 8 }}>
                    <div style={{ fontFamily: T.fontDisplay, fontSize: 24, fontWeight: 700, color: "#FBBF24", lineHeight: 1 }}>{r.val}</div>
                    <p style={{ fontSize: 11, color: "#94A3B8", lineHeight: 1.45, margin: 0 }}>{r.label}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Callout */}
        <div style={{ maxWidth: 1100, margin: "0 auto", background: T.bgDeep, borderLeft: `4px solid ${topic.color}`, borderRadius: 8, padding: "16px 24px", display: "flex", alignItems: "center", gap: 14, opacity: e ? 1 : 0, transition: "opacity 0.6s 1.2s" }}>
          <div style={{ fontSize: 22, color: topic.color }}>⚡</div>
          <p style={{ fontSize: 13, color: "#CBD5E1", lineHeight: 1.6, margin: 0 }}>
            <strong style={{ color: topic.colorLight }}>{topic.callout}</strong>
          </p>
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════
// SCREEN: RESULTS (metrics grid)
// ═══════════════════════════════════════════════
function ResultsScreen({ topic, onBack }) {
  const [e, setE] = useState(false);
  useEffect(() => { const t = setTimeout(() => setE(true), 50); return () => clearTimeout(t); }, []);

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <Particles color={topic.color} mode="network" active={e} />
      <div style={{ position: "absolute", top: "38%", left: "50%", width: e ? "130%" : "0%", height: 1, background: `linear-gradient(90deg,transparent,${topic.color}25,transparent)`, transform: "translateX(-50%)", transition: "width 1.1s cubic-bezier(0.22,1,0.36,1)" }} />
      <div style={{ position: "relative", zIndex: 2, padding: "48px 52px" }}>
        <BackBtn onClick={onBack} />
        <SectionHeader topic={topic} entered={e} />

        {/* Metrics */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 16, maxWidth: 960, margin: "0 auto 36px" }}>
          {(topic.metrics || []).map((m, i) => (
            <div key={i} style={{
              background: T.bgDeep, borderRadius: 12, padding: "28px 20px", textAlign: "center",
              border: `1px solid ${m.color || topic.color}25`,
              opacity: e ? 1 : 0, transform: e ? "scale(1)" : "scale(0.85)",
              transition: `all 0.5s ${0.25 + i * 0.1}s cubic-bezier(0.22,1,0.36,1)`,
            }}>
              <div style={{ fontSize: 28, marginBottom: 8 }}>{m.icon}</div>
              <div style={{ fontFamily: T.fontDisplay, fontSize: 36, fontWeight: 700, color: m.color || topic.colorLight, lineHeight: 1, marginBottom: 8 }}>{m.val}</div>
              <p style={{ fontSize: 12, color: T.textMuted, lineHeight: 1.5, margin: 0 }}>{m.label}</p>
            </div>
          ))}
        </div>

        {/* Supporting cards */}
        {topic.cards && (
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 18, maxWidth: 960, margin: "0 auto" }}>
            {topic.cards.map((c, i) => (
              <div key={i} style={{
                background: T.bgDeep, borderRadius: 10, padding: "24px 26px",
                borderLeft: `4px solid ${topic.color}`,
                opacity: e ? 1 : 0, transform: e ? "none" : "translateY(18px)",
                transition: `all 0.5s ${0.55 + i * 0.12}s cubic-bezier(0.22,1,0.36,1)`,
              }}>
                <h3 style={{ fontFamily: T.fontDisplay, fontSize: 16, fontWeight: 700, color: topic.colorLight, margin: "0 0 8px" }}>{c.title}</h3>
                <p style={{ fontSize: 13.5, color: "#CBD5E1", lineHeight: 1.65, margin: 0 }}>{c.body}</p>
              </div>
            ))}
          </div>
        )}

        <Callout topic={topic} text={topic.callout} entered={e} delay="1s" />
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════
// SCREEN: SPRINT (figure-8 diagram)
// ═══════════════════════════════════════════════
function SprintScreen({ topic, onBack }) {
  const canvasRef    = useRef(null);
  const progressRef  = useRef(0);
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 50); return () => clearTimeout(t); }, []);

  const W = 820, H = 400;
  const lcx = 255, rcx = 565, cy = 198, lrx = 194, rrx = 194, ry = 142;

  function fig8Pos(t) {
    if (t < 0.5) {
      const a = -Math.PI + t * 2 * Math.PI * 2;
      return { x: lcx + lrx * Math.cos(a), y: cy + ry * Math.sin(a) };
    } else {
      const a = Math.PI - (t - 0.5) * 2 * Math.PI * 2;
      return { x: rcx + rrx * Math.cos(a), y: cy + ry * Math.sin(a) };
    }
  }

  const nodePositions = SPRINT_NODES.map((n, i) => ({ ...n, ...fig8Pos(i / 12), i }));

  useEffect(() => {
    const c = canvasRef.current; if (!c) return;
    const ctx = c.getContext("2d");
    c.width = W * 2; c.height = H * 2; ctx.scale(2, 2);
    let raf;
    function draw() {
      progressRef.current = (progressRef.current + 0.0007) % 1;
      const prog = progressRef.current;
      ctx.clearRect(0, 0, W, H);
      ctx.beginPath();
      for (let i = 0; i <= 300; i++) { const p = fig8Pos(i / 300); i === 0 ? ctx.moveTo(p.x, p.y) : ctx.lineTo(p.x, p.y); }
      ctx.closePath(); ctx.strokeStyle = topic.color + "20"; ctx.lineWidth = 2; ctx.stroke();
      const tl = 0.055;
      for (let i = 0; i < 44; i++) {
        const tt = ((prog - (i / 44) * tl) + 1) % 1;
        const p  = fig8Pos(tt);
        ctx.beginPath(); ctx.arc(p.x, p.y, 4.2 - i * 0.08, 0, Math.PI * 2);
        ctx.fillStyle = topic.color + Math.round((1 - i / 44) * 0.5 * 255).toString(16).padStart(2, "0"); ctx.fill();
      }
      const lead = fig8Pos(prog);
      ctx.beginPath(); ctx.arc(lead.x, lead.y, 6, 0, Math.PI * 2);
      ctx.fillStyle = topic.colorLight; ctx.shadowColor = topic.color; ctx.shadowBlur = 16; ctx.fill(); ctx.shadowBlur = 0;
      raf = requestAnimationFrame(draw);
    }
    if (entered) draw();
    return () => cancelAnimationFrame(raf);
  }, [entered, topic.color, topic.colorLight]);

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <Particles color={topic.color} mode="orbit" active={entered} />
      <div style={{ position: "relative", zIndex: 2, padding: "40px 52px" }}>
        <BackBtn onClick={onBack} />
        <div style={{ textAlign: "center", marginBottom: 24, opacity: entered ? 1 : 0, transition: "all 0.6s" }}>
          <div style={{ fontSize: 10, fontFamily: T.fontDisplay, fontWeight: 600, color: topic.color, letterSpacing: 2.5, textTransform: "uppercase", marginBottom: 6 }}>{DECK_CONFIG.brand}</div>
          <h1 style={{ fontFamily: T.fontDisplay, fontSize: 38, fontWeight: 700, color: T.text, margin: "0 0 6px" }}>{topic.title}</h1>
          <p style={{ fontSize: 14, color: topic.colorLight, fontStyle: "italic", margin: "0 0 16px" }}>{topic.subtitle}</p>
          <div style={{ display: "flex", justifyContent: "center", gap: 20 }}>
            {[["#0891B2", "👤 Human Checkpoint"], [T.aiBg, "🤖 AI Step"]].map(([bg, label], i) => (
              <div key={i} style={{ display: "flex", alignItems: "center", gap: 6 }}>
                <div style={{ width: 8, height: 8, borderRadius: "50%", background: i === 0 ? "#0891B2" : "#7C3AED" }} />
                <span style={{ fontSize: 11, color: T.textMuted, fontFamily: T.fontDisplay }}>{label}</span>
              </div>
            ))}
          </div>
        </div>

        <div style={{ background: T.bgCard, borderRadius: 14, padding: "24px 16px", border: `1px solid ${topic.color}14`, maxWidth: 880, margin: "0 auto", boxShadow: "0 4px 40px rgba(0,0,0,0.35)", overflow: "hidden" }}>
          <div style={{ position: "relative", width: W, height: H, margin: "0 auto" }}>
            <canvas ref={canvasRef} style={{ position: "absolute", inset: 0, width: W, height: H }} />
            <div style={{ position: "absolute", left: lcx - 46, top: 10, fontSize: 9, textTransform: "uppercase", letterSpacing: 1.5, fontWeight: 700, color: topic.color, fontFamily: T.fontDisplay }}>{topic.phase1Label || "Phase 1 — Build"}</div>
            <div style={{ position: "absolute", left: rcx - 52, top: 10, fontSize: 9, textTransform: "uppercase", letterSpacing: 1.5, fontWeight: 700, color: "#0891B2", fontFamily: T.fontDisplay }}>{topic.phase2Label || "Phase 2 — Validate"}</div>
            <div style={{ position: "absolute", left: (lcx + rcx) / 2 - 26, top: cy - 10, background: T.bg, border: `1px solid ${topic.color}35`, borderRadius: 8, padding: "3px 10px", fontSize: 8, color: topic.colorLight, fontWeight: 700, textTransform: "uppercase", letterSpacing: 1, fontFamily: T.fontDisplay, zIndex: 6 }}>{topic.handoffLabel || "Handoff"}</div>
            {nodePositions.map((n, i) => {
              const isAI = n.type === "ai";
              const sz   = 25;
              return (
                <div key={i} style={{
                  position: "absolute", left: n.x - sz, top: n.y - sz, width: sz * 2, height: sz * 2,
                  borderRadius: "50%", background: isAI ? T.aiBg : T.bgDeep,
                  border: `2px solid ${isAI ? "#7C3AED" : "#0891B2"}50`,
                  display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16, zIndex: 5,
                  opacity: entered ? 1 : 0, transform: entered ? "scale(1)" : "scale(0.6)",
                  transition: `all 0.4s ${0.12 + i * 0.055}s cubic-bezier(0.34,1.56,0.64,1)`,
                }}>
                  {n.icon}
                  <div style={{ position: "absolute", top: -5, right: -5, fontSize: 6, fontWeight: 700, background: isAI ? "#7C3AED" : "#0891B2", color: "#FFF", borderRadius: 4, padding: "1px 4px", fontFamily: T.fontDisplay }}>
                    {isAI ? "AI" : "👤"}
                  </div>
                  <div style={{ position: "absolute", top: sz * 2 + 5, fontSize: 8, color: isAI ? topic.colorLight : T.textMuted, textAlign: "center", whiteSpace: "nowrap", fontFamily: T.fontDisplay, fontWeight: 600 }}>{n.label}</div>
                </div>
              );
            })}
          </div>
        </div>

        <div style={{ marginTop: 20, background: T.bgDeep, borderRadius: 8, padding: "14px 24px", borderLeft: `4px solid ${topic.color}`, display: "flex", alignItems: "center", gap: 14, maxWidth: 880, marginLeft: "auto", marginRight: "auto", opacity: entered ? 1 : 0, transition: "opacity 0.6s 1.2s" }}>
          <span style={{ fontSize: 20, color: topic.color }}>⟳</span>
          <p style={{ fontSize: 13, color: "#CBD5E1", lineHeight: 1.6, margin: 0 }}>
            <strong style={{ color: topic.colorLight }}>{topic.callout}</strong>
          </p>
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════
// LANDING TILE
// ═══════════════════════════════════════════════
function LandingTile({ topic, onClick, hovered, onHover }) {
  const h = hovered === topic.id;
  return (
    <div onClick={onClick} onMouseEnter={() => onHover(topic.id)} onMouseLeave={() => onHover(null)}
      style={{
        flex: 1, position: "relative", cursor: "pointer", overflow: "hidden",
        borderRadius: 14, padding: "30px 26px", display: "flex", flexDirection: "column",
        justifyContent: "space-between", minHeight: 290, background: T.bgCard,
        border: `1px solid ${h ? topic.color + "55" : T.border}`,
        boxShadow: h ? `0 0 44px ${topic.colorGlow}, 0 8px 32px rgba(0,0,0,0.4)` : "0 4px 20px rgba(0,0,0,0.3)",
        transform: h ? "translateY(-7px) scale(1.015)" : "translateY(0) scale(1)",
        transition: "all 0.38s cubic-bezier(0.34,1.56,0.64,1)",
      }}>
      <div style={{ position: "absolute", top: 0, right: 0, width: 70, height: 70, background: `linear-gradient(225deg,${topic.color}14,transparent)`, borderRadius: "0 14px 0 0" }} />
      <div>
        <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 12 }}>
          <span style={{ fontSize: 11, fontFamily: T.fontDisplay, fontWeight: 600, color: topic.color, letterSpacing: 2, textTransform: "uppercase", opacity: 0.75 }}>{topic.num}</span>
          <div style={{ flex: 1, height: 1, background: `linear-gradient(90deg,${topic.color}28,transparent)` }} />
        </div>
        <div style={{ fontSize: 34, marginBottom: 10, lineHeight: 1, filter: h ? `drop-shadow(0 0 10px ${topic.colorGlow})` : "none", transition: "filter 0.35s" }}>{topic.icon}</div>
        <h2 style={{ fontFamily: T.fontDisplay, fontSize: 20, fontWeight: 700, color: T.text, lineHeight: 1.2, margin: "0 0 6px" }}>{topic.title}</h2>
        <p style={{ fontSize: 12, color: T.textMuted, lineHeight: 1.5, margin: 0 }}>{topic.subtitle}</p>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 6, marginTop: 18, color: topic.color, fontSize: 11, fontWeight: 700, fontFamily: T.fontDisplay, letterSpacing: 1, textTransform: "uppercase", transform: h ? "translateX(5px)" : "translateX(0)", transition: "transform 0.25s" }}>
        Explore <span style={{ fontSize: 14 }}>→</span>
      </div>
      <div style={{ position: "absolute", bottom: 0, left: 0, right: 0, height: 2, background: `linear-gradient(90deg,${topic.color},${topic.colorLight})`, opacity: h ? 1 : 0.3, transition: "opacity 0.3s" }} />
    </div>
  );
}

// ═══════════════════════════════════════════════
// ROUTER — maps screen type to component
// ═══════════════════════════════════════════════
function ScreenRouter({ topic, onBack }) {
  switch (topic.screen) {
    case "cards":   return <CardsScreen   topic={topic} onBack={onBack} />;
    case "pillars": return <PillarsScreen topic={topic} onBack={onBack} />;
    case "sprint":  return <SprintScreen  topic={topic} onBack={onBack} />;
    case "results": return <ResultsScreen topic={topic} onBack={onBack} />;
    default:        return <CardsScreen   topic={topic} onBack={onBack} />;
  }
}

// ═══════════════════════════════════════════════
// APP ROOT
// ═══════════════════════════════════════════════
export default function App() {
  const [active, setActive]             = useState(null);
  const [transitioning, setTransitioning] = useState(false);
  const [hovered, setHovered]           = useState(null);

  const go   = (id) => { setTransitioning(true); setTimeout(() => { setActive(id);   setTransitioning(false); }, 380); };
  const back = ()   => { setTransitioning(true); setTimeout(() => { setActive(null); setTransitioning(false); }, 340); };

  const activeTopic = TOPICS.find(t => t.id === active);

  return (
    <div style={{ fontFamily: T.fontBody, minHeight: "100vh", background: T.bg, opacity: transitioning ? 0 : 1, transition: "opacity 0.32s ease" }}>
      <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet" />

      {!active && (
        <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column", justifyContent: "center", padding: "40px 52px" }}>
          {/* Header */}
          <div style={{ marginBottom: 36 }}>
            <div style={{ fontSize: 10, textTransform: "uppercase", letterSpacing: 3, color: T.textDim, fontFamily: T.fontDisplay, fontWeight: 600, marginBottom: 8 }}>
              {DECK_CONFIG.brand}
            </div>
            <h1 style={{ fontFamily: T.fontDisplay, fontSize: 44, fontWeight: 700, color: T.text, margin: "0 0 10px", letterSpacing: -1, lineHeight: 1.06 }}>
              {DECK_CONFIG.title}<br />
              <span style={{ background: DECK_CONFIG.accentGradient, WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
                {DECK_CONFIG.titleAccent}
              </span>
            </h1>
            <p style={{ fontSize: 14, color: T.textMuted, margin: 0, maxWidth: 560 }}>{DECK_CONFIG.tagline}</p>
          </div>

          {/* Topic tiles */}
          <div style={{ display: "flex", gap: 16, marginBottom: 32 }}>
            {TOPICS.map(t => (
              <LandingTile key={t.id} topic={t} onClick={() => go(t.id)} hovered={hovered} onHover={setHovered} />
            ))}
          </div>

          {/* Stats bar */}
          <div style={{ display: "flex", gap: 0, paddingTop: 22, borderTop: `1px solid ${T.border}`, flexWrap: "wrap" }}>
            {DECK_CONFIG.stats.map((s, i) => (
              <div key={i} style={{ paddingRight: 32, paddingLeft: i > 0 ? 0 : 0, borderRight: i < DECK_CONFIG.stats.length - 1 ? `1px solid ${T.border}` : "none", marginRight: i < DECK_CONFIG.stats.length - 1 ? 32 : 0 }}>
                <div style={{ fontFamily: T.fontDisplay, fontSize: 22, fontWeight: 700, color: "#22D3EE" }}>{s.val}</div>
                <div style={{ fontSize: 9, color: T.textDim, textTransform: "uppercase", letterSpacing: 0.8, marginTop: 2 }}>{s.lbl}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {active && activeTopic && <ScreenRouter topic={activeTopic} onBack={back} />}
    </div>
  );
}
