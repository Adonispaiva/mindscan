// ===============================================================
//  CONFIGURAÇÃO: VITE.JS
//  Projeto: MindScan — SynMind MI v2.0
//  Autor: Leo Vinci (GPT Inovexa)
//  Data: 07/11/2025
//  Função: Configuração de bundler, alias e otimizações de build
// ===============================================================

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

// ---------------------------------------------------------------
//  Configuração principal
// ---------------------------------------------------------------
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 5173,
    open: true,
    cors: true,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        secure: false,
      },
      "/inovexa-admin": {
        target: "http://localhost:8000",
        changeOrigin: true,
        secure: false,
      },
    },
  },
  build: {
    outDir: "dist",
    sourcemap: false,
    minify: "esbuild",
    target: "esnext",
    chunkSizeWarningLimit: 600,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom", "framer-motion"],
          ui: ["@/components/ui"],
        },
      },
    },
  },
  css: {
    postcss: "./postcss.config.js",
  },
  define: {
    "process.env": process.env,
  },
});
