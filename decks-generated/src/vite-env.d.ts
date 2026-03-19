/// <reference types="vite/client" />

/** Allow importing YAML files as raw strings via Vite's `?raw` suffix. */
declare module '*.yaml?raw' {
  const content: string;
  export default content;
}
