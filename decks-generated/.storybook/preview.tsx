import React, { useEffect } from 'react';
import type { Preview } from '@storybook/react';
import { ThemeContext } from '../src/components/context/ThemeContext.js';
import { StyleContext } from '../src/components/context/StyleContext.js';
import { THEMES, THEMES_BY_ID, THEME_FONT_URLS } from '../src/tokens/themes.js';
import { STYLE_MODES, STYLE_MODES_BY_ID } from '../src/tokens/style-modes.js';
import type { ThemeId } from '../src/tokens/themes.js';
import type { StyleModeId } from '../src/tokens/style-modes.js';

/**
 * Font loader component — injects a Google Fonts <link> for the active theme.
 */
function FontLoader({ themeId }: { readonly themeId: ThemeId }) {
  useEffect(() => {
    const id = 'storybook-google-fonts';
    let link = document.getElementById(id) as HTMLLinkElement | null;
    if (!link) {
      link = document.createElement('link');
      link.id = id;
      link.rel = 'stylesheet';
      document.head.appendChild(link);
    }
    link.href = THEME_FONT_URLS[themeId];
  }, [themeId]);

  return null;
}

const preview: Preview = {
  globalTypes: {
    theme: {
      name: 'Theme',
      description: 'Deck color theme',
      defaultValue: 'midnight-teal',
      toolbar: {
        icon: 'paintbrush',
        items: THEMES.map((t) => ({ value: t.id, title: t.name })),
        dynamicTitle: true,
      },
    },
    styleMode: {
      name: 'Style Mode',
      description: 'Visual chrome variant',
      defaultValue: 'clean',
      toolbar: {
        icon: 'component',
        items: STYLE_MODES.map((s) => ({ value: s.id, title: s.name })),
        dynamicTitle: true,
      },
    },
  },
  decorators: [
    (Story, context) => {
      const themeId = (context.globals.theme ?? 'midnight-teal') as ThemeId;
      const styleModeId = (context.globals.styleMode ?? 'clean') as StyleModeId;
      const theme = THEMES_BY_ID[themeId];
      const styleMode = STYLE_MODES_BY_ID[styleModeId];

      return (
        <ThemeContext.Provider value={theme}>
          <StyleContext.Provider value={styleMode}>
            <FontLoader themeId={themeId} />
            <div
              style={{
                width: 960,
                height: 540,
                background: theme.bg,
                padding: 40,
                fontFamily: `"${theme.fontBody}", system-ui, sans-serif`,
                color: theme.text,
                overflow: 'hidden',
                position: 'relative',
              }}
            >
              <Story />
            </div>
          </StyleContext.Provider>
        </ThemeContext.Provider>
      );
    },
  ],
};

export default preview;
