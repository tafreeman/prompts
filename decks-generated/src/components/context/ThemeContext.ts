import { createContext } from 'react';
import type { Theme } from '../../tokens/themes.js';
import { THEMES } from '../../tokens/themes.js';

/** React context for the active theme. Default: midnight-teal (first theme). */
export const ThemeContext = createContext<Theme>(THEMES[0]);
