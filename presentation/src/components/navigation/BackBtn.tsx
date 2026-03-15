/**
 * BackBtn — minimal back-navigation button using the active theme tokens.
 */

import React from "react";
import { useTheme } from "../hooks/useTheme.js";
import { usePresentationViewport } from "../hooks/usePresentationViewport.js";

interface BackBtnProps {
  onClick: () => void;
}

export function BackBtn({ onClick }: BackBtnProps) {
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

export default BackBtn;
