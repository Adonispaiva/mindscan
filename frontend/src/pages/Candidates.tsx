// Caminho completo: D:\mindscan\frontend\src\pages\Candidates.tsx

/**
 * ==========================================================================
 *  MindScan — Candidates Page
 *  Arquitetura: React 18 + TS + Vite + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Finalidade: Listagem e gerenciamento de candidatos avaliados
 * ==========================================================================
 */

export default function Candidates() {
    return (
        <div className="w-full h-full flex flex-col gap-6 animate-fade-in">
            {/* Header */}
            <div>
                <h1 className="text-2xl font-semibold tracking-tight">Candidatos</h1>
                <p className="text-gray-600 mt-1">
                    Visualize, filtre e gerencie todos os candidatos avaliados pela SynMind.
                </p>
            </div>

            {/* Table Placeholder */}
            <div className="ms-card">
                <h3 className="text-lg font-semibold mb-4">Lista de Candidatos</h3>
                <p className="text-gray-500">A tabela completa será adicionada em breve.</p>
            </div>
        </div>
    );
}