/**
 * useTheme — access the active theme from ThemeContext.
 * Throws if used outside a ThemeContext.Provider.
 */

import { useContext } from "react";
import { ThemeContext } from "../context/ThemeContext.js";

export function useTheme() {
  const theme = useContext(ThemeContext);
  if (!theme) {
    throw new Error("useTheme must be used within a ThemeContext.Provider");
  }
  return theme;
}

export default useTheme;
