# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\ocai\ocai_norms.py
# Última atualização: 2025-12-11T09:59:20.698978

"""
OCAI Norms
Normaliza valores brutos do instrumento OCAI para a escala 0–100.
"""

from typing import Dict


class OCAINorms:
    """
    Converte valores brutos do questionário de cultura organizacional
    em uma escala padronizada usada pelo MindScan.
    """

    def __init__(self):
        self.version = "1.0"
        self.max_raw = 10.0  # exemplo genérico

    def normalize(self, raw_scores: Dict[str, float]) -> Dict[str, float]:
        normalized = {}

        for item, val in raw_scores.items():
            v = max(min(val, self.max_raw), 0)
            normalized[item] = (v / self.max_raw) * 100

        return normalized
