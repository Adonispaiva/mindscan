# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\esquemas\esquemas_norms.py
# Última atualização: 2025-12-11T09:59:20.683445

"""
Esquemas Norms
Converte pontuações brutas do questionário de Esquemas em escala 0–100.
"""

from typing import Dict


class EsquemasNorms:
    """
    Normaliza valores brutos para faixa padronizada usada pelo MindScan.
    """

    def __init__(self):
        self.version = "1.0"

        # Escores máximos usuais do instrumento base (valores genéricos)
        self.max_raw = 36.0

    def normalize(self, raw_scores: Dict[str, float]) -> Dict[str, float]:
        normalized = {}

        for item, value in raw_scores.items():
            base = max(min(value, self.max_raw), 0)
            normalized[item] = (base / self.max_raw) * 100

        return normalized
