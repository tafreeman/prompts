import React from "react";
import { ThemeContext, ChromeContext } from "../src/components/context/index.js";
import { THEMES } from "../src/tokens/themes.ts";
import { STYLE_MODES, STYLE_MODES_BY_ID } from "../src/tokens/style-modes.ts";

const defaultTheme = THEMES[0]; // midnight-teal
const defaultChrome = STYLE_MODES_BY_ID["default"];

/** @type {import('@storybook/react-vite').Preview} */
const preview = {
  tags: ["autodocs"],
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    a11y: {
      test: "todo",
    },
  },

  initialGlobals: {
    theme: "midnight-teal",
    chrome: "default",
  },

  globalTypes: {
    theme: {
      name: "Theme",
      description: "Presentation color theme",
      toolbar: {
        icon: "paintbrush",
        items: THEMES.map((t) => ({ value: t.id, title: t.name })),
        dynamicTitle: true,
      },
    },
    chrome: {
      name: "Chrome",
      description: "Style mode (card shape, glow, borders)",
      toolbar: {
        icon: "grid",
        items: STYLE_MODES.map((m) => ({ value: m.id, title: m.name })),
        dynamicTitle: true,
      },
    },
  },

  decorators: [
    (Story, context) => {
      const themeId = context.globals.theme || "midnight-teal";
      const chromeId = context.globals.chrome || "default";
      const theme = THEMES.find((t) => t.id === themeId) || defaultTheme;
      const chrome = STYLE_MODES_BY_ID[chromeId] || defaultChrome;

      return (
        <ThemeContext.Provider value={theme}>
          <ChromeContext.Provider value={chrome}>
            <link href={theme.fontsUrl} rel="stylesheet" />
            <div
              style={{
                background: theme.bg,
                padding: 32,
                minHeight: "100vh",
                color: theme.text,
                fontFamily: theme.fontBody,
              }}
            >
              <Story />
            </div>
          </ChromeContext.Provider>
        </ThemeContext.Provider>
      );
    },
  ],
};

export default preview;
