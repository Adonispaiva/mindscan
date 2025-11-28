"""
BackendManager — Inovexa MindScan
Diretor Técnico: Leo Vinci

Responsável por:
    - Integrar o backend ao main.py da raiz
    - Inicializar API + Workers (quando implementados)
    - Padronizar logs e isolamentos de exceção
    - Garantir boot consistente do ecossistema interno
"""

import traceback
from pathlib import Path
from datetime import datetime


class BackendManager:
    """
    O BackendManager é o gateway oficial entre o main (raiz)
    e o backend interno do MindScan.

    O main raiz detecta automaticamente este manager
    porque ele expõe o método `run()`.
    """

    @staticmethod
    def _log(msg: str):
        """Log padronizado do Backend Manager."""
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[BackendManager {ts}] {msg}")

    @staticmethod
    def run():
        """
        Método chamado pelo main raiz.
        Inicializa o backend via start_backend().
        """
        BackendManager._log("Iniciando backend...")

        try:
            # Determina raiz do projeto MindScan
            ROOT = Path(__file__).resolve().parents[1]
            backend_path = ROOT / "backend"

            if not backend_path.exists():
                BackendManager._log("[ERRO] Pasta backend/ não encontrada.")
                return

            # Importa dinamicamente o backend
            from backend.main import start_backend

            BackendManager._log("Chamando start_backend()...")
            start_backend()

            BackendManager._log("Backend iniciado com sucesso.")

        except Exception as e:
            BackendManager._log(f"[ERRO CRÍTICO] Falha ao iniciar backend: {e}")
            traceback.print_exc()
