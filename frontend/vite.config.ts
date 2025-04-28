import { defineConfig } from "vite";
import react from '@vitejs/plugin-react-swc'
import path from "path";
import { componentTagger } from "lovable-tagger";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  //For local network access
  server: {
    host: "::",
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      }
    }
  },
  plugins: [
    react(),
    mode === 'development' &&
    componentTagger(),
  ].filter(Boolean),
  resolve: {
    //For simplifying import paths
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
}));
