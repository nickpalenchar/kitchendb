import path from 'node:path';
import { defineConfig } from 'vite';
import solidPlugin from 'vite-plugin-solid';
import fs from 'node:fs/promises'

const outputDir = path.join(__dirname, '..', '..', 'static', 'components');

const entrypoints: string[] = []
for (const file of await fs.readdir(path.join(__dirname, 'src'))) {
  console.log(file);
  // Capitalized files are exported.
  if (file[0] === file[0].toUpperCase() && !['.$_'].includes(file[0])) {
    entrypoints.push(path.join('src', file));
  }
};

export default defineConfig({
  plugins: [solidPlugin()],
  server: {
    port: 3000,
  },
  build: {
    target: 'es2015',
    emptyOutDir: true,
    rollupOptions: {
      input: entrypoints,
      output: {
        entryFileNames: '[name].js',
        dir: outputDir,
        globals: {
          window: 'window'
        }
      }
    }
  },
});
