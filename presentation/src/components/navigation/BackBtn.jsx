/**
 * BackBtn — minimal back-navigation button using the active theme tokens.
 *
 * @param {object} props
 * @param {function} props.onClick - Handler invoked when the button is clicked.
 */

import React from "react";
import PropTypes from "prop-types";
import { useTheme } from "../hooks/useTheme.js";
import { usePresentationViewport } from "../hooks/usePresentationViewport.js";

export function BackBtn({ onClick }) {
  const T = useTheme();
  const viewport = usePresentationViewport();

  return (
    <button
      onClick={onClick}
      style={{
        background: "none",
        border: "none",
        color: T.textDim,
        fontSize: viewport.isPhone ? 12 : 13,
        cursor: "pointer",
        fontFamily: T.fontDisplay,
        marginBottom: viewport.isPhone ? 14 : 20,
        display: "flex",
        alignItems: "center",
        gap: 6,
        padding: 0,
      }}
    >
      <span>&larr;</span> Back
    </button>
  );
}

BackBtn.propTypes = {
  onClick: PropTypes.func.isRequired,
};

export default BackBtn;
