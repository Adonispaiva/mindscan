/**
 * ==========================================================================
 *  MindScan — Home Page
 *  Arquitetura: React 18 + TS + Vite + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Finalidade: Página inicial do sistema (visão geral)
 * ==========================================================================
 */

export default function Home() {
    return (
        <div className="w-full h-full flex flex-col gap-6 animate-fade-in">
            {/* Header */}
            <div>
                <h1 className="text-2xl font-semibold tracking-tight">Bem-vindo ao MindScan</h1>
                <p className="text-gray-600 mt-1">
                    Sistema de diagnóstico psicoprofissional da SynMind.
                </p>
            </div>

            {/* Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="ms-card">
                    <h3 className="text-lg font-semibold mb-2">Testes ativos</h3>
                    <p className="text-gray-600">Gerencie e acompanhe testes em andamento.</p>
                </div>

                <div className="ms-card">
                    <h3 className="text-lg font-semibold mb-2">Candidatos</h3>
                    <p className="text-gray-600">Lista e análise dos perfis avaliados.</p>
                </div>

                <div className="ms-card">
                    <h3 className="text-lg font-semibold mb-2">Relatórios</h3>
                    <p className="text-gray-600">Geração e consulta de diagnósticos completos.</p>
                </div>

                <div className="ms-card">
                    <h3 className="text-lg font-semibold mb-2">Configurações</h3>
                    <p className="text-gray-600">Ajustes gerais e preferências da plataforma.</p>
                </div>
            </div>
        </div>
    );
}
