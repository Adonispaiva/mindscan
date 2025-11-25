// Caminho completo: D:\mindscan\frontend\src\pages\Login.tsx

/**
 * ===========================================================================
 *  MindScan — Login Page
 *  Arquitetura: React 18 + TS + Vite + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Finalidade: Autenticação do usuário para acesso ao MindScan
 * ===========================================================================
 */

export default function Login() {
    return (
        <div className="w-full h-screen flex items-center justify-center bg-gray-50 animate-fade-in">
            <div className="ms-card w-full max-w-md p-8">
                <h1 className="text-2xl font-semibold tracking-tight mb-6">Acessar MindScan</h1>

                <form className="flex flex-col gap-4">
                    <div className="flex flex-col gap-1">
                        <label className="text-sm font-medium">Email</label>
                        <input type="email" placeholder="seuemail@dominio.com" />
                    </div>

                    <div className="flex flex-col gap-1">
                        <label className="text-sm font-medium">Senha</label>
                        <input type="password" placeholder="••••••••" />
                    </div>

                    <button
                        type="submit"
                        className="w-full py-2 rounded-lg bg-indigo-600 text-white font-medium hover:bg-indigo-700 transition-all"
                    >
                        Entrar
                    </button>
                </form>
            </div>
        </div>
    );
}