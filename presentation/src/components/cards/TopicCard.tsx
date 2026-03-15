/**
 * TopicCard — generic content card with title, body, and optional icon.
 *
 * A flexible card component for rendering topic-level content blocks
 * across different deck layouts.
 *
 * @example
 *   <TopicCard
 *     title="Prompt Standardization"
 *     body="Established versioned prompt templates with embedded architecture context."
 *     icon="📋"
 *     color="#22D3EE"
 *   />
 */

import React from "react";

import { useTheme } from "../hooks/useTheme.js";
import { useChrome } from "../hooks/useChrome.js";
import type { Theme } from "../../tokens/themes.ts";
import type { StyleMode } from "../../tokens/style-modes.ts";

interface TopicCardProps {
  /** card heading */
  title: string;
  /** card body text */
  body: string;
  /** optional emoji or icon string */
  icon?: string;
  /** accent colour override */
  color?: string;
  /** optional click handler */
  onClick?: (e?: React.MouseEvent) => void;
}

function TopicCard({ title, body, icon, color, onClick }: TopicCardProps): React.ReactElement {
  const T: Theme = useTheme();
  const C: StyleMode = useChrome();

  const accent = color || T.text;
  const isClickable = typeof onClick === "function";

  return (
    <div
      role={isClickable ? "button" : undefined}
      tabIndex={isClickable ? 0 : undefined}
      onClick={onClick}
      onKeyDown={
        isClickable
          ? (e: React.KeyboardEvent<HTMLDivElement>) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                onClick(e as unknown as React.MouseEvent);
              }
            }
          : undefined
      }
      style={{
        background: T.bgCard,
        borderRadius: C.cardRadius,
        padding: "24px 28px",
        borderLeft: `${C.accentBarHeight + 1}px solid ${accent}`,
        cursor: isClickable ? "pointer" : "default",
        transition: "transform 0.3s ease, box-shadow 0.3s ease",
      }}
    >
      {icon && (
        <div
          style={{
            fontSize: 28,
            marginBottom: 12,
            lineHeight: 1,
          }}
        >
          {icon}
        </div>
      )}

      <h3
        style={{
          fontFamily: T.fontDisplay,
          fontSize: 17,
          fontWeight: C.headingWeight,
          color: accent,
          margin: "0 0 10px",
        }}
      >
        {title}
      </h3>

      {body && (
        <p
          style={{
            fontSize: 13.5,
            color: T.textMuted,
            lineHeight: 1.6,
            margin: 0,
          }}
        >
          {body}
        </p>
      )}
    </div>
  );
}

export default TopicCard;
