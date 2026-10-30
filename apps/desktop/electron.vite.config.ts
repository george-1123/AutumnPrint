import { defineConfig } from 'electron-vite';

export default defineConfig({
  main: { build: { externalizeDeps: false } },
  preload: { build: { externalizeDeps: false, rollupOptions: { output: { format: 'cjs', entryFileNames: 'index.cjs' } } } },
  renderer: {}
});
