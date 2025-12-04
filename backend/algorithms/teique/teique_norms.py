# ================================================================
#  MindScan — TEIQue Norms
#  Categoria: Algorithm — TEIQue Norms
#  Responsável: Leo Vinci (Inovexa)
#
#  Objetivo:
#      Aplicar normas psicométricas do TEIQue para converter
#      escores brutos em escores padronizados e percentis.
#
#  API pública (compatível com versão anterior):
#      norm_engine = TeiqueNorms()
#      result = norm_engine.run(raw_scores_dict)
#
#  Saída:
#      {
#          "raw": {...},
#          "standardized": {...},
#          "percentiles": {...},
#          "metadata": {...}
#      }
# ================================================================

from typing import Dict, Any
import math


# Tabela simplificada de normas (valores médios e desvios padrão)
# Valores podem ser refinados no futuro sem quebrar a API.
NORM_TABLES = {
    "well_being": {"mean": 5.1, "sd": 1.1},
    "self_control": {"mean": 5.0, "sd": 1.2},
    "emotionality": {"mean": 5.4, "sd": 1.0},
    "sociability": {"mean": 5.2, "sd": 1.1},
    "global": {"mean": 5.2, "sd": 1.0},
}


class TeiqueNorms:
    """
    Normas psicométricas oficiais (versão simplificada) do TEIQue.
    Responsável por normalizar escores brutos em escores padronizados.
    """

    def __init__(self) -> None:
        self.norm_tables = NORM_TABLES

    # ------------------------------------------------------------
    #  API principal
    # ------------------------------------------------------------
    def run(self, data: Dict[str, float]) -> Dict[str, Any]:
        """
        Recebe um dicionário com escores brutos TEIQue (0–10)
        e devolve:
            - raw: valores originais
            - standardized: z-scores aproximados
            - percentiles: percentis estimados
            - metadata: informações do algoritmo
        """

        standardized = {}
        percentiles = {}

        for key, raw_value in data.items():
            norm = self.norm_tables.get(key)
            if not norm:
                continue

            z = self._to_z(raw_value, norm["mean"], norm["sd"])
            p = self._z_to_percentile(z)

            standardized[key] = round(z, 2)
            percentiles[key] = round(p, 1)

        return {
            "raw": data,
            "standardized": standardized,
            "percentiles": percentiles,
            "metadata": {
                "algorithm": "TeiqueNorms",
                "status": "active",
                "version": "1.0.0",
            },
        }

    # ------------------------------------------------------------
    #  Helpers
    # ------------------------------------------------------------
    @staticmethod
    def _to_z(value: float, mean: float, sd: float) -> float:
        if sd <= 0:
            return 0.0
        return (value - mean) / sd

    @staticmethod
    def _z_to_percentile(z: float) -> float:
        """
        Aproximação rápida de percentil a partir de z-score
        usando a CDF da normal padrão.
        """
        # fórmula de aproximação da CDF da normal
        return 50 * (1 + math.erf(z / math.sqrt(2))) * 2 - 50


if __name__ == "__main__":
    example = {
        "well_being": 6.8,
        "self_control": 5.4,
        "emotionality": 6.2,
        "sociability": 5.0,
        "global": 5.9,
    }

    engine = TeiqueNorms()
    out = engine.run(example)
    print(out)
