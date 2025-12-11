# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\dass21\dass21_norms.py
# Última atualização: 2025-12-11T09:59:20.667799

"""
DASS-21 Norms
Normalização das pontuações do DASS-21 para a escala 0–100,
por subescala (Depressão, Ansiedade, Estresse).
"""

from typing import Dict


class Dass21Norms:
    """
    Responsável por aplicar normas e converter os escores brutos
    em uma métrica padronizada (0–100) usada pelo MindScan.
    """

    def __init__(self):
        self.version = "1.0"

        # Faixas brutas típicas DASS-21 (21 itens, escala 0–3)
        # Aqui usamos valores genéricos de referência para normalização.
        self.max_raw = {
            "depressao": 42.0,
            "ansiedade": 42.0,
            "estresse": 42.0,
        }

    def normalize(self, raw_scores: Dict[str, float]) -> Dict[str, float]:
        """
        Converte escores brutos em 0–100, por subescala.

        raw_scores:
            {
                "depressao": valor,
                "ansiedade": valor,
                "estresse": valor
            }
        """
        normalized: Dict[str, float] = {}

        for key, raw in raw_scores.items():
            max_val = self.max_raw.get(key, 42.0)
            if max_val <= 0:
                norm = 0.0
            else:
                norm = max(min((raw / max_val) * 100.0, 100.0), 0.0)

            normalized[key] = norm

        return normalized
