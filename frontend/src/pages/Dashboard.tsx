/**
 * ===========================================================================
 *  MindScan — Dashboard Page
 *  Arquitetura: React 18 + TS + Vite + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Finalidade: Visão geral dinâmica com widgets e métricas
 * ===========================================================================
 */

export default function Dashboard() {
    return (
        <div className="w-full h-full flex flex-col gap-6 animate-fade-in">
            {/* Header */}
            <div>
                <h1 className="text-2xl font-semibold tracking-tight">Dashboard</h1>
                <p className="text-gray-600 mt-1">
                    Panorama geral das operações do MindScan.
                </p>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="ms-card">
                    <h3 className="text-lg font-semibold mb-1">Testes ativos</h3>
                    <p className="text-3xl font-bold text-indigo-600">14</p>
                </div>

                <div className="ms-card">
                    <h3 className="text-lg font-semibold mb-1">Candidatos</h3>
                    <p className="text-3xl font-bold text-indigo-600">128</p>
                </div>

                <div className="ms-card">
                    <h3 className="text-lg font-semibold mb-1">Relatórios gerados</h3>
                    <p className="text-3xl font-bold text-indigo-600">62</p>
                </div>

                <div className="ms-card">
                    <h3 className="text-lg font-semibold mb-1">Pendências</h3>
                    <p className="text-3xl font-bold text-red-500">3</p>
                </div>
            </div>

            {/* Placeholder for charts & upcoming modules */}
            <div className="ms-card h-64 flex items-center justify-center text-gray-500">
                Gráficos e análises (coming soon)
            </div>
        </div>
    );
}
