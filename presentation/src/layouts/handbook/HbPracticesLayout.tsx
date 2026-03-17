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

export function HbPracticesLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 60); return () => clearTimeout(t); }, []);
  const practices = topic.practices as Array<{ dark?: boolean; highlight?: boolean; title: string; body: string }> || [];
  return (
    <div style={{ minHeight: "100vh", background: T.bg, display: "flex", flexDirection: "column" }}>
      <div style={{ height: 6, background: T.accent }} />
      <div style={{ flex: 1, padding: "36px 48px 0" }}>
        <BackBtn onClick={onBack} />
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", marginBottom: 10, opacity: entered ? 1 : 0, transition: "all 0.6s ease" }}>
          <div>
            <div style={{ fontSize: 10, fontFamily: T.fontDisplay, fontWeight: 700, letterSpacing: 2.5, textTransform: "uppercase", color: T.textDim, marginBottom: 6 }}>{topic.eyebrow as string || "Practice Areas"}</div>
            <h1 style={{ fontFamily: T.fontDisplay, fontSize: 40, fontWeight: 800, color: T.text, margin: "0 0 6px", letterSpacing: -0.5, lineHeight: 1.1 }}>{topic.title}</h1>
            <p style={{ fontFamily: T.fontBody, fontSize: 13, color: T.textMuted, fontStyle: "italic", margin: 0 }}>{topic.subtitle}</p>
          </div>
          <div style={{ fontFamily: T.fontDisplay, fontSize: 72, fontWeight: 800, color: `${T.text}10`, lineHeight: 1, paddingBottom: 4 }}>{topic.num as string}</div>
        </div>
        <p style={{ fontFamily: T.fontBody, fontSize: 14, color: T.textMuted, lineHeight: 1.7, maxWidth: 680, marginBottom: 28, opacity: entered ? 1 : 0, transition: "all 0.6s 0.1s ease" }}>{topic.summary as string}</p>
        {/* Practice cards grid */}
        <div style={{ display: "grid", gridTemplateColumns: `repeat(${Math.min(practices.length, 3)}, 1fr)`, gap: 3 }}>
          {practices.map((p, i) => {
            const isDark = p.dark;
            const isHighlight = p.highlight;
            const bg = isHighlight ? T.danger : isDark ? T.text : T.bgCard;
            const titleCol = isDark || isHighlight ? T.accent : T.text;
            const bodyCol = isDark || isHighlight ? `${T.accent}B0` : T.textMuted;
            const barCol = isDark ? T.accent : isHighlight ? T.accent : T.text;
            return (
              <div key={i} style={{ background: bg, padding: "28px 24px", opacity: entered ? 1 : 0, transform: entered ? "none" : "translateY(16px)", transition: `all 0.5s ${0.2 + i * 0.09}s cubic-bezier(0.22,1,0.36,1)` }}>
                <div style={{ width: "100%", height: 4, background: barCol, marginBottom: 20 }} />
                <div style={{ fontFamily: T.fontDisplay, fontSize: 11, fontWeight: 700, color: isDark || isHighlight ? `${T.accent}80` : T.textDim, letterSpacing: 2, textTransform: "uppercase", marginBottom: 10 }}>0{i + 1}</div>
                <h3 style={{ fontFamily: T.fontDisplay, fontSize: 16, fontWeight: 800, color: titleCol, margin: "0 0 10px", lineHeight: 1.2 }}>{p.title}</h3>
                <p style={{ fontFamily: T.fontBody, fontSize: 13, color: bodyCol, lineHeight: 1.65, margin: 0 }}>{p.body}</p>
              </div>
            );
          })}
        </div>
      </div>
      {/* Callout */}
      <div style={{ margin: "24px 48px 0", padding: "14px 20px", borderLeft: `4px solid ${T.text}`, background: T.bgDeep, opacity: entered ? 1 : 0, transition: "opacity 0.6s 0.9s ease", marginBottom: 48 }}>
        <p style={{ fontFamily: T.fontDisplay, fontSize: 14, fontWeight: 700, color: T.text, margin: 0 }}>&ldquo;{topic.callout}&rdquo;</p>
      </div>
    </div>
  );
}

export default HbPracticesLayout;
