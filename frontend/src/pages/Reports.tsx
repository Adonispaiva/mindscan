// Caminho completo: D:\mindscan\frontend\src\pages\Reports.tsx (informado separadamente acima)

/**
 * ===========================================================================
 *  MindScan — Reports Page
 *  Arquitetura: React 18 + TS + Vite + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Finalidade: Página de listagem de relatórios gerados pela SynMind
 * ===========================================================================
 */

export default function Reports() {
    return (
        <div className="w-full h-full flex flex-col gap-6 animate-fade-in">
            {/* Header */}
            <div>
                <h1 className="text-2xl font-semibold tracking-tight">Relatórios</h1>
                <p className="text-gray-600 mt-1">
                    Acesse todos os relatórios psicoprofissionais já gerados.
                </p>
            </div>

            {/* Placeholder */}
            <div className="ms-card">
                <h3 className="text-lg font-semibold mb-4">Lista de Relatórios</h3>
                <p className="text-gray-500">A lista completa será adicionada em breve.</p>
            </div>
        </div>
    );
}