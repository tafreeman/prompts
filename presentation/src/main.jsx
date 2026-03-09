import React, { lazy, Suspense, useState, useEffect } from 'react';
import ReactDOM from 'react-dom/client';

const VARIANTS = {
  v10:   { label: 'v10 — Original',   load: () => import('../genai_advocacy_hub_10.jsx') },
  v10_2: { label: 'v10.2 — Enhanced',  load: () => import('../genai_advocacy_hub_10_v2.0.jsx') },
  v13:   { label: 'v13 — Latest',     load: () => import('../genai_advocacy_hub_13.jsx') },
};

const DEFAULT_KEY = 'v13';

function getInitialKey() {
  const param = new URLSearchParams(window.location.search).get('app');
  return param && VARIANTS[param] ? param : DEFAULT_KEY;
}

// Lazy-wrap each variant once so React caches the resolved module
const lazyComponents = Object.fromEntries(
  Object.entries(VARIANTS).map(([key, { load }]) => [
    key,
    lazy(load),
  ])
);

const pickerStyle = {
  position: 'fixed',
  top: 12,
  right: 12,
  zIndex: 99999,
  display: 'flex',
  gap: 6,
  background: 'rgba(0,0,0,0.65)',
  backdropFilter: 'blur(12px)',
  borderRadius: 8,
  padding: '6px 10px',
  fontFamily: 'system-ui, sans-serif',
  fontSize: 13,
};

const btnBase = {
  border: 'none',
  borderRadius: 6,
  padding: '5px 12px',
  cursor: 'pointer',
  fontSize: 13,
  fontWeight: 600,
  transition: 'all 0.15s',
};

function Picker({ active, onChange }) {
  return (
    <div style={pickerStyle}>
      {Object.entries(VARIANTS).map(([key, { label }]) => (
        <button
          key={key}
          onClick={() => onChange(key)}
          style={{
            ...btnBase,
            background: key === active ? '#22D3EE' : 'rgba(255,255,255,0.08)',
            color: key === active ? '#0B1426' : 'rgba(255,255,255,0.7)',
          }}
        >
          {label}
        </button>
      ))}
    </div>
  );
}

function Root() {
  const [activeKey, setActiveKey] = useState(getInitialKey);

  useEffect(() => {
    const url = new URL(window.location);
    url.searchParams.set('app', activeKey);
    window.history.replaceState(null, '', url);
  }, [activeKey]);

  const ActiveApp = lazyComponents[activeKey];

  return (
    <>
      <Picker active={activeKey} onChange={setActiveKey} />
      <Suspense fallback={<LoadingScreen />}>
        <ActiveApp />
      </Suspense>
    </>
  );
}

function LoadingScreen() {
  return (
    <div style={{
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      height: '100vh', background: '#0B1426', color: '#22D3EE',
      fontFamily: 'system-ui', fontSize: 18,
    }}>
      Loading...
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Root />
  </React.StrictMode>
);
