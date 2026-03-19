import { createContext } from 'react';
import type { StyleMode } from '../../tokens/style-modes.js';
import { STYLE_MODES } from '../../tokens/style-modes.js';

/** React context for the active style mode. Default: clean (first style mode). */
export const StyleContext = createContext<StyleMode>(STYLE_MODES[0]);
