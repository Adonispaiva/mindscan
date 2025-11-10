// ===============================================================
//  ENTRY POINT: FRONTEND MINDSCAN
//  Projeto: MindScan — SynMind MI v2.0
//  Autor: Leo Vinci (GPT Inovexa)
//  Data: 07/11/2025
//  Função: Inicialização global do frontend React
// ===============================================================

import React from "react";
import ReactDOM from "react-dom/client";
import AppRoutes from "@/AppRoutes";
import "@/index.css";

// ShadCN / Tailwind / Framer Motion já integrados via vite.config

// ---------------------------------------------------------------
// Renderização principal da aplicação
// ---------------------------------------------------------------
ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <AppRoutes />
  </React.StrictMode>
);

// ---------------------------------------------------------------
// Service Worker opcional para PWA
// ---------------------------------------------------------------
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("/sw.js")
      .then((reg) => console.log("[MindScan] Service Worker registrado:", reg.scope))
      .catch((err) => console.warn("[MindScan] Erro no Service Worker:", err));
  });
}
