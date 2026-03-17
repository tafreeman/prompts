/**
 * useChrome — access the active style mode from ChromeContext.
 * Throws if used outside a ChromeContext.Provider.
 */

import { useContext } from "react";
import type { StyleMode } from "../../tokens/style-modes.ts";
import { ChromeContext } from "../context/ChromeContext.ts";

export function useChrome(): StyleMode {
  const chrome = useContext(ChromeContext);
  if (!chrome) {
    throw new Error("useChrome must be used within a ChromeContext.Provider");
  }
  return chrome;
}

export default useChrome;
