import { useContext } from 'react';
import type { Theme } from '../../tokens/themes.js';
import { ThemeContext } from '../context/ThemeContext.js';

/** Read the active theme from context. */
export function useTheme(): Theme {
  return useContext(ThemeContext);
}
