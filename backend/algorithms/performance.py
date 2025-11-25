# ============================================================
# MindScan — Performance Algorithm
# ============================================================
# Algoritmo responsável por medir competências de performance:
#
# - Produtividade
# - Foco
# - Organização
# - Adaptabilidade
# - Resolução de Problemas
#
# Cada dimensão é formada por um conjunto de itens.
# O algoritmo:
# - soma pontuações
# - normaliza via ScoreBuilder
# - gera descritores
# - consolida score geral de performance
#
# Versão completa e maximizada.
# ============================================================

from typing import Dict, Any
from backend.core.scoring import ScoreBuilder


class PerformanceAlgorithm:
    """
    Implementação completa do algoritmo de Performance.
    """

    DIMENSIONS = {
        "productivity": ["p1", "p2", "p3", "p4"],
        "focus": ["f1", "f2", "f3", "f4"],
        "organization": ["o1", "o2", "o3", "o4"],
        "adaptability": ["a1", "a2", "a3", "a4"],
        "problemsolving": ["s1", "s2", "s3", "s4"]
    }

    DESCRIPTORS = {
        "productivity": "Nível de entrega, disciplina de execução e consistência de resultados.",
        "focus": "Capacidade de manter atenção sustentada e evitar dispersões.",
        "organization": "Planejamento, estruturação e controle de tarefas.",
        "adaptability": "Flexibilidade para lidar com mudanças e cenários incertos.",
        "problemsolving": "Habilidade de diagnóstico, análise e solução de problemas."
    }

    def __init__(self):
        self.scoring = ScoreBuilder()

    # ------------------------------------------------------------
    # EXECUTAR PERFORMANCE
    # ------------------------------------------------------------
    def compute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Computa todas as dimensões de performance.
        """

        results = {}

        for dim, keys in self.DIMENSIONS.items():
            raw_values = [data.get(k, 0) for k in keys]
            raw_score = sum(raw_values) / len(raw_values)

            score_obj = self.scoring.build(
                dimension=dim,
                raw_score=raw_score,
                minimum=1,
                maximum=5,
                descriptor=self.DESCRIPTORS[dim],
                metadata={
                    "items": keys,
                    "raw_values": raw_values
                }
            )

            results[dim] = score_obj

        # Score geral de performance
        overall = sum(v["score"] for v in results.values()) / len(results)

        results["overall"] = {
            "dimension": "performance_overall",
            "score": round(overall, 2),
            "descriptor": "Índice geral de performance psicoprofissional.",
            "metadata": {"dimensions": list(self.DIMENSIONS.keys())}
        }

        return results


# Instância pública
performance = PerformanceAlgorithm()
