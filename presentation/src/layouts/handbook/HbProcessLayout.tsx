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

export function HbProcessLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 60); return () => clearTimeout(t); }, []);
  const steps = topic.steps as Array<{ num: string; title: string; body: string }> || [];
  const cols = steps.length <= 4 ? steps.length : 4;
  return (
    <div style={{ minHeight: "100vh", background: T.bg, display: "flex", flexDirection: "column" }}>
      <div style={{ height: 6, background: T.accent }} />
      <div style={{ flex: 1, padding: "36px 48px 0" }}>
        <BackBtn onClick={onBack} />
        <div style={{ marginBottom: 28, opacity: entered ? 1 : 0, transition: "all 0.6s ease" }}>
          <div style={{ fontSize: 10, fontFamily: T.fontDisplay, fontWeight: 700, letterSpacing: 2.5, textTransform: "uppercase", color: T.textDim, marginBottom: 6 }}>{topic.eyebrow as string || "Process"}</div>
          <h1 style={{ fontFamily: T.fontDisplay, fontSize: 40, fontWeight: 800, color: T.text, margin: "0 0 6px", letterSpacing: -0.5 }}>{topic.title}</h1>
          <p style={{ fontFamily: T.fontBody, fontSize: 13, color: T.textMuted, fontStyle: "italic", margin: 0 }}>{topic.subtitle}</p>
        </div>
        {/* Steps grid — 4 per row */}
        <div style={{ display: "grid", gridTemplateColumns: `repeat(${cols}, 1fr)`, gap: 3, marginBottom: 28 }}>
          {steps.map((step, i) => {
            const evenStep = i % 2 === 0;
            return (
              <div key={i} style={{ background: T.bgCard, padding: "24px 20px", borderTop: `5px solid ${evenStep ? T.accent : T.text}`, opacity: entered ? 1 : 0, transform: entered ? "none" : "translateY(14px)", transition: `all 0.45s ${0.15 + i * 0.07}s cubic-bezier(0.22,1,0.36,1)` }}>
                <div style={{ fontFamily: T.fontDisplay, fontSize: 36, fontWeight: 800, color: T.text, lineHeight: 1, marginBottom: 14 }}>{step.num}</div>
                <h3 style={{ fontFamily: T.fontDisplay, fontSize: 13, fontWeight: 800, color: T.text, margin: "0 0 8px", textTransform: "uppercase", letterSpacing: 0.5 }}>{step.title}</h3>
                <p style={{ fontFamily: T.fontBody, fontSize: 12.5, color: T.textMuted, lineHeight: 1.6, margin: 0 }}>{step.body}</p>
              </div>
            );
          })}
        </div>
      </div>
      {/* Bold manifesto-style callout */}
      <div style={{ background: T.text, padding: "24px 48px", textAlign: "center", opacity: entered ? 1 : 0, transition: "opacity 0.6s 1s ease" }}>
        <p style={{ fontFamily: T.fontDisplay, fontSize: 20, fontWeight: 800, color: T.accent, margin: 0, letterSpacing: -0.25 }}>&ldquo;{topic.callout}&rdquo;</p>
      </div>
    </div>
  );
}

export default HbProcessLayout;
