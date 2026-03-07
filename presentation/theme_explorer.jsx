import { useState, useEffect, useRef } from "react";

// ═══════════════════════════════════════════════════════════
// THEME EXPLORER — 6 Alternative Themes for Advocacy Deck
// ═══════════════════════════════════════════════════════════

const THEMES = [
  {
    id: "obsidian-ember",
    name: "Obsidian & Ember",
    vibe: "Editorial / Luxury Dark",
    description: "Matte charcoal surfaces with warm amber accents. Feels like a high-end consulting report printed on heavy stock. The serif display font adds gravitas without feeling stuffy.",
    fontDisplay: "'Playfair Display', serif",
    fontBody: "'Source Sans 3', sans-serif",
    fontsUrl: "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Source+Sans+3:wght@400;500;600;700&display=swap",
    bg: "#1A1A1E",
    bgCard: "#242428",
    bgDeep: "#2C2C32",
    text: "#E8E4DF",
    textMuted: "#9B9590",
    textDim: "#6B6560",
    border: "rgba(232,228,223,0.06)",
    accent: "#D4A853",
    accentLight: "#E8C97A",
    accentGlow: "rgba(212,168,83,0.25)",
    secondary: "#C75B39",
    secondaryLight: "#E07A58",
    gradient: ["#D4A853", "#C75B39"],
    pageColors: [
      { color: "#D4A853", light: "#E8C97A" },
      { color: "#C75B39", light: "#E07A58" },
      { color: "#5B8A72", light: "#7AB096" },
      { color: "#8B7EC8", light: "#A99ADD" },
    ],
    particleStyle: "network",
    cardBorderStyle: "left",
  },
  {
    id: "arctic-steel",
    name: "Arctic Steel",
    vibe: "Industrial / Minimalist Nordic",
    description: "Cool blue-grays with electric ice-blue accents. Inspired by Scandinavian industrial design — everything has purpose, nothing is decorative. Monospace display font signals engineering precision.",
    fontDisplay: "'JetBrains Mono', monospace",
    fontBody: "'Nunito Sans', sans-serif",
    fontsUrl: "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700;800&family=Nunito+Sans:wght@400;500;600;700&display=swap",
    bg: "#0F1318",
    bgCard: "#171D24",
    bgDeep: "#1E2630",
    text: "#D6DDE6",
    textMuted: "#7B8EA3",
    textDim: "#4E6178",
    border: "rgba(123,142,163,0.08)",
    accent: "#4FC3F7",
    accentLight: "#81D4FA",
    accentGlow: "rgba(79,195,247,0.2)",
    secondary: "#FF6B6B",
    secondaryLight: "#FF9999",
    gradient: ["#4FC3F7", "#B2EBF2"],
    pageColors: [
      { color: "#4FC3F7", light: "#81D4FA" },
      { color: "#FF6B6B", light: "#FF9999" },
      { color: "#69F0AE", light: "#9FFFC8" },
      { color: "#FFD54F", light: "#FFE082" },
    ],
    particleStyle: "grid",
    cardBorderStyle: "top",
  },
  {
    id: "midnight-verdant",
    name: "Midnight Verdant",
    vibe: "Deep Navy / Organic Tech",
    description: "Rich midnight blue with living green accents — tech that breathes. Avoids the cold sterility of typical dark themes. The rounded body font adds warmth without losing professionalism.",
    fontDisplay: "'Outfit', sans-serif",
    fontBody: "'Karla', sans-serif",
    fontsUrl: "https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&family=Karla:wght@400;500;600;700&display=swap",
    bg: "#0A1628",
    bgCard: "#112240",
    bgDeep: "#152A4E",
    text: "#CCD6F6",
    textMuted: "#8892B0",
    textDim: "#5A6480",
    border: "rgba(100,255,218,0.07)",
    accent: "#64FFDA",
    accentLight: "#9EFFD8",
    accentGlow: "rgba(100,255,218,0.18)",
    secondary: "#F78166",
    secondaryLight: "#FFA28B",
    gradient: ["#64FFDA", "#48BB78"],
    pageColors: [
      { color: "#64FFDA", light: "#9EFFD8" },
      { color: "#F78166", light: "#FFA28B" },
      { color: "#BD93F9", light: "#D6B4FF" },
      { color: "#F1FA8C", light: "#F8FCB8" },
    ],
    particleStyle: "network",
    cardBorderStyle: "left",
  },
  {
    id: "warm-slate",
    name: "Warm Slate",
    vibe: "Sophisticated / Warm Professional",
    description: "Warm gray base with terracotta and sage accents. Reads as confident and approachable — ideal for client-facing advocacy where you need trust, not flash. Geometric display font keeps it modern.",
    fontDisplay: "'Sora', sans-serif",
    fontBody: "'Libre Franklin', sans-serif",
    fontsUrl: "https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Libre+Franklin:wght@400;500;600&display=swap",
    bg: "#1C1B1F",
    bgCard: "#272529",
    bgDeep: "#302E33",
    text: "#EDE8E3",
    textMuted: "#A39E98",
    textDim: "#6E6A65",
    border: "rgba(237,232,227,0.06)",
    accent: "#C17C5A",
    accentLight: "#D99B7A",
    accentGlow: "rgba(193,124,90,0.22)",
    secondary: "#7EA87E",
    secondaryLight: "#A0C8A0",
    gradient: ["#C17C5A", "#D99B7A"],
    pageColors: [
      { color: "#C17C5A", light: "#D99B7A" },
      { color: "#7EA87E", light: "#A0C8A0" },
      { color: "#6B8EC2", light: "#8CAEE0" },
      { color: "#C4A265", light: "#DABB85" },
    ],
    particleStyle: "float",
    cardBorderStyle: "left",
  },
  {
    id: "neon-noir",
    name: "Neon Noir",
    vibe: "Cyberpunk / High Contrast",
    description: "True black with vivid neon cyan and magenta. High-impact and unapologetic — grabs attention in crowded presentation contexts. Best for audiences that value boldness and forward-thinking positioning.",
    fontDisplay: "'Chakra Petch', sans-serif",
    fontBody: "'Barlow', sans-serif",
    fontsUrl: "https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=Barlow:wght@400;500;600&display=swap",
    bg: "#050508",
    bgCard: "#0D0D12",
    bgDeep: "#14141C",
    text: "#EAEAF0",
    textMuted: "#8585A0",
    textDim: "#55556E",
    border: "rgba(0,255,255,0.06)",
    accent: "#00E5FF",
    accentLight: "#66F0FF",
    accentGlow: "rgba(0,229,255,0.2)",
    secondary: "#FF2D95",
    secondaryLight: "#FF6EB4",
    gradient: ["#00E5FF", "#FF2D95"],
    pageColors: [
      { color: "#00E5FF", light: "#66F0FF" },
      { color: "#FF2D95", light: "#FF6EB4" },
      { color: "#AAFF00", light: "#CCFF66" },
      { color: "#B388FF", light: "#D1B3FF" },
    ],
    particleStyle: "orbit",
    cardBorderStyle: "top",
  },
  {
    id: "paper-ink",
    name: "Paper & Ink",
    vibe: "Light Editorial / Printcraft",
    description: "Inverts the dark paradigm entirely — warm off-white with deep charcoal type and ink-blue accents. Feels like a well-designed white paper or annual report. Stands out precisely because most tech decks go dark.",
    fontDisplay: "'DM Serif Display', serif",
    fontBody: "'Atkinson Hyperlegible', sans-serif",
    fontsUrl: "https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Atkinson+Hyperlegible:wght@400;700&display=swap",
    bg: "#FAF8F5",
    bgCard: "#FFFFFF",
    bgDeep: "#F0EDE8",
    text: "#1A1A2E",
    textMuted: "#5C5C6F",
    textDim: "#8E8E9F",
    border: "rgba(26,26,46,0.08)",
    accent: "#1E40AF",
    accentLight: "#3B5FC0",
    accentGlow: "rgba(30,64,175,0.12)",
    secondary: "#B45309",
    secondaryLight: "#D97706",
    gradient: ["#1E40AF", "#7C3AED"],
    pageColors: [
      { color: "#1E40AF", light: "#3B5FC0" },
      { color: "#B45309", light: "#D97706" },
      { color: "#047857", light: "#059669" },
      { color: "#7C3AED", light: "#8B5CF6" },
    ],
    particleStyle: "none",
    cardBorderStyle: "left",
  },
];

// ─── MINI PARTICLE CANVAS ───
function MiniParticles({ theme, style: particleStyle, active }) {
  const canvasRef = useRef(null);
  const animRef = useRef(null);
  const pRef = useRef([]);

  useEffect(() => {
    const c = canvasRef.current;
    if (!c || !active || particleStyle === "none") return;
    const ctx = c.getContext("2d");
    const rect = c.getBoundingClientRect();
    c.width = rect.width * 2;
    c.height = rect.height * 2;
    ctx.scale(2, 2);
    const W = rect.width, H = rect.height;
    const count = 18;

    pRef.current = Array.from({ length: count }, () => ({
      x: Math.random() * W, y: Math.random() * H,
      vx: (Math.random() - 0.5) * 0.4, vy: (Math.random() - 0.5) * 0.4,
      r: Math.random() * 1.5 + 0.5, o: Math.random() * 0.4 + 0.1, life: Math.random() * 200,
    }));

    function tick() {
      ctx.clearRect(0, 0, W, H);
      const pts = pRef.current;
      pts.forEach(p => {
        p.life++;
        if (particleStyle === "orbit") {
          const cx = W / 2, cy = H / 2;
          const a = Math.atan2(p.y - cy, p.x - cx);
          p.x += Math.cos(a + Math.PI / 2) * 0.25;
          p.y += Math.sin(a + Math.PI / 2) * 0.25;
          const d = Math.sqrt((p.x - cx) ** 2 + (p.y - cy) ** 2);
          if (d > Math.max(W, H) * 0.55) {
            p.x = cx + (Math.random() - 0.5) * W * 0.5;
            p.y = cy + (Math.random() - 0.5) * H * 0.5;
          }
        } else if (particleStyle === "grid") {
          p.x += Math.sin(p.life * 0.01) * 0.15;
          p.y += Math.cos(p.life * 0.008) * 0.15;
        } else {
          p.x += Math.sin(p.life * 0.012) * 0.2;
          p.y += Math.cos(p.life * 0.01) * 0.2;
        }
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = theme.accent + Math.round(p.o * 255).toString(16).padStart(2, "0");
        ctx.fill();
      });

      if (particleStyle === "network" || particleStyle === "grid") {
        for (let i = 0; i < pts.length; i++) {
          for (let j = i + 1; j < pts.length; j++) {
            const dx = pts[i].x - pts[j].x, dy = pts[i].y - pts[j].y;
            const d = Math.sqrt(dx * dx + dy * dy);
            if (d < 70) {
              ctx.beginPath();
              ctx.moveTo(pts[i].x, pts[i].y);
              ctx.lineTo(pts[j].x, pts[j].y);
              ctx.strokeStyle = theme.accent + Math.round((1 - d / 70) * 30).toString(16).padStart(2, "0");
              ctx.lineWidth = 0.4;
              ctx.stroke();
            }
          }
        }
      }
      animRef.current = requestAnimationFrame(tick);
    }
    tick();
    return () => cancelAnimationFrame(animRef.current);
  }, [theme.accent, particleStyle, active]);

  if (particleStyle === "none") return null;
  return <canvas ref={canvasRef} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", pointerEvents: "none", opacity: 0.7 }} />;
}

// ─── SAMPLE CARD ───
function SampleCard({ theme, title, stat, statLabel, body, delay, borderStyle }) {
  return (
    <div style={{
      background: theme.bgDeep,
      borderRadius: 8,
      padding: "14px 16px",
      marginBottom: 8,
      display: "flex", alignItems: "flex-start", gap: 14,
      borderLeft: borderStyle === "left" ? `3px solid ${theme.accent}` : "none",
      borderTop: borderStyle === "top" ? `2px solid ${theme.accent}` : "none",
    }}>
      <div style={{ flexShrink: 0, textAlign: "center", minWidth: 44 }}>
        <div style={{ fontFamily: theme.fontDisplay, fontSize: 20, fontWeight: 700, color: theme.accentLight, lineHeight: 1 }}>{stat}</div>
        <div style={{ fontSize: 7, color: theme.textDim, textTransform: "uppercase", letterSpacing: 0.8, marginTop: 2 }}>{statLabel}</div>
      </div>
      <div>
        <h3 style={{ fontFamily: theme.fontDisplay, fontSize: 12, fontWeight: 700, color: theme.accentLight, margin: "0 0 4px" }}>{title}</h3>
        <p style={{ fontSize: 10, color: theme.textMuted, lineHeight: 1.5, margin: 0 }}>{body}</p>
      </div>
    </div>
  );
}

// ─── COLOR SWATCH ROW ───
function SwatchRow({ colors, label }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 6 }}>
      <span style={{ fontSize: 9, color: "#8B8B9F", width: 50, flexShrink: 0, fontFamily: "'JetBrains Mono', monospace" }}>{label}</span>
      <div style={{ display: "flex", gap: 3 }}>
        {colors.map((c, i) => (
          <div key={i} style={{ width: 18, height: 18, borderRadius: 4, background: c, border: "1px solid rgba(255,255,255,0.08)" }} title={c} />
        ))}
      </div>
    </div>
  );
}

// ─── THEME PREVIEW PANEL ───
function ThemePreview({ theme, expanded, onToggle }) {
  const isLight = theme.id === "paper-ink";

  return (
    <div style={{
      background: expanded ? theme.bg : "#18181F",
      borderRadius: 14,
      overflow: "hidden",
      border: expanded ? `1px solid ${theme.accent}35` : "1px solid rgba(255,255,255,0.06)",
      transition: "all 0.4s cubic-bezier(0.22,1,0.36,1)",
      boxShadow: expanded ? `0 8px 40px ${theme.accentGlow}` : "0 2px 12px rgba(0,0,0,0.3)",
    }}>
      <link href={theme.fontsUrl} rel="stylesheet" />

      {/* Header bar */}
      <div onClick={onToggle} style={{
        padding: "18px 22px",
        cursor: "pointer",
        background: theme.bg,
        display: "flex", alignItems: "center", justifyContent: "space-between",
        borderBottom: expanded ? `1px solid ${theme.border}` : "none",
      }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 4 }}>
            <div style={{ display: "flex", gap: 3 }}>
              {theme.pageColors.map((pc, i) => (
                <div key={i} style={{ width: 10, height: 10, borderRadius: "50%", background: pc.color }} />
              ))}
            </div>
            <h2 style={{ fontFamily: theme.fontDisplay, fontSize: 18, fontWeight: 700, color: theme.text, margin: 0 }}>{theme.name}</h2>
          </div>
          <p style={{ fontSize: 11, color: theme.textMuted, margin: 0, fontStyle: "italic" }}>{theme.vibe}</p>
        </div>
        <div style={{
          fontSize: 18, color: theme.accent, transform: expanded ? "rotate(180deg)" : "rotate(0)",
          transition: "transform 0.3s",
        }}>▾</div>
      </div>

      {/* Expanded content */}
      {expanded && (
        <div style={{ padding: 0 }}>
          {/* Description */}
          <div style={{ padding: "16px 22px", background: theme.bg }}>
            <p style={{ fontSize: 12, color: theme.textMuted, lineHeight: 1.65, margin: 0, fontFamily: theme.fontBody }}>{theme.description}</p>
          </div>

          {/* Live preview */}
          <div style={{ position: "relative", padding: "20px 22px", background: theme.bg, overflow: "hidden" }}>
            <MiniParticles theme={theme} style={theme.particleStyle} active={expanded} />

            <div style={{ position: "relative", zIndex: 2 }}>
              {/* Mock landing header */}
              <div style={{ marginBottom: 16 }}>
                <div style={{ fontSize: 8, textTransform: "uppercase", letterSpacing: 2.5, color: theme.textDim, fontFamily: theme.fontDisplay, fontWeight: 600, marginBottom: 4 }}>Your Project · Division</div>
                <h1 style={{ fontFamily: theme.fontDisplay, fontSize: 28, fontWeight: 700, color: theme.text, margin: "0 0 4px", letterSpacing: -0.5, lineHeight: 1.1 }}>
                  GenAI Transformation
                </h1>
                <span style={{ fontFamily: theme.fontDisplay, fontSize: 28, fontWeight: 700, background: `linear-gradient(90deg,${theme.gradient[0]},${theme.gradient[1]})`, WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", lineHeight: 1.1 }}>
                  Advocacy Deck
                </span>
              </div>

              {/* Mock tile row */}
              <div style={{ display: "flex", gap: 8, marginBottom: 14 }}>
                {theme.pageColors.map((pc, i) => (
                  <div key={i} style={{
                    flex: 1, background: theme.bgCard, borderRadius: 8, padding: "12px 10px",
                    border: `1px solid ${theme.border}`,
                    borderBottom: `2px solid ${pc.color}`,
                  }}>
                    <div style={{ fontSize: 20, marginBottom: 4 }}>{["◉", "⬡", "⟳", "△"][i]}</div>
                    <div style={{ fontFamily: theme.fontDisplay, fontSize: 10, fontWeight: 700, color: theme.text, lineHeight: 1.2 }}>
                      {["Human Loop", "Hurdles", "Sprint", "Results"][i]}
                    </div>
                    <div style={{ fontSize: 8, color: theme.textDim, marginTop: 2 }}>Subtitle text</div>
                  </div>
                ))}
              </div>

              {/* Mock stat bar */}
              <div style={{ display: "flex", gap: 16, paddingTop: 10, borderTop: `1px solid ${theme.border}` }}>
                {[{ v: "~40%", l: "Uplift" }, { v: "0", l: "Defects" }, { v: "~95%", l: "Predict." }].map((s, i) => (
                  <div key={i}>
                    <div style={{ fontFamily: theme.fontDisplay, fontSize: 14, fontWeight: 700, color: theme.accent }}>{s.v}</div>
                    <div style={{ fontSize: 7, color: theme.textDim, textTransform: "uppercase" }}>{s.l}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Mock detail screen */}
          <div style={{ padding: "16px 22px", background: theme.bg, borderTop: `1px solid ${theme.border}` }}>
            <div style={{ textAlign: "center", marginBottom: 12 }}>
              <div style={{ width: 34, height: 34, borderRadius: "50%", background: theme.accent + "16", border: `1.5px solid ${theme.accent}40`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16, margin: "0 auto 8px" }}>◉</div>
              <h2 style={{ fontFamily: theme.fontDisplay, fontSize: 18, fontWeight: 700, color: theme.text, margin: "0 0 2px" }}>Human in the Loop</h2>
              <p style={{ fontSize: 10, color: theme.accentLight, fontStyle: "italic", margin: 0, fontFamily: theme.fontBody }}>AI Accelerates. Humans Govern.</p>
              <div style={{ width: 40, height: 2, background: `linear-gradient(90deg,${theme.accent},${theme.accentLight})`, margin: "8px auto 0", borderRadius: 1 }} />
            </div>
            <SampleCard theme={theme} title="Human Review" stat="100%" statLabel="Reviewed" body="Every line passed through structured PR reviews." borderStyle={theme.cardBorderStyle} />
            <SampleCard theme={theme} title="Low Defects" stat="0" statLabel="Critical" body="Disciplined governance, zero critical defects." borderStyle={theme.cardBorderStyle} />
          </div>

          {/* Specs panel */}
          <div style={{ padding: "16px 22px", background: isLight ? "#F0EDE8" : "#111116", borderTop: `1px solid ${theme.border}` }}>
            <div style={{ fontSize: 10, fontWeight: 700, color: "#8B8B9F", textTransform: "uppercase", letterSpacing: 1.5, marginBottom: 10, fontFamily: "'JetBrains Mono', monospace" }}>Theme Specs</div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
              {/* Fonts */}
              <div>
                <div style={{ fontSize: 9, color: "#6B6B7F", marginBottom: 6, fontWeight: 600 }}>TYPOGRAPHY</div>
                <div style={{ marginBottom: 4 }}>
                  <span style={{ fontSize: 9, color: "#8B8B9F" }}>Display: </span>
                  <span style={{ fontFamily: theme.fontDisplay, fontSize: 12, fontWeight: 700, color: "#D0D0E0" }}>{theme.fontDisplay.split("'")[1]}</span>
                </div>
                <div>
                  <span style={{ fontSize: 9, color: "#8B8B9F" }}>Body: </span>
                  <span style={{ fontFamily: theme.fontBody, fontSize: 11, color: "#D0D0E0" }}>{theme.fontBody.split("'")[1]}</span>
                </div>
              </div>

              {/* Colors */}
              <div>
                <div style={{ fontSize: 9, color: "#6B6B7F", marginBottom: 6, fontWeight: 600 }}>PALETTE</div>
                <SwatchRow label="BG" colors={[theme.bg, theme.bgCard, theme.bgDeep]} />
                <SwatchRow label="ACCENT" colors={[theme.accent, theme.accentLight, ...theme.gradient]} />
                <SwatchRow label="PAGES" colors={theme.pageColors.map(p => p.color)} />
              </div>
            </div>

            {/* Features */}
            <div style={{ display: "flex", gap: 6, marginTop: 12, flexWrap: "wrap" }}>
              {[
                `Particles: ${theme.particleStyle}`,
                `Borders: ${theme.cardBorderStyle}`,
                theme.id === "paper-ink" ? "Light mode" : "Dark mode",
                isLight ? "High contrast" : "OLED-friendly",
              ].map((tag, i) => (
                <span key={i} style={{
                  fontSize: 8, padding: "3px 8px", borderRadius: 10,
                  background: "rgba(139,139,159,0.1)", color: "#8B8B9F",
                  border: "1px solid rgba(139,139,159,0.15)",
                  fontFamily: "'JetBrains Mono', monospace",
                }}>{tag}</span>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ─── COMPARISON GRID ───
function ComparisonView({ themes }) {
  return (
    <div style={{ overflowX: "auto" }}>
      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 11 }}>
        <thead>
          <tr style={{ borderBottom: "1px solid rgba(255,255,255,0.08)" }}>
            <th style={{ textAlign: "left", padding: "10px 12px", color: "#6B6B7F", fontSize: 9, textTransform: "uppercase", letterSpacing: 1.2, fontFamily: "'JetBrains Mono', monospace" }}>Theme</th>
            <th style={{ textAlign: "left", padding: "10px 12px", color: "#6B6B7F", fontSize: 9, textTransform: "uppercase", letterSpacing: 1.2, fontFamily: "'JetBrains Mono', monospace" }}>Vibe</th>
            <th style={{ textAlign: "left", padding: "10px 12px", color: "#6B6B7F", fontSize: 9, textTransform: "uppercase", letterSpacing: 1.2, fontFamily: "'JetBrains Mono', monospace" }}>Display Font</th>
            <th style={{ textAlign: "left", padding: "10px 12px", color: "#6B6B7F", fontSize: 9, textTransform: "uppercase", letterSpacing: 1.2, fontFamily: "'JetBrains Mono', monospace" }}>Body Font</th>
            <th style={{ textAlign: "center", padding: "10px 12px", color: "#6B6B7F", fontSize: 9, textTransform: "uppercase", letterSpacing: 1.2, fontFamily: "'JetBrains Mono', monospace" }}>Palette</th>
            <th style={{ textAlign: "center", padding: "10px 12px", color: "#6B6B7F", fontSize: 9, textTransform: "uppercase", letterSpacing: 1.2, fontFamily: "'JetBrains Mono', monospace" }}>Best For</th>
          </tr>
        </thead>
        <tbody>
          {themes.map((t, i) => (
            <tr key={t.id} style={{ borderBottom: "1px solid rgba(255,255,255,0.04)", background: i % 2 === 0 ? "transparent" : "rgba(255,255,255,0.015)" }}>
              <td style={{ padding: "10px 12px" }}>
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <div style={{ width: 22, height: 22, borderRadius: 6, background: t.bg, border: `2px solid ${t.accent}`, display: "flex", alignItems: "center", justifyContent: "center" }}>
                    <div style={{ width: 6, height: 6, borderRadius: "50%", background: t.accent }} />
                  </div>
                  <span style={{ fontWeight: 600, color: "#E0E0F0" }}>{t.name}</span>
                </div>
              </td>
              <td style={{ padding: "10px 12px", color: "#8B8B9F", fontStyle: "italic", fontSize: 10 }}>{t.vibe}</td>
              <td style={{ padding: "10px 12px" }}>
                <link href={t.fontsUrl} rel="stylesheet" />
                <span style={{ fontFamily: t.fontDisplay, color: "#C0C0D0", fontWeight: 700 }}>{t.fontDisplay.split("'")[1]}</span>
              </td>
              <td style={{ padding: "10px 12px" }}>
                <span style={{ fontFamily: t.fontBody, color: "#A0A0B0" }}>{t.fontBody.split("'")[1]}</span>
              </td>
              <td style={{ padding: "10px 12px" }}>
                <div style={{ display: "flex", justifyContent: "center", gap: 3 }}>
                  {[t.bg, t.accent, t.accentLight, t.secondary].map((c, j) => (
                    <div key={j} style={{ width: 14, height: 14, borderRadius: 3, background: c, border: "1px solid rgba(255,255,255,0.1)" }} />
                  ))}
                </div>
              </td>
              <td style={{ padding: "10px 12px", textAlign: "center", fontSize: 10, color: "#8B8B9F" }}>
                {[
                  "Executive / Consulting",
                  "Engineering / DevOps",
                  "Developer / Portfolio",
                  "Client / Trust-building",
                  "Innovation / Bold pitch",
                  "Print / Report style",
                ][i]}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// ═══════════════════════════════════════════════
// MAIN APP
// ═══════════════════════════════════════════════
export default function App() {
  const [expanded, setExpanded] = useState("obsidian-ember");
  const [view, setView] = useState("gallery");

  return (
    <div style={{ fontFamily: "'Nunito Sans', sans-serif", minHeight: "100vh", background: "#0C0C12", color: "#E0E0F0" }}>
      <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700&family=Nunito+Sans:wght@400;600;700&display=swap" rel="stylesheet" />

      {/* Header */}
      <div style={{ padding: "36px 40px 24px" }}>
        <div style={{ fontSize: 9, textTransform: "uppercase", letterSpacing: 3, color: "#55556E", fontFamily: "'JetBrains Mono', monospace", fontWeight: 500, marginBottom: 8 }}>
          Advocacy Deck · Starter Kit
        </div>
        <h1 style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 32, fontWeight: 700, color: "#E0E0F0", margin: "0 0 6px", letterSpacing: -0.5, lineHeight: 1.1 }}>
          Theme Explorer
        </h1>
        <p style={{ fontSize: 13, color: "#8B8B9F", margin: "0 0 20px", maxWidth: 600, lineHeight: 1.6 }}>
          Six distinct visual identities — each with its own typography, palette, particle style, and card treatment. Every theme is a complete config object ready to drop into the deck.
        </p>

        {/* View toggle */}
        <div style={{ display: "flex", gap: 6 }}>
          {[["gallery", "Gallery"], ["compare", "Compare"]].map(([k, l]) => (
            <button key={k} onClick={() => setView(k)} style={{
              padding: "6px 16px", borderRadius: 16, cursor: "pointer",
              fontFamily: "'JetBrains Mono', monospace", fontSize: 11, fontWeight: 600,
              background: view === k ? "rgba(79,195,247,0.12)" : "rgba(255,255,255,0.04)",
              border: `1px solid ${view === k ? "#4FC3F7" : "rgba(255,255,255,0.06)"}`,
              color: view === k ? "#4FC3F7" : "#6B6B7F",
              letterSpacing: 0.5,
            }}>{l}</button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div style={{ padding: "0 40px 48px" }}>
        {view === "gallery" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 12, maxWidth: 800 }}>
            {THEMES.map(t => (
              <ThemePreview
                key={t.id}
                theme={t}
                expanded={expanded === t.id}
                onToggle={() => setExpanded(expanded === t.id ? null : t.id)}
              />
            ))}
          </div>
        )}

        {view === "compare" && (
          <div style={{ background: "#111116", borderRadius: 12, padding: 20, border: "1px solid rgba(255,255,255,0.06)" }}>
            <ComparisonView themes={THEMES} />
          </div>
        )}

        {/* Usage notes */}
        <div style={{ marginTop: 32, padding: "20px 24px", background: "#111116", borderRadius: 10, border: "1px solid rgba(255,255,255,0.06)", maxWidth: 800 }}>
          <div style={{ fontSize: 10, fontWeight: 700, color: "#55556E", textTransform: "uppercase", letterSpacing: 1.5, marginBottom: 10, fontFamily: "'JetBrains Mono', monospace" }}>
            How to Use a Theme
          </div>
          <div style={{ fontSize: 12, color: "#8B8B9F", lineHeight: 1.7 }}>
            <p style={{ margin: "0 0 8px" }}>Each theme above is a complete configuration. To apply one to the deck starter kit, copy its values into the <code style={{ background: "rgba(79,195,247,0.1)", padding: "1px 5px", borderRadius: 3, color: "#81D4FA", fontFamily: "'JetBrains Mono', monospace", fontSize: 11 }}>deck.theme</code> section of your JSON config.</p>
            <p style={{ margin: "0 0 8px" }}>The font URLs are Google Fonts links — paste them into <code style={{ background: "rgba(79,195,247,0.1)", padding: "1px 5px", borderRadius: 3, color: "#81D4FA", fontFamily: "'JetBrains Mono', monospace", fontSize: 11 }}>theme.googleFontsUrl</code> and update <code style={{ background: "rgba(79,195,247,0.1)", padding: "1px 5px", borderRadius: 3, color: "#81D4FA", fontFamily: "'JetBrains Mono', monospace", fontSize: 11 }}>fontDisplay</code> and <code style={{ background: "rgba(79,195,247,0.1)", padding: "1px 5px", borderRadius: 3, color: "#81D4FA", fontFamily: "'JetBrains Mono', monospace", fontSize: 11 }}>fontBody</code> accordingly.</p>
            <p style={{ margin: 0 }}>Page-level accent colors come from the <code style={{ background: "rgba(79,195,247,0.1)", padding: "1px 5px", borderRadius: 3, color: "#81D4FA", fontFamily: "'JetBrains Mono', monospace", fontSize: 11 }}>pageColors</code> array — assign one to each page in your deck.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
