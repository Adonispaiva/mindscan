# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\hybrid_insight_engine.py
# Última atualização: 2025-12-11T09:59:20.792728

# ============================================================
# MindScan — Hybrid Insight Engine
# ============================================================
# Responsável por gerar insights avançados combinando:
# - padrões psicométricos
# - variações entre blocos
# - correlações híbridas
# - narrativa inferencial elevada
# ============================================================

from typing import Dict, Any


class HybridInsightEngine:

    def __init__(self):
        pass

    def generate(self, normalized: Dict[str, Any], reasoning: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera insights híbridos combinando inferências e métricas normalizadas.
        """

        insights = {}

        # ------------------------------------------------------------
        # 1. Integração Big Five + TEIQue
        # ------------------------------------------------------------
        big5 = normalized.get("big5", {})
        teique = normalized.get("teique", {})

        try:
            o_score = big5.get("O", {}).get("score", 0)
            emotion_reg = teique.get("EmotionalRegulation", {}).get("score", 0)

            if o_score > 60 and emotion_reg > 55:
                insights["creative_emotional_synergy"] = (
                    "Combinação rara de criatividade elevada com regulação emocional sólida."
                )
            elif o_score > 60 and emotion_reg < 40:
                insights["creative_emotional_tension"] = (
                    "Criatividade alta acompanhada de instabilidade emocional."
                )
        except Exception:
            pass

        # ------------------------------------------------------------
        # 2. Cruzamentos OCAI + Esquemas
        # ------------------------------------------------------------
        ocai = normalized.get("ocai", {})
        esquemas = normalized.get("esquemas", {})

        if "Hierarchy" in ocai and "Vulnerability" in esquemas:
            hv = esquemas["Vulnerability"]["score"]
            if hv > 60:
                insights["organizational_vulnerability_marker"] = (
                    "Tendência a absorver pressão hierárquica de forma sensível."
                )

        # ------------------------------------------------------------
        # 3. Heurística de consistência entre módulos
        # ------------------------------------------------------------
        if "directions" in normalized.get("bussola", {}):
            intensity = normalized["bussola"]["directions"].get("magnitude", 0)
            if intensity > 3:
                insights["directional_intensity"] = "Alta intensidade comportamental detectada."

        # ------------------------------------------------------------
        # 4. Inclusão do raciocínio de primeira camada
        # ------------------------------------------------------------
        insights.update(reasoning)

        return insights
