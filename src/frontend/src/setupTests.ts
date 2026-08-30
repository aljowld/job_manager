import { afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';

// `globals: false` in vite.config.ts means RTL's auto-cleanup detection
// (which relies on a global `afterEach`) does not kick in on its own.
afterEach(() => {
  cleanup();
});
