import React, { useState } from "react";
import { DeckPicker } from "../../../components/navigation/DeckPicker.tsx";

export default {
  title: "Navigation/DeckPicker",
  component: DeckPicker,
  parameters: {
    layout: "padded",
  },
};

const twoDecks = {
  native: { title: "Native", titleAccent: "" },
  onboarding: { title: "Onboarding", titleAccent: "" },
};

const threeDecks = {
  executive: { title: "Executive", titleAccent: "Summary" },
  engineering: { title: "Engineering", titleAccent: "Deep Dive" },
  onboarding: { title: "Onboarding", titleAccent: "Guide" },
};

const accentDecks = {
  "midnight-teal": { title: "Midnight", titleAccent: "Teal" },
  "gamma-dark": { title: "Gamma", titleAccent: "Dark" },
  "slate-amber": { title: "Slate", titleAccent: "Amber" },
};

export const Default = {
  args: {
    decks: twoDecks,
    selectedDeckId: "native",
    onSelectDeck: () => {},
  },
  render: (args) => (
    <div>
      <DeckPicker {...args} />
    </div>
  ),
};

export const SecondSelected = {
  args: {
    decks: twoDecks,
    selectedDeckId: "onboarding",
    onSelectDeck: () => {},
  },
  render: (args) => (
    <div>
      <DeckPicker {...args} />
    </div>
  ),
};

export const ThreeDecks = {
  args: {
    decks: threeDecks,
    selectedDeckId: "engineering",
    onSelectDeck: () => {},
  },
  render: (args) => (
    <div>
      <DeckPicker {...args} />
    </div>
  ),
};

export const WithTitleAccents = {
  args: {
    decks: accentDecks,
    selectedDeckId: "midnight-teal",
    onSelectDeck: () => {},
  },
  render: (args) => (
    <div>
      <DeckPicker {...args} />
    </div>
  ),
};

export const Interactive = {
  render: () => {
    const [selected, setSelected] = useState("executive");

    return (
      <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
        <DeckPicker
          decks={threeDecks}
          selectedDeckId={selected}
          onSelectDeck={setSelected}
        />
        <p style={{ fontSize: 12, opacity: 0.55, margin: 0 }}>
          Active deck: <strong>{selected}</strong> — click the buttons above to switch.
        </p>
      </div>
    );
  },
};

export const SingleDeckHidden = {
  render: () => (
    <div>
      <p style={{ fontSize: 12, opacity: 0.55, marginBottom: 12 }}>
        DeckPicker renders nothing when only one deck is provided (returns null).
      </p>
      <DeckPicker
        decks={{ onboarding: { title: "Onboarding", titleAccent: "" } }}
        selectedDeckId="onboarding"
        onSelectDeck={() => {}}
      />
      <p style={{ fontSize: 12, opacity: 0.4, fontStyle: "italic" }}>
        (no picker rendered above this line)
      </p>
    </div>
  ),
};
