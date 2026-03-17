/**
 * ChecklistLayout — approved / prohibited checklist screen.
 *
 * Extracted from genai_advocacy_hub_13.jsx (ChecklistScreen, layout id: "checklist").
 */

import { useState, useEffect } from "react";
import { useTheme } from "../../components/hooks/useTheme.ts";
import { useChrome } from "../../components/hooks/useChrome.ts";
import { usePresentationViewport } from "../../components/hooks/usePresentationViewport.ts";
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

interface ChecklistItem {
  icon?: string;
  title?: string;
  desc?: string;
}

interface ItemProps {
  item: ChecklistItem;
  delay: number;
}

export function ChecklistLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme() as Theme;
  const C = useChrome() as StyleMode;
  const viewport = usePresentationViewport();
  const [entered, setEntered] = useState<boolean>(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 60); return () => clearTimeout(t); }, []);
  const Item = ({ item, delay }: ItemProps) => (
    <div style={{ display: "flex", gap: 10, padding: "10px 14px", borderRadius: C.innerRadius, background: T.bgDeep, marginBottom: 8, opacity: entered ? 1 : 0, transform: entered ? "none" : "translateX(-12px)", transition: `all 0.4s ${delay}s ease` }}>
      <div style={{ fontSize: 16, flexShrink: 0, marginTop: 1 }}>{item.icon}</div>
      <div>
        <div style={{ fontFamily: T.fontDisplay, fontSize: 13, fontWeight: C.headingWeight, color: T.text, marginBottom: 3 }}>{item.title}</div>
        <p style={{ fontSize: 12, color: T.textMuted, lineHeight: 1.5, margin: 0 }}>{item.desc}</p>
      </div>
    </div>
  );
  return (
    <div style={{ position: "relative", minHeight: "100dvh", background: T.bg, overflowX: "hidden", overflowY: viewport.overlayScroll }}>
      <Particles color={topic.color} active={entered} />
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1100, margin: "0 auto", padding: `${viewport.pagePaddingTop}px ${viewport.pagePaddingX}px ${viewport.pagePaddingBottom}px` }}>
        <BackBtn onClick={onBack} />
        <SectionHeader topic={topic} entered={entered} />
        <div style={{ display: "grid", gridTemplateColumns: viewport.isCompact ? "1fr" : "1fr 1fr", gap: viewport.cardGap }}>
          <div>
            <div style={{ fontSize: 10, fontFamily: T.fontDisplay, fontWeight: C.headingWeight, color: T.success, letterSpacing: 2.5, textTransform: "uppercase", marginBottom: 12 }}>Approved</div>
            {((topic.approved as ChecklistItem[]) || []).map((item, i) => <Item key={i} item={item} delay={0.15 + i * 0.06} />)}
            {topic.awareness && (
              <>
                <div style={{ fontSize: 10, fontFamily: T.fontDisplay, fontWeight: C.headingWeight, color: T.warning, letterSpacing: 2.5, textTransform: "uppercase", marginTop: 16, marginBottom: 12 }}>Awareness Only</div>
                {(topic.awareness as ChecklistItem[]).map((item, i) => <Item key={`a${i}`} item={item} delay={0.5 + i * 0.06} />)}
              </>
            )}
          </div>
          <div>
            <div style={{ fontSize: 10, fontFamily: T.fontDisplay, fontWeight: C.headingWeight, color: T.danger, letterSpacing: 2.5, textTransform: "uppercase", marginBottom: 12 }}>Prohibited</div>
            {((topic.forbidden as ChecklistItem[]) || []).map((item, i) => <Item key={i} item={item} delay={0.2 + i * 0.06} />)}
          </div>
        </div>
        <div style={{ marginTop: 28, padding: "18px 22px", borderLeft: `${C.accentBarHeight}px solid ${T.accent}`, background: T.bgCard, borderRadius: `0 ${C.innerRadius}px ${C.innerRadius}px 0` }}>
          <p style={{ fontSize: 14, color: T.text, lineHeight: 1.65, margin: 0, fontWeight: 600 }}>&ldquo;{topic.callout}&rdquo;</p>
        </div>
      </div>
    </div>
  );
}

export default ChecklistLayout;
