import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

// Side-effect: register all layout components before first render.
import './layouts/register-all.js';

import App from './App.js';

const root = document.getElementById('root');
if (!root) throw new Error('Root element #root not found');

createRoot(root).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
