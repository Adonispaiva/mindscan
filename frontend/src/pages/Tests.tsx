/**
 * ===========================================================================
 *  MindScan — Tests Page
 *  Arquitetura: React 18 + TS + Vite + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Finalidade: Listagem de testes psicométricos disponíveis/ativos
 * ===========================================================================
 */

export default function Tests() {
    return (
        <div className="w-full h-full flex flex-col gap-6 animate-fade-in">
            {/* Header */}
            <div>
                <h1 className="text-2xl font-semibold tracking-tight">Testes</h1>
                <p className="text-gray-600 mt-1">
                    Gerencie e acompanhe todos os testes psicométricos do MindScan.
                </p>
            </div>

            {/* Table Placeholder */}
            <div className="ms-card">
                <h3 className="text-lg font-semibold mb-4">Lista de Testes</h3>
                <p className="text-gray-500">A tabela completa será adicionada em breve.</p>
            </div>
        </div>
    );
}
