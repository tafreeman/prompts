/**
 * useChrome — access the active style mode from ChromeContext.
 * Throws if used outside a ChromeContext.Provider.
 */

import { useContext } from "react";
import { ChromeContext } from "../context/ChromeContext.js";

export function useChrome() {
  const chrome = useContext(ChromeContext);
  if (!chrome) {
    throw new Error("useChrome must be used within a ChromeContext.Provider");
  }
  return chrome;
}

export default useChrome;
