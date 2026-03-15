/**
 * StatValue — bold number with a caption label beneath it.
 *
 * @param props.value - The primary stat (e.g. "~90%", "0", "14").
 * @param props.label - Descriptive caption below the value.
 * @param props.color - Override color for the value (defaults to theme.accent).
 */

import React from "react";
import { useTheme } from "../hooks/useTheme.js";
import { TYPE_SCALE } from "../../tokens/type-scale.ts";
import type { Theme } from "../../tokens/themes.ts";

interface StatValueProps {
  value: string;
  label: string;
  color?: string;
}

export function StatValue({ value, label, color }: StatValueProps): React.ReactElement {
  const theme: Theme = useTheme();

  return (
    <div style={{ textAlign: "center" }}>
      <div
        style={{
          ...TYPE_SCALE.STAT,
          fontFamily: theme.fontDisplay,
          color: color || theme.accent,
        }}
      >
        {value}
      </div>
      <div
        style={{
          ...TYPE_SCALE.CAPTION,
          color: theme.textDim,
        }}
      >
        {label}
      </div>
    </div>
  );
}

export default StatValue;
