// Caminho completo: D:\mindscan\frontend\src\pages\CandidateDetails.tsx

/**
 * ==========================================================================
 *  MindScan — CandidateDetails Page
 *  Arquitetura: React 18 + TS + Vite + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Finalidade: Exibir informações detalhadas de um candidato avaliado
 * ==========================================================================
 */

import { useParams } from "react-router-dom";

export default function CandidateDetails() {
    const { id } = useParams();

    return (
        <div className="w-full h-full flex flex-col gap-6 animate-fade-in">
            {/* Header */}
            <div>
                <h1 className="text-2xl font-semibold tracking-tight">Detalhes do Candidato</h1>
                <p className="text-gray-600 mt-1">
                    Informações completas sobre o candidato selecionado.
                </p>
            </div>

            {/* Candidate ID */}
            <div className="ms-card">
                <h3 className="text-lg font-semibold mb-1">ID do Candidato</h3>
                <p className="text-gray-700 text-sm">{id}</p>
            </div>

            {/* Placeholder for future profile data */}
            <div className="ms-card h-64 flex items-center justify-center text-gray-500">
                Dados completos do candidato (coming soon)
            </div>
        </div>
    );
}
