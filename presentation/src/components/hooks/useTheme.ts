/**
 * useTheme — access the active theme from ThemeContext.
 * Throws if used outside a ThemeContext.Provider.
 */

import { useContext } from "react";
import type { Theme } from "../../tokens/themes.ts";
import { ThemeContext } from "../context/ThemeContext.ts";

export function useTheme(): Theme {
  const theme = useContext(ThemeContext);
  if (!theme) {
    throw new Error("useTheme must be used within a ThemeContext.Provider");
  }
  return theme;
}

export default useTheme;
