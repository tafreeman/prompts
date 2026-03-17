/**
 * PillarsLayout — multi-column pillars + results screen.
 *
 * Extracted from genai_advocacy_hub_13.jsx (PillarsScreen, layout id: "pillars").
 */

import { useState, useEffect } from "react";
import { useTheme } from "../../components/hooks/useTheme.ts";
import { useChrome } from "../../components/hooks/useChrome.ts";
import BackBtn from "../../components/navigation/BackBtn.tsx";
import SectionHeader from "../../components/compound/SectionHeader.tsx";
import Particles from "../../components/animations/Particles.tsx";
import type { Theme } from "../../tokens/themes.ts";
import type { StyleMode } from "../../tokens/style-modes.ts";

interface Topic {
  id: string;
  title: string;
  subtitle?: string;
  color: string;
  colorLight?: string;
  colorGlow?: string;
  icon?: string;
  num?: string;
  order?: number;
  callout?: string;
  banner?: string;
  eyebrow?: string;
  summary?: string;
  heroPoints?: string[];
  talkingPoints?: string[];
  cards?: Record<string, unknown>[];
  [key: string]: unknown;
}

interface LayoutProps {
  topic: Topic;
  onBack: () => void;
}

export function PillarsLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme() as Theme;
  const C = useChrome() as StyleMode;
  const [entered, setEntered] = useState<boolean>(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 60); return () => clearTimeout(t); }, []);

  const pillars = (topic.pillars as Record<string, unknown>[]) || [];
  const results = (topic.results as Record<string, unknown>[]) || null;

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <Particles color={topic.color} active={entered} />
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1100, margin: "0 auto", padding: "36px 32px" }}>
        <BackBtn onClick={onBack} />
        <SectionHeader topic={topic} entered={entered} />
        <div style={{ display: "grid", gridTemplateColumns: `repeat(${Math.min(pillars.length, 5)}, 1fr)`, gap: 16, marginBottom: 20 }}>
          {pillars.map((p, i) => (
            <div key={i} style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "22px 20px", borderTop: `${C.accentBarHeight}px solid ${T.accent}`, opacity: entered ? 1 : 0, transform: entered ? "none" : "translateY(14px)", transition: `all 0.5s ${0.2 + i * 0.12}s ease` }}>
              <div style={{ fontSize: 24, marginBottom: 10 }}>{p.icon as string}</div>
              <h3 style={{ fontFamily: T.fontDisplay, fontSize: 14, fontWeight: C.headingWeight, color: T.accent, margin: "0 0 14px", textTransform: C.headingTransform, letterSpacing: C.labelTracking }}>{p.title as string}</h3>
              <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                {((p.items as string[]) || []).map((item, j) => (
                  <div key={j} style={{ display: "flex", alignItems: "flex-start", gap: 8 }}>
                    <div style={{ width: 5, height: 5, borderRadius: "50%", background: T.accent, marginTop: 5, flexShrink: 0 }} />
                    <p style={{ fontSize: 12, color: T.textMuted, lineHeight: 1.55, margin: 0 }}>{item}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
        {results && (
          <div style={{ display: "flex", gap: 16, marginBottom: 20 }}>
            {results.map((r, i) => (
              <div key={i} style={{ flex: 1, background: T.bgCard, borderRadius: C.cardRadius, padding: "16px 18px", borderLeft: `${C.accentBarHeight}px solid ${T.accent}`, opacity: entered ? 1 : 0, transition: `opacity 0.5s ${0.5 + i * 0.1}s ease` }}>
                <div style={{ fontFamily: T.fontDisplay, fontSize: 22, fontWeight: C.headingWeight, color: T.accent, lineHeight: 1, marginBottom: 4 }}>{r.val as string}</div>
                <p style={{ fontSize: 11, color: T.textMuted, margin: 0 }}>{r.label as string}</p>
              </div>
            ))}
          </div>
        )}
        <div style={{ marginTop: 28, padding: "18px 22px", borderLeft: `${C.accentBarHeight}px solid ${T.accent}`, background: T.bgCard, borderRadius: `0 ${C.innerRadius}px ${C.innerRadius}px 0` }}>
          <p style={{ fontSize: 14, color: T.text, lineHeight: 1.65, margin: 0, fontWeight: 600 }}>&ldquo;{topic.callout}&rdquo;</p>
        </div>
      </div>
    </div>
  );
}

export default PillarsLayout;
