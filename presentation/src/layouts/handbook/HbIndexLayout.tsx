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

export function HbIndexLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 60); return () => clearTimeout(t); }, []);
  const cats = topic.categories as Array<{ label: string; body: string }> || [];
  return (
    <div style={{ minHeight: "100vh", background: T.bg, display: "flex", flexDirection: "column" }}>
      <div style={{ height: 6, background: T.accent }} />
      <div style={{ flex: 1, padding: "36px 48px 0" }}>
        <BackBtn onClick={onBack} />
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", marginBottom: 32, opacity: entered ? 1 : 0, transition: "all 0.6s ease" }}>
          <div>
            <div style={{ fontSize: 10, fontFamily: T.fontDisplay, fontWeight: 700, letterSpacing: 2.5, textTransform: "uppercase", color: T.textDim, marginBottom: 6 }}>{topic.eyebrow as string || "Index"}</div>
            <h1 style={{ fontFamily: T.fontDisplay, fontSize: 40, fontWeight: 800, color: T.text, margin: "0 0 6px", letterSpacing: -0.5 }}>{topic.title}</h1>
            <p style={{ fontFamily: T.fontBody, fontSize: 13, color: T.textMuted, fontStyle: "italic", margin: 0 }}>{topic.subtitle}</p>
          </div>
          <div style={{ fontFamily: T.fontDisplay, fontSize: 84, fontWeight: 800, color: T.text, lineHeight: 1, opacity: 0.07 }}>{topic.num as string}</div>
        </div>
        {/* Category two-column grid */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 3 }}>
          {cats.map((cat, i) => (
            <div key={i} style={{ padding: "22px 26px", background: T.bgCard, borderTop: `4px solid ${i % 3 === 0 ? T.accent : (i % 3 === 2 ? T.text : T.bgDeep)}`, opacity: entered ? 1 : 0, transform: entered ? "none" : "translateY(12px)", transition: `all 0.45s ${0.12 + i * 0.08}s cubic-bezier(0.22,1,0.36,1)` }}>
              <div style={{ fontFamily: T.fontDisplay, fontSize: 11, fontWeight: 700, color: T.textDim, letterSpacing: 1.5, textTransform: "uppercase", marginBottom: 6 }}>0{i + 1}</div>
              <h3 style={{ fontFamily: T.fontDisplay, fontSize: 15, fontWeight: 800, color: T.text, margin: "0 0 8px" }}>{cat.label}</h3>
              <p style={{ fontFamily: T.fontBody, fontSize: 13, color: T.textMuted, lineHeight: 1.65, margin: 0 }}>{cat.body}</p>
            </div>
          ))}
        </div>
      </div>
      <div style={{ background: T.text, padding: "16px 48px", marginTop: 32 }}>
        <p style={{ fontFamily: T.fontDisplay, fontSize: 14, fontWeight: 700, color: T.accent, margin: 0, fontStyle: "italic" }}>&ldquo;{topic.callout}&rdquo;</p>
      </div>
    </div>
  );
}

export default HbIndexLayout;
