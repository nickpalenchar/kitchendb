import path from 'node:path';
import { defineConfig } from 'vite';
import solidPlugin from 'vite-plugin-solid';

const outputDir = path.join(__dirname, '..', '..', 'static', 'components');

export default defineConfig({
  plugins: [solidPlugin()],
  server: {
    port: 3000,
  },
  build: {
    target: 'esnext',
    rollupOptions: {
      input: ['src/App.tsx'],
      output: {
        entryFileNames: '[name].js',
        dir: outputDir,
      }
    } 
  },
});
