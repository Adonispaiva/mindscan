# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\mi_hybrid_router.py
# Última atualização: 2025-12-11T09:59:20.818000

# ============================================================
# MindScan — MI Hybrid Router
# ============================================================
# Responsável por:
# - Receber requisições MI
# - Determinar o modo de processamento
# - Gerenciar fallback seguro
# - Expor interface para o backend (API/Engine)
# ============================================================

from typing import Dict, Any
from .mi_engine_hybrid import MIEngineHybrid


class MIHybridRouter:

    def __init__(self):
        self.engine = MIEngineHybrid()

    def run(self, payload: Dict[str, Any], mode: str = None) -> Dict[str, Any]:

        mode = (mode or "hybrid_auto").strip().lower()

        try:
            response = self.engine.compute(payload, mode=mode)
            return {
                "status": "ok",
                "mode_used": mode,
                "response": response
            }

        except Exception as e:
            # FAILSAFE ABSOLUTO
            fallback = self.engine.compute(payload, mode="classic")
            return {
                "status": "fallback",
                "mode_used": "classic",
                "error": str(e),
                "response": fallback
            }
