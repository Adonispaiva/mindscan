/**
 * ==========================================================================
 *  MindScan — App Router
 *  Arquitetura: React 18 + TS + Vite + React Router DOM v6
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Finalidade: Gerenciar rotas principais da aplicação
 * ==========================================================================
 */

import { createBrowserRouter } from "react-router-dom";
import BaseLayout from "../layouts/BaseLayout";

// Páginas (serão criadas nos próximos turnos)
import Home from "../pages/Home";
import Dashboard from "../pages/Dashboard";
import Tests from "../pages/Tests";
import TestDetails from "../pages/TestDetails";
import Candidates from "../pages/Candidates";
import CandidateDetails from "../pages/CandidateDetails";
import Reports from "../pages/Reports";
import ReportDetails from "../pages/ReportDetails";
import Settings from "../pages/Settings";
import Login from "../pages/Login";
import Register from "../pages/Register";
import NotFound from "../pages/NotFound";

export const router = createBrowserRouter([
    {
        path: "/",
        element: (
            <BaseLayout>
                <Home />
            </BaseLayout>
        )
    },
    {
        path: "/dashboard",
        element: (
            <BaseLayout>
                <Dashboard />
            </BaseLayout>
        )
    },
    {
        path: "/tests",
        element: (
            <BaseLayout>
                <Tests />
            </BaseLayout>
        )
    },
    {
        path: "/tests/:id",
        element: (
            <BaseLayout>
                <TestDetails />
            </BaseLayout>
        )
    },
    {
        path: "/candidates",
        element: (
            <BaseLayout>
                <Candidates />
            </BaseLayout>
        )
    },
    {
        path: "/candidates/:id",
        element: (
            <BaseLayout>
                <CandidateDetails />
            </BaseLayout>
        )
    },
    {
        path: "/reports",
        element: (
            <BaseLayout>
                <Reports />
            </BaseLayout>
        )
    },
    {
        path: "/reports/:id",
        element: (
            <BaseLayout>
                <ReportDetails />
            </BaseLayout>
        )
    },
    {
        path: "/settings",
        element: (
            <BaseLayout>
                <Settings />
            </BaseLayout>
        )
    },
    {
        path: "/login",
        element: <Login />
    },
    {
        path: "/register",
        element: <Register />
    },
    {
        path: "*",
        element: <NotFound />
    }
]);
