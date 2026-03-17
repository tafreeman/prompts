/**
 * ChromeContext — provides the active style mode to all descendants.
 *
 * Mirrors the ChromeCtx from genai_advocacy_hub_13.jsx line 16.
 * Style modes control card radius, glow, borders, heading weight, etc.
 */

import { createContext } from "react";
import type { StyleMode } from "../../tokens/style-modes.ts";
import { STYLE_MODES_BY_ID } from "../../tokens/style-modes.ts";

export const ChromeContext = createContext<StyleMode>(STYLE_MODES_BY_ID["default"]);

export default ChromeContext;
