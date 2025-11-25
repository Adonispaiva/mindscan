# ============================================================
# MindScan — TEIQue Algorithm
# ============================================================
# Algoritmo psicométrico do TEIQue (Inteligência Emocional
# Traço), composto pelas dimensões:
#
# - Bem-estar
# - Autocontrole
# - Emocionalidade
# - Sociabilidade
#
# Funções:
# - Processamento de itens
# - Normalização via ScoreBuilder
# - Geração de descritores
# - Estrutura compatível com DiagnosticEngine
#
# Versão final e maximizada.
# ============================================================

from typing import Dict, Any
from backend.core.scoring import ScoreBuilder


class TEIQueAlgorithm:
    """
    Processador completo do TEIQue.
    """

    DIMENSIONS = {
        "wellbeing": ["wb1", "wb2", "wb3", "wb4"],
        "selfcontrol": ["sc1", "sc2", "sc3", "sc4"],
        "emotionality": ["em1", "em2", "em3", "em4"],
        "sociability": ["so1", "so2", "so3", "so4"],
    }

    DESCRIPTORS = {
        "wellbeing": "Propensão ao otimismo, autoconfiança e estabilidade emocional.",
        "selfcontrol": "Capacidade de regular impulsos, emoções e comportamentos sob pressão.",
        "emotionality": "Consciência emocional, empatia e clareza sobre os próprios sentimentos.",
        "sociability": "Habilidade de interação social, assertividade e comunicação.",
    }

    def __init__(self):
        self.scoring = ScoreBuilder()

    # ------------------------------------------------------------
    # PROCESSAR TEIQUE
    # ------------------------------------------------------------
    def compute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa o cálculo completo do TEIQue.
        """

        results = {}

        for dimension, keys in self.DIMENSIONS.items():
            raw_values = [data.get(k, 0) for k in keys]
            raw_score = sum(raw_values) / len(raw_values)

            score_obj = self.scoring.build(
                dimension=dimension,
                raw_score=raw_score,
                minimum=1,
                maximum=7,
                descriptor=self.DESCRIPTORS[dimension],
                metadata={
                    "items": keys,
                    "raw_values": raw_values
                }
            )

            results[dimension] = score_obj

        # Score global do TEIQue
        overall = sum(v["score"] for v in results.values()) / 4

        results["overall"] = {
            "dimension": "teique_overall",
            "score": round(overall, 2),
            "descriptor": "Índice geral de Inteligência Emocional Traço (TEIQue).",
            "metadata": {"dimensions": list(self.DIMENSIONS.keys())}
        }

        return results


# Instância pública
teique = TEIQueAlgorithm()
