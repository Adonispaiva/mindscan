/**
 * ==========================================================================
 *  MindScan — BaseLayout
 *  Arquitetura: React 18 + TS + Vite + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Finalidade: Estrutura global da aplicação (Navbar + Sidebar + Conteúdo)
 * ==========================================================================
 */

import { ReactNode } from "react";
import { Sidebar } from "../components/layout/Sidebar";
import { Navbar } from "../components/layout/Navbar";

interface BaseLayoutProps {
    children: ReactNode;
}

export default function BaseLayout({ children }: BaseLayoutProps) {
    return (
        <div className="w-full min-h-screen flex bg-gray-50 text-gray-900">
            {/* Sidebar */}
            <aside className="w-64 border-r border-gray-200 bg-white">
                <Sidebar />
            </aside>

            {/* Main Area */}
            <div className="flex flex-col flex-1 min-h-screen">
                {/* Top Navigation */}
                <header className="h-16 border-b border-gray-200 bg-white">
                    <Navbar />
                </header>

                {/* Content */}
                <main className="flex-1 p-6 overflow-auto">
                    {children}
                </main>
            </div>
        </div>
    );
}
S