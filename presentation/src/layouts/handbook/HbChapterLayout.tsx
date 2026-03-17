import React, { useState, useEffect } from "react";
import { useTheme } from "../../components/hooks/useTheme.ts";
import { useChrome } from "../../components/hooks/useChrome.ts";
import BackBtn from "../../components/navigation/BackBtn.tsx";

interface Topic {
  id: string;
  title: string;
  subtitle?: string;
  color: string;
  colorLight?: string;
  colorGlow?: string;
  icon?: string;
  callout?: string;
  [key: string]: unknown;
}

interface LayoutProps {
  topic: Topic;
  onBack: () => void;
}

export function HbChapterLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 60); return () => clearTimeout(t); }, []);
  return (
    <div style={{ minHeight: "100vh", background: T.bg, display: "flex", flexDirection: "column" }}>
      {/* Eyebrow bar */}
      <div style={{ background: T.accent, padding: "8px 48px", display: "flex", justifyContent: "space-between", alignItems: "center", borderBottom: `2px solid ${T.text}` }}>
        <span style={{ fontFamily: T.fontDisplay, fontSize: 11, fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", color: T.text }}>{topic.eyebrow as string || "Chapter"}</span>
        <span style={{ fontFamily: T.fontDisplay, fontSize: 11, fontWeight: 700, color: T.text }}>{topic.num as string}</span>
      </div>
      {/* Main two-column content */}
      <div style={{ flex: 1, display: "grid", gridTemplateColumns: "1fr 1fr", minHeight: 0 }}>
        {/* Left — headline + summary + bullets */}
        <div style={{ padding: "40px 48px", borderRight: `2px solid ${T.text}20`, display: "flex", flexDirection: "column" }}>
          <BackBtn onClick={onBack} />
          <div style={{ flex: 1, display: "flex", flexDirection: "column", justifyContent: "center", opacity: entered ? 1 : 0, transform: entered ? "none" : "translateY(20px)", transition: "all 0.7s cubic-bezier(0.22,1,0.36,1)" }}>
            <h1 style={{ fontFamily: T.fontDisplay, fontSize: 52, fontWeight: 800, color: T.text, lineHeight: 1.05, margin: "0 0 12px", letterSpacing: -1 }}>{topic.title}</h1>
            <p style={{ fontFamily: T.fontBody, fontSize: 13, color: T.textMuted, fontStyle: "italic", margin: "0 0 20px" }}>{topic.subtitle}</p>
            <p style={{ fontFamily: T.fontBody, fontSize: 14.5, color: T.textMuted, lineHeight: 1.75, margin: "0 0 28px" }}>{topic.summary as string}</p>
            {(topic.heroPoints as string[] || []).map((pt, i) => (
              <div key={i} style={{ display: "flex", gap: 12, marginBottom: 10, opacity: entered ? 1 : 0, transform: entered ? "none" : "translateX(-10px)", transition: `all 0.4s ${0.25 + i * 0.07}s ease` }}>
                <div style={{ width: 8, height: 8, background: T.accent, border: `2px solid ${T.text}`, borderRadius: "50%", marginTop: 7, flexShrink: 0 }} />
                <span style={{ fontFamily: T.fontBody, fontSize: 13.5, color: T.text, lineHeight: 1.55 }}>{pt}</span>
              </div>
            ))}
          </div>
        </div>
        {/* Right — chapter index / schedule table */}
        <div style={{ padding: "40px 48px", display: "flex", flexDirection: "column", justifyContent: "center" }}>
          <div style={{ fontSize: 10, fontFamily: T.fontDisplay, fontWeight: 700, letterSpacing: 2.5, textTransform: "uppercase", color: T.textDim, marginBottom: 24 }}>{topic.eyebrow as string || "Index"}</div>
          {(topic.chapters as Array<{ num: string; title: string; sub: string }> || []).map((ch, i) => (
            <div key={i} style={{ display: "flex", gap: 20, padding: "14px 0", borderBottom: `1px solid ${T.text}15`, alignItems: "flex-start", opacity: entered ? 1 : 0, transform: entered ? "none" : "translateY(8px)", transition: `all 0.4s ${0.15 + i * 0.08}s ease` }}>
              <div style={{ fontFamily: T.fontDisplay, fontSize: 20, fontWeight: 800, color: T.text, minWidth: 54, flexShrink: 0, paddingBottom: 2, borderBottom: `3px solid ${T.accent}` }}>{ch.num}</div>
              <div>
                <div style={{ fontFamily: T.fontDisplay, fontSize: 14, fontWeight: 700, color: T.text, marginBottom: 2 }}>{ch.title}</div>
                <div style={{ fontFamily: T.fontBody, fontSize: 12, color: T.textDim }}>{ch.sub}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
      {/* Callout footer bar */}
      <div style={{ background: T.text, padding: "16px 48px", borderTop: `2px solid ${T.text}` }}>
        <p style={{ fontFamily: T.fontDisplay, fontSize: 14, fontWeight: 700, color: T.accent, margin: 0, fontStyle: "italic" }}>&ldquo;{topic.callout}&rdquo;</p>
      </div>
    </div>
  );
}

export default HbChapterLayout;
