/**
 * TwoColLayout — two-column overview screen with cards, story notes, and callout.
 *
 * Layout ID: "two-col"
 * Extracted from genai_advocacy_hub_13.jsx OverviewScreen (lines 925-987).
 */

import React, { useState, useEffect } from "react";

import { useTheme } from "../../components/hooks/useTheme.ts";
import { useChrome } from "../../components/hooks/useChrome.ts";
import { usePresentationViewport } from "../../components/hooks/usePresentationViewport.ts";
import BackBtn from "../../components/navigation/BackBtn.tsx";
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

function TwoColLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme() as Theme;
  const C = useChrome() as StyleMode;
  const viewport = usePresentationViewport();
  const [entered, setEntered] = useState<boolean>(false);

  useEffect(() => {
    const timer = setTimeout(() => setEntered(true), 50);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div style={{ position: "relative", minHeight: "100dvh", background: T.bg, overflowX: "hidden", overflowY: viewport.overlayScroll }}>
      <Particles color={topic.color} type="future" active={entered} />
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1180, margin: "0 auto", padding: `${viewport.pagePaddingTop}px ${viewport.pagePaddingX}px ${viewport.pagePaddingBottom}px` }}>
        <BackBtn onClick={onBack} />
        <div style={{ display: "grid", gridTemplateColumns: viewport.isCompact ? "1fr" : "1.1fr 0.9fr", gap: viewport.isPhone ? 18 : 28, alignItems: "start" }}>
          <div style={{ opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(20px)", transition: "all 0.6s ease" }}>
            <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: 3, color: topic.colorLight, fontFamily: T.fontDisplay, marginBottom: 10 }}>{topic.eyebrow || "Overview"}</div>
            <h1 style={{ fontFamily: T.fontDisplay, fontSize: viewport.titleSize, color: T.text, margin: "0 0 10px", lineHeight: 1.05 }}>{topic.title}</h1>
            <p style={{ fontSize: viewport.subtitleSize, color: topic.colorLight, fontStyle: "italic", lineHeight: 1.5, margin: "0 0 14px" }}>{topic.subtitle}</p>
            {topic.summary && <p style={{ fontSize: viewport.bodySize, color: T.textMuted, lineHeight: 1.7, margin: "0 0 18px", maxWidth: viewport.isCompact ? "100%" : 620 }}>{topic.summary}</p>}
            {(topic.heroPoints?.length ?? 0) > 0 && (
              <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 18 }}>
                {topic.heroPoints!.map((point) => (
                  <span key={point} style={{ padding: "7px 12px", borderRadius: C.pillRadius, background: `${topic.color}12`, border: `1px solid ${topic.color}26`, fontSize: 12, color: T.text }}>{point}</span>
                ))}
              </div>
            )}
            <div style={{ display: "grid", gap: 12 }}>
              {(topic.cards ?? []).map((card, index) => (
                <div key={`${card.title as string}-${index}`} style={{ background: T.bgCard, borderRadius: C.innerRadius, padding: viewport.isPhone ? "14px 16px" : "16px 18px", borderLeft: `${C.accentBarHeight}px solid ${topic.color}`, opacity: entered ? 1 : 0, transform: entered ? "translateX(0)" : "translateX(-14px)", transition: `all 0.45s ${0.18 + index * 0.08}s ease` }}>
                  <div style={{ fontFamily: T.fontDisplay, fontSize: 17, color: T.text, marginBottom: 6 }}>{card.title as string}</div>
                  <p style={{ fontSize: viewport.isPhone ? 12.5 : 13.5, color: T.textMuted, lineHeight: 1.6, margin: 0 }}>{card.body as string}</p>
                </div>
              ))}
            </div>
          </div>
          <div style={{ opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(20px)", transition: "all 0.6s 0.12s ease" }}>
            <div style={{ background: `linear-gradient(180deg, ${T.bgCard}, ${T.bgDeep})`, borderRadius: C.cardRadius, padding: "22px 22px 18px", border: `${C.cardBorderWidth}px solid ${topic.color}24`, marginBottom: 16 }}>
              <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: 2.2, color: topic.colorLight, fontFamily: T.fontDisplay, marginBottom: 10 }}>Story Notes</div>
              <div style={{ display: "grid", gap: 10 }}>
                {(topic.talkingPoints || []).map((point, index) => (
                  <div key={`${point}-${index}`} style={{ display: "grid", gridTemplateColumns: "26px 1fr", gap: 10, alignItems: "start", paddingTop: index === 0 ? 0 : 10, borderTop: index === 0 ? "none" : `1px solid ${topic.color}14` }}>
                    <div style={{ width: 22, height: 22, borderRadius: "50%", background: `${topic.color}16`, color: topic.colorLight, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 11, fontWeight: 700 }}>{index + 1}</div>
                    <p style={{ fontSize: 13, color: T.textMuted, lineHeight: 1.6, margin: 0 }}>{point}</p>
                  </div>
                ))}
              </div>
            </div>
            <div style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "20px 22px", borderTop: `${C.accentBarHeight}px solid ${topic.color}` }}>
              <div style={{ fontFamily: T.fontDisplay, fontSize: 24, color: T.text, marginBottom: 10 }}>{topic.callout}</div>
              <div style={{ width: 96, height: 3, borderRadius: 999, background: `linear-gradient(90deg, ${topic.color}, ${topic.colorLight})` }} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default TwoColLayout;
export { TwoColLayout };
