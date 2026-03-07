// ═══════════════════════════════════════════════════════════════════════════════
// ADVOCACY DECK — Config-Driven Presentation Renderer
// ═══════════════════════════════════════════════════════════════════════════════
//
// TO CUSTOMIZE THIS DECK:
// 1. Edit deck-config.json (or inline CONFIG below for artifact use)
// 2. deck.title, deck.titleAccent, deck.tagline — landing page header
// 3. deck.stats — bottom stats bar on landing
// 4. pages[] — each entry becomes a tile + detail screen
// 5. page.layout — determines the screen type
// 6. page.cards — content for each card (shape depends on layout)
//
// AVAILABLE LAYOUTS:
//   stat-cards   — Metric cards (stat + body)
//   before-after — Challenge vs solution split
//   pillars      — Column breakdown + results
//   timeline     — Phased roadmap with milestones
//   sprint       — Figure-8 process diagram
//   results      — KPI metrics grid
//   personas     — Stakeholder role cards
//   comparison   — Evaluation matrix
//
// TO USE AS AI ARTIFACT: Replace the import line below with an inlined
// config object. Works with Claude, ChatGPT, Gemini, or any React artifact renderer.
// See advocacy-deck-artifact.jsx for the pre-inlined version.
// ═══════════════════════════════════════════════════════════════════════════════

import { useState, useEffect, useRef } from "react";
import config from "./deck-config.json";

// ───────────────────────────────────────────────
// HELPERS
// ───────────────────────────────────────────────
function hexToGlow(hex, opacity = 0.3) {
  const h = hex.replace("#", "");
  const r = parseInt(h.substring(0, 2), 16);
  const g = parseInt(h.substring(2, 4), 16);
  const b = parseInt(h.substring(4, 6), 16);
  return `rgba(${r},${g},${b},${opacity})`;
}

function hexAlpha(hex, alpha) {
  return hex + Math.round(alpha * 255).toString(16).padStart(2, "0");
}

// ───────────────────────────────────────────────
// THEME — Derived from config
// ───────────────────────────────────────────────
const T = config.deck.theme;
const DECK = config.deck;
const PAGES = config.pages.map((p) => ({
  ...p,
  colorGlow: hexToGlow(p.theme.color, 0.3),
}));

// ═══════════════════════════════════════════════
// PARTICLES ENGINE
// ═══════════════════════════════════════════════
function Particles({ color, mode = "network", active }) {
  const canvasRef = useRef(null);
  const animRef = useRef(null);
  const pRef = useRef([]);

  useEffect(() => {
    const c = canvasRef.current;
    if (!c) return;
    const ctx = c.getContext("2d");
    c.width = c.offsetWidth * 2;
    c.height = c.offsetHeight * 2;
    ctx.scale(2, 2);
    const W = c.offsetWidth,
      H = c.offsetHeight;
    const count = mode === "orbit" ? 40 : 28;

    pRef.current = Array.from({ length: count }, () => ({
      x: Math.random() * W,
      y: Math.random() * H,
      vx: (Math.random() - 0.5) * 0.6,
      vy: (Math.random() - 0.5) * 0.6,
      r: Math.random() * 2 + 0.8,
      o: Math.random() * 0.45 + 0.1,
      life: Math.random() * 200,
    }));

    function tick() {
      ctx.clearRect(0, 0, W, H);
      const pts = pRef.current;

      pts.forEach((p) => {
        p.life++;
        if (mode === "orbit") {
          const cx = W / 2,
            cy = H / 2;
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
        ctx.fillStyle =
          color +
          Math.round(p.o * 255)
            .toString(16)
            .padStart(2, "0");
        ctx.fill();
      });

      if (mode === "network") {
        for (let i = 0; i < pts.length; i++) {
          for (let j = i + 1; j < pts.length; j++) {
            const dx = pts[i].x - pts[j].x,
              dy = pts[i].y - pts[j].y;
            const d = Math.sqrt(dx * dx + dy * dy);
            if (d < 115) {
              ctx.beginPath();
              ctx.moveTo(pts[i].x, pts[i].y);
              ctx.lineTo(pts[j].x, pts[j].y);
              ctx.strokeStyle =
                color +
                Math.round((1 - d / 115) * 38)
                  .toString(16)
                  .padStart(2, "0");
              ctx.lineWidth = 0.4;
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
    <canvas
      ref={canvasRef}
      style={{
        position: "absolute",
        inset: 0,
        width: "100%",
        height: "100%",
        pointerEvents: "none",
        opacity: active ? 1 : 0,
        transition: "opacity 0.8s",
      }}
    />
  );
}

// ═══════════════════════════════════════════════
// SHARED UI ATOMS
// ═══════════════════════════════════════════════
function AnimatedEntry({ children, entered, delay = 0, style = {} }) {
  return (
    <div
      style={{
        opacity: entered ? 1 : 0,
        transform: entered ? "translateY(0)" : "translateY(20px)",
        transition: `all 0.6s ${delay}s cubic-bezier(0.22,1,0.36,1)`,
        ...style,
      }}
    >
      {children}
    </div>
  );
}

function BackBtn({ onClick }) {
  return (
    <button
      onClick={onClick}
      style={{
        background: "none",
        border: `1px solid ${T.border}`,
        color: T.textMuted,
        fontSize: 12,
        cursor: "pointer",
        fontFamily: T.fontDisplay,
        marginBottom: 24,
        display: "flex",
        alignItems: "center",
        gap: 6,
        padding: "6px 14px",
        borderRadius: 20,
        letterSpacing: 1,
      }}
    >
      ← Back
    </button>
  );
}

function SectionHeader({ page, entered }) {
  return (
    <div
      style={{
        textAlign: "center",
        marginBottom: 40,
        opacity: entered ? 1 : 0,
        transform: entered ? "translateY(0)" : "translateY(24px)",
        transition: "all 0.7s cubic-bezier(0.22,1,0.36,1)",
      }}
    >
      <div
        style={{
          width: 60,
          height: 60,
          borderRadius: "50%",
          background: hexAlpha(page.theme.color, 0.08),
          border: `2px solid ${hexAlpha(page.theme.color, 0.25)}`,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 26,
          margin: "0 auto 16px",
          boxShadow: `0 0 36px ${page.colorGlow}`,
        }}
      >
        {page.icon}
      </div>
      <div
        style={{
          fontSize: 10,
          fontFamily: T.fontDisplay,
          fontWeight: 600,
          color: page.theme.color,
          letterSpacing: 2.5,
          textTransform: "uppercase",
          marginBottom: 6,
        }}
      >
        {DECK.brand}
      </div>
      <h1
        style={{
          fontFamily: T.fontDisplay,
          fontSize: 40,
          fontWeight: 700,
          color: T.text,
          margin: "0 0 6px",
          letterSpacing: -0.5,
        }}
      >
        {page.headline || page.title}
      </h1>
      {page.subheadline || page.subtitle ? (
        <p
          style={{
            fontSize: 15,
            color: page.theme.light,
            fontStyle: "italic",
            margin: 0,
          }}
        >
          {page.subheadline || page.subtitle}
        </p>
      ) : null}
      <div
        style={{
          width: 64,
          height: 3,
          background: `linear-gradient(90deg,${page.theme.color},${page.theme.light})`,
          margin: "18px auto 0",
          borderRadius: 2,
        }}
      />
    </div>
  );
}

function Callout({ page, text, entered, delay = 0.9 }) {
  return (
    <div
      style={{
        textAlign: "center",
        marginTop: 32,
        padding: "22px 24px",
        borderTop: `1px solid ${hexAlpha(page.theme.color, 0.12)}`,
        borderBottom: `1px solid ${hexAlpha(page.theme.color, 0.12)}`,
        opacity: entered ? 1 : 0,
        transition: `opacity 0.8s ${delay}s`,
      }}
    >
      <p
        style={{
          fontSize: 15,
          color: T.textMuted,
          lineHeight: 1.65,
          margin: 0,
          maxWidth: 640,
          marginLeft: "auto",
          marginRight: "auto",
        }}
      >
        <span style={{ color: page.theme.light, fontWeight: 700 }}>
          "{text}"
        </span>
      </p>
    </div>
  );
}

function useEntrance() {
  const [entered, setEntered] = useState(false);
  useEffect(() => {
    const t = setTimeout(() => setEntered(true), 50);
    return () => clearTimeout(t);
  }, []);
  return entered;
}

function ScreenShell({ page, onBack, children, particleMode = "network" }) {
  const entered = useEntrance();
  return (
    <div
      style={{
        position: "relative",
        minHeight: "100vh",
        background: T.bg,
        overflow: "hidden",
      }}
    >
      <Particles color={page.theme.color} mode={particleMode} active={entered} />
      <div
        style={{
          position: "relative",
          zIndex: 2,
          maxWidth: 960,
          margin: "0 auto",
          padding: "48px 32px",
          opacity: entered ? 1 : 0,
          transform: entered ? "none" : "translateY(30px)",
          transition: "all 0.8s cubic-bezier(0.22,1,0.36,1)",
        }}
      >
        <BackBtn onClick={onBack} />
        <SectionHeader page={page} entered={entered} />
        {typeof children === "function" ? children(entered) : children}
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════
// SCREEN: STAT CARDS
// ═══════════════════════════════════════════════
function StatCardsScreen({ page, onBack }) {
  return (
    <ScreenShell page={page} onBack={onBack}>
      {(entered) => (
        <>
          {page.banner && (
            <AnimatedEntry entered={entered} delay={0.2}>
              <div
                style={{
                  background: hexAlpha(page.theme.color, 0.06),
                  border: `1px solid ${hexAlpha(page.theme.color, 0.15)}`,
                  borderLeft: `4px solid ${page.theme.color}`,
                  borderRadius: 8,
                  padding: "14px 22px",
                  marginBottom: 28,
                }}
              >
                <p
                  style={{
                    fontSize: 14,
                    color: "#CBD5E1",
                    lineHeight: 1.65,
                    margin: 0,
                  }}
                >
                  {page.banner}
                </p>
              </div>
            </AnimatedEntry>
          )}

          {(page.cards || []).map((c, i) => (
            <AnimatedEntry key={i} entered={entered} delay={0.3 + i * 0.15}>
              <div
                style={{
                  background: T.bgDeep,
                  borderRadius: 12,
                  padding: "26px 30px",
                  marginBottom: 18,
                  display: "flex",
                  alignItems: "flex-start",
                  gap: 22,
                  borderLeft: `4px solid ${page.theme.color}`,
                }}
              >
                <div style={{ flexShrink: 0, textAlign: "center", minWidth: 68 }}>
                  {c.stat && (
                    <div
                      style={{
                        fontFamily: T.fontDisplay,
                        fontSize: 30,
                        fontWeight: 700,
                        color: page.theme.light,
                        lineHeight: 1,
                      }}
                    >
                      {c.stat.value}
                    </div>
                  )}
                  {c.stat && (
                    <div
                      style={{
                        fontSize: 9,
                        color: T.textDim,
                        textTransform: "uppercase",
                        letterSpacing: 1,
                        marginTop: 3,
                      }}
                    >
                      {c.stat.label}
                    </div>
                  )}
                  {c.icon && !c.stat && (
                    <div style={{ fontSize: 28 }}>{c.icon}</div>
                  )}
                </div>
                <div>
                  <h3
                    style={{
                      fontFamily: T.fontDisplay,
                      fontSize: 17,
                      fontWeight: 700,
                      color: page.theme.light,
                      margin: "0 0 8px",
                    }}
                  >
                    {c.title}
                  </h3>
                  <p
                    style={{
                      fontSize: 14,
                      color: "#CBD5E1",
                      lineHeight: 1.65,
                      margin: 0,
                    }}
                  >
                    {c.body}
                  </p>
                </div>
              </div>
            </AnimatedEntry>
          ))}

          <Callout page={page} text={page.callout} entered={entered} />
        </>
      )}
    </ScreenShell>
  );
}

// ═══════════════════════════════════════════════
// SCREEN: BEFORE-AFTER
// ═══════════════════════════════════════════════
function BeforeAfterScreen({ page, onBack }) {
  return (
    <ScreenShell page={page} onBack={onBack}>
      {(entered) => (
        <>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: 18,
              maxWidth: 960,
              margin: "0 auto",
            }}
          >
            {(page.cards || []).map((c, i) => {
              const fromLeft = i % 2 === 0;
              return (
                <div
                  key={i}
                  style={{
                    background: T.bgDeep,
                    borderRadius: 12,
                    padding: "24px 26px",
                    borderLeft: `4px solid ${page.theme.color}`,
                    opacity: entered ? 1 : 0,
                    transform: entered
                      ? "translateX(0)"
                      : `translateX(${fromLeft ? "-30px" : "30px"})`,
                    transition: `all 0.6s ${0.3 + i * 0.12}s cubic-bezier(0.22,1,0.36,1)`,
                    backgroundImage: `radial-gradient(ellipse at ${fromLeft ? "left top" : "right top"}, ${hexAlpha(page.theme.color, 0.06)}, transparent 60%)`,
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: 10,
                      marginBottom: 16,
                    }}
                  >
                    <div
                      style={{
                        width: 28,
                        height: 28,
                        borderRadius: "50%",
                        background: hexAlpha(page.theme.color, 0.15),
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        fontSize: 12,
                        fontFamily: T.fontDisplay,
                        fontWeight: 700,
                        color: page.theme.light,
                      }}
                    >
                      {String(i + 1).padStart(2, "0")}
                    </div>
                    <h3
                      style={{
                        fontFamily: T.fontDisplay,
                        fontSize: 16,
                        fontWeight: 700,
                        color: page.theme.light,
                        margin: 0,
                      }}
                    >
                      {c.icon} {c.title}
                    </h3>
                  </div>

                  <div style={{ marginBottom: 14 }}>
                    <div
                      style={{
                        fontSize: 9,
                        fontFamily: T.fontDisplay,
                        fontWeight: 700,
                        color: "#EF4444",
                        letterSpacing: 1.5,
                        textTransform: "uppercase",
                        marginBottom: 4,
                      }}
                    >
                      Before
                    </div>
                    <p
                      style={{
                        fontSize: 13,
                        color: T.textMuted,
                        lineHeight: 1.6,
                        margin: 0,
                      }}
                    >
                      {c.before}
                    </p>
                  </div>

                  <div
                    style={{
                      height: 1,
                      background: `linear-gradient(90deg,${hexAlpha(page.theme.color, 0.2)},transparent)`,
                      marginBottom: 14,
                    }}
                  />

                  <div>
                    <div
                      style={{
                        fontSize: 9,
                        fontFamily: T.fontDisplay,
                        fontWeight: 700,
                        color: "#10B981",
                        letterSpacing: 1.5,
                        textTransform: "uppercase",
                        marginBottom: 4,
                      }}
                    >
                      After
                    </div>
                    <p
                      style={{
                        fontSize: 13,
                        color: "#CBD5E1",
                        lineHeight: 1.6,
                        margin: 0,
                      }}
                    >
                      {c.after}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>

          <Callout page={page} text={page.callout} entered={entered} />
        </>
      )}
    </ScreenShell>
  );
}

// ═══════════════════════════════════════════════
// SCREEN: PILLARS
// ═══════════════════════════════════════════════
function PillarsScreen({ page, onBack }) {
  const [entered, setEntered] = useState(false);
  const [step, setStep] = useState(0);
  useEffect(() => {
    const t = setTimeout(() => setEntered(true), 50);
    return () => clearTimeout(t);
  }, []);
  useEffect(() => {
    if (!entered) return;
    const timers = [0, 250, 500, 750].map((d, i) =>
      setTimeout(() => setStep(i + 1), 400 + d)
    );
    return () => timers.forEach(clearTimeout);
  }, [entered]);

  return (
    <div
      style={{
        position: "relative",
        minHeight: "100vh",
        background: T.bg,
        overflow: "hidden",
      }}
    >
      <Particles color={page.theme.color} mode="network" active={entered} />
      <div
        style={{ position: "absolute", inset: 0, pointerEvents: "none", overflow: "hidden" }}
      >
        {[...Array(6)].map((_, i) => (
          <div
            key={i}
            style={{
              position: "absolute",
              left: "-10%",
              top: `${12 + i * 14}%`,
              width: entered ? "120%" : "0%",
              height: 1,
              background: `linear-gradient(90deg,transparent,${hexAlpha(page.theme.color, 0.07)},transparent)`,
              transition: `width ${0.5 + i * 0.08}s ${0.15 + i * 0.05}s ease`,
            }}
          />
        ))}
      </div>
      <div style={{ position: "relative", zIndex: 2, padding: "40px 52px" }}>
        <BackBtn onClick={onBack} />
        <div
          style={{
            textAlign: "center",
            marginBottom: 36,
            opacity: entered ? 1 : 0,
            transition: "all 0.6s",
          }}
        >
          <div
            style={{
              fontSize: 10,
              fontFamily: T.fontDisplay,
              fontWeight: 600,
              color: page.theme.color,
              letterSpacing: 2.5,
              textTransform: "uppercase",
              marginBottom: 6,
            }}
          >
            {DECK.brand}
          </div>
          <h1
            style={{
              fontFamily: T.fontDisplay,
              fontSize: 40,
              fontWeight: 700,
              color: T.text,
              margin: "0 0 6px",
            }}
          >
            {page.headline || page.title}
          </h1>
          <p
            style={{
              fontSize: 14,
              color: page.theme.light,
              fontStyle: "italic",
              margin: 0,
            }}
          >
            {page.subtitle}
          </p>
        </div>

        <div
          style={{
            display: "flex",
            alignItems: "stretch",
            gap: 0,
            maxWidth: 1100,
            margin: "0 auto 24px",
            background: T.bgCard,
            borderRadius: 12,
            overflow: "hidden",
            border: `1px solid ${hexAlpha(page.theme.color, 0.09)}`,
          }}
        >
          {(page.pillars || []).map((p, i) => (
            <div
              key={i}
              style={{
                flex: 1,
                padding: "26px 22px",
                borderRight: `1px solid ${hexAlpha(page.theme.color, 0.07)}`,
                opacity: step > i ? 1 : 0,
                transform: step > i ? "none" : "translateY(14px)",
                transition: "all 0.5s cubic-bezier(0.22,1,0.36,1)",
              }}
            >
              <div style={{ fontSize: 26, marginBottom: 10 }}>{p.icon}</div>
              <h3
                style={{
                  fontFamily: T.fontDisplay,
                  fontSize: 13,
                  fontWeight: 700,
                  color: page.theme.light,
                  margin: "0 0 14px",
                  textTransform: "uppercase",
                  letterSpacing: 1,
                }}
              >
                {p.title}
              </h3>
              <div style={{ display: "flex", flexDirection: "column", gap: 7 }}>
                {p.items.map((item, j) => (
                  <div
                    key={j}
                    style={{ display: "flex", alignItems: "flex-start", gap: 8 }}
                  >
                    <div
                      style={{
                        width: 4,
                        height: 4,
                        borderRadius: "50%",
                        background: page.theme.color,
                        marginTop: 6,
                        flexShrink: 0,
                      }}
                    />
                    <p
                      style={{
                        fontSize: 12,
                        color: T.textMuted,
                        lineHeight: 1.55,
                        margin: 0,
                      }}
                    >
                      {item}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          ))}

          {page.results && (
            <div
              style={{
                flex: 1,
                padding: "26px 22px",
                background: `linear-gradient(135deg,${hexAlpha(page.theme.color, 0.07)},transparent)`,
                opacity:
                  step > (page.pillars?.length || 0) - 1 ? 1 : 0,
                transform:
                  step > (page.pillars?.length || 0) - 1
                    ? "none"
                    : "translateY(14px)",
                transition: "all 0.5s 0.2s cubic-bezier(0.22,1,0.36,1)",
              }}
            >
              <div style={{ fontSize: 26, marginBottom: 10 }}>🏆</div>
              <h3
                style={{
                  fontFamily: T.fontDisplay,
                  fontSize: 13,
                  fontWeight: 700,
                  color: page.theme.light,
                  margin: "0 0 14px",
                  textTransform: "uppercase",
                  letterSpacing: 1,
                }}
              >
                Results
              </h3>
              <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                {page.results.map((r, i) => (
                  <div
                    key={i}
                    style={{ display: "flex", alignItems: "baseline", gap: 8 }}
                  >
                    <div
                      style={{
                        fontFamily: T.fontDisplay,
                        fontSize: 24,
                        fontWeight: 700,
                        color: "#FBBF24",
                        lineHeight: 1,
                      }}
                    >
                      {r.val}
                    </div>
                    <p
                      style={{
                        fontSize: 11,
                        color: T.textMuted,
                        lineHeight: 1.45,
                        margin: 0,
                      }}
                    >
                      {r.label}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        <div
          style={{
            maxWidth: 1100,
            margin: "0 auto",
            background: T.bgDeep,
            borderLeft: `4px solid ${page.theme.color}`,
            borderRadius: 8,
            padding: "16px 24px",
            display: "flex",
            alignItems: "center",
            gap: 14,
            opacity: entered ? 1 : 0,
            transition: "opacity 0.6s 1.2s",
          }}
        >
          <div style={{ fontSize: 22, color: page.theme.color }}>⚡</div>
          <p style={{ fontSize: 13, color: "#CBD5E1", lineHeight: 1.6, margin: 0 }}>
            <strong style={{ color: page.theme.light }}>{page.callout}</strong>
          </p>
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════
// SCREEN: TIMELINE
// ═══════════════════════════════════════════════
function TimelineScreen({ page, onBack }) {
  const entered = useEntrance();
  const phases = page.phases || [];

  return (
    <div
      style={{
        position: "relative",
        minHeight: "100vh",
        background: T.bg,
        overflow: "hidden",
      }}
    >
      <Particles color={page.theme.color} mode="network" active={entered} />
      <div
        style={{
          position: "relative",
          zIndex: 2,
          padding: "48px 32px",
          maxWidth: 1100,
          margin: "0 auto",
        }}
      >
        <BackBtn onClick={onBack} />
        <SectionHeader page={page} entered={entered} />

        {/* Timeline track */}
        <div style={{ position: "relative", marginBottom: 32 }}>
          {/* Horizontal line */}
          <div
            style={{
              position: "absolute",
              top: 16,
              left: 0,
              right: 0,
              height: 2,
              background: hexAlpha(page.theme.color, 0.2),
              zIndex: 0,
            }}
          />
          {/* Animated progress line */}
          <div
            style={{
              position: "absolute",
              top: 16,
              left: 0,
              width: entered ? "100%" : "0%",
              height: 2,
              background: `linear-gradient(90deg,${page.theme.color},${page.theme.light})`,
              transition: "width 1.2s cubic-bezier(0.22,1,0.36,1) 0.3s",
              zIndex: 1,
            }}
          />

          {/* Phases */}
          <div
            style={{
              display: "grid",
              gridTemplateColumns: `repeat(${phases.length}, 1fr)`,
              gap: 16,
              position: "relative",
              zIndex: 2,
            }}
          >
            {phases.map((phase, pi) => (
              <div key={pi}>
                {/* Phase marker */}
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 10,
                    marginBottom: 20,
                    opacity: entered ? 1 : 0,
                    transform: entered ? "none" : "translateY(10px)",
                    transition: `all 0.5s ${0.4 + pi * 0.15}s cubic-bezier(0.22,1,0.36,1)`,
                  }}
                >
                  <div
                    style={{
                      width: 32,
                      height: 32,
                      borderRadius: "50%",
                      background: page.theme.color,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontSize: 14,
                      fontWeight: 700,
                      color: "#FFF",
                      fontFamily: T.fontDisplay,
                      boxShadow: `0 0 20px ${page.colorGlow}`,
                    }}
                  >
                    {pi + 1}
                  </div>
                  <div
                    style={{
                      fontSize: 12,
                      fontFamily: T.fontDisplay,
                      fontWeight: 700,
                      color: page.theme.light,
                      letterSpacing: 0.5,
                    }}
                  >
                    {phase.label}
                  </div>
                </div>

                {/* Phase cards */}
                <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                  {phase.cards.map((c, ci) => (
                    <div
                      key={ci}
                      style={{
                        background: T.bgDeep,
                        borderRadius: 10,
                        padding: "16px 18px",
                        borderLeft: `3px solid ${page.theme.color}`,
                        opacity: entered ? 1 : 0,
                        transform: entered ? "none" : "translateY(16px)",
                        transition: `all 0.5s ${0.5 + pi * 0.15 + ci * 0.1}s cubic-bezier(0.22,1,0.36,1)`,
                      }}
                    >
                      <div
                        style={{
                          display: "flex",
                          alignItems: "center",
                          gap: 8,
                          marginBottom: 6,
                        }}
                      >
                        {c.icon && <span style={{ fontSize: 16 }}>{c.icon}</span>}
                        <h4
                          style={{
                            fontFamily: T.fontDisplay,
                            fontSize: 14,
                            fontWeight: 700,
                            color: page.theme.light,
                            margin: 0,
                          }}
                        >
                          {c.title}
                        </h4>
                      </div>
                      <p
                        style={{
                          fontSize: 12,
                          color: T.textMuted,
                          lineHeight: 1.55,
                          margin: 0,
                        }}
                      >
                        {c.body}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        <Callout page={page} text={page.callout} entered={entered} />
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════
// SCREEN: SPRINT (figure-8 diagram)
// ═══════════════════════════════════════════════
function SprintScreen({ page, onBack }) {
  const canvasRef = useRef(null);
  const progressRef = useRef(0);
  const [entered, setEntered] = useState(false);
  useEffect(() => {
    const t = setTimeout(() => setEntered(true), 50);
    return () => clearTimeout(t);
  }, []);

  const sprint = page.sprint || {};
  const nodes = sprint.nodes || [];

  const W = 820,
    H = 400;
  const lcx = 255,
    rcx = 565,
    cy = 198,
    lrx = 194,
    rrx = 194,
    ry = 142;

  function fig8Pos(t) {
    if (t < 0.5) {
      const a = -Math.PI + t * 2 * Math.PI * 2;
      return { x: lcx + lrx * Math.cos(a), y: cy + ry * Math.sin(a) };
    } else {
      const a = Math.PI - (t - 0.5) * 2 * Math.PI * 2;
      return { x: rcx + rrx * Math.cos(a), y: cy + ry * Math.sin(a) };
    }
  }

  const nodePositions = nodes.map((n, i) => ({
    ...n,
    ...fig8Pos(i / nodes.length),
    i,
  }));

  useEffect(() => {
    const c = canvasRef.current;
    if (!c) return;
    const ctx = c.getContext("2d");
    c.width = W * 2;
    c.height = H * 2;
    ctx.scale(2, 2);
    let raf;
    function draw() {
      progressRef.current = (progressRef.current + 0.0007) % 1;
      const prog = progressRef.current;
      ctx.clearRect(0, 0, W, H);
      ctx.beginPath();
      for (let i = 0; i <= 300; i++) {
        const p = fig8Pos(i / 300);
        i === 0 ? ctx.moveTo(p.x, p.y) : ctx.lineTo(p.x, p.y);
      }
      ctx.closePath();
      ctx.strokeStyle = hexAlpha(page.theme.color, 0.12);
      ctx.lineWidth = 2;
      ctx.stroke();
      const tl = 0.055;
      for (let i = 0; i < 44; i++) {
        const tt = ((prog - (i / 44) * tl + 1) % 1);
        const p = fig8Pos(tt);
        ctx.beginPath();
        ctx.arc(p.x, p.y, 4.2 - i * 0.08, 0, Math.PI * 2);
        ctx.fillStyle =
          page.theme.color +
          Math.round((1 - i / 44) * 0.5 * 255)
            .toString(16)
            .padStart(2, "0");
        ctx.fill();
      }
      const lead = fig8Pos(prog);
      ctx.beginPath();
      ctx.arc(lead.x, lead.y, 6, 0, Math.PI * 2);
      ctx.fillStyle = page.theme.light;
      ctx.shadowColor = page.theme.color;
      ctx.shadowBlur = 16;
      ctx.fill();
      ctx.shadowBlur = 0;
      raf = requestAnimationFrame(draw);
    }
    if (entered) draw();
    return () => cancelAnimationFrame(raf);
  }, [entered, page.theme.color, page.theme.light]);

  return (
    <div
      style={{
        position: "relative",
        minHeight: "100vh",
        background: T.bg,
        overflow: "hidden",
      }}
    >
      <Particles color={page.theme.color} mode="orbit" active={entered} />
      <div style={{ position: "relative", zIndex: 2, padding: "40px 52px" }}>
        <BackBtn onClick={onBack} />
        <div
          style={{
            textAlign: "center",
            marginBottom: 24,
            opacity: entered ? 1 : 0,
            transition: "all 0.6s",
          }}
        >
          <div
            style={{
              fontSize: 10,
              fontFamily: T.fontDisplay,
              fontWeight: 600,
              color: page.theme.color,
              letterSpacing: 2.5,
              textTransform: "uppercase",
              marginBottom: 6,
            }}
          >
            {DECK.brand}
          </div>
          <h1
            style={{
              fontFamily: T.fontDisplay,
              fontSize: 38,
              fontWeight: 700,
              color: T.text,
              margin: "0 0 6px",
            }}
          >
            {page.title}
          </h1>
          <p
            style={{
              fontSize: 14,
              color: page.theme.light,
              fontStyle: "italic",
              margin: "0 0 16px",
            }}
          >
            {page.subtitle}
          </p>
          <div style={{ display: "flex", justifyContent: "center", gap: 20 }}>
            {[
              ["#0891B2", "👤 Human Checkpoint"],
              [T.aiBg, "🤖 AI Step"],
            ].map(([bg, label], i) => (
              <div
                key={i}
                style={{ display: "flex", alignItems: "center", gap: 6 }}
              >
                <div
                  style={{
                    width: 8,
                    height: 8,
                    borderRadius: "50%",
                    background: i === 0 ? "#0891B2" : "#7C3AED",
                  }}
                />
                <span
                  style={{
                    fontSize: 11,
                    color: T.textMuted,
                    fontFamily: T.fontDisplay,
                  }}
                >
                  {label}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div
          style={{
            background: T.bgCard,
            borderRadius: 14,
            padding: "24px 16px",
            border: `1px solid ${hexAlpha(page.theme.color, 0.08)}`,
            maxWidth: 880,
            margin: "0 auto",
            boxShadow: "0 4px 40px rgba(0,0,0,0.35)",
            overflow: "hidden",
          }}
        >
          <div style={{ position: "relative", width: W, height: H, margin: "0 auto" }}>
            <canvas
              ref={canvasRef}
              style={{ position: "absolute", inset: 0, width: W, height: H }}
            />
            <div
              style={{
                position: "absolute",
                left: lcx - 46,
                top: 10,
                fontSize: 9,
                textTransform: "uppercase",
                letterSpacing: 1.5,
                fontWeight: 700,
                color: page.theme.color,
                fontFamily: T.fontDisplay,
              }}
            >
              {sprint.phase1Label || "Phase 1 — Build"}
            </div>
            <div
              style={{
                position: "absolute",
                left: rcx - 52,
                top: 10,
                fontSize: 9,
                textTransform: "uppercase",
                letterSpacing: 1.5,
                fontWeight: 700,
                color: "#0891B2",
                fontFamily: T.fontDisplay,
              }}
            >
              {sprint.phase2Label || "Phase 2 — Validate"}
            </div>
            <div
              style={{
                position: "absolute",
                left: (lcx + rcx) / 2 - 26,
                top: cy - 10,
                background: T.bg,
                border: `1px solid ${hexAlpha(page.theme.color, 0.2)}`,
                borderRadius: 8,
                padding: "3px 10px",
                fontSize: 8,
                color: page.theme.light,
                fontWeight: 700,
                textTransform: "uppercase",
                letterSpacing: 1,
                fontFamily: T.fontDisplay,
                zIndex: 6,
              }}
            >
              {sprint.handoffLabel || "Handoff"}
            </div>
            {nodePositions.map((n, i) => {
              const isAI = n.type === "ai";
              const sz = 25;
              return (
                <div
                  key={i}
                  style={{
                    position: "absolute",
                    left: n.x - sz,
                    top: n.y - sz,
                    width: sz * 2,
                    height: sz * 2,
                    borderRadius: "50%",
                    background: isAI ? T.aiBg : T.bgDeep,
                    border: `2px solid ${isAI ? "#7C3AED50" : "#0891B250"}`,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 16,
                    zIndex: 5,
                    opacity: entered ? 1 : 0,
                    transform: entered ? "scale(1)" : "scale(0.6)",
                    transition: `all 0.4s ${0.12 + i * 0.055}s cubic-bezier(0.34,1.56,0.64,1)`,
                  }}
                >
                  {n.icon}
                  <div
                    style={{
                      position: "absolute",
                      top: -5,
                      right: -5,
                      fontSize: 6,
                      fontWeight: 700,
                      background: isAI ? "#7C3AED" : "#0891B2",
                      color: "#FFF",
                      borderRadius: 4,
                      padding: "1px 4px",
                      fontFamily: T.fontDisplay,
                    }}
                  >
                    {isAI ? "AI" : "👤"}
                  </div>
                  <div
                    style={{
                      position: "absolute",
                      top: sz * 2 + 5,
                      fontSize: 8,
                      color: isAI ? page.theme.light : T.textMuted,
                      textAlign: "center",
                      whiteSpace: "nowrap",
                      fontFamily: T.fontDisplay,
                      fontWeight: 600,
                    }}
                  >
                    {n.label}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div
          style={{
            marginTop: 20,
            background: T.bgDeep,
            borderRadius: 8,
            padding: "14px 24px",
            borderLeft: `4px solid ${page.theme.color}`,
            display: "flex",
            alignItems: "center",
            gap: 14,
            maxWidth: 880,
            marginLeft: "auto",
            marginRight: "auto",
            opacity: entered ? 1 : 0,
            transition: "opacity 0.6s 1.2s",
          }}
        >
          <span style={{ fontSize: 20, color: page.theme.color }}>⟳</span>
          <p style={{ fontSize: 13, color: "#CBD5E1", lineHeight: 1.6, margin: 0 }}>
            <strong style={{ color: page.theme.light }}>{page.callout}</strong>
          </p>
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════
// SCREEN: RESULTS (metrics grid)
// ═══════════════════════════════════════════════
function ResultsScreen({ page, onBack }) {
  const entered = useEntrance();
  return (
    <div
      style={{
        position: "relative",
        minHeight: "100vh",
        background: T.bg,
        overflow: "hidden",
      }}
    >
      <Particles color={page.theme.color} mode="network" active={entered} />
      <div
        style={{
          position: "absolute",
          top: "38%",
          left: "50%",
          width: entered ? "130%" : "0%",
          height: 1,
          background: `linear-gradient(90deg,transparent,${hexAlpha(page.theme.color, 0.15)},transparent)`,
          transform: "translateX(-50%)",
          transition: "width 1.1s cubic-bezier(0.22,1,0.36,1)",
        }}
      />
      <div
        style={{
          position: "relative",
          zIndex: 2,
          padding: "48px 52px",
        }}
      >
        <BackBtn onClick={onBack} />
        <SectionHeader page={page} entered={entered} />

        <div
          style={{
            display: "grid",
            gridTemplateColumns: `repeat(${Math.min((page.metrics || []).length, 4)}, 1fr)`,
            gap: 16,
            maxWidth: 960,
            margin: "0 auto 36px",
          }}
        >
          {(page.metrics || []).map((m, i) => (
            <div
              key={i}
              style={{
                background: T.bgDeep,
                borderRadius: 12,
                padding: "28px 20px",
                textAlign: "center",
                border: `1px solid ${hexAlpha(m.color || page.theme.color, 0.15)}`,
                opacity: entered ? 1 : 0,
                transform: entered ? "scale(1)" : "scale(0.85)",
                transition: `all 0.5s ${0.25 + i * 0.1}s cubic-bezier(0.22,1,0.36,1)`,
              }}
            >
              <div style={{ fontSize: 28, marginBottom: 8 }}>{m.icon}</div>
              <div
                style={{
                  fontFamily: T.fontDisplay,
                  fontSize: 36,
                  fontWeight: 700,
                  color: m.color || page.theme.light,
                  lineHeight: 1,
                  marginBottom: 8,
                }}
              >
                {m.value}
              </div>
              <p
                style={{
                  fontSize: 12,
                  color: T.textMuted,
                  lineHeight: 1.5,
                  margin: 0,
                }}
              >
                {m.label}
              </p>
            </div>
          ))}
        </div>

        {page.cards && (
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: 18,
              maxWidth: 960,
              margin: "0 auto",
            }}
          >
            {page.cards.map((c, i) => (
              <div
                key={i}
                style={{
                  background: T.bgDeep,
                  borderRadius: 10,
                  padding: "24px 26px",
                  borderLeft: `4px solid ${page.theme.color}`,
                  opacity: entered ? 1 : 0,
                  transform: entered ? "none" : "translateY(18px)",
                  transition: `all 0.5s ${0.55 + i * 0.12}s cubic-bezier(0.22,1,0.36,1)`,
                }}
              >
                <h3
                  style={{
                    fontFamily: T.fontDisplay,
                    fontSize: 16,
                    fontWeight: 700,
                    color: page.theme.light,
                    margin: "0 0 8px",
                  }}
                >
                  {c.title}
                </h3>
                <p
                  style={{
                    fontSize: 13.5,
                    color: "#CBD5E1",
                    lineHeight: 1.65,
                    margin: 0,
                  }}
                >
                  {c.body}
                </p>
              </div>
            ))}
          </div>
        )}

        <Callout page={page} text={page.callout} entered={entered} delay={1} />
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════
// SCREEN: PERSONAS
// ═══════════════════════════════════════════════
function PersonasScreen({ page, onBack }) {
  const entered = useEntrance();
  const cards = page.cards || [];
  const cols = cards.length <= 4 ? 2 : 3;

  return (
    <ScreenShell page={page} onBack={onBack}>
      {(ent) => (
        <>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: `repeat(${cols}, 1fr)`,
              gap: 18,
              maxWidth: 960,
              margin: "0 auto",
            }}
          >
            {cards.map((c, i) => (
              <div
                key={i}
                style={{
                  position: "relative",
                  background: T.bgDeep,
                  borderRadius: 12,
                  padding: "28px 24px",
                  borderLeft: `4px solid ${page.theme.color}`,
                  opacity: entered ? 1 : 0,
                  transform: entered ? "scale(1)" : "scale(0.88)",
                  transition: `all 0.5s ${0.25 + i * 0.1}s cubic-bezier(0.34,1.56,0.64,1)`,
                  cursor: "default",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = "translateY(-4px) scale(1.01)";
                  e.currentTarget.style.boxShadow = `0 8px 32px ${page.colorGlow}`;
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = "scale(1)";
                  e.currentTarget.style.boxShadow = "none";
                }}
              >
                {c.stat && (
                  <div
                    style={{
                      position: "absolute",
                      top: 16,
                      right: 16,
                      textAlign: "center",
                    }}
                  >
                    <div
                      style={{
                        fontFamily: T.fontDisplay,
                        fontSize: 22,
                        fontWeight: 700,
                        color: page.theme.light,
                        lineHeight: 1,
                      }}
                    >
                      {c.stat.value}
                    </div>
                    <div
                      style={{
                        fontSize: 8,
                        color: T.textDim,
                        textTransform: "uppercase",
                        letterSpacing: 0.8,
                        marginTop: 2,
                      }}
                    >
                      {c.stat.label}
                    </div>
                  </div>
                )}

                <div style={{ fontSize: 32, marginBottom: 12 }}>{c.icon}</div>
                <h3
                  style={{
                    fontFamily: T.fontDisplay,
                    fontSize: 17,
                    fontWeight: 700,
                    color: page.theme.light,
                    margin: "0 0 16px",
                  }}
                >
                  {c.title}
                </h3>

                <div style={{ marginBottom: 14 }}>
                  <div
                    style={{
                      fontSize: 9,
                      fontFamily: T.fontDisplay,
                      fontWeight: 700,
                      color: "#EF444499",
                      letterSpacing: 1.5,
                      textTransform: "uppercase",
                      marginBottom: 4,
                    }}
                  >
                    Pain Point
                  </div>
                  <p
                    style={{
                      fontSize: 13,
                      color: T.textMuted,
                      lineHeight: 1.6,
                      margin: 0,
                    }}
                  >
                    {c.pain}
                  </p>
                </div>

                <div
                  style={{
                    height: 1,
                    background: `linear-gradient(90deg,${hexAlpha(page.theme.color, 0.2)},transparent)`,
                    marginBottom: 14,
                  }}
                />

                <div>
                  <div
                    style={{
                      fontSize: 9,
                      fontFamily: T.fontDisplay,
                      fontWeight: 700,
                      color: "#10B98199",
                      letterSpacing: 1.5,
                      textTransform: "uppercase",
                      marginBottom: 4,
                    }}
                  >
                    With AI
                  </div>
                  <p
                    style={{
                      fontSize: 13,
                      color: "#CBD5E1",
                      lineHeight: 1.6,
                      margin: 0,
                    }}
                  >
                    {c.gain}
                  </p>
                </div>
              </div>
            ))}
          </div>

          <Callout page={page} text={page.callout} entered={entered} />
        </>
      )}
    </ScreenShell>
  );
}

// ═══════════════════════════════════════════════
// SCREEN: COMPARISON
// ═══════════════════════════════════════════════
function ComparisonScreen({ page, onBack }) {
  const entered = useEntrance();
  const comp = page.comparison || {};
  const columns = comp.columns || [];
  const rows = comp.rows || [];

  function scoreColor(score) {
    const s = score.toLowerCase();
    if (s === "strong" || s === "very large" || s === "available") return "#10B981";
    if (s === "medium" || s === "large" || s === "in progress" || s === "$$") return "#FBBF24";
    if (s === "basic" || s === "limited" || s === "cli-based") return T.textMuted;
    if (s === "$$$") return "#F59E0B";
    return T.textMuted;
  }

  return (
    <ScreenShell page={page} onBack={onBack}>
      {(ent) => (
        <>
          <div
            style={{
              maxWidth: 1000,
              margin: "0 auto",
              background: T.bgCard,
              borderRadius: 12,
              overflow: "hidden",
              border: `1px solid ${hexAlpha(page.theme.color, 0.12)}`,
            }}
          >
            {/* Header row */}
            <div
              style={{
                display: "grid",
                gridTemplateColumns: `180px repeat(${columns.length}, 1fr)`,
                background: hexAlpha(page.theme.color, 0.06),
                borderBottom: `1px solid ${hexAlpha(page.theme.color, 0.12)}`,
                position: "sticky",
                top: 0,
                zIndex: 3,
              }}
            >
              <div
                style={{
                  padding: "16px 20px",
                  fontFamily: T.fontDisplay,
                  fontSize: 11,
                  fontWeight: 700,
                  color: T.textDim,
                  letterSpacing: 1,
                  textTransform: "uppercase",
                }}
              >
                Criteria
              </div>
              {columns.map((col, i) => (
                <div
                  key={i}
                  style={{
                    padding: "16px 12px",
                    textAlign: "center",
                    opacity: entered ? 1 : 0,
                    transform: entered ? "none" : "translateY(-10px)",
                    transition: `all 0.4s ${0.2 + i * 0.08}s cubic-bezier(0.22,1,0.36,1)`,
                  }}
                >
                  <div style={{ fontSize: 20, marginBottom: 4 }}>{col.icon}</div>
                  <div
                    style={{
                      fontFamily: T.fontDisplay,
                      fontSize: 11,
                      fontWeight: 700,
                      color: page.theme.light,
                      letterSpacing: 0.3,
                    }}
                  >
                    {col.label}
                  </div>
                </div>
              ))}
            </div>

            {/* Body rows */}
            {rows.map((row, ri) => (
              <div
                key={ri}
                style={{
                  display: "grid",
                  gridTemplateColumns: `180px repeat(${columns.length}, 1fr)`,
                  background: ri % 2 === 0 ? "transparent" : hexAlpha(page.theme.color, 0.02),
                  borderBottom: `1px solid ${T.border}`,
                  opacity: entered ? 1 : 0,
                  transform: entered ? "none" : "translateY(12px)",
                  transition: `all 0.4s ${0.35 + ri * 0.08}s cubic-bezier(0.22,1,0.36,1)`,
                }}
              >
                <div
                  style={{
                    padding: "14px 20px",
                    fontFamily: T.fontDisplay,
                    fontSize: 13,
                    fontWeight: 600,
                    color: T.text,
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  {row.criteria}
                </div>
                {row.scores.map((score, si) => (
                  <div
                    key={si}
                    style={{
                      padding: "14px 12px",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                  >
                    <span
                      style={{
                        display: "inline-block",
                        padding: "4px 12px",
                        borderRadius: 6,
                        fontSize: 12,
                        fontWeight: 600,
                        fontFamily: T.fontDisplay,
                        color: scoreColor(score),
                        background: hexToGlow(scoreColor(score), 0.1),
                        border: `1px solid ${hexToGlow(scoreColor(score), 0.2)}`,
                      }}
                    >
                      {score}
                    </span>
                  </div>
                ))}
              </div>
            ))}
          </div>

          <Callout page={page} text={page.callout} entered={entered} />
        </>
      )}
    </ScreenShell>
  );
}

// ═══════════════════════════════════════════════
// LANDING TILE
// ═══════════════════════════════════════════════
function LandingTile({ page, onClick, hovered, onHover }) {
  const h = hovered === page.id;
  return (
    <div
      onClick={onClick}
      onMouseEnter={() => onHover(page.id)}
      onMouseLeave={() => onHover(null)}
      style={{
        flex: 1,
        position: "relative",
        cursor: "pointer",
        overflow: "hidden",
        borderRadius: 14,
        padding: "30px 26px",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        minHeight: 290,
        background: T.bgCard,
        border: `1px solid ${h ? hexAlpha(page.theme.color, 0.33) : T.border}`,
        boxShadow: h
          ? `0 0 44px ${page.colorGlow}, 0 8px 32px rgba(0,0,0,0.4)`
          : "0 4px 20px rgba(0,0,0,0.3)",
        transform: h ? "translateY(-7px) scale(1.015)" : "translateY(0) scale(1)",
        transition: "all 0.38s cubic-bezier(0.34,1.56,0.64,1)",
      }}
    >
      <div
        style={{
          position: "absolute",
          top: 0,
          right: 0,
          width: 70,
          height: 70,
          background: `linear-gradient(225deg,${hexAlpha(page.theme.color, 0.08)},transparent)`,
          borderRadius: "0 14px 0 0",
        }}
      />
      <div>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 8,
            marginBottom: 12,
          }}
        >
          <span
            style={{
              fontSize: 11,
              fontFamily: T.fontDisplay,
              fontWeight: 600,
              color: page.theme.color,
              letterSpacing: 2,
              textTransform: "uppercase",
              opacity: 0.75,
            }}
          >
            {page.num}
          </span>
          <div
            style={{
              flex: 1,
              height: 1,
              background: `linear-gradient(90deg,${hexAlpha(page.theme.color, 0.16)},transparent)`,
            }}
          />
        </div>
        <div
          style={{
            fontSize: 34,
            marginBottom: 10,
            lineHeight: 1,
            filter: h ? `drop-shadow(0 0 10px ${page.colorGlow})` : "none",
            transition: "filter 0.35s",
          }}
        >
          {page.icon}
        </div>
        <h2
          style={{
            fontFamily: T.fontDisplay,
            fontSize: 20,
            fontWeight: 700,
            color: T.text,
            lineHeight: 1.2,
            margin: "0 0 6px",
          }}
        >
          {page.title}
        </h2>
        <p style={{ fontSize: 12, color: T.textMuted, lineHeight: 1.5, margin: 0 }}>
          {page.subtitle}
        </p>
      </div>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 6,
          marginTop: 18,
          color: page.theme.color,
          fontSize: 11,
          fontWeight: 700,
          fontFamily: T.fontDisplay,
          letterSpacing: 1,
          textTransform: "uppercase",
          transform: h ? "translateX(5px)" : "translateX(0)",
          transition: "transform 0.25s",
        }}
      >
        Explore <span style={{ fontSize: 14 }}>→</span>
      </div>
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          height: 2,
          background: `linear-gradient(90deg,${page.theme.color},${page.theme.light})`,
          opacity: h ? 1 : 0.3,
          transition: "opacity 0.3s",
        }}
      />
    </div>
  );
}

// ═══════════════════════════════════════════════
// ROUTER
// ═══════════════════════════════════════════════
function ScreenRouter({ page, onBack }) {
  switch (page.layout) {
    case "stat-cards":
      return <StatCardsScreen page={page} onBack={onBack} />;
    case "before-after":
      return <BeforeAfterScreen page={page} onBack={onBack} />;
    case "pillars":
      return <PillarsScreen page={page} onBack={onBack} />;
    case "timeline":
      return <TimelineScreen page={page} onBack={onBack} />;
    case "sprint":
      return <SprintScreen page={page} onBack={onBack} />;
    case "results":
      return <ResultsScreen page={page} onBack={onBack} />;
    case "personas":
      return <PersonasScreen page={page} onBack={onBack} />;
    case "comparison":
      return <ComparisonScreen page={page} onBack={onBack} />;
    default:
      return <StatCardsScreen page={page} onBack={onBack} />;
  }
}

// ═══════════════════════════════════════════════
// APP ROOT
// ═══════════════════════════════════════════════
export default function App() {
  const [active, setActive] = useState(null);
  const [transitioning, setTransitioning] = useState(false);
  const [hovered, setHovered] = useState(null);

  const go = (id) => {
    setTransitioning(true);
    setTimeout(() => {
      setActive(id);
      setTransitioning(false);
    }, 380);
  };
  const back = () => {
    setTransitioning(true);
    setTimeout(() => {
      setActive(null);
      setTransitioning(false);
    }, 340);
  };

  const activePage = PAGES.find((p) => p.id === active);
  const gradient = `linear-gradient(90deg, ${DECK.accentGradient[0]}, ${DECK.accentGradient[1]})`;

  return (
    <div
      style={{
        fontFamily: T.fontBody,
        minHeight: "100vh",
        background: T.bg,
        opacity: transitioning ? 0 : 1,
        transition: "opacity 0.32s ease",
      }}
    >
      <link href={T.googleFontsUrl} rel="stylesheet" />

      {!active && (
        <div
          style={{
            minHeight: "100vh",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            padding: "40px 52px",
          }}
        >
          <div style={{ marginBottom: 36 }}>
            <div
              style={{
                fontSize: 10,
                textTransform: "uppercase",
                letterSpacing: 3,
                color: T.textDim,
                fontFamily: T.fontDisplay,
                fontWeight: 600,
                marginBottom: 8,
              }}
            >
              {DECK.brand}
            </div>
            <h1
              style={{
                fontFamily: T.fontDisplay,
                fontSize: 44,
                fontWeight: 700,
                color: T.text,
                margin: "0 0 10px",
                letterSpacing: -1,
                lineHeight: 1.06,
              }}
            >
              {DECK.title}
              <br />
              <span
                style={{
                  background: gradient,
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                }}
              >
                {DECK.titleAccent}
              </span>
            </h1>
            <p
              style={{
                fontSize: 14,
                color: T.textMuted,
                margin: 0,
                maxWidth: 560,
              }}
            >
              {DECK.tagline}
            </p>
          </div>

          <div style={{ display: "flex", gap: 16, marginBottom: 32, flexWrap: "wrap" }}>
            {PAGES.map((p) => (
              <LandingTile
                key={p.id}
                page={p}
                onClick={() => go(p.id)}
                hovered={hovered}
                onHover={setHovered}
              />
            ))}
          </div>

          <div
            style={{
              display: "flex",
              gap: 0,
              paddingTop: 22,
              borderTop: `1px solid ${T.border}`,
              flexWrap: "wrap",
            }}
          >
            {DECK.stats.map((s, i) => (
              <div
                key={i}
                style={{
                  paddingRight: 32,
                  borderRight:
                    i < DECK.stats.length - 1 ? `1px solid ${T.border}` : "none",
                  marginRight: i < DECK.stats.length - 1 ? 32 : 0,
                }}
              >
                <div
                  style={{
                    fontFamily: T.fontDisplay,
                    fontSize: 22,
                    fontWeight: 700,
                    color: DECK.accentGradient[0],
                  }}
                >
                  {s.val}
                </div>
                <div
                  style={{
                    fontSize: 9,
                    color: T.textDim,
                    textTransform: "uppercase",
                    letterSpacing: 0.8,
                    marginTop: 2,
                  }}
                >
                  {s.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {active && activePage && <ScreenRouter page={activePage} onBack={back} />}
    </div>
  );
}
