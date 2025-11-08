// ===============================================================
//  MÓDULO: APP ROUTES
//  Projeto: MindScan — SynMind MI v2.0
//  Autor: Leo Vinci (GPT Inovexa)
//  Data: 07/11/2025
//  Função: Definir e organizar as rotas principais do sistema
// ===============================================================

import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

// Páginas do sistema
import LoginAdmin from "@/pages/LoginAdmin";
import AdminPanelMilena from "@/pages/AdminPanelMilena";
import InovexaControlPanel from "@/pages/InovexaControlPanel";

// Rotas protegidas
import { UserRoute, AdminRoute, InovexaRoute } from "@/routes/protectedRoutes";

// Páginas públicas (usuário final)
import DiagnosticPage from "@/pages/DiagnosticPage";
import ReportPage from "@/pages/ReportPage";
import NotFound from "@/pages/NotFound";

// ---------------------------------------------------------------
//  Roteador principal
// ---------------------------------------------------------------
export default function AppRoutes() {
  return (
    <Router>
      <Routes>

        {/* =====================
            ÁREA PÚBLICA — Usuários Finais
           ===================== */}
        <Route path="/" element={<Navigate to="/diagnostico" replace />} />
        <Route
          path="/diagnostico"
          element={
            <UserRoute>
              <DiagnosticPage />
            </UserRoute>
          }
        />
        <Route
          path="/relatorio"
          element={
            <UserRoute>
              <ReportPage />
            </UserRoute>
          }
        />

        {/* =====================
            ÁREA ADMINISTRATIVA — Milena (SynMind)
           ===================== */}
        <Route
          path="/login"
          element={<LoginAdmin />}
        />
        <Route
          path="/admin"
          element={
            <AdminRoute>
              <AdminPanelMilena />
            </AdminRoute>
          }
        />

        {/* =====================
            ÁREA TÉCNICA — Inovexa
           ===================== */}
        <Route
          path="/inovexa/ctrl"
          element={
            <InovexaRoute>
              <InovexaControlPanel />
            </InovexaRoute>
          }
        />

        {/* =====================
            PÁGINAS GENÉRICAS
           ===================== */}
        <Route path="/unauthorized" element={<div className="p-8 text-center text-red-400">Acesso não autorizado.</div>} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}
