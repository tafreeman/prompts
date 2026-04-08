# Agentic Workflows UI

React 19 + Vite 6 dashboard for running and inspecting Agentic Workflows.

## Quick Start

```bash
cd agentic-workflows-v2/ui
npm install

npm run dev          # Dev server on :5173 (proxies /api and /ws)
npm run build        # Type check + production bundle
npm run test         # Vitest suite
npm run test:coverage
```

Backend proxy:
- Defaults to `http://localhost:8010`. Override with `VITE_API_PROXY_TARGET=http://<host>:<port>` when running the backend elsewhere.

## Architecture Notes

- Entry: `src/main.tsx` renders the app and query client providers.
- Routing & views: `src/routes/` and `src/pages/` (React Router 7).
- Flow visualization: `@xyflow/react` under `src/components/graph/`.
- Data fetching: `@tanstack/react-query` with backend API clients in `src/api/`.

Keep backend (`agentic-workflows-v2` FastAPI app) running for live data; the proxy forwards `/api` and `/ws` to the configured target.
