# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\dass21\dass21_dimensions.py
# Última atualização: 2025-12-11T09:59:20.652172

"""
DASS21 Dimensions — Versão ULTRA SUPERIOR
-------------------------------------------------------------

Converte pontuações numéricas em dimensões estruturadas:

- humor → (Depressão)
- tensão → (Ansiedade)
- carga mental → (Estresse)

Oferece descrições breves para engines superiores.
"""

from typing import Dict, Any


class DASS21Dimensions:
    def __init__(self):
        self.version = "2.0-ultra"

    def classify(self, value: float) -> str:
        if value < 30:
            return "baixo"
        if value < 60:
            return "moderado"
        return "alto"

    def describe(self, name: str, level: str) -> str:
        mapping = {
            ("depressao", "alto"): "Humor deprimido intenso com retração emocional.",
            ("depressao", "moderado"): "Indícios de humor deprimido e perda de energia.",
            ("ansiedade", "alto"): "Tensão elevada, hiperalerta e sensação de ameaça constante.",
            ("stress", "alto"): "Sobrecarga mental com risco de esgotamento.",
        }
        return mapping.get((name, level), "Nível dentro dos padrões esperados.")

    def run(self, scores: Dict[str, float]) -> Dict[str, Any]:
        output = {}
        for dim, value in scores.items():
            level = self.classify(value)
            output[dim] = {
                "value": value,
                "level": level,
                "description": self.describe(dim, level)
            }

        return {
            "module": "dass21_dimensions",
            "version": self.version,
            "dimensions": output
        }
