/**
 * OptionalDeckLink — landing-page navigation card for optional deck topics.
 *
 * Ported from v10.2 genai_advocacy_hub_10_v2.0.jsx.
 * Shows a wider, visually distinct card below the main tile grid for
 * topics marked `optional: true` (e.g. one-pager companion slides).
 */

import { useState, useRef, useCallback } from "react";
import type { Theme } from "../../tokens/themes.ts";

interface TopicShape {
  id: string;
  icon?: string;
  title: string;
  summary?: string;
  subtitle?: string;
  heroPoints?: string[];
  talkingPoints?: string[];
  color?: string;
  colorGlow?: string;
}

interface ChromeShape {
  cardRadius: number | string;
  [key: string]: unknown;
}

interface NavigateOrigin {
  x: number;
  y: number;
}

interface OptionalDeckLinkProps {
  topic: TopicShape;
  theme: Theme;
  chrome: ChromeShape;
  onNavigate: (topicId: string, origin: NavigateOrigin) => void;
}

export function OptionalDeckLink({ topic, theme: T, chrome: C, onNavigate }: OptionalDeckLinkProps) {
  const [hovered, setHovered] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  const handleClick = useCallback(() => {
    if (!ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    onNavigate(topic.id, { x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 });
  }, [topic.id, onNavigate]);

  return (
    <div
      ref={ref}
      role="button"
      tabIndex={0}
      onClick={handleClick}
      onKeyDown={(e: React.KeyboardEvent<HTMLDivElement>) => { if (e.key === "Enter") handleClick(); }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        display: "flex",
        flexDirection: "row",
        gap: 16,
        marginTop: 16,
        background: `linear-gradient(135deg, ${T.bgCard}, ${T.bgDeep || T.bg})`,
        border: `1px solid ${(topic.color || T.accent) + "30"}`,
        borderBottom: `3px solid ${topic.color || T.accent}`,
        borderRadius: C.cardRadius,
        padding: 20,
        cursor: "pointer",
        transform: hovered ? "translateY(-4px)" : "none",
        boxShadow: hovered
          ? `0 14px 48px rgba(0,0,0,0.24), 0 0 40px ${(topic.colorGlow || topic.color || T.accent) + "18"}`
          : "0 2px 12px rgba(0,0,0,0.15)",
        transition: "transform 0.25s cubic-bezier(0.22,1,0.36,1), box-shadow 0.25s ease",
        maxWidth: "100%",
        outline: "none",
      }}
    >
      {/* Left section: icon + title + summary + hero points */}
      <div style={{ flex: 1, minWidth: 0 }}>
        {topic.icon && (
          <div style={{ fontSize: 26, marginBottom: 6 }}>{topic.icon}</div>
        )}
        <div style={{
          fontFamily: T.fontDisplay,
          fontSize: 20,
          fontWeight: 700,
          color: T.text,
          lineHeight: 1.15,
        }}>
          {topic.title}
        </div>
        {(topic.summary || topic.subtitle) && (
          <div style={{
            fontSize: 12.5,
            color: T.textMuted,
            lineHeight: 1.5,
            marginTop: 6,
            maxWidth: 400,
          }}>
            {topic.summary || topic.subtitle}
          </div>
        )}
        {(topic.heroPoints || []).length > 0 && (
          <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginTop: 10 }}>
            {topic.heroPoints!.map((pt, i) => (
              <span
                key={i}
                style={{
                  border: `1px solid ${(topic.color || T.accent) + "40"}`,
                  borderRadius: 999,
                  padding: "3px 10px",
                  fontSize: 10,
                  color: topic.color || T.accent,
                  letterSpacing: 0.4,
                }}
              >
                {pt}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Right section: talking points + navigation link */}
      <div style={{ width: 190, flexShrink: 0, display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
        <div>
          {(topic.talkingPoints || []).slice(0, 2).map((pt, i) => (
            <div key={i} style={{
              fontSize: 11,
              color: T.textDim,
              lineHeight: 1.4,
              marginBottom: 6,
              paddingLeft: 10,
              borderLeft: `2px solid ${T.accent}30`,
            }}>
              {pt}
            </div>
          ))}
        </div>
        <div style={{
          fontSize: 11,
          color: T.accent,
          fontWeight: 600,
          letterSpacing: 0.3,
          marginTop: 8,
          display: "flex",
          alignItems: "center",
          gap: 4,
        }}>
          Open the one-pager
          <span style={{
            display: "inline-block",
            transform: hovered ? "translateX(4px)" : "none",
            transition: "transform 0.2s ease",
          }}>
            →
          </span>
        </div>
      </div>
    </div>
  );
}

export default OptionalDeckLink;
