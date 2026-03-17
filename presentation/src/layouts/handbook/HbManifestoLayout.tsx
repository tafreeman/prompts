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

export function HbManifestoLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 60); return () => clearTimeout(t); }, []);
  const lines = (topic.statement as string || "").split("\n");
  return (
    <div style={{ minHeight: "100vh", background: T.accent, display: "flex", flexDirection: "column" }}>
      <div style={{ height: 6, background: T.text }} />
      <div style={{ padding: "32px 48px 0", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <BackBtn onClick={onBack} />
        <div style={{ fontSize: 10, fontFamily: T.fontDisplay, fontWeight: 700, letterSpacing: 2.5, textTransform: "uppercase", color: `${T.text}70` }}>{topic.eyebrow as string}</div>
      </div>
      {/* Main statement */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column", justifyContent: "center", padding: "0 48px 0", maxWidth: 960, margin: "0 auto", width: "100%" }}>
        <h1 style={{ fontFamily: T.fontDisplay, fontSize: 68, fontWeight: 800, color: T.text, lineHeight: 1.08, margin: "0 0 48px", letterSpacing: -1.5, opacity: entered ? 1 : 0, transform: entered ? "none" : "translateY(24px)", transition: "all 0.8s cubic-bezier(0.22,1,0.36,1)" }}>
          {lines.map((line, i) => <span key={i}>{line}{i < lines.length - 1 && <br />}</span>)}
          <span style={{ fontFamily: T.fontDisplay, fontSize: 36, verticalAlign: "super" }}>*</span>
        </h1>
        {/* Beliefs */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "14px 56px" }}>
          {(topic.beliefs as string[] || []).map((b, i) => (
            <div key={i} style={{ display: "flex", gap: 14, alignItems: "flex-start", opacity: entered ? 1 : 0, transform: entered ? "none" : "translateX(-10px)", transition: `all 0.5s ${0.3 + i * 0.1}s ease` }}>
              <span style={{ fontFamily: T.fontDisplay, fontSize: 18, fontWeight: 800, color: T.text, flexShrink: 0, marginTop: 1 }}>→</span>
              <p style={{ fontFamily: T.fontBody, fontSize: 14.5, color: T.text, lineHeight: 1.6, margin: 0 }}>{b}</p>
            </div>
          ))}
        </div>
      </div>
      {/* Footer footnote */}
      <div style={{ background: T.text, padding: "16px 48px", borderTop: `2px solid ${T.text}`, marginTop: 40 }}>
        <p style={{ fontFamily: T.fontBody, fontSize: 12, color: T.accent, margin: 0, opacity: 0.9 }}>* {topic.callout}</p>
      </div>
    </div>
  );
}

export default HbManifestoLayout;
