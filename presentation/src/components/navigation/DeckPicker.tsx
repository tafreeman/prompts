/**
 * DeckPicker — horizontal button group for switching between deck variants.
 *
 * Highlights the active deck using the current theme's accent color.
 */

import React from "react";
import { useTheme } from "../hooks/useTheme.js";
import { useChrome } from "../hooks/useChrome.js";

interface DeckMeta {
  title: string;
  titleAccent?: string;
}

interface DeckPickerProps {
  decks: Record<string, DeckMeta>;
  selectedDeckId: string;
  onSelectDeck: (deckKey: string) => void;
}

export function DeckPicker({ decks, selectedDeckId, onSelectDeck }: DeckPickerProps) {
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

export default DeckPicker;
