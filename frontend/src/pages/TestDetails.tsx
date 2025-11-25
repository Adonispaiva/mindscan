// Caminho completo: D:\mindscan\frontend\src\pages\TestDetails.tsx

/**
 * ==========================================================================
 *  MindScan — TestDetails Page
 *  Arquitetura: React 18 + TS + Vite + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Finalidade: Página de detalhes de um teste psicométrico
 * ==========================================================================
 */

import { useParams } from "react-router-dom";

export default function TestDetails() {
    const { id } = useParams();

    return (
        <div className="w-full h-full flex flex-col gap-6 animate-fade-in">
            {/* Header */}
            <div>
                <h1 className="text-2xl font-semibold tracking-tight">Detalhes do Teste</h1>
                <p className="text-gray-600 mt-1">
                    Informações completas sobre o teste selecionado.
                </p>
            </div>

            {/* Test ID */}
            <div className="ms-card">
                <h3 className="text-lg font-semibold mb-1">ID do Teste</h3>
                <p className="text-gray-700 text-sm">{id}</p>
            </div>

            {/* Conteúdo futuro */}
            <div className="ms-card h-64 flex items-center justify-center text-gray-500">
                Dados completos do teste (coming soon)
            </div>
        </div>
    );
}