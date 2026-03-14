/**
 * StatValue — bold number with a caption label beneath it.
 *
 * @param {object} props
 * @param {string} props.value - The primary stat (e.g. "~90%", "0", "14").
 * @param {string} props.label - Descriptive caption below the value.
 * @param {string} [props.color] - Override color for the value (defaults to theme.accent).
 */

import React from "react";
import PropTypes from "prop-types";
import { useTheme } from "../hooks/useTheme.js";
import { TYPE_SCALE } from "../../tokens/type-scale.js";

export function StatValue({ value, label, color }) {
  const theme = useTheme();

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

StatValue.propTypes = {
  value: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  color: PropTypes.string,
};
