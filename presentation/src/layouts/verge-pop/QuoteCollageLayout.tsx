/**
 * QuoteCollageLayout — Verge-style layout with speech-bubble quote cards.
 * Layout ID: "quote-collage"
 */

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

export function QuoteCollageLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const [e, setE] = useState(false);
  useEffect(() => { const t = setTimeout(() => setE(true), 50); return () => clearTimeout(t); }, []);

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1180, margin: "0 auto", padding: "48px" }}>
        <BackBtn onClick={onBack} />
        <h1 style={{ fontFamily: T.fontDisplay, fontSize: 48, fontWeight: C.headingWeight, color: T.text, margin: "0 0 12px", lineHeight: 1.1 }}>
          {topic.title}
        </h1>
        {topic.subtitle && <p style={{ fontSize: 14, color: T.textMuted, margin: "0 0 28px", maxWidth: 600, lineHeight: 1.6 }}>{topic.subtitle}</p>}
        <div style={{ display: "flex", flexWrap: "wrap", gap: 14, marginBottom: 20, justifyContent: "center" }}>
          {(topic.quotes as Array<{ bgColor?: string; text: string }> || []).map((q, idx) => (
            <div key={idx} style={{
              position: "relative", background: q.bgColor || topic.color,
              borderRadius: C.cardRadius + 4, padding: "14px 18px",
              maxWidth: 260, minWidth: 160, flex: "0 1 auto",
              border: `${C.cardBorderWidth}px solid rgba(0,0,0,0.12)`,
              opacity: e ? 1 : 0, transform: e ? "scale(1)" : "scale(0.85)",
              transition: `all 0.4s ${0.05 + idx * 0.05}s cubic-bezier(0.34,1.56,0.64,1)`,
            }}>
              <p style={{ fontFamily: T.fontBody, fontSize: 13, color: "#000", lineHeight: 1.5, margin: 0, fontWeight: 500 }}>
                &ldquo;{q.text}&rdquo;
              </p>
              <div style={{
                position: "absolute", bottom: -8, left: 20 + (idx % 3) * 20,
                width: 0, height: 0,
                borderLeft: "8px solid transparent", borderRight: "8px solid transparent",
                borderTop: `8px solid ${q.bgColor || topic.color}`,
              }} />
            </div>
          ))}
        </div>
        {topic.centerLabel && (
          <div style={{ textAlign: "center", margin: "20px 0 24px" }}>
            <span style={{ fontFamily: T.fontDisplay, fontSize: 13, fontWeight: 700, color: T.text, letterSpacing: 3, textTransform: "uppercase", background: T.bgCard, padding: "10px 20px", borderRadius: C.cardRadius, border: `${C.cardBorderWidth}px solid ${T.text}` }}>
              {topic.centerLabel as string}
            </span>
          </div>
        )}
        <div style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "18px 22px", borderLeft: `${C.accentBarHeight}px solid ${topic.color}`, maxWidth: 700 }}>
          <p style={{ fontFamily: T.fontDisplay, fontSize: 18, color: T.text, margin: 0, fontWeight: 600 }}>{topic.callout}</p>
        </div>
      </div>
    </div>
  );
}

export default QuoteCollageLayout;
