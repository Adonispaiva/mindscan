// Caminho completo: D:\mindscan\frontend\src\pages\ReportDetails.tsx

/**
 * ===========================================================================
 *  MindScan — ReportDetails Page
 *  Arquitetura: React 18 + TS + Vite + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Finalidade: Exibir detalhes completos de um relatório gerado
 * ===========================================================================
 */

import { useParams } from "react-router-dom";

export default function ReportDetails() {
    const { id } = useParams();

    return (
        <div className="w-full h-full flex flex-col gap-6 animate-fade-in">
            {/* Header */}
            <div>
                <h1 className="text-2xl font-semibold tracking-tight">Detalhes do Relatório</h1>
                <p className="text-gray-600 mt-1">
                    Visualização completa do relatório psicoprofissional.
                </p>
            </div>

            {/* Report ID */}
            <div className="ms-card">
                <h3 className="text-lg font-semibold mb-1">ID do Relatório</h3>
                <p className="text-gray-700 text-sm">{id}</p>
            </div>

            {/* Placeholder para dados futuros */}
            <div className="ms-card h-64 flex items-center justify-center text-gray-500">
                Conteúdo completo do relatório (coming soon)
            </div>
        </div>
    );
}
