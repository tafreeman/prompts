/**
 * CatalogLayout — color-coded category catalog screen.
 *
 * Extracted from genai_advocacy_hub_13.jsx (CatalogScreen, layout id: "catalog").
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

export function CatalogLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme() as Theme;
  const C = useChrome() as StyleMode;
  const [entered, setEntered] = useState<boolean>(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 60); return () => clearTimeout(t); }, []);

  const categories = (topic.categories as Record<string, unknown>[]) || [];

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <Particles color={topic.color} active={entered} />
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1100, margin: "0 auto", padding: "36px 32px" }}>
        <BackBtn onClick={onBack} />
        <SectionHeader topic={topic} entered={entered} />
        <div style={{ display: "grid", gridTemplateColumns: `repeat(${Math.min(categories.length, 4)}, 1fr)`, gap: 16 }}>
          {categories.map((cat, ci) => (
            <div key={ci} style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "20px 18px", borderTop: `${C.accentBarHeight}px solid ${cat.color as string}`, opacity: entered ? 1 : 0, transform: entered ? "none" : "translateY(16px)", transition: `all 0.5s ${0.15 + ci * 0.12}s ease` }}>
              <h3 style={{ fontFamily: T.fontDisplay, fontSize: 14, fontWeight: C.headingWeight, color: cat.color as string, margin: "0 0 16px" }}>{cat.title as string}</h3>
              <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                {((cat.items as Record<string, unknown>[]) || []).map((item, i) => (
                  <div key={i} style={{ padding: "10px 12px", borderRadius: C.innerRadius, background: T.bgDeep, borderLeft: `${C.accentBarHeight}px solid ${cat.color as string}40` }}>
                    <div style={{ fontFamily: T.fontDisplay, fontSize: 12, fontWeight: C.headingWeight, color: T.text, marginBottom: 3 }}>{item.label as string}</div>
                    <p style={{ fontSize: 11.5, color: T.textMuted, lineHeight: 1.5, margin: 0 }}>{item.desc as string}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
        <div style={{ marginTop: 28, padding: "18px 22px", borderLeft: `${C.accentBarHeight}px solid ${T.accent}`, background: T.bgCard, borderRadius: `0 ${C.innerRadius}px ${C.innerRadius}px 0` }}>
          <p style={{ fontSize: 14, color: T.text, lineHeight: 1.65, margin: 0, fontWeight: 600 }}>&ldquo;{topic.callout}&rdquo;</p>
        </div>
      </div>
    </div>
  );
}

export default CatalogLayout;
