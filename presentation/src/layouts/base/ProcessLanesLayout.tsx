/**
 * ProcessLanesLayout — service-platform screen with capabilities, tabbed focus
 * panels, process lanes, talking points, and callout.
 *
 * Layout ID: "process-lanes"
 * Extracted from genai_advocacy_hub_13.jsx PlatformScreen (lines 1068-1153).
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

function ProcessLanesLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme() as Theme;
  const C = useChrome() as StyleMode;
  const viewport = usePresentationViewport();
  const [entered, setEntered] = useState<boolean>(false);
  const [activePanel, setActivePanel] = useState<number>(0);

  useEffect(() => {
    const timer = setTimeout(() => setEntered(true), 50);
    return () => clearTimeout(timer);
  }, []);

  const focusPanels = (topic.focusPanels as Record<string, unknown>[]) ?? [];
  const capabilities = (topic.capabilities as Record<string, unknown>[]) ?? [];
  const lanes = (topic.lanes as Record<string, unknown>[]) ?? [];

  return (
    <div style={{ position: "relative", minHeight: "100dvh", background: T.bg, overflowX: "hidden", overflowY: viewport.overlayScroll }}>
      <Particles color={topic.color} type="future" active={entered} />
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1240, margin: "0 auto", padding: `${viewport.pagePaddingTop}px ${viewport.pagePaddingX}px ${viewport.pagePaddingBottom}px` }}>
        <BackBtn onClick={onBack} />
        <div style={{ display: "grid", gridTemplateColumns: viewport.isCompact ? "1fr" : "1.05fr 0.95fr", gap: viewport.cardGap, marginBottom: 18 }}>
          <div style={{ opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(20px)", transition: "all 0.6s ease" }}>
            <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: 3, color: topic.colorLight, fontFamily: T.fontDisplay, marginBottom: 8 }}>{topic.eyebrow || "Service Platform"}</div>
            <h1 style={{ fontFamily: T.fontDisplay, fontSize: viewport.titleSize, color: T.text, margin: "0 0 10px", lineHeight: 1.06 }}>{topic.title}</h1>
            <p style={{ fontSize: viewport.subtitleSize, color: topic.colorLight, fontStyle: "italic", lineHeight: 1.5, margin: "0 0 14px" }}>{topic.subtitle}</p>
            {topic.summary && <p style={{ fontSize: viewport.bodySize, color: T.textMuted, lineHeight: 1.7, margin: "0 0 18px" }}>{topic.summary}</p>}
            <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 18 }}>
              {(topic.heroPoints ?? []).map((point) => (
                <span key={point} style={{ padding: "7px 12px", borderRadius: C.pillRadius, background: `${topic.color}12`, border: `1px solid ${topic.color}24`, fontSize: 12, color: T.text }}>{point}</span>
              ))}
            </div>
            <div style={{ display: "grid", gridTemplateColumns: viewport.isPhone ? "1fr" : "repeat(2, minmax(0, 1fr))", gap: 12 }}>
              {capabilities.map((capability, index) => (
                <div key={`${capability.title as string}-${index}`} style={{ background: T.bgCard, borderRadius: C.innerRadius, padding: "14px 16px", borderLeft: `${C.accentBarHeight}px solid ${topic.color}`, opacity: entered ? 1 : 0, transform: entered ? "translateX(0)" : "translateX(-14px)", transition: `all 0.45s ${0.18 + index * 0.08}s ease` }}>
                  <div style={{ fontFamily: T.fontDisplay, fontSize: 17, color: T.text, marginBottom: 6 }}>{capability.title as string}</div>
                  <p style={{ fontSize: 13.5, color: T.textMuted, lineHeight: 1.6, margin: 0 }}>{capability.body as string}</p>
                </div>
              ))}
            </div>
          </div>
          <div style={{ opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(20px)", transition: "all 0.6s 0.12s ease" }}>
            <div style={{ display: "flex", gap: 8, marginBottom: 12, flexWrap: "wrap" }}>
              {focusPanels.map((panel, index) => (
                <button key={`${panel.label as string}-${index}`} onClick={() => setActivePanel(index)} style={{ border: `1px solid ${index === activePanel ? topic.color : `${topic.color}20`}`, background: index === activePanel ? `${topic.color}18` : T.bgCard, color: index === activePanel ? topic.colorLight : T.textDim, borderRadius: C.pillRadius, padding: "7px 12px", fontSize: 12, cursor: "pointer", fontFamily: T.fontBody }}>{panel.label as string}</button>
              ))}
            </div>
            <div style={{ background: `linear-gradient(180deg, ${T.bgCard}, ${T.bgDeep})`, borderRadius: C.cardRadius, padding: "18px 20px", border: `${C.cardBorderWidth}px solid ${topic.color}24`, marginBottom: 14 }}>
              <div style={{ fontFamily: T.fontDisplay, fontSize: 24, color: T.text, marginBottom: 8 }}>{focusPanels[activePanel]?.title as string}</div>
              <p style={{ fontSize: 14, color: T.textMuted, lineHeight: 1.65, margin: 0 }}>{focusPanels[activePanel]?.body as string}</p>
            </div>
            <div style={{ display: "grid", gap: 12 }}>
              {lanes.map((lane, index) => (
                <div key={`${lane.title as string}-${index}`} style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "16px 18px", borderTop: `${C.accentBarHeight}px solid ${(lane.accent as string) || topic.color}` }}>
                  <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: 2.5, color: (lane.accent as string) || topic.colorLight, fontFamily: T.fontDisplay, marginBottom: 6 }}>{lane.title as string}</div>
                  <div style={{ fontFamily: T.fontDisplay, fontSize: 20, color: T.text, marginBottom: 6 }}>{lane.subtitle as string}</div>
                  <p style={{ fontSize: 12.5, color: T.textDim, margin: "0 0 12px" }}>{lane.persona as string}</p>
                  <div style={{ display: "grid", gap: 8 }}>
                    {((lane.steps as string[]) ?? []).map((step, stepIndex) => (
                      <div key={`${step}-${stepIndex}`} style={{ display: "grid", gridTemplateColumns: "24px 1fr", gap: 10, alignItems: "start" }}>
                        <div style={{ width: 22, height: 22, borderRadius: "50%", background: `${(lane.accent as string) || topic.color}18`, color: (lane.accent as string) || topic.colorLight, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 11, fontWeight: 700 }}>{stepIndex + 1}</div>
                        <p style={{ fontSize: 13, color: T.textMuted, lineHeight: 1.55, margin: 0 }}>{step}</p>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
        {(topic.talkingPoints?.length ?? 0) > 0 && (
          <div style={{ background: T.bgCard, borderRadius: 14, padding: viewport.isPhone ? "14px 14px" : "16px 18px", borderLeft: `4px solid ${topic.color}`, marginBottom: 14 }}>
            <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: 2.5, color: topic.colorLight, fontFamily: T.fontDisplay, marginBottom: 8 }}>Talking Points</div>
            <div style={{ display: "grid", gridTemplateColumns: viewport.isPhone ? "1fr" : "repeat(2, minmax(0, 1fr))", gap: 10 }}>
              {topic.talkingPoints!.map((point, index) => (
                <div key={`${point}-${index}`} style={{ fontSize: 13, color: T.textMuted, lineHeight: 1.6 }}>{point}</div>
              ))}
            </div>
          </div>
        )}
        <div style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "18px 20px", borderLeft: `${C.accentBarHeight + 1}px solid ${topic.color}` }}>
          <p style={{ fontFamily: T.fontDisplay, fontSize: 24, color: T.text, margin: 0 }}>{topic.callout}</p>
        </div>
      </div>
    </div>
  );
}

export default ProcessLanesLayout;
export { ProcessLanesLayout };
