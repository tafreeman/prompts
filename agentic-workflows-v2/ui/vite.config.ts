import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

const API_PROXY_TARGET = process.env.VITE_API_PROXY_TARGET || "http://localhost:8010";
const WS_PROXY_TARGET = API_PROXY_TARGET.replace(/^http/i, "ws");

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
  server: {
    port: 5173,
    proxy: {
      "/api": API_PROXY_TARGET,
      "/ws": {
        target: WS_PROXY_TARGET,
        ws: true,
      },
    },
  },
});
