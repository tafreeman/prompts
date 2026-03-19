import { useContext } from 'react';
import type { StyleMode } from '../../tokens/style-modes.js';
import { StyleContext } from '../context/StyleContext.js';

/** Read the active style mode from context. */
export function useStyle(): StyleMode {
  return useContext(StyleContext);
}
