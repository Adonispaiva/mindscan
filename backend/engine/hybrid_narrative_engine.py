# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\hybrid_narrative_engine.py
# Última atualização: 2025-12-11T09:59:20.792728

# ============================================================
# MindScan — Hybrid Narrative Engine
# ============================================================
# Responsável por:
# - Gerar narrativa psicodinâmica híbrida
# - Integrar insights, scores e padrões comportamentais
# - Criar linguagem estruturada para relatórios
# ============================================================

from typing import Dict, Any, List


class HybridNarrativeEngine:

    def __init__(self):
        pass

    def generate(self, insights: Dict[str, Any], normalized: Dict[str, Any]) -> List[str]:
        """
        Monta a narrativa híbrida a partir dos módulos consolidados.
        A narrativa é composta por blocos temáticos.
        """

        narrative = []

        # ------------------------------------------------------------
        # 1. Abertura — Identidade Psicométrica Global
        # ------------------------------------------------------------
        narrative.append(
            "A análise integrada sugere um padrão cognitivo-comportamental "
            "combinando elementos estruturais e emocionais de forma híbrida."
        )

        # ------------------------------------------------------------
        # 2. Construções a partir de insights chave
        # ------------------------------------------------------------
        for key, text in insights.items():
            narrative.append(f"- {text}")

        # ------------------------------------------------------------
        # 3. Observações derivadas de blocos normalizados
        # ------------------------------------------------------------
        try:
            big5 = normalized.get("big5", {})
            openness = big5.get("O", {}).get("score", None)
            if openness and openness > 60:
                narrative.append(
                    "Há um indicativo de elevada abertura à experiência, "
                    "relacionada a criatividade e busca por novidade."
                )
        except Exception:
            pass

        try:
            buss = normalized.get("bussola", {})
            mag = buss.get("directions", {}).get("magnitude", 0)
            if mag > 3:
                narrative.append(
                    "A intensidade direcional sugere motivação marcante e foco aplicado."
                )
        except Exception:
            pass

        # ------------------------------------------------------------
        # 4. Fechamento
        # ------------------------------------------------------------
        narrative.append(
            "A síntese híbrida completa reforça as tendências dominantes e "
            "indica pontos estratégicos de desenvolvimento pessoal."
        )

        return narrative
