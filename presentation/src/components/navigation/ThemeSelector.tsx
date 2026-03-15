/**
 * ThemeSelector — full-screen theme selection grid shown at startup.
 *
 * Renders a 3-column grid of theme preview cards with hover effects and
 * staggered entrance animation. Operates independently of ThemeContext
 * because it runs _before_ a theme is selected.
 */

import React, { useState, useEffect } from "react";
import { THEMES, THEME_SELECTOR_FONTS_URL } from "../../tokens/themes.ts";
import type { Theme } from "../../tokens/themes.ts";
import { usePresentationViewport } from "../hooks/usePresentationViewport.js";

interface ThemeSelectorProps {
  onSelect: (theme: Theme) => void;
}

export function ThemeSelector({ onSelect }: ThemeSelectorProps) {
  const [hovered, setHovered] = useState<string | null>(null);
  const [entered, setEntered] = useState(false);
  const viewport = usePresentationViewport();

  useEffect(() => {
    const t = setTimeout(() => setEntered(true), 50);
    return () => clearTimeout(t);
  }, []);

  return (
    <div style={{ minHeight: "100dvh", background: "#08101C", display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", padding: viewport.isPhone ? "24px 16px 32px" : viewport.isCompact ? "32px 24px" : "40px 48px", overflowY: viewport.overlayScroll }}>
      <link href={THEME_SELECTOR_FONTS_URL} rel="stylesheet" />

      <div style={{ textAlign: "center", marginBottom: 40, opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(20px)", transition: "all 0.6s ease" }}>
        <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: 4, color: "#64748B", fontFamily: "'Space Grotesk',sans-serif", fontWeight: 500, marginBottom: 12 }}>GenAI Transformation</div>
        <h1 style={{ fontFamily: "'Space Grotesk',sans-serif", fontSize: viewport.isPhone ? 30 : viewport.isCompact ? 34 : 40, fontWeight: 700, color: "#F0F4F8", margin: "0 0 10px", letterSpacing: -1 }}>Choose Your Theme</h1>
        <p style={{ fontSize: viewport.isPhone ? 13 : 14, color: "#94A3B8", margin: 0 }}>Select a visual style for the advocacy deck</p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: viewport.isPhone ? "1fr" : viewport.isCompact ? "1fr 1fr" : "1fr 1fr 1fr", gap: viewport.isPhone ? 12 : 16, maxWidth: 900, width: "100%" }}>
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
              <div style={{ background: t.bg, padding: viewport.isPhone ? "18px 16px 12px" : "20px 18px 14px", position: "relative" }}>
                {/* Accent bar */}
                <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: 3, background: `linear-gradient(90deg, ${t.gradient[0]}, ${t.gradient[1]})` }} />
                <div style={{ fontFamily: t.fontDisplay, fontSize: viewport.isPhone ? 16 : 18, fontWeight: 700, color: t.text, marginBottom: 4 }}>{t.name}</div>
                <div style={{ fontSize: 10, color: t.textDim, textTransform: "uppercase", letterSpacing: 1 }}>{t.vibe}</div>
              </div>
              {/* Preview body */}
              <div style={{ background: t.bgCard, padding: viewport.isPhone ? "12px 16px 14px" : "14px 18px 16px" }}>
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

export default ThemeSelector;
