/**
 * DeckPicker — horizontal button group for switching between deck variants.
 *
 * Highlights the active deck using the current theme's accent color.
 *
 * @param {object} props
 * @param {Record<string, {title: string, titleAccent: string}>} props.decks - Map of deck id to metadata.
 * @param {string} props.selectedDeckId - Currently active deck key.
 * @param {function} props.onSelectDeck - Called with the deck key when clicked.
 */

import React from "react";
import PropTypes from "prop-types";
import { useTheme } from "../hooks/useTheme.js";
import { useChrome } from "../hooks/useChrome.js";

export function DeckPicker({ decks, selectedDeckId, onSelectDeck }) {
  const T = useTheme();
  const C = useChrome();

  if (Object.keys(decks).length <= 1) {
    return null;
  }

  return (
    <div style={{ display: "flex", gap: 4 }}>
      {Object.entries(decks).map(([key, d]) => (
        <button
          key={key}
          onClick={() => onSelectDeck(key)}
          style={{
            background: key === selectedDeckId ? `${T.accent}20` : T.bgCard,
            border: `1px solid ${key === selectedDeckId ? T.accent : T.textDim + "30"}`,
            borderRadius: C.pillRadius,
            padding: "5px 12px",
            fontSize: 10,
            color: key === selectedDeckId ? T.accent : T.textDim,
            cursor: "pointer",
            fontFamily: T.fontBody,
            textTransform: "uppercase",
            letterSpacing: 0.8,
          }}
        >
          {d.title} {d.titleAccent}
        </button>
      ))}
    </div>
  );
}

DeckPicker.propTypes = {
  decks: PropTypes.objectOf(
    PropTypes.shape({
      title: PropTypes.string.isRequired,
      titleAccent: PropTypes.string,
    })
  ).isRequired,
  selectedDeckId: PropTypes.string.isRequired,
  onSelectDeck: PropTypes.func.isRequired,
};

export default DeckPicker;
