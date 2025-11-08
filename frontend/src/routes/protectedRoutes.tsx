// ===============================================================
//  MÓDULO: PROTECTED ROUTES
//  Projeto: MindScan — SynMind MI v2.0
//  Autor: Leo Vinci (GPT Inovexa)
//  Data: 07/11/2025
//  Função: Controle de acesso hierárquico (Usuário / Admin / Inovexa)
// ===============================================================

import React from "react";
import { Navigate } from "react-router-dom";

// ---------------------------------------------------------------
// Estrutura de papéis de acesso
// ---------------------------------------------------------------
export type UserRole = "user" | "admin" | "inovexa";

// ---------------------------------------------------------------
// Interface esperada de autenticação global
// ---------------------------------------------------------------
interface AuthContextType {
  isAuthenticated: boolean;
  role: UserRole;
  token?: string;
}

// Simulação de hook de contexto (deve ser integrado ao auth real)
const useAuth = (): AuthContextType => {
  const stored = localStorage.getItem("mindscan_auth");
  if (!stored) return { isAuthenticated: false, role: "user" };
  try {
    const parsed = JSON.parse(stored);
    return parsed;
  } catch {
    return { isAuthenticated: false, role: "user" };
  }
};

// ---------------------------------------------------------------
// Componente de rota protegida
// ---------------------------------------------------------------
interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRole?: UserRole;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, requiredRole = "user" }) => {
  const auth = useAuth();

  if (!auth.isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Hierarquia: inovexa > admin > user
  const hierarchy = { user: 1, admin: 2, inovexa: 3 };

  if (hierarchy[auth.role] < hierarchy[requiredRole]) {
    return <Navigate to="/unauthorized" replace />;
  }

  return <>{children}</>;
};

// ---------------------------------------------------------------
// Utilitários de rotas rápidas
// ---------------------------------------------------------------
export const UserRoute = ({ children }: { children: React.ReactNode }) => (
  <ProtectedRoute requiredRole="user">{children}</ProtectedRoute>
);

export const AdminRoute = ({ children }: { children: React.ReactNode }) => (
  <ProtectedRoute requiredRole="admin">{children}</ProtectedRoute>
);

export const InovexaRoute = ({ children }: { children: React.ReactNode }) => (
  <ProtectedRoute requiredRole="inovexa">{children}</ProtectedRoute>
);

// ---------------------------------------------------------------
// Exemplo de uso (em App.tsx ou Router principal)
//
// <Routes>
//   <Route path="/dashboard" element={<AdminRoute><AdminDashboard /></AdminRoute>} />
//   <Route path="/inovexa/ctrl" element={<InovexaRoute><InovexaControlPanel /></InovexaRoute>} />
//   <Route path="/diagnostico" element={<UserRoute><DiagnosticPage /></UserRoute>} />
// </Routes>
// ---------------------------------------------------------------
