// Caminho completo: D:\mindscan\frontend\src\pages\NotFound.tsx

/**
 * ===========================================================================
 *  MindScan — NotFound Page (404)
 *  Arquitetura: React 18 + TS + Vite + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Finalidade: Página exibida quando a rota não é encontrada
 * ===========================================================================
 */

export default function NotFound() {
    return (
        <div className="w-full h-screen flex flex-col items-center justify-center bg-gray-50 animate-fade-in text-center p-6">
            <h1 className="text-6xl font-bold text-indigo-600 mb-4">404</h1>
            <h2 className="text-2xl font-semibold tracking-tight mb-2">Página não encontrada</h2>
            <p className="text-gray-600 max-w-md">
                A rota acessada não existe. Verifique o endereço digitado ou retorne à página inicial.
            </p>
        </div>
    );
}