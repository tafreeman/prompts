/**
 * ThemeContext — provides the active theme's token values to all descendants.
 *
 * Mirrors the ThemeCtx from genai_advocacy_hub_13.jsx line 15.
 * The monolith passes the full theme object (from THEMES array).
 */

import { createContext } from "react";
import type { Theme } from "../../tokens/themes.ts";
import { THEMES } from "../../tokens/themes.ts";

export const ThemeContext = createContext<Theme>(THEMES[0]);

export default ThemeContext;
