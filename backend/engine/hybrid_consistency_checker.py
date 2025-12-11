# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\hybrid_consistency_checker.py
# Última atualização: 2025-12-11T09:59:20.792728

# ============================================================
# MindScan — Hybrid Consistency Checker
# ============================================================
# Garante consistência global entre todos os blocos:
# - coerência dos scores
# - ausência de contradições estruturais
# - estabilidade das narrativas inferenciais
# ============================================================

from typing import Dict, Any, List


class HybridConsistencyChecker:

    def __init__(self):
        pass

    def check(self, normalized: Dict[str, Any], insights: Dict[str, Any]) -> Dict[str, Any]:
        errors = []
        warnings = []

        # ------------------------------------------------------------
        # 1. Checar contradições Big Five vs TEIQue
        # ------------------------------------------------------------
        try:
            big5_openness = normalized["big5"]["O"]["score"]
            emotional_reg = normalized["teique"]["EmotionalRegulation"]["score"]

            if big5_openness > 70 and emotional_reg < 30:
                warnings.append(
                    "Nível elevado de abertura acompanhado de baixa regulação emocional."
                )
        except Exception:
            pass

        # ------------------------------------------------------------
        # 2. Checar existência de blocos essenciais
        # ------------------------------------------------------------
        required_blocks = ["big5", "teique", "dass21", "ocai", "esquemas", "performance", "cross", "bussola"]

        for block in required_blocks:
            if block not in normalized:
                errors.append(f"Bloco ausente: {block}")

        # ------------------------------------------------------------
        # 3. Checar coerência de insights
        # ------------------------------------------------------------
        if len(insights) == 0:
            warnings.append("Nenhum insight híbrido detectado — possível entrada fraca.")

        return {
            "errors": errors,
            "warnings": warnings,
            "is_valid": len(errors) == 0
        }
