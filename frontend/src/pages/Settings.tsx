// Caminho completo: D:\mindscan\frontend\src\pages\Settings.tsx

/**
 * ===========================================================================
 *  MindScan — Settings Page
 *  Arquitetura: React 18 + TS + Vite + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Finalidade: Configurações gerais da plataforma MindScan
 * ===========================================================================
 */

export default function Settings() {
    return (
        <div className="w-full h-full flex flex-col gap-6 animate-fade-in">
            {/* Header */}
            <div>
                <h1 className="text-2xl font-semibold tracking-tight">Configurações</h1>
                <p className="text-gray-600 mt-1">
                    Ajuste preferências e parâmetros gerais do sistema.
                </p>
            </div>

            {/* Placeholder */}
            <div className="ms-card">
                <h3 className="text-lg font-semibold mb-4">Preferências Gerais</h3>
                <p className="text-gray-500">As configurações completas serão adicionadas em breve.</p>
            </div>
        </div>
    );
}