import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  // Use relative asset paths so the built presentation can be opened
  // directly from the filesystem (for example by double-clicking index.html).
  base: './',
  plugins: [react()],
});
